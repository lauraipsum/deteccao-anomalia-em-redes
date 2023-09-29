# import networkx as nx
# import matplotlib.pyplot as plt
from data.data_read import criar_lista_de_adjacencia

lista_de_adjacencia = criar_lista_de_adjacencia()

def encontrar_vertices_de_corte(lista_de_adjacencia):
    momento_descoberta = [-1] * len(lista_de_adjacencia)  
    valor_minimo_alcancavel = [-1] * len(lista_de_adjacencia)  
    vertices_de_corte = set()  
    tempo = 0  
    pilha = []  
    vertices_isolados = set(range(len(lista_de_adjacencia)))  

    for vertice_inicial in range(len(lista_de_adjacencia)):
        if momento_descoberta[vertice_inicial] == -1:  
            pilha.append((vertice_inicial, None))  

            while pilha:
                u, pai = pilha[-1]  
                if momento_descoberta[u] == -1:
                    momento_descoberta[u] = tempo  
                    valor_minimo_alcancavel[u] = tempo
                    tempo += 1

                filho = 0
                for v in lista_de_adjacencia[u]:
                    if v == pai:
                        continue

                    if momento_descoberta[v] == -1:
                        pilha.append((v, u))  
                        filho += 1

                    valor_minimo_alcancavel[u] = min(valor_minimo_alcancavel[u], momento_descoberta[v])

                if filho == 0 and pai is not None:
                    valor_minimo_alcancavel[pai] = min(valor_minimo_alcancavel[pai], valor_minimo_alcancavel[u])

                todos_filhos_visitados = all(momento_descoberta[v] != -1 for v in lista_de_adjacencia[u])
                if todos_filhos_visitados:
                    pilha.pop()  

                if todos_filhos_visitados and pai is not None and valor_minimo_alcancavel[u] >= momento_descoberta[u]:
                    vertices_de_corte.add(pai)  

    vertices_de_corte_list = list(vertices_de_corte)

    with open("VerticesDeCorte.txt", "w") as f_vertices_de_corte:
        for vertex in vertices_de_corte_list:
            f_vertices_de_corte.write(f"{vertex}\n")

    with open("VerticesIsolados.txt", "w") as f_vertices_isolados:
        for vertex in vertices_de_corte_list:
            f_vertices_isolados.write(f'"{vertex}": [\n')

            isolados = [v for v in vertices_isolados if v != vertex]

            for i, isolado in enumerate(isolados):
                f_vertices_isolados.write(f'    {isolado}')
                if i < len(isolados) - 1:
                    f_vertices_isolados.write(',')
                f_vertices_isolados.write('\n')

            f_vertices_isolados.write(']\n')

    '''  grafico
    G = nx.Graph()
    for u, neighbors in enumerate(lista_de_adjacencia):
        for v in neighbors:
            G.add_edge(u, v)

    node_colors = ['red' if node in vertices_de_corte else 'blue' for node in G.nodes()]

    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
    plt.title('Graph Visualization')
    plt.show()

    '''
   

print("Iniciando a análise do grafo...")
encontrar_vertices_de_corte(lista_de_adjacencia)
