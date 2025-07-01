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