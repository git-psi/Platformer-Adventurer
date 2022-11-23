import pygame

class load_tiles():
    def __init__(self):
        #load obj
        self.obj = []
        self.obj.append([pygame.image.load("img\coin\Coin-1.png.png"), "obj/1"])
        self.obj.append([pygame.image.load("img\SlimeAnimations/Slime.png"), "obj/2"])
        self.obj.append([pygame.image.load("img/transparent.png"), "obj/3/1"]),
        self.obj.append([pygame.image.load("img/transparent.png"), "obj/3/2"]),
        self.obj.append([pygame.image.load("img/transparent.png"), "obj/3/3"]),
        self.obj.append([pygame.image.load("img\skeleton_sword/ready_1.png"), "obj/4"])

        self.pnj = []
        self.pnj.append([pygame.image.load("img/npc\individual sprites\medieval\merchant\merchant_00.png"), "pnj/1"])
        self.pnj.append([pygame.image.load("img/npc\individual sprites\medieval/adventurer_05/adventurer_05_1.png"), "pnj/2"])
        self.pnj.append([pygame.image.load("img/npc\individual sprites\medieval/king/king_00.png"), "pnj/3"])
        self.pnj.append([pygame.image.load("img/npc\individual sprites\medieval/captain/captain_1.png"), "pnj/4"])

        self.all_tiles_name = ["grass", "sand", "cake", "castle", "choco", "dirt", "metal", "purple", "sand", "snow", "tundra"]

    def get_tiles(self, tiles_name):
        if tiles_name == "obj":
            return self.obj
        if tiles_name == "pnj":
            return self.pnj
        else:
            tile = []
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}Half.png"), f"{tiles_name}/1/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfLeft.png"), f"{tiles_name}/2/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfMid.png"), f"{tiles_name}/3/half"])
            tile.append([pygame.image.load(f"img\PNG {tiles_name}\{tiles_name}HalfRight.png"), f"{tiles_name}/4/half"])
            num = 5
            for i in range(1, 37):
                try:
                    if i < 10:
                        i = "0"+str(i)
                    tile.append([pygame.image.load(f"img\PNG {tiles_name}\slice{str(i)}_{str(i)}.png"), f"{tiles_name}/{num}"])
                    num += 1
                except:pass
            return tile