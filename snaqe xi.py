import pygame
import random
import sys

pygame.init()

# ----- Screen Setup -----
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Da Emperor vs. Beatrix da Ai - Menu Edition")
clock = pygame.time.Clock()
FPS = 60

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

# Game states
STATE_MENU = 0
STATE_PLAYING = 1

game_state = STATE_MENU

# ----- Level Definitions -----
levels = {
    1: {
        "player_speed": 20, "ai_speed": 10,
        "opponent_collision_allowed": True,
        "self_collision_allowed": True,
        "closed_border": False,   # infinite/wrap-around
        "reset_on_collision": False,
        "food_count": 1,
        "win_points": 200,
        "win_message": "WINNER",
        "points_per_food": 10,
        "blocks_per_food": 3
    },
    2: {
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 200,
        "win_message": "WINNER",
        "points_per_food": 10,
        "blocks_per_food": 4
    },
    3: {
        "player_speed": 20, "ai_speed": 20,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 2,
        "win_points": 200,
        "win_message": "WINNER",
        "points_per_food": 10,
        "blocks_per_food": 4
    },
    4: {
        "player_speed": 15, "ai_speed": 20,
        "opponent_collision_allowed": False,
        "self_collision_allowed": False,
        "closed_border": False,
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 100,
        "win_message": "WINNER",
        "points_per_food": 10,
        "blocks_per_food": 2
    },
    5: {
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": False,
        "closed_border": True,   # closed border
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 100,
        "win_message": "WINNER",
        "points_per_food": 20,
        "blocks_per_food": 10
    },
    6: {
        "player_speed": 20, "ai_speed": 15,
        "opponent_collision_allowed": False,
        "self_collision_allowed": True,
        "closed_border": True,
        "reset_on_collision": True,
        "food_count": 1,
        "win_points": 400,
        "win_message": "YOU FUCKIN WON THE HARDEST LEVEL CONGRATS",
        "points_per_food": 20,
        "blocks_per_food": 5
    }
}
max_level = 6
current_level = 1
level_params = levels[current_level]

def compute_interval(speed):
    return max(1, round(FPS / speed))

player_interval = 0
ai_interval = 0

# Fonts
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)

# Strobe background for menu
def draw_strobe_background():
    strobe_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
    screen.fill(strobe_color)

def draw_confetti():
    for _ in range(200):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(confetti_colors)
        pygame.draw.rect(screen, color, (x, y, 5, 5))

def draw_strobe_fireworks():
    strobe_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
    screen.fill(strobe_color)
    for _ in range(30):
        x1 = random.randint(0, WIDTH)
        y1 = random.randint(0, HEIGHT)
        x2 = x1 + random.randint(-50, 50)
        y2 = y1 + random.randint(-50, 50)
        color = random.choice(confetti_colors)
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

def final_level_celebration(message):
    for _ in range(100):
        draw_strobe_fireworks()
        text = big_font.render(message, True, WHITE)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

def display_winner(message):
    for _ in range(100):
        screen.fill(BLACK)
        draw_confetti()
        text = big_font.render(message, True, WHITE)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

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

def spawn_food(count):
    global food_list
    food_list = []
    for _ in range(count):
        fx = random.randrange(0, WIDTH, snake_size)
        fy = random.randrange(0, HEIGHT, snake_size)
        food_list.append([fx, fy])

def load_level(lvl):
    global current_level, level_params, player_interval, ai_interval
    global player, ai, frame_count
    current_level = lvl
    level_params = levels[lvl]
    player_interval = compute_interval(level_params["player_speed"])
    ai_interval = compute_interval(level_params["ai_speed"])
    player = initial_snake_state(100, HEIGHT//2, "RIGHT")
    ai     = initial_snake_state(WIDTH-100, HEIGHT//2, "LEFT")
    spawn_food(level_params["food_count"])
    frame_count = 0

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
    if abs(dx) > abs(dy):
        return "RIGHT" if dx > 0 else "LEFT"
    else:
        return "DOWN" if dy > 0 else "UP"

def collision_with_self(snake):
    return snake[0] in snake[1:]

def collision_with_opponent(snake1, snake2):
    return snake1[0] in snake2

def reset_player():
    global player
    player = initial_snake_state(100, HEIGHT//2, "RIGHT")

def reset_ai():
    global ai
    ai = initial_snake_state(WIDTH-100, HEIGHT//2, "LEFT")

def next_level():
    global current_level, game_state
    if current_level < max_level:
        load_level(current_level + 1)
    else:
        # Final level
        if current_level == 6:
            final_level_celebration(level_params["win_message"])
        else:
            display_winner(level_params["win_message"])

def return_to_menu():
    global game_state
    game_state = STATE_MENU

def draw_main_menu():
    draw_strobe_background()
    # Draw the "LETS GO!!!" button
    pygame.draw.rect(screen, (200, 50, 50), BUTTON_RECT)  # Some color for the button
    btn_text = big_font.render("LETS GO!!!", True, WHITE)
    rect = btn_text.get_rect(center=BUTTON_RECT.center)
    screen.blit(btn_text, rect)

def handle_main_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_RECT.collidepoint(event.pos):
                # Start the game at level 1
                load_level(1)
                global game_state
                game_state = STATE_PLAYING
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Pause won't matter in menu, but let's just ignore
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
            if level_params["reset_on_collision"]:
                reset_player()
            else:
                return_to_menu()  # or sys.exit()
        if not level_params["self_collision_allowed"] and collision_with_self(player["snake"]):
            if level_params["reset_on_collision"]:
                reset_player()
            else:
                return_to_menu()
        if not level_params["opponent_collision_allowed"] and collision_with_opponent(player["snake"], ai["snake"]):
            if level_params["reset_on_collision"]:
                reset_player()
            else:
                return_to_menu()

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
            if level_params["reset_on_collision"]:
                reset_ai()
            else:
                return_to_menu()
        if not level_params["self_collision_allowed"] and collision_with_self(ai["snake"]):
            if level_params["reset_on_collision"]:
                reset_ai()
            else:
                return_to_menu()
        if not level_params["opponent_collision_allowed"] and collision_with_opponent(ai["snake"], player["snake"]):
            if level_params["reset_on_collision"]:
                reset_ai()
            else:
                return_to_menu()

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
            # final level
            final_level_celebration(level_params["win_message"])
        else:
            next_level()

    if ai["score"] >= level_params["win_points"]:
        # AI wins => return to main menu
        return_to_menu()

    # Drawing
    screen.fill(BLACK)
    for fpos in food_list:
        pygame.draw.rect(screen, GOLD, (fpos[0], fpos[1], snake_size, snake_size))
    for seg in player["snake"]:
        pygame.draw.rect(screen, TEAL, (seg[0], seg[1], snake_size, snake_size))
    for seg in ai["snake"]:
        pygame.draw.rect(screen, PURPLE, (seg[0], seg[1], snake_size, snake_size))
    p_text = font.render("Da Emperor: " + str(player["score"]), True, WHITE)
    a_text = font.render("Beatrix da Ai: " + str(ai["score"]), True, WHITE)
    lvl_text = font.render("Level: " + str(current_level), True, WHITE)
    screen.blit(p_text, (10, 10))
    screen.blit(a_text, (WIDTH - a_text.get_width() - 10, 10))
    screen.blit(lvl_text, ((WIDTH - lvl_text.get_width()) // 2, 10))

    pygame.display.update()

def main():
    global game_state, frame_count
    while True:
        if game_state == STATE_MENU:
            # Draw strobe background and the "LETS GO!!!" button
            draw_strobe_background()
            pygame.draw.rect(screen, (200,50,50), (WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50))
            btn_text = big_font.render("LETS GO!!!", True, WHITE)
            btn_rect = btn_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(btn_text, btn_rect)
            pygame.display.update()
            # handle menu events
            handle_main_menu_events()
            clock.tick(FPS)
        elif game_state == STATE_PLAYING:
            run_game_loop()
            frame_count += 1
            clock.tick(FPS)

def handle_main_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if user clicked "LETS GO!!!"
            mouse_pos = event.pos
            btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50)
            if btn_rect.collidepoint(mouse_pos):
                # Start game at level 1
                load_level(1)
                game_state = STATE_PLAYING

# Start at menu
main()
