DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    state CHAR(2),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    cost NUMERIC(10,2) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    state CHAR(2),
    region VARCHAR(50)
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    discount NUMERIC(10,2) DEFAULT 0,
    payment_method VARCHAR(50),
    sale_timestamp TIMESTAMP NOT NULL,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);