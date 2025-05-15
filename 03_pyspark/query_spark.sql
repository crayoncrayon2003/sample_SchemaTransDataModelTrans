SELECT
    CONCAT('urn:ngsi-ld:', ROW_NUMBER() OVER (ORDER BY `name`)) AS id,
    'test' AS type,
    STRUCT(`name`      AS value, 'Text' AS type) AS name,
    STRUCT(`address`   AS value, 'Text' AS type) AS address,
    STRUCT(`capacity`  AS value, 'Number' AS type) AS capacity,
    STRUCT(`latitude`  AS value, 'Number' AS type) AS latitude,
    STRUCT(`longitude` AS value, 'Number' AS type) AS longitude
FROM recode;
