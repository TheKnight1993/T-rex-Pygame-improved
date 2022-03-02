import pygame
from dino import Dino
from cloud import Cloud
from obstacles import *
from texturer import Texturer
import json

pygame.init()
# constants and preset variables
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
DIFFICULTY_SELECTOR = 3  # difficulty selector takes a numeric value, can be set via the menu
POINT_SPEED_MODIFIER = 100  # POINT_SPEED_MODIFIER takes a numeric value, higher values speed up the game less
POINT_GAIN_MODIFIER = 1  # POINT_GAIN_MODIFIER takes a numeric value, higher values give less points
GAME_SPEED_MODIFIER = 0.8
points = 0
ghost_points = 0
coin_cache = 0
game_speed = 10
x_pos_bg = 0
y_pos_bg = 380
obstacles = []
# pygame constants
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
background_image = pygame.image.load('Assets/images/dino-game-background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The T-rex Game')
title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 30)
subtitle_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 25)
button_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 15)
game_over_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 45)
price_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 15)
font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
button_color = (200, 200, 200)
clock = pygame.time.Clock()
# texture file constants/variables
texture_file = 'base_game'
game_textures = Texturer(texture_file)

selectedDifficulty = "Medium"
selectedTheme = "Default theme"


def draw_text_topleft(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(textobj, text_rect)


def draw_text_topright(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect()
    text_rect.topright = (x, y)
    surface.blit(textobj, text_rect)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect()
    text_rect.center = (x, y)
    surface.blit(textobj, text_rect)


def mainLoop():  # the loop that plays the game
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, coin_cache

    run = True
    player = Dino(game_textures)
    cloud = Cloud(SCREEN_WIDTH, game_speed, game_textures)
    death_count = 0
    def score():
        global points, game_speed, POINT_SPEED_MODIFIER, POINT_GAIN_MODIFIER, GAME_SPEED_MODIFIER, ghost_points
        global coin_cache

        ghost_points += 1
        if ghost_points == POINT_GAIN_MODIFIER and ghost_points != 0:
            ghost_points -= POINT_GAIN_MODIFIER
            points += 1
        if points >= 100 and points % POINT_SPEED_MODIFIER == 0 and ghost_points == 0:
            game_speed += GAME_SPEED_MODIFIER
            print(game_speed)
        if points % 100 == 0:
            coin_cache += 1

        draw_text_topright(('Points :' + str(points)), font, (0, 0, 0), SCREEN, 1000, 40)

    def background():
        global x_pos_bg, y_pos_bg

        image_width = game_textures.BG.get_width()
        SCREEN.blit(game_textures.BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(game_textures.BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(game_textures.BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(10)

        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(user_input)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(game_textures.SMALL_CACTI, SCREEN_WIDTH))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(game_textures.LARGE_CACTI, SCREEN_WIDTH))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(game_textures.BIRD, SCREEN_WIDTH))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                obstacles.pop()
                pygame.time.delay(500)
                save_coins(coin_cache)
                coin_cache = 0
                exit(100)
                death_count += 1
                deathMenu()

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(60)
        pygame.display.update()

# TODO: make menu functions with their own lööps
# TODO: make and implement the other menu functions
# TODO: difficulty, powerups and texture select
# TODO: very unlikely: pvp


def pauseMenu():  # right now a barebones copy of what is in what.py
    run = True
    while run:
        SCREEN.fill((200, 200, 200))
        # font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 30)
        text = font.render('Press Any Key To Resume', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 20)
        SCREEN.blit(text, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.KEYDOWN:
                mainLoop()

        clock.tick(60)
        pygame.display.update()


def mainMenu():  # has to become the true main menu, that goes to all the otehr loops
    run = True
    click = False
    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        # title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Main menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        mx, my = pygame.mouse.get_pos()
        button_play = pygame.Rect(50, 175, 200, 30)
        button_options = pygame.Rect(50, 215, 200, 30)
        button_exit = pygame.Rect(50, 255, 200, 30)

        draw_text_topleft("Play", button_font, (50, 50, 50), SCREEN, 60, 185)
        draw_text_topleft("Options", button_font, (50, 50, 50), SCREEN, 60, 225)
        draw_text_topleft("Exit game", button_font, (50, 50, 50), SCREEN, 60, 265)

        pygame.draw.rect(SCREEN, button_color, button_play, 3)
        pygame.draw.rect(SCREEN, button_color, button_options, 3)
        pygame.draw.rect(SCREEN, button_color, button_exit, 3)

        if button_play.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_play)
            draw_text_topleft("Play", button_font, (50, 50, 50), SCREEN, 60, 185)
            if click:
                mainLoop()
        if button_options.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_options)
            draw_text_topleft("Options", button_font, (50, 50, 50), SCREEN, 60, 225)
            if click:
                optionsMenu()
        if button_exit.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_exit)
            draw_text_topleft("Exit game", button_font, (50, 50, 50), SCREEN, 60, 265)
            if click:
                exit()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)


def optionsMenu():
    run = True
    click = False
    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        # title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Options menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        mx, my = pygame.mouse.get_pos()
        button_difficulty = pygame.Rect(50, 175, 200, 30)
        button_themes = pygame.Rect(50, 215, 200, 30)
        button_back = pygame.Rect(50, 500, 200, 30)


        draw_text_topleft("difficulty", button_font, (50, 50, 50), SCREEN, 60, 185)
        draw_text_topleft("Themes", button_font, (50, 50, 50), SCREEN, 60, 225)
        draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_difficulty, 3)
        pygame.draw.rect(SCREEN, button_color, button_themes, 3)
        pygame.draw.rect(SCREEN, button_color, button_back, 3)
        if button_difficulty.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_difficulty)
            draw_text_topleft("difficulty", button_font, (50, 50, 50), SCREEN, 60, 185)
            if click:
                difficultyMenu()
        if button_themes.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_themes)
            draw_text_topleft("Themes", button_font, (50, 50, 50), SCREEN, 60, 225)
            if click:
                textureMenu()
        if button_back.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_back)
            draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)
            if click:
                mainMenu()


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def difficultyMenu():
    run = True
    click = False
    global selectedDifficulty
    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        # title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("difficulty menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        draw_text_topleft("Select your difficulty:", button_font, (50, 50, 50), SCREEN, 50, 150)
        draw_text_topleft("Selected difficulty: " + selectedDifficulty, button_font, (50, 50, 50), SCREEN, 50, 400)
        mx, my = pygame.mouse.get_pos()
        button_easy = pygame.Rect(50, 175, 200, 30)
        button_medium = pygame.Rect(50, 215, 200, 30)
        button_hard = pygame.Rect(50, 255, 200, 30)
        button_back = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Easy", button_font, (50, 50, 50), SCREEN, 60, 185)
        draw_text_topleft("Medium", button_font, (50, 50, 50), SCREEN, 60, 225)
        draw_text_topleft("Hard", button_font, (50, 50, 50), SCREEN, 60, 265)
        draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_easy, 3)
        pygame.draw.rect(SCREEN, button_color, button_medium, 3)
        pygame.draw.rect(SCREEN, button_color, button_hard, 3)
        pygame.draw.rect(SCREEN, button_color, button_back, 3)
        if button_easy.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_easy)
            draw_text_topleft("Easy", button_font, (50, 50, 50), SCREEN, 60, 185)
            if click:
                selectedDifficulty = "Easy"
                pass

        if button_medium.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_medium)
            draw_text_topleft("Medium", button_font, (50, 50, 50), SCREEN, 60, 225)
            if click:
                selectedDifficulty = "Medium"
                pass
        if button_hard.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_hard)
            draw_text_topleft("Hard", button_font, (50, 50, 50), SCREEN, 60, 265)
            if click:
                selectedDifficulty = "Hard"
                pass
        if button_back.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_back)
            draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)
            if click:
                optionsMenu()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def textureMenu():
    run = True
    click = False
    global selectedTheme
    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Theme menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        draw_text_topleft("Select your Theme:", button_font, (50, 50, 50), SCREEN, 50, 150)
        draw_text_topleft("Selected Theme: " + selectedTheme, button_font, (50, 50, 50), SCREEN, 300, 510)
        mx, my = pygame.mouse.get_pos()

        button_default = pygame.Rect(50, 175, 100, 100)
        button_blue = pygame.Rect(160, 175, 100, 100)
        button_red = pygame.Rect(270, 175, 100, 100)
        button_green = pygame.Rect(50, 285, 100, 100)
        button_midnight_blue = pygame.Rect(160, 285, 100, 100)
        button_rainbow = pygame.Rect(270, 285, 100, 100)
        button_7 = pygame.Rect(50, 395, 100, 100)
        button_8 = pygame.Rect(160, 395, 100, 100)
        button_9 = pygame.Rect(270, 395, 100, 100)
        button_back = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_default, 3)
        pygame.draw.rect(SCREEN, button_color, button_blue, 3)
        pygame.draw.rect(SCREEN, button_color, button_red, 3)
        pygame.draw.rect(SCREEN, button_color, button_green, 3)
        pygame.draw.rect(SCREEN, button_color, button_midnight_blue, 3)
        pygame.draw.rect(SCREEN, button_color, button_rainbow, 3)
        pygame.draw.rect(SCREEN, button_color, button_7, 3)
        pygame.draw.rect(SCREEN, button_color, button_8, 3)
        pygame.draw.rect(SCREEN, button_color, button_9, 3)
        pygame.draw.rect(SCREEN, button_color, button_back, 3)

        dinoThemeDefault = pygame.image.load('Assets/base_game/Dino/DinoJumpDefault.png').convert_alpha()
        dinoThemeBlue = pygame.image.load('Assets/base_game/Dino/DinoJumpBlue.png').convert_alpha()
        dinoThemeRed = pygame.image.load('Assets/base_game/Dino/DinoJumpRed.png').convert_alpha()
        dinoThemeGreen = pygame.image.load('Assets/base_game/Dino/DinoJumpGreen.png').convert_alpha()
        dinoThemeMNBlue = pygame.image.load('Assets/base_game/Dino/DinoJumpMNBlue.png').convert_alpha()
        dinoThemeRainbow = pygame.image.load('Assets/base_game/Dino/DinoJumpRainbow.png').convert_alpha()
        themeLock = pygame.image.load('Assets/images/themeLock.png').convert_alpha()
        themeLockHover = pygame.image.load('Assets/images/themeLock.png').convert_alpha()

        dinoThemeBlue = pygame.transform.scale(dinoThemeBlue, (235, 250))
        dinoThemeRed = pygame.transform.scale(dinoThemeRed, (235, 250))
        dinoThemeGreen = pygame.transform.scale(dinoThemeGreen, (235, 250))
        dinoThemeMNBlue = pygame.transform.scale(dinoThemeMNBlue, (235, 250))
        dinoThemeRainbow = pygame.transform.scale(dinoThemeRainbow, (235, 250))
        themeLock = pygame.transform.scale(themeLock, (125, 125))
        themeLockHover = pygame.transform.scale(themeLock, (100, 100))

        SCREEN.blit(dinoThemeDefault, (60, 178))
        SCREEN.blit(dinoThemeBlue, (95, 160))
        SCREEN.blit(dinoThemeRed, (205, 160))
        SCREEN.blit(dinoThemeGreen, (-15, 270))
        SCREEN.blit(dinoThemeMNBlue, (95, 270))
        SCREEN.blit(dinoThemeRainbow, (205, 270))

        blueThemeUnlocked = True
        redThemeUnlocked = False
        greenThemeUnlocked = False
        mnblueThemeUnlocked = False
        rainbowThemeUnlocked = False

        if blueThemeUnlocked == False:
            SCREEN.blit(themeLock, (147, 162))
        if redThemeUnlocked == False:
            SCREEN.blit(themeLock, (257, 162))
        if greenThemeUnlocked == False:
            SCREEN.blit(themeLock, (37, 272))
        if mnblueThemeUnlocked == False:
            SCREEN.blit(themeLock, (147, 272))
        if rainbowThemeUnlocked == False:
            SCREEN.blit(themeLock, (257, 272))

        if button_default.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_default)
            SCREEN.blit(dinoThemeDefault, (60, 178))

            if click:
                selectedTheme = "Default theme"
                pass
        if button_blue.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_blue)
            SCREEN.blit(dinoThemeBlue, (95, 160))
            if blueThemeUnlocked == False:
                SCREEN.blit(themeLockHover, (158, 162))
                draw_text_topleft("1000", price_font, (218, 165, 32), SCREEN, 178, 252)
            if click and blueThemeUnlocked == True:
                selectedTheme = "Blue theme"
                pass
            else:
                # unlock blue theme
                pass
        if button_red.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_red)
            SCREEN.blit(dinoThemeRed, (205, 160))
            if redThemeUnlocked == False:
                SCREEN.blit(themeLockHover, (268, 162))
                draw_text_topleft("2000", price_font, (218, 165, 32), SCREEN, 288, 252)
            if click and redThemeUnlocked == True:
                selectedTheme = "Red theme"
                pass
            else:
                # unlock red theme
                pass
        if button_green.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_green)
            SCREEN.blit(dinoThemeGreen, (-15, 270))
            if greenThemeUnlocked == False:
                SCREEN.blit(themeLockHover, (48, 272))
                draw_text_topleft("3000", price_font, (218, 165, 32), SCREEN, 68, 362)
            if click and greenThemeUnlocked == True:
                selectedTheme = "Green theme"
                pass
            else:
                # unlock green theme
                pass
        if button_midnight_blue.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_midnight_blue)
            SCREEN.blit(dinoThemeMNBlue, (95, 270))
            if mnblueThemeUnlocked == False:
                SCREEN.blit(themeLockHover, (158, 272))
                draw_text_topleft("4000", price_font, (218, 165, 32), SCREEN, 178, 362)
            if click and mnblueThemeUnlocked == True:
                selectedTheme = "Default"
                pass
            else:
                # unlock mnblue theme
                pass
        if button_rainbow.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_rainbow)
            SCREEN.blit(dinoThemeRainbow, (205, 270))
            if rainbowThemeUnlocked == False:
                SCREEN.blit(themeLockHover, (268, 272))
                draw_text_topleft("9999", price_font, (218, 165, 32), SCREEN, 288, 362)
            if click and rainbowThemeUnlocked == True:
                selectedTheme = "rainbow theme"
                pass
            else:
                # unlock rainbow theme
                pass
        if button_back.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_back)
            draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)
            if click:
                optionsMenu()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)


def deathMenu():
    run = True
    click = False
    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        # title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("GAME OVER", game_over_font, (50, 50, 50), SCREEN, 60, 275)

        mx, my = pygame.mouse.get_pos()
        button_mainmenu = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Main menu", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_mainmenu, 3)

        if button_mainmenu.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN,button_color, button_mainmenu)
            draw_text_topleft("Main menu", button_font, (50, 50, 50), SCREEN, 60, 510)
            if click:
                mainMenu()



        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)



# difficulty
def set_modifier(selection_input):
    global DIFFICULTY_SELECTOR, POINT_SPEED_MODIFIER, POINT_GAIN_MODIFIER, GAME_SPEED_MODIFIER

    if selection_input == 1:  # easy difficulty?
        DIFFICULTY_SELECTOR = 1
        POINT_SPEED_MODIFIER = 400
        POINT_GAIN_MODIFIER = 5
        GAME_SPEED_MODIFIER = 0.4
    elif selection_input == 2:  # medium mode
        DIFFICULTY_SELECTOR = 2
        POINT_SPEED_MODIFIER = 200
        POINT_GAIN_MODIFIER = 3
        GAME_SPEED_MODIFIER = 0.8
    elif selection_input == 3:  # hardmode
        DIFFICULTY_SELECTOR = 3
        POINT_SPEED_MODIFIER = 100
        POINT_GAIN_MODIFIER = 1
        GAME_SPEED_MODIFIER = 0.8


# set different textures as texture file
def set_textures(filename):  # simple function to change the textures the game uses, still needs updating
    global game_textures
    game_textures = Texturer(filename)


def check_textures():  # function to check if a texture is unlocked or not
    pass


# coin system functions
def save_coins(gained_coins):  # saves hard-earned coins
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    coin_data = json_data['currency']
    old_coins = coin_data['coins']

    gained_coins = gained_coins + old_coins
    coin_data['coins'] = gained_coins

    json_data['currency'] = coin_data

    data_file.seek(0)
    data_file.truncate()

    json.dump(json_data, data_file, indent=2)
    data_file.close()


def spend_coins(coins_spent, json_data):
    coin_data = json_data['currency']
    old_coins = coin_data['coins']

    old_coins = old_coins - coins_spent
    coin_data['coins'] = old_coins
    return coin_data


def get_coins():
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    coin_data = json_data['currency']
    coins = coin_data['coins']

    data_file.close()
    return coins


def buy_texture(bought_item):  # unlocks unlocked textures
    global texture_file, game_textures, coin_cache

    data_file = open('data.json', 'r+')
    json_data = json.load(data_file)
    texture_data = json_data['textures']

    coins = get_coins()

    total_textures = len(texture_data)
    for i in range(0, total_textures):

        texture = texture_data[i]
        texture_name = texture['texture_name']
        texture_unlocked = texture['texture_unlocked']
        texture_price = texture['texture_price']

        if bought_item == texture_name:

            if not texture_unlocked:

                if coins >= texture_price:

                    texture_unlocked = True
                    coins = spend_coins(texture_price, json_data)
                    print(coins)
                    texture['texture_unlocked'] = texture_unlocked
                    texture_data[i] = texture
                    json_data['textures'] = texture_data
                    json_data['currency'] = coins

    data_file.seek(0)
    data_file.truncate()

    json.dump(json_data, data_file, indent=2)
    data_file.close()


def reset_coins():
    data_file = open('data.json', 'r+')
    json_data = json.load(data_file)
    coin_data = json_data['currency']
    coin_data['coins'] = 0
    json_data['currency'] = coin_data
    data_file.seek(0)
    data_file.truncate()
    json.dump(json_data, data_file, indent=2)
    data_file.close()

mainMenu()
