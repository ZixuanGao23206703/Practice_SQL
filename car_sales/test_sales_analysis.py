import unittest
import sqlite3
import pandas as pd

class TestCarSalesAnalysis(unittest.TestCase):

    def setUp(self):
        # Set up a temporary in-memory database for testing
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Create tables for testing
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cars (
            car_id INTEGER PRIMARY KEY,
            make TEXT,
            model TEXT,
            year INTEGER,
            price REAL,
            category TEXT
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            region_id INTEGER
        )
        ''')
        self.cursor.execute('''
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
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Regions (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT
        )
        ''')

        # Insert sample data into tables
        self.cursor.executemany('INSERT INTO Cars VALUES (?, ?, ?, ?, ?, ?)', [
            (1, 'Toyota', 'Camry', 2020, 24000, 'Sedan'),
            (2, 'Honda', 'Accord', 2019, 22000, 'Sedan'),
            (3, 'Ford', 'Mustang', 2018, 26000, 'Coupe'),
            (4, 'BMW', 'X5', 2021, 55000, 'SUV')
        ])
        self.cursor.executemany('INSERT INTO Customers VALUES (?, ?, ?, ?, ?)', [
            (1, 'John', 'Doe', 'john.doe@example.com', 1),
            (2, 'Jane', 'Smith', 'jane.smith@example.com', 2),
            (3, 'Mike', 'Brown', 'mike.brown@example.com', 3),
            (4, 'Anna', 'Davis', 'anna.davis@example.com', 4)
        ])
        self.cursor.executemany('INSERT INTO Sales VALUES (?, ?, ?, ?, ?)', [
            (1, 1, 1, '2024-08-01', 24000),
            (2, 2, 2, '2024-08-03', 22000),
            (3, 3, 3, '2024-08-10', 26000),
            (4, 4, 4, '2024-08-12', 55000)
        ])
        self.cursor.executemany('INSERT INTO Regions VALUES (?, ?)', [
            (1, 'North'),
            (2, 'South'),
            (3, 'East'),
            (4, 'West')
        ])
        self.conn.commit()

    def tearDown(self):
        # Close the connection after each test
        self.conn.close()

    def test_top_selling_models(self):
        query = '''
        SELECT c.make, c.model, COUNT(s.sale_id) as total_sales
        FROM Sales s
        JOIN Cars c ON s.car_id = c.car_id
        GROUP BY c.make, c.model
        ORDER BY total_sales DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        # Check if the top-selling model is correctly identified
        self.assertEqual(df.iloc[0]['model'], 'Camry')

    def test_sales_by_region(self):
        query = '''
        SELECT r.region_name, SUM(s.price) as total_sales
        FROM Sales s
        JOIN Customers cu ON s.customer_id = cu.customer_id
        JOIN Regions r ON cu.region_id = r.region_id
        GROUP BY r.region_name
        ORDER BY total_sales DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        # Check if the region with the highest sales is correctly identified
        self.assertEqual(df.iloc[0]['region_name'], 'West')

    def test_customer_spending(self):
        query = '''
        SELECT cu.first_name || ' ' || cu.last_name AS customer_name, SUM(s.price) AS total_spent
        FROM Sales s
        JOIN Customers cu ON s.customer_id = cu.customer_id
        GROUP BY customer_name
        ORDER BY total_spent DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        # Check if the highest spending customer is correctly identified
        self.assertEqual(df.iloc[0]['customer_name'], 'Anna Davis')

if __name__ == '__main__':
    unittest.main()
