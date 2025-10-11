CREATE DATABASE IF NOT EXISTS visualization_db;
USE visualization_db;

CREATE TABLE sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sales_amount DECIMAL(10,2),
    sales_date DATE,
    region VARCHAR(50)
);

CREATE TABLE user_behavior (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50),
    page_url VARCHAR(200),
    action_time DATETIME,
    duration INT
);

INSERT INTO sales_data (product_name, category, sales_amount, sales_date, region) VALUES
('iPhone 14', 'Electronics', 15000.00, '2024-01-15', 'North'),
('MacBook Pro', 'Electronics', 22000.00, '2024-01-16', 'East'),
('Coffee Machine', 'Home Appliances', 3000.00, '2024-01-17', 'South'),
('Office Chair', 'Furniture', 800.00, '2024-01-18', 'North'),
('Monitor', 'Electronics', 1200.00, '2024-01-19', 'East'),
('Smart Watch', 'Electronics', 2500.00, '2024-01-20', 'South'),
('Desk Lamp', 'Home Goods', 150.00, '2024-01-21', 'West');

INSERT INTO user_behavior (user_id, action_type, page_url, action_time, duration) VALUES
(1, 'View', '/home', '2024-01-15 10:00:00', 120),
(2, 'Click', '/products', '2024-01-15 11:30:00', 60),
(3, 'Purchase', '/checkout', '2024-01-16 14:20:00', 180),
(1, 'View', '/about', '2024-01-17 09:15:00', 90),
(2, 'Register', '/register', '2024-01-18 16:45:00', 150),
(4, 'View', '/products', '2024-01-19 13:20:00', 200),
(3, 'Click', '/home', '2024-01-20 15:30:00', 75);