CREATE TABLE store_records (
    id SERIAL PRIMARY KEY,
    row_id INT,
    order_id INT,
    order_date VARCHAR(10), 
    ship_date VARCHAR(10),
    ship_mode VARCHAR(25),
    customer_id VARCHAR(20),
    customer_name VARCHAR(50),
    segment VARCHAR(25),
    country VARCHAR(25),
    city VARCHAR(30),
    state VARCHAR(25),
    postal_code INT,
    region VARCHAR(25),
    product_id VARCHAR(30),
    category VARCHAR(30)
    subcategory VARCHAR(30),
    product_name VARCHAR(70),
    sales FLOAT,
    quantity INT,
    discount FLOAT,
    profit FLOAT
);