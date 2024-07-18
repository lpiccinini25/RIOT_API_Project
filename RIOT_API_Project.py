
import requests

api_key = 'RGAPI-f2234498-0b43-4612-a09c-afa88c8e7f86'
api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/llimeincoconut/0000'

print(requests.get(api_url))

api_url = api_url + '?api_key=' + api_key

resp = requests.get(api_url)
account_info = resp.json()
puuid = account_info['puuid']


match_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=20' + '&api_key=' + api_key
print(puuid)
resp = requests.get(match_url)
match_history = resp.json()


"""
for match in match_history:
    api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api_key
    resp = requests.get(api_url)
    stats = resp.json()
    player_index = stats['metadata']['participants'].index(puuid)
    lane = stats['info']['participants'][player_index]['challenges']['lane']
"""
def compare_cs(match_history, api_key):

    total_difference = 0

    for match in match_history:
        api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api_key
        resp = requests.get(api_url)
        stats = resp.json()
        my_index = stats['metadata']['participants'].index(puuid)
        if my_index > 4:
            enemy_index = my_index - 5
        else:
            enemy_index = my_index + 5
        

        enemy_cs = stats['info']['participants'][enemy_index]['totalMinionsKilled'] + stats['info']['participants'][enemy_index]['neutralMinionsKilled']
        my_cs = stats['info']['participants'][my_index]['totalMinionsKilled'] + stats['info']['participants'][my_index]['neutralMinionsKilled']

        cs_difference = my_cs - enemy_cs
        total_difference += cs_difference
    
    average_difference = total_difference / len(match_history)
    return average_difference

        
print(compare_cs(match_history, api_key))



