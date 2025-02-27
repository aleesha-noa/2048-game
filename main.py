import pygame
import random
import math

# initialize pygame
pygame.init()

##### GLOBAL VARIABLES #####
FPS = 60 # frames per second

# want game board to be a square, so HEIGHT == WIDTH
WIDTH = 800
HEIGHT = 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

# make outline grey (in RGB)
OUTLINE_COLOUR = (157, 155, 155)

# choose thickness of outline
OUTLINE_THICKNESS = 10

# set background and font colour
BACKGROUND_COLOUR = (205, 110, 101)
FONT_COLOUR = (119, 110, 101)

# use this to render text onto the screen
#TODO: change font
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20 # speed at which tiles will move in pixels per second

# make the display window in pygame
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

##### METHODS #####

def draw_grid(window):
    # draw horizontal and vertical lines to represent the separation between tiles and the border

    # first draw horizontal gridlines
    for row in range(1, ROWS): # draw a line for every row that is there, start at one and not zero since the first line is part of the border
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOUR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    # next draw vertical gridlines
    for col in range(1, COLS): # draw a line for every column line that is there, start at one and not zero since the first line is part of the border
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOUR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    # next do the border
    pygame.draw.rect(window, OUTLINE_COLOUR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window):
    window.fill(BACKGROUND_COLOUR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()    
  
    window.fill(BACKGROUND_COLOUR)
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock() # regulate the speed of the loop
    run = True

    while run:
        clock.rick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


    pygame.quit()

pygame.quit()


if __name__ == "__main__":
    main(WINDOW) # running the game on the specified window