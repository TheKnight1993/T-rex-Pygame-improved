import pygame

jumpFrame = False
# creates and handles the dino object
class Dino:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    def __init__(self, textures):
        self.running, self.ducking, self.jumping = True, False, False

        self.run_img = textures.RUNNING
        self.duck_img = textures.DUCKING
        self.jump_img = textures.JUMPING

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.JUMPAMOUNT = 1
        self.jumpAmount = self.JUMPAMOUNT
        self.livesAmount = 1
        self.jumpPowerup = False
    def update(self, userInput):
        global jumpAmount, jumpFrame, startTime
        if self.running:
            self.run()
        if self.ducking:
            self.duck()
        if self.jumping:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if jumpFrame == True:
            if (pygame.time.get_ticks() - startTime) > 250:
                jumpFrame = False
        if (userInput[pygame.K_w] or userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and jumpFrame == False:
            jumpFrame = True
            startTime = pygame.time.get_ticks()
            self.running = False
            self.ducking = False
            self.jumping = True
            if self.jumpAmount > 0:
                self.jump_vel = self.JUMP_VEL
                self.jumpAmount -= 1
        elif (userInput[pygame.K_s] or userInput[pygame.K_DOWN] or userInput[pygame.KMOD_LSHIFT]) and not self.jumping:
            self.running = False
            self.ducking = True
            self.jumping = False
        elif not (self.jumping or (userInput[pygame.K_s] or userInput[pygame.K_DOWN] or userInput[pygame.KMOD_SHIFT])):
            self.running = True
            self.ducking = False
            self.jumping = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def jump(self):
        global jumpAmount, JUMPAMOUNT
        self.image = self.jump_img
        if self.jumping:
            self.dino_rect.y -= self.jump_vel * 2
            self.jump_vel -= 0.4
        if self.dino_rect.y > 310:
            self.dino_rect.y = 310

            self.jumping = False
            self.jump_vel = self.JUMP_VEL
            self.jumpAmount = self.JUMPAMOUNT
    def draw(self, SCREEN):
        # print(self.dino_rect)
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
