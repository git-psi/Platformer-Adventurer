import pygame
import copy
from game import lifebar
from game import text_animation

class Player():
    def __init__(self, x, y, screen_height, screen):
        self.image_right = []
        self.image_left = []
        self.image_jump_right = []
        self.image_jump_left = []
        self.image_idle_right = []
        self.image_idle_left = []
        self.image_fall_right = []
        self.image_fall_left = []
        self.image_attack_1_right = []
        self.image_attack_1_left = []
        self.image_attack_2_right = []
        self.image_attack_2_left = []
        self.image_attack_3_right = []
        self.image_attack_3_left = []
        self.image_attack = [[self.image_attack_1_right, self.image_attack_1_left, 5], [self.image_attack_2_right, self.image_attack_2_left, 6], [self.image_attack_3_right, self.image_attack_3_left, 6]]
        self.image_dead_right = []
        self.image_dead_left = []
        self.attack_choice = 0
        self.index_0 = 0
        self.index_idle = 0
        self.index_jump = 0
        self.index_fall = 0
        self.index_attack = 0
        self.counter = 0
        self.counter_jump = 0
        self.counter_idle = 0
        self.counter_fall = 0
        self.counter_attack = 0
        self.cheat_font = pygame.font.Font("font/dogicapixel.ttf", 15)
        self.dammage = 10
        self.hide_game = pygame.Rect(0, 0, 2400, 700)
        self.attack_delay = 50
        self.attack_cooldown = 4

        for num in range(0, 5):
            img_right = pygame.image.load(f"img/adventurer/adventurer-attack1-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_attack_1_right.append(img_right)
            self.image_attack_1_left.append(img_left)
        for num in range(0, 6):
            img_right = pygame.image.load(f"img/adventurer/adventurer-attack2-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_attack_2_right.append(img_right)
            self.image_attack_2_left.append(img_left)
        for num in range(0, 6):
            img_right = pygame.image.load(f"img/adventurer/adventurer-attack3-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_attack_3_right.append(img_right)
            self.image_attack_3_left.append(img_left)

        for num in range(0, 6):
            img_right = pygame.image.load(f"img/adventurer/adventurer-run-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_right.append(img_right)
            self.image_left.append(img_left)

        for num in range(0, 4):
            img_right = pygame.image.load(f"img/adventurer/adventurer-jump-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_jump_right.append(img_right)
            self.image_jump_left.append(img_left)

        for num in range(0, 4):
            img_right = img_right = pygame.image.load(f"img/adventurer/adventurer-idle-2-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_idle_right.append(img_right)
            self.image_idle_left.append(img_left)
        
        for num in range(0, 2):
            img_right = img_right = pygame.image.load(f"img/adventurer/adventurer-fall-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_fall_right.append(img_right)
            self.image_fall_left.append(img_left)

        for num in range(0, 7):
            img_right = img_right = pygame.image.load(f"img/adventurer/adventurer-die-0{num}.png")
            img_right = pygame.transform.scale2x(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_dead_right.append(img_right)
            self.image_dead_left.append(img_left)

        self.image = self.image_idle_right[self.index_idle]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width() - 60
        self.height = self.image.get_height() -10
        self.vel_y = 0
        self.jumped = False
        self.in_air = False
        self.direction = 1
        self.screen_height = screen_height
        self.screen = screen
        self.animation = 2
        self.glitch_surface = pygame.Surface((160, 95))
        self.glitch_surface.set_alpha(128)
        self.glitch_surface.fill((0, 0, 0))
        self.life = 100
        self.life_max = copy.deepcopy(self.life)
        self.life_remove = 0
        self.immunity_counter = 0
        self.visible = True
        self.attack_possibility = True
        self.attack_restant = 3
        self.attack_time = 0
        self.lifebar = lifebar.Lifebar(self.screen, self.width, self.height, 0, -15, 20, 5)
        self.text_animation = text_animation.TextAnimation(self.screen)
        self.alive = True
        self.shield = 0

    def define_tile_list(self, tile_list):
        self.tile_list = tile_list

    def update(self, x_sup = 0, y_sup = 0, max_x_player = 1200, cheat = 0, fps = 30, slimes = pygame.sprite.Group, in_dialog = False, shield = 0):
        self.shield = shield
        dx = 0
        dy = 0
        walk_cooldown = 2
        idle_cooldown = 5
        jump_cooldown = 2
        fall_cooldown = 3
        attack_cooldown = self.attack_cooldown
        right = False
        left = False
        collide_tile = False

        if self.alive == True:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False and not self.animation == 4 and not in_dialog:
                self.vel_y = -15
                self.jumped = True

            if key[pygame.K_SPACE] == False:
                self.jumped = False

            if key[pygame.K_LEFT] and not self.animation == 4 and not key[pygame.K_RIGHT] and not in_dialog:
                dx -= 10
                self.counter += 1
                self.direction = -1
                if self.animation == 2:
                    self.animation = 0
                left = True
            if key[pygame.K_RIGHT] and not self.animation == 4 and not key[pygame.K_LEFT] and not in_dialog:
                dx += 10
                self.counter += 1
                self.direction = 1
                if self.animation == 2:
                    self.animation = 0
                right = True
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False or key[pygame.K_LEFT] and key[pygame.K_RIGHT] or in_dialog:
                left = False
                right = False
                if self.animation == 0: self.counter = 0
                if self.direction == 1 and self.animation == 0:
                    self.image = self.image_right[self.index_0]
                    self.index_0 = 0
                if self.direction == -1 and self.animation == 0:
                    self.image = self.image_left[self.index_0]
                    self.index_0 = 0
                if self.in_air == False and not self.animation == 1 and not self.animation == 3 and not self.animation == 4:
                    self.counter_idle += 1
                    self.animation = 2
            if key[pygame.K_RETURN] and not self.animation == 4 and self.attack_possibility == True and not in_dialog:
                self.animation = 4
                self.attack_restant -= 1
                if self.attack_restant == 0:
                    self.attack_restant = 3
                    self.attack_possibility = self.attack_delay
                self.attack_choice += 1
                if self.attack_choice > (len(self.image_attack) - 1):
                    self.attack_choice = 0
                self.counter_attack = self.image_attack[self.attack_choice][2] * attack_cooldown
                self.counter_attack_base = copy.deepcopy(self.counter_attack)
            if self.in_air and not self.animation == 4 and not self.animation == 1 and not self.animation == 3:
                self.animation = 1

            if self.attack_possibility != True:
                self.attack_possibility -= 1
                if self.attack_possibility == 0:
                    self.attack_possibility = True

            #handle animation
            if self.animation == 4:
                self.counter_attack -= 1
                self.index_attack = self.counter_attack_base // attack_cooldown - self.counter_attack // attack_cooldown
                self.attack_time = 0
                if self.index_attack >= self.counter_attack_base // attack_cooldown:
                    self.animation = 2
                else:
                    if self.direction == 1:
                        self.image = self.image_attack[self.attack_choice][0][self.index_attack]
                    if self.direction == -1:
                        self.image = self.image_attack[self.attack_choice][1][self.index_attack]
            else:
                self.attack_time += 1
                if self.attack_time == 50:
                    self.attack_restant = 3
                    self.attack_possibility = True
                    self.index_attack = 0



            if self.counter > walk_cooldown and self.animation == 0:
                self.counter = 0
                self.index_0 += 1
                if self.index_0 >= len(self.image_right):
                    self.index_0 = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index_0]
                if self.direction == -1:
                    self.image = self.image_left[self.index_0]

            if self.counter_idle > idle_cooldown and self.animation == 2:
                self.counter_idle = 0
                self.index_idle += 1
                if self.index_idle >= len(self.image_idle_right):
                    self.index_idle = 0
                if self.direction == 1:
                    self.image = self.image_idle_right[self.index_idle]
                if self.direction == -1:
                    self.image = self.image_idle_left[self.index_idle]

            if self.animation == 1: self.counter_jump += 1

            if self.animation == 1 and self.vel_y > 0:
                self.animation = 0
                self.counter_jump = 0
                self.index_jump = 0
                self.animation = 3
            else:
                if self.counter_jump > jump_cooldown and self.animation == 1:
                    self.counter_jump = 0
                    self.index_jump += 1
                    if self.index_jump <= 3:
                        if self.direction == 1:
                            self.image = self.image_jump_right[self.index_jump]
                        if self.direction == -1:
                            self.image = self.image_jump_left[self.index_jump]

            if self.in_air and not self.animation == 1 and not self.animation == 4:
                self.animation = 3

            if self.animation == 3:
                self.counter_fall += 1
                if self.direction == 1:
                    self.image = self.image_fall_right[self.index_fall]
                if self.direction == -1:
                    self.image = self.image_fall_left[self.index_fall]
                if self.in_air == False:
                    self.animation = 0
                    self.counter_fall = 0
                    self.index_fall = 0
            if self.counter_fall > fall_cooldown:
                self.counter_fall = 0
                self.index_fall += 1
                if self.index_fall >= len(self.image_fall_right):
                    self.index_fall = 0

            if not self.in_air and self.animation == 1:
                self.animation = 2


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision with slime
            if not self.immunity_counter and not in_dialog:
                for slime in slimes:
                    slime_rect = pygame.Rect(slime.rect.x + 47 + x_sup, slime.rect.y + 55 + y_sup, slime.width, slime.height)
                    if slime_rect.colliderect(self.rect.x + x_sup + 30, self.rect.y + y_sup + 10, self.width, self.height):
                        self.take_dammage(3, 15)

            self.in_air = True
            #check for collision
            for tile in self.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + 30 + dx, self.rect.y + 10, self.width, self.height):
                    dx = 0
                    collide_tile = True
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x + 30, self.rect.y + dy + 10, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check move background
            if not collide_tile:
                if self.rect.x >= 600 and self.rect.x <= max_x_player and right:
                    x_sup -= 10
                if self.rect.x <= max_x_player and self.rect.x >= 600 and left:
                    x_sup += 10
                if x_sup > 0:
                    x_sup = 0
                if abs(x_sup) + 600 > max_x_player:
                    x_sup = -max_x_player + 600

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        #draw player onto screen
        if self.visible:
            self.screen.blit(self.image, (self.rect.x + x_sup, self.rect.y + y_sup))
        if cheat == 1:
            if self.animation == 4:
                if self.direction == 1:
                    pygame.draw.rect(self.screen, (255, 20, 20), (self.rect.x + x_sup + 50, self.rect.y + y_sup - 10, self.width + 30, self.height + 40), 2)
                else: pygame.draw.rect(self.screen, (255, 20, 20), (self.rect.x + x_sup - 20, self.rect.y + y_sup - 10, self.width + 30, self.height + 40), 2)
            if collide_tile:
                pygame.draw.rect(self.screen, (255, 20, 20), (self.rect.x + x_sup + 30, self.rect.y + y_sup + 10, self.width, self.height), 2)
            else:
                pygame.draw.rect(self.screen, (0, 240, 0), (self.rect.x + x_sup + 30, self.rect.y + y_sup + 10, self.width, self.height), 2)
            x_cheat = self.cheat_font.render(f"x = {self.rect.x}", True, [255, 255, 255])
            y_cheat = self.cheat_font.render(f"y = {self.rect.y}", True, [255, 255, 255])
            fps = self.cheat_font.render(f"fps : {fps}", True, [255, 255, 255])
            self.screen.blit(self.glitch_surface, (1030, 10))
            pygame.draw.rect(self.screen, (80, 80, 80), (1028, 8, 164, 99), 4, border_radius = 5) #-2, -2, +4, +4
            self.screen.blit(x_cheat, (1040, 20))
            self.screen.blit(y_cheat, (1040, 50))
            self.screen.blit(fps, (1040, 80))
            pygame.draw.rect(self.screen, (0, 0, 255), self.hide_game, 5)

        if self.life <= 0 and self.alive == True:
            self.alive = 60

        if not self.alive == True and not self.alive == False:
            self.alive -= 1
            if self.direction == 1:
                self.image = self.image_dead_right[6 - (self.alive // 10)]
            if self.direction == -1:
                self.image = self.image_dead_left[6 - (self.alive // 10)]
            if self.alive <= 1:
                self.alive = False
            

        self.immunity()

        self.text_animation.update(x_sup, y_sup)

        if self.alive == True:
            self.lifebar.update(self.rect.x + x_sup + 30, self.rect.y + y_sup, self.life, self.life_max)

        #hide box
        self.hide_game.x = self.rect.x + x_sup - 1200 + self.width // 2
            
        return x_sup, y_sup

    def take_dammage(self, dammage : float, counter):
        if not self.immunity_counter and self.alive == True:
            print(1)
            dammage = (dammage) * (100 - self.shield)
            dammage = dammage//100
            self.life_remove += dammage
            self.immunity_counter = counter
            self.text_animation.add_dammage(self.rect.x + 30, self.rect.y, dammage)

    def immunity(self):
        if self.immunity_counter > 0:
            if self.life_remove > 0:
                if self.life_remove != 1:
                    self.life_remove -= 2
                    self.life -= 2
                else:
                    self.life_remove -= 1
                    self.life -= 1
            self.immunity_counter -= 1
            n = self.immunity_counter // 3
            if not (n % 2) == 0:
                self.visible = False
            else: self.visible = True
            if self.immunity_counter == 0:
                self.life_remove = 0

    def hide_box(self, box):
        if self.hide_game.colliderect(box):
            return True
        else: return False