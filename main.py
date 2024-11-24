import pygame
import numpy as np

pygame.init()

# window size
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gra w życie")

# grid settings
rows, cols = 100, 100
cell_size = screen_height // rows
alive, dead = 1, 0
grid = np.zeros((rows, cols), dtype=int)
running = False

#kolory
WHITE = (0, 100, 190)
BLACK = (210, 200, 130)
BUTTON_COLOR = (210, 1, 150)

def init_glider(grid):
    grid[1, 2] = grid[2, 3] = grid[3, 1] = grid[3, 2] = grid[3, 3] = alive

def init_oscillator(grid):
    mid_row, mid_col = rows // 2, cols // 2
    grid[mid_row, mid_col - 1: mid_col + 2] = alive

def init_random(grid):
    grid[:, :] = np.random.choice([alive, dead], size=(rows, cols))

def init_still_life(grid):
    mid_row, mid_col = rows // 2, cols // 2
    grid[mid_row:mid_row + 2, mid_col:mid_col + 2] = alive

def init_HWSS(grid):
    grid[2,1]=grid[4,1]=grid[5,2:8]=grid[4,7]=grid[3,7] = grid[2,6] = grid[1,3:5] = alive

def init_beacon(grid):
    mid_row, mid_col = rows // 2, cols // 2
    grid[mid_row:mid_row+1, mid_col:mid_col+2] = alive
    grid[mid_row+1:mid_row+2, mid_col:mid_col+2] = alive

    grid[mid_row+2:mid_row+3, mid_col+2:mid_col+4] = alive
    grid[mid_row+3:mid_row+4, mid_col+2:mid_col+4] = alive

def init_loaf(grid):
    mid_row, mid_col = rows // 2, cols // 2
    grid[mid_row:mid_row+1, mid_col+1:mid_col+3] = alive

    grid[mid_row+1:mid_row+2,mid_col:mid_col+1] = alive
    grid[mid_row+1:mid_row+2,mid_col+3:mid_col+4] = alive

    grid[mid_row+2:mid_row+3,mid_col+1:mid_col+2] = alive
    grid[mid_row+2:mid_row+3,mid_col+3:mid_col+4] = alive

    grid[mid_row+3:mid_row+4,mid_col+2:mid_col+3] = alive

def count_neighbors(grid, periodic_boundary=True):
    if periodic_boundary:
        neighbors = (
            np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1) +
            np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1) +
            np.roll(grid, 1, 0) + np.roll(grid, -1, 0) +
            np.roll(grid, 1, 1) + np.roll(grid, -1, 1)
        )
    else:
        extended_grid = np.pad(grid, 1, mode='edge')
        neighbors = (
            extended_grid[:-2, :-2] + extended_grid[:-2, 1:-1] + extended_grid[:-2, 2:] +
            extended_grid[1:-1, :-2] + extended_grid[1:-1, 2:] +
            extended_grid[2:, :-2] + extended_grid[2:, 1:-1] + extended_grid[2:, 2:]
        )
    return neighbors

def update(grid):
    neighbors = count_neighbors(grid,periodic_boundary=True)
    new_grid = np.where((grid == alive) & ((neighbors == 2) | (neighbors == 3)), alive, dead)
    new_grid = np.where((grid == dead) & (neighbors == 3), alive, new_grid)
    return new_grid

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = WHITE if grid[row, col] == alive else BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            # pygame.draw.rect(screen, (50, 50, 50), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

def draw_buttons():
    buttons = [("Glider", 10), ("Oscillator", 110), ("Random", 210), ("Block", 310),("HWSS",410),("Beacon",510),("Loaf",610), ("Start", 710), ("Clear", 810)]
    for text, x in buttons:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, screen_height - 40, 90, 30))
        font = pygame.font.Font(None, 24)
        label = font.render(text, True, BLACK)
        screen.blit(label, (x + 10, screen_height - 35))
    return buttons

def initialize_pattern(pattern):
    global grid
    grid = np.zeros((rows, cols), dtype=int)
    if pattern == "Glider":
        init_glider(grid)
    elif pattern == "Oscillator":
        init_oscillator(grid)
    elif pattern == "Random":
        init_random(grid)
    elif pattern == "Block":
        init_still_life(grid)
    elif pattern == "HWSS":
        init_HWSS(grid)
    elif pattern == "Beacon":
        init_beacon(grid)
    elif pattern =="Loaf":
        init_loaf(grid)

def handle_button_click(pos):
    global running
    buttons = draw_buttons()
    for text, x in buttons:
        button_rect = pygame.Rect(x, screen_height - 40, 90, 30)
        if button_rect.collidepoint(pos):
            if text == "Start":
                running = not running
            elif text == "Clear":
                clear_grid()
            else:
                initialize_pattern(text)

def clear_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)

def toggle_cell(pos):
    row, col = pos[1] // cell_size, pos[0] // cell_size
    grid[row, col] = alive if grid[row, col] == dead else dead

clock = pygame.time.Clock()
while True:
    screen.fill(BLACK)
    draw_grid()
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] > screen_height - 40:
                handle_button_click(event.pos)
            else:
                toggle_cell(event.pos)

    if running:
        grid = update(grid)

    pygame.display.flip()
    clock.tick(10)

