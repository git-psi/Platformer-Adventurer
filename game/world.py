import pygame
from game import objects
from game import ennemy
import tiles as tilespy
from game import pnj as pnjpy

class World():
    def __init__(self, world_data, tile_size, screen):

        self.world_data = world_data
        self.tile_size = tile_size
        self.screen = screen
        self.coin_counter = 0
        self.tiles = tilespy.load_tiles()
        self.xp = 0
        self.text_xp = []

        obj = self.tiles.get_tiles("obj")
        tiles = [obj]
        for tile_name in self.tiles.all_tiles_name:
            tiles.append(self.tiles.get_tiles(tile_name))

        self.all_tiles = {}
        for i in range(0, len(tiles)):
            for i2 in range(0, len(tiles[i])):
                self.all_tiles[tiles[i][i2][1]] = tiles[i][i2][0]

        #load groups
        self.coin_group = pygame.sprite.Group()
        self.slime_group = pygame.sprite.Group()
        self.pnj_group = pygame.sprite.Group()

    def def_player(self, player):
        self.player = player

    def calculate_tile(self):
        self.tiles = []
        self.transparent_tiles = []
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                try:
                    if not "obj" in tile:
                        img = pygame.transform.scale(self.all_tiles[tile], (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        if "half" in tile:
                            img_rect.height -= self.tile_size // 2 - 5
                        img_rect.x = col_count * self.tile_size
                        img_rect.y = row_count * self.tile_size
                        tile = (img, img_rect)
                        self.tiles.append(tile)
                    if tile == "obj/3":
                        img = pygame.transform.scale(self.all_tiles[tile], (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * self.tile_size
                        img_rect.y = row_count * self.tile_size
                        tile = (img, img_rect)
                        self.transparent_tiles.append(tile)
                except: pass
                col_count += 1
            row_count += 1
        return self.tiles
    
    def calculate_coin(self):
        self.coin_group.empty()
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if tile == "obj/1":
                    coin = objects.Coin(col_count * self.tile_size + (self.tile_size // 2), row_count * self.tile_size + (self.tile_size // 2), self.tile_size)
                    self.coin_group.add(coin)
                col_count += 1
            row_count += 1
    
    def calculate_ennemy(self):
        self.slime_group.empty()
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if tile == "obj/2":
                    try:
                        slime = ennemy.Enemy(col_count * self.tile_size - 41, row_count * self.tile_size - 32, self.screen, self.player)
                    except: slime = ennemy.Enemy(col_count * self.tile_size - 41, row_count * self.tile_size - 32, self.screen)
                    self.slime_group.add(slime)
                col_count += 1
            row_count += 1

    def calculate_pnj(self):
        self.pnj_group.empty()
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if tile == "obj/4":
                    pnj = pnjpy.Pnj(self.screen, col_count * self.tile_size + self.tile_size // 2, row_count * self.tile_size - 25, "merchant", "medieval")
                    self.pnj_group.add(pnj)
                col_count += 1
            row_count += 1

    def max_x_player(self):
        world_data_file = open("world_data", "r")
        world_data_file = world_data_file.read()
        row = world_data_file.split("\n")

        for line in row:
            numbers = (line.split("|"))
            max_x_player = 0
            for num in numbers:
                max_x_player += 50
        return max_x_player

    def draw(self, x_sup = 0, y_sup = 0, cheat = 0, glitch_mode = False, player_alive = True, in_dialog = False):
        for tile in self.tiles:
            tile[1].x = tile[1].x + x_sup
            tile[1].y = tile[1].y + y_sup
            self.screen.blit(tile[0], tile[1])
            if cheat == 1:
                pygame.draw.rect(self.screen, (255, 255, 255), (tile[1]), 2)

        for tile in self.transparent_tiles:
            tile[1].x = tile[1].x + x_sup
            tile[1].y = tile[1].y + y_sup
            if glitch_mode:
                self.screen.blit(tile[0], tile[1])

        #draw objects
        if not in_dialog:
            self.coin_counter += 1
            if self.coin_counter == 5:
                self.coin_group.update()
                self.coin_counter = 0
            for coin in self.coin_group:
                self.screen.blit(coin.image, ((coin.rect.x + x_sup), (coin.rect.y + y_sup)))
                if not player_alive == True:
                    self.coin_group.remove(coin)

            self.slime_group.update(self.transparent_tiles, x_sup, y_sup, cheat)

            for slime in self.slime_group:
                alive = slime.alive()
                if alive or not player_alive == True:
                    self.text_xp.append([slime.rect.x + 47, slime.rect.y + 40, 10])
                    self.slime_group.remove(slime)
                    self.xp += 10

        self.pnj_group.update(x_sup)
        

def world_data_function():
    world_data_file = open("world_data", "r")
    world_data_file = world_data_file.read()
    row = world_data_file.split("\n")
    world_data = []

    for line in row:
        world_data.append(line.split("|"))
    return world_data