import pygame
import copy

class Pnj(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, name, category_name):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.img = []
        for i in range(0, 5):
            img = pygame.image.load(f"img/npc\individual sprites\{category_name}\{name}\{name}_0{i}.png")
            img = pygame.transform.scale(img, (80, 80))
            self.img.append(img)
        self.index = 0
        self.counter = 0
        self.cooldown = 4
        self.pnj_img = self.img[self.index]
        self.rect = self.pnj_img.get_rect()
        self.rect.centerx = x
        self.rect.y = y
    
    def update(self, x_sup):
        self.counter += 1
        if self.counter > self.cooldown:
            self.counter = 0
            self.index += 1
            if self.index > len(self.img) - 1:
                self.index = 0
            self.pnj_img = self.img[self.index]
        rect = copy.deepcopy(self.rect)
        rect.x += x_sup

        self.screen.blit(self.pnj_img, rect)

    def player_collide(self, x_sup, player_rect, cheat):
        rect = copy.deepcopy(self.rect)
        rect.x += x_sup - 30
        rect.width += 60
        if cheat:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        if player_rect.colliderect(rect):
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                return True

        return False