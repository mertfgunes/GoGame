class game_logic:
    def __init__(self, board_size=7):
        # this is temporarily since it is going to be adjustable in the future
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 1  # 1 for black, 2 for white because black goes first.
        self.board_history = []
        self.current_player_history = []

        #score variable to keep track of the game.
        # not sure if it is going to be used.
        self.score_black = 0
        self.score_white = 0

        # prisoner counter
        self.prisoners_black = 0
        self.prisoners_white = 0

    def is_possible_move(self, x, y):
        # cheker for if the position is within bounds and empty
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return False
        if self.board[x][y] != 0:
            return False

        # check the liberties, the next method explains it
        self.board[x][y] = self.current_player
        has_liberty = self.check_liberties(x, y)
        self.board[x][y] = 0  # Undo the simulated move

        return has_liberty

    def check_liberties(self, x, y):
        # checker for the stone or its group has liberties
        visited = set()
        return self._has_liberties(x, y, visited)

    def _has_liberties(self, x, y, visited):
        # basically similiar with the has_liberties
        if (x, y) in visited:
            return False
        visited.add((x, y))

        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return False

        if self.board[x][y] == 0:
            return True

        if self.board[x][y] != self.current_player:
            return False

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return any(self._has_liberties(x + dx, y + dy, visited) for dx, dy in directions)

    def place_stone(self, x, y):
        if not self.is_possible_move(x, y):
            return False  # not possible move
        self.board_history.append([row[:] for row in self.board])
        self.current_player_history.append(self.current_player)
        self.board[x][y] = self.current_player
        self.capture_pieces(x, y)  # check and remove captured pieces
        self.swap_turn() #after each move turn swaps
        return True
    
    def undoLastMove(self):
        if len(self.board_history) > 0:  # Add this check
            print("Undoing last move")  # Add debug print
            self.board = self.board_history.pop()
            self.current_player = self.current_player_history.pop()
            return True
        print("No moves to undo")  # Add debug print
        return False
    
    def swap_turn(self):
        #swap turn
        self.current_player = 3 - self.current_player
        # swaps between 1 and 2
        # if it is first players turn, 3 - 1 = 2 turns into second player.
        #if it is the second player's turn, 3 - 2 = 1 turns into the first player.

    def capture_pieces(self, x, y):
        #capturing logic
        opponent = 3 - self.current_player
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # each direction
        to_capture = []

        def has_liberties(x, y, visited):
            #check for the group for liberties.
            if (x, y) in visited:
                return False
            visited.add((x, y))
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                return False
            if self.board[x][y] == 0:
                return True
            if self.board[x][y] != opponent:
                return False

            return any(has_liberties(x + dx, y + dy, visited) for dx, dy in directions)

        def collect_group(x, y, group):
            #collecting stones in a group
            if (x, y) in group or not (0 <= x < self.board_size and 0 <= y < self.board_size):
                return
            if self.board[x][y] == opponent:
                group.add((x, y))
                for dx, dy in directions:
                    collect_group(x + dx, y + dy, group)

        # checking each directions for opponent
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[nx][ny] == opponent:
                group = set()
                collect_group(nx, ny, group)
                if not has_liberties(nx, ny, set()):
                    to_capture.extend(group)

        #remove the captured prisoner.
        # and update the prisoner count here
        for cx, cy in to_capture:
            self.board[cx][cy] = 0

        if self.current_player == 1:
            self.prisoners_white += len(to_capture)
        else:
            self.prisoners_black += len(to_capture)

    def display_board(self):
        # Display the board in a readable format
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print()  # Add a blank line for better readability

    # Example Usage
# if __name__ == "__main__":
#     game = game_logic()
#     game.display_board()
#     game.place_stone(3, 3)  # Black
#     game.display_board()
#     game.place_stone(3, 4)  # White
#     game.display_board()
#     game.place_stone(2, 4)  # Black
#     game.display_board()
#     game.place_stone(4, 4)  # White
#     game.display_board()
#     game.place_stone(3, 5)  # Black
#     game.display_board()
#     game.place_stone(2, 3)  # White
#     game.display_board()

