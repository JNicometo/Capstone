import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from sqlalchemy import create_engine

# Define connection parameters for SQL Server
server = '192.168.68.89'
username = 'Joe'
password = '7973'
driver = 'ODBC Driver 17 for SQL Server'

# Create a connection string for SQLAlchemy
conn_str = f'mssql+pyodbc://{username}:{password}@{server}/master?driver={driver.replace(" ", "+")}'

teams_data = {
    "crd": {"name": "Arizona_Cardinals", "start_year": 1970},
    "atl": {"name": "Atlanta_Falcons", "start_year": 1970},
    "rav": {"name": "Baltimore_Ravens", "start_year": 1970},
    "buf": {"name": "Buffalo_Bills", "start_year": 1970},
    "car": {"name": "Carolina_Panthers", "start_year": 1995},
    "chi": {"name": "Chicago_Bears", "start_year": 1970},
    "cin": {"name": "Cincinnati_Bengals", "start_year": 1970},
    "cle": {"name": "Cleveland_Browns", "start_year": 1970},
    "dal": {"name": "Dallas_Cowboys", "start_year": 1970},
    "den": {"name": "Denver_Broncos", "start_year": 1970},
    "det": {"name": "Detroit_Lions", "start_year": 1970},
    "gnb": {"name": "Green_Bay_Packers", "start_year": 1970},
    "htx": {"name": "Houston_Texans", "start_year": 2002},
    "clt": {"name": "Indianapolis_Colts", "start_year": 1970},
    "jax": {"name": "Jacksonville_Jaguars", "start_year": 1970},
    "kan": {"name": "Kansas_City_Chiefs", "start_year": 1970},
    "sdg": {"name": "Los_Angeles_Chargers", "start_year": 1970},
    "ram": {"name": "Los_Angeles_Rams", "start_year": 1970},
    "mia": {"name": "Miami_Dolphins", "start_year": 1970},
    "min": {"name": "Minnesota_Vikings", "start_year": 1970},
    "nwe": {"name": "New_England_Patriots", "start_year": 1970},
    "nor": {"name": "New_Orleans_Saints", "start_year": 1970},
    "nyg": {"name": "New_York_Giants", "start_year": 1970},
    "nyj": {"name": "New_York_Jets", "start_year": 1970},
    "rai": {"name": "Las_Vegas_Raiders", "start_year": 1970},
    "phi": {"name": "Philadelphia_Eagles", "start_year": 1970},
    "pit": {"name": "Pittsburgh_Steelers", "start_year": 1970},
    "sfo": {"name": "San_Francisco_49ers", "start_year": 1970},
    "sea": {"name": "Seattle_Seahawks", "start_year": 1976},
    "tam": {"name": "Tampa_Bay_Buccaneers", "start_year": 1976},
    "oti": {"name": "Tennessee_Titans", "start_year": 1970},
    "was": {"name": "Washington_Commanders", "start_year": 1970}
}

tables = ['team_stats', 'games', 'team_conversions', 'passing', 'passing_post', 'rushing_and_receiving', 'rushing_and_receiving_post', 'defense', 'defense_post']

def pull_team_data(team, year):
    team_name = teams_data[team]["name"].replace(" ", "_")  # Replace spaces with underscores for database names
    database = team_name  # Use the team name as the database name
    
    # Create a connection to the team's database
    team_conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver.replace(" ", "+")}'
    team_engine = create_engine(team_conn_str)
    
    url = f"https://www.pro-football-reference.com/teams/{team}/{year}.htm"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for table_id in tables:
            table = soup.find('table', {'id': table_id})
            if table:
                try:
                    # Read the HTML table into a pandas DataFrame
                    df = pd.read_html(str(table))[0]
                    df['Team'] = team
                    df['Year'] = year
                    df['Table'] = table_id
                    
                    # Create a table name
                    table_name = f"{year}_{table_id}_{team}"
                    
                    # Save the DataFrame to the SQL Server database
                    df.to_sql(table_name, team_engine, if_exists='replace', index=False)
                    print(f"Data for {team} in {year} from table {table_id} added to {table_name}.")
                except Exception as e:
                    print(f"Failed to save data for {team} in {year} from table {table_id}: {e}")
            else:
                print(f"Table {table_id} not found for {team} in {year}.")
    else:
        print(f"Failed to retrieve data for {team} in {year}: {response.status_code}")

    # Add a delay between requests
    time.sleep(1)

# Example usage
pull_team_data('crd', 2024)


