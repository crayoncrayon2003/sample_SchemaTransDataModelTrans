SELECT
    CAST("name" AS TEXT) AS ReNameName,
    CAST("address" AS TEXT) AS ReNameAddress,
    COALESCE(CAST("capacity" AS DOUBLE PRECISION), 0) AS ReNameCapacity,
    COALESCE(CAST("latitude" AS DOUBLE PRECISION), 0) AS ReNameLatitude,
    COALESCE(CAST("longitude" AS DOUBLE PRECISION), 0) AS ReNameLongitude
FROM tmpTable