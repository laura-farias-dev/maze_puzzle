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
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []
        self.vertices = {}
        self.inicio = None
        self.fim = None
        self.gerar_labirinto()

    def gerar_labirinto(self):
        # Inicializa matriz com paredes
        self.matriz = [['#' for _ in range(self.colunas)] for _ in range(self.linhas)]
        
        # Gera caminhos aleatórios
        for i in range(1, self.linhas-1):
            for j in range(1, self.colunas-1):
                if random.random() > 0.3:  # 70% de chance de ser caminho
                    tipos = ['.', '?', '-']
                    pesos = [0.7, 0.2, 0.1]  # Probabilidades para cada tipo
                    self.matriz[i][j] = random.choices(tipos, weights=pesos)[0]

        # Coloca início e fim
        self.matriz[1][1] = 's'
        self.matriz[self.linhas-2][self.colunas-2] = 'e'

        # Cria vértices
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matriz[i][j] != '#':
                    vertice = Vertice(i, j, self.matriz[i][j])
                    self.vertices[(i, j)] = vertice
                    if self.matriz[i][j] == 's':
                        self.inicio = vertice
                    elif self.matriz[i][j] == 'e':
                        self.fim = vertice

        # Conecta vértices adjacentes
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.matriz[i][j] != '#':
                    vertice = self.vertices[(i, j)]
                    # Verifica vizinhos (cima, baixo, esquerda, direita)
                    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.linhas and 0 <= nj < self.colunas:
                            if self.matriz[ni][nj] != '#':
                                vertice.adjacentes.append(self.vertices[(ni, nj)])

    def get_custo(self, vertice):
        if vertice.tipo == '.':
            return 1
        elif vertice.tipo == '?':
            return 2
        elif vertice.tipo == '-':
            return 3
        return 0

    def heuristica(self, v1, v2):
        # Distância de Manhattan
        return abs(v1.x - v2.x) + abs(v1.y - v2.y)

class BuscaAEstrela:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.encontrado = False
        self.caminho = []

    def busca_aestrela(self):
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        # Inicializa fila de prioridade
        fila = PriorityQueue()
        inicio.custo_g = 0
        inicio.distancia_aestrela = self.labirinto.heuristica(inicio, fim)
        fila.put(inicio)
        
        while not fila.empty() and not self.encontrado:
            atual = fila.get()
            
            if atual == fim:
                self.encontrado = True
                self.reconstruir_caminho(atual)
                break
                
            atual.visitado = True
            
            for vizinho in atual.adjacentes:
                if not vizinho.visitado:
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
        init()  # Initialize colorama
        self.symbols = {
            '#': '█',  # Wall
            '.': '·',  # Smooth floor
            '?': '🌲',  # Forest
            '-': '~',  # Mud
            's': '🚶',  # Start
            'e': '🏁',  # End
            '*': '●'   # Path
        }
        
        self.colors = {
            '#': Fore.WHITE + Back.WHITE,
            '.': Fore.GREEN + Back.GREEN,
            '?': Fore.GREEN + Back.GREEN,
            '-': Fore.YELLOW + Back.YELLOW,
            's': Fore.BLUE + Back.BLUE,
            'e': Fore.RED + Back.RED,
            '*': Fore.CYAN + Back.CYAN
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_maze(self, matriz, caminho=None):
        self.clear_screen()
        print("\nLabirinto:")
        print("Legenda:")
        print(f"{self.colors['#']}█{Style.RESET_ALL} = Parede")
        print(f"{self.colors['.']}·{Style.RESET_ALL} = Piso liso (custo 1)")
        print(f"{self.colors['?']}🌲{Style.RESET_ALL} = Bosque (custo 2)")
        print(f"{self.colors['-']}~{Style.RESET_ALL} = Lama (custo 3)")
        print(f"{self.colors['s']}🚶{Style.RESET_ALL} = Início")
        print(f"{self.colors['e']}🏁{Style.RESET_ALL} = Fim")
        print(f"{self.colors['*']}●{Style.RESET_ALL} = Caminho encontrado")
        print("\n")

        # Se houver um caminho, marca ele na matriz
        if caminho:
            matriz_com_caminho = [list(linha) for linha in matriz]
            for x, y in caminho[1:-1]:  # Exclui início e fim
                matriz_com_caminho[x][y] = '*'
        else:
            matriz_com_caminho = matriz

        # Imprime o labirinto
        for linha in matriz_com_caminho:
            for celula in linha:
                print(f"{self.colors[celula]}{self.symbols[celula]}{Style.RESET_ALL}", end='')
            print()

    def animate_solution(self, matriz, caminho, delay=0.5):
        """Anima a solução do labirinto mostrando o caminho sendo construído"""
        if not caminho:
            print("Nenhum caminho encontrado!")
            return

        matriz_com_caminho = [list(linha) for linha in matriz]
        
        # Mostra o labirinto inicial
        self.print_maze(matriz)
        time.sleep(delay)

        # Anima o caminho
        for x, y in caminho[1:-1]:  # Exclui início e fim
            matriz_com_caminho[x][y] = '*'
            self.print_maze(matriz_com_caminho)
            time.sleep(delay)

def main():
    # Cria um labirinto
    labirinto = Labirinto(10, 10)
    
    # Mostra o labirinto original em ASCII
    print("\nLabirinto Original (ASCII):")
    for linha in labirinto.matriz:
        print(''.join(linha))
    
    # Cria o visualizador
    visualizer = MazeVisualizer()
    
    # Mostra o labirinto original colorido
    print("\nLabirinto Original (Colorido):")
    visualizer.print_maze(labirinto.matriz)
    input("\nPressione Enter para continuar...")
    
    # Executa A*
    busca = BuscaAEstrela(labirinto)
    busca.busca_aestrela()
    
    if busca.encontrado:
        print("\nSolução encontrada!")
        print("Animando o caminho...")
        visualizer.animate_solution(labirinto.matriz, busca.caminho)
        
        # Calcula o custo total
        custo_total = sum(labirinto.get_custo(labirinto.vertices[(x, y)]) 
                         for x, y in busca.caminho[1:])
        print(f"\nCusto total do caminho: {custo_total}")
    else:
        print("\nNenhuma solução encontrada!")

if __name__ == "__main__":
    main() 