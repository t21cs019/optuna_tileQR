import optuna
import subprocess
import re
import time
import optuna.visualization as vis

import sys

sys.path.append('/home/kubota/Work/optuna_turing/tools')
# Replace 'some_function' with the actual function name you want to import
from run_time_dgeqrf import run_time_dgeqrf


def objective(trial):
    size = 4096
    max_nb = 512

    nb = 2 * trial.suggest_int("nb", 2, max_nb/2)
    ib = 2 * trial.suggest_int("ib", 2, nb/4)
    return run_time_dgeqrf(16, size, nb, ib)


def normal_turing(n_trials):
    # WSL上のOptunaの実行
    start = time.time()  # 現在時刻（処理開始前）を取得

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials)

    end = time.time()  # 現在時刻（処理完了後）を取得

    time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する

    return study, time_diff


def main():
    trial = 20

    # 処理にかかった時間を表示
    study, time = normal_turing(trial)

    print(study.best_trial)
    print(f"処理にかかった時間は {time} 秒です")

if __name__ == "__main__":
    main()

