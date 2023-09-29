def criar_lista_de_adjacencia():
    lista_de_adjacencia = []

    with open("./data/teste2.txt", "r") as file:
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

        while len(lista_de_adjacencia) <= max(from_node, to_node):
            lista_de_adjacencia.append([])

        if relationship == 0:
            # Relação bidirecional para peer to peer
            lista_de_adjacencia[from_node].append(to_node)
            lista_de_adjacencia[to_node].append(from_node)
        elif relationship == 1:
            # Relação de provedor (from_node -> to_node)
            lista_de_adjacencia[from_node].append(to_node)
        elif relationship == -1:
            # Relação de cliente (from_node <- to_node)
            lista_de_adjacencia[to_node].append(from_node)
        elif relationship == 2:
            # Relação sibling-to-sibling, não tem uma direção específica
            lista_de_adjacencia[from_node].append(to_node)
            lista_de_adjacencia[to_node].append(from_node)

    return lista_de_adjacencia
