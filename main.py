import pygame
from dino import Dino
from cloud import Cloud
from obstacles import *
from texturer import Texturer
import json

pygame.init()
# preset variables; are constant or are used in calculations
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
POINT_SPEED_MODIFIER = 200  # takes a numeric value, higher values speed up the game less
POINT_GAIN_MODIFIER = 3  # takes a numeric value, higher values give less points
GAME_SPEED_MODIFIER = 0.8  # takes a numeric value, higher values give a more difficult game
points = 0
finalPoints = 0  # used to pass the amount of points gained to the death menu
ghost_points = 0  # used in calculations to lower the amount of points gained
game_speed = 10  # used to define how quickly the game moves
x_pos_bg = 0  # used to scroll the background
y_pos_bg = 380  # sets the height of the background
obstacles = []  # the list of obstacles to be able to remove them from memory
# pygame constants
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # sets the window to be displayed
background_image = pygame.transform.scale(pygame.image.load('Assets/images/dino-game-background.png'),
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The T-rex Game')
# fonts used in the menus and in the game
title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 30)
subtitle_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 25)
button_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 15)
game_over_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 45)
price_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 15)
font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
button_color = (200, 200, 200)
texture_file = 'base_game'  # sets the variable which houses the name for the texture
game_textures = Texturer(texture_file)  # sets the object that houses all the game textures
powerup = Powerup(game_textures.POWERUP, SCREEN_WIDTH)  # sets the object for powerups to be able to use it separately
clock = pygame.time.Clock()

# further variables that are being used
powerupFrame = False
invisFrame = False
selectedDifficulty = "Medium"
selectedTheme = "Default theme"
jumpPowerupActivated = False
shieldPowerupActivated = False
scorePowerupActivated = False
powerupActivated = False
jumpPowerupStartTime = 0
pointsPowerupStartTime = 0
jumpTimer = False
showPoints = False


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


def mainLoop():  # the loop that plays the game
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, livesAmount, invisFrame, powerupFrame
    global jumpPowerupActivated, shieldPowerupActivated, scorePowerupActivated, powerupActivated, jumpPowerupStartTime
    global POINT_GAIN_MODIFIER, finalPoints, powerup, showPoints, pointsPowerupStartTime, scoreTimer
    global JUMPAMOUNT, livesAmount, jumpTimer

    run = True
    player = Dino(game_textures)
    cloud = Cloud(SCREEN_WIDTH, game_speed, game_textures)

    # function to update the score including different speed
    def score():
        global points, game_speed, POINT_SPEED_MODIFIER, POINT_GAIN_MODIFIER, GAME_SPEED_MODIFIER, ghost_points

        ghost_points += 1
        if ghost_points == POINT_GAIN_MODIFIER and ghost_points != 0:
            ghost_points -= POINT_GAIN_MODIFIER
            points += 1
        if points >= 100 and points % POINT_SPEED_MODIFIER == 0 and ghost_points == 0:
            game_speed += GAME_SPEED_MODIFIER

        draw_text_topright(('Points :' + str(points)), font, (0, 0, 0), SCREEN, 1000, 40)

    # function to draw the background
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
        # checks if the window close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(user_input)

        # displays how many lives the player has
        heart = pygame.transform.scale(pygame.image.load('Assets/images/heart.png'), (30, 30))
        if 0 < player.livesAmount < 4:
            SCREEN.blit(heart, (20, 20))
        if 1 < player.livesAmount < 4:
            SCREEN.blit(heart, (50, 20))
        if 2 < player.livesAmount < 4:
            SCREEN.blit(heart, (80, 20))
        if player.livesAmount > 3:
            draw_text_topleft("Your Lives: " + str(player.livesAmount), font, (0, 0, 0), SCREEN, 20, 30)

        # checks if there are no obstacles on screen and randomly chooses a new obstacle
        if len(obstacles) == 0:
            randomChoice = random.randint(1, 100)
            powerup.rect.y = 250
            if randomChoice <= 32:
                obstacles.append(SmallCactus(game_textures.SMALL_CACTI, SCREEN_WIDTH))
                powerupActivated = False
            elif randomChoice <= 64:
                obstacles.append(LargeCactus(game_textures.LARGE_CACTI, SCREEN_WIDTH))
                powerupActivated = False
            elif randomChoice <= 96:
                obstacles.append(Bird(game_textures.BIRD, SCREEN_WIDTH))
                powerupActivated = False
            elif randomChoice <= 100:
                powerup = Powerup(game_textures.POWERUP, SCREEN_WIDTH)
                obstacles.append(powerup)
                powerupActivated = True

        # loop to update obstacles (powerup and normal) and check for interactions
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(game_speed, obstacles)
            # randomly selects a powerup if the powerup obstacle was interacted with
            if player.dino_rect.colliderect(obstacle.rect) and powerupActivated:
                powerup.rect.y = 100000
                randomPowerup = random.randint(0, 99)
                powerupFrame = True
                if randomPowerup < 33:
                    shieldPowerupActivated = True
                elif randomPowerup < 66:
                    jumpPowerupActivated = True
                elif randomPowerup < 99:
                    scorePowerupActivated = True
            if not player.dino_rect.colliderect(obstacle.rect) and powerupFrame:  # used to make sure of no double powerups
                powerupFrame = False
            if shieldPowerupActivated:  # adds a life as a 'shield'
                player.livesAmount += 1
                shieldPowerupActivated = False
            if jumpPowerupActivated:  # adds a jump for a double jump
                player.JUMPAMOUNT += 1
                player.jumpAmount += 1
                jumpPowerupActivated = False
                player.jumpPowerup = True
                jumpPowerupStartTime = pygame.time.get_ticks()
                jumpTimer = True
            if player.jumpPowerup:  # draws the message that notifies the player of the activated jump powerup
                draw_text_topleft("Double Jump Activated", font, (0, 0, 0), SCREEN, 20, 50)
            if (pygame.time.get_ticks() - jumpPowerupStartTime) > 15000 and player.running and jumpTimer:
                # removes the extra jump after 15 seconds
                player.JUMPAMOUNT -= 1
                player.jumpAmount -= 1
                player.jumpPowerup = False
                jumpPowerupStartTime = 0
                jumpTimer = False
            if scorePowerupActivated:  # gives the player an amount of points based on the game speed
                points += 50 * int(game_speed)
                scorePowerupActivated = False
                showPoints = True
                pointsPowerupStartTime = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - pointsPowerupStartTime) > 2500 and showPoints:
                showPoints = False

            if showPoints:  # notifies the player if the bonus points powerup has been activated
                draw_text_topleft("Bonus Points!", subtitle_font, (0, 0, 0), SCREEN, 400, 150)

            # checks if the player interacts with a normal obstacle and lowers the amount of lives
            if player.dino_rect.colliderect(obstacle.rect) and not invisFrame and not powerupActivated:
                player.livesAmount -= 1
                invisFrame = True  # used to not take away too many lives
            if not player.dino_rect.colliderect(obstacle.rect) and invisFrame:
                invisFrame = False
            if player.livesAmount < 1:  # if the player has no lives this is called and ends the run
                obstacles.pop()
                powerupFrame = False
                invisFrame = False
                jumpPowerupActivated = False
                shieldPowerupActivated = False
                scorePowerupActivated = False
                powerupActivated = False
                jumpPowerupStartTime = 0
                player.JUMPAMOUNT = 1
                pygame.time.delay(250)
                save_coins(int(points / 100))
                finalPoints = points
                save_highscore(finalPoints)
                points = 0
                ghost_points = 0
                game_speed = 10
                player.livesAmount = 1
                deathMenu()

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(60)
        pygame.display.update()


def mainMenu():  # the main menu, runs the game and has access to different submenus and exiting the game
    run = True
    click = False

    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Main menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)

        draw_text_topright(str(get_coins()), price_font, (50, 50, 50), SCREEN, 1050, 47)
        coin = pygame.image.load('Assets/images/coin.jpg').convert_alpha()
        coin = pygame.transform.scale(coin, (35, 35))
        SCREEN.blit(coin, (1050, 35))

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


def optionsMenu():  # the menu that has access to the 2 submenus for changing the difficulty and the game textures
    run = True
    click = False

    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Options menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)

        draw_text_topright(str(get_coins()), price_font, (50, 50, 50), SCREEN, 1050, 47)
        coin = pygame.image.load('Assets/images/coin.jpg').convert_alpha()
        coin = pygame.transform.scale(coin, (35, 35))
        SCREEN.blit(coin, (1050, 35))

        mx, my = pygame.mouse.get_pos()
        button_difficulty = pygame.Rect(50, 175, 200, 30)
        button_themes = pygame.Rect(50, 215, 200, 30)
        button_back = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Difficulty", button_font, (50, 50, 50), SCREEN, 60, 185)
        draw_text_topleft("Themes", button_font, (50, 50, 50), SCREEN, 60, 225)
        draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_difficulty, 3)
        pygame.draw.rect(SCREEN, button_color, button_themes, 3)
        pygame.draw.rect(SCREEN, button_color, button_back, 3)
        if button_difficulty.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_difficulty)
            draw_text_topleft("Difficulty", button_font, (50, 50, 50), SCREEN, 60, 185)
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


def difficultyMenu():  # menu to select a different difficulty for the game
    global POINT_SPEED_MODIFIER, POINT_GAIN_MODIFIER, GAME_SPEED_MODIFIER, selectedDifficulty
    run = True
    click = False

    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        # title_font = pygame.font.Font('Assets/font/PressStart2P-Regular.ttf', 20)
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Difficulty menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        draw_text_topleft("Select your difficulty:", button_font, (50, 50, 50), SCREEN, 50, 150)
        draw_text_topleft("Selected difficulty: " + selectedDifficulty, button_font, (50, 50, 50), SCREEN, 50, 400)

        draw_text_topright(str(get_coins()), price_font, (50, 50, 50), SCREEN, 1050, 47)
        coin = pygame.image.load('Assets/images/coin.jpg').convert_alpha()
        coin = pygame.transform.scale(coin, (35, 35))
        SCREEN.blit(coin, (1050, 35))

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
                POINT_SPEED_MODIFIER = 400
                POINT_GAIN_MODIFIER = 5
                GAME_SPEED_MODIFIER = 0.4
        if button_medium.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_medium)
            draw_text_topleft("Medium", button_font, (50, 50, 50), SCREEN, 60, 225)
            if click:
                selectedDifficulty = "Medium"
                POINT_SPEED_MODIFIER = 200
                POINT_GAIN_MODIFIER = 3
                GAME_SPEED_MODIFIER = 0.8
        if button_hard.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_hard)
            draw_text_topleft("Hard", button_font, (50, 50, 50), SCREEN, 60, 265)
            if click:
                selectedDifficulty = "Hard"
                POINT_SPEED_MODIFIER = 100
                POINT_GAIN_MODIFIER = 2
                GAME_SPEED_MODIFIER = 0.8
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
    global selectedTheme, game_textures
    run = True
    click = False

    while run:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(background_image, (0, 0))
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("Theme menu", subtitle_font, (50, 50, 50), SCREEN, 110, 85)
        draw_text_topleft("Select your Theme:", button_font, (50, 50, 50), SCREEN, 50, 150)
        draw_text_topleft("Selected Theme: " + selectedTheme, button_font, (50, 50, 50), SCREEN, 300, 510)
        draw_text_topright(str(get_coins()), price_font, (50, 50, 50), SCREEN, 1050, 47)
        coin = pygame.image.load('Assets/images/coin.jpg').convert_alpha()
        coin = pygame.transform.scale(coin, (35, 35))
        SCREEN.blit(coin, (1050, 35))

        mx, my = pygame.mouse.get_pos()

        button_default = pygame.Rect(50, 175, 100, 100)
        button_blue = pygame.Rect(160, 175, 100, 100)
        button_red = pygame.Rect(270, 175, 100, 100)
        button_green = pygame.Rect(50, 285, 100, 100)
        button_midnight_blue = pygame.Rect(160, 285, 100, 100)
        button_rainbow = pygame.Rect(270, 285, 100, 100)
        button_mario = pygame.Rect(50, 395, 100, 100)
        button_luigi = pygame.Rect(160, 395, 100, 100)
        button_toad = pygame.Rect(270, 395, 100, 100)
        button_back = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Back", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_default, 3)
        pygame.draw.rect(SCREEN, button_color, button_blue, 3)
        pygame.draw.rect(SCREEN, button_color, button_red, 3)
        pygame.draw.rect(SCREEN, button_color, button_green, 3)
        pygame.draw.rect(SCREEN, button_color, button_midnight_blue, 3)
        pygame.draw.rect(SCREEN, button_color, button_rainbow, 3)
        pygame.draw.rect(SCREEN, button_color, button_mario, 3)
        pygame.draw.rect(SCREEN, button_color, button_luigi, 3)
        pygame.draw.rect(SCREEN, button_color, button_toad, 3)
        pygame.draw.rect(SCREEN, button_color, button_back, 3)

        dinoThemeDefault = pygame.image.load('Assets/base_game/Dino/DinoJump.png').convert_alpha()
        dinoThemeBlue = pygame.image.load('Assets/blue/Dino/DinoJump.png').convert_alpha()
        dinoThemeRed = pygame.image.load('Assets/red/Dino/DinoJump.png').convert_alpha()
        dinoThemeGreen = pygame.image.load('Assets/green/Dino/DinoJump.png').convert_alpha()
        dinoThemeMNBlue = pygame.image.load('Assets/midnight/Dino/DinoJump.png').convert_alpha()
        dinoThemeRainbow = pygame.image.load('Assets/rainbow/Dino/DinoJump.png').convert_alpha()
        themeLock = pygame.image.load('Assets/images/themeLock.png').convert_alpha()
        dinoMario = pygame.image.load('Assets/mario/Dino/DinoRun1.png').convert_alpha()
        dinoLuigi = pygame.image.load('Assets/luigi/Dino/DinoRun1.png').convert_alpha()
        dinoToad = pygame.image.load('Assets/toad/Dino/DinoRun1.png').convert_alpha()

        dinoThemeSize = dinoThemeDefault.get_size()
        dinoThemeBlue = pygame.transform.scale(dinoThemeBlue, dinoThemeSize)
        dinoThemeRed = pygame.transform.scale(dinoThemeRed, dinoThemeSize)
        dinoThemeGreen = pygame.transform.scale(dinoThemeGreen, dinoThemeSize)
        dinoThemeMNBlue = pygame.transform.scale(dinoThemeMNBlue, dinoThemeSize)
        dinoThemeRainbow = pygame.transform.scale(dinoThemeRainbow, dinoThemeSize)

        dinoMario = pygame.transform.scale(dinoMario, (70, 90))
        dinoLuigi = pygame.transform.scale(dinoLuigi, (70, 90))
        dinoToad = pygame.transform.scale(dinoToad, (70, 90))
        themeLock = pygame.transform.scale(themeLock, (125, 125))
        themeLockHover = pygame.transform.scale(themeLock, (100, 100))

        SCREEN.blit(dinoThemeDefault, (60, 178))

        SCREEN.blit(dinoThemeBlue, (165, 175))
        SCREEN.blit(dinoThemeRed, (275, 175))
        SCREEN.blit(dinoThemeGreen, (55, 285))
        SCREEN.blit(dinoThemeMNBlue, (165, 285))
        SCREEN.blit(dinoThemeRainbow, (275, 285))
        SCREEN.blit(dinoMario, (60, 400))
        SCREEN.blit(dinoLuigi, (170, 400))
        SCREEN.blit(dinoToad, (280, 400))

        blueThemeUnlocked, blueThemePrice = check_textures("blue")
        redThemeUnlocked, redThemePrice = check_textures("red")
        greenThemeUnlocked, greenThemePrice = check_textures("green")
        mnblueThemeUnlocked, mnblueThemePrice = check_textures("midnight")
        rainbowThemeUnlocked, rainbowThemePrice = check_textures("rainbow")
        marioThemeUnlocked, marioThemePrice = check_textures("mario")
        luigiThemeUnlocked, luigiThemePrice = check_textures("luigi")
        toadThemeUnlocked, toadThemePrice = check_textures("toad")

        if not blueThemeUnlocked:
            SCREEN.blit(themeLock, (147, 162))
        if not redThemeUnlocked:
            SCREEN.blit(themeLock, (257, 162))
        if not greenThemeUnlocked:
            SCREEN.blit(themeLock, (37, 272))
        if not mnblueThemeUnlocked:
            SCREEN.blit(themeLock, (147, 272))
        if not rainbowThemeUnlocked:
            SCREEN.blit(themeLock, (257, 272))
        if not marioThemeUnlocked:
            SCREEN.blit(themeLock, (37, 382))
        if not luigiThemeUnlocked:
            SCREEN.blit(themeLock, (147, 382))
        if not toadThemeUnlocked:
            SCREEN.blit(themeLock, (257, 382))

        if button_default.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_default)
            SCREEN.blit(dinoThemeDefault, (60, 178))

            if click:
                selectedTheme = "Default theme"
                game_textures = Texturer("base_game")
        if button_blue.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_blue)
            SCREEN.blit(dinoThemeBlue, (165, 175))
            if not blueThemeUnlocked:
                SCREEN.blit(themeLockHover, (158, 162))
                draw_text_topleft(blueThemePrice, price_font, (218, 165, 32), SCREEN, 178, 252)
            if click and blueThemeUnlocked:
                selectedTheme = "Blue theme"
                game_textures = Texturer("blue")
            elif click and not blueThemeUnlocked:
                unlock_texture("blue")
                game_textures = Texturer("blue")
        if button_red.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_red)
            SCREEN.blit(dinoThemeRed, (275, 175))
            if not redThemeUnlocked:
                SCREEN.blit(themeLockHover, (268, 162))
                draw_text_topleft(redThemePrice, price_font, (218, 165, 32), SCREEN, 288, 252)
            if click and redThemeUnlocked:
                selectedTheme = "Red theme"
                game_textures = Texturer("red")
            elif click and not redThemeUnlocked:
                unlock_texture("red")
                game_textures = Texturer("red")
        if button_green.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_green)
            SCREEN.blit(dinoThemeGreen, (55, 285))
            if not greenThemeUnlocked:
                SCREEN.blit(themeLockHover, (48, 272))
                draw_text_topleft(greenThemePrice, price_font, (218, 165, 32), SCREEN, 68, 362)
            if click and greenThemeUnlocked:
                selectedTheme = "Green theme"
                game_textures = Texturer("green")
            elif click and not greenThemeUnlocked:
                unlock_texture("green")
                game_textures = Texturer("green")
        if button_midnight_blue.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_midnight_blue)
            SCREEN.blit(dinoThemeMNBlue, (165, 285))
            if not mnblueThemeUnlocked:
                SCREEN.blit(themeLockHover, (158, 272))
                draw_text_topleft(mnblueThemePrice, price_font, (218, 165, 32), SCREEN, 178, 362)
            if click and mnblueThemeUnlocked:
                selectedTheme = "Midnight Blue theme"
                game_textures = Texturer("midnight")
            elif click and not mnblueThemeUnlocked:
                unlock_texture("midnight")
                game_textures = Texturer("midnight")
        if button_rainbow.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_rainbow)
            SCREEN.blit(dinoThemeRainbow, (275, 285))
            if not rainbowThemeUnlocked:
                SCREEN.blit(themeLockHover, (268, 272))
                draw_text_topleft(rainbowThemePrice, price_font, (218, 165, 32), SCREEN, 288, 362)
            if click and rainbowThemeUnlocked:
                selectedTheme = "rainbow theme"
                game_textures = Texturer("rainbow")
            elif click and not rainbowThemeUnlocked:
                unlock_texture("rainbow")
                game_textures = Texturer("rainbow")
        if button_mario.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_mario)
            SCREEN.blit(dinoMario, (60, 400))
            if not marioThemeUnlocked:
                SCREEN.blit(themeLockHover, (48, 382))
                draw_text_topleft(marioThemePrice, price_font, (218, 165, 32), SCREEN, 68, 472)
            if click and marioThemeUnlocked:
                selectedTheme = "Mario theme"
                game_textures = Texturer("mario")
            elif click and not marioThemeUnlocked:
                unlock_texture("mario")
                game_textures = Texturer("mario")
        if button_luigi.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_luigi)
            SCREEN.blit(dinoLuigi, (170, 400))
            if not luigiThemeUnlocked:
                SCREEN.blit(themeLockHover, (158, 382))
                draw_text_topleft(luigiThemePrice, price_font, (218, 165, 32), SCREEN, 178, 472)
            if click and luigiThemeUnlocked:
                selectedTheme = "Luigi theme"
                game_textures = Texturer("luigi")
            elif click and not luigiThemeUnlocked:
                unlock_texture("luigi")
                game_textures = Texturer("luigi")
        if button_toad.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_toad)
            SCREEN.blit(dinoToad, (280, 400))
            if not toadThemeUnlocked:
                SCREEN.blit(themeLockHover, (268, 382))
                draw_text_topleft(toadThemePrice, price_font, (218, 165, 32), SCREEN, 288, 472)
            if click and toadThemeUnlocked:
                selectedTheme = "Toad theme"
                game_textures = Texturer("toad")
            elif click and not toadThemeUnlocked:
                unlock_texture("toad")
                game_textures = Texturer("toad")
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
        draw_text_topleft("The T-Rex Runner Game", title_font, (50, 50, 50), SCREEN, 100, 50)
        draw_text_topleft("GAME OVER", game_over_font, (50, 50, 50), SCREEN, 60, 275)
        draw_text_topleft("Score: " + str(finalPoints), font, (50, 50, 50), SCREEN, 60, 400)
        draw_text_topleft("Highscore: " + str(get_highscore()), font, (50, 50, 50), SCREEN, 60, 425)
        draw_text_topright(str(get_coins()), price_font, (50, 50, 50), SCREEN, 1050, 47)
        coin = pygame.image.load('Assets/images/coin.jpg').convert_alpha()
        coin = pygame.transform.scale(coin, (35, 35))
        SCREEN.blit(coin, (1050, 35))

        mx, my = pygame.mouse.get_pos()
        button_mainmenu = pygame.Rect(50, 500, 200, 30)

        draw_text_topleft("Main menu", button_font, (50, 50, 50), SCREEN, 60, 510)

        pygame.draw.rect(SCREEN, button_color, button_mainmenu, 3)

        if button_mainmenu.collidepoint((mx, my)):
            pygame.draw.rect(SCREEN, button_color, button_mainmenu)
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


def spend_coins(coins_spent, json_data):  # spends a certain amount of coins
    coin_data = json_data['currency']
    old_coins = coin_data['coins']

    old_coins = old_coins - coins_spent
    coin_data['coins'] = old_coins
    return coin_data


def get_coins():  # returns the amount of coins one has acquired
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    coin_data = json_data['currency']
    coins = coin_data['coins']

    data_file.close()
    return coins


# texture system functions
def unlock_texture(theme_name):  # unlocks locked textures
    global texture_file, game_textures

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

        if theme_name == texture_name:

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


def check_textures(theme_name):  # checks if a given texture is unlocked
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    texture_data = json_data['textures']

    data_file.close()

    total_textures = len(texture_data)
    for i in range(0, total_textures):

        texture = texture_data[i]
        texture_name = texture['texture_name']
        texture_unlocked = texture['texture_unlocked']
        texture_price = texture['texture_price']

        if texture_name == theme_name:
            texture_price = str(texture_price)
            return texture_unlocked, texture_price


def get_highscore():  # gives the current high score
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    highscore = json_data['highscore']

    data_file.close()
    return highscore


def save_highscore(new_score):  # saves a possible new high score
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    old_highscore = json_data['highscore']
    if new_score > get_highscore():
        json_data['highscore'] = new_score
    else:
        json_data['highscore'] = old_highscore

    data_file.seek(0)
    data_file.truncate()

    json.dump(json_data, data_file, indent=2)
    data_file.close()


# reset functions are for testing purposes
def reset_textures():  # resets the unlocked property of all textures to false
    data_file = open('data.json', 'r+')

    json_data = json.load(data_file)
    texture_data = json_data['textures']

    total_textures = len(texture_data)
    for i in range(0, total_textures):
        texture = texture_data[i]
        if texture['texture_unlocked']:
            texture['texture_unlocked'] = False
            texture_data[i] = texture
            json_data['textures'] = texture_data

    data_file.seek(0)
    data_file.truncate()

    json.dump(json_data, data_file, indent=2)
    data_file.close()


def reset_coins():  # resets the amount of coins to 0
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
