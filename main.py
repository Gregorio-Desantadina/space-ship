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



def skin_selector(current_skin_id, skin_list):

    # Get the amount of skins in the list
    menu_limit = len(skin_list)
    
    # Get a list of skin IDs
    # Also but not required, get a list of the skin paths
    skin_id_list, skin_dir_list = zip(*skin_list)
    #    current_skin_index = [(index, skin_data) for index, skin_data in enumerate(skin_list) if skin_data[0] == current_skin_id][0]
    
    # From this list of skin IDs, get the index of the current skin
    current_skin_index = skin_id_list.index(current_skin_id)
    
    # Get the current skin data from the skin list
    current_skin = skin_list[current_skin_index]
    
    # Initialize the menu values
    new_skin = current_skin
    menu_option = current_skin_index
    
    # Flow control var
    selecting = True
    
    while selecting:
        clock.tick(FPS)
        draw_bg()
        events = pygame.event.get()
        
        # Draw the menu      
        draw_text(f"Current skin: {current_skin}"  , score_font, GREEN , 60, 250)
        draw_text(f"Selecting skin: {new_skin}"  , score_font, BLUE , 60, 300)
        

        # Menu algorithm
        if 'up' in get_event_keys(events):
            menu_option = (menu_option + 1) % menu_limit
        if 'down' in get_event_keys(events):
            menu_option = (menu_option - 1) % menu_limit
        if '[1]' in get_event_keys(events):
            selecting = False
        
        # Update the SELECTED skin from the memory list (just list)
        new_skin = skin_list[menu_option]
        
        # Refresh the frame                   
        pygame.display.update()
       
       
    # Once it is accepted the NEW SELECTED skin, just grab the ID and return it 
    new_skin_id = new_skin[0]                      
    return new_skin_id



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
            if event.type == pygame.QUIT:
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



    # Pull all the data from the table SKINS, make an list in memory with it
    cursor.execute("SELECT * from skins")
    skin_list = cursor.fetchall()
    
    # Chose on porpuse, the USER to play
    user_id = 1
    
    
    # Get the skin ID that user is using
    cursor.execute(f"SELECT id_skin FROM user WHERE id = {user_id}")
    
    # ID de la skin usada actualmente
    current_skin_id = cursor.fetchone()[0]
    
    # Call the selector, it has to return the chosen new skin ID
    new_skin_id = skin_selector(current_skin_id, skin_list)
    
    # Update USER table
    cursor.execute(f"UPDATE user SET id_skin = {new_skin_id} WHERE id = {user_id}")
    conn.commit()
    

    # Select the skin
    cursor.execute(f"SELECT skin_dir FROM skins INNER JOIN user ON skins.id = user.id_skin WHERE user.id = {user_id}")
    SKIN_DIR = cursor.fetchone()[0]

    # Run the game loop
    score = game_loop(cursor, SKIN_DIR)

    # Save the score
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
