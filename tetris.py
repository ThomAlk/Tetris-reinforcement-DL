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
        pg.draw.rect(self.screen, (100, 100, 100), (550, 200, 200, 200))
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

    def draw_locked(self, color_grid):
        cell_size = 40
        for y, row in enumerate(color_grid):
            for x, color in enumerate(row):
                if color:
                    pg.draw.rect(self.screen, color, (100 + x*cell_size, 100 + y*cell_size, cell_size, cell_size))

    def draw_next_piece(self, piece):
        '''
        Draws the next piece in the preview area.
        '''
        cell_size = 40
        for x, y in piece.get_blocks():
            pg.draw.rect(self.screen, piece.color, (575 + (x-3)*cell_size, 250 + y*cell_size, cell_size, cell_size))

    def draw_game_over_overlay(self):
        '''
        Draws a semi-transparent game over overlay with text and instructions.
        '''
        overlay = pg.Surface((800, 1000), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with alpha for transparency
        self.screen.blit(overlay, (0, 0))
        # Draw the Game Over text
        font = pg.font.SysFont(None, 96)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 400))
        self.screen.blit(text, text_rect)
        # Draw a smaller instruction
        font_small = pg.font.SysFont(None, 48)
        text2 = font_small.render("Press any key to quit", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(400, 500))
        self.screen.blit(text2, text2_rect)

    def draw_score(self, score):
        '''
        Draws the current score on the screen.
        '''
        font = pg.font.SysFont(None, 48)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (600, 50))

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
        self.x = 3
        self.y = 0

    def get_blocks(self):
        '''
        Returns the absolute positions of all blocks in the current rotation.
        '''
        return [(x + self.x, y + self.y) for x, y in self.shape[self.rotation]]

    def rotate(self, locked_grid=None):
        '''
        Rotates the piece to the next rotation state, with wall kicks and collision checks if locked_grid is provided.
        '''
        old_rotation = self.rotation
        old_x = self.x
        old_y = self.y
        self.rotation = (self.rotation + 1) % len(self.shape)
        if locked_grid is not None:
            if not self.is_within_grid():
                self.push_into_grid()
            if self.collides_with_another_piece(locked_grid):
                kicked = False
                for dx in [-1, 1, -2, 2]:
                    self.x += dx
                    if not self.collides_with_another_piece(locked_grid) and self.is_within_grid():
                        kicked = True
                        break
                    self.x -= dx
                if not kicked:
                    # Try shifting up (rare, but for completeness)
                    for dy in [-1, -2]:
                        self.y += dy
                        if not self.collides_with_another_piece(locked_grid) and self.is_within_grid():
                            kicked = True
                            break
                        self.y -= dy
                if not kicked:
                    # Revert rotation if all kicks fail
                    self.rotation = old_rotation
                    self.x = old_x
                    self.y = old_y

    def is_within_grid(self, grid_width=10, grid_height=20):
        '''
        Returns True if all blocks of the piece are within the grid.
        '''
        for x, y in self.get_blocks():
            if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
                return False
        return True

    def push_into_grid(self, grid_width=10, grid_height=20):
        '''
        Shifts the piece back into the grid if any block is out of bounds.
        '''
        blocks = self.get_blocks()
        min_x = min(x for x, y in blocks)
        max_x = max(x for x, y in blocks)
        min_y = min(y for x, y in blocks)
        max_y = max(y for x, y in blocks)
        if min_x < 0:
            self.x += -min_x
        if max_x >= grid_width:
            self.x -= (max_x - (grid_width - 1))
        if min_y < 0:
            self.y += -min_y
        if max_y >= grid_height:
            self.y -= (max_y - (grid_height - 1))

    def collides_with_another_piece(self, locked_grid):
        for x, y in self.get_blocks():
            if locked_grid[y][x]:
                return True
        return False

def killing(_piece):
    '''
    Locks the piece into the grid and returns a new piece.
    '''
    global color_grid, locked_grid, next_piece
    for x, y in _piece.get_blocks():
        if 0 <= x < 10 and 0 <= y < 20:
            color_grid[y][x] = _piece.color
            locked_grid[y][x] = True
    piece = next_piece
    next_piece = Piece(random.choice(list(SHAPES.keys())))
    return piece 

def falling(_piece, fall_time, fall_speed):
        '''
        Handles the falling logic for the piece.
        '''
        fall_time += 1
        if fall_time >= fall_speed:
            _piece.y += 1  # Move piece down
            fall_time = 0
            # If piece is out of grid or collides, revert and lock
            if not _piece.is_within_grid() or _piece.collides_with_another_piece(locked_grid):
                _piece.y -= 1
                return killing(_piece), fall_time
        return _piece, fall_time

def line_check():
    '''
    Checks for full lines in locked_grid, removes them, and shifts above lines down in both locked_grid and color_grid.
    '''
    global locked_grid, color_grid, score
    new_locked = []
    new_color = []
    for y in range(20):
        if all(locked_grid[y]):
            # Skip this row (remove it)
            continue
        new_locked.append(locked_grid[y][:])
        new_color.append(color_grid[y][:])
    # Count how many lines were removed
    lines_removed = 20 - len(new_locked)
    score += score_dict.get(lines_removed)  # Update score based on lines removed

    # Add empty rows at the top
    for _ in range(lines_removed):
        new_locked.insert(0, [False]*10)
        new_color.insert(0, [None]*10)
    locked_grid = new_locked
    color_grid = new_color

def check_game_over(piece, locked_grid):
    '''
    Returns True if any block of the given piece would spawn in a locked cell.
    '''
    for x, y in piece.get_blocks():
        if locked_grid[y][x]:
            return True
    return False

if __name__ == "__main__":
    # Main game logic starts here
    SHAPES = {
        # Dictionary of all Tetris shapes and their colors
        'I': {
            'shape': [
                [(0,1), (1,1), (2,1), (3,1)],
                [(2,0), (2,1), (2,2), (2,3)]
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
                [(1,0), (1,1), (2,1), (2,2)]
            ],
            'color': (0, 255, 0)
        },
        'Z': {
            'shape': [
                [(0,0), (1,0), (1,1), (2,1)],
                [(2,0), (1,1), (2,1), (1,2)]
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
    
    #Fall
    fall_time = 0  # Counter for piece falling
    fall_speed = 30  # How many frames before the piece falls one cell
    
    #Movement
    move_delay = 30  # Frames between moves when holding a key
    move_left_counter = 0  # Counter for holding left
    move_right_counter = 0  # Counter for holding right
    move_down_counter = 0  # Counter for holding down


    #Grids
    color_grid = [[None for _ in range(10)] for _ in range(20)]
    locked_grid = [[False for _ in range(10)] for _ in range(20)]


    #Locking
    lock_delay_counter = 0
    lock_delay_frames = 30  # Number of frames before locking

    #Score
    score = 0
    score_dict= {
        0: 0,
        1: 40,
        2: 100, 
        3: 300, 
        4: 1200
        }  


    clock = pg.time.Clock()  # Controls the frame rate
    pg.init()  # Initialize pygame
    graphics = Graphics()  # Create graphics handler
    running = True  # Main loop flag
    current_piece = Piece(random.choice(list(SHAPES.keys())))  # The current falling piece
    next_piece = Piece(random.choice(list(SHAPES.keys())))  # The next piece to fall

    pg.mixer.init()
    pg.mixer.music.load("background_music.mp3")  
    pg.mixer.music.play(-1)

    while running:
        '''
        Main game loop:
        - Handles timing, drawing, piece falling, and input.
        '''
        clock.tick(60)  # Limit to 60 FPS
        graphics.background()   # Draw background and grid
        graphics.draw_piece(current_piece)  # Draw the current piece
        graphics.draw_locked(color_grid)  # Draw the locked pieces on the grid
        graphics.draw_next_piece(next_piece)  # Draw the next piece in the preview area
        graphics.draw_score(score)  # Draw the current score
        # Handle falling piece
        current_piece, fall_time = falling(current_piece, fall_time, fall_speed)

        # --- GAME OVER OVERLAY ---
 
        if check_game_over(current_piece, locked_grid):
            graphics.draw_game_over_overlay()
            pg.display.flip()
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                        waiting = False
            running = False
            continue

        # --- INPUT HANDLING ---
        keys = pg.key.get_pressed()
        # Left movement (tricky: only move once per delay interval)
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            move_left_counter += 1
            if move_left_counter == 1 or move_left_counter > move_delay:
                current_piece.x -= 1  # Only move if delay threshold met
                if not current_piece.is_within_grid() or current_piece.collides_with_another_piece(locked_grid):
                    current_piece.x += 1
        else:
            move_left_counter = 0

        # Right movement (tricky: only move once per delay interval)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            move_right_counter += 1
            if move_right_counter == 1 or move_right_counter > move_delay:
                current_piece.x += 1
                if not current_piece.is_within_grid() or current_piece.collides_with_another_piece(locked_grid):
                    current_piece.x -= 1
        else:
            move_right_counter = 0

        # Down movement (tricky: only move once per delay interval)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            move_down_counter += 1
            if move_down_counter == 1 or move_down_counter > move_delay:
                current_piece.y += 1
                if not current_piece.is_within_grid() or current_piece.collides_with_another_piece(locked_grid):
                    current_piece.y -= 1
        else:
            move_down_counter = 0


        # Handle quit event and rotation
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_z:
                    current_piece.rotate(locked_grid)

        line_check()
        pg.display.flip()  # Update the display
    pg.quit()  # Quit pygame when the game loop ends