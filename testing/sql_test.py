import pyodbc

# Define connection parameters
server = '192.168.68.89'  # Example: 'localhost\SQLEXPRESS' or 'your_server.database.windows.net'
database = 'test'
username = 'Joe'
password = '7973'
driver = '{ODBC Driver 17 for SQL Server}'

try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}'
    )
    print("Connected successfully!")

    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        IF OBJECT_ID('dbo.test', 'U') IS NOT NULL
            DROP TABLE dbo.test;
        CREATE TABLE dbo.test (
            this INT,
            worked INT
        )
    ''')
    print("Table created successfully!")

    # Insert rows
    for i in range(1, 11):
        cursor.execute('INSERT INTO dbo.test (this, worked) VALUES (?, ?)', (i, i))
    conn.commit()
    print("Rows inserted successfully!")

    # Verify insertion
    cursor.execute('SELECT * FROM dbo.test')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except pyodbc.Error as e:
    print("Connection failed:", e)
    print("SQL State:", e.args[0])
    print("Error Message:", e.args[1])
finally:
    if 'conn' in locals():
        conn.close()
