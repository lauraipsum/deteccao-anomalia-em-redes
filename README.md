# Detecção de pontos críticos em rede

  Detecção de todas as arestas de corte em uma rede indicando pontos criticos de falha, ou seja, pontos na rede que, se falharem, isolam parte da rede, e identificação de quais pontos ficariam isolados em consequencia da indisponibilidade de tais pontos críticos. 

#  `data_read.py`

O módulo `data_read.py` é responsável por ler dados de um arquivo de entrada e criar uma lista de adjacência que representa um grafo. 
As relações podem ser de diferentes tipos, como bidirecional, de provedor, de cliente ou sibling-to-sibling.

#  `main.py`

O módulo `main.py` é o ponto de entrada do programa e realiza uma série de análises em um grafo representado pela lista de adjacência gerada pelo módulo `data_read.py`. 

- É chamada a função `criar_lista_de_adjacencia` do módulo `data_read.py` para obter a lista de adjacência que representa o grafo.

- Em seguida,  é chamada a função  `encontrar_vertices_de_corte`  para identificar os vértices de corte no grafo.
	-	O código começa pela função `encontrar_vertices_de_corte`, que usa o algoritmo de busca em profundidade (DFS) para encontrar vértices de corte em um grafo.
	-	Inicializa listas `momento_descoberta` e `valor_minimo_alcancavel` para acompanhar o momento de descoberta de cada vértice e o valor mínimo alcançável a partir dele.
	- `tempo` é uma variável que é incrementada a cada vez que um vértice é descoberto, para rastrear o tempo de descoberta.
	-  `pilha` é uma pilha que mantém os pares `(v, u)` de vértices adjacentes, onde `u` é o pai de `v` na busca em profundidade.
	-  A função `dfs(u, pai)` realiza a busca em profundidade a partir do vértice `u`, onde `pai` é o vértice pai de `u` na busca.
	-  Para cada vértice `v` adjacente a `u`:
		-   Se `v` não foi descoberto (`momento_descoberta[v] == -1`), o algoritmo o empilha na pilha e atualiza o valor mínimo alcançável de `u`.
		-   Se `v` já foi descoberto, o algoritmo atualiza o valor mínimo alcançável de `u` considerando `v`.
		-   Se `v` tiver um valor mínimo alcançável maior ou igual ao momento de descoberta de `u` e `u` não for o vértice inicial da busca, então `u` é um vértice de corte.
		- Quando não há mais filhos para explorar ou quando a busca termina, o algoritmo atualiza o valor mínimo alcançável do pai de `u`, se aplicável.
	-  A função percorre todos os vértices iniciais não descobertos para encontrar os vértices de corte.
  
- Em seguida, os vértices de corte são escritos em um arquivo chamado "VerticesDeCorte.txt".

- Identifica-se os subgrafos que resultam da remoção dos vértices de corte usando a função `encontrar_subgrafos_apos_remocao`.
	-  A função `encontrar_subgrafos_apos_remocao` recebe a lista de vértices de corte e a lista de adjacência original.
	-  Ela cria cópias da lista de adjacência, remove o vértice de corte e suas arestas dessas cópias.
	-  Em seguida, cria um subgrafo a partir das arestas da cópia da lista de adjacência.
	-  Encontra os componentes conectados no subgrafo usando `nx.connected_components`.
	-  Remove o vértice de corte de cada componente.
	-  Armazena as informações do vértice de corte, subgrafo e componentes em uma lista `subgrafos`.

-  Os subgrafos são escritos em um arquivo chamado "Subgrafos.txt".


Ambos os módulos trabalham juntos para analisar e representar informações sobre o grafo a partir dos dados de entrada fornecidos.
