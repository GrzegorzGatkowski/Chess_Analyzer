import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = 'data/chess.db'
connection = sqlite3.connect(db_path)

# Create a cursor object
cursor = connection.cursor()

# Execute a query to retrieve all table names from the database schema
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all table names from the result set
table_names = cursor.fetchall()

# Iterate over table names and read each table into a DataFrame
for table_name in table_names:
    table_name = table_name[0]  # Extract the table name from the result
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", connection)
    
    # Now you have a DataFrame for each table, 'df'
    # You can work with 'df' as needed, for example, print the first few rows:
    print(f"Table: {table_name}")
    print(df)
    print("\n")

# Close the database connection
connection.close()
