
import requests
import pygame
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
screen_width = 500
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
COLOR_INACTIVE = pygame.Color('lightskyblue3')
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
    input_riot_id = SummonerIDInputBox(screen_width/1.3, screen_height/2, 300, 25)
    input_boxes = [input_riot_id]
    while not done: 
        for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    quit()
                for box in input_boxes:
                    done, text = box.handle_event(event)
        window.fill(black)

        for box in input_boxes:
            box.update()
            box.draw(screen)
        

        largeText = pygame.font.SysFont("ariel",25)

        TextSurf, TextRect = text_objects("Please Enter Your Riot name and Riot Id", largeText)
 
        TextRect.center = ((screen_width/1.035),(screen_height/3))

        window.blit(TextSurf, TextRect)
 
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)
    choose_analysis_screen(text)

def choose_analysis_screen(riot_id_and_name):
    riot_id_and_name = riot_id_and_name.split("#")
    riot_name = riot_id_and_name[0]
    riot_id = riot_id_and_name[1]
    puuid = get_puuid(riot_name, riot_id, api_key)
    match_history = get_match_history(puuid, api_key)
    done = False
    window.fill(black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if clock exit, quit game
                pygame.quit()
                quit()
        button('average kda', screen_width/2, screen_height/2, 100, 100, green, bright_green, lambda: display_average_kda(puuid, match_history, api_key))

        largeText = pygame.font.SysFont("Georgia",25)

        TextSurf, TextRect = text_objects('Data taken from the last ' + str(len(match_history)) + ' games', largeText)
        TextRect.center = ((screen_width/2),(screen_height/6))
        window.blit(TextSurf, TextRect)


        pygame.display.update()



        clock = pygame.time.Clock()
        clock.tick(15)
    


def display_average_kda(puuid, match_history, api_key):
    average_kda = get_average_kda(puuid, match_history, api_key)
    statText = pygame.font.SysFont("Georgia",20)
    textSurf, textRect = text_objects(str(average_kda), statText)
    window.blit(textSurf, textRect)

def get_average_kda(puuid, match_history, api_key):
    sum = 0 
    for match in match_history:
        api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api_key
        resp = requests.get(api_url)
        match_broad = resp.json()
        player_index = match_broad['metadata']['participants'].index(puuid)
        playerGameStats = match_broad['info']['participants'][player_index]['challenges']
        sum += playerGameStats['kda']
    return sum / len(match_history)

def get_puuid(name, riot_id, api_key):
    puuid_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' + name + '/' + riot_id + '?api_key=' + api_key
    resp = requests.get(puuid_url)
    account_info = resp.json()
    puuid = account_info["puuid"]
    return puuid

def get_match_history(puuid, api_key):
    api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=20&api_key='+ api_key
    resp = requests.get(api_url)
    match_history = resp.json()
    return match_history 




window = pygame.display.set_mode((1000,550))
enter_riot_id()



        

