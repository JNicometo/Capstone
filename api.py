from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc

# Database connection details
SERVER = "192.168.68.89"
USERNAME = "Joe"
PASSWORD = "7973"
DRIVER = "{ODBC Driver 17 for SQL Server}"

# Create FastAPI instance
app = FastAPI()

# Enable CORS
origins = [
    "http://127.0.0.1:5500",  # Add the origin of your frontend application
    "http://localhost:5500",  # Add localhost if you are using it
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to connect to a specific team database
def get_db_connection(team_db: str):
    try:
        conn = pyodbc.connect(
            f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={team_db};UID={USERNAME};PWD={PASSWORD}"
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", str(e))
        return None

@app.get("/{database}/{year}/{table_type}/{team_abbr}")

def get_team_data(database: str, year: int, table_type: str, team_abbr: str):
    table_type = table_type  # Ensure case consistency
    valid_table_types = {
        "defense",
        "passing",
        "ScheduleAndResults",
        "rushing_and_receiving"
    }
    
    if table_type not in valid_table_types:
        raise HTTPException(status_code=400, detail=f"Invalid table type. Choose from {valid_table_types}")

    table_name = f"[{year}_{table_type}_{team_abbr}]"
    
    conn = get_db_connection(database)  # Connect to the selected database
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    
    return records
