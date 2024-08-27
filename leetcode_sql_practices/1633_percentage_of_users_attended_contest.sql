SELECT
    r.contest_id,
    ROUND(COUNT(r.user_id) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage
FROM
    Register AS r
GROUP BY
    r.contest_id
ORDER BY
    percentage DESC,
    r.contest_id ASC;






-- WITH TotalUsers AS (
--     SELECT COUNT(*) AS total_users
--     FROM Users
-- )

-- SELECT
--     r.contest_id,
--     COALESCE(
--         ROUND(
--             COUNT(r.contest_id)*100/
--             tu.total_users, 
--             2), 
--         0) AS percentage
-- FROM
--     Register AS r
-- CROSS JOIN
--     TotalUsers AS tu
-- LEFT JOIN
--     Users AS u
--     ON u.user_id = r.user_id
-- GROUP BY
--     r.contest_id
-- ORDER BY
--     percentage DESC,
--     r.contest_id ASC
