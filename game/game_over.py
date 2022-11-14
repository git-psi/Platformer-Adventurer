import pygame
from game import button

class GameOver():
    def __init__(self, screen, width, height):
        self.restart_btn = button.Button(screen, "Restart", 100)
        self.quit_btn = button.Button(screen, "Quit", 100)
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.iteration = 0
        self.red_s = pygame.Surface((self.screen_width, self.screen_height))
        self.red_s.fill((255, 0, 0))

    def update(self):
        if self.iteration < self.screen_width:
            self.iteration += 50
            if self.iteration > self.screen_width:
                self.iteration = self.screen_width
        self.red_s.set_alpha(20000 // self.screen_width * self.iteration // 100)
        self.screen.blit(self.red_s, ((-self.screen_width + self.iteration), 0))
        width = self.screen_width // 2
        width += 1200 - self.iteration
        if self.restart_btn.draw(width, self.screen_height // 2 - 50):
            return "restart"
        if self.quit_btn.draw(width, self.screen_height // 2 + 50):
            return "quit"

        return False