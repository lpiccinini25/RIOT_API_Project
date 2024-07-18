
import requests
import pygame
import functions


black = (0,0,0)
white = (255,255,255)

api_key = 'RGAPI-267c12a7-85cd-4d85-9f5e-ea9d4d1645a3'
api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/llimeincoconut/0000'

print(requests.get(api_url))


api_url = api_url + '?api_key=' + api_key

puuid = functions.get_puuid('llimeincoconut', '0000', api_key)


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

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
screen_width = 500
screen_height = 500


def game_start_screen(): #add game start screen
    game_start = True
    while game_start: #start screen loop
        for event in pygame.event.get():
                if event.type == pygame.QUIT: #if clock exit, quit game
                    pygame.quit()
                    quit()
        window.fill(black)
        #^ fill in screen black

        
        #^add image of a chicken


        clock = pygame.time.Clock()
        #^ clock for death screen

        largeText = pygame.font.SysFont("ariel",65)
        #^ create font to render in text

        #^^ create text boxes for Final Score and Final level for death screen
        TextSurf, TextRect = text_objects("Welcome to", largeText)
        LTextSurf, LTextRect = text_objects("Crossy Street!", largeText)
        #^^ create text boxes for welcoming text
        TextRect.center = ((screen_width/2),(screen_height/5.5))
        LTextRect.center = ((screen_width/2),(screen_height/3.5))
        #^^ set the location of the text boxes
        window.blit(TextSurf, TextRect)
        window.blit(LTextSurf, LTextRect)
        #^ render text onto the window

        button("Quit",250,450,100,50,red,bright_red,quit)
        #quit and restart buttons^
        pygame.display.update()
        clock.tick(15)

window = pygame.display.set_mode((500, 500))
game_start_screen()



        

