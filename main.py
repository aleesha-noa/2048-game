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


##### CLASSES #####
class Tile:
    # set the colours of the different tile values
    # colours for 2, 4, 8, 16, 32, 64, etc.
    COLOURS = [
        (237, 229, 218), 
        (238, 225, 201), 
        (243, 178, 122), 
        (246, 150, 101), 
        (247, 124, 95), 
        (247, 95, 59), 
        (237, 208, 115), 
        (237, 204, 99), 
        (236, 202, 80)
    ]

    def __init__(self, value, row, col):
        # for each tile, need to know its position (row and column) and its value
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_colour(self):
        colour_index = int(math.log2(self.value)) - 1 # need to subtract one since base is 0
        colour = self.COLOURS[colour_index]
        return colour # gives colour based on value of the tile


    def draw(self, window):
        # draw the rectangle than the value after

        colour = self.get_colour()
        pygame.draw.rect(window, colour, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOUR) # created a surface that contains the text
        window.blit(
            text, 
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2), 
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)
            )
        )

    def set_position(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_HEIGHT)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


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

def get_random_position(tiles):
    # make sure not to place tile in a tile that already exists
    row = None
    col = None
    
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set() # tells which tiles have already merged in a specific movement

    # go through response for each possibility (left, right, up down)
    # if user presses left arrow key
    if direction == "left":
        sort_function = lambda x: x.col
        reverse = False # whether to sort in ascending or descending order
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0 # if equal to 0, already as far left as the tile can go
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}") # looking to the tile to the left of the current tile
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL # whether or not we should merge the tile based on the current movement of that tile
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL # when moving but tile to the left is not the same value as the current tile
        ceil = True
    
    # if user presses right arrow key
    elif direction == "right":
        sort_function = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col +1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    
    # if user presses up arrow key
    elif direction == "up":
        sort_function = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    
    # if user presses down arrow key
    elif direction == "down":
        sort_function = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_function, reverse=reverse)

        for j, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            # getting next tile
            next_tile = get_next_tile(tile)

            # if no next tile, just move
            if not next_tile:
                tile.move(delta)

            # if there is a next tile, and that value is the same as the current value, then initiative merge operation
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else: # perform merge operation
                    next_tile.value *= 2
                    sorted_tiles.pop(j)
                    blocks.add(tile)

            # now have a next tile that is not the same as the current one, so only move to the border of the next tile
            elif move_check(tile, next_tile):
                tile.move(delta)

            # if none of the above is true, just continue and don't update (no merge operation)
            else:
                continue
            
            tile.set_position(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)

    return end_game(tiles)

def end_game(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row, col = get_random_position(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col) # choose to add either a 2 or 4 tile
    return "continue"

def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)

def generate_tiles():
    # randomly pick two positions to put the tiles in
    tiles = {}
    
    for i in range(2):
        row, col = get_random_position(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    
    return tiles

def main(window):
    clock = pygame.time.Clock() # regulate the speed of the loop
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


    pygame.quit()

pygame.quit()


if __name__ == "__main__":
    main(WINDOW) # running the game on the specified window