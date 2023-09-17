from data.data_read import criar_dicionario_de_adjacencia

dicionario_de_adjacencia = criar_dicionario_de_adjacencia()

def encontrar_arestas_de_corte(dicionario_de_adjacencia):

    tempo_descoberta = {node: -1 for node in dicionario_de_adjacencia.keys()}  #    tempo de descoberta de cada vertice
    low = {node: -1 for node in dicionario_de_adjacencia.keys()}  # valor "low" de cada vertice
    arestas_corte = set()  #    conjunto p armazenar as arestas de corte encontradas
    tempo = 0  #   contador p atribuir valores de tempo de descoberta
    pilha = []  #   pilha para implementar a busca em profundidade (DFS)

    for vertice_inicial in dicionario_de_adjacencia.keys():
        if tempo_descoberta[vertice_inicial] == -1:  #  verifica se o vertice de início ainda não foi descoberto
            pilha.append((vertice_inicial, None))  #    se não tiver sido descoberto, adiciona à pilha para iniciar uma nova busca em profundidade

            while pilha:
                u, pai = pilha[-1]  # pega o vertice no topo da pilha e seu vertice pai
                if tempo_descoberta[u] == -1:
                    tempo_descoberta[u] = tempo  # registra o tempo de descoberta para o vertice
                    low[u] = tempo
                    tempo += 1

                filho = 0
                for v in dicionario_de_adjacencia.get(u, []):
                    if v == pai:
                        continue

                    if tempo_descoberta[v] == -1:
                        pilha.append((v, u))  # adiciona os vizinhos não visitados à pilha
                        filho += 1

                    low[u] = min(low[u], tempo_descoberta[v])  # atualiza o valor "low" do vertice atual

                if filho == 0 and pai is not None:
                    low[pai] = min(low[pai], low[u])  # atualiza o valor "low" do pai( se necessário)

                todos_filhos_visitados = all(tempo_descoberta[v] != -1 for v in dicionario_de_adjacencia[u])
                if todos_filhos_visitados:
                    pilha.pop()  # remove o vertice atual da pilha se todos os vizinhos foram visitados

                if todos_filhos_visitados and pai is not None and low[u] >= tempo_descoberta[u]:
                    arestas_corte.add((pai, u))  # se a condição for atendida, a aresta é uma aresta de corte
                    
    with open("ArestasDeCorte.txt", "w") as f_arestas_corte:
        for edge in arestas_corte:
            f_arestas_corte.write(f"{edge[0]} - {edge[1]}\n")

print("Iniciando a análise do grafo...")
encontrar_arestas_de_corte(dicionario_de_adjacencia)
