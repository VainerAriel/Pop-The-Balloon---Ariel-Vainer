from Game import *


# a class for generating explosions
class Explosion:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.stage = 0
        self.finish = False

    # show the current frame of the explosion
    def show(self):
        image(explosion[self.stage], self.x, self.y)

    # update the frames and remove the explosion when done
    def update(self):
        self.stage += 1
        if self.stage == 5:
            self.finish = True
