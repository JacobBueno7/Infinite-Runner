import random, pygame, math, time
pygame.init()

# Constants
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 800
HEIGHT = 800
FPS = 60

# Variables
player_x = 200
player_y = 400
score = 0
y_change = 15
gravity = 1
scroll_x = 0 
last_obstacle_time = 0
spawn_rate = 2
obstacle_speed = 3
obstacles = []
timer = 5


clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("infinite runner")
font = pygame.font.SysFont('Comic Sans MS', 30)

running = True
jumping = False

def spawner():
    scored = False
    obstacle_height = random.randint(30, 60)
    obstacle_width = 20
    obstacle_x = random.randint(WIDTH, WIDTH+200)
    obstacle_y = 430
    obstacles.append([obstacle_width, obstacle_height, obstacle_x, obstacle_y, obstacle_speed, scored])

def dead():
    global score, screen
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill(BLACK)
        end_text = font.render("Game Over!", True, WHITE, BLACK)
        score_text = font.render(f'Score: {score}', True, WHITE, BLACK)
        screen.blit(end_text, (350, 350))
        screen.blit(score_text, (350, 400))
        pygame.display.flip()


while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    score_text = font.render(f'Score: {score}', True, WHITE, BLACK)
    screen.blit(score_text, (50, 50))
    curr_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    floor = pygame.draw.rect(screen, WHITE, [0, 430, WIDTH, 5])
    player = pygame.draw.rect(screen, RED, [player_x, player_y, 30, 30])
    keys = pygame.key.get_pressed()

    # Jumping
    if keys[pygame.K_SPACE]:
        jumping = True
    if jumping or player_y < 400:
        player_y -= y_change 
        y_change -= gravity
    if player_y > 400:
        player_y = 400
    if player_y == 400 and y_change != 15:
        y_change = 15
    jumping = False

    # Obstacles
    for object in obstacles:
        object[2] -= object[4]
        wall = pygame.draw.rect(screen, BLUE, [object[2], object[3]-object[1], object[0], object[1]])
        if wall.colliderect(player):
            running = False
            dead()

        if object[2] == -100:
            obstacles.remove(object)

        if object[2] < player_x and object[5] == False:
            score += 1
            object[5] = True
    
    if curr_time-last_obstacle_time > spawn_rate:
        spawner()
        last_obstacle_time = curr_time
        obstacle_speed += 0.1
        timer -= 1
        if timer == 0:
            if spawn_rate - 0.2 != 0:
                spawn_rate -= 0.2
            timer = 5

    pygame.display.flip()

pygame.quit()
