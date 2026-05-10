# optuna_tileQR

PLASMAライブラリのタイル型QR分解（dgeqrf）における
タイルサイズ `nb` と内部ブロック幅 `ib` のパラメータチューニング環境。

Optunaによるベイズ最適化と総当たりベンチマークを組み合わせ、
複数のマシンで再現可能な計測環境を自動構築できる。

## ディレクトリ構成

```
optuna_tileQR/
├── setup/
│   ├── config.sh               # パス・バージョン設定（ここを編集）
│   ├── install.sh              # 一括セットアップ（最初に1回実行）
│   ├── install_openblas.sh     # OpenBLAS ビルド
│   ├── install_plasma.sh       # PLASMA ビルド
│   ├── install_noflush.sh      # NoFlush（Tune_SSRFB）ビルド
│   ├── install_python_deps.sh  # Python環境（uv）
│   └── check.sh                # インストール確認
├── src/
│   ├── run_time_dgeqrf.py      # GFLOPS計測コア関数
│   ├── benchmark.py            # 総当たりベンチマーク
│   ├── heatmap.py              # ヒートマップ生成
│   ├── optuna_main.py          # Optunaチューニング メイン
│   ├── optuna_base.py          # 共通関数（保存・可視化）
│   └── tuning/
│       ├── normal_optuna.py    # 広い範囲でのOptuna
│       ├── select_optuna.py    # 絞り込み範囲でのOptuna
│       └── ssrfb_optuna.py     # NoFlush連携Optuna
├── results/                    # 計測結果（.gitignoreで除外）
│   ├── benchmark/
│   └── optuna/
├── run_benchmark.sh            # ベンチマーク実行ラッパー
├── run_optuna.sh               # Optunaチューニング実行ラッパー
└── README.md
```

---

## セットアップ

### 事前に必要なもの（管理者権限が必要）

```bash
sudo apt update && sudo apt install -y cmake gfortran curl wget git
```

### 一括セットアップ

```bash
git clone git@github.com:t21cs019/optuna_tileQR.git
cd optuna_tileQR
bash setup/install.sh
```

以下が自動でインストールされる：
- Python環境（uv + 仮想環境 `.venv`）
- OpenBLAS（ソースからビルド）
- PLASMA（ソースからビルド）
- NoFlush / Tune_SSRFB（ソースからビルド）

### インストール確認

```bash
bash setup/check.sh
```

全項目 `[OK]` になればセットアップ完了。

---

## 使い方

### ベンチマーク（総当たり）

```bash
# デフォルト設定で実行
bash run_benchmark.sh

# パラメータを指定して実行
bash run_benchmark.sh --size 4096 --nb-min 32 --nb-max 512 --ib-min 8 --step 4 --trials 2

# ヘルプ
bash run_benchmark.sh --help
```

結果は `results/benchmark/<ホスト名>_size<N>_..._<日時>.csv` に自動保存される。

| オプション | 説明 | デフォルト |
|----------|------|---------|
| `--threads` | OMP_NUM_THREADS | CPUコア数 |
| `--size` | 行列サイズ | 4096 |
| `--nb-min` | nb 最小値 | 32 |
| `--nb-max` | nb 最大値 | 512 |
| `--ib-min` | ib 最小値 | 8 |
| `--step` | ステップ幅 | 4 |
| `--trials` | 計測繰り返し回数 | 1 |

### ヒートマップ生成

```bash
.venv/bin/python src/heatmap.py --input results/benchmark/xxx.csv

# スレッド数を指定してフィルタリング
.venv/bin/python src/heatmap.py --input results/benchmark/xxx.csv --threads 16
```

### Optunaチューニング

```bash
# normalモード（広い探索範囲）
bash run_optuna.sh --mode normal --counts 10 --trials 25 50 100

# selectモード（絞り込み範囲、nb-min/maxを指定）
bash run_optuna.sh --mode select --nb-min 192 --nb-max 336 --counts 10 --trials 50

# ssrfbモード（NoFlush連携）
bash run_optuna.sh --mode ssrfb --nb-min 192 --nb-max 336 --counts 10 --trials 25

# ヘルプ
bash run_optuna.sh --help
```

| オプション | 説明 | デフォルト |
|----------|------|---------|
| `--mode` | normal / select / ssrfb / all | normal |
| `--counts` | 繰り返し回数 | 10 |
| `--trials` | Optuna試行回数（複数指定可） | 25 |
| `--size` | 行列サイズ | 4096 |
| `--nb-min` | nb 最小値 | モードごとのデフォルト |
| `--nb-max` | nb 最大値 | モードごとのデフォルト |
| `--threads` | OMP_NUM_THREADS | CPUコア数 |

---

## 別マシンへの移植

```bash
# 1. 必要なシステムパッケージ（管理者権限）
sudo apt update && sudo apt install -y cmake gfortran curl wget git

# 2. リポジトリをclone
git clone git@github.com:t21cs019/optuna_tileQR.git
cd optuna_tileQR

# 3. 一括セットアップ
bash setup/install.sh

# 4. 確認
bash setup/check.sh

# 5. 計測開始
bash run_benchmark.sh
```

## 計測結果の管理

- `results/` 以下のCSV・PNGは `.gitignore` で除外
- ファイル名にホスト名・日時が入るため、複数マシンの結果を同じフォルダに集めても区別できる