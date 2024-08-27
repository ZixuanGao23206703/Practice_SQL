WITH MinEventDates AS (
    SELECT player_id, MIN(event_date) AS min_event_date
    FROM Activity
    GROUP BY player_id
)

SELECT
    ROUND(
        COUNT(
            CASE
                WHEN a.event_date = min_event_date + INTERVAL 1 DAY
                THEN 1
                ELSE NULL
            END) /
        COUNT(DISTINCT a.player_id), 2
    ) AS fraction
FROM Activity AS a
JOIN MinEventDates AS m
    ON m.player_id = a.player_id













-- Correct, but inefficient version (time limit exceeded)
-- SELECT
--     ROUND(
--         COUNT(
--             CASE
--                 WHEN event_date = (
--                     SELECT MIN(event_date) + INTERVAL 1 DAY
--                     FROM Activity AS sub
--                     WHERE sub.player_id = Activity.player_id
--                 ) THEN 1
--                 ELSE NULL
--             END
--         ) /
--         COUNT(DISTINCT player_id), 2
--     ) AS fraction
-- FROM Activity
