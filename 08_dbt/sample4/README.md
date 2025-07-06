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

## get duckdb
```
wget https://github.com/duckdb/duckdb/releases/download/v1.3.1/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
chmod +x duckdb
rm duckdb_cli-linux-amd64.zip
```

## modify dbt_project.yml
./project/test_project/dbt_project.yml

### edit1
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
  test_project:
    +materialized: view
```

### edit2
add following
```
seeds:
  test_project:
    agency:
      +column_types:
        agency_id: VARCHAR(255)
        agency_name: VARCHAR(255)
        agency_url: VARCHAR(255)
        agency_timezone: VARCHAR(255)
        agency_lang: VARCHAR(255)
        agency_phone: VARCHAR(255)
        agency_fare_url: VARCHAR(255)
        agency_email: VARCHAR(255)
    stops:
      +column_types:
        stop_id: VARCHAR(255)
        stop_code: VARCHAR(255)
        stop_name: VARCHAR(255)
        stop_desc: VARCHAR(255)
        stop_lat: DOUBLE
        stop_lon: DOUBLE
        zone_id: VARCHAR(255)
        stop_url: VARCHAR(255)
        location_type: INTEGER
        parent_station: VARCHAR(255)
        stop_timezone: VARCHAR(255)
        wheelchair_boarding: INTEGER
        level_id: VARCHAR(255)
        platform_code: VARCHAR(255)
    routes:
      +column_types:
        route_id: VARCHAR(255)
        agency_id: VARCHAR(255)
        route_short_name: VARCHAR(255)
        route_long_name: VARCHAR(255)
        route_desc: VARCHAR(255)
        route_type: INTEGER
        route_url: VARCHAR(255)
        route_color: VARCHAR(255)
        route_text_color: VARCHAR(255)
    trips:
      +column_types:
        trip_id: VARCHAR(255)
        route_id: VARCHAR(255)
        service_id: VARCHAR(255)
        trip_headsign: VARCHAR(255)
        trip_short_name: VARCHAR(255)
        direction_id: INTEGER
        block_id: VARCHAR(255)
        shape_id: VARCHAR(255)
        wheelchair_accessible: INTEGER
        bikes_allowed: INTEGER
    stop_times:
      +column_types:
        trip_id: VARCHAR(255)
        arrival_time: TIME
        departure_time: TIME
        stop_id: VARCHAR(255)
        stop_sequence: INTEGER
        stop_headsign: VARCHAR(255)
        pickup_type: INTEGER
        drop_off_type: INTEGER
        shape_dist_traveled: DOUBLE
        timepoint: INTEGER
    calendar:
      +column_types:
        service_id: VARCHAR(255)
        monday: INTEGER
        tuesday: INTEGER
        wednesday: INTEGER
        thursday: INTEGER
        friday: INTEGER
        saturday: INTEGER
        sunday: INTEGER
        start_date: VARCHAR(255) # DATE
        end_date: VARCHAR(255) # DATE
    calendar_dates:
      +column_types:
        service_id: VARCHAR(255)
        date: VARCHAR(255) # DATE
        exception_type: INTEGER
    fare_attributes:
      +column_types:
        fare_id: VARCHAR(255)
        price: DOUBLE
        currency_type: VARCHAR(255)
        payment_method: INTEGER
        transfers: INTEGER
        agency_id: VARCHAR(255)
        transfer_duration: BIGINT
    fare_rules:
      +column_types:
        fare_id: VARCHAR(255)
        route_id: VARCHAR(255)
        origin_id: VARCHAR(255)
        destination_id: VARCHAR(255)
        contains_id: VARCHAR(255)
    shapes:
      +column_types:
        shape_id: VARCHAR(255)
        shape_pt_lat: DOUBLE
        shape_pt_lon: DOUBLE
        shape_pt_sequence: INTEGER
        shape_dist_traveled: DOUBLE
    frequencies:
      +column_types:
        trip_id: VARCHAR(255)
        start_time: TIME
        end_time: TIME
        headway_secs: INTEGER
        exact_times: INTEGER
    transfers:
      +column_types:
        from_stop_id: VARCHAR(255)
        to_stop_id: VARCHAR(255)
        transfer_type: INTEGER
        min_transfer_time: INTEGER
    pathways:
      +column_types:
        pathway_id: VARCHAR(255)
        from_stop_id: VARCHAR(255)
        to_stop_id: VARCHAR(255)
        pathway_mode: INTEGER
        is_bidirectional: INTEGER
        length: DOUBLE
        traversal_time: INTEGER
        stair_count: INTEGER
        max_slope: DOUBLE
        min_width: DOUBLE
        signposted_as: VARCHAR(255)
        reversed_signposted_as: VARCHAR(255)
    levels:
      +column_types:
        level_id: VARCHAR(255)
        level_index: DOUBLE
        level_name: VARCHAR(255)
    agency_jp:
      +column_types:
        agency_id: VARCHAR(255)
        agency_postal: VARCHAR(255)
        agency_address: VARCHAR(255)
    jp_offices:
      +column_types:
        office_id: VARCHAR(255)
        office_name: VARCHAR(255)
        office_url: VARCHAR(255)
        office_phone: VARCHAR(255)
        office_address: VARCHAR(255)
    jp_lines:
      +column_types:
        line_id: VARCHAR(255)
        line_code: VARCHAR(255)
        line_symbol: VARCHAR(255)
        line_name: VARCHAR(255)
        line_color: VARCHAR(255)
        line_sort_order: INTEGER
    jp_operators:
      +column_types:
        operator_id: VARCHAR(255)
        operator_name: VARCHAR(255)
        operator_url: VARCHAR(255)
        operator_phone: VARCHAR(255)
        operator_address: VARCHAR(255)
    jp_stop_offices:
      +column_types:
        stop_id: VARCHAR(255)
        office_id: VARCHAR(255)
    jp_route_lines:
      +column_types:
        route_id: VARCHAR(255)
        line_id: VARCHAR(255)
    translations:
      +column_types:
        table_name: VARCHAR(255)
        field_name: VARCHAR(255)
        language: VARCHAR(255)
        translation: VARCHAR(255)
        record_id: VARCHAR(255)
    feed_info:
      +column_types:
        feed_publisher_name: VARCHAR(255)
        feed_publisher_url: VARCHAR(255)
        feed_lang: VARCHAR(255)
        feed_start_date: DATE
        feed_end_date: DATE
        feed_version: VARCHAR(255)
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
      path: ./db/database.duckdb
      database: database
      extensions:
      - json
      - spatial
```

## create dir
mkdir ./db


## create sample data
```
cd ./project/test_project/seeds
wget https://api.gtfs-data.jp/v2/organizations/kokacity/feeds/sinaicommunitybus/files/feed.zip
unzip feed.zip -d ./
rm feed.zip

for f in *.txt; do mv -- "$f" "${f%.txt}.csv"; done
```

## create macros
./project/test_project/macros/copy_to_file.sql

```
{% macro copy_to_file(relation, path, format='csv') %}
    {% set sql %}
        COPY {{ relation }} TO '{{ path }}' (FORMAT {{ format }});
    {% endset %}
    {{ log("Running: " ~ sql, info=True) }}
    {% do run_query(sql) %}
{% endmacro %}
```

## create models

./project/test_project/models/stops_ngsi.sql
```
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
```


./project/test_project/models/trips_ngsi.sql
```
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
```


./project/test_project/models/routes_ngsi.sql
```
with stops_ordered as (
    select
        stop_id,
        stop_lon,
        stop_lat,
        stop_sequence,
        trip_id
    from {{ ref('stop_times') }} st
    join {{ ref('stops') }} s on st.stop_id = s.stop_id
),

routes_geojson as (
    select
        route_id,
        '{ "type": "Feature", "geometry": { "type": "LineString", "coordinates": [' ||
        string_agg('[' || CAST(stop_lon AS varchar) || ',' || CAST(stop_lat AS varchar) || ']', ',') ||
        ']}, "properties": { "route_id": "' || route_id || '" } }' as geojson
    from (
        select
            r.route_id,
            s.stop_lon,
            s.stop_lat,
            st.stop_sequence
        from {{ ref('routes') }} r
        join {{ ref('trips') }} t on t.route_id = r.route_id
        join {{ ref('stop_times') }} st on st.trip_id = t.trip_id
        join {{ ref('stops') }} s on s.stop_id = st.stop_id
        where t.trip_id = (
            select trip_id from {{ ref('trips') }} where route_id = r.route_id limit 1
        )
        order by r.route_id, st.stop_sequence
    ) as ordered_points
    group by route_id
)

select
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    r.route_type,
    g.geojson as location
from {{ ref('routes') }} r
left join routes_geojson g on r.route_id = g.route_id

```


./project/test_project/models/schema.yml
```
version: 2

models:
  - name: stops_ngsi
    description: "GTFS stops を NGSIv2形式に変換"
    columns:
      - name: id
        tests: [not_null]
      - name: location
        description: "GeoJSON形式のPoint"

  - name: trips_ngsi
    description: "GTFS trips を NGSIv2形式に変換"
    columns:
      - name: id
        tests: [not_null]
      - name: location
        description: "出発停留所のGeoJSON Point"

  - name: routes_ngsi
    description: "GTFS routes を NGSIv2形式に変換（LineString）"
    columns:
      - name: id
        tests: [not_null]
      - name: location
        description: "GeoJSON LineString（ルート全体）"
```

## build
cd ./project/test_project

### confirm connection based on profiles.yml
```
dbt debug
```

### load seed
```
dbt seed --profiles-dir ./
```

### create model
```
dbt run
```

### output file
```
mkdir -p output
```

```
dbt run-operation copy_to_file --args '{"relation": "stops_ngsi", "path": "output/stops_ngsi.json", "format": "json"}'
dbt run-operation copy_to_file --args '{"relation": "routes_ngsi", "path": "output/routes_ngsi.json", "format": "json"}'
dbt run-operation copy_to_file --args '{"relation": "trips_ngsi", "path": "output/trips_ngsi.json", "format": "json"}'
```


## Note
If you get a build error,
```
dbt clean
rm -rf target/
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