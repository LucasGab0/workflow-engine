#!/bin/bash
# ============================================================
# Workflow Engine — Script de Execução Padrão
# Uso: ./run.sh [basico|avancado|estresse|all|generate]
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/src"
DATA="$SCRIPT_DIR/data"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

header() {
    echo -e "\n${YELLOW}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Workflow Engine — Orquestrador de Tarefas${NC}"
    echo -e "${YELLOW}════════════════════════════════════════${NC}\n"
}

check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}[ERRO] Python não encontrado. Instale Python 3.8+${NC}"
        exit 1
    fi
    PYTHON=$(command -v python3 || command -v python)
}

run_scenario() {
    local name=$1
    local input="$DATA/input_${name}.json"
    local output="$DATA/output_${name}.json"

    echo -e "${GREEN}[RUN]${NC} Cenário: $name"
    echo -e "      Entrada: $input"
    echo -e "      Saída:   $output\n"

    if [ ! -f "$input" ]; then
        echo -e "${RED}[ERRO] Arquivo de entrada não encontrado: $input${NC}"
        echo "       Execute primeiro: ./run.sh generate"
        exit 1
    fi

    $PYTHON "$SRC/main.py" "$input" "$output"
    echo -e "\n${GREEN}✓ Concluído: $output${NC}\n"
}

header
check_python

MODE=${1:-"all"}

case "$MODE" in
    generate)
        echo -e "${GREEN}[GENERATE]${NC} Gerando arquivos de teste...\n"
        $PYTHON "$SRC/generate_data.py"
        ;;
    basico)
        run_scenario "basico"
        ;;
    avancado)
        run_scenario "avancado"
        ;;
    estresse)
        run_scenario "estresse"
        ;;
    all)
        echo "Gerando dados de teste..."
        $PYTHON "$SRC/generate_data.py"
        echo ""
        run_scenario "basico"
        run_scenario "avancado"
        run_scenario "estresse"
        echo -e "${GREEN}✓ Todos os cenários executados com sucesso!${NC}"
        ;;
    *)
        echo "Uso: ./run.sh [generate|basico|avancado|estresse|all]"
        echo ""
        echo "  generate  — Gera os arquivos de entrada (/data)"
        echo "  basico    — Executa o cenário básico"
        echo "  avancado  — Executa o cenário avançado (com edge cases)"
        echo "  estresse  — Executa o cenário de estresse (10k tarefas)"
        echo "  all       — Gera dados e executa todos os cenários"
        exit 1
        ;;
esac
