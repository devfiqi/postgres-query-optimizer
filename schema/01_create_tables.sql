-- Users table (will have 100k rows)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    country VARCHAR(50),
    is_premium BOOLEAN DEFAULT FALSE
);

-- Products table (will have 10k rows)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Orders table (will have 1M rows)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT NOW(),
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
);

-- Order items table (will have 5M rows)
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    price DECIMAL(10,2)
);