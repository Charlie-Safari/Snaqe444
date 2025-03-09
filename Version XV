import pygame
import random
import sys

pygame.init()

# ----- Screen Setup -----
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Da Emperor vs. Beatrix da Ai - Menu Edition")
clock = pygame.time.Clock()
FPS = 240  # Increased FPS for smoother graphics

# ----- Colors -----
BLACK   = (0, 0, 0)
TEAL    = (0, 128, 128)       # Da Emperor (Player)
PURPLE  = (128, 0, 128)       # Beatrix da Ai (AI)
GOLD    = (255, 215, 0)       # Food
WHITE   = (255, 255, 255)
YELLOW  = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN    = (0, 255, 255)
confetti_colors = [YELLOW, MAGENTA, CYAN, WHITE]

snake_size = 10

# ----- Level Definitions -----
# Original speeds increased by +10 across the board.
levels = {
    1: {  # LETS GOOO!!!
        "player_speed": 20, "ai_speed": 10,
        "opponent_collision_allowed": True,
        "self_collision_allowed": True,
        "closed_border": False,   # infinite/wrap-around
        "reset_on_collision": False,
        "food_count": 1,
        "win_points": 200,
        "points_per_food": 10,
        "blocks_per_food": 3,
        "win_message": "WINNER",
        "level_title": "Chapter 1 - LETS GOOO!!!"
    },
    2: {  # GET RUGGED!!!
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 200,
        "points_per_food": 10,
        "blocks_per_food": 4,
        "win_message": "WINNER",
        "level_title": "Chapter 2 - GET RUGGED!!!"
    },
    3: {  # Net Neutrality
        "player_speed": 20, "ai_speed": 20,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 2,
        "win_points": 200,
        "points_per_food": 10,
        "blocks_per_food": 4,
        "win_message": "WINNER",
        "level_title": "Chapter 3 - Net Neutrality"
    },
    4: {  # I challenge you to a Dual.
        "player_speed": 20, "ai_speed": 17,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 100,
        "points_per_food": 10,
        "blocks_per_food": 2,
        "win_message": "WINNER",
        "level_title": "Chapter 4 - I challenge you to a Dual."
    },
    5: {  # Intermission (Checkpoint)
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": False,
        "closed_border": True,   # closed border
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 100,
        "points_per_food": 20,
        "blocks_per_food": 10,
        "win_message": "WINNER",
        "level_title": "Chapter 5 - Intermission"
    },
    6: {  # RUN FORREST!!!
        "player_speed": 25, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": True,   # closed border
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 400,
        "points_per_food": 20,
        "blocks_per_food": 5,
        "win_message": "WINNER",
        "level_title": "Chapter 6 - RUN FORREST!!!"
    },
    7: {  # Tiptoe Through the Tulips
        "player_speed": 15, "ai_speed": 10,
        "opponent_collision_allowed": True,
        "self_collision_allowed": False,
        "closed_border": True,   # solid border
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 200,
        "points_per_food": 10,
        "blocks_per_food": 1,
        "win_message": "WINNER",
        "level_title": "Chapter 7 - Tiptoe Through the Tulips"
    },
    8: {  # Watch your step
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": True,
        "self_collision_allowed": False,
        "closed_border": False,  # infinite/wrap-around
        "reset_on_collision": False,
        "food_count": 1,
        "win_points": 200,
        "points_per_food": 20,
        "blocks_per_food": 7,
        "win_message": "WINNER",
        "level_title": "Chapter 8 - Watch your step"
    },
    9: {  # Lightning War
        "player_speed": 15, "ai_speed": 15,
        "opponent_collision_allowed": True,
        "self_collision_allowed": True,
        "closed_border": False,  # infinite/wrap-around
        "reset_on_collision": False,
        "food_count": 20,
        "win_points": 500,
        "points_per_food": 5,
        "blocks_per_food": 1,
        "win_message": "WINNER",
        "level_title": "Chapter 9 - Lightning War"
    },
    10: {  # Tranquility
        "player_speed": 10, "ai_speed": 5,
        "opponent_collision_allowed": False,
        "self_collision_allowed": False,
        "closed_border": True,   # solid border
        "reset_on_collision": "HALF",  # special half reset
        "food_count": 1,
        "win_points": 200,
        "points_per_food": 10,
        "blocks_per_food": 1,
        "win_message": "YOU FUCKIN WON THE GAME FAM! THAT WAS THE HARDEST LEVEL!!  CONGRATS!!!",
        "level_title": "Chapter 10 - Tranquility"
    }
}
max_level = 10
current_level = 1
level_params = levels[current_level]

# ----- Helper: Compute Update Interval (Lower value means faster movement) -----
def compute_interval(speed):
    # Add +10 speed bonus to both snakes on every level.
    return max(1, round(FPS / (speed + 10)))

player_interval = 0
ai_interval = 0

# ----- Global Time Tracking -----
start_time = 0  # Set in load_level

# ----- Fonts -----
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)

# ----- Effects -----
def draw_strobe_background():
    strobe_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    screen.fill(strobe_color)

def draw_confetti():
    for _ in range(200):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(confetti_colors)
        pygame.draw.rect(screen, color, (x, y, 5, 5))

def draw_strobe_fireworks():
    strobe_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    screen.fill(strobe_color)
    for _ in range(30):
        x1 = random.randint(0, WIDTH)
        y1 = random.randint(0, HEIGHT)
        x2 = x1 + random.randint(-50, 50)
        y2 = y1 + random.randint(-50, 50)
        color = random.choice(confetti_colors)
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

def final_level_celebration(message):
    duration_ms = pygame.time.get_ticks() - start_time
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    time_text = f"Time: {minutes}:{seconds:02d}"
    for _ in range(100):
        draw_strobe_fireworks()
        win_text = big_font.render(message, True, WHITE)
        time_render = font.render(time_text, True, WHITE)
        rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        time_rect = time_render.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(win_text, rect)
        screen.blit(time_render, time_rect)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

def display_winner(message):
    duration_ms = pygame.time.get_ticks() - start_time
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    time_text = f"Time: {minutes}:{seconds:02d}"
    for _ in range(100):
        screen.fill(BLACK)
        draw_confetti()
        win_text = big_font.render(message, True, WHITE)
        time_render = font.render(time_text, True, WHITE)
        rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        time_rect = time_render.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(win_text, rect)
        screen.blit(time_render, time_rect)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

# ----- Level Transition Screen -----
def level_transition_screen(level):
    transition_duration = 2000  # 2 seconds
    start_transition = pygame.time.get_ticks()
    title = level_params.get("level_title", f"Chapter {level}")
    while pygame.time.get_ticks() - start_transition < transition_duration:
        draw_strobe_background()
        transition_text = big_font.render(title, True, WHITE)
        rect = transition_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(transition_text, rect)
        pygame.display.update()
        clock.tick(FPS)

# ----- Snake Initialization -----
def initial_snake_state(x, y, direction):
    return {
        "snake": [
            [x, y],
            [x - snake_size, y],
            [x - 2 * snake_size, y]
        ],
        "dir": direction,
        "growth": 0,
        "score": 0
    }

player_name = "Da Emperor"
ai_name = "Beatrix da Ai"
player_color = TEAL
ai_color = PURPLE

player = None
ai = None
food_list = []
frame_count = 0
paused = False

STATE_MENU = 0
STATE_PLAYING = 1
game_state = STATE_MENU

# Main Menu Button
BUTTON_RECT = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)

# For "Get Rugged!!" message display (in milliseconds)
rugged_duration = 2000  # 2 seconds
rugged_messages = {"player": None, "ai": None}

def spawn_food(count):
    global food_list
    food_list = []
    for _ in range(count):
        fx = random.randrange(0, WIDTH, snake_size)
        fy = random.randrange(0, HEIGHT, snake_size)
        food_list.append([fx, fy])

def load_level(lvl):
    global current_level, level_params, player_interval, ai_interval, start_time, frame_count
    global player, ai
    current_level = lvl
    level_params = levels[lvl]
    # Add +10 to speeds when computing intervals.
    player_interval = compute_interval(level_params["player_speed"])
    ai_interval = compute_interval(level_params["ai_speed"])
    player = initial_snake_state(100, HEIGHT//2, "RIGHT")
    ai     = initial_snake_state(WIDTH-100, HEIGHT//2, "LEFT")
    spawn_food(level_params["food_count"])
    frame_count = 0
    start_time = pygame.time.get_ticks()
    if lvl > 1:
        level_transition_screen(lvl)

def toggle_pause():
    global paused
    paused = not paused

def update_snake(snake, direction, closed_border):
    head = snake[0].copy()
    if direction == "UP":
        head[1] -= snake_size
    elif direction == "DOWN":
        head[1] += snake_size
    elif direction == "LEFT":
        head[0] -= snake_size
    elif direction == "RIGHT":
        head[0] += snake_size
    if closed_border:
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return None
    else:
        head[0] %= WIDTH
        head[1] %= HEIGHT
    snake.insert(0, head)
    return head

# Enhanced AI: Avoid collisions by not moving into any cell occupied by the player's snake.
def ai_choose_direction(snake, foods):
    head = snake[0]
    best = None
    best_dist = None
    for f in foods:
        dist = abs(f[0] - head[0]) + abs(f[1] - head[1])
        if best is None or dist < best_dist:
            best = f
            best_dist = dist
    dx = best[0] - head[0]
    dy = best[1] - head[1]
    base_dir = None
    if abs(dx) > abs(dy):
        base_dir = "RIGHT" if dx > 0 else "LEFT"
    else:
        base_dir = "DOWN" if dy > 0 else "UP"
    # Check safety: simulate the next position
    def simulate_direction(d):
        temp = head.copy()
        if d == "UP":
            temp[1] -= snake_size
        elif d == "DOWN":
            temp[1] += snake_size
        elif d == "LEFT":
            temp[0] -= snake_size
        elif d == "RIGHT":
            temp[0] += snake_size
        temp[0] %= WIDTH
        temp[1] %= HEIGHT
        return temp
    next_pos = simulate_direction(base_dir)
    # If next position is in player's snake, try alternatives
    if next_pos in player["snake"]:
        safe_dirs = []
        for d in ["UP", "DOWN", "LEFT", "RIGHT"]:
            np = simulate_direction(d)
            if np not in snake and np not in player["snake"]:
                safe_dirs.append(d)
        if safe_dirs:
            return random.choice(safe_dirs)
    return base_dir

def collision_with_self(snake):
    return snake[0] in snake[1:]

def collision_with_opponent(snake1, snake2):
    return snake1[0] in snake2

def reset_player():
    global player, rugged_messages
    if current_level == 10 and level_params["reset_on_collision"] == "HALF":
        player["score"] //= 2
        half = len(player["snake"]) // 2
        player["snake"] = player["snake"][:half]
    elif current_level == 5:
        load_level(5)
    else:
        player = initial_snake_state(100, HEIGHT//2, "RIGHT")
    rugged_messages["ai"] = pygame.time.get_ticks()  # Show "Get Rugged!!" under opponent's score

def reset_ai():
    global ai, rugged_messages
    if current_level == 10 and level_params["reset_on_collision"] == "HALF":
        ai["score"] //= 2
        half = len(ai["snake"]) // 2
        ai["snake"] = ai["snake"][:half]
    elif current_level == 5:
        load_level(5)
    else:
        ai = initial_snake_state(WIDTH-100, HEIGHT//2, "LEFT")
    rugged_messages["player"] = pygame.time.get_ticks()  # Show "Get Rugged!!" under opponent's score

def next_level():
    global current_level, game_state
    if current_level < max_level:
        load_level(current_level + 1)
    else:
        final_level_celebration(level_params["win_message"])

def return_to_menu():
    global game_state
    game_state = STATE_MENU

def draw_main_menu():
    draw_strobe_background()
    pygame.draw.rect(screen, (200,50,50), BUTTON_RECT)
    btn_text = big_font.render("LETS GO!!!", True, WHITE)
    rect = btn_text.get_rect(center=BUTTON_RECT.center)
    screen.blit(btn_text, rect)

def handle_main_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_RECT.collidepoint(event.pos):
                load_level(1)
                game_state = STATE_PLAYING
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pass

def run_game_loop():
    global frame_count, paused, game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                toggle_pause()
            if not paused:
                if event.key == pygame.K_UP and player["dir"] != "DOWN":
                    player["dir"] = "UP"
                elif event.key == pygame.K_DOWN and player["dir"] != "UP":
                    player["dir"] = "DOWN"
                elif event.key == pygame.K_LEFT and player["dir"] != "RIGHT":
                    player["dir"] = "LEFT"
                elif event.key == pygame.K_RIGHT and player["dir"] != "LEFT":
                    player["dir"] = "RIGHT"

    if paused:
        clock.tick(FPS)
        return

    # Update Player
    if frame_count % player_interval == 0:
        p_head = update_snake(player["snake"], player["dir"], level_params["closed_border"])
        if level_params["closed_border"] and p_head is None:
            reset_player()
        if not level_params["self_collision_allowed"] and collision_with_self(player["snake"]):
            if level_params["reset_on_collision"] == "HALF":
                player["score"] //= 2
                half = len(player["snake"]) // 2
                player["snake"] = player["snake"][:half]
            else:
                player["score"] = 0
            ai["score"] += 10
            reset_player()
        if not level_params["opponent_collision_allowed"] and collision_with_opponent(player["snake"], ai["snake"]):
            if level_params["reset_on_collision"] == "HALF":
                player["score"] //= 2
                half = len(player["snake"]) // 2
                player["snake"] = player["snake"][:half]
            else:
                player["score"] = 0
            ai["score"] += 10
            reset_player()

        if player["snake"][0] in food_list:
            player["score"] += level_params["points_per_food"]
            player["growth"] += level_params["blocks_per_food"]
            food_list.remove(player["snake"][0])
            while len(food_list) < level_params["food_count"]:
                fx = random.randrange(0, WIDTH, snake_size)
                fy = random.randrange(0, HEIGHT, snake_size)
                food_list.append([fx, fy])
        else:
            if player["growth"] > 0:
                player["growth"] -= 1
            else:
                player["snake"].pop()

    # Update AI
    if frame_count % ai_interval == 0:
        ai["dir"] = ai_choose_direction(ai["snake"], food_list)
        a_head = update_snake(ai["snake"], ai["dir"], level_params["closed_border"])
        if level_params["closed_border"] and a_head is None:
            reset_ai()
        if not level_params["self_collision_allowed"] and collision_with_self(ai["snake"]):
            if level_params["reset_on_collision"] == "HALF":
                ai["score"] //= 2
                half = len(ai["snake"]) // 2
                ai["snake"] = ai["snake"][:half]
            else:
                ai["score"] = 0
            player["score"] += 10
            reset_ai()
        if not level_params["opponent_collision_allowed"] and collision_with_opponent(ai["snake"], player["snake"]):
            if level_params["reset_on_collision"] == "HALF":
                ai["score"] //= 2
                half = len(ai["snake"]) // 2
                ai["snake"] = ai["snake"][:half]
            else:
                ai["score"] = 0
            player["score"] += 10
            reset_ai()

        if ai["snake"][0] in food_list:
            ai["score"] += level_params["points_per_food"]
            ai["growth"] += level_params["blocks_per_food"]
            food_list.remove(ai["snake"][0])
            while len(food_list) < level_params["food_count"]:
                fx = random.randrange(0, WIDTH, snake_size)
                fy = random.randrange(0, HEIGHT, snake_size)
                food_list.append([fx, fy])
        else:
            if ai["growth"] > 0:
                ai["growth"] -= 1
            else:
                ai["snake"].pop()

    # Win Condition
    if player["score"] >= level_params["win_points"]:
        if current_level == max_level:
            final_level_celebration(level_params["win_message"])
        else:
            next_level()
    if ai["score"] >= level_params["win_points"]:
        return_to_menu()

    # ----- Drawing -----
    screen.fill(BLACK)
    for fpos in food_list:
        pygame.draw.rect(screen, GOLD, (fpos[0], fpos[1], snake_size, snake_size))
    for seg in player["snake"]:
        pygame.draw.rect(screen, TEAL, (seg[0], seg[1], snake_size, snake_size))
    for seg in ai["snake"]:
        pygame.draw.rect(screen, PURPLE, (seg[0], seg[1], snake_size, snake_size))
    p_text = font.render("Da Emperor: " + str(player["score"]), True, WHITE)
    a_text = font.render("Beatrix da Ai: " + str(ai["score"]), True, WHITE)
    title_text = font.render(level_params.get("level_title", f"Chapter {current_level}"), True, WHITE)
    screen.blit(p_text, (10, 10))
    screen.blit(a_text, (WIDTH - a_text.get_width() - 10, 10))
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 10))

    # Draw "Get Rugged!!" messages under the opponent's score
    current_time = pygame.time.get_ticks()
    if rugged_messages["player"] and current_time - rugged_messages["player"] < rugged_duration:
        rugged_text = font.render("Get Rugged!!", True, WHITE)
        screen.blit(rugged_text, (10, 30))  # Under Da Emperor (when AI got rugged)
    if rugged_messages["ai"] and current_time - rugged_messages["ai"] < rugged_duration:
        rugged_text = font.render("Get Rugged!!", True, WHITE)
        screen.blit(rugged_text, (WIDTH - a_text.get_width() - 10, 30))  # Under Beatrix (when player got rugged)

    pygame.display.update()
    clock.tick(FPS)
    frame_count += 1

def main():
    global game_state, frame_count
    while True:
        if game_state == STATE_MENU:
            draw_strobe_background()
            draw_main_menu()
            pygame.display.update()
            handle_main_menu_events()
            clock.tick(FPS)
        elif game_state == STATE_PLAYING:
            run_game_loop()
            clock.tick(FPS)

def handle_main_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
            if btn_rect.collidepoint(event.pos):
                load_level(1)
                game_state = STATE_PLAYING

# Start at Main Menu
main()
