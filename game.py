# --- SeaBattle game for practical work on SkillFactory FPW-2.0 course
# --- Evgeniy Ivanov, flow FPW-42, Okt'2021
import random
import time


class BoardException(Exception):
    def __init__(self, message):
        super().__init__(message)


class OutOfBoardException(BoardException):
    def __init__(self, message='Out of board'):
        super().__init__(message)


class CollisionOnBoardException(BoardException):
    def __init__(self, message='Collision on board'):
        super().__init__(message)


class Dot:

    DOT_STATES = {
        'hit': '*',
        'miss': 'M',
        'dead': 'X',
        'blank': '_'
    }

    def __init__(self, row=0, col=0, state=DOT_STATES['blank']):
        self.row = row
        self.col = col
        self.state = state

    @property
    def visible(self):
        return False if self.state in ['4', '3', '2', '1'] else True
        # return True if self.state in ['4', '3', '2', '1'] else True

    def __eq__(self, other):
        return True if self.row == other.row and self.col == other.col else False

    def __repr__(self):
        return str((self.row, self.col))

    def __str__(self):
        return self.state


class Ship:

    def __init__(self, ship_size: int, horizontal=True):
        self.ship_size = ship_size
        self.lives = ship_size
        self.horizontal = horizontal
        self.dots = []
        self.set_position(0, 0)

    def __repr__(self):
        return str([dot.state for dot in self.dots])

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
        self.ships = [Ship(ship_size, Board.random_direction()) for ship_size in self.ships_types]
        self.lives = len(self.ships)
        self.random_set_ships()

    def random_set_ships(self):
        for ship in self.ships:
            while True:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                try:
                    self.move_ship(ship, row, col)
                except BoardException:
                    continue
                else:
                    break

    def move_ship(self, ship: Ship, row: int, col: int):
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
                    if not self.cells[_row][_col].state == Dot.DOT_STATES['blank']:
                        return True
            return False
        # ---
        if row + ship.ship_size > self.board_size or col + ship.ship_size > self.board_size:
            raise OutOfBoardException
        else:
            if collision():
                raise CollisionOnBoardException
            else:
                ship.set_position(row, col)
                for dot in ship.dots:
                    self.cells[dot.row][dot.col] = dot


class Game:
    def __init__(self):
        self.board_size = 10
        self.players = (
            Board(self.board_size), # - Human board
            Board(self.board_size)  # - AI board
        )

    def __str__(self):
        top_panel = f'{" " * 10}PLAYER SHIPS {self.players[0].lives}{" " * 26}TARGET SHIPS {self.players[1].lives}\n'
        field = '|0||1||2||3||4||5||6||7||8||9|'
        field = f'{" " * 3}{field}{" " * 10}{field}\n'
        for line in range(self.board_size):
            # --- human board ---
            field += f'|{line}| '
            for cell in self.players[0].cells[line]:
                field += f'{cell}  '
            # --- AI board ---
            field += ' ' * 6 + f'|{line}| '
            for cell in self.players[1].cells[line]:
                field += f'{cell if cell.visible else Dot.DOT_STATES["blank"]}  '
            field += '\n'
        return top_panel + field

    def ai_strike(self):
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        self.strike(0, row, col)

    def human_strike(self, row: int, col: int):
        self.strike(1, row, col)

    def strike(self, player: int, row: int, col: int):
        target = Dot(row, col)
        for ship in self.players[player].ships:
            for dot in ship.dots:
                if dot == target:
                    if dot.state in [Dot.DOT_STATES['hit'], Dot.DOT_STATES['dead']]:
                        return
                    dot.state = Dot.DOT_STATES['hit']
                    if ship.lives > 0:
                        ship.lives -= 1
                    if ship.lives == 0 and self.players[player].lives > 0:
                        self.players[player].lives -= 1
                        for _dot in ship.dots:
                            _dot.state = Dot.DOT_STATES['dead']
                    return
        # ---
        self.players[player].cells[row][col].state = Dot.DOT_STATES['miss'] if player == 1 else Dot.DOT_STATES['blank']

    def check_win(self, player: int) -> bool:
        return False if any([ship.lives for ship in self.players[player].ships]) else True


def start():

    def test_game(count):
        for i in range(count):
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            game.human_strike(row, col)
            if game.check_win(1):
                print('Human win!!!')
                return
            game.ai_strike()
            if game.check_win(0):
                print('AI win!!!')
                return

    msg1 = f'Type row, col (like 12, 65, etc.) or type q - to exit game: '

    game = Game()
    print(game)

    game_test = False
    # game_test = True

    if game_test:
        test_game(500)
        print(game)
    else:
        while True:
            rc = input(msg1)
            print()
            if not rc[:2].isdigit():
                if rc[0] == 'q':
                    break
                else:
                    continue
            else:
                game.human_strike(int(rc[0]), int(rc[1]))
                print(game)
                if game.check_win(1):
                    print('Human win!!!')
                    return

                print('AI...')
                time.sleep(1)
                game.ai_strike()
                print(game)
                if game.check_win(0):
                    print('AI win!!!')
                    return


if __name__ == '__main__':
    start()
