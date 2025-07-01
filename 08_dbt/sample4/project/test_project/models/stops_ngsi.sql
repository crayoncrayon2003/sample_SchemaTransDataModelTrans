SELECT
  stop_id AS id,
  'Station' AS type,
  stop_name AS stopName,
  JSON_OBJECT(
    'type', 'Point',
    'coordinates', JSON_ARRAY(stop_lon, stop_lat)
  ) AS location
FROM {{ ref('stops') }}
WHERE stop_lat IS NOT NULL AND stop_lon IS NOT NULL