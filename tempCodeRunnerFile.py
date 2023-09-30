    for vertex in vertices_de_corte_list:
            f_vertices_isolados.write(f'"{vertex}": [\n')

            isolados = [v for v in vertices_isolados if v != vertex]

            while isolados:
                combined_sets = set()
                for s in isolados:
                    combined_sets |= s
                isolados = [s for s in isolados if s != combined_sets]

                f_vertices_isolados.write(f'    {list(combined_sets)}')
                if isolados:
                    f_vertices_isolados.write(',')

                f_vertices_isolados.write('\n')

            f_vertices_isolados.write(']\n')
