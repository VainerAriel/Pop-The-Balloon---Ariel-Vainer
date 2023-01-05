from Game import *


# class for generating pigs
class Balloon:
    def __init__(self, pos, index):
        self.x = 120*pos + 120*(pos-1)
        self.y = -100
        self.size = 125 / 2
        self.die = False
        self.die_by_player = False

        self.index = index
        self.life = index + 1
        self.max_life = index + 1
        if index == 0:
            self.index = 0
        elif index == 1:
            self.index = 1
        else:
            self.index = 3

    # show the pig at his current stage
    def show(self):
        image(pigs[self.index + self.max_life - self.life], self.x - self.size, self.y - self.size)

    # move the pig down
    def update(self):
        self.y += 5

    # check if pig hit the floor
    def out_of_screen(self):
        return self.y > 1030 - self.size
