-- Method 1: using INNER JOIN (joining the activity table with itself)
SELECT
    S.machine_id,
    ROUND(AVG(E.timestamp - S.timestamp), 3) AS processing_time
FROM
    Activity AS S -- Start time table
INNER JOIN
    Activity AS E -- End time table
    ON S.machine_id = E.machine_id
    AND S.process_id = E.process_id
    AND S.activity_type = 'start'
    AND E.activity_type = 'end'
GROUP BY
    S.machine_id

-- Method 2: using a temporary table (faster)
-- WITH PairedEvents AS (
--     SELECT
--         machine_id,
--         process_id,
--         MIN(CASE WHEN activity_type = 'start' THEN timestamp END) AS start_time,
--         MIN(CASE WHEN activity_type = 'end' THEN timestamp END) AS end_time
--     FROM
--         Activity
--     GROUP BY
--         machine_id,
--         process_id
-- )
-- SELECT
--     machine_id,
--     ROUND(AVG(end_time - start_time), 3) AS processing_time
-- FROM
--     PairedEvents
-- GROUP BY
--     machine_id;
