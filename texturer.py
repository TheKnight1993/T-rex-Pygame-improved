import pygame


# Set the object that houses the textures for the game
class Texturer:
    def __init__(self, filename):
        self.RUNNING = [
            pygame.image.load('Assets/{}/Dino/DinoRunDefault1.png'.format(filename)),
            pygame.image.load('Assets/{}/Dino/DinoRunDefault2.png'.format(filename))
        ]
        self.DUCKING = [
            pygame.image.load('Assets/{}/Dino/DinoDuckDefault1.png'.format(filename)),
            pygame.image.load('Assets/{}/Dino/DinoDuckDefault2.png'.format(filename))
        ]
        self.JUMPING = pygame.image.load('Assets/{}/Dino/DinoJumpDefault.png'.format(filename))

        self.SMALL_CACTI = [
            pygame.image.load('Assets/{}/Cactus/SmallCactus1.png'.format(filename)),
            pygame.image.load('Assets/{}/Cactus/SmallCactus2.png'.format(filename)),
            pygame.image.load('Assets/{}/Cactus/SmallCactus3.png'.format(filename))
        ]
        self.LARGE_CACTI = [
            pygame.image.load('Assets/{}/Cactus/LargeCactus1.png'.format(filename)),
            pygame.image.load('Assets/{}/Cactus/LargeCactus2.png'.format(filename)),
            pygame.image.load('Assets/{}/Cactus/LargeCactus3.png'.format(filename))
        ]
        self.BIRD = [
            pygame.image.load('Assets/{}/Bird/Bird1.png'.format(filename)),
            pygame.image.load('Assets/{}/Bird/Bird2.png'.format(filename))
        ]

        self.CLOUD = pygame.image.load('Assets/{}/Other/Cloud.png'.format(filename))
        self.BG = pygame.image.load('Assets/{}/Other/Track.png'.format(filename))

