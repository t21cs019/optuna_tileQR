#!/usr/bin/env bash
# =============================================================================
# run_optuna.sh — Optuna チューニング実行ラッパー
#
# 使い方:
#   bash run_optuna.sh [optuna_main.py に渡すオプション]
#
# 例:
#   bash run_optuna.sh --mode normal --counts 5 --trials 25 50
#   bash run_optuna.sh --mode ssrfb --counts 3 --trials 100
#   bash run_optuna.sh --help
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/setup/config.sh"

export LD_LIBRARY_PATH="${OPENBLAS_INSTALL}/lib:${PLASMA_INSTALL}/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

if [ -f "${SCRIPT_DIR}/.venv/bin/python" ]; then
    PYTHON="${SCRIPT_DIR}/.venv/bin/python"
else
    echo "[ERROR] .venv が見つかりません。先に bash setup/install.sh を実行してください。"
    exit 1
fi

if [ ! -f "${PLASMA_TEST}" ]; then
    echo "[ERROR] plasmatest が見つかりません: ${PLASMA_TEST}"
    echo "        先に bash setup/install.sh を実行してください。"
    exit 1
fi

cd "${SCRIPT_DIR}/src"
exec "${PYTHON}" optuna_main.py "$@"
