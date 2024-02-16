import random

# " "|" "|" "         0 1 2 
# ----------          3 4 5  -> 9
# " "|" "|" "         6 7 8
# ----------
# " "|" "|" "

# créditos método de verify_win = https://www.reddit.com/r/learnpython/comments/16g1jlc/tictactoe_check_win/

class TicTacToe:
  def __init__(self):
    self.board =  " " * 9
    self.player = None
    self.ai_player = None
    self.max_depth = 50
    self.turn = None
    
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
          return self.board[a]  # RETORNA O GANHADOR
        
      if " " not in self.board:
        return "DRAW" 
        
      return None # ninguem ganhou nem emaptou
  
  def switch_player(self):
    self.turn = "X" if self.turn == "O" else "X"
    
  def is_valid_play(self, pos):
    if pos < 0 or pos > 8:
      print("nem sei oq te dizer...")
      return False
      
    return self.board[pos] == " "
  
  def possible_plays(self):
    possible_plays = []
    for i in range(len(self.board)):
      if self.board[i] == " ":
        possible_plays.append(i)
    return possible_plays
    
  def print_board(self):
    print("   ")
    for i in range(3):
        print("|".join(self.board[i * 3:(i + 1) * 3]))
        if i < 2:
            print("-" * 5)
    print("   ")

  def decide_inicial_player(self):
    return random.choice(["X", "O"])
  
  def player_turn(self):
    choosed_play = None

    while choosed_play not in self.possible_plays():
      choosed_play = int(input("Sua vez, escolha um numero de 0 a 8: "))
    self.make_play(choosed_play)
    
  def ai_player_turn(self):
    print("Vez do robozão")
    # minmax....

  def game_loop(self):
    print("== Jogo inciando ==");
    while self.player not in ["O", "X"]:
      self.player = input("escolha seu jogador (X ou O): ").upper()
      if self.player not in ["O", "X"]:
          print("por favor escolhe X ou O né.")
      else: self.ai_player = "X" if self.player == "O" else "O"
    
    print("Agora vamos decidir quem incia, tá nas mãos de deus")
    self.turn = self.decide_inicial_player()
    print(f'Jogador {self.turn} que começa')

    while self.verify_win() != None:
      if self.turn == self.player:
        self.player_turn()
      else:
        self.ai_player_turn()

jogo = TicTacToe()
jogo.game_loop()