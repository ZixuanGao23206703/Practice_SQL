SELECT 
    s.user_id,
    ROUND(
        COALESCE( -- returns 1st non-NULL statement, if result of division is NULL, returns 0
            COUNT(CASE WHEN c.action = 'confirmed' THEN 1 END) * 1.0 /  -- result multiplied by 1.0 to convert to float, alternate: CAST((...) AS FLOAT), or CAST((...) AS DECIMAL(10,2))
            NULLIF(COUNT(CASE WHEN c.action IN ('confirmed', 'timeout') THEN 1 END), 0),  -- returns NULL if result of 1st statement is 0
            0
        ), 2
    ) AS confirmation_rate
FROM 
    Signups s
LEFT JOIN 
    Confirmations c ON s.user_id = c.user_id
GROUP BY 
    s.user_id;






-- WITH counts AS (
--     SELECT
--         s.user_id,
--         COUNT(CASE WHEN c.action='confirmed' THEN 1 END) AS confirmed,
--         COUNT(CASE WHEN c.action='timeout' THEN 1 END) AS timeout
--     FROM
--         Signups AS s
--     LEFT JOIN
--         Confirmations AS c
--         ON c.user_id = s.user_id
--     GROUP BY
--         s.user_id
-- )

-- SELECT
--     user_id,
--     CASE
--         WHEN confirmed+timeout = 0 THEN 0
--         ELSE ROUND(confirmed / (confirmed+timeout), 2)
--     END AS confirmation_rate
-- FROM
--     counts
