from data.data_read import criar_lista_de_adjacencia

lista_de_adjacencia = criar_lista_de_adjacencia()

def encontrar_vertices_de_corte(lista_de_adjacencia):

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

    for vertex in vertices_de_corte:
        vertices_isolados.discard(vertex)

    with open("VerticesDeCorte.txt", "w") as f_vertices_de_corte:
        for vertex in vertices_de_corte:
            f_vertices_de_corte.write(f"{vertex}\n")
            print(f"Vértice de corte: {vertex}")

    with open("VerticesIsolados.txt", "w") as f_vertices_isolados:
        for vertex in vertices_isolados:
            f_vertices_isolados.write(f"{vertex}\n")

print("Iniciando a análise do grafo...")
print(lista_de_adjacencia)
encontrar_vertices_de_corte(lista_de_adjacencia)
