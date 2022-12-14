import pygame
import copy
from game import button as buttonpy

class Dialog():
    def __init__(self, screen, first_text, text, name = False):
        self.name = name
        self.screen = screen
        self.dialog_box = pygame.image.load("img/dialogbox.png")
        self.dialog_box = pygame.transform.scale(self.dialog_box, (600, 240))
        self.dialog_box_rect = self.dialog_box.get_rect()
        self.dialog_box_rect.center = (screen.get_width() // 2, (screen.get_height() // 5) * 1)
        self.s_black = pygame.Surface((screen.get_width(), screen.get_height()))
        self.s_black.set_alpha(230)
        self.s_black.fill((0, 0, 0))
        self.counter = 0
        self.letter_counter = 0
        self.text_cooldown = 1
        self.text_counter = 0
        self.font = pygame.font.Font("font/dogicapixel.ttf", 17)
        self.first_text = first_text
        self.first_text_read = False
        self.text = text
        self.diff_text = self.first_text.split("|")
        self.buy = False

        self.speak_txt = self.font.render("[press return to speak]", True, (255, 255, 255))
        self.continue_txt =  self.font.render("[press return to contine]", True, (255, 255, 255))
        self.continue_txt.set_alpha(100)
        self.txt_rect = self.speak_txt.get_rect()
        self.txt_rect.center = (self.screen.get_width() // 2, self.screen.get_height() - 30)
        self.txt_counter = -1000
        self.txt_direction = 20
        self.font_btn = pygame.font.Font("font/dogicapixel.ttf", 13)

    def txt(self, txt):
        self.txt_counter += self.txt_direction
        if self.txt_counter >= 355 or self.txt_counter <= -100 and self.txt_direction < 0:
            self.txt_direction *= -1
        if self.txt_counter >= 0 and self.txt_counter <= 255:
            txt.set_alpha(self.txt_counter)
        if self.txt_counter < 0:
            txt.set_alpha(0)
        self.screen.blit(txt, self.txt_rect)

    def update(self, key, buy):
        if not self.buy: self.s_black.set_alpha(220)
        else: self.s_black.set_alpha(240)
        self.screen.blit(self.s_black, (0, 0))
        
        if buy:
            self.buy = False
            self.change_text(buy=buy)

        if not self.buy:
            self.screen.blit(self.dialog_box, self.dialog_box_rect)
            self.counter += 1
            if self.counter >= self.text_cooldown and not self.letter_counter > len(self.diff_text[self.text_counter]):
                self.counter = 0
                self.letter_counter += 1

            if "_*" in self.diff_text[self.text_counter]:
                text_lines, all_btn_text = self.diff_text[self.text_counter].split("_*")
                text_lines = text_lines.split("\n")
                sup_line_num = ((35*4) - (35*len(text_lines))) // 2
                button = True
                if self.letter_counter >= len(self.diff_text[self.text_counter]):
                    all_btn_text = all_btn_text.split("/")
                    all_btn = []
                    for i in range(0, len(all_btn_text)):
                        all_btn.append(buttonpy.Button(self.screen, all_btn_text[i], font=self.font_btn))
                    num_btn = 0
                    for btn in all_btn:
                        if btn.draw(self.screen.get_width() // 2,  100 + 15 + sup_line_num + num_btn * 40 + 180):
                            if all_btn_text[num_btn] == "Buy":
                                self.buy = True
                                return "buy"

                            if self.name == "adventurer_05":
                                if all_btn_text[num_btn] == "...":
                                    add_text = "You're not talkative I see.|My name is : Wyatt the wizard !\nI came here to see\nthe merchant of this region."
                                    for text in add_text.split("|"):
                                        self.diff_text.append(text)
                                elif all_btn_text[num_btn] == "An adventurer":
                                    add_text = "What a coincidence !\nI'm an adventurer too.|My name is : Wyatt the wizard !\nI came here to see\nthe merchant of this region."
                                    for text in add_text.split("|"):
                                        self.diff_text.append(text)
                                button = "pass"

                            if self.name == "king":
                                if all_btn_text[num_btn] == "Of course":
                                    add_text = "Grrrrr !\nEveryone is there to strip me !|I am the king of this place..."
                                    for text in add_text.split("|"):
                                        self.diff_text.append(text)
                                elif all_btn_text[num_btn] == "No way":
                                    add_text = "It's good !\nFinally someone who isn't here for my money.|I am the king of this place..."
                                    for text in add_text.split("|"):
                                        self.diff_text.append(text)
                                button = "pass"

                            else:
                                button = "pass"
                        num_btn += 1

            else:
                button = False
                text_lines = self.diff_text[self.text_counter].split("\n")
                sup_line_num = ((35*4) - (35*len(text_lines))) // 2
            line_num = 0
            for line in text_lines:
                text = ""
                letter_counter = copy.deepcopy(self.letter_counter)
                if not line_num == 0:
                    for i in range (0, (len(text_lines) - (len(text_lines) - line_num))):
                        letter_counter -= len(text_lines[i])
                for i in range(0, letter_counter):
                    if not i > len(line) - 1:
                        text += line[i]
                text = self.font.render(text, True, (255, 255, 255))
                rect = text.get_rect()
                rect.y = 100 + 15 + 35 * line_num + sup_line_num - 5
                rect.centerx = self.screen.get_width() // 2
                self.screen.blit(text, rect)
                line_num += 1
            if self.letter_counter >= len(self.diff_text[self.text_counter]) and not button:
                self.txt(self.continue_txt)
            else:
                self.txt_counter = -1000
            if self.change_text(key, button) == "end":
                return False
            return True
        return "buy"


    def change_text(self, key = False, button = False, buy = False):
        if key == True and self.letter_counter >= len(self.diff_text[self.text_counter]) and not button or button == "pass" or buy:
            self.letter_counter = 0
            self.text_counter += 1
            if self.text_counter >= len(self.diff_text):
                self.text_counter = 0
                if self.first_text_read == False:
                    self.diff_text = self.text.split("|")
                    self.first_text_read = True
                    self.text_counter += 1
                else:
                    self.txt_counter = -1000
                    return "end"
        return True