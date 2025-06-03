import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

grafo = nx.Graph()

arestas = [
    ('A', 'C', 2), ('A', 'D', 1),
    ('C', 'D', 1), ('C', 'E', 2),
    ('D', 'E', 1), ('E', 'B', 2)
]

grafo.add_weighted_edges_from(arestas)

caminho = nx.dijkstra_path(grafo, source='A', target='B')

posicoes = nx.spring_layout(grafo, seed=42)

figura, eixo = plt.subplots(figsize=(8, 6))

def atualizar(passo):
    eixo.clear()

    nx.draw(grafo, posicoes, ax=eixo, with_labels=True, node_color='lightgray', node_size=700, edge_color='gray')

    if passo > 0:
        subcaminho = caminho[:passo+1]
        arestas_percorridas = list(zip(subcaminho[:-1], subcaminho[1:]))

        nx.draw_networkx_nodes(grafo, posicoes, nodelist=subcaminho, node_color='skyblue', node_size=700, ax=eixo)

        nx.draw_networkx_edges(grafo, posicoes, edgelist=arestas_percorridas, edge_color='blue', width=2, ax=eixo)

    pesos = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, posicoes, edge_labels=pesos, ax=eixo)

    eixo.set_title(f"Passo {passo}/{len(caminho)-1}: {'->'.join(caminho[:passo+1])}")

animacao = animation.FuncAnimation(figura, atualizar, frames=len(caminho), interval=1000, repeat=False)

plt.show()

