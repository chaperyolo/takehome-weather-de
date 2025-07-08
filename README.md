# Data Engineer - Take Home Assignment
This is a take-home assignment for the Data Engineer position, completed by **Javier Navarro Véliz**.

## Project Overview

The goal of this project is to extract, transform, and store weather data from the [weather.gov API](https://www.weather.gov/documentation/services-web-api), and then run analytical queries on the data using SQL.

## How to run

### 1. Clone the repository
```bash
git clone https://github.com/chaperyolo/takehome-weather-de
cd takehome-weather-de
```

### 2. Set up your environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Duplicate the example file and edit it as needed

```bash
cp .env.example .env
```

Or create your own .env file with the following structure:

```env
STATION_ID=KGPH
API_BASE_URL=https://api.weather.gov
USER_AGENT=(example_weather_app, contact@example.com)
DB_PATH=db/weather_data.db
QUERIES_DIR=queries
```

### 4. Run the pipeline

```bash
python3 main.py
```

This will:
- Create a local SQLite database
- Fetch data from the past 7 days (or from the last record onwards on the next runs)
- Insert new observations while avoiding duplicates

### 5. Run the SQL queries

```bash
python3 run_queries.py
```
This script executes all .sql queries inside the queries/ folder and prints the results.


## Environment Variables

The following variables should be defined in your `.env` file:

| Variable       | Default (if not provided)                     |
|----------------|-----------------------------------------------|
| `STATION_ID`   | `KGPH`                                        |
| `API_BASE_URL` | `https://api.weather.gov`                     |
| `USER_AGENT`   | `(example_weather_app, contact@example.com)`  |
| `DB_PATH`      | `db/weather_data.db`                          |

If any of these are not provided, the script will fall back to the default values above without throwing an error.