/* Question: category of most sold products (rank top 5) */
SELECT category, SUM(quantity) FROM store_records GROUP BY category ORDER BY sum DESC LIMIT 3;

/* Question: top 5 list of products that generate the most profit */
SELECT SUM(profit), product_id, product_name FROM store_records GROUP BY product_id, product_name ORDER BY sum DESC LIMIT 5;

/* Question: top 5 list of products that generate the least profit*/
SELECT SUM(profit), product_id, product_name FROM store_records GROUP BY product_id, product_name ORDER BY sum ASC LIMIT 5;