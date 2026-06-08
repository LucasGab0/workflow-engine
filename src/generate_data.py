"""
Gerador Automático de Dados de Teste
Gera input_basico.json, input_avancado.json e input_estresse.json
com os volumes exigidos pela rubrica.

Uso: python generate_data.py
"""

import json
import random
import uuid
import os


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def gen_task_id(i: int) -> str:
    return f"task_{i:06d}"


def save_json(data: dict, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size_kb = os.path.getsize(path) / 1024
    print(f"  [OK] {filename} — {len(data['tasks'])} tarefas, "
          f"{len(data['dependencies'])} dependências, "
          f"{size_kb:.1f} KB")


# ──────────────────────────────────────────────
# BÁSICO: valida lógica central, sem edge cases
# ──────────────────────────────────────────────
def generate_basico():
    """
    10 tarefas em cadeia linear simples: t0 -> t1 -> t2 -> ... -> t9
    Ordem esperada: t0, t1, ..., t9 (sem ambiguidade)
    """
    n = 10
    tasks = [
        {"id": gen_task_id(i), "name": f"Tarefa {i}", "urgency": n - i, "description": f"Etapa {i}"}
        for i in range(n)
    ]

    deps = []
    for i in range(1, n):
        # task_i depende de task_{i-1}
        deps.append({"from": gen_task_id(i), "to": gen_task_id(i - 1)})

    save_json({"tasks": tasks, "dependencies": deps}, "input_basico.json")


# ──────────────────────────────────────────────
# AVANÇADO: edge cases reais
# ──────────────────────────────────────────────
def generate_avancado():
    """
    Edge cases incluídos:
        1. Nós desconectados (sem dependências)
        2. Dependências duplicadas (devem ser ignoradas pelo motor)
        3. Um ciclo curto: A -> B -> C -> A
        4. Subgrafos independentes em paralelo
    """
    tasks = []
    deps = []
    idx = 0

    # Subgrafo 1: cadeia linear 20 tarefas
    chain_start = idx
    for i in range(chain_start, chain_start + 20):
        tasks.append({"id": gen_task_id(i), "name": f"Chain-{i}", "urgency": random.randint(1, 10)})
        if i > chain_start:
            deps.append({"from": gen_task_id(i), "to": gen_task_id(i - 1)})
    idx += 20

    # Subgrafo 2: árvore binária de dependências (fan-in)
    root = idx
    tasks.append({"id": gen_task_id(root), "name": "Root", "urgency": 10})
    for i in range(root + 1, root + 9):
        tasks.append({"id": gen_task_id(i), "name": f"Leaf-{i}", "urgency": random.randint(1, 5)})
        deps.append({"from": gen_task_id(root), "to": gen_task_id(i)})
    idx = root + 9

    # Nós desconectados (sem deps)
    for i in range(idx, idx + 5):
        tasks.append({"id": gen_task_id(i), "name": f"Isolado-{i}", "urgency": 1})
    idx += 5

    # Dependências duplicadas (edge case)
    deps.append({"from": gen_task_id(1), "to": gen_task_id(0)})  # duplicata
    deps.append({"from": gen_task_id(2), "to": gen_task_id(1)})  # duplicata

    # CICLO: task_idx -> task_idx+1 -> task_idx+2 -> task_idx (ciclo fechado)
    c0, c1, c2 = idx, idx + 1, idx + 2
    tasks.append({"id": gen_task_id(c0), "name": "Ciclo-A", "urgency": 5})
    tasks.append({"id": gen_task_id(c1), "name": "Ciclo-B", "urgency": 5})
    tasks.append({"id": gen_task_id(c2), "name": "Ciclo-C", "urgency": 5})
    deps.append({"from": gen_task_id(c1), "to": gen_task_id(c0)})
    deps.append({"from": gen_task_id(c2), "to": gen_task_id(c1)})
    deps.append({"from": gen_task_id(c0), "to": gen_task_id(c2)})  # fecha o ciclo!

    save_json({"tasks": tasks, "dependencies": deps}, "input_avancado.json")


# ──────────────────────────────────────────────
# ESTRESSE: volumetria mínima da rubrica
# 10.000 tarefas | 25.000 dependências | 1 ciclo profundo oculto
# ──────────────────────────────────────────────
def generate_estresse():
    """
    Estratégia de geração:
        - 9.980 tarefas organizadas em 200 subgrafos do tipo DAG aleatório
        - Cada subgrafo tem ~50 nós e ~120 arestas internas
        - 20 tarefas reservadas para o CICLO PROFUNDO OCULTO
        - Total final: >= 10.000 tarefas, >= 25.000 dependências
    """
    random.seed(42)  # seed fixa = resultados reprodutíveis
    tasks = []
    deps_set = set()  # evita duplicatas
    deps = []

    N_TASKS = 10_000
    N_SUBGRAPHS = 200
    TASKS_PER_SUBGRAPH = 49   # 200 * 49 = 9.800 + 20 ciclo = 9.820 (completamos abaixo)
    EXTRA = N_TASKS - N_SUBGRAPHS * TASKS_PER_SUBGRAPH - 20  # tarefas extras isoladas

    urgency_pool = list(range(1, 101))

    # Gera subgrafos DAG aleatórios
    task_idx = 0
    for sg in range(N_SUBGRAPHS):
        start = task_idx
        end = start + TASKS_PER_SUBGRAPH

        for i in range(start, end):
            tasks.append({
                "id": gen_task_id(i),
                "name": f"sg{sg}_t{i - start}",
                "urgency": random.choice(urgency_pool)
            })

        # Cria arestas aleatórias dentro do subgrafo (apenas forward = sem ciclo local)
        # Garante que i < j para edge (i -> j), nunca volta → DAG garantido
        node_list = list(range(start, end))
        edges_added = 0
        target_edges = 125  # ~25.000 total / 200 subgrafos

        attempts = 0
        while edges_added < target_edges and attempts < 5000:
            attempts += 1
            i = random.randint(start, end - 2)
            j = random.randint(i + 1, end - 1)
            key = (gen_task_id(i), gen_task_id(j))
            if key not in deps_set:
                deps_set.add(key)
                deps.append({"from": gen_task_id(j), "to": gen_task_id(i)})
                edges_added += 1

        task_idx = end

    # Tarefas extras isoladas (nós sem arestas)
    for i in range(task_idx, task_idx + EXTRA):
        tasks.append({
            "id": gen_task_id(i),
            "name": f"isolated_{i}",
            "urgency": random.choice(urgency_pool)
        })
    task_idx += EXTRA

    # ────────────────────────────────────────────
    # CICLO PROFUNDO OCULTO (profundidade = 20 nós)
    # Inserido nas últimas 20 tarefas
    # c0 -> c1 -> c2 -> ... -> c19 -> c0
    # ────────────────────────────────────────────
    cycle_nodes = list(range(task_idx, task_idx + 20))
    for i in cycle_nodes:
        tasks.append({
            "id": gen_task_id(i),
            "name": f"deep_cycle_{i - task_idx:02d}",
            "urgency": random.choice(urgency_pool)
        })

    for k in range(len(cycle_nodes)):
        frm = cycle_nodes[(k + 1) % len(cycle_nodes)]
        to_ = cycle_nodes[k]
        key = (gen_task_id(frm), gen_task_id(to_))
        if key not in deps_set:
            deps_set.add(key)
            deps.append({"from": gen_task_id(frm), "to": gen_task_id(to_)})

    print(f"\n[ESTRESSE] Tarefas geradas: {len(tasks)}")
    print(f"[ESTRESSE] Dependências geradas: {len(deps)}")
    print(f"[ESTRESSE] Ciclo profundo oculto: {len(cycle_nodes)} nós")

    save_json({"tasks": tasks, "dependencies": deps}, "input_estresse.json")


def main():
    print("=== Gerador de Dados de Teste — Workflow Engine ===\n")

    print("[1/3] Gerando input_basico.json...")
    generate_basico()

    print("[2/3] Gerando input_avancado.json...")
    generate_avancado()

    print("[3/3] Gerando input_estresse.json...")
    generate_estresse()

    print("\n✓ Todos os arquivos gerados em /data/")


if __name__ == "__main__":
    main()
