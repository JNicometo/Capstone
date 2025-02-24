from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import requests

def Rushing_and_Receiving(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'rushing_and_receiving'})
        if table:
            # Read the HTML table into a pandas DataFrame without headers
            df = pd.read_html(str(table), header=None)[0]
            return df
        else:
            print("Table not found")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

team_abbr = "buf"
year = 2024

url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
url_make = url.format(team_abbr, year)
response = requests.get(url_make)

df = Rushing_and_Receiving(response)
print(df.columns)