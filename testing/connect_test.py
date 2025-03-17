import pyodbc

server = "192.168.68.89"
database = "Buffalo_Bills"
username = "Joe"
password = "7973"
driver = "{ODBC Driver 17 for SQL Server}"

try:
    conn = pyodbc.connect(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
