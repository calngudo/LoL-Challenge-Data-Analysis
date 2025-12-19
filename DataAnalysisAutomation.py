from dotenv import load_dotenv
import os, requests, pandas as pd, pygsheets, gspread, dotenv, psycopg2
from gspread import set_with_dataframe
from dotenv import load_dotenv
load_dotenv()

service_account = pygsheets.authorize(service_file='JSONs\\sacred-machine-481117-v7-c1c1ee2e05af.json')
sheet = service_account.open_by_url("https://docs.google.com/spreadsheets/d/1am8ie_kqq52wcbJ1pnpVkwVYQWKep1Wxsp_UZe90w3c/edit?usp=sharing")
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

def get_puuid(region = 'americas', gameName = None, tagLine = None):
    if gameName is not None and tagLine is not None:
        link = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={RIOT_API_KEY}'
        response = requests.get(link)
        if response.status_code == 200:
            return response.json()['puuid']
        else:
            print(response.status_code, response.text)
            return None
    else:
        print("Missing tagline or gamename")
        return None
    