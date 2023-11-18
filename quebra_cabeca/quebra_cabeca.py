from tabuleiro import Tabuleiro
from collections import  deque

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
    self.tabuleiro = Tabuleiro(lado, random)
    
  def busca_em_largura(self):
    pass
  
  def final_state_verifier(self):
    counter = 0  
    in_order_flag = True

    for i in range(self.lado):
        for j in range(self.lado):
            print(counter)
            if self.tabuleiro.tabuleiro[i][j] != counter:
                in_order_flag = False
                break
            counter += 1
        if not in_order_flag:
            break

    print("Em ordem! (estado final)" if in_order_flag else "Não está em ordem (não tá no estado final)" )
    return in_order_flag


            
quebra_cabeca = QuebraCabeca(2)
quebra_cabeca.tabuleiro.print_tabuleiro()
quebra_cabeca.final_state_verifier()
# solução = quebra_cabeca.busca_em_largura()
