import random 

#
#        X
#     Y [2, 3, 4, 5]
#       [1, 0, 2, 4]
#
#    Y = ALTURA
#    X = HORIZONTAL


class Tabuleiro:
  def __init__(self, lado, random = True, custom_state = []):
    self.lado = lado
    if(random and custom_state == []):
      self.incializa_tabuleiro_random()
    elif(custom_state):
       self.inicializa_tabuleiro_custom(custom_state)
    else: 
      self.inicializa_tabuleiro()
    self.movimentos = {'cima': self.mover_cima, 'baixo': self.mover_baixo, 'direita': self.mover_direita, 'esquerda': self.mover_esquerda}

  def inicializa_tabuleiro(self):
    self.tabuleiro = [[i + j * self.lado for i in range(1, self.lado + 1)] for j in range(self.lado)]
    self.tabuleiro[-1][-1] = 0
    self.x = self.lado - 1
    self.y = self.lado - 1

  def inicializa_tabuleiro_custom(self, custom_state):
    self.tabuleiro = custom_state
    player_position = self.get_player_position() #pega posição do player e seta no self.x e self.y
    self.y = player_position[0]
    self.x = player_position[1]
    
  def incializa_tabuleiro_random(self):
    numbers = list(range(0, self.lado * self.lado)) # gerando os numeros
    random.shuffle(numbers) #numeros na ordem aleatoria
    self.tabuleiro = [[numbers.pop(0) if numbers else 0 for _ in range(self.lado)] for _ in range(self.lado)] #botando os elementos na matriz
    
    player_position = self.get_player_position() #pega posição do player e seta no self.x e self.y
    self.y = player_position[0]
    self.x = player_position[1]
    
  def get_player_position(self):
     for i in range(self.lado):
        for j in range(self.lado):
            if self.tabuleiro[i][j] == 0:
              return i, j
            
  def mover(self, movimento):
    if(movimento == "cima"):
      self.mover_cima()
    if(movimento == "baixo"):
      self.mover_baixo()
    if(movimento == "esquerda"):
      self.mover_esquerda()
    if(movimento == "direita"):
      self.mover_direita()

  def troca(self, novo_x, novo_y):
    aux = self.tabuleiro[novo_y][novo_x] # pegando o elemento na posição
    self.tabuleiro[novo_y][novo_x] = self.tabuleiro[self.y][self.x]
    self.tabuleiro[self.y][self.x] = aux

  def mover_cima(self):
    if self.pode_subir():
        self.troca(self.x, self.y - 1)
        self.y = self.y - 1
        return True
    return False

  def mover_baixo(self):
    if self.pode_descer():
        self.troca(self.x, self.y + 1)
        self.y = self.y + 1
        return True
    return False

  def mover_direita(self):
    if self.pode_direita():
        self.troca(self.x + 1, self.y)
        self.x = self.x + 1
        return True
    return False

  def mover_esquerda(self):
    if self.pode_esquerda():
        self.troca(self.x - 1, self.y)
        self.x = self.x - 1
        return True
    return False

  def movimentos_possiveis(self):
    lista_movimentos = []
    lista_acoes = []

    # pra cima
    if self.pode_subir():
        novo_y = self.y - 1
        lista_movimentos.append((self.x, novo_y))
        lista_acoes.append('cima')

    # pra baixo
    if self.pode_descer():
        novo_y = self.y + 1
        lista_movimentos.append((self.x, novo_y))
        lista_acoes.append('baixo')

    # pra direita
    if self.pode_direita():
        novo_x = self.x + 1
        lista_movimentos.append((novo_x, self.y))
        lista_acoes.append('direita')

    # pra esquerda
    if self.pode_esquerda():
        novo_x = self.x - 1
        lista_movimentos.append((novo_x, self.y))
        lista_acoes.append('esquerda')

    return lista_movimentos, lista_acoes

  def pode_descer(self):
    return self.y < (self.lado - 1)

  def pode_subir(self):
    return self.y > 0

  def pode_direita(self):
    return self.x < (self.lado - 1)

  def pode_esquerda(self):
    return self.x > 0

  def print_pos(self):
    print(f'x = {self.x}, y = {self.y}')

  def print_tabuleiro(self):
    for linha in self.tabuleiro:
      print(linha)
