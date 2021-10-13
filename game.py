# --- SeaBattle game for practical work on SkillFactory FPW-2.0 course
# --- Evgeniy Ivanov, flow FPW-42, Okt'2021

import random


DOT_STATES = {
    'blank': '-',  # - sea wave (start cell state)
    'hit':   'H',  # - hit strike
    'miss':  'M',  # - miss strike
    1: '1',        # - ship1 part
    2: '2',        # - ship2 part
    3: '3',        # - ship3 part
    4: '4',        # - ship4 part
}


class CellBusy(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotValidState(Exception):
    def __init__(self, message):
        super().__init__(message)


class OutOfBoard(Exception):
    def __init__(self, message):
        super().__init__(message)


class WrongCellState(Exception):
    def __init__(self, message):
        super().__init__(message)


class Cell:

    def __init__(self, start_state):
        if start_state in DOT_STATES.values():
            self.state = start_state
        else:
            raise WrongCellState(f'Wrong cell state {start_state}')

    def __str__(self):
        return self.state

    @property
    def no_busy(self):
        return True if self.state == DOT_STATES['blank'] else False


class Board:
    """
        Why operator 'pass' not implement to 'if-else' linear expression?
        Construction '<func/operation> if <expression> else pass' throws SyntaxError in Python 3.9
        It's stupid bug =) Posted issue report to https://bugs.python.org/issue45456
    """

    def __init__(self, board_size):
        self.board_size = board_size  # - width, height
        self.cells = [[Cell(DOT_STATES['blank']) for cell in range(self.board_size)] for cell in range(self.board_size)]

    def find_blank_cells(self, horizontal_direction, ship_size):
        # -- Check blank cells + check left, top for col & check top, bottom for row
        # -- Not 100% work but makes board fill more rarefied
        def check(_row, _col):
            def check_around():
                # -- Bullshit code but it work =) will be refactored in future
                _row_top = _row + 1 if _row + 1 < self.board_size else _row
                _row_bottom = _row - 1 if _row - 1 > 0 else _row
                _col_right = _col + 1 if _col + 1 < self.board_size else _col
                _col_left = _col - 1 if _col - 1 > 0 else _col

                return all([
                            self.cells[_row_top][_col_right].no_busy,
                            self.cells[_row_top][_col_left].no_busy,
                            self.cells[_row_bottom][_col_right].no_busy,
                            self.cells[_row_bottom][_col_left].no_busy,
                            0 < _col_right < self.board_size, 0 < _col_left < self.board_size,
                            0 < _row_top < self.board_size, 0 < _row_bottom < self.board_size
                       ])

            if horizontal_direction:
                return all([self.cells[_row][_col + shift].no_busy for shift in range(ship_size)]) and check_around()
            else:
                return all([self.cells[_row + shift][_col].no_busy for shift in range(ship_size)]) and check_around()

        # -- Find all blank cells on board
        blank_cells = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if col + ship_size <= self.board_size and horizontal_direction:
                    blank_cells.append((row, col)) if check(row, col) else ''
                if row + ship_size <= self.board_size and not horizontal_direction:
                    blank_cells.append((row, col)) if check(row, col) else ''

        return blank_cells

    def add_ship(self, horizontal_direction, ship_size):
        # -- Get all blank cells of board
        blank_cells = self.find_blank_cells(horizontal_direction, ship_size)
        # -- Select random cell set from blank cells
        target_cells = blank_cells[random.randint(0, len(blank_cells)) - 1]
        # -- Fill selected cells with values of state ship part
        for shift in range(ship_size):
            if horizontal_direction:
                self.cells[target_cells[0]][target_cells[1] + shift].state = DOT_STATES[ship_size]
            else:
                self.cells[target_cells[0] + shift][target_cells[1]].state = DOT_STATES[ship_size]


class Game:

    def __init__(self):
        self.board_size = 10  # - width, height
        self.players = (Board(self.board_size), Board(self.board_size))  # - player1 (Human) & player2 (AI) boards

    def __str__(self):
        field = ''
        shift = 3
        for line in range(self.board_size):
            field += ' ' * shift
            for cell in self.players[0].cells[line]:
                field += f'{cell}  '
            field += ' ' * shift * 2
            for cell in self.players[1].cells[line]:
                field += f'{cell}  '
            field += '\n'
        return field

    def place_ships_random(self, player):
        ships = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        for ship_size in ships:
            self.players[player].add_ship(True if random.random() > random.random() else False, ship_size)


def start():
    pass

    game = Game()

    game.place_ships_random(0)
    game.place_ships_random(1)

    print(f'\n{game}')


if __name__ == '__main__':
    start()
