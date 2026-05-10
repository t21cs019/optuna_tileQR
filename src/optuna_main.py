"""
optuna_main.py — Optuna チューニングのメイン実行スクリプト

使い方:
    python optuna_main.py [オプション]

例:
    # normal モードを5回×25試行で実行
    python optuna_main.py --mode normal --counts 5 --trials 25

    # select モードでnb範囲を指定して実行
    python optuna_main.py --mode select --nb-min 192 --nb-max 336 --counts 10 --trials 50

    # 全モードを実行（ssrfb は NoFlush が必要）
    python optuna_main.py --mode all --counts 10 --trials 25 50 100
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from optuna_base import save_best_trial, visualize_study_results
from tuning.normal_optuna import normal_tuning
from tuning.select_optuna import select_tuning
from tuning.ssrfb_optuna import ssrfb_tuning

RESULTS_BASE = os.path.join(os.path.dirname(__file__), "..", "results", "optuna")


def run_mode(mode: str, tuning_fn, counts: int, trials_list: list, extra_kwargs: dict):
    result_dir = os.path.join(RESULTS_BASE, mode)

    for n_trials in trials_list:
        csv_path = os.path.join(result_dir, str(n_trials), "optuna_results.csv")

        for i in range(counts):
            fig_dir = os.path.join(result_dir, str(n_trials), f"run_{i + 1}")
            os.makedirs(fig_dir, exist_ok=True)

            print(f"\n=== [{mode}] {i + 1}/{counts} 回目 (trials={n_trials}) ===")
            study, elapsed = tuning_fn(n_trials=n_trials, **extra_kwargs)

            best_params = study.best_trial.params
            best_value = study.best_trial.value

            save_best_trial(i + 1, elapsed, best_params, best_value, csv_path)
            visualize_study_results(best_params, best_value, study, fig_dir)

            print(f"  最適: nb={best_params['nb']}, ib={best_params['ib']}, "
                  f"GFLOPS={best_value:.4f}, {elapsed:.1f}秒")

    print(f"\n[{mode}] 完了 → {result_dir}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="PLASMA dgeqrf Optuna チューニング",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["normal", "select", "ssrfb", "all"],
        default="normal",
        help="実行モード（デフォルト: normal）"
    )
    parser.add_argument("--counts",  type=int, default=10,
                        help="繰り返し回数（デフォルト: 10）")
    parser.add_argument("--trials",  type=int, nargs="+", default=[25],
                        help="Optuna試行回数（複数指定可、デフォルト: 25）")
    parser.add_argument("--size",    type=int, default=4096,
                        help="行列サイズ（デフォルト: 4096）")
    parser.add_argument("--nb-min",  type=int, default=None,
                        help="nb 最小値（省略時はモードのデフォルト）")
    parser.add_argument("--nb-max",  type=int, default=None,
                        help="nb 最大値（省略時はモードのデフォルト）")
    parser.add_argument("--threads", type=int, default=os.cpu_count(),
                        help="OMP_NUM_THREADS（デフォルト: CPUコア数）")
    return parser.parse_args()


def main():
    args = parse_args()

    common = {"size": args.size, "num_threads": args.threads}
    if args.nb_min:
        common["nb_min"] = args.nb_min
    if args.nb_max:
        common["nb_max"] = args.nb_max

    modes = {
        "normal": normal_tuning,
        "select": select_tuning,
        "ssrfb":  ssrfb_tuning,
    }

    targets = list(modes.keys()) if args.mode == "all" else [args.mode]

    for mode in targets:
        run_mode(mode, modes[mode], args.counts, args.trials, common)

    print("\n全ての最適化が完了しました。")


if __name__ == "__main__":
    main()
