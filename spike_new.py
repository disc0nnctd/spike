import numpy as np
import cv2
import random
import time

dimensions = [500, 300]

BIRD_SIZE = 20
APPLE_SIZE = 10

APPLE_MAX_DIST_FROM_WALL = 20 + APPLE_SIZE


def set_apple_position():
    return [random.randrange(1 + APPLE_MAX_DIST_FROM_WALL//10, dimensions[1]//10 - APPLE_MAX_DIST_FROM_WALL//10) * 10,
                       random.randrange(1 + APPLE_MAX_DIST_FROM_WALL//10, dimensions[0]//10 - APPLE_MAX_DIST_FROM_WALL//10) * 10]

def collide_apple(score):
    apple_position = set_apple_position()
    score += 1
    return apple_position, score

def collision_with_apple(bird_position, apple_position):

    #print('----')
    #print(apple_position[0], range(bird_position[0], bird_position[0] + BIRD_SIZE))
    #print(apple_position[1], range(bird_position[1], bird_position[1] + BIRD_SIZE) )
    if apple_position[0] in range(bird_position[0], bird_position[0] + BIRD_SIZE + 10)\
            and apple_position[1] in range(bird_position[1], bird_position[1] + BIRD_SIZE+10):
        return 1
    else:
        return 0


def collision_with_walls(bird_body):
    if bird_body[0] >= 300 - BIRD_SIZE or bird_body[0] < 0 + BIRD_SIZE//2:
        return 1
    else:
        return 0

def collision_with_top_bottom(bird_body):
    if bird_body[1] >= 500 - BIRD_SIZE//2 or bird_body[1] < 0 + BIRD_SIZE//2:
        return 1
    else:
        return 0

def spike_collide_spike(spike1, spike2):
    if spike2[0][0] == spike1[0][0]:
        if spike2[0][1] <= spike1[0][1] <= spike2[1][1] or spike2[0][1] <= spike1[1][1] <= spike2[1][1]:
            return 1
    return 0




img = np.zeros((dimensions[0], dimensions[1], 3), dtype='uint8')
# Initial Snake and Apple position
bird_position = [dimensions[0]//2 - BIRD_SIZE, dimensions[1]//2 - BIRD_SIZE]

apple_position = set_apple_position()
score = 0
prev_button_direction = 1
jump = 0
bird_body = bird_position
bird_direction = 1

in_jump = 0
jump_cooldown = 0

SPIKE_SIZE = 20


spikes = []
spike_count = 1
JUMP_MULTIPLIER = 3
MAX_SPIKE_COUNT = 10

wall_collide_count = 0

MAX_SPIKES_PER_WALL = MAX_SPIKE_COUNT//2
def generate_spike(pre_existing_spikes):
    spike_x1 = random.choice([0, dimensions[1]])
    spike_x2 = spike_x1 + SPIKE_SIZE if spike_x1 == 0 else spike_x1 - SPIKE_SIZE

    spike_y1 = random.randrange(SPIKE_SIZE, dimensions[0] // 10 - SPIKE_SIZE//10) * 10
    spike_y2 = spike_y1 + SPIKE_SIZE

    if len(pre_existing_spikes) > 0:
        all_spikes = np.array(pre_existing_spikes)
        same_wall = all_spikes[[all_spikes[:,:,0] == spike_x1][0][:,0]==True][:,:,1]

        if len(same_wall) == MAX_SPIKES_PER_WALL:
            return None

        if len(same_wall) == 0:
            pass
        else:
            spike_collide = True
            spike_list_collide = []
            while spike_collide:
                for y in same_wall:
                    if not ((y[0] <= spike_y1 <= y[1] or y[0] <= spike_y1 <= y[1]) or (y[0] <= spike_y2 <= y[1] or y[0] <= spike_y2 <= y[1])):
                        spike_list_collide.append(False)
                        if len(spike_list_collide) == len(same_wall):
                            spike_collide = any(spike_list_collide)
                    else:
                        print("Colliding")
                        spike_list_collide = []
                        spike_y1 = random.randrange(SPIKE_SIZE, dimensions[0] // 10 - SPIKE_SIZE) * 10
                        spike_y2 = spike_y1 + SPIKE_SIZE
                        break
        for y in same_wall:
            if ((y[0] <= spike_y1 <= y[1] or y[0] <= spike_y1 <= y[1]) or (
                    y[0] <= spike_y2 <= y[1] or y[0] <= spike_y2 <= y[1])):
                print("Spike STILL COLLIDE")

    return (spike_x1, spike_y1), (spike_x2, spike_y2)


while True:
    cv2.imshow('bird', img)
    cv2.waitKey(1)
    img = np.zeros((dimensions[0], dimensions[1], 3), dtype='uint8')
    # Display Apple
    cv2.rectangle(img, (apple_position[0], apple_position[1]), (apple_position[0] + APPLE_SIZE, apple_position[1] + APPLE_SIZE),
                  (0, 0, 255), 3)
    # Display Snake
    cv2.rectangle(img, (bird_position[0], bird_position[1]), (bird_position[0] + BIRD_SIZE, bird_position[1] + BIRD_SIZE), (0, 255, 0), 3)

    for spike in spikes:
        cv2.rectangle(img, (spike[0][0], spike[0][1]),
                      (spike[1][0], spike[1][1]),
                      (255, 0, 0), 3)


    # Takes step after fixed time
    t_end = time.time() + 0.05
    k = -1
    while time.time() < t_end:
        if k == -1:
            k = cv2.waitKey(1)
        else:
            continue


    if k == ord('w'):
        jump = 1

    #w

    if jump == 1 and in_jump==0:# and jump_cooldown==0:
        print("jumping now")
        in_jump = 30
        jump_cooldown = 60
    jump = 0
    if jump_cooldown:
        jump_cooldown -= 10

    if in_jump > 0:
        bird_body[1] -= 10 * JUMP_MULTIPLIER
        in_jump -= 10


    if bird_direction == 0:
        bird_body[0] -= 10
    else:
        bird_body[0] += 10





    bird_body[1] += 10


    if collision_with_apple(bird_position, apple_position):
        print("apple")
        apple_position, score = collide_apple(score)
    else:
        bird_position = bird_body


    if collision_with_top_bottom(bird_body) == 1:
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = np.zeros((dimensions[0], dimensions[1], 3), dtype='uint8')
        cv2.putText(img, 'Your Score is {}'.format(score), (10, 250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('bird', img)
        cv2.waitKey(0)

        break

    if collision_with_walls(bird_body) == 1:
        wall_collide_count += 1
        spikes = []
        if wall_collide_count%1==0:
            spike_count += 1 if spike_count < MAX_SPIKE_COUNT else 0
        for _ in range(spike_count):
            new_spike = generate_spike(spikes)
            if new_spike:
                spikes.append(new_spike)


        bird_direction = 0 if bird_direction == 1 else 1


cv2.destroyAllWindows()