import os
import sqlite3
from urllib import response
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

# --- initial config ---
load_dotenv()

#loading environment variables. printing and selecting default if the variable is not found
STATION_ID = os.getenv("STATION_ID", "KGPH")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.weather.gov")
USER_AGENT = os.getenv("USER_AGENT", "(example_weather_app, contact@example.com)")
DB_PATH = os.getenv("DB_PATH", "db/weather_data.db")

# creates the directory for the database if it doesn't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# --- initialize the database ---
def init_db():
    '''this function initializes the database and creates the weather_data table if it doesn't exist already'''
    with sqlite3.connect(DB_PATH) as conn:
        #create table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                station_id TEXT,
                station_name TEXT,
                timezone TEXT,
                latitude REAL,
                longitude REAL,
                observation_timestamp TEXT,
                temperature REAL,
                wind_speed REAL,
                humidity REAL,
                PRIMARY KEY (station_id, observation_timestamp)
            );
        """)

# --- Fetch data ---
def fetch_data():
    '''this function fetches the station and observations data from the API'''
    headers = {"User-Agent": USER_AGENT}

    # station metadata
    url_station = f"{API_BASE_URL}/stations/{STATION_ID}"
    try:
        station = requests.get(url_station, headers=headers)
        station.raise_for_status()
        station_json = station.json()
    #handles errors
    except Exception as e:
        raise RuntimeError(f"Error fetching station info: {e}")

    # saving the timezone because it is not included in the observations
    station_timezone = station_json['properties']['timeZone']

    # observations
    url_obs = f"{API_BASE_URL}/stations/{STATION_ID}/observations"

    # avoids re-downloading data already present in the database.
    # uses the latest timestamp stored to fetch only new observations. (if any)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(observation_timestamp)
            FROM weather_data
            WHERE station_id = ?
        """, (STATION_ID,))
        result = cursor.fetchone()[0]
    if result:
        start_date = datetime.strptime(result, "%Y-%m-%dT%H:%M:%S")
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        #utcnow is deprecated but i'm keeping it for compatibility with more python versions
        start_date = datetime.utcnow() - timedelta(days=7)
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        response = requests.get(url_obs, headers=headers, params={"start": start_date_str})
        response.raise_for_status()
        observations = response.json().get("features", [])
    except Exception as e:
        raise RuntimeError(f"Error fetching observations: {e}")

    return station_json, observations, station_timezone

# --- cleaning data ---
def transform_data(station, features, timezone):
    if not features:
        print("No features found for selected station.")
        return pd.DataFrame()

    df = pd.json_normalize(features)

    columns_needed = [
        'properties.stationId',
        'properties.stationName',
        'properties.timestamp',
        'properties.temperature.value',
        'properties.windSpeed.value',
        'properties.relativeHumidity.value',
        'geometry.coordinates'
    ]

    df = df[columns_needed]
    df.columns = [
        'station_id',
        'station_name',
        'timestamp',
        'temperature',
        'wind_speed',
        'humidity',
        'coordinates'
    ]

    df['latitude'] = df['coordinates'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
    df['longitude'] = df['coordinates'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)
    df.drop(columns=['coordinates'], inplace=True)

    df['timezone'] = timezone

    # --- cleaning ---
    #cleaning timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(None)

    #rounding temperature, widn speed and humidity to 2 decimal places
    df['temperature'] = df['temperature'].astype(float).round(2)
    df['wind_speed'] = df['wind_speed'].astype(float).round(2)
    df['humidity'] = df['humidity'].astype(float).round(2)


    return df

# --- inserting data in db ---
def insert_data(df):
    if df.empty:
        print("No data to insert.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO weather_data (
                        station_id, station_name, timezone,
                        latitude, longitude, observation_timestamp,
                        temperature, wind_speed, humidity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.station_id,
                    row.station_name,
                    row.timezone,
                    row.latitude,
                    row.longitude,
                    row.timestamp.strftime('%Y-%m-%dT%H:%M:%S'), #because sqlite doesn't support datetime 
                    round(row.temperature, 2) if pd.notnull(row.temperature) else None,
                    round(row.wind_speed, 2) if pd.notnull(row.wind_speed) else None,
                    round(row.humidity, 2) if pd.notnull(row.humidity) else None
                ))
                if cursor.rowcount > 0: # means a new record was inserted
                    inserted += 1
            except sqlite3.IntegrityError:
                continue  # in case the record already exists
        conn.commit()
        print(f"{inserted} new records inserted")

# --- pipeline ---
def main():
    print("starting pipeline...")
    init_db()
    station, features, timezone = fetch_data()
    df = transform_data(station, features, timezone)
    insert_data(df)
    print("pipeline completed")

if __name__ == "__main__":
    main()