COPY store_records(row_id, order_id, order_date, ship_date, ship_mode,
       customer_id, customer_name, segment, country, city, state,
       postal_code, region, product_id, category, sub_category,
       product_name, sales, quantity, discount, profit)
       FROM '/Users/Filepath/sample_superstore_updated.csv' DELIMITER ',' CSV HEADER;

