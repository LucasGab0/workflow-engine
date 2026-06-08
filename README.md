[README.md]
# workflow-engine# Workflow Engine — Orquestrador de Agentes Autônomos

> **Projeto 2** — Disciplina de Estruturas de Dados e Algoritmos

## Membros da Equipe

| Nome | GitHub |
|------|--------|
| Lucas Gabriel Brasileiro Da Silva | @LucasGab0 |
| Marco Valerio | @Wichmann24 |

---

## Sobre o Projeto

Motor de execução responsável por resolver a **ordem correta** em que milhares de tarefas dependentes devem ser executadas, detectando deadlocks e priorizando tarefas urgentes.

### Requisitos Funcionais Implementados

| RF | Estrutura | Arquivo |
|----|-----------|---------|
| RF01 | Grafo Direcionado — Lista de Adjacência | `src/graph.py` |
| RF02 | Ordenação Topológica — Algoritmo de Kahn | `src/topological_sort.py` |
| RF03 | DFS — Detecção de Ciclos (coloração 3-estados) | `src/cycle_detector.py` |
| RF04 | Fila de Prioridade — Max-Heap manual | `src/max_heap.py` |

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa (biblioteca padrão apenas)

---

## Como Executar

### Opção 1 — Script automatizado (recomendado)

```bash
# Dar permissão de execução
chmod +x run.sh

# Gerar dados E executar todos os cenários
./run.sh all

# Apenas gerar os arquivos de teste
./run.sh generate

# Executar cenário específico
./run.sh basico
./run.sh avancado
./run.sh estresse
```

### Opção 2 — Execução manual

```bash
# 1. Gerar arquivos de teste
python src/generate_data.py

# 2. Executar o engine
python src/main.py data/input_basico.json   data/output_basico.json
python src/main.py data/input_avancado.json data/output_avancado.json
python src/main.py data/input_estresse.json data/output_estresse.json
```

---

## Estrutura do Repositório

```
/
├── src/
│   ├── main.py               # Orquestrador principal (CLI)
│   ├── graph.py              # RF01: Grafo Direcionado
│   ├── cycle_detector.py     # RF03: DFS + Detecção de Ciclos
│   ├── topological_sort.py   # RF02: Ordenação Topológica (Kahn)
│   ├── max_heap.py           # RF04: Max-Heap (Fila de Prioridade)
│   └── generate_data.py      # Gerador automático de dados de teste
├── data/
│   ├── input_basico.json     # 10 tarefas, cadeia linear
│   ├── input_avancado.json   # 37 tarefas, edge cases + ciclo
│   └── input_estresse.json   # 10.000 tarefas, 25.020 dependências
├── docs/
│   └── documentacao_tecnica.md
├── run.sh
└── README.md
```

---

## Formato de Entrada

```json
{
  "tasks": [
    { "id": "task_000001", "name": "Processar Pagamento", "urgency": 9 }
  ],
  "dependencies": [
    { "from": "task_000002", "to": "task_000001" }
  ]
}
```

> `"from"` depende de `"to"` → `"to"` é executada **antes**.

---

## Prova de Carga (Estresse)

| Métrica | Resultado |
|---------|-----------|
| Tarefas | 10.000 |
| Dependências | 25.020 |
| Ciclo profundo oculto | 20 nós |
| Tempo de execução | **< 0,2 segundos** |
| Ciclo detectado corretamente | ✅ Sim |
| Estouro de memória | ✅ Não |

---

## Complexidade Assintótica

| Módulo | Complexidade |
|--------|-------------|
| Grafo (inserção) | O(1) amortizado |
| DFS detecção de ciclos | **O(V + E)** |
| Ordenação Topológica (Kahn) | O(V + E) |
| Max-Heap insert/extract | **O(log N)** |
| **Pipeline completo** | **O((V + E) · log V)** |

---

## Bibliotecas Utilizadas

| Biblioteca | Finalidade | Permitida? |
|------------|------------|------------|
| `json` | Leitura/escrita de arquivos | ✅ Stdlib |
| `random` | Geração de dados sintéticos | ✅ Apenas no gerador |
| `os`, `sys` | I/O e paths | ✅ Stdlib |

> **Nenhuma** biblioteca de grafos, heaps ou ordenação foi utilizada no núcleo do sistema.

---

## Documentação Técnica Completa

Ver [`docs/documentacao_tecnica.md`](docs/documentacao_tecnica.md)
