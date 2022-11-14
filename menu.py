import pygame
from game import world
from game import button

pygame.init()

clock = pygame.time.Clock()
fps = 30

#load font and color
txt_font = [pygame.font.Font("font/made tommy medium.otf", 22), pygame.font.Font("font/made tommy medium.otf", 17)]
title_font = [pygame.font.Font("font/PilotCommand-3zn93.otf", 50), pygame.font.Font("font/PilotCommand-3zn93.otf", 28)]
black = (0, 0, 0)

#load screen
screen_width = 800
screen_height = 500
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)

world = world.World(0, 50, screen)

#create buttons
button_create_world = button.Button(screen, "Create World", 70)
button_create_world_readme = button.Button(screen, "Rules", 0)
button_play = button.Button(screen, "Play", 70)
button_play_readme = button.Button(screen, "Rules", 0)
button_back = button.Button(screen, "<< Back ", 0)
button_all_license = button.Button(screen, "See Licenses", 45)

#load images
background_img = pygame.image.load("img/background.png")
background_img = pygame.transform.scale(background_img, (889, 500))

pygame_img = pygame.image.load("img/pygame_powered.png")
pygame_img = pygame.transform.scale(pygame_img, (500, 198))
pygame_img_rect = pygame_img.get_rect()
pygame_img_rect.center = (screen_width // 2, 120)

text_level_creator = open("Readme/readme_level_creator.txt", "r").read()
text_game = open("Readme/readme_game.txt", "r").read()
text_licenses = open("Readme/readme_licenses.txt", "r").read()
in_readme = False

scroll = 0
max_scroll = 0

def readme(text, in_readme, size = 0):
    max_scroll = 0
    all_lines = text.split("\n")
    line_counter = 3
    for line in all_lines:
        try:
            if line[0] == "*":
                line = line[1:]
                line = title_font[size].render(line, True, black)
                line_rect = line.get_rect()
                x = screen_width // 2
                y = line_counter * 25 - scroll
                line_rect.center = (x, y)
                screen.blit(line, line_rect)
            else:
                line = txt_font[size].render(line, True, black)
                if line.get_rect().width > 700:
                    line = txt_font[size].render("TOO LONG LINE", True, black)
                    screen.blit(line, (50, line_counter * 25 - scroll))
                screen.blit(line, (50, line_counter * 25 - scroll))
        except: pass
        line_counter += 1
        max_scroll += 25
    max_scroll -= 400
    if button_back.draw(screen_width - 79, screen_height - 480):
        in_readme = False
    return max_scroll, in_readme

launch = False
run = True
while run:
    clock.tick(fps)

    #draw the background and the logo
    screen.blit(background_img, (0, 0))
    if in_readme == False:
        screen.blit(pygame_img, pygame_img_rect)

    #draw buttons
    if in_readme == False:
        create_world = button_create_world.draw(screen_width // 2, screen_height // 2 + 130)
        create_world_readme = button_create_world_readme.draw(screen_width // 2, screen_height // 2 + 165)
        play = button_play.draw(screen_width // 2, screen_height // 2 + 20)
        play_readme = button_play_readme.draw(screen_width // 2, screen_height // 2 + 55)
        see_license = button_all_license.draw(screen_width - 100, screen_height - 22)
        if scroll != 0:
            scroll = 0
        if create_world:
            run = False
            launch = "level_creator"
        elif create_world_readme:
            in_readme = "level_creator"
        elif play:
            run = False
            launch = "game"
        elif play_readme:
            in_readme = "game"
        elif see_license:
            in_readme = "licenses"
    elif in_readme == "level_creator":
        max_scroll, in_readme = readme(text_level_creator, in_readme)
    elif in_readme == "game":
        max_scroll, in_readme = readme(text_game, in_readme)
    elif in_readme == "licenses":
        max_scroll, in_readme = readme(text_licenses, in_readme, 1)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and not in_readme == False:
            if abs(scroll) < max_scroll:
                scroll += 30
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and not in_readme == False:
            if scroll > 0:
                scroll -= 30

    pygame.display.update()

pygame.quit()

if launch == "level_creator":
    from level_creator import level_creator
elif launch == "game":
    from game import game

print("rappel : Galatée")