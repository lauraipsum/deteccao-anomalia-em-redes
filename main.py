from data.data_read import criar_lista_de_adjacencia

lista_de_adjacencia = criar_lista_de_adjacencia()

def encontrar_vertices_de_corte(lista_de_adjacencia):

    momento_descoberta = [-1] * len(lista_de_adjacencia)  # momento de descoberta de cada vértice
    valor_minimo_alcancavel = [-1] * len(lista_de_adjacencia)  # valor "valor_minimo_alcancavel" de cada vértice
    vertices_de_corte = set()  # conjunto para armazenar os vértices de corte encontrados
    tempo = 0  # contador para atribuir valores de tempo de descoberta
    pilha = []  # pilha para implementar a busca em profundidade (DFS)

    for vertice_inicial in range(len(lista_de_adjacencia)):
        if momento_descoberta[vertice_inicial] == -1:  # verifica se o vértice de início ainda não foi descoberto
            pilha.append((vertice_inicial, None))  # se não tiver sido descoberto, adiciona à pilha para iniciar uma nova busca em profundidade

            while pilha:
                u, pai = pilha[-1]  # pega o vértice no topo da pilha e seu vértice pai
                if momento_descoberta[u] == -1:
                    momento_descoberta[u] = tempo  # registra o tempo de descoberta para o vértice
                    valor_minimo_alcancavel[u] = tempo
                    tempo += 1

                filho = 0
                for v in lista_de_adjacencia[u]:
                    if v == pai:
                        continue

                    if momento_descoberta[v] == -1:
                        pilha.append((v, u))  # adiciona os vizinhos não visitados à pilha
                        filho += 1

                    valor_minimo_alcancavel[u] = min(valor_minimo_alcancavel[u], momento_descoberta[v])  # atualiza o valor "valor_minimo_alcancavel" do vértice atual

                if filho == 0 and pai is not None:
                    valor_minimo_alcancavel[pai] = min(valor_minimo_alcancavel[pai], valor_minimo_alcancavel[u])  # atualiza o valor "valor_minimo_alcancavel" do pai (se necessário)

                todos_filhos_visitados = all(momento_descoberta[v] != -1 for v in lista_de_adjacencia[u])
                if todos_filhos_visitados:
                    pilha.pop()  # remove o vértice atual da pilha se todos os vizinhos foram visitados

                if todos_filhos_visitados and pai is not None and valor_minimo_alcancavel[u] >= momento_descoberta[u]:
                    vertices_de_corte.add(pai)  # se a condição for atendida, o vértice pai é um vértice de corte

    with open("VerticesDeCorte.txt", "w") as f_vertices_de_corte:
        for vertex in vertices_de_corte:
            f_vertices_de_corte.write(f"{vertex}\n")

print("Iniciando a análise do grafo...")
encontrar_vertices_de_corte(lista_de_adjacencia)
