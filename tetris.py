import pygame as pg
import random

class Graphics:
    '''
    Handles all drawing operations for the game window, grid, and pieces.
    '''
    def __init__(self):
        self.screen = pg.display.set_mode((800, 1000))  # Set window size (width, height)
        pg.display.set_caption("Tetrus")
    def background(self):
        '''
        Draws the background and the grid for the Tetris play area.
        '''
        self.screen.fill((128, 128, 128))  
        pg.draw.rect(self.screen, (200, 200, 200), (100, 100, 400, 800))
        cell_size = 40
        for x in range(11):  # 10 columns need 11 lines
            pg.draw.line(self.screen, (100, 100, 100), (100 + x * cell_size, 100), (100 + x * cell_size, 900))
        for y in range(21):  # 20 rows need 21 lines
            pg.draw.line(self.screen, (100, 100, 100), (100, 100 + y * cell_size), (500, 100 + y * cell_size))   

    def draw_piece(self, piece):
        '''
        Draws a Tetris piece on the board at its current position and rotation.
        '''
        cell_size = 40
        for x, y in piece.get_blocks():
            pg.draw.rect(self.screen, piece.color, (100 + x*cell_size, 100 + y*cell_size, cell_size, cell_size))

class Piece:
    '''
    Represents a Tetris piece (tetromino), including its shape, color, position, and rotation.
    '''
    def __init__(self, shape_key):
        '''
        Initialize the piece with its shape, color, and position.
        '''
        self.shape_key = shape_key
        self.shape = SHAPES[shape_key]['shape']
        self.color = SHAPES[shape_key]['color']
        self.rotation = 0
        self.x = 0
        self.y = 0

    def get_blocks(self):
        '''
        Returns the absolute positions of all blocks in the current rotation.
        '''
        return [(x + self.x, y + self.y) for x, y in self.shape[self.rotation]]

    def rotate(self):
        '''
        Rotates the piece to the next rotation state.
        '''
        self.rotation = (self.rotation + 1) % len(self.shape)

if __name__ == "__main__":
    # Main game logic starts here
    SHAPES = {
        # Dictionary of all Tetris shapes and their colors
        'I': {
            'shape': [
                [(0,1), (1,1), (2,1), (3,1)],
                [(2,0), (2,1), (2,2), (2,3)],
                [(0,2), (1,2), (2,2), (3,2)],
                [(1,0), (1,1), (1,2), (1,3)]
            ],
            'color': (0, 255, 255)
        },
        'O': {
            'shape': [
                [(1,0), (2,0), (1,1), (2,1)]
            ],
            'color': (255, 255, 0)
        },
        'T': {
            'shape': [
                [(1,0), (0,1), (1,1), (2,1)],
                [(1,0), (1,1), (2,1), (1,2)],
                [(0,1), (1,1), (2,1), (1,2)],
                [(1,0), (0,1), (1,1), (1,2)]
            ],
            'color': (128, 0, 128)
        },
        'S': {
            'shape': [
                [(1,0), (2,0), (0,1), (1,1)],
                [(1,0), (1,1), (2,1), (2,2)],
                [(1,1), (2,1), (0,2), (1,2)],
                [(0,0), (0,1), (1,1), (1,2)]
            ],
            'color': (0, 255, 0)
        },
        'Z': {
            'shape': [
                [(0,0), (1,0), (1,1), (2,1)],
                [(2,0), (1,1), (2,1), (1,2)],
                [(0,1), (1,1), (1,2), (2,2)],
                [(1,0), (0,1), (1,1), (0,2)]
            ],
            'color': (255, 0, 0)
        },
        'J': {
            'shape': [
                [(0,0), (0,1), (1,1), (2,1)],
                [(1,0), (2,0), (1,1), (1,2)],
                [(0,1), (1,1), (2,1), (2,2)],
                [(1,0), (1,1), (0,2), (1,2)]
            ],
            'color': (0, 0, 255)
        },
        'L': {
            'shape': [
                [(2,0), (0,1), (1,1), (2,1)],
                [(1,0), (1,1), (1,2), (2,2)],
                [(0,1), (1,1), (2,1), (0,2)],
                [(0,0), (1,0), (1,1), (1,2)]
            ],
            'color': (255, 165, 0)
        }
    }
    fall_time = 0  # Counter for piece falling
    fall_speed = 30  # How many frames before the piece falls one cell

    move_delay = 30  # Frames between moves when holding a key
    move_left_counter = 0  # Counter for holding left
    move_right_counter = 0  # Counter for holding right
    move_down_counter = 0  # Counter for holding down




    clock = pg.time.Clock()  # Controls the frame rate
    pg.init()  # Initialize pygame
    graphics = Graphics()  # Create graphics handler
    running = True  # Main loop flag
    current_piece = Piece(random.choice(list(SHAPES.keys())))  # The current falling piece

    while running:
        '''
        Main game loop:
        - Handles timing, drawing, piece falling, and input.
        '''
        clock.tick(60)  # Limit to 60 FPS
        graphics.background()   # Draw background and grid
        graphics.draw_piece(current_piece)  # Draw the current piece

        # Handle falling piece
        fall_time += 1
        if fall_time >= fall_speed:
            current_piece.y += 1  # Move piece down
            fall_time = 0

        pg.display.flip()  # Update the display

        # --- INPUT HANDLING ---
        keys = pg.key.get_pressed()
        # Left movement (tricky: only move once per delay interval)
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            move_left_counter += 1
            if move_left_counter == 1 or move_left_counter > move_delay:
                current_piece.x -= 1  # Only move if delay threshold met
        else:
            move_left_counter = 0

        # Right movement (tricky: only move once per delay interval)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            move_right_counter += 1
            if move_right_counter == 1 or move_right_counter > move_delay:
                current_piece.x += 1
        else:
            move_right_counter = 0

        # Down movement (tricky: only move once per delay interval)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            move_down_counter += 1
            if move_down_counter == 1 or move_down_counter > move_delay:
                current_piece.y += 1
        else:
            move_down_counter = 0

        # Handle quit event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    pg.quit()  # Quit pygame when the game loop ends