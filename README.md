# Data Engineer - Take Home Assignment
This is a take-home assignment for the Data Engineer position, completed by **Javier Navarro Véliz**.

## Project Overview

The goal of this project is to extract, transform, and store weather data from the [weather.gov API](https://www.weather.gov/documentation/services-web-api), and then run analytical queries on the data using SQL.

## How to run

## Environment Variables

The following variables should be defined in your `.env` file:

| Variable       | Default (if not provided)                     |
|----------------|-----------------------------------------------|
| `STATION_ID`   | `KGPH`                                        |
| `API_BASE_URL` | `https://api.weather.gov`                     |
| `USER_AGENT`   | `(example_weather_app, contact@example.com)`  |
| `DB_PATH`      | `db/weather_data.db`                          |

If any of these are not provided, the script will fall back to the default values above without throwing an error.