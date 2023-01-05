from Bullet import *


# class for the slingshot
class Player:
    size_x = slingshot.get_width()
    size_y = slingshot.get_height()

    def __init__(self):
        self.x = 120 + 240 * 3 - self.size_x / 2
        self.y = 1080 - 10 - self.size_y
        self.lane = 3
        self.move_amount = 0
        self.move_left = True
        self.move_right = True
        self.can_shoot = True

    # show player
    def show(self):
        image(slingshot, self.x, self.y)

    # update the player position
    def update(self):
        if self.x > 1950:
            self.x = -130

        if self.x < -130:
            self.x = 1950

        # player can only shoot in the lane
        if self.x != 120 + 240 * self.lane - self.size_x / 2:
            self.x += self.move_amount * 40
        else:
            self.can_shoot = True

    # move the player to a different lane
    def move_player(self, vel):
        if self.move_left or self.move_right:
            self.lane = (self.lane + vel) % 8
            self.move_amount = vel
            self.move_left = False
            self.move_right = False
            self.can_shoot = False


player = Player()
