from labirinto import Labirinto
from busca_aestrela import BuscaAEstrela
from impressao import MazeVisualizer

def main():
    # Criando o labirinto com a matriz fornecida
    labirinto = Labirinto([
        ["S", ".", ".", ".", "?", ".", ".", ".", "."],
        [".", "#", "#", "#", ".", "~", "~", "#", "."],
        [".", ".", "?", ".", ".", "~", ".", "#", "."],
        ["#", "#", ".", "#", ".", "~", ".", "#", "."],
        [".", ".", ".", "#", ".", "?", ".", ".", "."],
        [".", "#", ".", "#", "#", "?", "#", "#", "."],
        [".", "#", ".", ".", ".", ".", ".", "#", "."],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
        [".", ".", ".", "?", ".", ".", ".", ".", "E"]
    ])
    
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