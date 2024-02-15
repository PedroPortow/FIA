


# " "|" "|" "         0 1 2 
# ----------          3 4 5  -> 9
# " "|" "|" "         6 7 8
# ----------
# " "|" "|" "

class TicTacToe:
  def __init__(self):
    self.board =  " " * 9
    self.player = "X"
    
  def make_play(self, pos):
    if self.is_valid_play(pos):
      self.board = self.board[:pos] + self.player + self.board[pos+1:]
      self.switch_player()  
    else:
      print("invalid play your dumb af")
  
  def verify_win(self):
      possible_win_combinations = [
            (0, 1, 2),  
            (3, 4, 5), 
            (6, 7, 8),  
            (0, 3, 6),  
            (1, 4, 7),  
            (2, 5, 8), 
            (0, 4, 8),  
            (2, 4, 6)  
      ]
      
      for a, b, c in possible_win_combinations:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]  
        
      if " " not in self.board:
       print("empate q sem graça")
       return "Draw"
        
      return False
  
  def switch_player(self):
    if self.player == "X":
      self.player = "O"
    else:
      self.player = "X"
    
  def is_valid_play(self, pos):
    if pos < 0 or pos > 8:
      print("nem sei oq te dizer...")
      return False
      
    return self.board[pos] == " "

  def print_board(self):
    # print(self.board)
    for i in range(3):
        print(self.board[i*3:(i+1)*3])
        if i < 2:
            print("-" * 5)


jogo = TicTacToe()
jogo.print_board()
jogo.make_play(2)
jogo.print_board()