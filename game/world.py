import pygame
from game import objects
from game import ennemy

class World():
    def __init__(self, world_data, tile_size, screen):

        self.world_data = world_data
        self.tile_size = tile_size
        self.screen = screen
        self.coin_counter = 0

        self.obj = []
        self.obj.append((pygame.image.load("img\coin\Coin-1.png.png"), "obj/1"))
        self.obj.append((pygame.image.load("img\SlimeAnimations/Slime.png"), "obj/2"))
        self.obj.append((pygame.image.load("img/transparent.png"), "obj/3"))
        self.img = []
        self.img.append((pygame.image.load("img\PNG Grass\grassHalf.png"), "grass/1"))
        self.img.append((pygame.image.load("img\PNG Grass\grassHalfLeft.png"), "grass/2"))
        self.img.append((pygame.image.load("img\PNG Grass\grassHalfMid.png"), "grass/3"))
        self.img.append((pygame.image.load("img\PNG Grass\grassHalfRight.png"), "grass/4"))
        num = 5
        for i in range(1, 37):
            if i >= 1 and i <= 7 or i >= 12:
                if i < 10:
                    i = "0"+str(i)
                self.img.append((pygame.image.load(f"img\PNG Grass\slice{str(i)}_{str(i)}.png"), f"grass/{num}"))
                num += 1
        self.img1 = []
        self.img1.append((pygame.image.load("img\PNG Sand\sandHalf.png"), "sand/1"))
        self.img1.append((pygame.image.load("img\PNG Sand\sandHalfLeft.png"), "sand/2"))
        self.img1.append((pygame.image.load("img\PNG Sand\sandHalfMid.png"), "sand/3"))
        self.img1.append((pygame.image.load("img\PNG Sand\sandHalfRight.png"), "sand/4"))
        num = 5
        for i in range(1, 37):
            if i >= 1 and i <= 7 or i >= 12:
                if i < 10:
                    i = "0"+str(i)
                self.img1.append((pygame.image.load(f"img\PNG Sand\slice{str(i)}_{str(i)}.png"), f"sand/{num}"))
                num += 1

        self.all_tiles = {}
        for i in range(0, len(self.obj)):
            self.all_tiles[self.obj[i][1]] = self.obj[i][0]
        for i in range(0, len(self.img)):
            self.all_tiles[self.img[i][1]] = self.img[i][0]
        for i in range(0, len(self.img1)):
            self.all_tiles[self.img1[i][1]] = self.img1[i][0]

        #load groups
        self.coin_group = pygame.sprite.Group()
        self.slime_group = pygame.sprite.Group()

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
                    if not tile == "obj/1" and not tile == "obj/2" and not tile == "obj/3":
                        img = pygame.transform.scale(self.all_tiles[tile], (self.tile_size, self.tile_size))
                        img_rect = img.get_rect()
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

    def draw(self, x_sup = 0, y_sup = 0, cheat = 0, glitch_mode = False, player_alive = True):
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
                self.slime_group.remove(slime)
        

def world_data_function():
    world_data_file = open("world_data", "r")
    world_data_file = world_data_file.read()
    row = world_data_file.split("\n")
    world_data = []

    for line in row:
        world_data.append(line.split("|"))
    return world_data