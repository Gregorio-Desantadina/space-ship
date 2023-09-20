import pygame
import sqlite3
import math
from pygame.locals import *
from config import *
from objects.asteroid import Asteroid
from objects.ship import Ship
from DB import *

# Initialize Pygame
pygame.init()

# Set up some properties
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 30
font = pygame.font.Font(None, 36)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (200,200,100)

count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_bg():
    screen.fill(BLACK)

def get_event_keys(events):
    keys = []
    for event in events:
        if event.type == pygame.KEYDOWN:
            keys.append(pygame.key.name(event.key))
    return keys

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


SkinSelect = False

def skin_selector(cursor, char2number, SkinList):
    character_selector = True
    while character_selector == True:
        clock.tick(FPS)
        draw_bg()
        events = pygame.event.get()
        key = pygame.key.get_pressed()

        draw_text(f"Skin: {char2number}"  , score_font, BLUE , 60, 250)
        

        if 'up' in get_event_keys(events) and SkinSelect == False:
            char2number = math.ceil((char2number + 1) % SkinList) 
            print(char2number)
        if 'down' in get_event_keys(events) and SkinSelect == False:
            char2number = math.ceil((char2number - 1) % SkinList)
            print(char2number)
        if '[1]' in get_event_keys(events):
            cursor.execute(f"UPDATE user SET id_skin = {char2number} WHERE id = 1")
            cursor.execute("SELECT id_skin FROM user WHERE id = 1")
            hola = cursor.fetchone()
            print(hola)
            character_selector = False
        pygame.display.update()



def game_loop(cursor, skin):
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Create the player
    player = Ship(skin)
    all_sprites.add(player)

    # Create the asteroids
    for i in range(10):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    # Score
    score = 0

    # Load the high score
    cursor.execute("SELECT MAX(score) FROM scores")
    high_score = cursor.fetchone()[0]
    if high_score is None:
        high_score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Update
        all_sprites.update()

        # Collision detection
        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits:
            # Game over
            return score

        # Draw everything
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Draw the score
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw the high score
        high_score_text = font.render(str(high_score), True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(60)

        # Increase the score
        score += 1

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)

    # Create the database if it doesn't exist
    cursor = conn.cursor()
    init_db(conn)

    # LIMIT skins
    cursor.execute("SELECT count(id) from skins")
    SkinList = cursor.fetchall()[0][0]
    print(SkinList)

    # SKIN selector
    cursor.execute("SELECT id_skin FROM user LIMIT 1")
    char2number = cursor.fetchone()[0]
    skin_selector(cursor, char2number, SkinList)
    
    

    # Select the skin
    cursor.execute("SELECT skin_dir FROM skins INNER JOIN user ON skins.id = user.id_skin")
    SKIN_DIR = cursor.fetchall()[0][0]

    # Run the game loop
    score = game_loop(cursor, SKIN_DIR)

    # Save the score
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
