import random


# handling functions for the obstacle objects
class Obstacle:
    def __init__(self, image, type, screen_width):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


# creates the different obstacle objects
class SmallCactus(Obstacle):
    def __init__(self, image, screen_width):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, screen_width)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, screen_width):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, screen_width)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image, screen_width):
        self.type = 0
        super().__init__(image, self.type, screen_width)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Powerup(Obstacle):
    def __init__(self, image, screen_width):
        self.type = 0
        super().__init__(image, self.type, screen_width)
        self.rect.y = 250

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
