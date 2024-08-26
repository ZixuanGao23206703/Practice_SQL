import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
conn = sqlite3.connect('car_sales.db')
cursor = conn.cursor()

# Create tables using the cursor
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cars (
    car_id INTEGER PRIMARY KEY,
    make TEXT,
    model TEXT,
    year INTEGER,
    price REAL,
    category TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    region_id INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY,
    car_id INTEGER,
    customer_id INTEGER,
    sale_date TEXT,
    price REAL,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT
)
''')

# Sample data for Cars
cars_data = [
    (1, 'Toyota', 'Camry', 2020, 24000, 'Sedan'),
    (2, 'Honda', 'Accord', 2019, 22000, 'Sedan'),
    (3, 'Ford', 'Mustang', 2018, 26000, 'Coupe'),
    (4, 'BMW', 'X5', 2021, 55000, 'SUV')
]

# Sample data for Customers
customers_data = [
    (1, 'John', 'Doe', 'john.doe@example.com', 1),
    (2, 'Jane', 'Smith', 'jane.smith@example.com', 2),
    (3, 'Mike', 'Brown', 'mike.brown@example.com', 3),
    (4, 'Anna', 'Davis', 'anna.davis@example.com', 4)
]

# Sample data for Sales
sales_data = [
    (1, 1, 1, '2024-08-01', 24000),
    (2, 2, 2, '2024-08-03', 22000),
    (3, 3, 3, '2024-08-10', 26000),
    (4, 4, 4, '2024-08-12', 55000)
]

# Sample data for Regions
regions_data = [
    (1, 'North'),
    (2, 'South'),
    (3, 'East'),
    (4, 'West')
]

# Insert data into tables using cursor
cursor.executemany('INSERT OR IGNORE INTO Cars VALUES (?, ?, ?, ?, ?, ?)', cars_data)
cursor.executemany('INSERT OR IGNORE INTO Customers VALUES (?, ?, ?, ?, ?)', customers_data)
cursor.executemany('INSERT OR IGNORE INTO Sales VALUES (?, ?, ?, ?, ?)', sales_data)
cursor.executemany('INSERT OR IGNORE INTO Regions VALUES (?, ?)', regions_data)

# Commit the changes
conn.commit()

# Conduct analysis

# 1. Top Selling Car Models
query = '''
SELECT c.make, c.model, COUNT(s.sale_id) as total_sales
FROM Sales s
JOIN Cars c ON s.car_id = c.car_id
GROUP BY c.make, c.model
ORDER BY total_sales DESC
'''
top_selling_models = pd.read_sql_query(query, conn)
print("Top Selling Car Models:")
print(top_selling_models)

# 2. Sales Performance by Region
query = '''
SELECT r.region_name, SUM(s.price) as total_sales
FROM Sales s
JOIN Customers cu ON s.customer_id = cu.customer_id
JOIN Regions r ON cu.region_id = r.region_id
GROUP BY r.region_name
ORDER BY total_sales DESC
'''
sales_by_region = pd.read_sql_query(query, conn)
print("\nSales Performance by Region:")
print(sales_by_region)

# 3. Customer Spending Analysis
query = '''
SELECT cu.first_name || ' ' || cu.last_name AS customer_name, SUM(s.price) AS total_spent
FROM Sales s
JOIN Customers cu ON s.customer_id = cu.customer_id
GROUP BY customer_name
ORDER BY total_spent DESC
'''
customer_spending = pd.read_sql_query(query, conn)
print("\nCustomer Spending Analysis:")
print(customer_spending)

# Visualization

# Top Selling Models Bar Chart
sns.barplot(x='model', y='total_sales', data=top_selling_models)
plt.title('Top Selling Car Models')
plt.show()

# Sales by Region Pie Chart
sales_by_region.plot.pie(y='total_sales', labels=sales_by_region['region_name'], autopct='%1.1f%%')
plt.title('Sales Distribution by Region')
plt.show()

# Customer Spending Histogram
sns.histplot(customer_spending['total_spent'], bins=10)
plt.title('Customer Spending Distribution')
plt.show()

# Close the database connection
conn.close()
