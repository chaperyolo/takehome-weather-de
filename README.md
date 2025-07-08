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

| Variable       | Description                | Default (if not provided)                     |
|----------------|----------------------------|-----------------------------------------------|
| `STATION_ID`   |NOAA station ID             | `KGPH`                                        |
| `API_BASE_URL` |Base URL of the weather API | `https://api.weather.gov`                     |
| `USER_AGENT`   |Required for API access     | `(example_weather_app, contact@example.com)`  |
| `DB_PATH`      |SQLite DB location          | `db/weather_data.db`                          |
| `QUERIES_DIR`  |Folder with .sql queries    | `queries`                                     |

If any of these are not provided, the script will fall back to the default values above without throwing an error.

## Notes & Assumptions
- The pipeline avoids inserting duplicate records using `INSERT OR IGNORE`.
- If data already exists in the database, the script fetches only newer observations.
- Date filtering is based on the observation_timestamp column.
- Important: One of the queries computes weekly metrics starting from last Monday.
Because the pipeline only fetches the last 7 days of data, if the script is run for the first time mid-week (e.g., Wednesday), there may not be enough historical data to cover the full week (Monday and Tuesday would be missing).
This design choice follows the assignment’s instruction to fetch only 7 days of data.
- Creating an index on observation_timestamp in the `weather_data` table may improve performance for larger datasets (not included in this version for simplicity).

## Compatibility

This project has been tested with the following Python versions:

- Python 3.9
- Python 3.10
- Python 3.12

Other versions may work, but these are the ones confirmed to be compatible.