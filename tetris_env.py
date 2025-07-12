import numpy as np
import random

class TetrisEnv:
    def __init__(self):
        self.grid_width = 10
        self.grid_height = 20
        self.SHAPES = {
            'I': {'shape': [[(0,1), (1,1), (2,1), (3,1)], [(2,0), (2,1), (2,2), (2,3)]], 'color': (0, 255, 255)},
            'O': {'shape': [[(1,0), (2,0), (1,1), (2,1)]], 'color': (255, 255, 0)},
            'T': {'shape': [[(1,0), (0,1), (1,1), (2,1)], [(1,0), (1,1), (2,1), (1,2)], [(0,1), (1,1), (2,1), (1,2)], [(1,0), (0,1), (1,1), (1,2)]], 'color': (128, 0, 128)},
            'S': {'shape': [[(1,0), (2,0), (0,1), (1,1)], [(1,0), (1,1), (2,1), (2,2)]], 'color': (0, 255, 0)},
            'Z': {'shape': [[(0,0), (1,0), (1,1), (2,1)], [(2,0), (1,1), (2,1), (1,2)]], 'color': (255, 0, 0)},
            'J': {'shape': [[(0,0), (0,1), (1,1), (2,1)], [(1,0), (2,0), (1,1), (1,2)], [(0,1), (1,1), (2,1), (2,2)], [(1,0), (1,1), (0,2), (1,2)]], 'color': (0, 0, 255)},
            'L': {'shape': [[(2,0), (0,1), (1,1), (2,1)], [(1,0), (1,1), (1,2), (2,2)], [(0,1), (1,1), (2,1), (0,2)], [(0,0), (1,0), (1,1), (1,2)]], 'color': (255, 165, 0)}
        }
        self.action_space = 5  # 0: None, 1: Left, 2: Right, 3: Rotate, 4: Down
        self.reward_dict = {
        0: 0,
        1: 40,
        2: 100, 
        3: 300, 
        4: 1200
        }  
        self.reset()

    class Piece:
        def __init__(self, shape_key, shapes):
            self.shape_key = shape_key
            self.shape = shapes[shape_key]['shape']
            self.rotation = 0
            self.x = 3
            self.y = 0

        def get_blocks(self):
            return [(x + self.x, y + self.y) for x, y in self.shape[self.rotation]]

        def rotate(self, locked_grid, grid_width, grid_height):
            old_rotation = self.rotation
            old_x = self.x
            old_y = self.y
            self.rotation = (self.rotation + 1) % len(self.shape)
            if not self.is_within_grid(grid_width, grid_height) or self.collides_with_another_piece(locked_grid):
                self.rotation = old_rotation
                self.x = old_x
                self.y = old_y

        def is_within_grid(self, grid_width, grid_height):
            for x, y in self.get_blocks():
                if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
                    return False
            return True

        def collides_with_another_piece(self, locked_grid):
            for x, y in self.get_blocks():
                if y >= len(locked_grid) or x >= len(locked_grid[0]) or locked_grid[y][x]:
                    return True
            return False

    def reset(self):
        self.locked_grid = [[False for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.score = 0
        self.lines_cleared = 0
        self.current_piece = self.Piece(random.choice(list(self.SHAPES.keys())), self.SHAPES)
        self.next_piece = self.Piece(random.choice(list(self.SHAPES.keys())), self.SHAPES)
        self.done = False
        return self.get_state()

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True

        # Actions: 0: No-op, 1: Left, 2: Right, 3: Rotate, 4: Down, 
        if action == 1:
            self.current_piece.x -= 1
            if not self.current_piece.is_within_grid(self.grid_width, self.grid_height) or self.current_piece.collides_with_another_piece(self.locked_grid):
                self.current_piece.x += 1
        elif action == 2:
            self.current_piece.x += 1
            if not self.current_piece.is_within_grid(self.grid_width, self.grid_height) or self.current_piece.collides_with_another_piece(self.locked_grid):
                self.current_piece.x -= 1
        elif action == 3:
            self.current_piece.rotate(self.locked_grid, self.grid_width, self.grid_height)
        elif action == 4:
            self.current_piece.y += 1
            if not self.current_piece.is_within_grid(self.grid_width, self.grid_height) or self.current_piece.collides_with_another_piece(self.locked_grid):
                self.current_piece.y -= 1

        # Move piece down by one (gravity)
        self.current_piece.y += 1
        if not self.current_piece.is_within_grid(self.grid_width, self.grid_height) or self.current_piece.collides_with_another_piece(self.locked_grid):
            self.current_piece.y -= 1
            # Lock the piece
            for x, y in self.current_piece.get_blocks():
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    self.locked_grid[y][x] = True
            # Check for line clears
            lines_cleared = 0
            new_locked = []
            for y in range(self.grid_height):
                if all(self.locked_grid[y]):
                    lines_cleared += 1
                else:
                    new_locked.append(self.locked_grid[y][:])
            for _ in range(lines_cleared):
                new_locked.insert(0, [False]*self.grid_width)
            self.locked_grid = new_locked
            self.lines_cleared += lines_cleared
            reward = self.reward_dict.get(lines_cleared, 0)
            # Spawn next piece
            self.current_piece = self.next_piece
            self.next_piece = self.Piece(random.choice(list(self.SHAPES.keys())), self.SHAPES)
            # Check for game over
            if self.current_piece.collides_with_another_piece(self.locked_grid):
                self.done = True
                return self.get_state(), reward, True
            return self.get_state(), reward, False
        return self.get_state(), 0, False

    def get_state(self):
        # State: grid + current piece position/shape/rotation (simple version)
        grid = np.array(self.locked_grid, dtype=np.float32)
        piece_grid = np.zeros_like(grid)
        for x, y in self.current_piece.get_blocks():
            piece_grid[y][x] = 1.0
        state = np.stack([grid, piece_grid], axis=0)  # Shape: (2, 20, 10)
        return state