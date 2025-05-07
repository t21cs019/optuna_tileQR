import optuna
import subprocess
import re
import time

import sys
sys.path.append('/home/kubota/Work/optuna_turing/tools')
from run_time_dgeqrf import run_time_dgeqrf


def find_best_ib(nb, min_ib, max_ib):
    """
    Find the best ib value for a given nb by running NoFlush and analyzing the output.

    Args:
        nb (int): The NB size to test.
        min_ib (int): The minimum IB size.
        max_ib (int): The maximum IB size.
        noflush_path (str): Path to the NoFlush executable.

    Returns:
        tuple: The best ib value and its corresponding execution time.
    """

    noflush_path = "/home/kubota/Work/optuna_turing/tools/Tune_SSRFB-master/NoFlush"  # Correct path to NoFlush executable

    best_ib = None
    best_time = float('inf')

    for ib in range(min_ib, max_ib + 1, 2):
        print(f"Testing nb={nb}, ib={ib}...")

        # Run NoFlush with the current ib
        try:
            result = subprocess.run(
                [noflush_path, str(nb), str(ib), str(ib)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            # Parse the output
            for line in result.stdout.splitlines():
                if line.startswith(f"{nb}, {ib},"):
                    _, _, time = line.split(", ")
                    time = float(time)
                    if time < best_time:
                        best_time = time
                        best_ib = ib
        except subprocess.CalledProcessError as e:
            print(f"Error running NoFlush with nb={nb}, ib={ib}: {e}")
            continue

    return best_ib, best_time


def objective(trial):
    size = 4096
    max_nb = 336
    min_nb = 192
    
    nb = 2 * trial.suggest_int("nb", min_nb/2, max_nb/2)

    best_ib, best_time = find_best_ib(nb, 4, nb/2)

    if best_ib is not None:
        print(f"The best ib for nb={nb} is {best_ib} with time {best_time:.6f} seconds.")
    else:
        print(f"No valid ib found for nb={nb}.")
        return 0

    return run_time_dgeqrf(16, size, nb, best_ib)


def ssrfb_turing(n_trials):
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
    study, time = ssrfb_turing(trial)

    print(study.best_trial)
    print(f"処理にかかった時間は {time} 秒です")

if __name__ == "__main__":
    main()
