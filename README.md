# Automatic File Report Generation from SQL Data

This project is designed to connect to a MySQL database, execute an SQL query, fetch data, and generate a report in various formats (Excel, CSV, JSON, Parquet). The generated reports are stored locally, and optionally, their metadata (file path and report name) is stored in a SQLite database. This project also includes a graphical user interface (GUI) built using `tkinter` to allow users to input database connection details and select the desired file format for the generated report.

## Features

- **MySQL Database Connection**: Securely connect to a MySQL database by entering connection details (host, user, password, and database name).
- **SQL Query Execution**: Executes SQL queries to retrieve data from the database.
- **Report Generation in Multiple Formats**: Generates reports in Excel, CSV, JSON, or Parquet formats, with a timestamp appended to the file name.
- **SQLite Database Integration (Optional)**: Stores the generated report’s metadata (file name and file path) in a SQLite database.
- **Graphical User Interface (GUI)**: User-friendly GUI for entering connection details, selecting the file format, and generating reports.

## Installation

### Prerequisites

- Python 3.x
- `mysql-connector-python` package
- `pandas` package
- `tkinter` (usually included with Python installations)
- `openpyxl` (for handling Excel file formats)
- `sqlite3` (included with Python installations)
- `pyarrow` (for handling Parquet file formats)

### Install Dependencies

You can install the required dependencies using `pip`:

```bash
pip install mysql-connector-python pandas openpyxl pyarrow
```

## Project Structure

```
│
├── main.py                   # Main Python script
├── reports/                  # Directory where generated reports are stored
├── reports.db                # SQLite database file 
```

## How to Run

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Run the application**:

```bash
python main.py
```

3. **Use the GUI**:
   - Choose between "Local" or "Remote" connection modes.
   - Enter your MySQL database connection details (host, user, password, database).
   - Select the desired file format (Excel, CSV, JSON, or Parquet).
   - Click on the "Connect and Generate Report" button to execute the process.

The selected report will be generated and stored in the `reports/` directory, and optionally, the report metadata will be stored in the SQLite database.

## Example Usage

In the GUI, enter the following values:

- **Host**: `localhost` (or a remote host address)
- **User**: `root`
- **Password**: `your_password`
- **Database**: `your_database`
- **File Type**: Select between Excel, CSV, JSON, or Parquet.

The script will execute the default query (e.g., `SELECT * FROM customers`) and generate a report named `customers_report_<timestamp>.<file_format>`.

## Code Overview

### MySQL Connection

The `connect_to_database()` function establishes a connection to the MySQL database using the provided credentials. If successful, the connection object is returned.

```python
def connect_to_database(host, user, password, database):
    # MySQL connection logic
```

### Query Execution

The `execute_query()` function runs the SQL query and returns the fetched data as a list of dictionaries.

```python
def execute_query(connection, query):
    # SQL query execution logic
```

### Report Generation

The `generate_file_report()` function generates a report from the fetched data in the format chosen by the user (Excel, CSV, JSON, or Parquet). The report is saved with a timestamp in the `reports/` directory.

```python
def generate_file_report(data, file_name, file_type):
    # Report generation logic based on the selected file format
```

### Storing in SQLite

The `store_file_in_database()` function stores the report’s metadata in a SQLite database for tracking purposes.

```python
def store_file_in_database(file_path, sqlite_db='reports.db'):
    # Store report metadata in SQLite database
```

### GUI Application

The project uses `tkinter` to provide a simple user interface. Users can enter their MySQL connection details, select the desired file format, and trigger the report generation with a button click.

```python
# Tkinter application logic
root.mainloop()
```

## Future Improvements

- **Custom Queries**: Allow users to input custom SQL queries via the GUI.
- **Error Handling**: Improve error handling for database connections and file operations.
- **Advanced Reporting Options**: Add features like report filtering, custom formatting, and multi-database support.
- **Automatic Upload to Data Lakes**: Implement functionality to automatically upload generated reports to a Data Lake using cloud services like AWS S3 or Hadoop, enhancing scalability and data storage management for large datasets.
