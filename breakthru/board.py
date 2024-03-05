import random

class Board:
  def __init__(self):
    self.board = self.initialize_board()

    # QUANDO FOR PLAYER VS IA, ESSE É O PLAYER
    self.player_1 = 'G'    

    # SEMPRE VAI SER IA
    self.player_2 = 'S'

    self.turn = 'G'
    self.mode = None
    self.nodes_evaluated = 0
    self.heuristic_weights = {
      'close_to_edge': 10,
      'silvers_near_flagship': 15
    }

  def choose_each_side(self):
    self.player_1 = random.choice(['G', 'S'])
    self.player_2 = 'G' if self.player_1 == 'S' else 'S'
    print(f"Player 1 is '{self.player_1}', AI is '{self.player_2}'")

  def get_gold_player_pieces_symb(self):
     return ('G', 'X')
  
  def choose_first_player(self):
    return random.choice(['G', 'S']);

  def is_player_turn(self):
    return self.turn == self.player_1
  
  def is_ai_turn(self):
    return self.turn == self.player_2
  
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
    captured_piece = self.board[play_row][play_col]  
    self.board[play_row][play_col] = self.board[start_row][start_col]  
    self.board[start_row][start_col] = None  
    return captured_piece  # vai retornar o peça capturada, se tiver uma né pode ser nonee

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
  
  def player_2_turn(self):
    max_depth = 3 # profundiade maxima

    best_score = float('-inf')
    best_play = None

    possible_plays = self.gold_player_possible_plays() if self.player_2 == 'G' else self.silver_player_possible_plays()

                  # X    Y                        # X  Y
    # PLAY => ( (POSIÇÃO ATUAL DA PEÇA)  ,  (NOVA POSIÇÃO DA PLAY)  )
    for play in possible_plays:
      print("---")
      print(play)
      print("---")
      self.print_board()
      captured_piece = self.make_play(*play[0], *play[1])  # faz a jogaoda e retorna a peça
      print(captured_piece)
      self.print_board()
      score = self.minimax(depth=0, is_maximizing=True, alpha=float('-inf'), beta=float('inf'), max_depth=max_depth)
      self.undo_play(*play[1], *play[0], captured_piece)
      self.print_board()

      if score > best_score:
          best_score = score
          best_play = play
    if best_play:
        self.make_play(*best_play[0], *best_play[1])
        self.switch_player()  

  def get_flasgship_pos(self):
    return [(r, c) for r, row in enumerate(self.board) for c, val in enumerate(row) if val == 'X'][0]
  
  def get_flagship_distance_from_edge(self):
    flagship_pos = self.get_flasgship_pos()
    return min(flagship_pos[0], 6-flagship_pos[0], flagship_pos[1], 6-flagship_pos[1])
  
  def silvers_pieces_near_flagship(self):
    silvers_near_flagship = 0
    flagship_pos = self.get_flasgship_pos()

    for row, col in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if 0 <= flagship_pos[0]+row < 7 and 0 <= flagship_pos[1]+col < 7:
            if self.board[flagship_pos[0]+row][flagship_pos[1]+col] == 'S':
                silvers_near_flagship += 1
    return silvers_near_flagship


  def heuristic_evaluation(self):
    gold_evaluation = (7 - self.get_flagship_distance_from_edge()) * self.heuristic_weights['close_to_edge'] # 10
    silver_evaluation = self.silvers_pieces_near_flagship() * self.heuristic_weights['silvers_near_flagship']  #15
    
    if self.player_2 == 'G': # se AI é G
        return gold_evaluation - silver_evaluation
    elif self.player_2 == 'S': # se AI É S
        return silver_evaluation - gold_evaluation


  def evaluate_board(self, result, depth):
      if result == 'G': 
        return -1000 + depth
      elif result == 'S': 
        return 1000 - depth
      else:  # HEURÍSTICA
        return self.heuristic_evaluation()

  # TODO: Vai ter max_depth mesmo? vou ignorar por enquanto
  # TODO: Implementar pro modo IAxIA, esse primeiro vai ser somente pensando que
  # MEU TIME => G, BOT TIME => S
  def minimax(self, depth, is_maximizing, alpha, beta, max_depth = 10000):
    result = self.verify_win()  # Vitória => 'G', 'S' 

    if result is not None or depth == max_depth:  # Se chegou em um estado de vitória ou chegou no limite de depth sem acabar o jogo
      return self.evaluate_board(result, depth)

      
    if is_maximizing:
      max_score = float('-inf')
      possible_plays = self.gold_player_possible_plays() if self.turn == 'G' else self.silver_player_possible_plays()
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
        min_eval = float('inf')
        possible_plays = self.silver_player_possible_plays() if self.turn == 'G' else self.gold_player_possible_plays()
        for play in possible_plays:
            captured_piece = self.make_play(*play[0], *play[1])
            score = self.minimax(depth + 1, True, alpha, beta, max_depth)
            self.undo_play(*play[1], *play[0], captured_piece)

            min_eval = min(min_eval, score)
            beta = min(beta, score)

            if beta <= alpha:
                break
        return min_eval
    

  
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
