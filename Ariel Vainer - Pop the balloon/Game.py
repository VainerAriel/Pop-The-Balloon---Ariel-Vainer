import random
import time
import math

import pygame

WIDTH = 1920
HEIGHT = 1080
FPS = 30

clock = pygame.time.Clock()  # fps
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen


# make all game variables
class Game:
    def __init__(self):
        self.max_balloons = 100

        self.balloons = []
        self.bullets = []
        self.explosions = []

        self.balloons.clear()
        self.bullets.clear()
        self.explosions.clear()

        self.start = round(time.time() * 1000)
        self.start2 = round(time.time() * 1000)
        self.start3 = round(time.time() * 1000)
        self.start4 = round(time.time() * 1000)

        self.frame_count = 0
        self.show_bird = True
        self.life_count = 5
        self.energy_count = 0  # limit 175
        self.energy_flash = 0

        self.old_wave = 1
        self.wave = 1
        self.kill_count = 0
        self.total_kills = 0
        self.total_misses = 0
        self.total_shots = 0
        self.reset_count = 0
        self.progress = 1

        self.time_count = 0
        self.min_count, self.sec_count = 0, 0

        self.score = 0
        self.current_bg = random.randint(0, 0)

        self.next_bird = 0

        self.state = 0


game = Game()

HIGH_WAVE = 1
HIGH_MIN_COUNT, HIGH_SEC_COUNT = 0, 0
HIGH_TIME_COUNT = 0
HIGH_SCORE = 0

angry_bird = []

location = "Assets\\Fonts\\font.ttf"
font = pygame.font.Font(location, 150)
font2 = pygame.font.Font(location, 50)
font3 = pygame.font.Font(location, 27)


def loadify(img):
    return pygame.image.load(img).convert_alpha()


bg = [loadify("Assets\\Images\\bg\\bg" + str(i) + ".png") for i in range(2)]
lines = loadify("Assets\\Images\\bg\\lines.png")
slingshot = loadify("Assets\\Images\\slingshot\\slingshot2.png")
pigs = [loadify("Assets\\Images\\pigs\\pig" + str(i) + ".png") for i in range(6)]
for i in range(len(pigs)):
    pigs[i] = pygame.transform.scale(pigs[i], (125, 125))

angry_bird.append(loadify("Assets\\Images\\birds\\red.png"))
angry_bird.append(loadify("Assets\\Images\\birds\\yellow.png"))
angry_bird.append(loadify("Assets\\Images\\birds\\black.png"))
# angry_bird.append(loadify("Assets\\Images\\birds\\green.png"))

for i in range(len(angry_bird)):
    angry_bird[i] = pygame.transform.scale(angry_bird[i], (65, 65))

explosion = [loadify("Assets\\Images\\explosion\\" + str(i) + ".png") for i in range(5)]

for i in range(len(explosion)):
    explosion[i] = pygame.transform.scale(explosion[i], (125, 125))

lives = loadify("Assets\\Images\\bars\\lives.png")
energy = loadify("Assets\\Images\\bars\\energy.png")
fix = [loadify("Assets\\Images\\bars\\fix" + str(i) + ".png") for i in range(2)]
red_bar = loadify("Assets\\Images\\bars\\life\\red_bar.png")
red_end = loadify("Assets\\Images\\bars\\life\\red_end.png")

blue_bar = [loadify("Assets\\Images\\bars\\energy\\blue_bar" + str(i) + ".png") for i in range(3)]
blue_end = [loadify("Assets\\Images\\bars\\energy\\blue_end" + str(i) + ".png") for i in range(3)]

instructions = loadify("Assets\\Images\\starting screen\\instructions.png")
black_box = loadify("Assets\\Images\\bars\\black_box.png")
black_box = pygame.transform.scale(black_box, (350, 130))

end = loadify("Assets\\Images\\ending screen\\end.png")

red_bar = pygame.transform.scale(red_bar, (72, 34))

for i in range(len(blue_bar)):
    blue_bar[i] = pygame.transform.scale(blue_bar[i], (2, 34))

probability = {"0": 0, "1": 33, "2": 67}


def image(img, x, y):
    screen.blit(img, (x, y))


def button_rect(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    return (click[0]) and (x + w > mouse[0] > x and y + h > mouse[1] > y)


def button_circ(x, y, r):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    return (click[0]) and (math.dist([mouse[0], mouse[1]], [x, y]) < r)


def text_center(_string, f, color, x, y):
    string = f.render(_string, True, color)
    string_rect = string.get_rect()
    string_rect.center = (x, y)
    screen.blit(string, string_rect)


def text_corner(_string, f, color, x, y):
    string = f.render(_string, True, color)
    string_rect = string.get_rect()
    string_rect.topleft = (x, y)
    screen.blit(string, string_rect)
