"""
Workflow Engine — Orquestrador Principal
Integra todos os módulos: Grafo, DFS, Ordenação Topológica, Max-Heap.
"""

import json
import sys
import os

# Garante que o diretório /src está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph import Graph
from cycle_detector import detect_cycles
from topological_sort import topological_sort


def load_input(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_output(data: dict, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_graph(tasks: list, dependencies: list) -> tuple[Graph, dict]:
    """
    Constrói o grafo a partir da lista de tarefas e dependências.

    Convenção de aresta:
        dependency["from"] -> dependency["to"]
        Significa: "from" DEPENDE de "to" (to deve ser executada antes de from).
    """
    graph = Graph()
    tasks_meta = {}

    for task in tasks:
        task_id = task["id"]
        graph.add_node(task_id)
        tasks_meta[task_id] = {
            "name": task.get("name", task_id),
            "urgency": task.get("urgency", 0),
            "description": task.get("description", ""),
        }

    for dep in dependencies:
        # dep["from"] depende de dep["to"]
        # Para execução: to deve vir ANTES de from
        # Modelamos como aresta to -> from (to "libera" from)
        graph.add_edge(dep["to"], dep["from"])

    return graph, tasks_meta


def run_engine(input_path: str, output_path: str):
    print(f"[ENGINE] Carregando entrada: {input_path}")
    data = load_input(input_path)

    tasks = data.get("tasks", [])
    dependencies = data.get("dependencies", [])

    print(f"[ENGINE] Tarefas: {len(tasks)} | Dependências: {len(dependencies)}")

    # RF01 — Constrói o Grafo Direcionado
    graph, tasks_meta = build_graph(tasks, dependencies)
    print(f"[ENGINE] Grafo construído: {graph.node_count} nós, {graph.edge_count} arestas")

    # RF03 — DFS: Detecção de Ciclos (verificação preventiva)
    print("[ENGINE] Executando detecção de ciclos (DFS)...")
    cycle_result = detect_cycles(graph)

    if cycle_result["has_cycle"]:
        print(f"[ENGINE] ⚠ DEADLOCK DETECTADO: {len(cycle_result['cycles'])} ciclo(s) encontrado(s).")
        for i, cycle in enumerate(cycle_result["cycles"][:5]):  # mostra até 5
            print(f"  Ciclo {i+1}: {' -> '.join(cycle)}")
    else:
        print("[ENGINE] ✓ Nenhum ciclo detectado. Execução segura.")

    # RF02 + RF04 — Ordenação Topológica com Max-Heap de prioridade
    print("[ENGINE] Executando ordenação topológica (Kahn + Max-Heap)...")
    sort_result = topological_sort(graph, tasks_meta)

    if sort_result["success"]:
        print(f"[ENGINE] ✓ Ordem de execução calculada: {len(sort_result['execution_order'])} tarefas.")
    else:
        print(f"[ENGINE] ✗ Falha: {sort_result['error']}")

    # Monta saída
    output = {
        "summary": {
            "total_tasks": len(tasks),
            "total_dependencies": len(dependencies),
            "nodes_in_graph": graph.node_count,
            "edges_in_graph": graph.edge_count,
        },
        "cycle_detection": {
            "has_cycle": cycle_result["has_cycle"],
            "total_cycles_found": len(cycle_result["cycles"]),
            "cycles": [
                {"nodes": c} for c in cycle_result["cycles"][:20]  # limita output
            ],
        },
        "topological_sort": {
            "success": sort_result["success"],
            "tasks_scheduled": len(sort_result["execution_order"]),
            "execution_order": sort_result["execution_order"],
            "error": sort_result["error"],
        },
    }

    save_output(output, output_path)
    print(f"[ENGINE] Saída salva em: {output_path}")
    return output


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <input.json> <output.json>")
        print("Exemplo: python main.py ../data/input_basico.json ../data/output_basico.json")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"[ERRO] Arquivo de entrada não encontrado: {input_path}")
        sys.exit(1)

    run_engine(input_path, output_path)


if __name__ == "__main__":
    main()
