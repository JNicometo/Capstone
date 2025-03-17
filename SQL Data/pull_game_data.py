import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

def ScheduleAndResults(response):
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'games'})
        if table:
            # Read the HTML table into a pandas DataFrame
            df = pd.read_html(str(table))[0]
            
            # Define the custom headers
            header = [
                "Week", "Day", "Date", "time", 
                "box score", "W/L", "OT", "Rec", "home", "Opp", "Tm", "Opp", "O_1stD", "O_TotYd", "O_PassY", 
                "O_RushY", "O_TO", "D_1stD", "D_TotYd", "D_PassY", "D_RushY", "D_TO"
            ]
            
            header2 = [
                "Week", "Day", "Date", "time", 
                "box score", "W/L", "OT", "Rec", "home", "Opp", "Tm", "Opp", "O_1stD", "O_TotYd", "O_PassY", 
                "O_RushY", "O_TO", "D_1stD", "D_TotYd", "D_PassY", "D_RushY", "D_TO", "exp points Offense", "exp points Defense", "exp points Sp. Tms"
            ]
            
            # Check the number of columns and set the appropriate header
            if len(df.columns) == 22:
                df.columns = header
            elif len(df.columns) == 25:
                df.columns = header2
            else:
                print(f"Unexpected number of columns: {len(df.columns)}")
                return None
            
            # Remove the first row (which was used as the header)
            #df = df[1:].reset_index(drop=True)
            
            # Update the 'home' column
            df['home'] = df['home'].apply(lambda x: False if x == '@' else True)
            
            return df
        else:
            print("Table not found")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

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

'''
team_abbr = "buf"
year = 1990

url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
url_make = url.format(team_abbr, year)
response = requests.get(url_make)
##Example usage
df = ScheduleAndResults(response)
print(df)
'''