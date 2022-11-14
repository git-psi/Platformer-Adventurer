import pygame

class AllBlock():
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 45
        self.column = [self.obj, self.img, self.img1, self.img, self.img1, self.img]
        for column in range(0, len(self.column)):
            for block in range(0, len(self.column[column])):
                self.column[column][block][0] = pygame.transform.scale(self.column[column][block][0], (self.tile_size, self.tile_size))
        self.s_black = pygame.Surface((screen.get_width(), screen.get_height()))
        self.s_black.set_alpha(200)
        self.s_black.fill((0, 0, 0))
        self.rect = self.column[1][10][0].get_rect()
        self.num_of_column = len(self.column) + 1


    def choose_block(self, y_sup, mouse_clicked):
        self.screen.blit(self.s_black, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for column in range(0, len(self.column)):
            for block in range(0, len(self.column[column])):
                self.rect.center = ((column + 1) * (self.screen.get_width() // self.num_of_column), block * 50 + 100 + y_sup)
                if self.rect.collidepoint(mouse_pos) and mouse_pos[1] < 700:
                    rect = pygame.Rect((column + 1) * (self.screen.get_width() // self.num_of_column) - 28, block * 50 + 100 + y_sup - 28, self.tile_size + 10, self.tile_size + 10)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)
                    if mouse_clicked:
                        return(self.column[column][block][1])
                self.screen.blit(self.column[column][block][0], self.rect)

        return False