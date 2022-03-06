import pygame


# Set the object that houses the textures for the game
class Texturer:
    def __init__(self, filename):
        self.base_image_run = pygame.image.load('Assets/base_game/Dino/DinoRun1.png')
        self.image_size_run = self.base_image_run.get_size()
        self.base_image_jump = pygame.image.load('Assets/base_game/Dino/DinoJump.png')
        self.image_size_jump = self.base_image_jump.get_size()
        self.base_image_duck = pygame.image.load('Assets/base_game/Dino/DinoDuck1.png')
        self.image_size_duck = self.base_image_duck.get_size()

        self.RUNNING = [
            pygame.transform.scale(pygame.image.load('Assets/{}/Dino/DinoRun1.png'.format(filename)),
                                   self.image_size_run),
            pygame.transform.scale(pygame.image.load('Assets/{}/Dino/DinoRun2.png'.format(filename)),
                                   self.image_size_run)
        ]

        self.DUCKING = [
            pygame.transform.scale(pygame.image.load('Assets/{}/Dino/DinoDuck1.png'.format(filename)),
                                   self.image_size_duck),
            pygame.transform.scale(pygame.image.load('Assets/{}/Dino/DinoDuck2.png'.format(filename)),
                                   self.image_size_duck)
        ]

        self.JUMPING = pygame.transform.scale(pygame.image.load('Assets/{}/Dino/DinoJump.png'.format(filename)),
                                              self.image_size_jump)

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

