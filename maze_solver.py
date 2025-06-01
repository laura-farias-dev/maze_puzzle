from queue import PriorityQueue
import random
from colorama import init, Fore, Back, Style
import os
import time

class Vertice:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.visitado = False
        self.adjacentes = []
        self.distancia_aestrela = float('inf')
        self.custo_g = float('inf')
        self.pai = None

    def __lt__(self, other):
        return self.distancia_aestrela < other.distancia_aestrela

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
        # 1. Inicializa a matriz inteira com paredes.
        self.matriz = [['#' for _ in range(self.colunas)] for _ in range(self.linhas)]
        
        # 2. Define os tipos de terreno aberto e suas probabilidades.
        tipos_terreno_aberto = ['.', '?', '-'] 
        pesos_terreno_aberto = [0.33, 0.33, 0.33] # Mais chance de '.', depois '?', depois '-'
        
        # Probabilidade de uma célula interna ser uma PAREDE.
        # Ex: 0.3 significa 30% de chance de ser parede, 70% de ser terreno aberto.
        probabilidade_ser_parede_interna = 0.3 

        # Itera sobre as células INTERNAS para definir se são paredes ou terreno.
        for i in range(1, self.linhas - 1): 
            for j in range(1, self.colunas - 1): 
                if random.random() > probabilidade_ser_parede_interna:
                    # Se não for parede, escolhe um tipo de terreno aberto.
                    self.matriz[i][j] = random.choices(tipos_terreno_aberto, weights=pesos_terreno_aberto)[0]
                # Else: a célula permanece '#' (parede), como foi inicializada.

        # 3. Define as coordenadas do início e fim.
        start_pos = (1, 1)
        end_pos = (self.linhas - 2, self.colunas - 2)

        # 4. Garante que as células adjacentes ao início e fim sejam caminho '.',
        #    isso pode "abrir" paredes internas que estejam bloqueando o início/fim.
        #    Afeta apenas células INTERNAS.
        posicoes_para_limpar = set()
        # Adjacentes ao início
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            ni_s, nj_s = start_pos[0] + di, start_pos[1] + dj
            # Verifica se está dentro dos limites INTERNOS (não na borda de parede externa)
            if 1 <= ni_s < self.linhas - 1 and 1 <= nj_s < self.colunas - 1:
                posicoes_para_limpar.add((ni_s, nj_s))
        
        # Adjacentes ao fim
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni_e, nj_e = end_pos[0] + di, end_pos[1] + dj
            if 1 <= ni_e < self.linhas - 1 and 1 <= nj_e < self.colunas - 1:
                posicoes_para_limpar.add((ni_e, nj_e))

        for r, c in posicoes_para_limpar:
            # Só altera para '.' se não for a posição exata do início ou do fim.
            if (r, c) != start_pos and (r, c) != end_pos:
                self.matriz[r][c] = '.' 
        
        # 5. Garante que as posições de início e fim sejam marcadas como 's' e 'e'
        #    e sejam transitáveis (sobrescrevendo paredes, se houver).
        self.matriz[start_pos[0]][start_pos[1]] = 's'
        self.matriz[end_pos[0]][end_pos[1]] = 'e'

        # 6. Cria os vértices do grafo.
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matriz[i][j] != '#': # Apenas para células que não são paredes
                    vertice = Vertice(i, j, self.matriz[i][j])
                    self.vertices[(i, j)] = vertice
                    if self.matriz[i][j] == 's':
                        self.inicio = vertice
                    elif self.matriz[i][j] == 'e':
                        self.fim = vertice
        
        # Ajuste para o caso de labirintos muito pequenos onde início e fim podem ser o mesmo.
        if start_pos == end_pos and self.matriz[start_pos[0]][start_pos[1]] == 'e':
            if self.inicio is None and (start_pos[0], start_pos[1]) in self.vertices:
                 self.inicio = self.vertices[(start_pos[0], start_pos[1])]

        # 7. Conecta os vértices adjacentes.
        for i in range(self.linhas):
            for j in range(self.colunas):
                if (i,j) in self.vertices: # Se existe um vértice na posição (i,j)
                    vertice_atual = self.vertices[(i,j)]
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Vizinhos
                        ni, nj = i + di, j + dj
                        # Verifica se o vizinho está dentro dos limites e também é um vértice (não parede)
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

class BuscaAEstrela:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.encontrado = False
        self.caminho = []

    def busca_aestrela(self):
        for v in self.labirinto.vertices.values():
            v.visitado = False
            v.custo_g = float('inf')
            v.distancia_aestrela = float('inf')
            v.pai = None

        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        if not inicio or not fim:
            print("Erro: Ponto de início ou fim não definido adequadamente no labirinto.")
            self.encontrado = False
            return

        fila = PriorityQueue()
        inicio.custo_g = 0
        inicio.distancia_aestrela = self.labirinto.heuristica(inicio, fim)
        fila.put(inicio)
        
        while not fila.empty() and not self.encontrado:
            atual = fila.get()
            
            if atual.visitado:
                continue
            
            atual.visitado = True
                
            if atual == fim:
                self.encontrado = True
                self.reconstruir_caminho(atual)
                break
            
            for vizinho in atual.adjacentes:
                novo_custo = atual.custo_g + self.labirinto.get_custo(vizinho)
                if novo_custo < vizinho.custo_g:
                    vizinho.custo_g = novo_custo
                    vizinho.distancia_aestrela = novo_custo + self.labirinto.heuristica(vizinho, fim)
                    vizinho.pai = atual
                    fila.put(vizinho)

    def reconstruir_caminho(self, vertice):
        atual = vertice
        while atual is not None:
            self.caminho.append((atual.x, atual.y))
            atual = atual.pai
        self.caminho.reverse()

class MazeVisualizer:
    def __init__(self):
        init() 
        self.symbols = {
            '#': '█', '.': '·', '?': 'F', '-': '~', 
            's': 'S', 'e': 'E', '*': 'o' 
        }
        self.colors = {
            '#': Fore.WHITE + Back.WHITE, '.': Fore.GREEN + Back.GREEN,
            '?': Fore.GREEN + Back.GREEN, '-': Fore.YELLOW + Back.YELLOW,
            's': Fore.BLUE + Back.BLUE, 'e': Fore.RED + Back.RED,
            '*': Fore.CYAN + Back.CYAN
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_maze(self, matriz, caminho=None):
        self.clear_screen()
        print("\nLabirinto:")
        print("Legenda:")
        print(f"{self.colors['#']}{self.symbols['#']}{Style.RESET_ALL} = Parede")
        print(f"{self.colors['.']}{self.symbols['.']}{Style.RESET_ALL} = Piso liso (custo 1)")
        print(f"{self.colors['?']}{self.symbols['?']}{Style.RESET_ALL} = Floresta (custo 2)")
        print(f"{self.colors['-']}{self.symbols['-']}{Style.RESET_ALL} = Lama (custo 3)")
        print(f"{self.colors['s']}{self.symbols['s']}{Style.RESET_ALL} = Início")
        print(f"{self.colors['e']}{self.symbols['e']}{Style.RESET_ALL} = Fim")
        print(f"{self.colors['*']}{self.symbols['*']}{Style.RESET_ALL} = Caminho encontrado")
        print("\n")

        matriz_para_imprimir = [list(linha) for linha in matriz]

        if caminho:
            for x, y in caminho:
                if 0 <= x < len(matriz_para_imprimir) and 0 <= y < len(matriz_para_imprimir[0]):
                    if matriz_para_imprimir[x][y] not in ['s', 'e']:
                         if matriz_para_imprimir[x][y] == '#':
                            pass 
                         matriz_para_imprimir[x][y] = '*' 
        
        for i in range(len(matriz_para_imprimir)):
            for j in range(len(matriz_para_imprimir[i])):
                celula_tipo = matriz_para_imprimir[i][j]
                simbolo_final = self.symbols.get(celula_tipo, celula_tipo)
                cor_final = self.colors.get(celula_tipo, Fore.WHITE + Back.BLACK)
                print(f"{cor_final}{simbolo_final}{Style.RESET_ALL}", end='') 
            print() 

    def animate_solution(self, matriz, caminho, delay=0.05):
        if not caminho:
            print("Nenhum caminho encontrado!")
            return

        for i in range(len(caminho)):
            matriz_frame = [list(row) for row in matriz] 
            
            for k in range(i + 1):
                xc_k, yc_k = caminho[k]
                if 0 <= xc_k < len(matriz_frame) and 0 <= yc_k < len(matriz_frame[0]):
                    if matriz[xc_k][yc_k] not in ['s', 'e']: 
                        matriz_frame[xc_k][yc_k] = '*'
            
            self.print_maze(matriz_frame) 
            time.sleep(delay)

def main():
    tamanho_labirinto = 20 
    labirinto = Labirinto(tamanho_labirinto)
    
    print("\nLabirinto Original (ASCII):")
    for linha in labirinto.matriz:
        print(''.join(linha)) 
    
    visualizer = MazeVisualizer()
    
    print("\nLabirinto Original (Colorido):")
    visualizer.print_maze(labirinto.matriz)
    input("\nPressione Enter para encontrar a solução...")
    
    busca = BuscaAEstrela(labirinto)
    busca.busca_aestrela()
    
    if busca.encontrado:
        print("\nSolução encontrada!")
        print("Animando o caminho...")
        visualizer.animate_solution(labirinto.matriz, busca.caminho)
        
        if labirinto.fim: 
            custo_total_g = labirinto.fim.custo_g
            print(f"\nCusto total do caminho (g do nó final): {custo_total_g}")
    else:
        print("\nNenhuma solução encontrada!")

if __name__ == "__main__":
    main()