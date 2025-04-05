import pygame
from pathlib import Path
pygame.font.init() # Initialize the font module of pygame
pygame.mixer.init() # Initialize the sound module in pygame


# Good practice is to define constants in all caps
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Make a window with specific width and height
pygame.display.set_caption("First Game!") # Set a description for the window name

# Define color constants (RGB format)
WHITE = (255,255,255) # Store the color tuple
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# Define a border for the game window (x position, y position, width, height)
BORDER = pygame.Rect((WIDTH/2) - 5 , 0, 10, HEIGHT) # Rectangle from (445, 0) to (455,0) (x position = 445)


HEALTH_FONT = pygame.font.SysFont('comicsans', 40) # Set the font for the health text
WINNER_FONT = pygame.font.SysFont('comicsans', 100) # Set the font for the winner text

FPS = 60 # Set frames per second
VELOCITY = 5 # Set movement speed of spaceship
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Define user events (numbers make sure it has a unique event id)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Define assets folder
ASSETS_FOLDER = Path(__file__).parent / 'Assets'

# Define spaceship image paths
YELLOW_SPACESHIP_PATH = ASSETS_FOLDER / 'spaceship_yellow.png'
RED_SPACESHIP_PATH = ASSETS_FOLDER / 'spaceship_red.png'
SPACE_PATH = ASSETS_FOLDER / 'space.png'

# Save images in pygame image variable
YELLOW_SPACESHIP_IMAGE = pygame.image.load(YELLOW_SPACESHIP_PATH)
RED_SPACESHIP_IMAGE = pygame.image.load(RED_SPACESHIP_PATH)
SPACE_IMAGE = pygame.image.load(SPACE_PATH)

# Define sound paths
BULLET_HIT_PATH = ASSETS_FOLDER / 'Grenade+1.mp3'
BULLET_FIRE_PATH = ASSETS_FOLDER / 'Gun+Silencer.mp3'

# Load sound paths as pygame sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(BULLET_HIT_PATH)
BULLET_FIRE_SOUND = pygame.mixer.Sound(BULLET_FIRE_PATH)


# Rescale space image
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

# Rescale and rotate images
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90
)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """Function that handles the movement of bullets, handle the collision, and handle removing bullets when they collide or move off screen"""
    # Check if yellow bullet collided with end of screen or red spaceship
    for bullet in yellow_bullets:
        # Move the bullet
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet): # Note: there's a colliderect call in pygame that will tell you if two rectangles collided
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) # Remove the bullet from yellow_bullet list
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        # Move the bullet
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet): # Note: there's a colliderect call in pygame that will tell you if two rectangles collided
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet) # Remove the bullet from red_bullet list
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
     draw_text = WINNER_FONT.render(text, 1, WHITE)
     WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

     pygame.display.update()
     pygame.time.delay(5000)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        """Function that draws the window and all the objects in it"""
        WIN.blit(SPACE, (0,0)) # Sets the background of the window (takes a tuple in RGB format)
        pygame.draw.rect(WIN,BLACK,BORDER) # Draw the border in the middle of the screen

        # Draw the health of each spaceship
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE) # Render the text
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE) # Render the text
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10,10))

        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # Use this when a surface needs to be drawn onto the screen
        WIN.blit(RED_SPACESHIP, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet) # Draw the red bullets

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet) # Draw the yellow bullets
             
        # Note: When you draw, it draws from top left hand corner so (0,0) is top left corner
        # Order matters when drawing surfaces, you can draw on top of something
        # When we draw things in pygame, the window won't be updated until explicitly updated
        pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
        """Function that handles the movement of the yellow spaceship"""
        if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0 : # Left key
             yellow.x -= VELOCITY
        if keys_pressed[pygame.K_d] and yellow.x + yellow.width - 20 + VELOCITY < BORDER.x: # Right key
             yellow.x += VELOCITY
        if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: # Up key
             yellow.y -= VELOCITY
        if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VELOCITY < HEIGHT - 15: # Down key
             yellow.y += VELOCITY

def red_handle_movement(keys_pressed, red):
        """Function that handles the movement of the red spaceship"""
        if keys_pressed[pygame.K_LEFT] and red.x - 5 -  VELOCITY > BORDER.x: # Left key
             red.x -= VELOCITY
        if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY < WIDTH: # Right key
             red.x += VELOCITY
        if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: # Up key
             red.y -= VELOCITY
        if keys_pressed[pygame.K_DOWN] and red.y + red.height + VELOCITY < HEIGHT - 15: # Down key
             red.y += VELOCITY

# Things game loops handle
# Redraws the window
# Checks for collisions
# Update the score
# Update player position, etc.
def main():
    red = pygame.Rect(800, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Arguments for Rect: x position, y position, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Arguments for Rect: x position, y position, width, height

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    # Set up a while loop for an infinite loop until the game ends
    # This is necessary so the game doesn't instantly open and then close
    run = True
    while run:
        clock.tick(FPS) # Controls the speed of this while loop
        # This is the first step for every event loop in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check if user quit the window
                run = False # Ends the while loop
                pygame.quit() # Quits the game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        print(yellow_bullets)
        keys_pressed = pygame.key.get_pressed()

        if winner_text != "":
            draw_winner(winner_text)
            break

        # Handle movement for each spaceship
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) # Draw the window and all the objects in it

    main() # The game restarts when the while loop breaks

if __name__ == "__main__":
    main()