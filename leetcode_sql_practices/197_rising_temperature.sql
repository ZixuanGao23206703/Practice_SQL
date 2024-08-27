SELECT
    Current.id
FROM
    Weather AS Current
LEFT JOIN
    Weather AS Previous
    ON Previous.recordDate = (
        SELECT recordDate
        FROM Weather
        WHERE recordDate < Current.recordDate
        AND DATEDIFF(Current.recordDate, recordDate) = 1
        )
WHERE
    Previous.temperature IS NOT NULL
    AND Previous.temperature < Current.temperature
