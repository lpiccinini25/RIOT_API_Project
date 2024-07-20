
import requests
import pygame
import asyncio
import aiohttp
import pygame.font
pygame.init()

black = (0,0,0)
white = (255,255,255)

api_key = 'RGAPI-a076eb99-f790-4996-aeda-96f804bafddd'
api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/llimeincoconut/0000'

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
"""

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
screen_width = 1000
screen_height = 500

def text_objects(text, font): #create text objects
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None): #add button function
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            # runs whatever function is input, could be self.run() or quitgame()
            action()
    else: # if no action, meaning button not clicked, then render buttons
        pygame.draw.rect(window, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        window.blit(textSurf, textRect)


screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = white
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class SummonerIDInputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True, self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        
        return False, self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def enter_riot_id():
    done = False
    input_riot_id = SummonerIDInputBox(screen_width/2.5, screen_height/1.7, 100, 25)
    input_boxes = [input_riot_id]
    while not done: 
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit()
                for box in input_boxes:
                    done, riot_name = box.handle_event(event)
        window.fill(black)

        for box in input_boxes:
            box.update()
            box.draw(screen)
        

        font = pygame.font.SysFont("Ariel",25)
        text = font.render("Please enter your Riot name and Riot ID", True, white)
        window.blit(text, text.get_rect(center=(screen_width/2, screen_height/2)))

        font = pygame.font.SysFont('Ariel', 20)
        text = font.render('(Example: SummonerName#0000)', True, white)
        window.blit(text, text.get_rect(center=(screen_width/2, screen_height/1.85)))

 
        leagueLogo = pygame.image.load('LeagueOfLegends.png')

        leagueLogo = pygame.transform.smoothscale(leagueLogo, (leagueLogo.get_width()/1.5, leagueLogo.get_height()/1.5))
        window.blit(leagueLogo, leagueLogo.get_rect(center=(screen_width/2, screen_height/3.5)))
 
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)
    main_screen(riot_name)

def main_screen(riot_id_and_name):

    def get_puuid(name, riot_id):
        puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + name + '/' + riot_id + '?api_key=' + api_key
        resp = requests.get(puuid_url)
        account_info = resp.json()
        puuid = account_info["puuid"]
        return puuid

    def get_match_history(puuid):
        api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=20&api_key='+ api_key
        resp = requests.get(api_url)
        match_history = resp.json()
        return match_history 

    riot_id_and_name = riot_id_and_name.split("#")
    riot_name = riot_id_and_name[0]
    riot_id = riot_id_and_name[1]
    puuid = get_puuid(riot_name, riot_id)
    matchHistory = get_match_history(puuid)

    done = False
    window.fill(black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if clock exit, quit game
                pygame.quit()
                quit()
        button('Average KDA', screen_width/2, screen_height/2, 150, 100, green, bright_green, lambda: display_average_kda(puuid, matchHistory))
        button('Average CS difference', screen_width/7, screen_height/2, 150, 100, green, bright_green, lambda: display_average_cs_diff(puuid, matchHistory))

        largeText = pygame.font.SysFont("Georgia",25)

        TextSurf, TextRect = text_objects('Data taken from last ' + str(len(matchHistory)) + ' games', largeText)
        TextRect.center = ((screen_width/2),(screen_height/6))
        window.blit(TextSurf, TextRect)

        

        pygame.display.update()

        clock = pygame.time.Clock()
        clock.tick(15)

def display_average_kda(puuid, matchHistory):
    average_kda = asyncio.run(get_average_kda(puuid, matchHistory))
    statText = pygame.font.SysFont("Georgia",20)
    textSurf, textRect = text_objects(str(average_kda), statText)
    window.blit(textSurf, textRect)

def display_average_cs_diff(puuid, matchHistory):
    average_cs_diff = asyncio.run(get_average_cs_diff(puuid, matchHistory))
    font = pygame.font.SysFont("Ariel",25)
    text = font.render((str(average_cs_diff)[0:3]), True, white)
    window.blit(text, text.get_rect(center=(screen_width/2.3, screen_height/1.5)))


async def get_average_kda(puuid, matchHistory):
    async with aiohttp.ClientSession() as session:
        sum = 0 
        matchHistory = get_tasks(session, matchHistory)
        matchHistory = await asyncio.gather(*matchHistory)
        for match in matchHistory:
            match = await match.json()
            player_index = match['metadata']['participants'].index(puuid)
            sum += match['info']['participants'][player_index]['challenges']['kda']
        return sum / len(matchHistory)

async def get_average_cs_diff(puuid, matchHistory):
    async with aiohttp.ClientSession() as session:    
        totalDifference = 0
        totalGames = len(matchHistory)
        matchHistory = get_tasks(session, matchHistory)
        matchHistory = await asyncio.gather(*matchHistory)

        for match in matchHistory:

            match = await match.json()
            myIndex = match['metadata']['participants'].index(puuid)

            if myIndex > 4:
                enemyIndex = myIndex - 5
            else:
                enemyIndex = myIndex + 5

            enemyCs = match['info']['participants'][enemyIndex]['totalMinionsKilled'] + match['info']['participants'][enemyIndex]['neutralMinionsKilled']
            myCs = match['info']['participants'][myIndex]['totalMinionsKilled'] + match['info']['participants'][myIndex]['neutralMinionsKilled']
            csDifference = myCs - enemyCs
            totalDifference += csDifference
    
        average_difference = totalDifference / totalGames
        return average_difference

def get_tasks(session, matchHistory):
        asyncMatchHistory = []
        for match in matchHistory:
            asyncMatchHistory.append(session.get('https://americas.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api_key, ssl=False))
        return asyncMatchHistory





window = pygame.display.set_mode((1000,550))
pygame.display.set_caption("Riot Api Project")
enter_riot_id()



        

