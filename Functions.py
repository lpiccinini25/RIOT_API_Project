import requests

def get_puuid(name, riot_id):
    puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + name + '/' + riot_id
    resp = 



def get_final_url(api_url, api_key):
    return api_url + '?api_key=' + api_key

def get_match_history(name, riot_id):
    'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' 
