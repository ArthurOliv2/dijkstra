import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parâmetros
num_vertices = 8
max_peso = 10
min_arestas_por_vertice = 2

# Gerar nomes dos nós automaticamente (A, B, C, ...)
vertices = [chr(ord('A') + i) for i in range(num_vertices)]

# Criar grafo vazio
grafo = nx.Graph()
grafo.add_nodes_from(vertices)

# Garantir conexões mínimas para cada vértice
for v in vertices:
    conexoes = random.sample([u for u in vertices if u != v], random.randint(min_arestas_por_vertice, num_vertices - 1))
    for u in conexoes:
        if not grafo.has_edge(v, u):  # evita duplicatas
            peso = random.randint(1, max_peso)
            grafo.add_edge(v, u, weight=peso)

# Escolher aleatoriamente ponto de partida e chegada
origem, destino = random.sample(vertices, 2)

# Calcular o menor caminho (com tratamento de erro caso não haja caminho)
try:
    caminho = nx.dijkstra_path(grafo, source=origem, target=destino)
except nx.NetworkXNoPath:
    print("Não há caminho entre os pontos selecionados.")
    exit()

# Layout dos nós
posicoes = nx.spring_layout(grafo, seed=42)

# Criar a figura
figura, eixo = plt.subplots(figsize=(8, 6))

# Função para atualizar a animação
def atualizar(passo):
    eixo.clear()
    nx.draw(grafo, posicoes, ax=eixo, with_labels=True, node_color='lightgray', node_size=700, edge_color='gray')
    
    if passo > 0:
        subcaminho = caminho[:passo+1]
        arestas_percorridas = list(zip(subcaminho[:-1], subcaminho[1:]))
        
        nx.draw_networkx_nodes(grafo, posicoes, nodelist=subcaminho, node_color='skyblue', node_size=700, ax=eixo)
        nx.draw_networkx_edges(grafo, posicoes, edgelist=arestas_percorridas, edge_color='blue', width=2, ax=eixo)

    # Mostrar pesos
    pesos = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, posicoes, edge_labels=pesos, ax=eixo)

    eixo.set_title(f"Passo {passo}/{len(caminho)-1}: {' ➜ '.join(caminho[:passo+1])}")

# Criar a animação
animacao = animation.FuncAnimation(figura, atualizar, frames=len(caminho), interval=1000, repeat=False)

# Informar no terminal
print(f"Origem: {origem} | Destino: {destino}")
print(f"Menor caminho encontrado: {' ➜ '.join(caminho)}")

# Mostrar a animação
plt.show()