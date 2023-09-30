import networkx as nx
import matplotlib.pyplot as plt
from data.data_read import criar_lista_de_adjacencia

lista_de_adjacencia = criar_lista_de_adjacencia()

def encontrar_vertices_de_corte(lista_de_adjacencia):
    #print(lista_de_adjacencia)

    momento_descoberta = [-1] * len(lista_de_adjacencia)  # momento de descoberta de cada vértice
    valor_minimo_alcancavel = [-1] * len(lista_de_adjacencia)  # valor "valor_minimo_alcancavel" de cada vértice
    vertices_de_corte = set()  # conjunto para armazenar os vértices de corte encontrados
    tempo = 0  # contador para atribuir valores de tempo de descoberta
    pilha = []  # pilha para implementar a busca em profundidade (DFS)
    vertices_isolados = set(range(len(lista_de_adjacencia)))  # conjunto para armazenar todos os vértices como isolados inicialmente

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

                if valor_minimo_alcancavel[v] >= momento_descoberta[u] and pai is not None:
                    vertices_de_corte.add(u)

            elif v != pai:
                valor_minimo_alcancavel[u] = min(valor_minimo_alcancavel[u], momento_descoberta[v])

        if filho == 0 and pai is not None:
            valor_minimo_alcancavel[pai] = min(valor_minimo_alcancavel[pai], valor_minimo_alcancavel[u])

    for vertice_inicial in range(len(lista_de_adjacencia)):
        if momento_descoberta[vertice_inicial] == -1:
            dfs(vertice_inicial, None)


    '''
    for vertex in vertices_de_corte:
        vertices_isolados.discard(vertex)
        print(vertices_isolados)
    '''

    
    vertices_de_corte_list = list(vertices_de_corte)

    with open("VerticesDeCorte.txt", "w") as f_vertices_de_corte:
        for vertex in vertices_de_corte_list:
            f_vertices_de_corte.write(f"{vertex}\n")
            print(f"Vértice de corte: {vertex}")

    with open("VerticesIsolados.txt", "w") as f_vertices_isolados:
        for vertex in vertices_de_corte_list:
            f_vertices_isolados.write(f'"{vertex}": [\n')

            isolados = [v for v in vertices_isolados if v != vertex]
            visited = set()

            while isolados:
                subgraph = set()
                stack = [isolados[0]]

                while stack:
                    v = stack.pop()
                    subgraph.add(v)
                    visited.add(v)

                    for neighbor in lista_de_adjacencia[v]:
                        if neighbor in isolados and neighbor not in visited:
                            stack.append(neighbor)

                isolados = [v for v in isolados if v not in subgraph]
                f_vertices_isolados.write(f'    {subgraph}')
                if isolados:
                    f_vertices_isolados.write(',')

                f_vertices_isolados.write('\n')

            f_vertices_isolados.write(']\n')


    G = nx.DiGraph()  # Crie um grafo direcionado

    # Adicione nós ao grafo
    for i in range(len(lista_de_adjacencia)):
        G.add_node(i)

    # Adicione arestas direcionadas com base nas informações da lista de adjacência
    for u, neighbors in enumerate(lista_de_adjacencia):
        for v in neighbors:
            G.add_edge(u, v)

    node_colors = ['red' if node in vertices_de_corte else 'blue' for node in G.nodes()]

    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
    plt.title('Graph Visualization')
    plt.show()
    

print("Iniciando a análise do grafo...")
print(lista_de_adjacencia)
vertices_de_corte = encontrar_vertices_de_corte(lista_de_adjacencia)

subgrafos = encontrar_subgrafos_apos_remocao(vertices_de_corte, lista_de_adjacencia)

G = nx.Graph()
for u, neighbors in enumerate(lista_de_adjacencia):
    for v in neighbors:
        G.add_edge(u, v)


plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42) 
nx.draw(G, pos, with_labels=True, node_size=200, node_color='lightblue', font_size=10, font_color='black')
plt.title("Grafo original")
plt.show(block=True) 

for i, (vertice_de_corte, subgrafo) in enumerate(subgrafos):
    print(f"Subgrafo {i + 1} (removendo vértice de corte {vertice_de_corte}):")
    for j, componente in enumerate(subgrafo):
        print(f"Componente {j + 1}:", componente)
        
        subgraph_G = G.subgraph(componente) 
        plt.figure(figsize=(8, 6))
        nx.draw(
            subgraph_G,
            pos,
            with_labels=True,
            node_size=200,
            node_color='lightblue',
            font_size=10,
            font_color='black'
        )
        plt.title(f"Subgraph {i + 1} - Component {j + 1}")
        plt.show(block=True) 

plt.show()



