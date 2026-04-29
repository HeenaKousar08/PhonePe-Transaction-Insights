#Top States by Transaction Amount
SELECT state, SUM(amount) as total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;

#Category Performance
SELECT category, SUM(amount) as total
FROM aggregated_transaction
GROUP BY category
ORDER BY total DESC;

#Yearly Trend
SELECT year, SUM(amount) as yearly_total
FROM aggregated_transaction
GROUP BY year;