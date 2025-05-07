import os
import csv

import sys
sys.path.append('/home/kubota/Work/optuna_turing/tools')
from optuna_base import save_best_trial, visualize_study_results, debag_print

import sys
sys.path.append('/home/kubota/Work/optuna_turing/turing')
from normal_optuna import normal_turing
from select_optuna import select_turing
from ssrfb_optuna import ssrfb_turing

def measurements_normal_optuna(counts, trials):
    normal_resutl_dir = "/home/kubota/Work/optuna_turing/result/normal_optuna"

    for i in range(counts):
        output_fig_dir = f"{normal_resutl_dir}/{trials}/trial_{i + 1}"
        output_csv_file = f"{normal_resutl_dir}/{trials}/optuna_turing.csv"

        # ディレクトリを作成（存在しない場合）
        os.makedirs(output_fig_dir, exist_ok=True)

        print(f"=== {i + 1}/{counts} 回目の最適化を開始します ===")
        study, time = normal_turing(trials)

        # 最適なパラメータペアと性能値を抽出
        best_trial = study.best_trial
        best_params = best_trial.params
        best_value = best_trial.value

        # チューニング結果を記録
        save_best_trial(i + 1, time, best_params, best_value, output_csv_file)

        # 可視化を一括で実行し、画像を保存
        visualize_study_results(best_params, best_value, study, output_fig_dir)
         
def measurements_select_optuna(counts, trials):
    select_resutl_dir = "/home/kubota/Work/optuna_turing/result/select_optuna"

    for i in range(counts):
        output_fig_dir = f"{select_resutl_dir}/{trials}/trial_{i + 1}"
        output_csv_file = f"{select_resutl_dir}/{trials}/optuna_turing.csv"

        # ディレクトリを作成（存在しない場合）
        os.makedirs(output_fig_dir, exist_ok=True)

        print(f"=== {i + 1}/{counts} 回目の最適化を開始します ===")
        study, time = select_turing(trials)

        # 最適なパラメータペアと性能値を抽出
        best_trial = study.best_trial
        best_params = best_trial.params
        best_value = best_trial.value

        # チューニング結果を記録
        save_best_trial(i + 1, time, best_params, best_value, output_csv_file)

        # 可視化を一括で実行し、画像を保存
        visualize_study_results(best_params, best_value, study, output_fig_dir)

def measurements_ssrfb_optuna(counts, trials):
    ssrfb_resutl_dir = "/home/kubota/Work/optuna_turing/result/ssrfb_optuna"

    for i in range(counts):
        output_fig_dir = f"{ssrfb_resutl_dir}/{trials}/trial_{i + 1}"
        output_csv_file = f"{ssrfb_resutl_dir}/{trials}/optuna_turing.csv"

        # ディレクトリを作成（存在しない場合）
        os.makedirs(output_fig_dir, exist_ok=True)

        print(f"=== {i + 1}/{counts} 回目の最適化を開始します ===")
        study, time = ssrfb_turing(trials)

        # 最適なパラメータペアと性能値を抽出
        best_trial = study.best_trial
        best_params = best_trial.params
        best_value = best_trial.value

        # チューニング結果を記録
        save_best_trial(i + 1, time, best_params, best_value, output_csv_file)

        # 可視化を一括で実行し、画像を保存
        visualize_study_results(best_params, best_value, study, output_fig_dir)


def main():
    # # 実行回数
    # counts = 1
    # # 試行回数
    # trials = 10

    # # 最適化を実行
    # measurements_normal_optuna(counts, trials)
    measurements_ssrfb_optuna(10, 25)
    # measurements_ssrfb_optuna(10, 50)
    # measurements_ssrfb_optuna(10, 100)

    measurements_normal_optuna(10, 25)
    measurements_normal_optuna(10, 50)
    measurements_normal_optuna(10, 100)
    
    measurements_select_optuna(10, 25)
    measurements_select_optuna(10, 50)
    measurements_select_optuna(10, 100)

    print("全ての最適化が完了しました。")

if __name__ == "__main__":
    main()