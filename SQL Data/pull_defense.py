from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import requests

def defense(response):
    header1 = [
        "Rk", "Player", "Age", "Pos", "G", "GS",
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "PD", "FF", "Fmb", "FR", "Yds", "FRTD",
        "Sk", 
        "tackle_Comb", "tackle_Solo", "tackle_Ast", "TFL", "QBHits",
        "Sfty", "Awards"
    ]
    header2 = [
        "Rk", "Player", "Age", "Pos", "G", "GS", 
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "Fmb", "FR", "fm_Yds", "FRTD", 
        "Sk", "Sfty", "Awards"
    ]
    header3 = [
        "Rk", "Player", "Age", "Pos", "G", "GS", 
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "FF", "Fmb", "FR", "fm_Yds", "FRTD", 
        "tackle_Comb", "Sk", "Sfty", "Awards"
    ]
    header4 = [
        "Rk", "Player", "Age", "Pos", "G", "GS",
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "PD", "FF", "Fmb", "FR", "Yds", "FRTD",
        "Sk", 
        "tackle_Comb", "tackle_Solo", "tackle_Ast", "TFL",
        "Sfty", "Awards"
    ]
    header5 = [
        "Rk", "Player", "Age", "Pos", "G", "GS", 
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "Fmb", "FR", "fm_Yds", "FRTD", 
        "Sk", "tackle_Comb", "Sfty", "Awards"
    ]
    header6 = [
        "Rk", "Player", "Age", "Pos", "G", "GS",
        "Int", "int_Yds", "IntTD", "int_Lng", 
        "FF", "Fmb", "FR", "Yds", "FRTD",
        "Sk", 
        "tackle_Comb", "tackle_Solo", "tackle_Ast",
        "Sfty", "Awards"
    ]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'defense'})
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
            elif len(df.columns) == len(header3):
                df.columns = header3
            elif len(df.columns) == len(header4):
                df.columns = header4
            elif len(df.columns) == len(header5):
                df.columns = header5
            elif len(df.columns) == len(header6):
                df.columns = header6
            else:
                print(f"Unexpected number of columns: {len(df.columns)}")
                return None
            #print(df)
            return df
        else:
            print("Table not found")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

##team_abbr = "buf"
##year = 1995

##url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
##url_make = url.format(team_abbr, year)
##esponse = requests.get(url_make)

##df = defense(response)
##print(df)
