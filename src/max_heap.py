"""
RF04 — Fila de Prioridade implementada como Max-Heap
Gerencia tarefas prontas para execução ordenadas por urgência.
"""


class MaxHeap:
    """
    Max-Heap implementada manualmente sobre um array.
    A raiz sempre contém o elemento de MAIOR prioridade.

    Complexidade:
        - insert (push): O(log N)
        - extract_max (pop): O(log N)
        - peek: O(1)
        - build_heap: O(N)
    """

    def __init__(self):
        # heap[0] é a raiz (maior prioridade)
        self._data = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _sift_up(self, i: int):
        """Sobe o elemento na posição i até restaurar a propriedade do heap."""
        while i > 0:
            parent = self._parent(i)
            # Compara por prioridade (primeiro campo da tupla)
            if self._data[i][0] > self._data[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i: int):
        """Desce o elemento na posição i até restaurar a propriedade do heap."""
        size = len(self._data)
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)

            if left < size and self._data[left][0] > self._data[largest][0]:
                largest = left

            if right < size and self._data[right][0] > self._data[largest][0]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def push(self, priority: int, task_id: str, urgency: int):
        """
        Insere tarefa na heap.
        Tupla: (priority, task_id, urgency) — Python compara elemento a elemento.
        """
        self._data.append((priority, task_id, urgency))
        self._sift_up(len(self._data) - 1)

    def pop(self) -> tuple:
        """Remove e retorna o elemento de maior prioridade. O(log N)."""
        if self.is_empty():
            raise IndexError("Heap vazia — nenhuma tarefa disponível.")
        # Troca raiz com o último e remove o último
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        if self._data:
            self._sift_down(0)
        return item

    def peek(self) -> tuple:
        """Retorna o elemento de maior prioridade sem remover. O(1)."""
        if self.is_empty():
            raise IndexError("Heap vazia.")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)
