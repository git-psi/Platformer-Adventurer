import pygame
import copy

class Dialog():
    def __init__(self, screen):
        self.screen = screen
        self.dialog_box = pygame.image.load("img/dialogbox.png")
        self.dialog_box = pygame.transform.scale(self.dialog_box, (600, 240))
        self.dialog_box_rect = self.dialog_box.get_rect()
        self.dialog_box_rect.center = (screen.get_width() // 2, (screen.get_height() // 5) * 1)
        self.s_black = pygame.Surface((screen.get_width(), screen.get_height()))
        self.s_black.set_alpha(200)
        self.s_black.fill((0, 0, 0))
        self.counter = 0
        self.text_counter = 0
        self.text_cooldown = 1
        self.font = pygame.font.Font("font/dogicapixel.ttf", 17)
        self.text = "Hello Adventurer\nI'm a simple merchant...\nDo you want something ?\n(potion, level up...)"

    def update(self):
        self.screen.blit(self.s_black, (0, 0))
        self.screen.blit(self.dialog_box, self.dialog_box_rect)
        self.counter += 1
        if self.counter > self.text_cooldown and not self.text_counter > len(self.text):
            self.counter = 0
            self.text_counter += 1
        text_lines = self.text.split("\n")
        line_num = 0
        for line in text_lines:
            text = ""
            text_counter = copy.deepcopy(self.text_counter)
            if not line_num == 0:
                for i in range (0, (len(text_lines) - (len(text_lines) - line_num))):
                    text_counter -= len(text_lines[i])
            for i in range(0, text_counter):
                if not i > len(line) - 1:
                    text += line[i]
            text = self.font.render(text, True, (255, 255, 255))
            rect = text.get_rect()
            rect.y = 100 + 15 + 35 * line_num
            rect.centerx = self.screen.get_width() // 2
            self.screen.blit(text, rect)
            line_num += 1