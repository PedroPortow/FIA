from tabuleiro import Tabuleiro
from queue import Queue
import copy

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
    
  def busca_em_largura(self):
    queue_to_visit = [self.tabuleiro]
    visited_states = []
    
    while queue_to_visit:
      current_board_state = queue_to_visit.pop()
      
      print("------------------------------")
      current_board_state.print_tabuleiro()
      print("------------------------------")
      
      if self.final_state_verifier(current_board_state.tabuleiro):
        print("achou a solução")
        return
      
      # transformar pra string e adicioanr no visited_states pra comparacao
      current_state_to_str = str(current_board_state.tabuleiro) 
      
      possible_board_states, possible_movements = current_board_state.movimentos_possiveis()
      
      #pra cada movimento, deve adicionar em uma fila
      for next_board_state, movement in zip(possible_board_states, possible_movements):
        print(movement)
        new_board = self.new_board_state(current_board_state, movement)
        queue_to_visit.append(new_board)

  def new_board_state(self, current_board, movement):
    new_board = Tabuleiro(self.lado, False, current_board.tabuleiro)
    new_board.identificar_movimento(movement)
    return new_board
      
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
        
        if in_order_flag:
           print("CABOBOBOBOBOO")

    return in_order_flag

quebra_cabeca = QuebraCabeca(2)
quebra_cabeca.tabuleiro.print_tabuleiro()
# quebra_cabeca.tabuleiro.identificar_movimento("direita")
# quebra_cabeca.tabuleiro.print_tabuleiro()
# quebra_cabeca.final_state_verifier()
quebra_cabeca.busca_em_largura()
