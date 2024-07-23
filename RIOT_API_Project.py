import requests
import pygame
import asyncio
import aiohttp
import time
import os 

pygame.init()

api_key = 'RGAPI-49cc35ef-fab2-4de5-b41e-b76d2092baee'

async def updateChampionJson():
    async with aiohttp.ClientSession() as session:
        latest = await session.get("https://ddragon.leagueoflegends.com/api/versions.json")
        version = await latest.json()

        ddragon = await session.get('https://ddragon.leagueoflegends.com/cdn/' + version[0] + '/data/en_US/champion.json')
        championJson = await ddragon.json()
        return championJson['data']

async def keyToCharacterDict(championId=None):
    if championId not in championIdToName:
        for champion in championJson:
            champion = champion.split()
            if len(champion) > 1:
                champion = champion[0] + champion[1]
            else:
                champion = champion[0]
            championIdToName[championJson[champion]['key']] = champion
    else:
        return championIdToName[championId]

championIdToName = dict()
championJson = asyncio.run(updateChampionJson())
asyncio.run(keyToCharacterDict('5'))

window = pygame.display.set_mode((1000,550))

black = (0,0,0)
white = (255,255,255)
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

    def draw(self, window):
        # Blit the text.
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, 2)

def enter_riot_id():

    input_riot_id = SummonerIDInputBox(screen_width/2.5, screen_height/1.7, 100, 25)
    input_boxes = [input_riot_id]
    done = False

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
            box.draw(window)

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

    window.fill(black)

    riot_id_and_name = riot_id_and_name.split("#")
    riot_name = riot_id_and_name[0]
    riot_id = riot_id_and_name[1]

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

    puuid = get_puuid(riot_name, riot_id)
    matchHistory = get_match_history(puuid)

    def get_summonerId(puuid, matchHistory):
        api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + matchHistory[0] + '?api_key=' + api_key
        resp = requests.get(api_url)
        match = resp.json()
        playerIndex = match['metadata']['participants'].index(puuid)
        summonerId = match['info']['participants'][playerIndex]['summonerId']
        return summonerId

    def get_summonerInformation(summonerId):
        api_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/' + summonerId + '?api_key=' + api_key
        resp = requests.get(api_url)
        summonerInfo = resp.json()
        return summonerInfo['profileIconId'], summonerInfo['summonerLevel'], summonerInfo['accountId']
    
    summonerId = get_summonerId(puuid, matchHistory)
    IconId, summonerLevel, accountId =  get_summonerInformation(summonerId)

    font = pygame.font.SysFont('Ariel', 30)
    text = font.render(riot_name + '#' + riot_id, True, white)
    window.blit(text, text.get_rect(center=(screen_width*3/4, screen_height * 3/30)))

    font = pygame.font.SysFont('Ariel', 30)
    text = font.render('Level: ' + str(summonerLevel), True, white)
    window.blit(text, text.get_rect(center=(screen_width*3/4, screen_height * 24/30)))

    icon = pygame.image.load(os.path.abspath("C:\\Users\\Lucap\\Desktop\\RIOT_API_Project\\ProfileIcons" + "\\" + str(IconId) + ".png"))
    window.blit(icon, icon.get_rect(center=(screen_width * 3/4, screen_height * 4/9)))

    regularText = pygame.font.SysFont('Georgia', 15)
    def createTextBox(x, y, msg):
        TextSurf, TextRect = text_objects(msg, regularText)
        TextRect.update(x, y, 10, 10)
        window.blit(TextSurf, TextRect)

    average_kda = str(asyncio.run(get_average_kda(puuid, matchHistory)))
    average_cs_diff = str(asyncio.run(get_average_cs_diff(puuid, matchHistory)))
    winrate = str(asyncio.run(get_winrate(puuid, matchHistory)))

    xAlignment1 = screen_width * 1/12
    createTextBox(xAlignment1, screen_height*1/7, 'Average KDA: ' + average_kda)
    createTextBox(xAlignment1, screen_height*2/7, 'Average CS Deficit/Lead: ' + average_cs_diff)
    createTextBox(xAlignment1, screen_height*3/7, 'Winrate: ' + winrate + '%' )

    superSmallText = pygame.font.SysFont("Georgia",20)
    TextSurf, TextRect = text_objects('Data taken from last ' + str(len(matchHistory)) + ' games', superSmallText)
    TextRect.update(screen_width/40, screen_height/30, 10, 10)
    window.blit(TextSurf, TextRect)

    asyncio.run(display_championMastery(puuid))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if clock exit, quit game
                pygame.quit()
                quit()

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def get_tasks(session, matchHistory):
        asyncMatchHistory = []
        for match in matchHistory:
            time.sleep(0.50)
            asyncMatchHistory.append(session.get('https://americas.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api_key, ssl=False))
        return asyncMatchHistory

async def get_average_kda(puuid, matchHistory):
    async with aiohttp.ClientSession() as session:
        sum = 0 
        matchHistory = get_tasks(session, matchHistory)
        matchHistory = await asyncio.gather(*matchHistory)
        for match in matchHistory:
            match = await match.json()
            player_index = match['metadata']['participants'].index(puuid)
            sum += match['info']['participants'][player_index]['challenges']['kda']
        
        KDA =  str(sum / len(matchHistory))
        KDA = float(KDA[0:4])
        return str(KDA)

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

async def get_winrate(puuid, matchHistory):
    async with aiohttp.ClientSession() as session:  
        wins = 0
        total_games = len(matchHistory)
        matchHistory = get_tasks(session, matchHistory)
        matchHistory = await asyncio.gather(*matchHistory)

        for match in matchHistory:
            match = await match.json()
            myIndex = match['metadata']['participants'].index(puuid)
            if match['info']['participants'][myIndex]['win'] == True:
                wins += 1
        
        wins = wins / total_games
        winrate = str(wins)
        winrate = float(winrate[0:5])
        winrate = str(float(winrate) * 100)[0:2]

        return winrate

async def display_championMastery(puuid):
    api_url = 'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/' + puuid + '/top?count=3&api_key=' + api_key

    async with aiohttp.ClientSession() as session:
            resp = await session.get(api_url)
            topMasteries = await resp.json()
            space = 14
            for mastery in topMasteries:
                space += 1
                x = screen_width * (space / 18)
                championId = mastery['championId']
                championName = championIdToName[str(championId)]
                championIcon = pygame.image.load(os.path.abspath("C:\\Users\\Lucap\\Desktop\\RIOT_API_Project\\champion" + "\\" + championName + ".png"))
                championIcon = pygame.transform.smoothscale(championIcon, (championIcon.get_width()*1/2, championIcon.get_height()*1/2))
                window.blit(championIcon, championIcon.get_rect(center=(x, screen_height*9/10)))

pygame.display.set_caption("Riot Api Project")
enter_riot_id()