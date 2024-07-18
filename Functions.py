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