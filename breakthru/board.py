import random

class Board:
  def __init__(self):
    self.board = self.initialize_board()
    self.on_ai_turn_finished = None 
    
    self.player_1 = None     
    self.ai_player = None
    self.turn = self.choose_first_player()
    self.nodes_evaluated = 0
    self.heuristic_weights = {
      'close_to_edge': 10,
      'silvers_near_flagship': 15
    }

    self.choose_each_side()
  def choose_each_side(self):
    self.player_1 = random.choice(['G', 'S'])
    self.ai_player = 'G' if self.player_1 == 'S' else 'S'

  def choose_first_player(self):
    return random.choice(['G', 'S']);

  def get_gold_player_pieces_symb(self):
     return ["G", "X"]

  def is_player_turn(self):
    return self.turn == self.player_1
  
  def is_ai_turn(self):
    return self.turn == self.ai_player
  
  def is_valid_first_press(self, row, col):
    self.print_board()
    if self.turn == "G" and self.board[row][col] in self.get_gold_player_pieces_symb():
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
  
  def is_game_over(self):
    for i in [0, 6]:    # Vitória do GOLD
      for j in range(7): 
        if self.board[i][j] == 'X' or self.board[j][i] == 'X':
            print("Gold ganhou! Chegou nos outermost squares")
            return
        
    flagship_found = False    # WIN SILVER (N TEM FLAGSHIP)
    for row in self.board:
      if 'X' in row:
        flagship_found = True
        break

    if not flagship_found:
      print("Silver wins! (Flagship was captured)")
      return 'S'
  
  def is_valid_play(self, start_row, start_col, play_row, play_col):
    target_piece = self.board[play_row][play_col]
    row_diff = abs(play_row - start_row)
    col_diff = abs(play_col - start_col)

    if row_diff > 1 or col_diff > 1: # Movimento 1x1 limitado
        return False

    is_diagonal_play = row_diff == 1 and col_diff == 1 # Verificando se é na diagonal

    if target_piece is None and not is_diagonal_play: # Movimento pra espaço vazio X Y sem captura
        return True

    if is_diagonal_play:   # Precisa ser captura
        if self.is_gold_turn() and target_piece == "S":  # Captura do GOLD
            return True
        elif self.is_silver_turn() and target_piece in self.get_gold_player_pieces_symb():  # Captura do SILVER
            return True
        return False  # Não permite movimento diagonal sem ser de captura

    return False   # aqui vai cair casos como, movimentar pra um lugar ocupado sem poder comer tipo na reta

  def is_gold_turn(self):
    return self.turn == "G"

  def is_silver_turn(self):
    return self.turn == "S"

  def make_play(self, start_row, start_col, play_row, play_col):  
    captured_piece = self.board[play_row][play_col]  
    self.board[play_row][play_col] = self.board[start_row][start_col]  
    self.board[start_row][start_col] = None  
    return captured_piece  

  def verify_win(self):
    for i in [0, 6]:  # WIN GOLD     
      for j in range(7):
        if self.board[i][j] == 'X' or self.board[j][i] == 'X':
            print("Gold ganhou! Chegou nos outermost squares")
            return 'G'
    
    flagship_found = False    # WIN SILVER (N TEM FLAGSHIP)
    for row in self.board:
      if 'X' in row:
        flagship_found = True
        break

    if not flagship_found:
      print("Silver wins! (Flagship was captured)")
      return 'S'

    return None # Não foi vitória de ninguem
  
  def ai_player_turn(self):
    max_depth = 3

    best_score = float('-inf')
    best_play = None

    possible_plays = self.gold_player_possible_plays() if self.ai_player == 'G' else self.silver_player_possible_plays()
                                              # X     Y                        # X  Y
    for play in possible_plays: # PLAY => ( (POSIÇÃO ATUAL DA PEÇA)  ,  (NOVA POSIÇÃO DA PLAY)  )
      self.print_board()
      
      captured_piece = self.make_play(*play[0], *play[1]) 
      print(f"Peça capturada -> {captured_piece}")
      print(f"Board após a captura")
      self.print_board()

      score = self.minimax(depth=0, is_maximizing=True, alpha=float('-inf'), beta=float('inf'), max_depth=max_depth)
      self.undo_play(*play[1], *play[0], captured_piece)

      if score > best_score:
          best_score = score
          best_play = play
    if best_play:
        self.make_play(*best_play[0], *best_play[1])
        self.switch_player()  
        if self.on_ai_turn_finished:  # Verifica se o callback foi definido
          self.on_ai_turn_finished() 

  def get_flasgship_pos(self):
    return [(r, c) for r, row in enumerate(self.board) for c, val in enumerate(row) if val == 'X'][0]
  
  def get_flagship_distance_from_edge(self, flagship_pos):
    return min(flagship_pos[0], 6-flagship_pos[0], flagship_pos[1], 6-flagship_pos[1])
  
  def silvers_pieces_near_flagship(self, flagship_pos):
    silvers_near_flagship = 0

    for row, col in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if 0 <= flagship_pos[0]+row < 7 and 0 <= flagship_pos[1]+col < 7:
            if self.board[flagship_pos[0]+row][flagship_pos[1]+col] == 'S':
                silvers_near_flagship += 1
    return silvers_near_flagship

  def heuristic_evaluation(self): # Definindo pesos pra cada heurística, pra poder alterar o quão o resultado de uma heurística é "importante"
    flagship_pos = self.get_flasgship_pos()
    gold_evaluation = (7 - self.get_flagship_distance_from_edge(flagship_pos)) * self.heuristic_weights['close_to_edge'] # 10
    silver_evaluation = self.silvers_pieces_near_flagship(flagship_pos) * self.heuristic_weights['silvers_near_flagship']  #15
    
    if self.ai_player == 'G': # se AI é G
        return gold_evaluation - silver_evaluation
    elif self.ai_player == 'S': # se AI É S
        return silver_evaluation - gold_evaluation

  def evaluate_board(self, result, depth):
      if result == self.player_1: 
        return -1000 + depth
      elif result == self.ai_player: 
        return 1000 - depth
      else:  
        return self.heuristic_evaluation()

  def minimax(self, depth, is_maximizing, alpha, beta, max_depth = 10000):
    result = self.verify_win() 

    if result is not None or depth == max_depth:  # Se chegou em um estado de vitória ou chegou no limite de depth sem acabar o jogo
      return self.evaluate_board(result, depth)
      
    if is_maximizing:
      max_score = float('-inf')
      possible_plays = self.gold_player_possible_plays() if self.ai_player == 'G' else self.silver_player_possible_plays()
      
      for play in possible_plays:
        captured_piece = self.make_play(*play[0], *play[1])
        score = self.minimax(depth + 1, False, alpha, beta, max_depth)
        self.undo_play(*play[1], *play[0], captured_piece)

        max_score = max(max_score, score)
        alpha = max(alpha, score)

        if beta <= alpha:
            break
      return max_score
    else:
        min_score = float('inf')
        possible_plays = self.silver_player_possible_plays() if self.ai_player == 'G' else self.gold_player_possible_plays()
        
        for play in possible_plays:
            captured_piece = self.make_play(*play[0], *play[1])
            score = self.minimax(depth + 1, True, alpha, beta, max_depth)
            self.undo_play(*play[1], *play[0], captured_piece)

            min_score = min(min_score, score)
            beta = min(beta, score)

            if beta <= alpha:
                break
        return min_score
    
  def undo_play(self, start_row, start_col, play_row, play_col, captured_piece):
    self.board[play_row][play_col] = self.board[start_row][start_col]
    self.board[start_row][start_col] = captured_piece
 
  def gold_player_possible_plays(self):
    possible_plays = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]  #

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] in self.get_gold_player_pieces_symb():  # G e
          for direction in directions:
            target_row, target_col = row + direction[0], col + direction[1]

            if 0 <= target_row < len(self.board) and 0 <= target_col < len(self.board[0]):  # dentro do tabuleiro
              target_piece = self.board[target_row][target_col]

              if abs(direction[0]) == 1 and abs(direction[1]) == 1 and target_piece == 'S':  # diagonal precisa ser captura
                  possible_plays.append(((row, col), (target_row, target_col)))

              elif target_piece is None and not (abs(direction[0]) == 1 and abs(direction[1]) == 1): # ta certo isso? era pra mover pra um espaco vazio
                  possible_plays.append(((row, col), (target_row, target_col)))

    return possible_plays


  def silver_player_possible_plays(self):
    possible_plays = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]  

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == 'S':  # passa iterando pelas peças até achar uma silver
          for direction in directions:
            target_row, target_col = row + direction[0], col + direction[1]

            if 0 <= target_row < len(self.board) and 0 <= target_col < len(self.board[0]): # dentro do tabuleiro
                target_piece = self.board[target_row][target_col]

                if abs(direction[0]) == 1 and abs(direction[1]) == 1: # se for na diagonal, tem que capturar
                    if target_piece in self.get_gold_player_pieces_symb():  
                        possible_plays.append(((row, col), (target_row, target_col)))
                elif target_piece is None:    # movimento vertical/hor pra espaço vazio
                    possible_plays.append(((row, col), (target_row, target_col)))

    return possible_plays #vai ser um ((pos1, pos2), (targetpos1, targetpos2)) 
  
  def switch_player(self):
    print('SWITANDO PLAYER! ! !')
    if self.turn == 'G':
      self.turn = 'S'
    elif self.turn == 'S':
      self.turn = 'G'

  def print_board(self):
      for row in self.board:
          print(' '.join(['-' if cell is None else cell for cell in row]))
      print("")
      print("")
      print("")

board = Board()
