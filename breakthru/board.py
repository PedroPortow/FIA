import random
import sys

# TABULEIRO 
#   0 1 2 3 4 5 6
# 0 



# B => BOT (AI)
# P => PLAYER

# UM MOVIMENTO POR VEZ (OU CAPTURA)

# CAPTURA SÓ NA DIAGONAL!
# ( QUE NEM O PEÃO DO XADREZ )

# SE FLAGSHIP CHEGAR NO OUTERMOST SQUARES, GOLD GANHA
# SE SILVER CAPTURAR O FLAGSHIP, SILVER GANHA

class Board:
  def __init__(self):
    self.board = self.initialize_board()
    self.player = 'G'      
    # self.player = None          
    self.ai = 'S'
    # self.ai = None
    self.turn = 'G'
    # self.turn = self.choose_first_player()  
    # self.choose_each_side()

  def choose_each_side(self):
    self.player = random.choice(['G', 'S'])
    self.ai = 'G' if self.player == 'S' else 'S'
    print(f"Player is '{self.player}', AI is '{self.ai}'")

  def get_gold_player_pieces_symb(self):
     return ('G', 'X')
  
  def choose_first_player(self):
    return random.choice(['G', 'S']);

  def is_player_turn(self):
    return self.turn == self.player
  
  def is_ai_turn(self):
    return self.turn == self.ai
  
  def is_valid_first_press(self, row, col):
    if self.turn == "G" and (self.board[row][col] == "G" or self.board[row][col] == "X"):
      return True
    elif self.turn == "S" and (self.board[row][col] == "S"):
      return True
    
    return False

  def initialize_board(self):
    board = [[None for _ in range(7)] for _ in range(7)]
    
    board[3][3] = 'X' 
    
    for i in range(2, 5):
        for j in range(2, 5):
            if (i == 2 or i == 4) or (j == 2 or j == 4):
                board[i][j] = 'G' 

    for i in range(0, 1): 
          for j in range(2, 5):
              board[i][j] = 'S'
              board[6][j] = 'S'

    for i in range(2, 5):  
          for j in range(0, 1):
              board[i][j] = 'S'
              board[i][6] = 'S'

    return board
  
  def is_valid_play(self, start_row, start_col, play_row, play_col):
    target_play = self.board[play_row][play_col]
    row_diff = abs(play_row - start_row)
    col_diff = abs(play_col - start_col)

    if row_diff > 1 or col_diff > 1: # Movimento 1x1 limitado
        return False

    is_diagonal_play = row_diff == 1 and col_diff == 1 # verificando se é na diagonal

    if target_play is None and not is_diagonal_play: # se n tem nada no taret, e não é na diagonal pode dale
        return True

    if is_diagonal_play:    # aqui tem que verificar se é uma captura
        if self.is_gold_turn() and target_play == "S":  # gold captura S
            return True
        elif self.is_silver_turn() and target_play in self.get_gold_player_pieces_symb(): 
            return True
        return False  # pra não permitir comer a propria peça na diagonal

    # aqui vai cair casos como, movimentar pra um lugar ocupado sem poder comer tipo na reta
    return False

  def is_gold_turn(self):
    return self.turn == "G"

  def is_silver_turn(self):
    return self.turn == "S"

  def make_play(self, start_row, start_col, play_row, play_col):
    self.board[play_row][play_col] = self.board[start_row][start_col]
    self.board[start_row][start_col] = None  
    
  def verify_win(self):
   # WIN DO GOLD PLAYER 
    for i in [0, 6]: 
      for j in range(7):
        if self.board[i][j] == 'X' or self.board[j][i] == 'X':
            print("Gold ganhou! Chegou nos outermost squares")
            return 'G'
    
    # WIN DO SILVER (N TEM FLAGSHIP)
    flagship_found = False
    for row in self.board:
      if 'X' in row:
        flagship_found = True
        break

    if not flagship_found:
      print("Silver wins! (Flagship was captured)")
      return 'S'

    return None
  
  def ai_player_turn(self, max_depth):
    print("Vez do computter")

  
  def minimax(self, depth, is_maximizing, alpha, beta, max_depth):
    pass


  def switch_player(self):
    if self.turn == 'G':
      self.turn = 'S'
    elif self.turn == 'S':
      self.turn = 'G'

  def print_board(self):
      for row in self.board:
          print(' '.join(['-' if cell is None else cell for cell in row]))

board = Board()
