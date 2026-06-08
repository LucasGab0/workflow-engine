[documentacao_tecnica.md](https://github.com/user-attachments/files/28727012/documentacao_tecnica.md)
# Documentação Técnica — Workflow Engine

## Visão Geral

O **Workflow Engine** é um motor de execução responsável por resolver a ordem em que milhares de tarefas dependentes devem ser executadas. Todas as estruturas de dados e algoritmos foram implementados **manualmente**, sem uso de bibliotecas de alto nível.

---

## Arquitetura do Sistema

```
/src
  ├── graph.py            # RF01 — Grafo Direcionado (Lista de Adjacência)
  ├── cycle_detector.py   # RF03 — DFS para detecção de ciclos
  ├── topological_sort.py # RF02 — Ordenação Topológica (Kahn + Max-Heap)
  ├── max_heap.py         # RF04 — Fila de Prioridade (Max-Heap manual)
  ├── main.py             # Orquestrador principal (CLI)
  └── generate_data.py    # Gerador automático dos arquivos de teste
```

---

## Estruturas de Dados Implementadas

### RF01 — Grafo Direcionado com Lista de Adjacência

**Arquivo:** `graph.py`

**Justificativa de escolha:**
- Lista de Adjacência é preferível à Matriz de Adjacência quando o grafo é **esparso** (E << V²).
- No pior caso do nosso cenário de estresse: 10.000 nós e 25.000 arestas → densidade de apenas 0,025%.
- Matriz de Adjacência exigiria 10.000² = 100.000.000 de células → inviável em memória.

**Complexidade:**
| Operação | Lista de Adjacência | Matriz de Adjacência |
|---|---|---|
| Adicionar nó | O(1) | O(V²) (resize) |
| Adicionar aresta | O(1) | O(1) |
| Iterar vizinhos | O(grau(v)) | O(V) |
| Espaço | **O(V + E)** | O(V²) |

---

### RF04 — Max-Heap (Fila de Prioridade)

**Arquivo:** `max_heap.py`

**Implementação:** Array com sift_up e sift_down manuais.

**Propriedade do Heap:** `heap[pai] >= heap[filho]` para todo índice.

**Índices:**
```
pai(i)    = (i - 1) // 2
esquerdo  = 2*i + 1
direito   = 2*i + 2
```

**Complexidade:**
| Operação | Complexidade |
|---|---|
| `push` (insert) | **O(log N)** |
| `pop` (extract_max) | **O(log N)** |
| `peek` (máximo) | **O(1)** |
| Build heap | O(N) |

---

### RF03 — DFS com Detecção de Ciclos (Coloração 3-estados)

**Arquivo:** `cycle_detector.py`

**Algoritmo de coloração:**
- `WHITE` — nó ainda não visitado
- `GRAY` — nó em progresso (está na pilha de chamadas atual)
- `BLACK` — nó completamente processado

**Lógica:**
> Se ao explorar os vizinhos de um nó GRAY encontramos outro nó GRAY, existe uma **back edge** — ou seja, estamos voltando para um ancestral na árvore DFS. Isso caracteriza um ciclo.

**Complexidade:** O(V + E) — cada nó e aresta são visitados exatamente uma vez.

**Por que prevenir ciclos?**
Em um sistema de execução de tarefas, um ciclo de dependências representa um **deadlock**: A depende de B, B depende de C, C depende de A — nenhuma tarefa pode ser iniciada.

---

### RF02 — Ordenação Topológica (Algoritmo de Kahn)

**Arquivo:** `topological_sort.py`

**Algoritmo de Kahn (baseado em in-degree):**
1. Calcula o `in-degree` de todos os nós.
2. Insere na Max-Heap todos os nós com `in-degree = 0` (sem dependências pendentes).
3. Enquanto a heap não estiver vazia:
   - Extrai o nó de **maior urgência** (Max-Heap).
   - Adiciona à sequência de execução.
   - Para cada vizinho: decrementa `in-degree`. Se chegar a 0, insere na heap.
4. Se a sequência final for menor que V → ciclo detectado → execução abortada.

**Integração RF02 + RF04:**
A substituição da fila FIFO pela **Max-Heap** garante que, entre todas as tarefas prontas para execução (sem dependências pendentes), sempre seja escolhida a de **maior urgência** — alinhando a Ordenação Topológica com o requisito da Fila de Prioridade.

**Complexidade:** O((V + E) · log V)
- O(V + E) iterações pelo grafo
- O(log V) por operação de heap

---

## Formato de Entrada (input.json)

```json
{
  "tasks": [
    {
      "id": "task_000001",
      "name": "Processar Pagamento",
      "urgency": 9,
      "description": "Valida e processa o pagamento"
    }
  ],
  "dependencies": [
    {
      "from": "task_000002",
      "to": "task_000001"
    }
  ]
}
```

> **Convenção:** `"from"` depende de `"to"`. Ou seja: `"to"` deve ser executada **antes** de `"from"`.

---

## Formato de Saída (output.json)

```json
{
  "summary": {
    "total_tasks": 10000,
    "total_dependencies": 25020,
    "nodes_in_graph": 10000,
    "edges_in_graph": 25020
  },
  "cycle_detection": {
    "has_cycle": true,
    "total_cycles_found": 1,
    "cycles": [
      { "nodes": ["task_009980", "task_009981", "...", "task_009980"] }
    ]
  },
  "topological_sort": {
    "success": false,
    "tasks_scheduled": 9980,
    "execution_order": ["task_000000", "..."],
    "error": "Ordenação topológica incompleta: ciclo detectado."
  }
}
```

---

## Prova de Carga — Teste de Estresse

| Métrica | Valor |
|---|---|
| Tarefas | 10.000 |
| Dependências | 25.020 |
| Ciclo oculto | 20 nós de profundidade |
| Tempo de execução | **< 0,2 segundos** |
| Uso de memória | ~30 MB |
| Nós detectados no ciclo | 20 (100% de precisão) |

**Conclusão:** O sistema processa o cenário de estresse dentro dos limites de tempo e memória esperados para complexidade O((V + E) · log V).

---

## Restrições Respeitadas

- ✅ Nenhuma biblioteca de grafos utilizada (`networkx` proibido)
- ✅ Nenhum `heapq` do Python utilizado (heap manual)
- ✅ Nenhuma estrutura de ordenação da stdlib (`sorted`, `list.sort` proibidos no core)
- ✅ Código processado dinamicamente — sem hardcode de saída
- ✅ Entrada e saída via arquivos JSON padronizados
