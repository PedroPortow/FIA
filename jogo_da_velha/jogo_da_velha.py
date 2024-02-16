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
    

  def minmax(self, depth, is_maximizing, max_depth):
    if self.verify_win() == self.player: # eu ganhei, -1 pra ai
      return -1
    elif self.verify_win() == self.ai_player: #parabens robozao
      return +1
    elif self.verify_win() == "DRAW" or depth == max_depth: #aqui ou emaptou ou chegou na altura maxima
      return 0 
    
    if is_maximizing:
      max_score = -float('inf')

      for play in self.possible_plays(): 
        self.board = self.board[:play] + self.ai_player + self.board[play+1:]
        score = self.minimax(depth + 1, False, max_depth) # +1 de profundidade, agora temq ue minimizar
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        max_score = max(score, max_score)
      return max_score
    else: 
      min_score = float('inf')

      for play in self.possible_plays(): 
        self.board = self.board[:play] + self.player + self.board[play+1:]
        score = self.minimax(depth + 1, True, max_depth) # agora maximizando (eu jogando, como se fosse)
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        min_score = min(score, min_score)
      return min_score

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