from dotenv import load_dotenv
import requests, os 

load_dotenv()

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

def get_matchhistory(puuid, count):
    link = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={datestart}&endTime={dateend}&queue={queuetype}&type=ranked&start=0&count={count}&api_key={RIOT_API_KEY}'
    response = requests.get(link)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
    return None

def get_match_details(match_id):
    link = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}'
    response = requests.get(link)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
    return None