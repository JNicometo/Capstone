import pyodbc

# Database connection details
server = "192.168.68.89"
database = "Buffalo_Bills"  # Make sure this is the correct DB name
username = "Joe"
password = "7973"
driver = "{ODBC Driver 17 for SQL Server}"

# Connect to SQL Server
conn = pyodbc.connect(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
cursor = conn.cursor()

# Corrected SQL query with square brackets around table name
query = "SELECT * FROM [1970_ScheduleAndResults_buf]"
cursor.execute(query)

# Fetch and print results
columns = [column[0] for column in cursor.description]  # Get column names
rows = cursor.fetchall()

for row in rows:
    print(dict(zip(columns, row)))  # Convert row to dictionary

# Close connection
cursor.close()
conn.close()

