SELECT
  t.trip_id AS id,
  'Trip' AS type,
  t.trip_headsign AS tripHeadSign,
  JSON_OBJECT(
    'type', 'Point',
    'coordinates', JSON_ARRAY(s.stop_lon, s.stop_lat)
  ) AS location
FROM {{ ref('trips') }} t
LEFT JOIN {{ ref('stop_times') }} st ON t.trip_id = st.trip_id AND st.stop_sequence = 1
LEFT JOIN {{ ref('stops') }} s ON st.stop_id = s.stop_id
WHERE s.stop_lat IS NOT NULL AND s.stop_lon IS NOT NULL