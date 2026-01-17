import pygame
import requests
import sys
import random
import numpy as np # Ensure numpy is installed: pip install numpy

# --- CONFIGURATION ---
JAVA_URL = "http://localhost:8080/api/traffic"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BG_COLOR = (30, 30, 30)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
CAR_COLOR = (255, 50, 50)
GREEN_LIGHT = (0, 255, 0)
RED_LIGHT = (255, 0, 0)

# --- Q-LEARNING HYPERPARAMETERS ---
ALPHA = 0.1     # Learning Rate
GAMMA = 0.9     # Discount Factor
EPSILON = 0.1   # Exploration Rate

# The Brain: Q-Table dictionary
q_table = {}

# --- HELPER FUNCTIONS ---
def get_state_key(green_lane, n_cars, e_cars):
    # Simplify state into "Bins" to make learning faster
    n_bin = n_cars // 5
    e_bin = e_cars // 5
    return (green_lane, n_bin, e_bin)

def choose_action(state_key):
    # Epsilon-Greedy Strategy
    if random.uniform(0, 1) < EPSILON:
        return random.choice([0, 1]) # Explore
    
    # Exploit
    if state_key not in q_table:
        q_table[state_key] = [0.0, 0.0]
    return np.argmax(q_table[state_key])

def update_q_table(old_state, action, reward, new_state):
    if old_state not in q_table: q_table[old_state] = [0.0, 0.0]
    if new_state not in q_table: q_table[new_state] = [0.0, 0.0]
    
    old_value = q_table[old_state][action]
    next_max = np.max(q_table[new_state])
    
    new_value = (1 - ALPHA) * old_value + ALPHA * (reward + GAMMA * next_max)
    q_table[old_state][action] = new_value

# --- DRAWING FUNCTIONS ---
def draw_roads(screen):
    pygame.draw.rect(screen, ROAD_COLOR, (350, 0, 100, 800)) # Vertical
    pygame.draw.rect(screen, ROAD_COLOR, (0, 350, 800, 100)) # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 350), 2)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (350, 400), 2)

def draw_cars(screen, north_count, east_count):
    for i in range(north_count):
        y_pos = 330 - (i * 30)
        if y_pos > 0: 
            pygame.draw.circle(screen, CAR_COLOR, (375, y_pos), 12) 

    for i in range(east_count):
        x_pos = 330 - (i * 30)
        if x_pos > 0:
            pygame.draw.circle(screen, CAR_COLOR, (x_pos, 425), 12) 

def draw_lights(screen, current_green_lane):
    n_color = GREEN_LIGHT if current_green_lane == "NORTH" else RED_LIGHT
    pygame.draw.circle(screen, n_color, (300, 300), 20) 
    e_color = GREEN_LIGHT if current_green_lane == "EAST" else RED_LIGHT
    pygame.draw.circle(screen, e_color, (300, 500), 20) 

# --- MAIN LOOP ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Traffic Control (Reinforcement Learning)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

running = True
last_state_key = None
last_action = 0

print("Starting AI Training...")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 1. Get Environment State
    try:
        data = requests.get(f"{JAVA_URL}/state", timeout=0.5).json()
    except:
        continue 

    n_cars = data['north_cars']
    e_cars = data['east_cars']
    green = data['current_green']
    
    current_state_key = get_state_key(green, n_cars, e_cars)

    # 2. Learn (Update Q-Table)
    if last_state_key is not None:
        reward = -1 * (n_cars + e_cars) 
        update_q_table(last_state_key, last_action, reward, current_state_key)

    # 3. Decide
    action = choose_action(current_state_key)
    
    # 4. Act
    try:
        requests.post(f"{JAVA_URL}/action", json={"action": int(action)}, timeout=0.5)
    except: pass
    
    last_state_key = current_state_key
    last_action = action

    # 5. VISUALIZE (These are now uncommented!)
    screen.fill(BG_COLOR)
    draw_roads(screen)
    draw_cars(screen, n_cars, e_cars)
    draw_lights(screen, green)
    
    brain_text = f"Q-Table Size: {len(q_table)} states | Current Reward: {-1*(n_cars+e_cars)}"
    screen.blit(font.render(brain_text, True, (255, 255, 255)), (10, 10))

    pygame.display.flip()
    clock.tick(5) # Training Speed

pygame.quit()
sys.exit()