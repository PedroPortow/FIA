from tabuleiro import Tabuleiro
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
            # obj tabuluiro  #next_move #moves made
    queue = [(self.tabuleiro, "", [])] 
    visited = []
    
    while queue:
      current_board, movement_to_do, moves_done = queue.pop(0)
      
      if self.final_state_verifier(current_board.tabuleiro):
        print("glória")
        for moves in moves_done:
          print(moves)
        return
      
      # if current_board.tabuleiro in visited:
      #   print("caiu na desgraça vvv")
      #   continue
      
      current_board.print_tabuleiro()
      
      # PRECISO PASSAR O MOVES_DONE PARA A FRENTE...
      _, possible_movements = current_board.movimentos_possiveis()
      
      if(movement_to_do != ""):
        current_board.identificar_movimento(movement_to_do)
        moves_done.append(movement_to_do)
        visited.append(current_board.tabuleiro)
      
      print("----- DEOPIS DO MOV")
      current_board.print_tabuleiro()
            
      #pra cada movimento, deve adicionar em uma fila
      for movement in possible_movements:
        queue.append((current_board, movement, moves_done))
              
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
quebra_cabeca.busca_em_largura()
