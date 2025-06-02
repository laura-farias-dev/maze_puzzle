import os
import time
from colorama import init, Fore, Back, Style

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
        # Limpa a tela do terminal
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

        # Cria uma cópia da matriz para não modificar a original
        matriz_para_imprimir = [list(linha) for linha in matriz]

        # Se houver um caminho, marca ele na matriz
        if caminho:
            for x, y in caminho:
                if 0 <= x < len(matriz_para_imprimir) and 0 <= y < len(matriz_para_imprimir[0]):
                    if matriz_para_imprimir[x][y] not in ['s', 'e']:
                         if matriz_para_imprimir[x][y] == '#':
                            pass  # Não marca paredes
                         matriz_para_imprimir[x][y] = '*' 
        
        # Imprime a matriz com as cores e símbolos apropriados
        for i in range(len(matriz_para_imprimir)):
            for j in range(len(matriz_para_imprimir[i])):
                celula_tipo = matriz_para_imprimir[i][j]
                simbolo_final = self.symbols.get(celula_tipo, celula_tipo)
                cor_final = self.colors.get(celula_tipo, Fore.WHITE + Back.BLACK)
                print(f"{cor_final}{simbolo_final}{Style.RESET_ALL}", end='') 
            print() 

    def animate_solution(self, matriz, caminho, delay=0.5):
        # Verifica se existe um caminho para animar
        if not caminho:
            print("Nenhum caminho encontrado!")
            return

        # Anima o caminho passo a passo
        for i in range(len(caminho)):
            # Cria uma cópia da matriz para cada frame da animação
            matriz_frame = [list(row) for row in matriz] 
            
            # Marca o caminho até o ponto atual
            for k in range(i + 1):
                xc_k, yc_k = caminho[k]
                if 0 <= xc_k < len(matriz_frame) and 0 <= yc_k < len(matriz_frame[0]):
                    if matriz[xc_k][yc_k] not in ['s', 'e']: 
                        matriz_frame[xc_k][yc_k] = '*'
            
            # Imprime o frame atual e espera o delay
            self.print_maze(matriz_frame) 
            time.sleep(delay) 