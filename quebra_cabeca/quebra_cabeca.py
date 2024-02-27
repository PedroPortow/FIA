from tabuleiro import Tabuleiro
from copy import deepcopy
import heapq
import itertools
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
    
  def busca_em_largura(self):
    # Complexidade: (d => profundidade árvore, b => quantidade movimentos possíveis no nível d)
      # Tempo = O(b^(d+1)) => é 
      # d + 1 pois estou abrindo todos os nós possíveis de um nível antes de detectar se um deles é a solução
      # Espaço = O(b^(d+1))
    # É completa, se tiver uma solução ela vai achar! (pode demorar muito, cada vez q a arvore vai se aprofundando)
    # É otima pois as operações (movimentos do quebra cabeça) tem o mesmo custo sempre
      
    queue = [(self.tabuleiro, [])]  
    visited = [self.tabuleiro.tabuleiro]
    nodes_expanded = 0  
    max_depth = 0  

    while queue:
      current_board, movements_sequence = queue.pop(0)
      nodes_expanded += 1
      current_depth = len(movements_sequence)

      if current_depth > max_depth:
        max_depth = current_depth

      if self.final_state_verifier(current_board.tabuleiro):
          current_board.print_tabuleiro()
          print("Número de movimentos:", len(movements_sequence))
          print("Movimentos realizados:", movements_sequence)
          print("Nós expandidos:", nodes_expanded)
          print("Profundidade Máxima:", max_depth)
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
    nodes_expanded = 0  
    max_depth = 0 

    while stack:
      current_board, movements_sequence = stack.pop()
      nodes_expanded += 1
      current_depth = len(movements_sequence)

      if current_depth > max_depth:
        max_depth = current_depth

      if self.final_state_verifier(current_board.tabuleiro):
          current_board.print_tabuleiro()
          print("Número de movimentos:", len(movements_sequence))
          print("Movimentos realizados:", movements_sequence)
          print("Nós expandidos:", nodes_expanded)
          print("Profundidade Máxima:", max_depth)
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
    nodes_expanded = 0  
    max_depth = 0 

    while stack:
      current_board, movements_sequence = stack.pop()
      nodes_expanded += 1
      current_depth = len(movements_sequence)

      if current_depth > max_depth:
        max_depth = current_depth

      if self.final_state_verifier(current_board.tabuleiro):
          current_board.print_tabuleiro()
          print("Número de movimentos:", len(movements_sequence))
          print("Movimentos realizados:", movements_sequence)
          print("Nós expandidos:", nodes_expanded)
          print("Profundidade Máxima:", max_depth)
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
    print(f"Não foi possivel achar solução com o limite de profundidade ({limit})")
    return False
  
  def busca_aprofundamento_iterativo(self):
    # Complexidade: (d => profundidade, b => quantidade movimentos possíveis no nível)
      # Tempo = O(b^d)
      # Espaço = O(b*d)
    # É completa, pois vai aumentando o limite até achar a solução (e também tem a verificação para não formar ciclos infitos)
    # É ótima
    
    max_integer = sys.maxsize
    for limit in range(1, max_integer):
      print("Limite: ", limit)
      result = self.busca_em_profundidade_limitada(limit)
      if result:
          return result
      

  def busca_com_informacao(self, chosen_heuristic = "Manhattan"):
    print(" ") 
    print("--- A* --")
    # Expandir nó "mais desejável" que ainda não foi expandido
    # Função de avaliação do nó => heurística
    # A* = Evitar expandir caminhos caros (custo pra chegar em n)
    # f(n) = g(n) + h(n)
    # g(n) => custo pra alcançar n (custo até chegar aqui no n)
    # h(n) => custo estimado de n até o objetivo (usando heurística)
    # f(n) => custo total estimado do caminho através de n até o objetivo
    # A cada nó verificar o custo de f e pegar o menor (QUE AINDA NÃO TENHA SIDO EXPANDIDO!)

    counter = itertools.count()  #  contador para desempate do heapq

    heuristic = self.manhattan_distance if chosen_heuristic == "Manhattan" else self.numbers_out_of_place
    initial_heuristic_cost = heuristic(self.tabuleiro.tabuleiro)

                     #f(n)                           #tabuleiro  #g(n) #lista de movimentos feitos pra chegar até aqui
    queue = [(initial_heuristic_cost, next(counter), self.tabuleiro, 0, [])]
    heapq.heapify(queue) # lista de prioridade
    visited = []
    nodes_expanded = 0
    max_depth = 0
   

    while queue:
      current_f, _, current_board, current_g, path = heapq.heappop(queue)

      if self.final_state_verifier(current_board.tabuleiro):
        print("Número de movimentos:", len(path))
        print("Movimentos realizados:", path)
        print("Nós expandidos:", nodes_expanded)
        print("Profundidade Máxima:", max_depth)
        current_board.print_tabuleiro()
        return

      visited.append(self.tabuleiro.tabuleiro)
      nodes_expanded += 1

      _, possible_movements = current_board.movimentos_possiveis()

      current_board.print_tabuleiro()
      print("-------")

      for movement in possible_movements:
        new_board = deepcopy(current_board)
        new_board.mover(movement)
      
        if new_board.tabuleiro not in visited:
          new_g_cost = current_g + 1
          new_h_cost = heuristic(new_board.tabuleiro)
          new_f_cost = new_g_cost + new_h_cost
          heapq.heappush(queue, (new_f_cost, next(counter), new_board, new_g_cost, path + [movement]))

          if new_g_cost > max_depth:
            max_depth = new_g_cost
        else: print("tabuleiro já visitado")
   
  def numbers_out_of_place(self, tabuleiro):
    wrong_pos_numbers = 0
    counter = 1
    for i in range(self.lado):
        for j in range(self.lado):
            if counter == self.last_position and tabuleiro[i][j] != 0: 
                wrong_pos_numbers += 1
                break
            if tabuleiro[i][j] != counter:
                wrong_pos_numbers += 1
            counter += 1
    return wrong_pos_numbers
  
  def manhattan_distance(self, board):
    # Créditos: https://github.com/Bishalsarang/8-Puzzle-Problem/blob/master/solve.py
    
    distance = 0
    for i in range(self.lado):
        for j in range(self.lado):
            tile = board[i][j]
            if tile != 0:
                target_x, target_y = divmod(tile - 1, self.lado)
                distance += abs(target_x - i) + abs(target_y - j)
    return distance
  
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
quebra_cabeca.busca_em_largura()
quebra_cabeca.busca_em_profundidade()
quebra_cabeca.busca_em_profundidade_limitada()
quebra_cabeca.busca_aprofundamento_iterativo()
quebra_cabeca.busca_com_informacao()
