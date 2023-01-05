from Game import *


# class to generate bullets when space pressed
class Bullet:

    def __init__(self, x, y, next_bird, size=angry_bird[0].get_size()[0]):
        self.x = x
        self.y = y
        self.size = size
        self.next_bird = next_bird
        self.die = False
        self.kill_balloon = False

    # show the current bird (only for show, the birds don't matter)
    def show(self):
        image(angry_bird[self.next_bird], self.x - self.size / 2, self.y - self.size / 2)

    # move the bird up
    def update(self):
        self.y -= 10

    # check if bird out of screen
    def out_of_screen(self):
        return self.y + self.size / 2 < 0

    # check for collision with pigs
    def collide(self):
        for j in range(len(game.balloons) - 1, -1, -1):
            if math.dist((self.x, self.y), (game.balloons[j].x, game.balloons[j].y)) < self.size / 2 + game.balloons[j].size:
                if game.balloons[j].life > 1:
                    game.balloons[j].life -= 1
                else:
                    game.balloons[j].die = True
                    self.kill_balloon = True
                    game.balloons[j].die_by_player = True
                self.die = True
