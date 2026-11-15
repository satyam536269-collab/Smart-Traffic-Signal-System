
import pygame
import sys

from AI import count_vehicles, choose_green_direction, explain_decision

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Smart Traffic Management")

clock = pygame.time.Clock()

# Colors
GREEN = (40, 150, 60)
ROAD = (55, 55, 55)
WHITE = (255, 255, 255)
YELLOW = (255, 210, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 23)
small_font = pygame.font.SysFont("Arial", 17)

# Cars
cars = [
    # North to South
    [-1, 405, -50, "down", (0, 150, 255)],
    [-1, 405, -150, "down", (0, 150, 255)],
    [-1, 405, -250, "down", (0, 150, 255)],

    # South to North
    [-1, 485, 650, "up", (255, 255, 0)],
    [-1, 485, 750, "up", (255, 255, 0)],
    [-1, 485, 850, "up", (255, 255, 0)],

    # West to East
    [-1, -60, 245, "right", (255, 100, 100)],
    [-1, -160, 245, "right", (255, 100, 100)],
    [-1, -260, 245, "right", (255, 100, 100)],

    # East to West
    [-1, 960, 335, "left", WHITE],
    [-1, 1060, 335, "left", WHITE],
    [-1, 1160, 335, "left", WHITE]
]

# Initial traffic analysis
traffic = count_vehicles(cars)

# AI decision
best_direction = choose_green_direction(traffic)

# Map selected direction to road phase
vertical_green = best_direction in ("North", "South")

running = True
best_direction = "North"
last_switch = pygame.time.get_ticks()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Live traffic analysis
    traffic = count_vehicles(cars)
    # AI decision (fair: queue compare + max 10 sec green)
    now = pygame.time.get_ticks()
    elapsed = now - last_switch
    if elapsed >= 5000:
        v_count = traffic["North"] + traffic["South"]
        h_count = traffic["East"] + traffic["West"]
        if vertical_green:
            switch = (h_count > v_count) or (elapsed >= 10000 and h_count > 0)
        else:
            switch = (v_count > h_count) or (elapsed >= 10000 and v_count > 0)
        if switch:
            vertical_green = not vertical_green
            group = ("North", "South") if vertical_green else ("East", "West")
            best_direction = max(group, key=traffic.get)
            last_switch = now
    vertical_green = best_direction in ("North", "South")
    screen.fill(GREEN)

    # Roads
    pygame.draw.rect(screen, ROAD, (0, 220, WIDTH, 160))
    pygame.draw.rect(screen, ROAD, (370, 0, 160, HEIGHT))

    # Road markings
    pygame.draw.line(screen, YELLOW, (0, 300), (370, 300), 3)
    pygame.draw.line(screen, YELLOW, (530, 300), (900, 300), 3)
    pygame.draw.line(screen, YELLOW, (450, 0), (450, 220), 3)
    pygame.draw.line(screen, YELLOW, (450, 380), (450, 600), 3)

    # Signal colors
    vertical_color = (0, 255, 0) if vertical_green else RED
    horizontal_color = RED if vertical_green else (0, 255, 0)

    pygame.draw.circle(screen, vertical_color, (340, 190), 18)
    pygame.draw.circle(screen, vertical_color, (560, 410), 18)

    pygame.draw.circle(screen, horizontal_color, (560, 190), 18)
    pygame.draw.circle(screen, horizontal_color, (340, 410), 18)

    # Move cars according to AI signal
    for car in cars:

        _, x, y, direction, color = car
        speed = 2
                # Collision prevention
        blocked = False

        for other in cars:
            if other is car:
                continue

            _, ox, oy, odirection, _ = other

            if odirection != direction:
                continue

            if direction in ("up", "down"):
                same_lane = abs(x - ox) < 25

                if direction == "down":
                    ahead = 0 < oy - y < 60
                else:
                    ahead = 0 < y - oy < 60

            else:
                same_lane = abs(y - oy) < 25

                if direction == "right":
                    ahead = 0 < ox - x < 60
                else:
                    ahead = 0 < x - ox < 60

            if same_lane and ahead:
                blocked = True
                break

        if blocked:
            speed = 0
        if direction == "down":
            if vertical_green or y < 175 or y > 180:
                y += speed
            if y > HEIGHT:
                y = -50

        elif direction == "up":
            if vertical_green or y > 385 or y < 380:
                y -= speed
            if y < -50:
                y = HEIGHT

        elif direction == "right":
            if not vertical_green or x < 325 or x > 330:
                x += speed
            if x > WIDTH:
                x = -60

        elif direction == "left":
            if not vertical_green or x > 530 or x < 525:
                x -= speed
            if x < -60:
                x = WIDTH

        car[1] = x
        car[2] = y

        if direction in ("down", "up"):
            pygame.draw.rect(
                screen, color, (x, y, 35, 50),
                border_radius=6
            )
        else:
            pygame.draw.rect(
                screen, color, (x, y, 50, 35),
                border_radius=6
            )

    # Display AI information
    title = font.render("AI SMART TRAFFIC SYSTEM", True, WHITE)
    screen.blit(title, (260, 25))

    decision = small_font.render(
        "AI Selected: " + best_direction,
        True, WHITE
    )
    screen.blit(decision, (20, 420))

    status = "VERTICAL GREEN" if vertical_green else "HORIZONTAL GREEN"

    screen.blit(
        small_font.render("Signal: " + status, True, WHITE),
        (20, 450)
    )

    reason = f"N:{traffic['North']}  S:{traffic['South']}  E:{traffic['East']}  W:{traffic['West']} vehicles"

    screen.blit(
        small_font.render(reason, True, WHITE),
        (20, 480)
    )

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
