import pygame

class TextAnimation():
    def __init__(self, screen):
        self.font = pygame.font.Font("font/dogicapixelbold.ttf", 15)
        self.screen = screen
        self.coin = []
        self.dammage = []
        self.xp = []

    def add_coin(self, x, y):
        self.coin.append([x, y, 20])

    def add_dammage(self, x, y, dammage):
        self.dammage.append([x, y, 10, dammage])

    def add_xp(self, x, y, xp):
        self.xp.append([x, y, 20, xp])


    def update(self, x_sup, y_sup):
        remove_i = 0
        for i in range(0, len(self.coin)):
            i -= remove_i
            text = self.font.render("+1 Coin", True, (int(3 * self.coin[i][2] + 195), int(3 * self.coin[i][2] + 195), 0))
            self.coin[i][2] -= 1
            self.coin[i][1] -= 7
            self.screen.blit(text, (self.coin[i][0] + x_sup, self.coin[i][1] + y_sup))
            if self.coin[i][2] <= 0:
                del self.coin[i]
                remove_i += 1

        remove_i = 0
        for i in range(0, len(self.dammage)):
            i -= remove_i
            text = self.font.render(f"-{str(self.dammage[i][3])}", True, (int(3 * self.dammage[i][2] + 195), 0, 0))
            self.dammage[i][2] -= 1
            self.dammage[i][1] -= 3
            self.screen.blit(text, (self.dammage[i][0] + x_sup, self.dammage[i][1] + y_sup))
            if self.dammage[i][2] <= 0:
                del self.dammage[i]
                remove_i += 1

        remove_i = 0
        for i in range(0, len(self.xp)):
            i -= remove_i
            text = self.font.render(f"+{str(self.xp[i][3])}xp", True, (2*self.xp[i][2], int(3 * self.xp[i][2] + 180), 2*self.xp[i][2]))
            self.xp[i][2] -= 1
            self.xp[i][1] -= 7
            self.screen.blit(text, (self.xp[i][0] + x_sup, self.xp[i][1] + y_sup))
            if self.xp[i][2] <= 0:
                del self.xp[i]
                remove_i += 1