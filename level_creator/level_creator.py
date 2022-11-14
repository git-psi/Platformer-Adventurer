import pygame
from pygame.locals import *
from game import world as world_py
from level_creator import all_block as all_blockpy

pygame.init()

clock = pygame.time.Clock()
fps = 30

screen_width = 1200
screen_height = 800
screen_size = (screen_width, screen_height)
tile_size = 50
x_sup = 0
y_sup = 0
number_of_line_base = 14
number_of_column_base = 24

screen = pygame.display.set_mode(screen_size)

#load images
background_img = pygame.image.load("img/background.png")
background_img = pygame.transform.scale(background_img, (1244, 700))
target_square_img = pygame.image.load("img/target_square.png")
target_square_img = pygame.transform.scale(target_square_img, (tile_size, tile_size))
button_img = pygame.image.load("img/button.png")
button_img = pygame.transform.scale(button_img, (150, 150))

#load fonts and color
white = (255, 255, 255)
black = (0, 0, 0)

number_of_buttons = 4
button_font = pygame.font.Font("font/dogica.ttf", 10)

def draw_grid():
    #draw the grid
    for line in range(0, (screen_height // tile_size) + 1):
        pygame.draw.line(screen, black, (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(0, screen_width // tile_size):
        pygame.draw.line(screen, black, (line * tile_size, 0), (line * tile_size, screen_height))
    

def draw_mouse():
    mouse = pygame.mouse.get_pos()

    x = (mouse[0] // tile_size) * tile_size
    y = (mouse[1] // tile_size) * tile_size
    if x <= 23 * tile_size and y <= 13 * tile_size:
        mouse_pos = (x, y)
        screen.blit(target_square_img, mouse_pos)


def draw_menu():
    pygame.draw.rect(screen, black, pygame.Rect(0, 700, 1200, 100))

    if restart_button.draw() and not block:
        reload_data()
        return "Restart"
    if save_button.draw() and not block:
        return "Save"
    if choose_block_button.draw() and not block:
        return "block"
    if play_button.draw() and not block:
        return "play"
    else: return False
    


def reload_data():
    world_data = ""
    for i in range(0, number_of_line_base):
        for i in range(0, number_of_column_base):
            world_data += "0|"
        world_data = world_data[:-1]
        world_data += "\n"
    world_data = world_data[:-1]
    world_data_file = open("world_data", "w")
    world_data_file.write(world_data)
    world_data_file.close()

def save_data(world_data):
    world_data_file = open("world_data", "r")
    world_data_remove = 1000000000000
    for line in world_data:
        world_line_data_remove = 0
        for tile in line:
            if tile == 0:
                world_line_data_remove += 1
            else: world_line_data_remove = 0
        if world_line_data_remove < world_data_remove:
            world_data_remove = world_line_data_remove

    world_data_file = open("world_data", "w")
    world_data_write = ""
    for line in world_data:
        for tile in range(len(line) - world_data_remove):
            world_data_write += f"{line[tile]}|"
        world_data_write = world_data_write[:-1]
        world_data_write += "\n"
    world_data_write = world_data_write[:-1]
    world_data_file.write(world_data_write)
    world_data_file.close()
class Button():
    def __init__(self, x, y, image, text):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-10)
        self.clicked = False
        self.text = button_font.render(text, True, white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (x, y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and pygame.mouse.get_pos()[1] > 710:
                action = True
                self.clicked = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y + 10))
        screen.blit(self.text, self.text_rect)

        return action

def add_line():
    for line in world_data:
        line.append(0)

number_of_line = 0
for line in open("world_data"):
    number_of_column = 0
    number_of_line += 1
    num_of_column = line.split("|")
    for column in num_of_column:
        number_of_column += 1

world_data = world_py.world_data_function()

world = world_py.World(world_data, tile_size, screen)

restart_button = Button((1200 // (number_of_buttons + 1)), 750, button_img, "Restart")
save_button = Button((1200 // (number_of_buttons + 1)) * 2, 750, button_img, "Save")
choose_block_button = Button((1200 // (number_of_buttons + 1)) * 3, 750, button_img, "Choose Block")
play_button = Button((1200 // (number_of_buttons + 1)) * 4, 750, button_img, "Play")

all_block = all_blockpy.AllBlock(screen)

tile_num = 1

change_possiblity = True
change_possiblity_num = 0

world.calculate_coin()
world.calculate_ennemy()

block = False
clickable_block = False
all_block_sup = 0
run = True
while run:

    clock.tick(fps)


    #draw the background
    screen.blit(background_img, (0, 0))

    world.calculate_tile()
    world.draw(x_sup, y_sup, 0, True)

    draw_grid()

    if not block: draw_mouse()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not block:
            mouse = pygame.mouse.get_pos()
            x = (mouse[0] // tile_size)
            y = (mouse[1] // tile_size)
            x += (x_sup // tile_size) * -1
            y += (y_sup // tile_size) * -1
            if x <= number_of_column and y <= number_of_line and mouse[1] < 700:
                world_data[y][x] = str(tile_num)
                if str(tile_num) == "obj/1":
                    world.calculate_coin()
                if str(tile_num) == "obj/2":
                    world.calculate_ennemy()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not block:
            mouse = pygame.mouse.get_pos()
            x = (mouse[0] // tile_size)
            y = (mouse[1] // tile_size)
            x += (x_sup // tile_size) * -1
            y += (y_sup // tile_size) * -1
            if x <= number_of_column and y <= number_of_line:
                world_data[y][x] = 0
                if str(tile_num) == "obj/1":
                    world.calculate_coin()
                world.calculate_ennemy()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and block:
            all_block_sup -= 80
            if all_block_sup < -1500:
                all_block_sup = -1500
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and block:
            all_block_sup += 80
            if all_block_sup > 0:
                all_block_sup = 0
        if not block and not all_block_sup == 0:
            all_block_sup = 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if x_sup < 0:
                x_sup += tile_size
        if keys[K_RIGHT]:
            x_sup -= tile_size
            if not number_of_column_base + abs(x_sup // 50) <= number_of_column:
                number_of_column += 1
                add_line()

    if block:
        mouse_clicked = False
        if not pygame.mouse.get_pressed()[0] and not clickable_block:
            clickable_block = True
        if pygame.mouse.get_pressed()[0] and clickable_block:
            mouse_clicked = True
        response = all_block.choose_block(all_block_sup, mouse_clicked)
        if not response == False:
            block = False
            tile_num = response

    menu_response =  draw_menu()

    if menu_response == "Restart":
        world_data = world_py.world_data_function()
        world = world_py.World(world_data, tile_size, screen)
        number_of_line = number_of_line_base
        number_of_column = number_of_column_base
    elif menu_response == "Save":
        save_data(world_data)
    elif menu_response == "block":
        clickable_block = False
        block = True
    elif menu_response == "play":
        run = False
        pygame.quit()
        from game import game

    pygame.display.update()

pygame.quit()