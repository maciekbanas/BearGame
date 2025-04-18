import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = win.get_size()

pygame.display.set_caption("Miś Platformówka")

BEAR_WIDTH = 80
BEAR_HEIGHT = 80

def load_gif_frames(filename):
    from PIL import Image
    gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame = gif.convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()

            py_image = pygame.image.fromstring(data, size, mode)
            frames.append(py_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

bear_idle_frames = load_gif_frames("bear_idle.gif")
bear_walk_right = load_gif_frames("bear_walk_right.gif")
bear_walk_left = load_gif_frames("bear_walk_left.gif")
bear_attack_1 = load_gif_frames("bear_attack_1.gif")
bear_attack_2 = load_gif_frames("bear_attack_2.gif")
bear_jump = load_gif_frames("bear_jump.gif")

# Pozycja
bear_x = 100
bear_y = 400
bear_speed = 5
bear_frame_index = 0
bear_frame_timer = 0
bear_frame_delay = 500

is_jumping = False
jump_phase = None
jump_height = 80
jump_speed = 8
jump_start_y = bear_y

jump_direction = 0  # -1: w lewo, 1: w prawo, 0: pionowo
current_attack_frames = []
attacking = False
attack_key_pressed = False

thing_frames = load_gif_frames("thing.gif")
thing_x = 400
thing_y = 400
thing_visible = True


clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(24)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                attack_key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                attacking = False
                attack_key_pressed = False
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_LEFT]
    moving_right = keys[pygame.K_RIGHT]
    attack = keys[pygame.K_a]
    jump = keys[pygame.K_UP]
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        jump_start_y = bear_y
        bear_frame_index = 0
        bear_frame_timer = 0
        if keys[pygame.K_LEFT]:
            jump_direction = -1
        elif keys[pygame.K_RIGHT]:
            jump_direction = 1
        else:
            jump_direction = 0
        jump_phase = "up"

    bear_rect = pygame.Rect(bear_x, bear_y, BEAR_WIDTH, BEAR_HEIGHT)
    thing_rect = pygame.Rect(thing_x, thing_y, thing_frames[0].get_width(), thing_frames[0].get_height())

    if attack and thing_visible and bear_rect.colliderect(thing_rect):
        thing_visible = False

    if is_jumping:
        bear_frame_timer += dt
        if bear_frame_timer >= bear_frame_delay:
            bear_frame_index = (bear_frame_index + 1) % len(bear_jump)
            bear_frame_timer = 0
        current_frame = bear_jump[bear_frame_index]
    else:
        if moving_left:
            bear_x -= bear_speed
        elif moving_right:
            bear_x += bear_speed

    if moving_right:
        bear_frame_timer += dt
        if bear_frame_timer >= bear_frame_delay:
            bear_frame_index = (bear_frame_index + 1) % len(bear_walk_right)
            bear_frame_timer = 0
        current_frame = bear_walk_right[bear_frame_index]
    elif moving_left:
        bear_frame_timer += dt
        if bear_frame_timer >= bear_frame_delay:
            bear_frame_index = (bear_frame_index + 1) % len(bear_walk_left)
            bear_frame_timer = 0
        current_frame = bear_walk_left[bear_frame_index]
    elif attack_key_pressed:
        if not attacking:
            attacking = True
            current_attack_frames = random.choice([bear_attack_1, bear_attack_2])
            bear_frame_index = 0
            bear_frame_timer = 0

        bear_frame_timer += dt
        if bear_frame_timer >= bear_frame_delay:
            bear_frame_index = (bear_frame_index + 1) % len(current_attack_frames)
            bear_frame_timer = 0
        current_frame = bear_attack[bear_frame_index]

        current_frame = current_attack_frames[bear_frame_index]
    elif is_jumping:
        if jump_phase == "up":
            bear_y -= jump_speed
            bear_x += bear_speed * jump_direction
            if bear_y <= jump_start_y - jump_height:
                jump_phase = "down"
        elif jump_phase == "down":
            bear_y += jump_speed
            bear_x += bear_speed * jump_direction
            if bear_y >= jump_start_y:
                bear_y = jump_start_y
                is_jumping = False
                jump_phase = None
                jump_direction = 0
    else:
        bear_frame_timer += dt
        if bear_frame_timer >= bear_frame_delay:
            bear_frame_index = (bear_frame_index + 1) % len(bear_idle_frames)
            bear_frame_timer = 0
        current_frame = bear_idle_frames[bear_frame_index]

    win.fill((135, 206, 250))
    win.blit(current_frame, (bear_x, bear_y))
    if thing_visible:
        win.blit(thing_frames[0], (thing_x, thing_y))

    pygame.display.update()

pygame.quit()
