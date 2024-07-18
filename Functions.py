import requests
import pygame

white = (255,255,255)

def get_puuid(name, riot_id, api_key):
    puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + name + '/' + riot_id + '?api_key=' + api_key
    resp = requests.get(puuid_url)
    account_info = resp.json()
    puuid = account_info['puuid']
    return puuid

def get_match_history(name, riot_id):
    'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' 

