import random
from vertice import Vertice

class Labirinto:
    def __init__(self, tamanho):
        self.linhas = max(3, tamanho)
        self.colunas = self.linhas 
        self.matriz = []
        self.vertices = {}
        self.inicio = None
        self.fim = None
        self.gerar_labirinto()

    def gerar_labirinto(self):
        # 1. Inicializa a matriz toda com paredes
        self.matriz = [['#' for _ in range(self.colunas)] for _ in range(self.linhas)]
        
        # 2. Define os tipos de terreno e as probabilidades
        tipos_terreno_aberto = ['.', '?', '-'] 
        pesos_terreno_aberto = [0.33, 0.33, 0.33]
        
        # Probabilidade célula interna ser PAREDE
        probabilidade_ser_parede_interna = 0.3 

        # Itera sobre as células INTERNAS
        for i in range(1, self.linhas - 1): 
            for j in range(1, self.colunas - 1): 
                if random.random() > probabilidade_ser_parede_interna:
                    # Se não for parede, escolhe um tipo de terreno
                    self.matriz[i][j] = random.choices(tipos_terreno_aberto, weights=pesos_terreno_aberto)[0]
                

        # 3. Define as coordenadas do início e fim.
        start_pos = (1, 1)
        end_pos = (self.linhas - 2, self.colunas - 2)

        # 4. Garante que as células adjacentes ao início e fim sejam caminho
        posicoes_para_limpar = set()
        # Adjacentes ao início
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            ni_s, nj_s = start_pos[0] + di, start_pos[1] + dj
            # Verifica se está dentro dos limites INTERNOS
            if 1 <= ni_s < self.linhas - 1 and 1 <= nj_s < self.colunas - 1:
                posicoes_para_limpar.add((ni_s, nj_s))
        
        # Adjacentes ao fim
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni_e, nj_e = end_pos[0] + di, end_pos[1] + dj
            if 1 <= ni_e < self.linhas - 1 and 1 <= nj_e < self.colunas - 1:
                posicoes_para_limpar.add((ni_e, nj_e))

        for r, c in posicoes_para_limpar:
            # Só altera para '.' se não for a posição exata do início ou do fim
            if (r, c) != start_pos and (r, c) != end_pos:
                self.matriz[r][c] = '.' 
        
        # 5. Garante que as posições de início e fim sejam marcadas como 's' e 'e'
        self.matriz[start_pos[0]][start_pos[1]] = 's'
        self.matriz[end_pos[0]][end_pos[1]] = 'e'

        # 6. Cria os vértices do grafo
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matriz[i][j] != '#': # Só pra células que não são paredes
                    vertice = Vertice(i, j, self.matriz[i][j])
                    self.vertices[(i, j)] = vertice
                    if self.matriz[i][j] == 's':
                        self.inicio = vertice
                    elif self.matriz[i][j] == 'e':
                        self.fim = vertice
        
        
        if start_pos == end_pos and self.matriz[start_pos[0]][start_pos[1]] == 'e':
            if self.inicio is None and (start_pos[0], start_pos[1]) in self.vertices:
                 self.inicio = self.vertices[(start_pos[0], start_pos[1])]

        # 7. Conecta os vértices adjacentes
        for i in range(self.linhas):
            for j in range(self.colunas):
                if (i,j) in self.vertices: # Se existe um vértice na posição (i,j)
                    vertice_atual = self.vertices[(i,j)]
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Vizinhos
                        ni, nj = i + di, j + dj
                        # Verifica se o vizinho está dentro dos limites e também é um vértice
                        if 0 <= ni < self.linhas and 0 <= nj < self.colunas and (ni,nj) in self.vertices:
                            vertice_vizinho = self.vertices[(ni,nj)]
                            vertice_atual.adjacentes.append(vertice_vizinho)

    def get_custo(self, vertice):
        if vertice.tipo == '.':
            return 1
        elif vertice.tipo == '?':
            return 2
        elif vertice.tipo == '-':
            return 3
        return 0

    def heuristica(self, v1, v2):
        return abs(v1.x - v2.x) + abs(v1.y - v2.y) 