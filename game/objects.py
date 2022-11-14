import pygame
import random

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_size):
		pygame.sprite.Sprite.__init__(self)
		self.img_num = random.randint(1,7)
		self.img_dict = {
			1 : pygame.image.load("img/coin/Coin-1.png.png"),
			2 : pygame.image.load("img/coin/Coin-2.png.png"),
			3 : pygame.image.load("img/coin/Coin-3.png.png"),
			4 : pygame.image.load("img/coin/Coin-4.png.png"),
			5 : pygame.image.load("img/coin/Coin-5.png.png"),
			6 : pygame.image.load("img/coin/Coin-6.png.png"),
			7 : pygame.image.load("img/coin/Coin-7.png.png")
		}
		self.image = pygame.transform.scale(self.img_dict[1], (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = x
		self.y = y
		self.tile_size = tile_size

	def update(self):
		self.img_num += 1
		if self.img_num > 7:
			self.img_num = 1
		self.image = self.img_dict[self.img_num]
		self.image = pygame.transform.scale(self.img_dict[self.img_num], (self.tile_size // 2, self.tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)