SELECT *
FROM Cinema
WHERE
    id % 2 = 1
    AND description NOT LIKE '%boring%'
    -- % is a wildcard, that represents zero or more characters. It can be used at the beginning, end, or both sides
    -- w/o '...' it will be treated as column name, not column value
ORDER BY rating DESC
