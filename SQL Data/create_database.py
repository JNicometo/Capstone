import pyodbc

# Define connection parameters for SQL Server
server = '192.168.68.89'
database = 'master'  # Connect to the master database to create new databases
username = 'Joe'
password = '7973'
driver = '{ODBC Driver 17 for SQL Server}'

# Create a connection to the SQL Server
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str, autocommit=True)  # Enable autocommit mode
cursor = conn.cursor()

teams_years = {
    "Arizona Cardinals": 1920, "Atlanta Falcons": 1966, "Baltimore Ravens": 1996, "Buffalo Bills": 1960, 
    "Carolina Panthers": 1995, "Chicago Bears": 1920, "Cincinnati Bengals": 1968, "Cleveland Browns": 1946,
    "Dallas Cowboys": 1960, "Denver Broncos": 1960, "Detroit Lions": 1930, "Green Bay Packers": 1921, 
    "Houston Texans": 2002, "Indianapolis Colts": 1953, "Jacksonville Jaguars": 1995, "Kansas City Chiefs": 1960,
    "Los Angeles Chargers": 1960, "Los Angeles Rams": 1937, "Miami Dolphins": 1966, "Minnesota Vikings": 1961, 
    "New England Patriots": 1960, "New Orleans Saints": 1967, "New York Giants": 1925, "New York Jets": 1960,
    "Las Vegas Raiders": 1960, "Philadelphia Eagles": 1933, "Pittsburgh Steelers": 1933, "San Francisco 49ers": 1950, 
    "Seattle Seahawks": 1976, "Tampa Bay Buccaneers": 1976, "Tennessee Titans": 1960, "Washington Commanders": 1932
}

# Loop through the teams and create a database for each team
for team in teams_years.keys():
    database_name = team.replace(" ", "_")  # Replace spaces with underscores for database names
    try:
        cursor.execute(f"CREATE DATABASE [{database_name}]")
        print(f"Database {database_name} created successfully.")
    except pyodbc.Error as e:
        print(f"Failed to create database {database_name}: {e}")

# Close the connection to the SQL Server
conn.close()