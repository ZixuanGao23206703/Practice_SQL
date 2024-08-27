SELECT
    p.product_id,
    COALESCE( -- if result of division is NULL (dividing by zero), then return 0
        ROUND(
            SUM(
                CASE 
                WHEN (s.purchase_date >= p.start_date) 
                    AND (s.purchase_date <= p.end_date)
                THEN p.price * s.units
                END
            ) / 
            SUM(
                CASE 
                WHEN (s.purchase_date >= p.start_date) 
                    AND (s.purchase_date <= p.end_date)
                THEN s.units
                END        
            ), 2
        ), 0
    ) AS average_price
FROM 
    Prices AS p
LEFT JOIN 
    UnitsSold AS s
    ON p.product_id = s.product_id
GROUP BY
    p.product_id




-- Better solution
-- SELECT 
--     p.product_id, 
--     IFNULL(
--         ROUND(
--             SUM(units*price)/SUM(units),2
--         ),0
--     ) AS average_price
-- FROM 
--     Prices p 
-- LEFT JOIN 
--     UnitsSold u
--     ON p.product_id = u.product_id 
--     AND u.purchase_date BETWEEN start_date AND end_date
-- GROUP BY 
--     product_id
