from vertice import Vertice

class Labirinto:
    def __init__(self, matriz):
        if not matriz or not matriz[0]:
            raise ValueError("Matriz inválida: deve ser uma matriz não vazia")
            
        self.matriz = matriz
        self.linhas = len(matriz)
        self.colunas = len(matriz[0])
        self.vertices = {}
        self.inicio = None
        self.fim = None
        self.processar_labirinto()
        
        # Verificação após processamento
        if self.inicio is None:
            raise ValueError("Não foi encontrado ponto de início (S) no labirinto")
        if self.fim is None:
            raise ValueError("Não foi encontrado ponto de fim (E) no labirinto")

    def processar_labirinto(self):
        # Cria os vértices do grafo
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matriz[i][j] != '#':  # Só para células que não são paredes
                    tipo = self.matriz[i][j].lower()  # Converte para minúsculo
                    vertice = Vertice(i, j, tipo)
                    self.vertices[(i, j)] = vertice
                    if self.matriz[i][j].upper() == 'S':
                        self.inicio = vertice
                    elif self.matriz[i][j].upper() == 'E':
                        self.fim = vertice

        # Conecta os vértices adjacentes
        for i in range(self.linhas):
            for j in range(self.colunas):
                if (i,j) in self.vertices:  # Se existe um vértice (não é parede)
                    vertice_atual = self.vertices[(i,j)]
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Olha para os vizinhos
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
        elif vertice.tipo == '~':
            return 3
        return 0

    def heuristica(self, v1, v2):
        return abs(v1.x - v2.x) + abs(v1.y - v2.y)
        
    def __str__(self):
        # Método para visualizar o labirinto
        return '\n'.join([''.join(linha) for linha in self.matriz]) 