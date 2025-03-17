import requests
from bs4 import BeautifulSoup

url = "https://www.pro-football-reference.com/teams/buf/1970.htm"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    table_ids = [table.get('id') for table in tables if table.get('id')]
    print("Table IDs found:", table_ids)
else:
    print(f"Failed to retrieve data: {response.status_code}")