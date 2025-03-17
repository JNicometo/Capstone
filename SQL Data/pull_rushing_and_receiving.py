from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import requests

def Rushing_and_Receiving(response):
    header1 = [
        "Rk", "Player", "Age", "Pos", "G", "GS", "rush_Att", "rush_Yds", "rush_TD", "rush_Lng", 
        "rush_Y/A", "rush_Y/G", "rush_A/G", "Rec", "rec_Yds", "rec_Y/R", "rec_TD", "rec_Lng", "rec_R/G", "rec_Y/G", 
        "scrim_Touch", "scrim_Y/Tch", "YScm", "total_TD", "Fmb", "Awards"
    ]
    header2 = [
        "Rk", "Player", "Age", "Pos", "G", "GS", 
        "rush_Att", "rush_Yds", "rush_TD", "rush_1D", "rush_Succ%", "rush_Lng", "rush_Y/A", "rush_Y/G", "rush_A/G", 
        "targets", "Rec", "rec_Yds", "rec_Y/R", "rec_TD", "rec_1D", "rec_Succ%", "rec_Lng", "rec_R/G", "rec_Y/G", "Ctch%", "Y/Tgt", 
        "scrim_Touch", "scrim_Y/Tch", "YScm", "total_TD", "Fmb", "Awards"
    ]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'rushing_and_receiving'})
        if table:
            # Read the HTML table into a pandas DataFrame without headers
            df = pd.read_html(str(table), header=None)[0]
            # Remove the first row (which was used as the header)
            #df = df.iloc[1:].reset_index(drop=True)
            # Check the number of columns and set the appropriate header
            #print(f"Number of columns in DataFrame: {len(df.columns)}")
            if len(df.columns) == len(header1):
                df.columns = header1
            elif len(df.columns) == len(header2):
                df.columns = header2
            else:
                print(f"Unexpected number of columns: {len(df.columns)}")
                return None
            ##print(df)
            return df
        else:
            print("Table not found")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
'''
team_abbr = "buf"
year = 1990

url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
url_make = url.format(team_abbr, year)
response = requests.get(url_make)

df = Rushing_and_Receiving(response)
if df is not None:
    print(df)
else:
    print("No data to display")
'''