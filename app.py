import pygame
import game_config as gc

from pygame import display, event, image,transform
from time import sleep
from demon import Demon

def find_index_from_xy(x, y):
    row = y // gc.IMAGE_SIZE
    col = x // gc.IMAGE_SIZE
    index = row * gc.NUM_TILES_SIDE + col
    return row, col, index

pygame.init()
display.set_caption('MathchingDemon')
screen = display.set_mode((gc.SCREEN_SIZE, gc.SCREEN_SIZE))
matched = image.load('other_assets/matched.png')
matched = transform.scale(matched,(900,900))
background = image.load('other_assets/backgroundx.png')
background = transform.scale(background,(900,900))
running = True
tiles = [Demon(i) for i in range(0, gc.NUM_TILES_TOTAL)]
current_images_displayed = []
score = 0
colorx = (186, 186, 186)
frame_count = 0
frame_rate = 60
start_time = 10
pygame.mixer.init()
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

while running:
    current_events = event.get()

    for e in current_events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col, index = find_index_from_xy(mouse_x, mouse_y)
            if index not in current_images_displayed:
                if len(current_images_displayed) > 1:
                    current_images_displayed = current_images_displayed[1:] + [index]
                else:
                    current_images_displayed.append(index)

    # Display 
    screen.fill((0 , 0 ,0))
    screen.blit(background ,(0,0))
    total_skipped = 0
    # Score   
    myfont = pygame.font.SysFont("GG25", 45)
    scoretext = myfont.render("Score = "+str(score),1,(186, 186, 186))
    screen.blit(scoretext, (150, 800))
    #Time
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 45)
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)    
    text = font.render(output_string, True, colorx)
    screen.blit(text, [550, 800])
    frame_count += 1
    clock.tick(frame_rate)
    if total_seconds == 0 :
      running = False  
     
    for i, tile in enumerate(tiles):
        current_image = tile.image if i in current_images_displayed else tile.box
        if not tile.skip:
            screen.blit(current_image, (tile.col * gc.IMAGE_SIZE + gc.MARGIN, tile.row * gc.IMAGE_SIZE + gc.MARGIN))
        else:
            total_skipped += 1

    display.flip()

    # Check for matches
    if len(current_images_displayed) == 2:
        idx1, idx2 = current_images_displayed
        if tiles[idx1].name == tiles[idx2].name:
            score += 1
            my_sound = pygame.mixer.Sound('sound/mathching.wav')
            my_sound.play()
            my_sound.set_volume(0.2)
            tiles[idx1].skip = True
            tiles[idx2].skip = True
            
            # display matched message
            sleep(0.2)
            screen.blit(matched, (10, 10))
            display.flip()
            sleep(0.5)
            current_images_displayed = []

    if total_skipped == len(tiles):
        running = False

print("YOUR SCORE IS " +str(score))