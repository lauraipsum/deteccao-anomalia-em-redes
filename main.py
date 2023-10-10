import copy
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from data.data_read import criar_lista_de_adjacencia

def encontrar_vertices_de_corte(lista_de_adjacencia):
    momento_descoberta = [-1] * len(lista_de_adjacencia)
    valor_minimo_alcancavel = [-1] * len(lista_de_adjacencia)
    vertices_de_corte = set()
    tempo = 0
    pilha = []

    def dfs(u, pai):
        nonlocal tempo
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
                dfs(v, u)
                valor_minimo_alcancavel[u] = min(valor_minimo_alcancavel[u], valor_minimo_alcancavel[v])

                if valor_minimo_alcancavel[v] >= momento_descoberta[u]:
                    vertices_de_corte.add(u)

            elif v != pai:
                valor_minimo_alcancavel[u] = min(valor_minimo_alcancavel[u], momento_descoberta[v])

        if filho == 0 and pai is not None:
            valor_minimo_alcancavel[pai] = min(valor_minimo_alcancavel[pai], valor_minimo_alcancavel[u])

    for vertice_inicial in range(len(lista_de_adjacencia)):
        if momento_descoberta[vertice_inicial] == -1:
            dfs(vertice_inicial, None)

    return vertices_de_corte

def lista_adjacencia_para_arestas(lista_de_adjacencia):
    arestas = []
    #print(lista_de_adjacencia)
    for u, vizinhos in enumerate(lista_de_adjacencia):
        for v in vizinhos:
            arestas.append((u, v))
    print (arestas)
    return arestas

#removido pois a solução abaixo dela faz o serviçp de forma correta o erro anteriror e justamente no ato da impressão 
# def encontrar_subgrafos_apos_remocao(vertices_de_corte, lista_de_adjacencia):
#     def dfs(u, visited):
#         visited[u] = True
#         componente_conectada.add(u)
#         for v in lista_de_adjacencia[u]:
#             if not visited[v]:
#                 dfs(v, visited)

#     subgrafos = []
#     arestas_original = lista_adjacencia_para_arestas(lista_de_adjacencia)

#     for vertice_de_corte in vertices_de_corte:
#         copia_lista_adjacencia = copy.deepcopy(lista_de_adjacencia)
#         copia_lista_adjacencia[vertice_de_corte] = []  # remove o vértice de corte e suas arestas
#         arestas_subgrafo = lista_adjacencia_para_arestas(copia_lista_adjacencia)

#         # inicializa as estruturas para encontrar as componentes conectadas
#         visited = [False] * len(lista_de_adjacencia)
#         subgrafo = {}
#         componentes = []

#         for u in range(len(lista_de_adjacencia)):
#             if not visited[u]:
#                 componente_conectada = set()
#                 dfs(u, visited)
#                 componentes.append(componente_conectada)

#         # remove o vértice de corte dos componentes
#         for componente in componentes:
#             componente.discard(vertice_de_corte)

#         # cria o subgrafo
#         for aresta in arestas_subgrafo:
#             u, v = aresta
#             if u in componente_conectada and v in componente_conectada:
#                 subgrafo.setdefault(u, []).append(v)
#                 subgrafo.setdefault(v, []).append(u)
#         #aparentemente o componenete abaixo "subgrafo esta tendo um papel meio inutil a ser passado para a frente"
#         #print("aqui", subgrafo)
#         #print("aqui2", componentes)
#         subgrafos.append((vertice_de_corte, subgrafo, componentes))

#     return subgrafos

def encontrar_subgrafos_apos_remocao(vertices_de_corte, lista_de_adjacencia):
    def dfs(u, visited):
        visited[u] = True
        componente_original.append(u)
        for v in lista_de_adjacencia[u]:
            if not visited[v]:
                dfs(v, visited)

    subgrafos = []
    arestas_original = lista_adjacencia_para_arestas(lista_de_adjacencia)

    for vertice_de_corte in vertices_de_corte:
        copia_lista_adjacencia = copy.deepcopy(lista_de_adjacencia)
        copia_lista_adjacencia[vertice_de_corte] = []  # remove o vértice de corte e suas arestas
        arestas_subgrafo = lista_adjacencia_para_arestas(copia_lista_adjacencia)

        # inicializa as estruturas para encontrar as componentes conectadas
        visited = [False] * len(lista_de_adjacencia)
        subgrafo = {}
        componentes = []

        for u in range(len(lista_de_adjacencia)):
            if not visited[u]:
                componente_original = []
                dfs(u, visited)
                if any(v in vertices_de_corte for v in componente_original):
                    componentes.append(componente_original)

        # remove o vértice de corte dos componentes
        for componente in componentes:
            componente.remove(vertice_de_corte)

        # cria o subgrafo
        for aresta in arestas_subgrafo:
            u, v = aresta
            if u in componente_original and v in componente_original:
                subgrafo.setdefault(u, []).append(v)
                subgrafo.setdefault(v, []).append(u)

        subgrafos.append((vertice_de_corte, subgrafo, componentes))

    return subgrafos

                
def escrever_subgrafos(subgrafos, lista_de_adjacencia):
    #print("aqui1", subgrafos)
    with open("Subgrafos.txt", "w") as f_subgrafos:
        for i, (vertice_de_corte, subgrafo, componentes) in enumerate(subgrafos):
            f_subgrafos.write(f"Subgrafo {i + 1} (Removido o vertice de corte {vertice_de_corte}):\n")
            for j, componente in enumerate(componentes, start=1):
                #print(j)
                f_subgrafos.write(f"Componente {j}:\n")
                f_subgrafos.write("[\n")

                vertices_isolados = set(componente)
                visited = set()
                #print(vertices_isolados, " i\n")
                while vertices_isolados:
                    subgraph = set()
                    stack = [next(iter(vertices_isolados))]

                    while stack:
                        v = stack.pop()
                        subgraph.add(v)
                        visited.add(v)

                        for neighbor in lista_de_adjacencia[v]:
                            if neighbor in vertices_isolados and neighbor not in visited:
                                stack.append(neighbor)

                    vertices_isolados -= subgraph
                    f_subgrafos.write("    " + str(list(subgraph)) + ",\n")

                f_subgrafos.write("]\n")
                
def plotar_grafo_com_vertices_de_corte(grafo, vertices_de_corte):
    print(grafo)
    pos = nx.spring_layout(grafo)
    
    vertices_normais = set(grafo.nodes()) - set(vertices_de_corte)
    
    nx.draw_networkx_nodes(grafo, pos, nodelist=vertices_normais, node_color='c', node_size=300)
    
    nx.draw_networkx_nodes(grafo, pos, nodelist=vertices_de_corte, node_color='r', node_size=300)
    
    nx.draw_networkx_edges(grafo, pos)

    labels = {v: v for v in grafo.nodes()}
    nx.draw_networkx_labels(grafo, pos, labels=labels)

    plt.show()
    
def main():
    print("Iniciando a análise do grafo...")
    
    lista_de_adjacencia = criar_lista_de_adjacencia()
    
    vertices_de_corte = encontrar_vertices_de_corte(lista_de_adjacencia)
   
    with open("VerticesDeCorte.txt", "w") as f_vertices_de_corte:
        for vertex in vertices_de_corte:
            f_vertices_de_corte.write(f"Vertice de corte: {vertex}\n")

    subgrafos = encontrar_subgrafos_apos_remocao(vertices_de_corte, lista_de_adjacencia)
    
    escrever_subgrafos(subgrafos, lista_de_adjacencia)
    
    grafo = nx.DiGraph(lista_adjacencia_para_arestas(lista_de_adjacencia))
    plotar_grafo_com_vertices_de_corte(grafo, vertices_de_corte)

if __name__ == "__main__":
    main()
