import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, SPACE
import time
import math

actual_game_coords = [653, 585, 1142, 803]
game_coords = [653, 347, 1142, 763]

previous_clicks = []

stage_no = 3

no_of_clicks_this_level = 0
start_time_of_level = time.time()

print("stage no {}".format(stage_no))


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def shoot_some_fuckers(screen):
    global game_coords, previous_clicks, stage_no, no_of_clicks_this_level

    for y in range(238, len(screen) - 5, 2):
        for x in range(5, len(screen[y]) - 5, 2):
            if screen[y][x] < 10:
                actual_x = x + game_coords[0]
                actual_y = y + game_coords[1]

                click_bubble_range = 30
                if stage_no == 3:
                    click_bubble_range = 0

                too_close = False
                for pos in previous_clicks:
                    if dist(actual_x, actual_y, pos[0], pos[1]) < click_bubble_range:
                        too_close = True
                        break
                if too_close:
                    continue

                click(actual_x, actual_y)
                no_of_clicks_this_level += 1

                if stage_no == 0:
                    # time.sleep(0.03)
                    click(actual_x + 3, actual_y)
                    no_of_clicks_this_level += 1

                    # time.sleep(0.03)
                    max_previous_click_length = 3

                if stage_no == 1:
                    max_previous_click_length = 5

                if stage_no == 2:
                    max_previous_click_length = 5

                if stage_no == 3:
                    max_previous_click_length = 1

                previous_clicks.append([actual_x, actual_y])
                if len(previous_clicks) > max_previous_click_length:
                    del previous_clicks[0]

                if stage_no < 2:
                    return


def upgrade_gun():
    for i in range(40):
        click(804, 425)
        click(806, 425)
    for j in range(5):
        time.sleep(0.1)
        for i in range(200):
            click(718, 435)
            click(720, 435)
            click(720, 437)
            click(718, 437)

    click(918, 736)


# only start the program after the mouse is on the left screen
while True:
    mouse_pos = queryMousePosition()
    if mouse_pos.x <= 0:
        break

print("alright we good to go")
while True:
    mouse_pos = queryMousePosition()

    if game_coords[0] < mouse_pos.x < game_coords[2] and game_coords[1] < mouse_pos.y < game_coords[3]:
        start_time = time.time()
        screen = np.array(ImageGrab.grab(bbox=game_coords))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        if screen[347 - game_coords[1], 684 - game_coords[0]] > 180:
            PressKey(SPACE)
            time.sleep(0.05)
            ReleaseKey(SPACE)

        if screen[732 - game_coords[1], 872 - game_coords[0]] < 150:
            shoot_some_fuckers(screen)
            clicks_per_second = no_of_clicks_this_level / (time.time() - start_time_of_level)
            print("Clicks per second {}".format(clicks_per_second))

        elif screen[732 - game_coords[1], 872 - game_coords[0]] > 250:
            time.sleep(3)
            upgrade_gun()
            time.sleep(3)
            start_time_of_level = time.time()
            no_of_clicks_this_level = 0

        # print("Frame took {} seconds".format((time.time() - start_time)))
