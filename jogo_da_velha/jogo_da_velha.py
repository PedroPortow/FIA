import random

# " "|" "|" "         0 1 2 
# ----------          3 4 5  -> 9
# " "|" "|" "         6 7 8
# ----------
# " "|" "|" "

# créditos método de verify_win = https://www.reddit.com/r/learnpython/comments/16g1jlc/tictactoe_check_win/
# https://en.wikipedia.org/wiki/alfa%E2%80%93beta_pruning

class TicTacToe:
  def __init__(self):
    self.board =  " " * 9
    self.player = None
    self.ai_player = None
    self.max_depth = 50
    self.turn = None
    
  def make_play(self, pos, player):
    if self.is_valid_play(pos):
      self.board = self.board[:pos] + player + self.board[pos+1:]
      print("movimentouu feito")
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
    if self.turn == "X":
      self.turn = 'O'
    elif self.turn == "O":
      self. turn = "X"
    
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
    valid_plays = self.possible_plays()

    print(valid_plays)
    while choosed_play not in valid_plays:
      try:
          choosed_play = int(input("Sua vez, escolha um número de 0 a 8: "))
          if choosed_play not in valid_plays:
              print("DE 0 A 8")
      except ValueError:
          print("Inserir somente NUMEROS de 0 a 8")

    self.make_play(choosed_play, self.player)
    
  def ai_player_turn(self, max_depth):
    print("Vez do robozão")
    # minmax....

    best_score = -float('inf')
    best_play = None
    
    for play in self.possible_plays(): 
      self.board = self.board[:play] + self.ai_player + self.board[play+1:]
      score = self.minmax(0, False, max_depth)
      self.board = self.board[:play] + ' ' + self.board[play+1:]

      if score > best_score:
        best_score = score
        best_play = play 
    self.make_play(best_play, self.ai_player)

  def minmax_alfa_beta(self, depth, is_maximizing, alfa, beta, max_depth):
       
  # # Poda Alfa: Se, durante a busca, o valor de beta de um nó minimizador se torna menor ou igual ao valor de alfa de algum de seus ancestrais, então esse nó e seus descendentes não precisam ser explorados, pois o maximizador já tem uma opção melhor.
  # # ~Poda Beta: Se, durante a busca, o valor de alfa de um nó maximizador se torna maior ou igual ao valor de beta de algum de seus ancestrais, então esse nó e seus descendentes não precisam ser explorados, pois o minimizador já tem uma opção melhor.
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
        score = self.minmax_alfa_beta(depth + 1, False, alfa, beta, max_depth) # agora minimizar, mandando o alfa e beta
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        max_score = max(score, max_score)
        alfa = max(alfa, score) # maximizando o alfa
        if beta <= alfa: # se já achou um beta men
          break 
      return max_score
    else: 
      min_score = float('inf')

      for play in self.possible_plays(): 
        self.board = self.board[:play] + self.player + self.board[play+1:]
        score = self.minmax_alfa_beta(depth + 1, True, alfa, beta, max_depth) # agora maximizando (eu jogando, como se fosse)
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        min_score = min(score, min_score)
        beta = min(beta, score)
        if beta <= alfa:
          break  
      return min_score

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
        score = self.minmax(depth + 1, False, max_depth) # +1 de profundidade, agora temq ue minimizar
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        max_score = max(score, max_score)
      return max_score
    else: 
      min_score = float('inf')

      for play in self.possible_plays(): 
        self.board = self.board[:play] + self.player + self.board[play+1:]
        score = self.minmax(depth + 1, True, max_depth) # agora maximizando (eu jogando, como se fosse)
        self.board = self.board[:play] + ' ' + self.board[play+1:] # refazendo o movimento pra não ter q ficar criando cópia de tabuleiro...
        min_score = min(score, min_score)
      return min_score
 

  def ai_player_turn_alfa_beta(self, max_depth):
    print("Vez do robozão com poda alfa beta")
    # minmax....

    best_score = -float('inf')
    best_play = None
    alfa = float('-inf')
    beta = float('inf')
    
    for play in self.possible_plays(): 
      self.board = self.board[:play] + self.ai_player + self.board[play+1:]
      score = self.minmax_alfa_beta(0, False, alfa, beta, max_depth)
      self.board = self.board[:play] + ' ' + self.board[play+1:]

      if score > best_score:
        best_score = score
        best_play = play
        alfa = max(alfa, best_score)  #atualzia alfa, beta vai ser usado só dentro do minimax pq ele é pra minimizar
    self.make_play(best_play, self.ai_player)

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

    print("Modo de jogo da IA:")
    print("1- minimax")
    print("2- minimax com poda alfa-beta")
    ia_mode = 0
    while ia_mode not in [1, 2]:
        try:
            ia_mode = int(input("Escolha o modo (1 ou 2): "))
            if ia_mode not in [1, 2]:
                print("Escolhe entre 1 e 2")
        except ValueError:
            print("Tem q ser um numero 1 ou 2")

    while True:
      self.print_board()

      if self.verify_win():
        print("cabo")
        break
      print(f'vez do {self.turn}')
      if self.turn == self.player:
        self.player_turn()
        self.switch_player()
      else:
        if ia_mode == 1:
          self.ai_player_turn(1000)
          self.switch_player()
        elif ia_mode == 2:
          self.ai_player_turn_alfa_beta(1000)
          self.switch_player()

jogo = TicTacToe()
jogo.game_loop()