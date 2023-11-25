from tabuleiro import Tabuleiro
from copy import deepcopy
import sys

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
    # Complexidade: (d => profundidade árvore, b => quantidade movimentos possíveis no nível d)
      # Tempo = O(b^(d+1)) => é d + 1 pois estou abrindo todos os nós possíveis de um nível antes de detectar se um deles é a solução
      # Espaço = O(b^(d+1))
    # É completa, se tiver uma solução ela vai achar! (pode demorar muito, cada vez q a arvore vai se aprofundando)
    # É otima pois as operações (movimentos do quebra cabeça) tem o mesmo custo sempre
      
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

  def busca_em_profundidade(self):
    # Complexidade: (d => profundidade máxima gerada por cada nó, b => quantidade movimentos possíveis no nível d)
      # Tempo = O(b^d)
      # Espaço = O(b*d)
    # Essa implemetanção é completa! Pois eu verifico se o estado do tabuleiro já foi visitado (evitando ciclos!)
    # Não é otima, pois ela encontra a primeira a solução. Mas não necessariamente, essa primeira solução vai ser a com
    # menor quantidade de movimentos!
      
    stack = [(self.tabuleiro, [])]  
    visited = [self.tabuleiro.tabuleiro]

    while stack:
      current_board, movements_sequence = stack.pop()

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
            stack.append((new_board, movements_sequence + [movement]))
            
  def busca_em_profundidade_limitada(self, limit = 50):
    # Complexidade: (m => limite de profundidade, b => quantidade movimentos possíveis no nível)
      # Tempo = O(b^m)
      # Espaço = O(b*m)
    # Pode ser incompleta, se a solução estiver abaxo do limite
    # Não é otima, pois ela encontra a primeira a solução. Mas não necessariamente, essa primeira solução vai ser a com
    # menor quantidade de movimentos!
      
    stack = [(self.tabuleiro, [])]  
    visited = [self.tabuleiro.tabuleiro]

    while stack:
      current_board, movements_sequence = stack.pop()

      if self.final_state_verifier(current_board.tabuleiro):
          current_board.print_tabuleiro()
          print("Número de movimentos:", len(movements_sequence))
          print("Movimentos realizados:", movements_sequence)
          return True
      
      movements_quantity = len(movements_sequence)
      
      if movements_quantity >= limit: # passa pro proximo tabuleiro da pilha 
        continue
    
      _, possible_movements = current_board.movimentos_possiveis()

      for movement in possible_movements:
          new_board = deepcopy(current_board)
          new_board.mover(movement)

          if new_board.tabuleiro not in visited:
            visited.append(new_board.tabuleiro)
            stack.append((new_board, movements_sequence + [movement]))
    print(f"Não foi possivel achar solução com o limite de profundidade passado! ({limit})")
    return False
  
  def busca_aprofundamento_iterativo(self):
    # Complexidade: (d => profundidade, b => quantidade movimentos possíveis no nível)
      # Tempo = O(b^d)
      # Espaço = O(b*d)
    # É completa, pois vai aumentando o limite até achar a solução (e também tem a verificação para não formar ciclos infitos)
    # Não é otima, pois ela encontra a primeira a solução. Mas não necessariamente, essa primeira solução vai ser a com
    # menor quantidade de movimentos. E além disso, ela explora alguns caminhos repetidamente
    
    max_integer = sys.maxsize
    for limit in range(1, max_integer):
      print("Limite: ", limit)
      result = self.busca_em_profundidade_limitada(limit)
      if result:
          return result
        
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

quebra_cabeca = QuebraCabeca(3)
quebra_cabeca.tabuleiro.print_tabuleiro()
print("Não dá pra resolver :(" if quebra_cabeca.isnt_solvable() else "Dá pra resolver!")
quebra_cabeca.busca_aprofundamento_iterativo()
