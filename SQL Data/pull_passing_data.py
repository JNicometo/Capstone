import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine


def passing(response):
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'passing'})
        if table:
            # Read the HTML table into a pandas DataFrame
            df = pd.read_html(str(table))[0]
            
            return df
        else:
            print("Table not found")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    
#df = passing("crd", 1970)
#print(df)
#print(df.shape)