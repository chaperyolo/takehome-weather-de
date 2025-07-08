SELECT 
    station_id,
    AVG(temperature) AS avg_temperature
FROM 
    weather_data
WHERE 
    DATE(observation_timestamp) >= DATE('now', 'weekday 1', '-7 days')
    AND DATE(observation_timestamp) <= DATE('now', 'weekday 0')
GROUP BY 
    station_id;