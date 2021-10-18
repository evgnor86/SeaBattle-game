# --- SeaBattle game for practical work on SkillFactory FPW-2.0 course
# --- Evgeniy Ivanov, flow FPW-42, Okt'2021
import random


class OutOfBoardException(Exception):
    def __init__(self, message='Out of board'):
        super().__init__(message)


class Dot:
    def __init__(self, row=0, col=0, state='_'):
        self.row = row
        self.col = col
        self.state = state

    def __eq__(self, other):
        return True if self.state == other.state else False

    def __repr__(self):
        return str((self.row, self.col))

    def __str__(self):
        return self.state


class Ship:
    def __init__(self, horizontal=True, ship_size=1):
        self.ship_size = ship_size
        self.horizontal = horizontal
        self.dots = []
        self.set_position(0, 0)

    def __repr__(self):
        return str([int(dot.state) for dot in self.dots])

    def set_position(self, row=0, col=0):
        if self.horizontal:
            self.dots = [Dot(row, col + i, f'{self.ship_size}') for i in range(self.ship_size)]
        else:
            self.dots = [Dot(row + i, col, f'{self.ship_size}') for i in range(self.ship_size)]


class Board:
    @staticmethod
    def random_direction():
        return bool(((0, 1) * 5)[random.randint(0, 9)])

    def __init__(self, board_size: int):
        self.__iter = []
        self.board_size = board_size
        self.cells = [[Dot(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        self.ships_types = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        self.ships = [Ship(Board.random_direction(), ship_size) for ship_size in self.ships_types]
        self.random_set_ships()

    def random_set_ships(self):
        for ship in self.ships:
            while True:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                try:
                    self.move_ship(ship, row, col)
                except OutOfBoardException:
                    continue
                else:
                    break

    def move_ship(self, ship, row, col):
        # ---
        def collision():
            if ship.horizontal:
                _rows = [_row for _row in range(row - 1, row + 2) if 0 <= _row < self.board_size]
                _cols = [_col for _col in range(col - 1, col + ship.ship_size + 1) if 0 <= _col < self.board_size]
            else:
                _rows = [_row for _row in range(row - 1, row + ship.ship_size + 1) if 0 <= _row < self.board_size]
                _cols = [_col for _col in range(col - 1, col + 2) if 0 <= _col < self.board_size]
            for _row in _rows:
                for _col in _cols:
                    if self.cells[_row][_col].state != '_':
                        return True
            return False
        # ---
        if row + ship.ship_size > self.board_size or col + ship.ship_size > self.board_size:
            raise OutOfBoardException
        else:
            if collision():
                raise OutOfBoardException
            else:
                ship.set_position(row, col)
                for dot in ship.dots:
                    self.cells[dot.row][dot.col] = dot


class Game:
    def __init__(self):
        self.board_size = 10
        self.players = (
            Board(self.board_size),  # - Human board
            Board(self.board_size)  # - AI board
        )

    def __str__(self):
        top_panel = f'{" " * 12}PLAYER SHIPS{" " * 28}TARGET SHIPS\n'
        field = '|0||1||2||3||4||5||6||7||8||9|'
        field = f'{" " * 3}{field}{" " * 10}{field}\n'
        for line in range(self.board_size):
            field += f'|{line}| '
            for cell in self.players[0].cells[line]:
                field += f'{cell}  '
            field += ' ' * 6 + f'|{line}| '
            for cell in self.players[1].cells[line]:
                field += f'{cell}  '
            field += '\n'
        return top_panel + field


def start():
    # board = Board(10)
    # for ship in board.ships:
    #     print(ship.horizontal, ship.dots)

    game = Game()
    print(game)


if __name__ == '__main__':
    start()
