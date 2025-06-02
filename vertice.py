class Vertice:
    def __init__(self, x, y, tipo):  
        self.x = x                  
        self.y = y                 
        self.tipo = tipo          
        self.visitado = False       
        self.adjacentes = []        
        self.distancia_aestrela = float('inf')  # Distância total estimada (f = g + h)
        self.custo_g = float('inf') # Custo acumulado do caminho até esse vértice
        self.pai = None             

    def __lt__(self, other):
        return self.distancia_aestrela < other.distancia_aestrela 