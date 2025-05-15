# 1.dbt
## Create New Project
```
mkdir project
cd project
dbt init

> Enter a name for your project (letters, digits, underscore): test_project
> The profile test already exists in /home/user/.dbt/profiles.yml. Continue and overwrite it? [y/N]: y
> Which database would you like to use?
> [1] duckdb
Enter a number: 1
```

project
├── logs/
└── test_project/
    ├── analyses/
    │   └── .gitkeep
    ├── macros/
    │   └── .gitkeep
    ├── models/
    │   └── example/
    │       ├── my_first_dbt_model.sql
    │       ├── my_second_dbt_model.sql
    │       └── schema.yml
    ├── seeds/
    │   └── .gitkeep
    ├── snapshots/
    │   └── .gitkeep
    ├── tests/
    │   └── .gitkeep
    ├── .gitkeep
    ├── dbt_project.yml
    └── README.md

## remove example
```
rm -R models/example
```

## modify dbt_project.yml
./project/test_project/dbt_project.yml

delete following
```
models:
  test_project:
    # Config indicated by + and applies to all files under models/example/
    example:
      +materialized: view
```

add following
```
models:
  csv_transformations:
    +materialized: table
```

## create profiles.yml
./project/test_project/profiles.yml

```
test_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      threads: 1
      path: ./duckdb/database.duckdb
      database: database
```

## create dir
./project/test_project/duckdb

## create sample data
./project/test_project/seeds/csv_format_1.csv

```
id,name,created_at
1,Alice,2024-01-01 00:00:00
2,Bob,2024-01-02 00:00:00
3,Charlie,2024-01-03 00:00:00
```


./project/test_project/seeds/csv_format_2.csv
```
id,name,created_at
1,Alice,2024-01-01
2,Bob,2024-01-02
3,Charlie,2024-01-03
```

## create macros
./project/test_project/macros/generate_sql.sql
```
{% macro generate_sql(input_csv_path, columns) %}
SELECT
{% for col in columns %}
    {{ col.name }} AS {{ col.alias }}{% if not loop.last %},{% endif %}
{% endfor %}
FROM read_csv_auto('{{ input_csv_path }}')
{% endmacro %}
```

## create models
./project/test_project/models/csv_format_1_transformation.sql
```
{% set columns = [
    {"name": "id", "alias": "id"},
    {"name": "name", "alias": "value"},
    {"name": "created_at", "alias": "timestamp"}
] %}

{{ generate_sql("./seeds/csv_format_1.csv", columns) }}
```


./project/test_project/models/csv_format_1_transformation.sql
```
{% set columns = [
    {"name": "id", "alias": "id"},
    {"name": "name", "alias": "value"},
    {"name": "created_at", "alias": "timestamp"}
] %}

{{ generate_sql("./seeds/csv_format_2.csv", columns) }}
```

## build
```
cd ./project/test_project

# confirm connection based on profiles.yml
dbt debug

# load seed
dbt seed

# create model
dbt run
```

## Note
If you get a build error,
```
dbt clean
```

```
rm ./project/test_project/dev.duckdb
```


# 2. How to use
```
pip install dbt-core dbt-duckdb duckdb pandas ray
```

./sample2.py
```
import duckdb
con = duckdb.connect('path/to/your.duckdb')
result = con.execute("SELECT * FROM main.csv_to_ngsi_model").fetchall()
```