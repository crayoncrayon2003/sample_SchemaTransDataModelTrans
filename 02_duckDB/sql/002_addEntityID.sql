SELECT *,
        'urn:ngsi-ld:csv:' || LPAD(CAST(ROW_NUMBER() OVER (ORDER BY ReNameName) AS VARCHAR), 3, '0') AS entityid
FROM tmpTable