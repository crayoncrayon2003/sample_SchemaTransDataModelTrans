{% macro copy_to_file(table_name, file_path, format='csv') %}
    {% if format | lower == 'csv' %}
        {% set sql %}
            COPY {{ table_name }} TO '{{ file_path }}' (FORMAT CSV, HEADER TRUE, DELIMITER ',');
        {% endset %}
    {% elif format | lower == 'json' %}
        {% set sql %}
            COPY {{ table_name }} TO '{{ file_path }}' (FORMAT JSON);
        {% endset %}
    {% else %}
        {{ exceptions.raise_compiler_error("Unsupported format: " ~ format) }}
    {% endif %}
    {% do run_query(sql) %}
{% endmacro %}
