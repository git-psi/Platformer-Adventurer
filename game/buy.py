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

        self.sword = [(pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_03a.png"), (40, 40)), "Wooden Sword : 12 damage", 10, 12),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_03b.png"), (40, 40)), "Iron Sword : 15 damage", 5, 15),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\sword_03c.png"), (40, 40)), "Golden Sword : 30 damage", 10, 30)
            ]
        self.sword_index = 0

        self.shield = [(pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\shield_03a.png"), (40, 40)), f"Wooden Shield : -2% damage", 10, 2),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\shield_03b.png"), (40, 40)), f"Iron Shield : -7% damage", 10, 7),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\shield_03c.png"), (40, 40)), f"Blue Shield : -15% damage", 10, 15)
            ]
        self.shield_index = 0

        self.max_health = [(pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48/book_03d.png"), (40, 40)), "Increase Maximum Health : 110", 10, 110),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48/book_03d.png"), (40, 40)), "Increase Maximum Health : 120", 10, 120),
            (pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48/book_03d.png"), (40, 40)), "Increase Maximum Health : 130", 10, 130)
        ]
        self.max_health_index = 0


        self.objs = [] #(obj : pygame.image, name : str, price : int)
        self.objs.append(self.sword[self.sword_index])
        self.objs.append(self.shield[self.shield_index])
        self.objs.append(self.max_health[self.max_health_index])
        self.objs.append((pygame.transform.scale(pygame.image.load("img\Kyrise's 16x16 RPG Icon Pack - V1.3\icons/48x48\potion_01a.png"), (40, 40)), "Regeneration Of Life : 10%", 10, 10))

    def draw(self, num_coin, all_info, shield):
        if self.back_btn.draw(self.screen.get_width() - 79, self.screen.get_height() - 680):
            return num_coin, shield, True
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
                obj_button = True
                if "Regeneration Of Life" in obj[1]:
                    if self.player.life == self.player.life_max:
                        obj_button = False
                if obj_button:
                    if self.buy_btn.draw(270, self.screen.get_height() - 600 + (obj_num - 1) * 70 + 10):
                        num_coin -= obj[2]

                        if "Sword" in obj[1]:
                            self.player.dammage = obj[3]
                            self.sword_index += 1
                            if not self.sword_index >= len(self.sword):
                                self.objs[obj_num - 1] = self.sword[self.sword_index]
                            else: self.objs.pop(obj_num - 1)

                        if "Shield" in obj[1]:
                            shield = obj[3]
                            self.shield_index += 1
                            if not self.shield_index >= len(self.shield):
                                self.objs[obj_num - 1] = self.shield[self.shield_index]
                            else: self.objs.pop(obj_num - 1)

                        if "Regeneration Of Life" in obj[1]:
                            print(1)
                            sup_life = obj[3] * self.player.life_max // 100
                            if sup_life + self.player.life > self.player.life_max:
                                sup_life = self.player.life_max - self.player.life
                            self.player.life += sup_life

                        if "Increase Maximum Health" in obj[1]:
                            self.player.life += obj[3] - self.player.life_max
                            self.player.life_max = obj[3]
                            self.max_health_index += 1
                            if not self.max_health_index >= len(self.max_health):
                                self.objs[obj_num - 1] = self.max_health[self.max_health_index]
                            else: self.objs.pop(obj_num - 1)

            #draw info
            info_num = 1
            for info in all_info:
                info = self.font.render(info, True, (255, 255, 255))
                info_rect = info.get_rect()
                info_rect.y = self.screen.get_height() - 20
                info_rect.centerx = (self.screen.get_width() // (len(all_info) + 1)) * info_num
                self.screen.blit(info, info_rect)
                info_num += 1

        return num_coin, shield, False