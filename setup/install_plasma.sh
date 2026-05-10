#!/usr/bin/env bash
# =============================================================================
# install_plasma.sh — PLASMA を GitHub からcloneしてビルド・インストール
# 管理者権限不要。${PLASMA_INSTALL} にインストールする。
# OpenBLAS のインストールが先に完了している必要がある。
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

WORK_DIR="${HOME}/Download/build_plasma"
SRC_DIR="${WORK_DIR}/plasma"

echo "======================================================"
echo " PLASMA インストール開始"
echo " インストール先: ${PLASMA_INSTALL}"
echo "======================================================"

# OpenBLAS の確認
if [ ! -f "${OPENBLAS_INSTALL}/lib/libopenblas.so" ]; then
    echo "[ERROR] OpenBLAS が見つかりません: ${OPENBLAS_INSTALL}/lib/libopenblas.so"
    echo "        先に install_openblas.sh を実行してください。"
    exit 1
fi

# すでにインストール済みか確認
if [ -f "${PLASMA_TEST}" ]; then
    echo "[SKIP] PLASMA はすでにインストール済みです。"
    echo "       再インストールしたい場合は ${PLASMA_INSTALL} を削除してください。"
    exit 0
fi

# 必要なコマンドの確認
for cmd in cmake python3 gfortran git; do
    if ! command -v "${cmd}" &>/dev/null; then
        echo "[ERROR] '${cmd}' が見つかりません。インストールしてください。"
        exit 1
    fi
done

mkdir -p "${WORK_DIR}"

# ソースの取得
if [ -d "${SRC_DIR}/.git" ]; then
    echo "[1/3] 既存のソースを使用します: ${SRC_DIR}"
    cd "${SRC_DIR}"
    git pull --ff-only || echo "       git pull をスキップ（ローカル変更あり）"
else
    echo "[1/3] PLASMA を git clone しています..."
    cd "${WORK_DIR}"
    git clone "${PLASMA_GIT_URL}" plasma
    cd "${SRC_DIR}"
fi

# CMake ビルド
echo "[2/3] CMake でビルドしています..."
mkdir -p build && cd build

cmake .. \
    -DCMAKE_INSTALL_PREFIX="${PLASMA_INSTALL}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DBLAS_LIBRARIES="${OPENBLAS_INSTALL}/lib/libopenblas.so" \
    -DLAPACK_LIBRARIES="${OPENBLAS_INSTALL}/lib/libopenblas.so" \
    -DCBLAS_INCLUDE_DIRS="${OPENBLAS_INSTALL}/include" \
    -DLAPACKE_INCLUDE_DIRS="${OPENBLAS_INSTALL}/include"

make -j"${NUM_MAKE_JOBS}"

# インストール
echo "[3/3] インストールしています -> ${PLASMA_INSTALL}"
make install

echo ""
echo "[完了] PLASMA のインストールが完了しました。"
echo "       テストバイナリ: ${PLASMA_TEST}"