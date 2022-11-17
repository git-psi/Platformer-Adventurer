import pygame
from game import button
from game import text_animation

class Buy():
    def __init__(self, screen, player):
        self.text_animation = text_animation.TextAnimation(screen)
        self.player = player
        self.screen = screen
        self.back_btn = button.Button(screen, "<< Back")
        self.buy_btn = button.Button(screen, "buy", -60, pygame.font.Font("font/dogicapixel.ttf", 12))
        self.font = pygame.font.Font("font/dogicapixel.ttf", 12)
        self.objs = [] #(obj : pygame.image, name : str, price : int)
        self.objs.append((pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_02b.png"), (40, 40)), "Damage increase : +1", 10))
        self.objs.append((pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_02b.png"), (40, 40)), "Object 2", 2))
        self.objs.append((pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_02b.png"), (40, 40)), "Object 3", 45))

    def draw(self, num_coin):
        num_coin += 20
        if self.back_btn.draw(self.screen.get_width() - 79, self.screen.get_height() - 680):
            return True
        coin = self.font.render(f"Coin : {num_coin}", True, (255, 255, 255))
        coin_rect = coin.get_rect()
        coin_rect.y = self.screen.get_height() - 685
        coin_rect.centerx = self.screen.get_width() // 2
        self.screen.blit(coin, (coin_rect))

        obj_num = 0
        for obj in self.objs:
            name = self.font.render(obj[1], True, (255, 255, 255))
            rect = name.get_rect()
            rect.centery = self.screen.get_height() - 600 + obj_num * 70 - 10
            rect.x = 90
            self.screen.blit(name, (rect))

            price = self.font.render(f"Price : {obj[2]}coin", True, (255, 255, 255))
            rect.centery += 20
            self.screen.blit(price, (rect))

            rect = obj[0].get_rect()
            rect.x = 40
            rect.centery = self.screen.get_height() - 600 + obj_num * 70
            self.screen.blit(obj[0], rect)
            obj_num += 1

            if num_coin >= obj[2]:
                if self.buy_btn.draw(270, self.screen.get_height() - 600 + (obj_num - 1) * 70 + 10):
                    print(1)
                    if obj[1] == "Damage increase : +1":
                        self.player.damage_increase(1)

        return False