import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import time


import pull_game_data
import pull_passing_data
import pull_rushing_and_receiving
import pull_defense

server = '192.168.68.89'
username = 'Joe'
password = '7973'
driver = 'ODBC Driver 17 for SQL Server'

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
    "was": {"name": "Washington_Commanders", "start_year": 2000}
    }



def save_data_to_sql(data_function, response, data_type, engine):
    df = data_function(response)
    if df is not None and not df.empty:
        table_name = f"{year}_{data_type}_{team_abbr}"
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data for {team_abbr} in {year} ({data_type}) saved to table {table_name}.")
    else:
        print(f"No data available for {team_abbr} in {year} ({data_type}).")



    
# Loop through each team and each year to pull data and save to the database
for team_abbr, team_info in teams_data.items():
    team_name = team_info["name"].replace(" ", "_")  # Replace spaces with underscores for database names
    start_year = team_info["start_year"]
    
    # Create a connection string for SQLAlchemy
    conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{team_name}?driver={driver.replace(" ", "+")}'
    engine = create_engine(conn_str)
    
    for year in range(start_year, 2025): 
        
        url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
        url_make = url.format(team_abbr, year)
        response = requests.get(url_make)  
        

        save_data_to_sql(pull_game_data.ScheduleAndResults,response, 'ScheduleAndResults', engine)
        save_data_to_sql(pull_passing_data.passing, response, 'passing', engine)
        save_data_to_sql(pull_rushing_and_receiving.Rushing_and_Receiving, response, 'Rushing_and_Receiving', engine)
        save_data_to_sql(pull_defense.defense, response, 'defense', engine)
        time.sleep(4)