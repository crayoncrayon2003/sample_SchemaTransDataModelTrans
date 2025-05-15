SELECT
    'urn:ngsi-ld:' || COALESCE(CAST(name AS VARCHAR), 'null') AS id,
    'test' AS type,
    json_object('value', COALESCE(name,      NULL), 'type', 'Text') AS name,
    json_object('value', COALESCE(address,   NULL), 'type', 'Text') AS address,
    json_object('value', COALESCE(capacity,  NULL), 'type', 'Number') AS capacity,
    json_object('value', COALESCE(latitude,  NULL), 'type', 'Number') AS latitude,
    json_object('value', COALESCE(longitude, NULL), 'type', 'Number') AS longitude,
FROM df;
