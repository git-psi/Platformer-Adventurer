import pygame
import copy

class Button():
    def __init__(self, screen, text, sup_size = 0):
        self.font = pygame.font.Font("font/dogica.ttf", 15)
        self.image = pygame.image.load("img/button.png")
        self.image = pygame.transform.scale(self.image, (150 + sup_size, 150 + sup_size))
        self.clicked = False
        self.text = self.font.render(text, True, (255, 255, 255))
        self.screen = screen
        self.sup_size = sup_size

    def draw(self, x, y):
        action = False

        rect = self.image.get_rect()
        rect.center = (x, y-10)
        text_rect = self.text.get_rect()
        text_rect.center = (x, y)

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        rect_pos = copy.deepcopy(rect)
        rect_pos.height -= 110 + self.sup_size
        rect_pos.center = (x, y)
        if rect_pos.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        self.screen.blit(self.image, (rect.x, rect.y + 10))
        self.screen.blit(self.text, text_rect)
        #pygame.draw.rect(self.screen, (255, 0, 0), rect_pos, 4)

        return action

    def collide(self, x, y):
        rect = self.image.get_rect()
        rect.center = (x, y-10)
        text_rect = self.text.get_rect()
        text_rect.center = (x, y)

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        rect_pos = copy.deepcopy(rect)
        rect_pos.height -= 110 + self.sup_size
        rect_pos.center = (x, y)
        if rect_pos.collidepoint(pos):
            return True
        else: return False