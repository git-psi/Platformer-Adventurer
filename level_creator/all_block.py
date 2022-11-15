import pygame
import tiles as tilespy
from game import button

class AllBlock():
    def __init__(self, screen):
        self.tiles = tilespy.load_tiles()
        self.screen = screen
        self.tile_size = 45
        self.column = [self.tiles.get_tiles("obj")]
        for tile_name in self.tiles.all_tiles_name:
            self.column.append(self.tiles.get_tiles(tile_name))
        for column in range(0, len(self.column)):
            for block in range(0, len(self.column[column])):
                self.column[column][block][0] = pygame.transform.scale(self.column[column][block][0], (self.tile_size, self.tile_size))
        self.s_black = pygame.Surface((screen.get_width(), screen.get_height()))
        self.s_black.set_alpha(200)
        self.s_black.fill((0, 0, 0))
        self.rect = self.column[1][10][0].get_rect()
        self.num_of_column = len(self.column) + 1
        self.back_button = button.Button(screen, "Back")
        self.font = pygame.font.Font("font/dogica.ttf", 5)


    def choose_block(self, y_sup, mouse_clicked, tile_num):
        self.screen.blit(self.s_black, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        if self.back_button.draw(1120, 25):
            return tile_num

        for column in range(0, len(self.column)):
            for block in range(0, len(self.column[column])):
                self.rect.center = ((column + 1) * (self.screen.get_width() // self.num_of_column), block * 50 + 100 + y_sup)
                if self.rect.collidepoint(mouse_pos) and mouse_pos[1] < 700 and not self.back_button.collide(1120, 25):
                    rect = pygame.Rect((column + 1) * (self.screen.get_width() // self.num_of_column) - 27, block * 50 + 100 + y_sup - 37, self.tile_size + 10, self.tile_size + 20)
                    pygame.draw.rect(self.screen, (224, 224, 224), rect, border_radius=10)
                    text = self.column[column][block][1]
                    if "half" in text:
                        text = text[:-5]
                    block_name = self.font.render(text, True, (0, 0, 0))
                    self.screen.blit(block_name, (self.rect.x, self.rect.y - 10, self.rect.width, self.rect.height))
                    if mouse_clicked:
                        return(self.column[column][block][1])
                self.screen.blit(self.column[column][block][0], self.rect)

        self.back_button.draw(1120, 25)

        return False