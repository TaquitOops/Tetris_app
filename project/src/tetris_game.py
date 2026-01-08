import random
from typing import List, Tuple

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 25

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': '#00f0f0',
    'O': '#f0f000',
    'T': '#a000f0',
    'S': '#00f000',
    'Z': '#f00000',
    'J': '#0000f0',
    'L': '#f0a000'
}


class Piece:
    def __init__(self, shape_type: str):
        self.type = shape_type
        self.shape = SHAPES[shape_type]
        self.color = COLORS[shape_type]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_cells(self) -> List[Tuple[int, int]]:
        cells = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    cells.append((self.x + x, self.y + y))
        return cells


class TetrisGame:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.spawn_piece()
        self.spawn_next_piece()

    def spawn_piece(self):
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            shape_type = random.choice(list(SHAPES.keys()))
            self.current_piece = Piece(shape_type)

        if not self.is_valid_position(self.current_piece):
            self.game_over = True

    def spawn_next_piece(self):
        shape_type = random.choice(list(SHAPES.keys()))
        self.next_piece = Piece(shape_type)

    def is_valid_position(self, piece: Piece, offset_x: int = 0, offset_y: int = 0) -> bool:
        for x, y in piece.get_cells():
            new_x = x + offset_x
            new_y = y + offset_y

            if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                return False

            if new_y >= 0 and self.board[new_y][new_x] is not None:
                return False

        return True

    def move_piece(self, dx: int, dy: int) -> bool:
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self) -> bool:
        original_shape = self.current_piece.shape
        self.current_piece.rotate()

        if not self.is_valid_position(self.current_piece):
            self.current_piece.shape = original_shape
            return False
        return True

    def lock_piece(self):
        for x, y in self.current_piece.get_cells():
            if y >= 0:
                self.board[y][x] = self.current_piece.color

        self.clear_lines()
        self.spawn_piece()
        self.spawn_next_piece()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board[y][x] is not None for x in range(BOARD_WIDTH)):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [None for _ in range(BOARD_WIDTH)])

        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(len(lines_to_clear), 100) * self.level

            if self.lines_cleared >= self.level * 10:
                self.level += 1

    def drop_piece(self) -> bool:
        if not self.move_piece(0, 1):
            self.lock_piece()
            return False
        return True

    def hard_drop(self):
        while self.move_piece(0, 1):
            pass
        self.lock_piece()

    def reset_board(self):
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.game_over = False
        self.spawn_piece()
        self.spawn_next_piece()

    def reduce_score(self):
        self.score = self.score // 2
