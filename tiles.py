import pygame

class load_tiles():
    def __init__(self):
        #load obj
        self.obj = []
        self.obj.append([pygame.image.load("img\coin\Coin-1.png.png"), "obj/1"])
        self.obj.append([pygame.image.load("img\SlimeAnimations/Slime.png"), "obj/2"])
        self.obj.append([pygame.image.load("img/transparent.png"), "obj/3"])
        self.obj.append([pygame.image.load("img/npc\individual sprites\medieval\merchant\merchant_00.png"), "obj/4"])

        self.all_tiles_name = ["grass", "sand", "cake", "castle", "choco", "dirt", "metal", "purple", "sand", "snow", "tundra"]

    def get_tiles(self, tiles_name):
        if tiles_name == "obj":
            return self.obj
        else:
            tile = []
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}Half.png"), f"{tiles_name}/1/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfLeft.png"), f"{tiles_name}/2/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfMid.png"), f"{tiles_name}/3/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfRight.png"), f"{tiles_name}/4/half"])
            num = 5
            for i in range(1, 37):
                #if i >= 1 and i <= 7 or i >= 12:
                try:
                    if i < 10:
                        i = "0"+str(i)
                    tile.append([pygame.image.load(f"img\PNG {tiles_name}\slice{str(i)}_{str(i)}.png"), f"{tiles_name}/{num}"])
                    num += 1
                except:pass
            return tile