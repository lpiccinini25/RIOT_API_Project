
import requests
import pygame
import functions


black = (0,0,0)
white = (255,255,255)

def text_objects(text, font): #create text objects
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def button(self,msg,x,y,w,h,ic,ac,action=None): #add button function
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(self.window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            # runs whatever function is input, could be self.run() or quitgame()
            print(action)
            action()
    else: # if no action, meaning button not clicked, then render buttons
        pygame.draw.rect(self.window, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.window.blit(textSurf, textRect)

api_key = 'RGAPI-267c12a7-85cd-4d85-9f5e-ea9d4d1645a3'
api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/llimeincoconut/0000'

print(requests.get(api_url))


api_url = api_url + '?api_key=' + api_key

puuid = functions.get_puuid('llimeincoconut', '0000')


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

        

