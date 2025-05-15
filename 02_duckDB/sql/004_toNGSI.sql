SELECT json_group_array(
    json_object(
        'id', entityid,
        'type', entitytype,
        'ReNameName', json_object('value', ReNameName, 'type', 'Text'),
        'ReNameAddress', json_object('value', ReNameAddress, 'type', 'Text'),
        'ReNameCapacity', json_object('value', ReNameCapacity, 'type', 'Number'),
        'location', json_object(
            'type', 'geo:json',
            'value', json_object(
                'type', 'Point',
                'coordinates', [ReNameLongitude, ReNameLatitude]
            )
        )
    )
) AS json_result
FROM tmpTable