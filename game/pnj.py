import pygame
import copy
import random
from game import dialog as dialogpy

class Pnj(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, name, category_name, first_text, text, method):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img = []
        if method == 0:
            for i in range(0, 5):
                img = pygame.image.load(f"img/npc\individual sprites\{category_name}\{name}\{name}_0{i}.png")
                img = pygame.transform.scale(img, (80, 80))
                self.img.append(img)
        if method == 1:
            for i in range(1, 5):
                img = pygame.image.load(f"img/npc\individual sprites\{category_name}\{name}\{name}_{i}.png")
                img = pygame.transform.scale(img, (80, 80))
                self.img.append(img)
        self.index = random.randint(0, 3)
        self.counter = 0
        self.cooldown = 4
        self.pnj_img = self.img[self.index]
        self.rect = self.pnj_img.get_rect()
        self.rect.centerx = x
        self.rect_sup_x = copy.deepcopy(self.rect)
        self.rect.y = y
        self.dialogclass = dialogpy.Dialog(screen, first_text, text, name)
    
    def update(self, x_sup):
        self.counter += 1
        if self.counter > self.cooldown:
            self.counter = 0
            self.index += 1
            if self.index > len(self.img) - 1:
                self.index = 0
            self.pnj_img = self.img[self.index]
        self.rect_sup_x = copy.deepcopy(self.rect)
        self.rect_sup_x.x += x_sup

        self.screen.blit(self.pnj_img, self.rect_sup_x)

    def player_collide(self, x_sup, player_rect, cheat, key):
        rect2 = copy.deepcopy(self.rect)
        rect2.x += x_sup - 30
        rect2.width += 60
        if cheat:
            pygame.draw.rect(self.screen, (0, 0, 0), rect2, 2)

        if player_rect.colliderect(rect2):
            if key == True:
                return "dialog"
            else: return "collide"

        self.dialogclass.txt_counter = -1000
        return False

    def dialog(self, key, buy = False):
        response = self.dialogclass.update(key, buy)
        return response