
import requests
import pygame
import functions


black = (0,0,0)
white = (255,255,255)

api_key = 'RGAPI-267c12a7-85cd-4d85-9f5e-ea9d4d1645a3'
api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/llimeincoconut/0000'


puuid = functions.get_puuid('llimeincoconut', '0000', api_key)


match_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?start=0&count=20' + '&api_key=' + api_key
print(puuid)
resp = requests.get(match_url)
match_history = resp.json()


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
    input_box1 = InputBox(screen_width/2-100, screen_height/2, 140, 32)

    input_boxes = [input_box1]
    while game_start: #start screen loop
        for event in pygame.event.get():
                if event.type == pygame.QUIT: #if clock exit, quit game
                    pygame.quit()
                    quit()
                for box in input_boxes:
                    box.handle_event(event)
        window.fill(black)
        #^ fill in screen black

        for box in input_boxes:
            box.update()
            box.draw(screen)
        
        #^add image of a chicken


        clock = pygame.time.Clock()
        #^ clock for death screen

        largeText = pygame.font.SysFont("ariel",25)
        #^ create font to render in text

        #^^ create text boxes for Final Score and Final level for death screen
        TextSurf, TextRect = text_objects("Please Enter Your Riot name and Riot Id", largeText)

        #^^ create text boxes for welcoming text
        TextRect.center = ((screen_width/2),(screen_height/5.5))
        #^^ set the location of the text boxes
        window.blit(TextSurf, TextRect)
        #^ render text onto the window

        #quit and restart buttons^
        pygame.display.update()
        clock.tick(15)

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
            print(action)
            action()
    else: # if no action, meaning button not clicked, then render buttons
        pygame.draw.rect(window, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        window.blit(textSurf, textRect)


pygame.init()
screen = pygame.display.set_mode((640, 480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

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
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


pygame.init()
window = pygame.display.set_mode((500, 500))
game_start_screen()



        

