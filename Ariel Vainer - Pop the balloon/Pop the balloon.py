import pygame

pygame.init()

from Balloon import *
from Player import *
from Explosion import *
from Game import *


# function to draw the energy bar and the lives bar
def draw_bars():
    # lives
    image(lives, 0, 15)

    # lives
    for i in range(game.life_count):
        if i != game.life_count - 1:
            image(red_bar, 68 + 72 * i, 36)
        else:
            image(pygame.transform.scale(red_bar, (50, 34)), 68 + 72 * i, 36)
            image(red_end, 68 + 72 * i + 50, 36)

    # energy
    image(energy, WIDTH - energy.get_width(), 15)

    # energy flashing
    if game.frame_count % 3 == 0:
        game.energy_flash = (game.energy_flash + 1) % 3

    # show energy bar
    for i in range(game.energy_count):
        if game.energy_count < 180:
            if i == 0:
                image(blue_end[1], WIDTH - energy.get_width() + 21, 36)
            else:
                image(blue_bar[1], WIDTH - energy.get_width() + 21 + 12 + 2 * (i - 1), 36)
        else:
            if i == 0:
                image(blue_end[game.energy_flash], WIDTH - energy.get_width() + 21, 36)
            else:
                image(blue_bar[game.energy_flash], WIDTH - energy.get_width() + 21 + 12 + 2 * (i - 1), 36)

    # fix both bars
    image(fix[0], 0, 15)
    image(fix[1], WIDTH - 75, 15)


def draw_stats():
    text = font.render("Wave " + str(game.wave), True, (0, 0, 0))

    text_rect = text.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2 - 50)

    if round(time.time() * 1000) - game.start3 < 2000:
        screen.blit(text, text_rect)

    if game.state == 1:
        image(black_box, 960 - black_box.get_width() / 2, 15)
        game.time_count = round(time.time() * 1000) - game.start4
    game.min_count, game.sec_count = str(game.time_count // 60000).zfill(2), str(
        game.time_count // 1000 % 60).zfill(2)

    if game.state == 1:
        text_center("Time: " + game.min_count + ":" + game.sec_count, font2, (255, 255, 255), WIDTH / 2, 50)
        text_center("Score: " + f'{game.score:,}', font2, (255, 255, 255), WIDTH / 2, 110)


def main():
    global HIGH_WAVE, HIGH_MIN_COUNT, HIGH_SEC_COUNT, HIGH_TIME_COUNT, HIGH_SCORE

    # draw the background
    image(bg[game.current_bg], 0, 0)
    image(lines, 0, 0)

    # show the instruction image
    if game.state == 0:
        image(instructions, 0, 0)
        draw_bars()

    # game state
    elif game.state == 1 or game.state == 2:

        # spawn new pigs
        limit_wave = 10
        if game.wave < limit_wave:
            millis_to_next_balloon = random.randint(2000 - game.wave * 75, 3000 - game.wave * 50)
        else:
            millis_to_next_balloon = random.randint(1000 - limit_wave * 50, 2000)
        if len(game.balloons) < game.max_balloons:
            if round(time.time() * 1000) - game.start > millis_to_next_balloon:
                game.start = round(time.time() * 1000)
                game.balloons.append(Balloon(round(random.randint(1, 8)), round(random.randint(0, 2))))

        # showing, updating, and removing pigs
        for i in range(len(game.balloons) - 1, -1, -1):
            game.balloons[i].show()
            game.balloons[i].update()
            if game.balloons[i].out_of_screen():
                game.balloons[i].die = True

                if game.state == 1:
                    game.life_count -= 1

            # increasing score if the pig dies
            if game.balloons[i].die:
                if game.balloons[i].die_by_player:
                    if game.energy_count < 180:
                        game.energy_count += 12
                    if game.balloons[i].index == 0:
                        game.score += 10
                    elif game.balloons[i].index == 1:
                        game.score += 30
                    elif game.balloons[i].index == 3:
                        game.score += 100

                game.explosions.append(
                    Explosion(game.balloons[i].x - game.balloons[i].size, game.balloons[i].y - game.balloons[i].size,
                              game.balloons[i].size))
                game.balloons.remove(game.balloons[i])

        # show the player in the game
        if game.state == 1:
            player.show()
        else:
            # showing the ending screen
            image(end, 0, 0)

        # showing, updating, and removing bullets
        if game.state == 1:
            for i in range(len(game.bullets) - 1, -1, -1):
                game.bullets[i].show()
                game.bullets[i].update()

                for j in range(len(game.balloons) - 1, -1, -1):
                    if math.dist((game.bullets[i].x, game.bullets[i].y), (game.balloons[j].x, game.balloons[j].y)) < \
                            game.bullets[i].size / 2 + \
                            game.balloons[j].size:
                        if game.balloons[j].life > 1:
                            game.balloons[j].life -= 1
                        else:
                            game.balloons[j].die = True
                            game.bullets[i].kill_balloon = True
                            game.balloons[j].die_by_player = True
                        game.bullets[i].die = True

                if game.bullets[i].out_of_screen():
                    game.bullets[i].die = True
                    game.total_misses += 1.0
                if game.bullets[i].kill_balloon:
                    game.kill_count += 1
                    game.total_kills += 1
                if game.bullets[i].die:
                    game.bullets.remove(game.bullets[i])

            # show the next bird on the slingshot
            if game.show_bird:
                image(angry_bird[game.next_bird], player.x + player.size_x / 2 - angry_bird[0].get_size()[0] / 2,
                      player.y + 2 * player.size_y / 9 - 10 - angry_bird[0].get_size()[0] / 2)

            if round(time.time() * 1000) - game.start2 > 500:
                game.show_bird = True

        # show the explosions above the pigs
        for i in range(len(game.explosions) - 1, -1, -1):
            if not game.explosions[i].finish:
                game.explosions[i].show()
                if game.frame_count % 2 == 0:
                    game.explosions[i].update()
            else:
                game.explosions.remove(game.explosions[i])

        # draw all the bars
        draw_bars()

        # move the player left and right
        if game.state == 1:
            player.update()

        # progressing with the waves
        game.oldWave = game.wave
        game.wave = (game.kill_count - game.reset_count) // (4 + math.floor(game.progress * 1)) + game.progress

        if game.oldWave != game.wave:
            game.start3 = round(time.time() * 1000)
            game.reset_count = game.kill_count
            game.progress += 1

        # draw all the stats of the screen
        draw_stats()

        # moving to death screen
        if game.life_count <= 0:
            game.state = 2

        # changing high scores
        if game.score > HIGH_SCORE:
            HIGH_SCORE = game.score
        if game.time_count > HIGH_TIME_COUNT:
            HIGH_TIME_COUNT = game.time_count
        if game.wave > HIGH_WAVE:
            HIGH_WAVE = game.wave
        HIGH_MIN_COUNT, HIGH_SEC_COUNT = str(HIGH_TIME_COUNT // 60000).zfill(2), str(
            HIGH_TIME_COUNT // 1000 % 60).zfill(2)

        # drawing all the different facts at the end of the screen
        if game.state == 2:
            # Score:
            # Time survived:
            # Current wave:
            # Total pigs killed
            # Total missed shots:

            # High score:
            # Highest time survived:
            # Highest wave:
            # Total birds shot
            # Accuracy:

            values_left = ["Total score: " + str(game.score), "Time survived: " + game.min_count + ":" + game.sec_count,
                           "Current wave: " + str(game.wave), "Total pigs killed: " + str(game.total_kills),
                           "Total missed shots: " + str(round(game.total_misses))]

            values_right = ["High-score: " + str(HIGH_SCORE), "Highest time: " + HIGH_MIN_COUNT + ":" + HIGH_SEC_COUNT,
                            "Highest wave: " + str(HIGH_WAVE), "Total birds shot: " + str(game.total_shots)]

            if game.total_shots == 0:
                values_right.append("Accuracy: 0%")
            else:
                values_right.append("Accuracy: " + str(
                    round(100 * ((game.total_shots - game.total_misses) / game.total_shots))) + "%")

            for i in range(5):
                text_corner(values_left[i], font3, (0, 0, 0), 660, 400 + 60 * i)
                text_corner(values_right[i], font3, (0, 0, 0), 1040, 400 + 60 * i)

    pygame.display.flip()


def keyboard(event, pressed_keys):
    # move player left and right
    if game.state == 1:
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            player.move_player(-1)

        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            player.move_player(1)

        # shoot
        if pressed_keys[pygame.K_SPACE]:
            if round(time.time() * 1000) - game.start2 > 500:
                if player.can_shoot:
                    game.bullets.append(
                        Bullet(player.x + player.size_x / 2, player.y + 2 * player.size_y / 9 - 10, game.next_bird))

                    game.start2 = round(time.time() * 1000)
                    random_num = random.randint(0, 100)
                    game.show_bird = False
                    game.total_shots += 1
                    for bird in range(len(angry_bird) - 1, -1, -1):
                        if random_num > probability[str(bird)]:
                            game.next_bird = bird
                            break

        # activate the powerup
        if pressed_keys[pygame.K_e] or pressed_keys[pygame.K_RETURN]:
            if game.energy_count >= 180:
                game.energy_count = 0
                for i in range(len(game.balloons)):
                    game.balloons[i].die = True
                    game.total_kills += 1

        # change booleans to true when key is up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.move_left = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.move_right = True


running = True


def mouse():
    global running, game, player

    mouse_pos = pygame.mouse.get_pos()

    # check for click on the start button
    if game.state == 0:
        if math.dist((mouse_pos[0], mouse_pos[1]), (1180, 904)) < 71 and pygame.mouse.get_pressed()[0]:
            game.state = 1
            game.start4 = round(time.time() * 1000)

    # check for again button and exit button
    elif game.state == 2:
        if math.dist((mouse_pos[0], mouse_pos[1]), (1106, 750)) < 65 and pygame.mouse.get_pressed()[0]:
            game = Game()
            player = Player()
            game.frame_count = 0
            print(game.frame_count)
        if math.dist((mouse_pos[0], mouse_pos[1]), (825, 750)) < 65 and pygame.mouse.get_pressed()[0]:
            running = False


while running:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed_keys[pygame.K_ESCAPE]:
            running = False

        keyboard(event, pressed_keys)

    mouse()

    main()

    # change the frame count
    game.frame_count += 1

    clock.tick(FPS)
