import random
import time

class Board:
  def __init__(self):
    self.board = self.initialize_board()
    self.on_ai_turn_finished = None 
    
    self.player_1 = None     
    self.ai_player = None
    self.turn = self.choose_first_player()
    self.nodes_evaluated = 0

    self.heuristic_weights = {
      'close_to_edge': 100,
      'silvers_near_flagship': 120,
      'gold_pieces_near_flagship': 50,  
      'capturable_pieces': 50,
      'captured_pieces': 60,
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
  
  def is_gold_turn(self):
    return self.turn == "G"

  def is_silver_turn(self):
    return self.turn == "S"
  
  def make_play(self, start_row, start_col, play_row, play_col):  
    captured_piece = self.board[play_row][play_col]  
    self.board[play_row][play_col] = self.board[start_row][start_col]  
    self.board[start_row][start_col] = None  
    
    return captured_piece  
  
  def undo_play(self, start_row, start_col, play_row, play_col, captured_piece):
    self.board[play_row][play_col] = self.board[start_row][start_col]
    self.board[start_row][start_col] = captured_piece
  
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

    return False   # aqui vai cair casos como, movimentar pra um lugar ocupado tipo na reta ou horizontal


  def verify_win(self):
    for i in [0, 6]:   
      for j in range(7):
        if self.board[i][j] == 'X' or self.board[j][i] == 'X':
            print("Gold ganhou!")
            return 'G'
    
    flagship_found = False    
    for row in self.board:
      if 'X' in row:
        flagship_found = True
        break

    if not flagship_found:
      print("Silver ganhou!")
      return 'S'

    return None
  
  def ai_player_turn(self):
    start_time = time.time()  
    
    self.nodes_evaluated = 0
    max_depth = 4

    best_score = float('-inf')
    best_play = None

    possible_plays = self.gold_player_possible_plays() if self.ai_player == 'G' else self.silver_player_possible_plays()
    
    for play in possible_plays: 
      
      captured_piece = self.make_play(*play[0], *play[1]) 
      score = self.minimax(depth=0, is_maximizing=True, alpha=float('-inf'), beta=float('inf'), max_depth=max_depth)
      self.undo_play(*play[1], *play[0], captured_piece)

      if score > best_score:
          best_score = score
          best_play = play
    if best_play:
        self.make_play(*best_play[0], *best_play[1])
        self.switch_player()  

        end_time = time.time()  
        elapsed_time = end_time - start_time

        print(f"IA levou {elapsed_time} segundos para jogar.")
        print(f"Nós avaliados: {self.nodes_evaluated}")

        if self.on_ai_turn_finished: 
          self.on_ai_turn_finished(elapsed_time, self.nodes_evaluated) 

  def get_flasgship_pos(self):
    return [(r, c) for r, row in enumerate(self.board) for c, val in enumerate(row) if val == 'X'][0]
  
  def get_flagship_distance_from_edge(self, flagship_pos):
    return (6 - min(flagship_pos[0], 6-flagship_pos[0], flagship_pos[1], 6-flagship_pos[1])) 
  
  def silvers_pieces_near_flagship(self, flagship_pos):
    silvers_near_flagship = 0

    for row, col in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if 0 <= flagship_pos[0]+row < 7 and 0 <= flagship_pos[1]+col < 7:
            if self.board[flagship_pos[0]+row][flagship_pos[1]+col] == 'S':
                silvers_near_flagship += 1
    return silvers_near_flagship
  
  def gold_pieces_near_flagship(self, flagship_pos):            
    gold_pieces_near_flagship = 0

    for row, col in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if 0 <= flagship_pos[0]+row < 7 and 0 <= flagship_pos[1]+col < 7:
            if self.board[flagship_pos[0]+row][flagship_pos[1]+col] == 'G':
                gold_pieces_near_flagship += 1
    return gold_pieces_near_flagship
  
  def captured_pieces(self):  # Retorna quantas peças do inimigo foram capturadas
    total_gold_pieces = 0
    total_silver_pieces = 0

    for row in self.board:
        for cell in row:
            if cell == 'G' or cell == 'X':  
                total_gold_pieces += 1
            elif cell == 'S':
                total_silver_pieces += 1

    golds_captured = 9 - total_gold_pieces
    silvers_captured = 12 - total_silver_pieces

    if self.ai_player == 'G':
        return silvers_captured 
    elif self.ai_player == 'S':
        return golds_captured

  def capturable_pieces(self):  # Retorna quantas peças do inimigo podem ser capturadas
    capturable_pieces_count = 0
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Direções diagonais 

    for row in range(len(self.board)):
        for col in range(len(self.board[row])):
            current_piece = self.board[row][col]

            if self.ai_player == "G" and current_piece in self.get_gold_player_pieces_symb(): 
                for diagonal_row, diagonal_col in directions:
                    check_row, check_col = row + diagonal_row, col + diagonal_col

                    if 0 <= check_row < 7 and 0 <= check_col < 7: 
                        target_piece = self.board[check_row][check_col] 

                        if target_piece == "S":  
                            capturable_pieces_count += 1

            elif self.ai_player == "S" and current_piece == "S":
                for diagonal_row, diagonal_col in directions:
                    check_row, check_col = row + diagonal_row, col + diagonal_col

                    if 0 <= check_row < 7 and 0 <= check_col < 7:  
                        target_piece = self.board[check_row][check_col]

                        if target_piece in self.get_gold_player_pieces_symb(): 
                            capturable_pieces_count += 1 

    return capturable_pieces_count
  
  def heuristic_evaluation(self):
    flagship_pos = self.get_flasgship_pos()

    flagship_dist_edge = self.get_flagship_distance_from_edge(flagship_pos) * self.heuristic_weights['close_to_edge'] # Distância flagship pro edge do tabuleiro

    silver_near_flagship = self.silvers_pieces_near_flagship(flagship_pos) * self.heuristic_weights['silvers_near_flagship'] # Silvers perto do flagship (1 casa em todas as dir)
    
    gold_protection = self.gold_pieces_near_flagship(flagship_pos) * self.heuristic_weights['gold_pieces_near_flagship'] # Golds perto do flahship (1 cada em todas dir)

    capturable_pieces = self.capturable_pieces() * self.heuristic_weights['capturable_pieces'] # Retorna peças capturable pelo jogador atual (G ou S)
    
    captured_pieces = self.captured_pieces() * self.heuristic_weights['captured_pieces']  # Retorna peças capturadas pelo jogador atual (G ou S)


    if self.ai_player == 'G':  
        return (flagship_dist_edge - silver_near_flagship + gold_protection + capturable_pieces + captured_pieces) 
    elif self.ai_player == 'S': 
        return (silver_near_flagship - flagship_dist_edge - gold_protection + capturable_pieces + captured_pieces)

  def evaluate_board(self, result):
      if result == self.player_1: 
        return -9999
      elif result == self.ai_player: 
        return 9999
      else:  
        return self.heuristic_evaluation()

  def minimax(self, depth, is_maximizing, alpha, beta, max_depth = 4):
    self.nodes_evaluated += 1
    result = self.verify_win() 

    if result is not None or depth == max_depth:  
      return self.evaluate_board(result)
      
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
