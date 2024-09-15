import mysql.connector
import pandas as pd
import os
import sqlite3
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Function to connect to the MySQL database
def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,  # Utiliser l'adresse sélectionnée
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Successfully connected to the MySQL database")
        return connection
    except Error as e:
        messagebox.showerror("Connection Error", f"Error connecting to MySQL: {e}")
        return None

# Execute an SQL query and fetch data
def execute_query(connection, query):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        print(f"Error executing the query: {e}")
        return None

# Generate different file types (Excel, CSV, JSON, Parquet)
def generate_file_report(data, file_name, file_type):
    try:
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("Date:%Y_%m_%d_Time:%H:%M")
        directory = "/Users/morgan/Desktop/Personal Project/Excel-Data-Report/reports/"
        
        # Map the user-friendly names to the file extensions
        if file_type == "Excel":
            file_extension = "xlsx"
        elif file_type == "Csv":
            file_extension = "csv"
        elif file_type == "Json":
            file_extension = "json"
        elif file_type == "Parquet":
            file_extension = "parquet"
        
        file_path = f"{directory}{file_name}_{timestamp}.{file_extension}"

        if file_type == "Excel":
            df.to_excel(file_path, index=False)
        elif file_type == "Csv":
            df.to_csv(file_path, index=False)
        elif file_type == "Json":
            df.to_json(file_path, orient='records', lines=True)
        elif file_type == "Parquet":
            df.to_parquet(file_path, index=False)

        print(f"{file_type.upper()} report generated: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error generating the {file_type} file: {e}")
        return None

# Store the generated file in a SQLite database (optional)
def store_file_in_database(file_path, sqlite_db='reports.db'):
    try:
        connection = sqlite3.connect(sqlite_db)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_name TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO reports (report_name, file_path)
            VALUES (?, ?)
        ''', (os.path.basename(file_path), file_path))
        connection.commit()
        print(f"File stored in the SQLite database: {file_path}")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error storing the file in SQLite: {e}")

# Function to connect and generate the report
def connect_and_generate_report():
    host = host_entry.get() if connection_mode.get() == 'remote' else "localhost"
    user = user_entry.get()
    password = password_entry.get()
    database = database_entry.get()
    file_type = file_type_var.get()

    connection = connect_to_database(host, user, password, database)

    if connection is not None:
        query = "SELECT * FROM customers"  # Example query
        data = execute_query(connection, query)

        if data:
            excel_file = generate_file_report(data, 'customers_report', file_type)

            if excel_file:
                store_file_in_database(excel_file)

        connection.close()
    else:
        messagebox.showerror("Error", "Unable to connect to the database")

# Create the user interface
root = tk.Tk()
root.title("MySQL Connection")

# Disable window resizing
root.resizable(False, False)

# Radio buttons for local or remote connection
tk.Label(root, text="Connection Mode").grid(row=0, column=0, sticky=tk.W)
connection_mode = tk.StringVar(value="local")  # Default to local
tk.Radiobutton(root, text="Local", variable=connection_mode, value="local").grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Remote", variable=connection_mode, value="remote").grid(row=0, column=2, sticky=tk.W)

# Host field for remote connection (appears after the mode is chosen)
tk.Label(root, text="Host").grid(row=1, column=0, sticky=tk.W)
host_entry = tk.Entry(root)
host_entry.grid(row=1, column=1, columnspan=2)

# Labels and text fields for connection information
tk.Label(root, text="User").grid(row=2, column=0, sticky=tk.W)
user_entry = tk.Entry(root)
user_entry.grid(row=2, column=1, columnspan=2)

tk.Label(root, text="Password").grid(row=3, column=0, sticky=tk.W)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=3, column=1, columnspan=2)

tk.Label(root, text="Database").grid(row=4, column=0, sticky=tk.W)
database_entry = tk.Entry(root)
database_entry.grid(row=4, column=1, columnspan=2)

# Dropdown for file type selection with user-friendly names
tk.Label(root, text="File Type").grid(row=5, column=0, sticky=tk.W)
file_type_var = tk.StringVar(value="Excel")
file_type_dropdown = tk.OptionMenu(root, file_type_var, "Excel", "Csv", "Json", "Parquet")
file_type_dropdown.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E)  # Align dropdown

# Button to connect and generate the report
generate_button = tk.Button(root, text="Connect and Generate Report", command=connect_and_generate_report)
generate_button.grid(row=6, column=0, columnspan=3)

# Run the tkinter application
root.mainloop()
