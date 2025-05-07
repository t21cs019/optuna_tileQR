import optuna
import subprocess
import re
import time
import csv
import optuna.visualization as vis

import sys

sys.path.append('/home/kubota/Work/optuna_turing/tools')
from run_time_dgeqrf import run_time_dgeqrf
from optuna_base import visualize_study_results


def objective(trial):
    size = 4096
    min_nb = 192
    max_nb = 336
    min_ib = 10

    nb = 2 * trial.suggest_int("nb", min_nb/2, max_nb/2)
    ib = 2 * trial.suggest_int("ib", min_ib/2, nb/4)

    return run_time_dgeqrf(16, size, nb, ib)


def optuna_turing(n_trials):
    # WSL上のOptunaの実行
    start = time.time()  # 現在時刻（処理開始前）を取得

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials)

    end = time.time()  # 現在時刻（処理完了後）を取得

    time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する

    return study, time_diff


def main():
    # 処理にかかった時間を表示
    time = optuna_turing(20)
    print(f"処理にかかった時間は {time} 秒です")

if __name__ == "__main__":
    main()

