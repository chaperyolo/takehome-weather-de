WITH ordered AS (
    SELECT 
        station_id,
        observation_timestamp,
        wind_speed,
        LAG(wind_speed) OVER (
            PARTITION BY station_id 
            ORDER BY observation_timestamp
        ) AS previous_wind_speed
    FROM 
        weather_data
    WHERE 
        DATE(observation_timestamp) >= DATE('now', '-7 days')
),
diffs AS (
    SELECT 
        station_id,
        ABS(wind_speed - previous_wind_speed) AS wind_diff
    FROM 
        ordered
    WHERE 
        wind_speed IS NOT NULL AND previous_wind_speed IS NOT NULL
)
SELECT 
    station_id,
    MAX(wind_diff) AS max_wind_speed_change
FROM 
    diffs
GROUP BY 
    station_id;