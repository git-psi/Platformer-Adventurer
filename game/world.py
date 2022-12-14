import pygame
from game import objects
from game import ennemy
import tiles as tilespy
from game import pnj as pnjpy
import copy

class World():
    def __init__(self, world_data, tile_size, screen, player = False):

        self.world_data = world_data
        self.player = player
        self.tile_size = tile_size
        self.screen = screen
        self.coin_counter = 0
        self.tiles = tilespy.load_tiles()
        self.xp = 0
        self.text_xp = []

        self.guard_txt = [
            ["I'm Marius !\nI am a king's guard", "Don't you dare hit the king !|He is my only family...|Long live the king !"],
            ["We are the king's guards !\nWe received an extraordinary training.", "Hello adventurer !|Goodbye !"],
            ["I'm Ivor...\nThe king hired me to protect him.", "...|See you soon..."],
            ["...hello", "...hello\n...|...Goodbye..."]
        ]

        obj = self.tiles.get_tiles("obj")
        pnj = self.tiles.get_tiles("pnj")
        tiles = [obj, pnj]
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

    def calculate_tile(self, rect = False):
        self.tiles = []
        self.transparent_tiles = []
        row_count = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if self.player:
                    collide_rect = self.player.rect.x + 1300 > col_count * self.tile_size and self.player.rect.x - 1300 < col_count * self.tile_size
                else: collide_rect = True
                try:
                    if collide_rect:
                        if not "obj" in tile and not "pnj" in tile:
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
                if "obj/2" in str(tile):
                    color = "Normal"
                    if tile == "obj/2/1": color = "Normal"
                    elif tile == "obj/2/2": color = "Blue"
                    elif tile == "obj/2/3": color = "Red"
                    try:
                        slime = ennemy.Enemy(col_count * self.tile_size - 41, row_count * self.tile_size - 32, self.screen, self.player, color=color)
                    except: slime = ennemy.Enemy(col_count * self.tile_size - 41, row_count * self.tile_size - 32, self.screen, color=color)
                    self.slime_group.add(slime)
                col_count += 1
            row_count += 1

    def calculate_pnj(self):
        self.pnj_group.empty()
        row_count = 0
        guard_counter = 0
        for row in self.world_data:
            col_count = 0
            for tile in row:
                if guard_counter >= len(self.guard_txt): guard_counter = 0
                if tile == "pnj/1":
                    first_text = "Hello Adventurer\nI'm a simple merchant...|My name is Dalcke Badulf\nBut you can call me \"Badu\""
                    text = "Hello...|Do you want something ?\n(potion, level up...)\nI have a lot of item..._*Buy/Goodbye|Goodbye !"
                    pnj = pnjpy.Pnj(self.screen, col_count * self.tile_size + self.tile_size // 2, row_count * self.tile_size - 25, "merchant", "medieval", first_text, text, 0)
                    self.pnj_group.add(pnj)
                if tile == "pnj/2":
                    first_text = "Hello who are you ?_*An adventurer/..."
                    text = "Wyatt says hello !|Take good care of yourself !\nLots of monsters hanging around here.|See you soon..."
                    pnj = pnjpy.Pnj(self.screen, col_count * self.tile_size + self.tile_size // 2, row_count * self.tile_size - 25, "adventurer_05", "medieval", first_text, text, 1)
                    self.pnj_group.add(pnj)
                if tile == "pnj/3":
                    first_text = "Hello to you, peasants of my kingdom\nIf you're here for the money you can leave !_*Of course/No way"
                    text = "Bow before your king !|I won't waste my time\ntalking to people of low society.|Have a good time on my kingdom !"
                    pnj = pnjpy.Pnj(self.screen, col_count * self.tile_size + self.tile_size // 2, row_count * self.tile_size - 25, "king", "medieval", first_text, text, 0)
                    self.pnj_group.add(pnj)
                if tile == "pnj/4":
                    first_text = self.guard_txt[guard_counter][0]
                    text = self.guard_txt[guard_counter][1]
                    pnj = pnjpy.Pnj(self.screen, col_count * self.tile_size + self.tile_size // 2, row_count * self.tile_size - 25, "captain", "medieval", first_text, text, 1)
                    self.pnj_group.add(pnj)
                    guard_counter += 1
                col_count += 1
            row_count += 1

    def max_x_player(self):
        world_data_file = open("world_data.txt", "r")
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
                self.coin_counter = 0
            for coin in self.coin_group:
                coin_rect = copy.deepcopy(coin.rect)
                coin_rect.x += x_sup
                if self.player != False:
                    if self.player.hide_box(coin_rect):
                        coin.update()
                        self.screen.blit(coin.image, ((coin.rect.x + x_sup), (coin.rect.y + y_sup)))
                        if not player_alive == True:
                            self.coin_group.remove(coin)
                else:
                    coin.update()
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

        if self.player:
            for pnj in self.pnj_group:
                rect = copy.deepcopy(pnj.rect)
                rect.x += x_sup
                if self.player.hide_box(rect):
                    pnj.update(x_sup)
        else: self.pnj_group.update(x_sup)
        

def world_data_function():
    world_data_file = open("world_data.txt", "r")
    world_data_file = world_data_file.read()
    row = world_data_file.split("\n")
    world_data = []

    for line in row:
        world_data.append(line.split("|"))
    return world_data