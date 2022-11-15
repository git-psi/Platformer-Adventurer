import pygame
from pygame.locals import *
from game import world as worldpy
from game import player as playerpy
from game import text_animation as txtpy
from game import game_over as game_overpy

pygame.init()

clock = pygame.time.Clock()
fps = 30

screen_width = 1200
screen_height = 700
screen_size = (screen_width, screen_height)
tile_size = 50
x_world = 0
y_world = 0
cheat = 0
score = 0


#load images
background_img = pygame.image.load("img/background.png")
background_img = pygame.transform.scale(background_img, (1244, 700))
coin = pygame.image.load("img\coin\Coin-7.png.png")
coin = pygame.transform.scale(coin, (30, 30))

#load font
font = pygame.font.Font("font/dogicapixel.ttf", 15)


def draw_box(x, y, width, height):
    #load menu
    menu_surface = pygame.Surface((width, height))
    menu_surface.set_alpha(128)
    menu_surface.fill((0, 0, 0))
    screen.blit(menu_surface, (x, y))
    pygame.draw.rect(screen, (80, 80, 80), ((x - 2), (y - 2), (width + 4), (height + 4)), 4, border_radius = 5) #-2, -2, +4, +4


screen = pygame.display.set_mode(screen_size)

def start():
    world_data = worldpy.world_data_function()
    world = worldpy.World(world_data, tile_size, screen)
    tiles = world.calculate_tile()

    player = playerpy.Player(100, screen_height - 50, tiles, screen_height, screen)
    world.def_player(player)

    world.calculate_coin()
    world.calculate_ennemy()
    world.calculate_pnj()
    max_x_player = world.max_x_player() - 600


    text_animation = txtpy.TextAnimation(screen)

    game_over = game_overpy.GameOver(screen, screen_width, screen_height)

    return world_data, world, tiles, player, max_x_player, text_animation, game_over

world_data, world, tiles, player, max_x_player, text_animation, game_over = start()

run = True
while run:
    clock.tick(fps)
    #draw the background
    screen.blit(background_img, (0, 0))

    world.calculate_tile()

    world.draw(x_world, y_world, cheat=cheat, glitch_mode = cheat, player_alive = player.alive)

    #draw box
    draw_box(10, 10, 190, 75)

    #update text
    text_animation.update(x_world, y_world)

    #draw score
    screen.blit(coin, (20, 20))
    score_text = font.render(f" x {str(score)}", True, [255, 255, 255])
    screen.blit(score_text, (50, 27))

    #draw life
    life = font.render(f"Life : {player.life}/{player.life_total}", True, [255, 255, 255])
    screen.blit(life, (25, 55))

    x_world, y_world = player.update(x_world, y_world, max_x_player, cheat, str(round(clock.get_fps(), 2)), world.slime_group)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.key.get_pressed()[K_F12]:
            if cheat == 0:
                cheat = 1
            else: cheat = 0

    if pygame.sprite.spritecollide(player, world.coin_group, True):
        score += 1
        text_animation.add_coin(player.rect.x, player.rect.y)

    
    if player.alive == False or player.alive < 60 and player.alive != True:
        response = game_over.update()
        if response == "quit":
            run = False
        if response == "restart":
            world_data, world, tiles, player, max_x_player, text_animation, game_over = start()
            x_world = 0
            y_world = 0
            score = 0

    pygame.display.update()

pygame.quit()