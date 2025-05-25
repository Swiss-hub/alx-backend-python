#!/usr/bin/python3
import mysql.connector
import csv
import uuid

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# Connect specifically to ALX_prodev DB
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table
def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX(user_id)
    )
    """
    cursor.execute(query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

# Insert data from CSV file
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            uid = str(uuid.uuid4())
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (uid, row['name'], row['email'], row['age']))
    connection.commit()
    print("Data inserted successfully")
    cursor.close()