"""
RF02 — Ordenação Topológica (Algoritmo de Kahn)
Determina a sequência linear exata de execução das tarefas.
"""

from graph import Graph
from max_heap import MaxHeap


def topological_sort(graph: Graph, tasks_meta: dict) -> dict:
    """
    Ordenação Topológica usando o Algoritmo de Kahn (BFS por in-degree).

    Integração com RF04 (Fila de Prioridade / Max-Heap):
        - Em vez de usar uma fila simples (FIFO), usamos a Max-Heap para sempre
          processar primeiro a tarefa com MAIOR urgência dentre as que estão
          prontas (in-degree == 0).

    Algoritmo:
        1. Calcular in-degree de todos os nós.
        2. Inserir nós com in-degree=0 na Max-Heap (tarefas sem dependências).
        3. Enquanto a heap não estiver vazia:
            a. Extrair a tarefa de maior urgência.
            b. Adicioná-la à sequência de execução.
            c. Para cada vizinho, decrementar in-degree.
            d. Se in-degree do vizinho chegar a 0, inserir na heap.
        4. Se a sequência final tiver menos nós que o grafo → há ciclo.

    Complexidade: O((V + E) * log V)
        - O(V + E) para percorrer o grafo
        - O(log V) por operação de heap (insert/extract)

    Retorna:
        {
            "success": bool,
            "execution_order": [lista de task_ids em ordem de execução],
            "error": str (apenas se success=False)
        }
    """
    # Copia do in-degree para não modificar o grafo original
    in_degree_copy = {node: graph.get_in_degree(node) for node in graph.get_all_nodes()}

    heap = MaxHeap()

    # Inicializa a heap com todas as tarefas sem dependência
    for node in graph.get_all_nodes():
        if in_degree_copy[node] == 0:
            urgency = tasks_meta.get(node, {}).get("urgency", 0)
            # Negamos urgency para usar Max-Heap como ordenador de maior urgência
            heap.push(urgency, node, urgency)

    execution_order = []

    while not heap.is_empty():
        priority, task_id, urgency = heap.pop()
        execution_order.append(task_id)

        for neighbor in graph.get_neighbors(task_id):
            in_degree_copy[neighbor] -= 1
            if in_degree_copy[neighbor] == 0:
                neighbor_urgency = tasks_meta.get(neighbor, {}).get("urgency", 0)
                heap.push(neighbor_urgency, neighbor, neighbor_urgency)

    total_nodes = graph.node_count

    if len(execution_order) < total_nodes:
        return {
            "success": False,
            "execution_order": execution_order,
            "error": (
                f"Ordenação topológica incompleta: {len(execution_order)}/{total_nodes} "
                f"tarefas processadas. Ciclo detectado no grafo — abortando execução."
            )
        }

    return {
        "success": True,
        "execution_order": execution_order,
        "error": None
    }
