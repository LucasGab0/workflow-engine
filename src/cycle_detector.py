"""
RF03 — Busca em Profundidade (DFS) para Detecção de Ciclos
Previne deadlocks antes de iniciar a execução.
"""

from graph import Graph


def detect_cycles(graph: Graph) -> dict:
    """
    Detecta ciclos em um grafo direcionado usando DFS com coloração de nós.

    Estados de cor:
        WHITE (0) = não visitado
        GRAY  (1) = visitado nesta chamada recursiva (em progresso)
        BLACK (2) = totalmente processado

    Um ciclo existe se encontrarmos uma aresta de um nó GRAY para outro GRAY
    (back edge — aresta de retorno).

    Complexidade: O(V + E)

    Retorna:
        {
            "has_cycle": bool,
            "cycles": [[lista de nós que formam cada ciclo]]
        }
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph.get_all_nodes()}
    # Mantém o caminho atual para reconstruir o ciclo
    path = []
    path_set = set()
    cycles_found = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        path_set.add(node)

        for neighbor in graph.get_neighbors(node):
            if color[neighbor] == GRAY:
                # Back edge encontrada — ciclo detectado!
                # Reconstrói o ciclo a partir do caminho atual
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles_found.append(cycle)
            elif color[neighbor] == WHITE:
                dfs(neighbor)

        path.pop()
        path_set.discard(node)
        color[node] = BLACK

    for node in graph.get_all_nodes():
        if color[node] == WHITE:
            dfs(node)

    return {
        "has_cycle": len(cycles_found) > 0,
        "cycles": cycles_found
    }
