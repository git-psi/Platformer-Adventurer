import pygame

class Lifebar():
    def __init__(self, screen, width, height, x_sup = 0, y_sup = 0, width_sup = 0, height_sup = 0, name = ""):
        self.screen = screen
        self.bar_width = 60 + width_sup
        self.bar_height = 10 + height_sup
        self.x_sup = (width // 2) - (self.bar_width // 2) - x_sup
        self.y_sup = (height // 2) - 30 + y_sup
        self.name = name

    def update(self, x, y, life, life_total):
        life_width = (self.bar_width * life) // life_total
        x += self.x_sup
        y += self.y_sup
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, (0, 80, 0), (x + 2, y + 2, (self.bar_width - 4), (self.bar_height - 4)))
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 2, y + 2, (life_width - 4), (self.bar_height - 4)))