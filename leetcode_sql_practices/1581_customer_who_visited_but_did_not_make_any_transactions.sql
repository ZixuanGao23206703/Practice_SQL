-- SELECT
--     V.customer_id,
--     COUNT(*) AS count_no_trans
-- FROM
--     Visits AS V
-- WHERE 
--     V.visit_id NOT IN (SELECT visit_id FROM Transactions)
-- GROUP BY
--     V.customer_id

SELECT
    V.customer_id,
    COUNT(V.visit_id) AS count_no_trans 
FROM
    Visits AS V
LEFT JOIN
    Transactions AS T
    ON V.visit_id = T.visit_id  
WHERE
    T.transaction_id IS NULL 
GROUP BY
    V.customer_id; 
