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

# class Cell:
#
#     DOT_STATES = (
#         '-',  # - sea wave (start cell state)
#         '#',  # - ship part
#         'H',  # - hit strike
#         'M',  # - miss strike
#     )
#
#     def __init__(self):
#         self._state = self.DOT_STATES[0]
#         pass
#
#     @property
#     def state(self):
#         return self._state
#
#     @state.setter
#     def state(self, value: str):
#         if value in self.DOT_STATES:
#             if self._state != self.DOT_STATES[0] and value != self.DOT_STATES[0]:
#                 raise CellBusy(f'Cell already busy')
#             else:
#                 self._state = value
#         else:
#             raise NotValidState(f'State {value} not valid')
#
#     def __str__(self):
#         return self._state
#
#
# class Board:
#
#     def __init__(self, board_size):
#         self._board_size = board_size  # - width, height
#         self._cells = [[Cell() for i in range(self._board_size[0])] for i in range(self._board_size[1])]
#
#     @property
#     def cells(self):
#         return self._cells
#
#     @cells.setter
#     def cells(self, value):
#         if not (0 <= value['top'] < self._board_size[0] and 0 <= value['left'] < self._board_size[1]):
#             raise OutOfBoard('Out off board')
#         else:
#             self._cells[value['top']][value['left']].state = value['state']
#
#     def add_ship(self, horizontal, top, left, ship_size):
#         try:
#             for i in range(ship_size):
#                 if horizontal:
#                     self.cells = {'top': top, 'left': left + i, 'state': Cell.DOT_STATES[1]}
#                 else:
#                     self.cells = {'top': top + i, 'left': left, 'state': Cell.DOT_STATES[1]}
#         except CellBusy:
#             for i in range(ship_size):
#                 if horizontal:
#                     self.cells = {'top': top, 'left': left + i, 'state': Cell.DOT_STATES[0]}
#                 else:
#                     self.cells = {'top': top + i, 'left': left, 'state': Cell.DOT_STATES[0]}
#             return False
#
#         return True
#


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

    def __init__(self, board_size):
        self.board_size = board_size  # - width, height
        self.cells = [[Cell(DOT_STATES['blank']) for cell in range(self.board_size)] for cell in range(self.board_size)]

    def find_blank_cells(self, horizontal_direction, ship_size):

        def is_busy(_row, _col):
            if horizontal_direction:
                return all([self.cells[_row][_col + shift].no_busy for shift in range(ship_size)])
            else:
                return all([self.cells[_row + shift][_col].no_busy for shift in range(ship_size)])

        blank_cells = []

        if horizontal_direction:
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if col + ship_size <= self.board_size:
                        if is_busy(row, col):
                            blank_cells.append((row, col))
        else:
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if row + ship_size <= self.board_size:
                        if is_busy(row, col):
                            blank_cells.append((row, col))

        return blank_cells

    def add_ship(self, horizontal_direction, ship_size):
        blank_cells = self.find_blank_cells(horizontal_direction, ship_size)
        target_cell = blank_cells[random.randint(0, len(blank_cells)) - 1]

        if horizontal_direction:
            for shift in range(ship_size):
                self.cells[target_cell[0]][target_cell[1] + shift].state = DOT_STATES[ship_size]
        else:
            for shift in range(ship_size):
                self.cells[target_cell[0] + shift][target_cell[1]].state = DOT_STATES[ship_size]


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
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for ship_size in ships:
            self.players[player].add_ship(True if random.random() > 0.86 else False, ship_size)


def start():
    pass

    game = Game()
    # size, count = 3, 2
    # for player in range(2):
    #     c = count
    #     y = random.randint(0, game.board_size[0] - 1)
    #     x = random.randint(0, game.board_size[1] - size)
    #     while c > 0:
    #         try:
    #             #r = game.players[player].add_ship(bool(random.randint(0, 2)), y, x, size)
    #             r = game.players[player].add_ship(True, y, x, size)
    #         except OutOfBoard:
    #             y = random.randint(0, game.board_size[0] - 1)
    #             x = random.randint(0, game.board_size[1] - size)
    #         if r:
    #             y = random.randint(0, game.board_size[0] - 1)
    #             x = random.randint(0, game.board_size[1] - size)
    #             print(c, y, x, size)
    #             c -= 1
    #
    # print(f'\n{game}')
    # print(game.players[0].find_blank_cells(False, 4))
    # game.players[0].add_ship(False, 4)

    game.place_ships_random(0)
    game.place_ships_random(1)

    print(f'\n{game}')


if __name__ == '__main__':
    start()
