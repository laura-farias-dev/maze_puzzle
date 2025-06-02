from queue import PriorityQueue

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