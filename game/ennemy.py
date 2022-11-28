import pygame
import random
from game import lifebar
import copy
from game import text_animation

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, player = False, color = "Normal"):
        pygame.sprite.Sprite.__init__(self)
        color2 = color

        if color2 == "Normal":
            color2 = ""
            self.life_base = random.randint(30, 50)
            self.life = copy.deepcopy(self.life_base)
            self.dammage = 10
            self.attack_cooldown = 2
        if color == "Blue":
            self.life_base = random.randint(50, 80)
            self.life = copy.deepcopy(self.life_base)
            self.dammage = 20
            self.attack_cooldown = 2
        if color == "Red":
            self.life_base = random.randint(80, 120)
            self.life = copy.deepcopy(self.life_base)
            self.dammage = 30
            self.attack_cooldown = 1
        
        self.image_right = []
        self.image_left = []
        self.image_attack_right = []
        self.image_attack_left = []
        self.image_dead_right = []
        self.image_dead_left = []
        self.idle_index = 0
        self.idle_counter = random.randint(0, 3)
        self.attack_index = 0
        self.dead_counter = 0
        self.dead_index = 0
        self.attack_counter = 0

        for num in range(1, 4):
            img_right = pygame.image.load(f"img/SlimeAnimations/{color}/Idle/png/Slime{color2}_Idle{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)

        for num in range(1, 15):
            img_right = pygame.image.load(f"img/SlimeAnimations/{color}/Attack/png/Slime{color2}_Attack{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_attack_right.append(img_right)
            self.image_attack_left.append(img_left)

        for num in range(1, 12):
            img_right = pygame.image.load(f"img/SlimeAnimations/{color}/Death/png/Slime{color2}_Death{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_dead_right.append(img_right)
            self.image_dead_left.append(img_left)
        
        self.image = self.image_right[self.idle_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = [2, -2]
        self.move_direction = random.choice(self.move_direction)
        self.screen = screen
        self.width = self.image.get_width() - 90
        self.height = self.image.get_height() - 55
        self.animation = 0
        self.walk_cooldown = 4
        self.dead_cooldown = 1
        self.player = player
        self.immunity_counter = 0
        self.visible = True
        self.life_remove = 0
        self.dammage_possible = True
        self.is_alive = True
        self.lifebar = lifebar.Lifebar(screen, self.width, self.height, 3)
        self.text_animation = text_animation.TextAnimation(self.screen)

    def immunity(self):
        if self.life_remove:
            self.life_remove -= 2
            self.life -= 2
        if (self.life - self.life_remove) <= 0:
            self.animation = 2
        if self.immunity_counter > 0:
            self.immunity_counter -= 1
            n = self.immunity_counter // 2
            self.dammage_possible = False
            if not (n % 2) == 0:
                self.visible = False
            else: self.visible = True   
        else:
            self.dammage_possible = True
            if self.life <= 0:
                self.is_alive = False

    def update(self, transparent_tile, x_sup, y_sup, cheat):
        if self.player:
            see = self.player.hide_box((self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height))
        else: see = True

        if see:
            self.immunity()

            if self.player:
                player_rect = pygame.Rect(self.player.rect.x + 30 + x_sup - 20, self.player.rect.y + 10 + y_sup, self.player.width + 40, self.player.height)

            if self.player:
                #check collision with sword
                if self.player.animation == 4 and not self.immunity_counter and self.player.index_attack == 2 and self.dammage_possible == True:
                    if self.player.direction == 1:
                        sword_rect = pygame.Rect(self.player.rect.x + x_sup + 50, self.player.rect.y + y_sup - 10, self.player.width + 30, self.player.height + 40)
                        for i in range(10):
                            if sword_rect.colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height) and self.dammage_possible == True:
                                self.rect.x += 4
                                self.immunity_counter = 20
                                self.life_remove += self.player.dammage
                                self.text_animation.add_dammage(self.rect.x + 47, self.rect.y + 55, self.life_remove)
                                self.dammage_possible = False
                                for tile in transparent_tile:
                                    if tile[1].colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height):
                                        self.rect.x -= 4
                    else:
                        sword_rect = pygame.Rect(self.player.rect.x + x_sup - 20, self.player.rect.y + y_sup - 10, self.player.width + 30, self.player.height + 40)
                        for i in range(10):
                            if sword_rect.colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height) and self.dammage_possible == True:
                                self.rect.x -= 4
                                self.immunity_counter = 20
                                self.life_remove += self.player.dammage
                                self.text_animation.add_dammage(self.rect.x + 47, self.rect.y + 40, self.life_remove)
                                self.dammage_possible = False
                                for tile in transparent_tile:
                                    if tile[1].colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height):
                                        self.rect.x += 4

            if not self.immunity_counter > 0:
                if self.animation == 0:
                    self.idle_counter += 1

                if self.animation == 1:
                    self.attack_counter += 1

                if self.player:
                    if player_rect.colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height):
                        if not self.animation == 1:
                            self.attack_index = 0
                            self.attack_counter = 0
                            self.animation = 1

                    else:
                        if self.animation == 1:
                            self.animation = 0
                        self.rect.x += self.move_direction
                        for tile in transparent_tile:
                            if tile[1].colliderect(self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height):
                                self.move_direction *= -1

                if self.idle_counter > self.walk_cooldown and self.animation == 0:
                    self.idle_counter = 0
                    self.idle_index += 1
                    if self.idle_index >= len(self.image_right):
                        self.idle_index = 0
                    if self.move_direction > 0:
                        self.image = self.image_right[self.idle_index]
                    elif self.move_direction < 1:
                        self.image = self.image_left[self.idle_index]

                elif self.attack_counter >= self.attack_cooldown and self.animation == 1:
                    self.attack_counter = 0
                    self.attack_index += 1
                    if self.attack_index >= len(self.image_attack_right):
                        self.attack_index = 0
                    if (self.player.rect.x + 30 + x_sup + (self.player.width // 2)) <= (self.rect.x + x_sup + (self.rect.width // 2)):
                        self.image = self.image_attack_right[self.attack_index]
                    elif (self.player.rect.x + 30 + x_sup + (self.player.width // 2)) > (self.rect.x + x_sup + (self.rect.width // 2)):
                        self.image = self.image_attack_left[self.attack_index]

                if self.attack_index == 10:
                    self.player.take_dammage(self.dammage, 50)

            if self.animation == 2:
                self.dead_counter += 1

            if self.dead_counter > self.dead_cooldown and self.animation == 2:
                self.dead_counter = 0
                self.dead_index += 1
                if self.move_direction > 0:
                    self.image = self.image_dead_right[self.dead_index]
                elif self.move_direction < 1:
                    self.image = self.image_dead_left[self.dead_index]

            if self.visible:
                self.screen.blit(self.image, ((self.rect.x + x_sup), (self.rect.y + y_sup)))

            self.lifebar.update((self.rect.x + x_sup + 47), (self.rect.y + y_sup + 55), self.life, self.life_base)

            self.text_animation.update(x_sup, y_sup)

            if cheat:
                pygame.draw.rect(self.screen, (255, 255, 255), player_rect, 2)
                pygame.draw.rect(self.screen, (0, 0, 0), (self.rect.x + 47 + x_sup, self.rect.y + 55 + y_sup, self.width, self.height), 2)

    def alive(self):
        if not self.is_alive:
            return self
        else: return False



class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, player = False):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        self.idle_img = []
        self.idle_index = 0
        self.idle_counter = 0
        self.idle_cooldown = 3
        for img_x in range(0, 4):
            img_right = self.get_image(img_x*100, 0)
            img_right = pygame.transform.scale(img_right, (170, 170))
            self.idle_img.append([img_right, pygame.transform.flip(img_right, True, False)])

        self.glowing_img = []
        self.glowing_index = 0
        self.glowing_counter = 0
        self.glowing_cooldown = 3
        for img_x in range(0, 8):
            img_right = self.get_image(img_x*100, 100)
            img_right = pygame.transform.scale(img_right, (170, 170))
            self.glowing_img.append([img_right, pygame.transform.flip(img_right, True, False)])

        self.atk_img = []
        self.atk_index = 0
        self.atk_counter = 0
        self.atk_cooldown = 3
        #main attack
        # for img_x in range(0, 8):
        #     img_right = self.get_image(img_x*100, 200)
        #     img_right = pygame.transform.scale(img_right, (170, 170))
        #     self.atk_img.append([img_right, pygame.transform.flip(img_right, True, False)])
        #melee attack
        for img_x in range(0, 7):
            img_right = self.get_image(img_x*100, 400)
            img_right = pygame.transform.scale(img_right, (170, 170))
            self.atk_img.append([img_right, pygame.transform.flip(img_right, True, False)])
        #laser attack
        # for img_x in range(0, 7):
        #     img_right = self.get_image(img_x*100, 500)
        #     img_right = pygame.transform.scale(img_right, (170, 170))
        #     self.atk_img.append([img_right, pygame.transform.flip(img_right, True, False)])

        self.animation = 0
        self.rect = self.idle_img[0][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.rect.width -= 70
        self.rect.height -= 80
        self.img = self.idle_img[self.idle_index][0]
        self.direction = 0
        self.speed = 3

    def update(self, x_sup, y_sup, cheat):
        rect = copy.deepcopy(self.rect)
        rect.x += x_sup

        if self.player:
            see = self.player.hide_box(rect)
        else: see = "create"

        if see == True:

            if self.rect.centerx < self.player.rect.centerx:
                self.direction = 0
                if self.animation == 0:
                    self.rect.x += self.speed
            if self.rect.centerx > self.player.rect.centerx:
                self.direction = 1
                if self.animation == 0:
                    self.rect.x -= self.speed

            #idle animation
            if self.animation == 0:
                self.idle_counter += 1
                if self.idle_counter > self.idle_cooldown:
                    self.idle_counter = 0
                    self.idle_index += 1
                    if self.idle_index >= len(self.idle_img):
                        self.idle_index = 0
                self.img = self.idle_img[self.idle_index][self.direction]

            #atk annimation
            elif self.animation == 1:
                self.atk_counter += 1
                if self.atk_counter > self.atk_cooldown:
                    self.atk_counter = 0
                    self.atk_index += 1
                    if self.atk_index >= len(self.atk_img):
                        self.atk_index = 0
                self.img = self.atk_img[self.atk_index][self.direction]

            #glowing animation
            elif self.animation == 2:
                self.glowing_counter += 1
                if self.glowing_counter > self.glowing_cooldown:
                    self.glowing_counter = 0
                    self.glowing_index += 1
                    if self.glowing_index >= len(self.glowing_img):
                        self.glowing_index = 0
                self.img = self.glowing_img[self.glowing_index][self.direction]

        if see == True or see == "create":
            self.screen.blit(self.img, rect)
            rect.x += 35
            rect.y += 35
            if rect.colliderect(self.player.rect):
                self.animation = 1
            else: self.animation = 0
            if cheat:
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 4)

    def get_image(self, x, y):
        image = pygame.Surface([100, 100])
        image.blit(pygame.image.load("img\Mecha-stone Golem 0.1\PNG sheet\Character_sheet.png"), (0, 0), (x, y, 100, 100))
        image.set_colorkey([0, 0, 0])
        return image