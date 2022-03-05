import pygame


# Set the object that houses the textures for the game
class Texturer:
    def __init__(self, filename):
        self.RUNNING = [
            pygame.image.load('Assets/{}/Dino/DinoRun1.png'.format(filename)),
            pygame.image.load('Assets/{}/Dino/DinoRun2.png'.format(filename))
        ]
        self.DUCKING = [
            pygame.image.load('Assets/{}/Dino/DinoDuck1.png'.format(filename)),
            pygame.image.load('Assets/{}/Dino/DinoDuck2.png'.format(filename))
        ]
        self.JUMPING = pygame.image.load('Assets/{}/Dino/DinoJump.png'.format(filename))

        self.SMALL_CACTI = [
            pygame.image.load('Assets/base_game/Cactus/SmallCactus1.png'),
            pygame.image.load('Assets/base_game/Cactus/SmallCactus2.png'),
            pygame.image.load('Assets/base_game/Cactus/SmallCactus3.png')
        ]
        self.LARGE_CACTI = [
            pygame.image.load('Assets/base_game/Cactus/LargeCactus1.png'),
            pygame.image.load('Assets/base_game/Cactus/LargeCactus2.png'),
            pygame.image.load('Assets/base_game/Cactus/LargeCactus3.png')
        ]
        self.BIRD = [
            pygame.image.load('Assets/base_game/Bird/Bird1.png'),
            pygame.image.load('Assets/base_game/Bird/Bird2.png')
        ]

        self.CLOUD = pygame.image.load('Assets/base_game/Other/Cloud.png')
        self.BG = pygame.image.load('Assets/base_game/Other/Track.png')

