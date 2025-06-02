# Maze Solver

Este é um programa que gera e resolve labirintos usando o algoritmo A* (A Estrela).

## Requisitos

- Python 3.x
- colorama

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como usar

Execute o programa principal:
```bash
python main.py
```

O programa irá:
1. Gerar um labirinto aleatório
2. Mostrar o labirinto em formato ASCII e colorido
3. Encontrar o caminho mais curto do início ao fim usando o algoritmo A*
4. Animar a solução encontrada

## Legenda

- █ = Parede
- · = Piso liso (custo 1)
- F = Floresta (custo 2)
- ~ = Lama (custo 3)
- S = Início
- E = Fim
- o = Caminho encontrado 