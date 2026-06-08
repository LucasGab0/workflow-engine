"""
RF01 — Grafo Direcionado com Lista de Adjacência
Modela dependências entre tarefas.
"""


class Graph:
    """
    Grafo Direcionado implementado com Lista de Adjacência (dicionário de listas).
    Complexidade:
        - Inserção de nó/aresta: O(1) amortizado
        - Iteração sobre vizinhos: O(grau do nó)
        - Espaço: O(V + E)
    """

    def __init__(self):
        # adjacency[u] = lista de nós v tal que existe aresta u -> v
        self.adjacency = {}
        # in_degree[v] = quantidade de arestas que chegam em v
        self.in_degree = {}
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node_id: str):
        if node_id not in self.adjacency:
            self.adjacency[node_id] = []
            self.in_degree[node_id] = 0
            self.node_count += 1

    def add_edge(self, from_node: str, to_node: str):
        """Adiciona aresta direcionada: from_node -> to_node (from depende de to)."""
        self.add_node(from_node)
        self.add_node(to_node)
        self.adjacency[from_node].append(to_node)
        self.in_degree[to_node] += 1
        self.edge_count += 1

    def get_neighbors(self, node_id: str):
        return self.adjacency.get(node_id, [])

    def get_all_nodes(self):
        return list(self.adjacency.keys())

    def get_in_degree(self, node_id: str) -> int:
        return self.in_degree.get(node_id, 0)
