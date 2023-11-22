from tabuleiro import Tabuleiro
from copy import deepcopy

# Algoritmos necessários:

# Busca em Largura
# Busca em Profundidade
# Busca em Profundidade Limitada
# Busca em Profundidade Iterativa/Aprofundamento Iterativo
# Busca com informação
  # Busca usando heurísticas
  # Testar pelo menos duas heurísticas diferentes
  
# RELATÓRIO

# Características da busca
#   Complexidade Assintótica
#     em tempo
#     em espaço/memória
# Discussão sobre características de algoritmos de buscas
  # A busca é ótima?
  # A busca é completa?

class QuebraCabeca:
  def __init__(self, lado, random = True):
    self.lado = lado
    self.last_position = lado * lado
    self.tabuleiro = Tabuleiro(lado, random)
    self.realized_movements = []
    
  def isnt_solvable(self):
    flatten_board = [tile for row in self.tabuleiro.tabuleiro for tile in row]
    inversions = sum(
        sum(flatten_board[i] > flatten_board[j] and flatten_board[j] != 0 for j in range(i + 1, len(flatten_board)))
        for i in range(len(flatten_board) - 1)
    )
    blank_row = next(i for i, row in enumerate(self.tabuleiro.tabuleiro) if 0 in row) + 1  # 1-based indexing

    if self.lado % 2 == 1:
        return inversions % 2 == 0
    else:
        return (inversions + blank_row) % 2 == 1

    
  def busca_em_largura(self):
    queue = [(self.tabuleiro, [])]  
    visited = [self.tabuleiro.tabuleiro]

    while queue:
      current_board, movements_sequence = queue.pop(0)

      if self.final_state_verifier(current_board.tabuleiro):
          current_board.print_tabuleiro()
          print("Número de movimentos:", len(movements_sequence))
          print("Movimentos realizados:", movements_sequence)
          return

      _, possible_movements = current_board.movimentos_possiveis()

      for movement in possible_movements:
          new_board = deepcopy(current_board)
          new_board.mover(movement)

          if new_board.tabuleiro not in visited:
            visited.append(new_board.tabuleiro)
            queue.append((new_board, movements_sequence + [movement]))
        
  def final_state_verifier(self, board):
    counter = 1 
    in_order_flag = True
    
    for i in range(self.lado):
        for j in range(self.lado):
            if counter == self.last_position:
              if board[i][j] != 0:
                in_order_flag = False
                break
            elif board[i][j] != counter:
                in_order_flag = False
                break
            
            counter += 1
        if not in_order_flag:
            break
        
    return in_order_flag

quebra_cabeca = QuebraCabeca(2)
quebra_cabeca.tabuleiro.print_tabuleiro()
print(quebra_cabeca.isnt_solvable())
quebra_cabeca.busca_em_largura()
