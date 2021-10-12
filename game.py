# --- SeaBattle game for practical work on SkillFactory FPW-2.0 course
# --- Evgeniy Ivanov, flow FPW-42, Okt'2021

import random


class CellBusy(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotValidState(Exception):
    def __init__(self, message):
        super().__init__(message)


class OutOfBoard(Exception):
    def __init__(self, message):
        super().__init__(message)


class Cell:

    DOT_STATES = (
        '-',  # - sea wave (start cell state)
        '#',  # - ship part
        'H',  # - hit strike
        'M',  # - miss strike
    )

    def __init__(self):
        self._state = self.DOT_STATES[0]
        pass

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        if value in self.DOT_STATES:
            if self._state != self.DOT_STATES[0] and value != self.DOT_STATES[0]:
                raise CellBusy(f'Cell already busy')
            else:
                self._state = value
        else:
            raise NotValidState(f'State {value} not valid')

    def __str__(self):
        return self._state


class Board:

    def __init__(self, board_size):
        self._board_size = board_size  # - width, height
        self._cells = [[Cell() for i in range(self._board_size[0])] for i in range(self._board_size[1])]

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        if not (0 <= value['top'] < self._board_size[0] and 0 <= value['left'] < self._board_size[1]):
            raise OutOfBoard('Out off board')
        else:
            self._cells[value['top']][value['left']].state = value['state']

    def add_ship(self, horizontal, top, left, ship_size):
        try:
            for i in range(ship_size):
                if horizontal:
                    self.cells = {'top': top, 'left': left + i, 'state': Cell.DOT_STATES[1]}
                else:
                    self.cells = {'top': top + i, 'left': left, 'state': Cell.DOT_STATES[1]}
        except CellBusy:
            for i in range(ship_size):
                if horizontal:
                    self.cells = {'top': top, 'left': left + i, 'state': Cell.DOT_STATES[0]}
                else:
                    self.cells = {'top': top + i, 'left': left, 'state': Cell.DOT_STATES[0]}
            return False

        return True


class Game:

    def __init__(self, board_size):
        self.board_size = board_size  # - width, height
        self.players = (Board(self.board_size), Board(self.board_size))  # - player1 (Human) board, player2 (AI) board

    def __str__(self):
        field = ''
        for row in range(self.board_size[0]):
            for cell in self.players[0].cells[row]:
                field += f'{cell} '
            field += ' '*3
            for cell in self.players[1].cells[row]:
                field += f'{cell} '
            field += '\n'
        return field


def start():

    game = Game((6, 6))
    size, count = 3, 2
    for player in range(2):
        c = count
        y = random.randint(0, game.board_size[0] - 1)
        x = random.randint(0, game.board_size[1] - size)
        while c > 0:
            try:
                #r = game.players[player].add_ship(bool(random.randint(0, 2)), y, x, size)
                r = game.players[player].add_ship(True, y, x, size)
            except OutOfBoard:
                y = random.randint(0, game.board_size[0] - 1)
                x = random.randint(0, game.board_size[1] - size)
            if r:
                y = random.randint(0, game.board_size[0] - 1)
                x = random.randint(0, game.board_size[1] - size)
                print(c, y, x, size)
                c -= 1

    print(f'\n{game}')


if __name__ == '__main__':
    start()
