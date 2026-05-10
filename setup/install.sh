#!/usr/bin/env bash
# =============================================================================
# install.sh — plasma-bench 環境を一括セットアップする
#
# 使い方:
#   git clone <your-repo-url> ~/Workspace/plasma-bench
#   cd ~/Workspace/plasma-bench
#   bash setup/install.sh
#
# 実行順序:
#   1. Python 環境（uv + venv）
#   2. OpenBLAS
#   3. PLASMA
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================"
echo " plasma-bench セットアップ開始"
echo "======================================================"
echo ""

# 1. Python / uv（OpenBLAS・PLASMAのビルドにPythonが必要なため最初に）
echo ">>> [1/3] Python 環境（uv）のセットアップ"
bash "${SCRIPT_DIR}/install_python_deps.sh"
echo ""

# 2. OpenBLAS
echo ">>> [2/3] OpenBLAS のインストール"
bash "${SCRIPT_DIR}/install_openblas.sh"
echo ""

# 3. PLASMA
echo ">>> [3/3] PLASMA のインストール"
bash "${SCRIPT_DIR}/install_plasma.sh"
echo ""

echo "======================================================"
echo " セットアップ完了！"
echo ""
echo " ※ NoFlush（SSRFB用）は別途手動インストールが必要です。"
echo "   詳細は README.md の「NoFlushのセットアップ」を参照してください。"
echo ""
echo " セットアップの確認:"
echo "   bash setup/check.sh"
echo ""
echo " ベンチマーク実行:"
echo "   bash run_benchmark.sh --help"
echo "======================================================"
