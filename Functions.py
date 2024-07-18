import requests

def get_puuid(name, riot_id):
    puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + name + '/' + riot_id
    resp = requests.get(puuid_url)
    account_info = resp.json()
    puuid = account_info['puuid']
    return puuid

def get_match_history(name, riot_id):
    'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' 
