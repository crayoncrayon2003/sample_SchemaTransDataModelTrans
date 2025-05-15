{% macro generate_ngsi_sql(ref_name) %}
WITH numbered AS (
  SELECT
    'urn:ngsi-ld:csv:' || LPAD(CAST(ROW_NUMBER() OVER (ORDER BY name) AS VARCHAR), 3, '0') AS id,
    name,
    created_at
  FROM {{ ref(ref_name) }}
)

SELECT json_group_array(
  json_object(
    'id', id,
    'type', 'sampletype',
    'name', json_object('value', name, 'type', 'Text'),
    'created_at', json_object('value', created_at, 'type', 'DateTime')
  )
) AS json_result
FROM numbered
{% endmacro %}
