import random
import sys

# TABULEIRO 
# 0 1 2 3 4 5 6 7 8 9 10 
# 0 N N N N N N N N N N N
# 1 N N N P P P P P N N N
# 2 N N N N N N N N N N N
# 3 N P N N G G G N N P N
# 4 N P N G N N N G N P N
# 5 N P N G N X N G N P N
# 6 N P N G N N N G N P N
# 7 N P N N G G G N N P N
# 8 N N N N N N N N N N N
# 9 N N N P P P P P N N N
# 10 N N N N N N N N N N N

# B => BOT (AI)
# P => PLAYER
class Board:
  def __init__(self):
    self.board = self.initialize_board()
    self.player = None          
    self.ai = None
    self.turn = self.choose_first_player()  
    self.choose_each_side()

  def choose_each_side(self):
    self.player = random.choice(['G', 'S'])
    self.ai = 'G' if self.player == 'S' else 'S'
    print(f"Player is '{self.player}', AI is '{self.ai}'")

  def choose_first_player(self):
    return random.choice(['G', 'S']);

  def is_player_turn(self):
    return self.turn == self.player
    
  def initialize_board(self):
    board = [[None for _ in range(11)] for _ in range(11)]
    
    center = 5  #
    board[center][center] = 'X' # => X = NAVIO PRINCIPAL
    
    for i in range(3, 8):
        for j in range(3, 8):
            if (i == 3 or i == 7) or (j == 3 or j == 7):
                board[i][j] = 'G' # => X = ESCORTAS

    # to-do: arrumar essa coisa feia
    for i in range(1, 2):  # Linha X com navios prateados
          for j in range(3, 8):
              board[i][j] = 'S'

    for i in range(9, 10):  # Linha X com navios Srateados
          for j in range(3, 8):
              board[i][j] = 'S'

    for i in range(3, 8):  # Linha Y com navios Srateados
          for j in range(1, 2):
              board[i][j] = 'S'

    for i in range(3, 8):  # Linha Y com navios Srateados
          for j in range(9, 10):
              board[i][j] = 'S'

    return board
  
  def print_board(self):
      for row in self.board:
          print(' '.join(['-' if cell is None else cell for cell in row]))
   

board = Board()
board.print_board()
print(board.turn)