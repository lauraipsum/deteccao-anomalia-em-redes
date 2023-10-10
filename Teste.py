import copy
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Grafo:
    # Inicializar o grafo
    def __init__(self, direcionado=True):
        self.m_direcionado = direcionado
        self.vertices_qtd = 0
        self.aresta_qtd = 0
        self.grafo = {}
        self.vertices_de_corte = []
        self.aresta_ent_vertices = []
        self.subgrafos_apos_remocao = []

    def representacao_interna(self):
        print("Representação Interna: ", self.grafo)

    # add vértices
    def add_vertices(self, v):
        if v in self.grafo:
            print("Vértice: ", v, "já existe")
        else:
            self.grafo[v] = []
            self.vertices_qtd = self.vertices_qtd + 1

    # add arestas
    def add_arestas(self, v1, v2, peso=1):
        if v1 not in self.grafo:
            print("Vértice ", v1, "não existe")
        elif v2 not in self.grafo:
            print("Vértice ", v2, "não existe")
        else:
            temp = [v2, peso]
            self.grafo[v1].append(temp)
            self.aresta_qtd += 1
            if not self.m_direcionado and v1 != v2:
                temp = [v1, peso]
                self.grafo[v2].append(temp)
    # remover vértices
    def remover_vertice(self, v):
        self.grafo.pop(v)
        for i in self.grafo.keys():
            for j in self.grafo[i]:
                if v in j:
                    self.grafo[i].remove(j)

    # remover arestas
    def remover_aresta(self, a):
        for i in self.grafo.keys():
            for j in self.grafo[i]:
                if a in j:
                    self.grafo[i].remove(j)

    # imprimir lista de adj
    def print_lista_adj(self):
        for vertice in self.grafo:
            print(vertice, end='| ')
            for aresta in self.grafo[vertice]:
                print(" -> ", aresta[0], "Peso: ", aresta[1], end=' ')
            print("")
    
    # Teste de algoritimo - verificar o grau do grafo
    def grau(self, v):
        if v in self.grafo:
            return len(self.grafo[v])
        return 0

    # Existe uma aresta entre os vértices 'u' e 'v'?
    def existe_aresta(self, u, v):
        tof = False
        if (u in self.grafo):
            for valor in self.grafo[u]:
                if (v in valor):
                    tof = True
                    break
            return tof
        
    #ler os dados de entrada
    def lerDados(self, arquivo):
        with open(arquivo, "r") as file:
            lines = file.readlines()

        in_data_section = False

        for line in lines:
            line = line.strip()

            if line.startswith("# FromNodeId"):
                in_data_section = True
                continue

            if not in_data_section:
                continue

            columns = line.split()
            from_node = int(columns[0])
            to_node = int(columns[1])
            relationship = int(columns[2])

            # Verifica se os vértices existem e adiciona-os se necessário
            if from_node not in self.grafo:
                self.add_vertices(from_node)
            if to_node not in self.grafo:
                self.add_vertices(to_node)

            # Adiciona as arestas de acordo com o tipo de relação
            if relationship == 0:
                # Relação bidirecional para peer to peer
                self.add_arestas(from_node, to_node)
                self.add_arestas(to_node, from_node)
            elif relationship == 1:
                # Relação de provedor (from_node -> to_node)
                self.add_arestas(from_node, to_node)
            elif relationship == -1:
                # Relação de cliente (from_node <- to_node)
                self.add_arestas(to_node, from_node)
            elif relationship == 2:
                # Relação sibling-to-sibling, sem direção específica
                self.add_arestas(from_node, to_node)
                self.add_arestas(to_node, from_node)

    #encontra os vertices de corte 
    def encontrarVerticesCorte(self):
        visitados = {}  # Dicionário para manter o controle de quais vértices já foram visitados
        descoberta = {}  # Dicionário para manter o controle dos tempos de descoberta
        baixo = {}  # Dicionário para manter o controle dos tempos de descoberta mais baixos alcançáveis
        pai = {}  # Dicionário para manter o controle dos pais dos vértices na árvore DFS
        tempo = 0  # Inicializa o tempo de descoberta

        #variavel para armazenar os vertices de corte
        vertices_de_corte = set()

        # Inicializa os dicionários
        for vertice in self.grafo.keys():
            visitados[vertice] = False
            descoberta[vertice] = float("inf")
            baixo[vertice] = float("inf")
            pai[vertice] = None

        # Função DFS para encontrar os vértices de corte
        def DFS(u):
            nonlocal tempo
            filhos = 0  # Contador de filhos na árvore DFS

            visitados[u] = True
            descoberta[u] = tempo
            baixo[u] = tempo
            tempo += 1

            for v, _ in self.grafo[u]:
                if not visitados[v]:
                    filhos += 1
                    pai[v] = u

                    DFS(v)

                    # Atualiza o valor 'baixo' de u
                    baixo[u] = min(baixo[u], baixo[v])

                    # Verifica se u é um vértice de corte
                    if pai[u] is None and filhos > 1:
                        #print("Vértice de corte1:", u)
                        vertices_de_corte.add(u)
                    if pai[u] is not None and baixo[v] >= descoberta[u]:
                        #print("Vértice de corte:", u)
                        vertices_de_corte.add(u)
                elif v != pai[u]:
                    baixo[u] = min(baixo[u], descoberta[v])

        # Chama a função DFS a partir de cada vértice não visitado
        for vertice in self.grafo.keys():
            if not visitados[vertice]:
                DFS(vertice)

        self.vertices_de_corte.append(vertices_de_corte)
    
    def lista_adjacencia_para_arestas(self):
        lista_de_arestas = []

        for vertice, arestas in self.grafo.items():
            for destino, peso in arestas:
                if self.m_direcionado:
                    lista_de_arestas.append((vertice, destino))
                else:
                    # Adicione a aresta apenas se não for direcionada para evitar duplicações
                    if (destino, vertice) not in lista_de_arestas:
                        lista_de_arestas.append((vertice, destino))

        self.aresta_ent_vertices = lista_de_arestas

    
    def encontrar_subgrafos_apos_remocao(self):
        subgrafos = []

        for vertice in self.vertices_de_corte[0]:  # Supondo que há apenas um conjunto de vértices de corte
            # Faça uma cópia profunda do grafo original para evitar modificações indesejadas
            grafo_copia = copy.deepcopy(self.grafo)

            # Remova o vértice de corte atual e todas as arestas associadas
            if vertice in grafo_copia:
                grafo_copia.pop(vertice)
            for v in grafo_copia:
                grafo_copia[v] = [aresta for aresta in grafo_copia[v] if aresta[0] != vertice]

            # Encontre os subgrafos conectados após a remoção
            subgrafos_conectados = []
            visitados = set()

            def DFS(u, subgrafo):
                visitados.add(u)
                subgrafo.add(u)

                for v, _ in grafo_copia[u]:
                    if v not in visitados:
                        DFS(v, subgrafo)

            for v in grafo_copia:
                if v not in visitados:
                    subgrafo_atual = set()
                    DFS(v, subgrafo_atual)
                    subgrafos_conectados.append(subgrafo_atual)

            subgrafos.append(subgrafos_conectados)

        self.subgrafos_apos_remocao = subgrafos

    def escrever_subgrafos_e_vertices(self):
        subgrafos = self.subgrafos_apos_remocao
        verticesDeCorte = self.vertices_de_corte
        
        #escreve no arquivo os vertices de corte
        with open("VerticesDeCorte,txt", "w") as f_vertices_de_corte:
            f_vertices_de_corte.write(f"Esses sao os vertices de possivel vunerabilidade na rede de entrada:\n")
            for vertex in verticesDeCorte:
                for vert in vertex:
                    f_vertices_de_corte.write(f"    Vertice de corte: {vert}\n")

        #escreve no arquivo os subgrafos para cada caso de vertice de corte existente na rede 
        with open("Subgrafos.txt", "w") as f_subgrafos:
            f_subgrafos.write(f"Abaixo estao os subgrafos gerados apartoir de cada vertice de corte:\n")
            for i, subgrafos_conectados in enumerate(subgrafos):
                f_subgrafos.write(f"    Subgrafos apos a remocao do vertice {list(g.vertices_de_corte[0])[i]}:\n")
                for subgrafo in subgrafos_conectados:
                    f_subgrafos.write(f"        {subgrafo},\n")
        
    def plotarGrafo(self):
        # Criar um objeto DiGraph
        G = nx.DiGraph()

        # Listas para armazenar vértices normais (azuis) e vértices de corte (vermelhos)
        vertices_normais = []
        vertices_corte = []

        # Adicionar nós e arestas do grafo ao DiGraph
        for vertice, arestas in self.grafo.items():
            G.add_node(vertice)
            if vertice in self.vertices_de_corte[0]:  # Supondo que há apenas um conjunto de vértices de corte
                vertices_corte.append(vertice)
            else:
                vertices_normais.append(vertice)
            for destino, peso in arestas:
                G.add_edge(vertice, destino)

        # Organizar o grafo em formato de árvore usando o layout kamada_kawai
        pos = nx.kamada_kawai_layout(G)

        # Desenhar vértices normais (azuis)
        nx.draw(G, pos, nodelist=vertices_normais, node_color='blue', node_size=300, with_labels=True, font_size=10, font_color='black', arrows=True)

        # Desenhar vértices de corte (vermelhos)
        nx.draw(G, pos, nodelist=vertices_corte, node_color='red', node_size=300, with_labels=True, font_size=10, font_color='black', arrows=True)

        # Exibir o gráfico
        plt.show()


    def start(self):
        self.lerDados("data/camilinho.txt")
        self.encontrarVerticesCorte()
        self.lista_adjacencia_para_arestas()
        self.encontrar_subgrafos_apos_remocao()
        self.escrever_subgrafos_e_vertices()
        self.plotarGrafo()
    

g = Grafo(True)

g.start()



