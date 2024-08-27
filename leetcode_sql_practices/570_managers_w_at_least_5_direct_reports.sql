SELECT
    m.name
FROM
    Employee AS m
INNER JOIN
    Employee AS e
    ON e.managerId = m.id
GROUP BY
    m.id,
    m.name
HAVING
    COUNT(e.id) > 4




-- WITH Manager AS (
--     SELECT
--         m.name,
--         m.id,
--         COUNT(e.id) AS report_count
--     FROM
--         Employee AS m
--     INNER JOIN
--         Employee AS e
--         ON e.managerID = m.id
--     GROUP BY
--         m.name,
--         m.id
-- )
-- SELECT
--     name
-- FROM
--     Manager
-- WHERE
--     report_count > 4
