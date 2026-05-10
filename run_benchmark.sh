#!/usr/bin/env bash
# =============================================================================
# run_benchmark.sh — ベンチマーク実行ラッパー
# 環境変数のセットアップを自動で行ってから benchmark.py を実行する
#
# 使い方:
#   bash run_benchmark.sh [benchmark.py に渡すオプション]
#
# 例:
#   bash run_benchmark.sh --size 4096 --nb-min 32 --nb-max 512 --trials 2
#   bash run_benchmark.sh --help
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/setup/config.sh"

# ライブラリパスの設定
export LD_LIBRARY_PATH="${OPENBLAS_INSTALL}/lib:${PLASMA_INSTALL}/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"

# Python 実行環境（リポジトリ直下の .venv を使う）
if [ -f "${SCRIPT_DIR}/.venv/bin/python" ]; then
    PYTHON="${SCRIPT_DIR}/.venv/bin/python"
else
    echo "[ERROR] .venv が見つかりません。先に bash setup/install.sh を実行してください。"
    exit 1
fi

# plasmatest の存在確認
if [ ! -f "${PLASMA_TEST}" ]; then
    echo "[ERROR] plasmatest が見つかりません: ${PLASMA_TEST}"
    echo "        先に bash setup/install.sh を実行してください。"
    exit 1
fi

cd "${SCRIPT_DIR}/src"
exec "${PYTHON}" benchmark.py "$@"
