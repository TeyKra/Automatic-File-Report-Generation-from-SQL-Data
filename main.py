import mysql.connector
import pandas as pd
import os
import sqlite3
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  
from datetime import datetime

# Function to connect to the MySQL database
def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,  
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

# Function to execute an SQL query and fetch the data
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

# Function to generate reports in different file formats (Excel, CSV, JSON, Parquet)
def generate_file_report(data, file_name, file_type, folder=None):
    try:
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M")  # Replace ":" with "-"
        if folder:
            directory = f"/Users/morgan/Desktop/Personal Project/Excel-Data-Report/reports/{folder}/"
            # Create the folder if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            directory = "/Users/morgan/Desktop/Personal Project/Excel-Data-Report/reports/"
        
        # Map user-friendly names to file extensions
        if file_type == "Excel":
            file_extension = "xlsx"
        elif file_type == "Csv":
            file_extension = "csv"
        elif file_type == "Json":
            file_extension = "json"
        elif file_type == "Parquet":
            file_extension = "parquet"
        
        # Generate the file path with timestamp
        file_path = f"{directory}{file_name}_{timestamp}.{file_extension}"

        # Generate and save the report in the selected format
        if file_type == "Excel":
            df.to_excel(file_path, index=False)
            store_file_in_database(file_path)  
        elif file_type == "Csv":
            df.to_csv(file_path, index=False)
            store_file_in_database(file_path)
        elif file_type == "Json":
            df.to_json(file_path, orient='records', lines=True)
            store_file_in_database(file_path)
        elif file_type == "Parquet":
            df.to_parquet(file_path, index=False)
            store_file_in_database(file_path)

        print(f"{file_type.upper()} report generated: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error generating the {file_type} file: {e}")
        return None

# Function to store the generated file information in a SQLite database
def store_file_in_database(file_path, sqlite_db=None):
    try:
        if sqlite_db is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sqlite_db = os.path.join(script_dir, "reports.db")
        
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
    except sqlite3.Error as e:
        print(f"Error storing the file in SQLite: {e}")

# Function to retrieve the list of tables from the MySQL database
def get_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return [table[0] for table in tables] 
    except Error as e:
        print(f"Error fetching table list: {e}")
        return []

# Function to connect to the database and generate the report based on user input
def connect_and_generate_report():
    host = host_entry.get() if connection_mode.get() == 'remote' else "localhost"
    user = user_entry.get()
    password = password_entry.get()
    database = database_entry.get()
    file_type = file_type_var.get()
    
    # Connect to the database
    connection = connect_to_database(host, user, password, database)

    if connection is not None:
        selected_table = table_var.get()

        # Generate reports for all tables if 'All tables' is selected
        if selected_table == "All tables":
            tables = get_tables(connection)
            timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M")  # Replace ":" with "-"
            folder_name = f"{file_type}_All_tables_{timestamp}"

            for table in tables:
                query = f"SELECT * FROM {table}"
                data = execute_query(connection, query)
                if data:
                    generate_file_report(data, f'{table}_report', file_type, folder_name)
        else:
            # Generate report for the selected table
            query = f"SELECT * FROM {selected_table}"
            data = execute_query(connection, query)
            if data:
                generate_file_report(data, f'{selected_table}_report', file_type)

        connection.close()
    else:
        messagebox.showerror("Error", "Unable to connect to the database")

# Function to populate the table dropdown with the list of tables from the database
def populate_table_dropdown():
    host = host_entry.get() if connection_mode.get() == 'remote' else "localhost"
    user = user_entry.get()
    password = password_entry.get()
    database = database_entry.get()

    connection = connect_to_database(host, user, password, database)
    
    if connection:
        tables = get_tables(connection)
        tables.insert(0, "All tables")  # Add 'All tables' option
        table_dropdown['values'] = tables
        table_dropdown.current(0)  # Set 'All tables' as default
        connection.close()
    else:
        messagebox.showerror("Error", "Unable to fetch tables")

# Create the user interface using tkinter
root = tk.Tk()
root.title("MySQL Connection")

root.resizable(False, False)

# Using grid layout for proper vertical alignment of input fields
tk.Label(root, text="Connection Mode").grid(row=0, column=0, sticky=tk.W)
connection_mode = tk.StringVar(value="local")  # Default connection mode is 'local'
tk.Radiobutton(root, text="Local", variable=connection_mode, value="local").grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Remote", variable=connection_mode, value="remote").grid(row=0, column=1, sticky=tk.W, padx=60)

# Host field (for remote connection only)
tk.Label(root, text="Host").grid(row=1, column=0, sticky=tk.W)
host_entry = tk.Entry(root)
host_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W+tk.E)

# Fields for MySQL connection details
tk.Label(root, text="User").grid(row=2, column=0, sticky=tk.W)
user_entry = tk.Entry(root)
user_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E)

tk.Label(root, text="Password").grid(row=3, column=0, sticky=tk.W)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W+tk.E)

tk.Label(root, text="Database").grid(row=4, column=0, sticky=tk.W)
database_entry = tk.Entry(root)
database_entry.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E)

# Dropdown for selecting the table to generate a report
tk.Label(root, text="Select Table").grid(row=5, column=0, sticky=tk.W)
table_var = tk.StringVar()
table_dropdown = ttk.Combobox(root, textvariable=table_var)
table_dropdown.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E)

# Dropdown for selecting the file type (Excel, CSV, JSON, Parquet)
tk.Label(root, text="File Type").grid(row=6, column=0, sticky=tk.W)
file_type_var = tk.StringVar(value="Excel")
file_type_dropdown = tk.OptionMenu(root, file_type_var, "Excel", "Csv", "Json", "Parquet")
file_type_dropdown.grid(row=6, column=1, columnspan=2, sticky=tk.W+tk.E)

# Button to fetch tables and populate the dropdown
populate_button = tk.Button(root, text="Fetch Tables", command=populate_table_dropdown)
populate_button.grid(row=7, column=0, columnspan=3, sticky=tk.W+tk.E)

# Button to connect to the database and generate the report
generate_button = tk.Button(root, text="Connect and Generate Report", command=connect_and_generate_report)
generate_button.grid(row=8, column=0, columnspan=3, sticky=tk.W+tk.E)

# Run the tkinter application
root.mainloop()
