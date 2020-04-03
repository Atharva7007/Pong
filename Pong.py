import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()

# Setting the main window
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.Font("freesansbold.ttf", 32)

# Defining ball characteristics
ball = pygame.Rect(SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 - 10, 20, 20)
ball_speed_x = 5
ball_speed_y = 5

PAD_WIDTH = 10
PAD_HEIGHT = 80

player_pad_y = (SCREEN_HEIGHT - PAD_HEIGHT) / 2
player_pad_y_change = 0
player_pad = pygame.Rect(5, player_pad_y, PAD_WIDTH, PAD_HEIGHT)
player_score_value = 0
player_game_score = 0

opponent_pad_y = (SCREEN_HEIGHT - PAD_HEIGHT) / 2
opponent_pad_y_change = 0
opponent_pad = pygame.Rect(SCREEN_WIDTH - PAD_WIDTH - 5, opponent_pad_y, PAD_WIDTH, PAD_HEIGHT)
opponent_score_value = 0
opponent_game_score = 0

FPS = 60 # Frames per second limit

WHITE = (255, 255, 255) # RGB for paddle and ball colour



running = True

# Game loop
while running:
    screen.fill((0, 0,  40))
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            # Player movement
            if event.key == pygame.K_w: # Go up if W is pressed
                player_pad_y_change = -7
            elif event.key == pygame.K_s: # Go down if S is pressed
                player_pad_y_change = 7

            # Opponent movement using arrowkeys
            if event.key == pygame.K_UP:
                opponent_pad_y_change = -7
            elif event.key == pygame.K_DOWN:
                opponent_pad_y_change = 7

        # Stop moving if KEY_UP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_pad_y_change = 0
            elif event.key == pygame.K_s:
                player_pad_y_change = 0

            if event.key == pygame.K_UP:
                opponent_pad_y_change = 0
            elif event.key == pygame.K_DOWN:
                opponent_pad_y_change = 0

    # Updating opponent pad location
    opponent_pad_y += opponent_pad_y_change
    opponent_pad = pygame.Rect(SCREEN_WIDTH - PAD_WIDTH - 5, opponent_pad_y, PAD_WIDTH, PAD_HEIGHT)

    # Ball collision with left side of the screen
    if ball.x <= 0 :
        # Teleport the ball back to the centre
        ball.x = SCREEN_WIDTH / 2 - 10
        ball.y = SCREEN_HEIGHT / 2 - 10

        opponent_score_value += 1 # Opponent scores

        # Randomize ball's motion after teleportation
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    # Ball collision with right side of the screen
    if ball.x >= SCREEN_WIDTH:
        # Teleport the ball back to the centre
        ball.x = SCREEN_WIDTH / 2 - 10
        ball.y = SCREEN_HEIGHT / 2 - 10

        player_score_value += 1 # Player scores

        # Randomize ball's motion after teleportation
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

    if player_score_value > 10:
        player_game_score += 1
        player_score_value = 0
        opponent_score_value = 0
    elif opponent_score_value > 10:
        opponent_game_score += 1
        opponent_score_value = 0
        player_score_value = 0

    # Check if ball hits the top or bottom of the screen
    if ball.y <= 50 or ball.y >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Collision detection between ball and paddle
    if ball.colliderect(player_pad):
        ball_speed_x *= -1
    if ball.colliderect(opponent_pad):
        ball_speed_x *= -1

    # Update ball's speed
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Paddle cannot go outside the playing screen
    if player_pad.top <= 50:
        player_pad_y = 50
    if player_pad_y + PAD_HEIGHT >= SCREEN_HEIGHT:
        player_pad_y = SCREEN_HEIGHT - PAD_HEIGHT

    # Paddle cannot go outside playing screen
    if opponent_pad.top <= 50:
        opponent_pad_y = 50
    if opponent_pad_y + PAD_HEIGHT >= SCREEN_HEIGHT:
        opponent_pad_y = SCREEN_HEIGHT - PAD_HEIGHT

    # Update player's pad position
    player_pad_y += player_pad_y_change
    player_pad = pygame.Rect(5, player_pad_y, PAD_WIDTH, PAD_HEIGHT)

    # Drawing all the stuff on the screen
    pygame.draw.rect(screen, WHITE, player_pad)
    pygame.draw.rect(screen, WHITE, opponent_pad)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    pygame.draw.aaline(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))
    pygame.draw.ellipse(screen, WHITE, ball)

    # Render the scores
    player_score = font.render(str(player_score_value), True, (255, 255, 255))
    opponent_score = font.render(str(opponent_score_value), True, (255, 255, 255))

    player_score_display = font.render(str(player_game_score), True, (255, 255, 255))
    opponent_score_display = font.render(str(opponent_game_score), True, (255, 255, 255))

    # Display the scores
    screen.blit(player_score, (SCREEN_WIDTH / 2 - 80, 10))
    screen.blit(opponent_score, (SCREEN_WIDTH / 2 + 50, 10))

    screen.blit(player_score_display, (50, 10))
    screen.blit(opponent_score_display, (SCREEN_WIDTH - 50, 10))

    pygame.display.update()
