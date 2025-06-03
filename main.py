import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

num_vertices = 8 
max_peso = 10
min_arestas_por_vertice = 2

def gerar_grafo_com_caminho():
    while True:
        vertices = ['A', 'B'] + [chr(ord('C') + i) for i in range(num_vertices - 2)]
        grafo = nx.Graph()
        grafo.add_nodes_from(vertices)

        for v in vertices:
            conexoes = random.sample([u for u in vertices if u != v], random.randint(min_arestas_por_vertice, num_vertices - 1))
            for u in conexoes:
                if not grafo.has_edge(v, u):
                    peso = random.randint(1, max_peso)
                    grafo.add_edge(v, u, weight=peso)

        if nx.has_path(grafo, 'A', 'B'):
            return grafo, vertices

grafo, vertices = gerar_grafo_com_caminho()
origem = 'A'
destino = 'B'
caminho = nx.dijkstra_path(grafo, source=origem, target=destino)

peso_total = sum(grafo[u][v]['weight'] for u, v in zip(caminho[:-1], caminho[1:]))

posicoes = nx.spring_layout(grafo, seed=42)

figura, eixo = plt.subplots(figsize=(8, 6))

def atualizar(passo):
    eixo.clear()
    nx.draw(grafo, posicoes, ax=eixo, with_labels=True, node_color='lightgray', node_size=700, edge_color='gray')

    if passo > 0:
        subcaminho = caminho[:passo+1]
        arestas_percorridas = list(zip(subcaminho[:-1], subcaminho[1:]))
        nx.draw_networkx_nodes(grafo, posicoes, nodelist=subcaminho, node_color='skyblue', node_size=700, ax=eixo)
        nx.draw_networkx_edges(grafo, posicoes, edgelist=arestas_percorridas, edge_color='red', width=2, ax=eixo)

    pesos = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, posicoes, edge_labels=pesos, ax=eixo)

    eixo.set_title(f"Passo {passo}/{len(caminho)-1}: {' ➜ '.join(caminho[:passo+1])}")

print(f"Caminho de A até B: {' ➜ '.join(caminho)}")
print(f"Peso total do caminho: {peso_total}")

animacao = animation.FuncAnimation(figura, atualizar, frames=len(caminho), interval=1000, repeat=False)

plt.show()