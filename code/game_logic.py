class GoGame:
    def __init__(self, board_size=7):
        # this is temporarily since it is going to be adjustable in the future
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 1  # 1 for black, 2 for white because black goes first.

