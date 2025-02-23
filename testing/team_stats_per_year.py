import requests
from bs4 import BeautifulSoup
import pandas as pd

team = "buf"
year = 2024

url = "https://www.pro-football-reference.com/teams/{}/{}.htm"
url_make = url.format(team, year)
response = requests.get(url_make)

x=0 
while x < 1:
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'games'})
        if table:
            # Read the HTML table into a pandas DataFrame
            df = pd.read_html(str(table))[0]
            print(df)
            x = x+1

        else:
            print("Table not found")
            x = x+1
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        x = x+1

