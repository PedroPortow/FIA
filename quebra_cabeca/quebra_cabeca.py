from tabuleiro import Tabuleiro
from queue import Queue

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
    
  def busca_em_largura(self):
    # fila vai ter que armazenar os estados a serem explorados
    # solução ótima
    queue_to_visit = [self.tabuleiro]
    visited_states = []

    print(queue_to_visit)

    while queue_to_visit:
      board_current_state = queue_to_visit.pop(0)
      # print(board_current_state.tabuleiro)

      if self.final_state_verifier(board_current_state.tabuleiro):
        return

      visited_states.append(board_current_state)
      # print(visited_states)

      possible_board_states, possible_movements = board_current_state.movimentos_possiveis()
      
      for possible_board_states, possible_movements in zip(possible_board_states, possible_movements):
        # new_board_state = 

  def new_board_state(self, board):
    pass     
  
  def final_state_verifier(self, board):
    counter = 1 
    in_order_flag = True
    
    # verifica se tá em ordem crescente 1, 2, 3... e o ultimo é 0

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

    print("Em ordem! (estado final)" if in_order_flag else "Não está em ordem (não tá no estado final)" )
    return in_order_flag

quebra_cabeca = QuebraCabeca(2)
quebra_cabeca.tabuleiro.print_tabuleiro()
# quebra_cabeca.final_state_verifier()
quebra_cabeca.busca_em_largura()
