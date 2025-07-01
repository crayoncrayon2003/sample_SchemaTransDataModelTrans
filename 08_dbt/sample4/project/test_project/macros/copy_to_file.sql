{% macro copy_to_file(relation, path, format='csv') %}
    {% set sql %}
        COPY {{ relation }} TO '{{ path }}' (FORMAT {{ format }});
    {% endset %}
    {{ log("Running: " ~ sql, info=True) }}
    {% do run_query(sql) %}
{% endmacro %}