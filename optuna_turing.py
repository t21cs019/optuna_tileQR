import os
import csv

import optuna.visualization as vis

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


def debag_print(best_params, best_value, time):        
    print(f"最適なパラメータ: nb={best_params['nb']}, ib={best_params['ib']}")
    print(f"最適なObjective Value: {best_value}")
    print(f"処理にかかった時間は {time} 秒です")

def save_best_trial(counts, time, best_params, best_value, output_file):
    """
    最適な試行の結果をCSVファイルに保存する関数。
    """
    # CSVファイルに追記モードで書き込む
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        # ヘッダー行を追加（ファイルが空の場合のみ）
        if f.tell() == 0:
            writer.writerow(['Trial', 'Execution Time (s)', 'nb', 'ib', 'Objective Value'])
        # 試行結果を記録
        writer.writerow([counts, time, best_params['nb'], best_params['ib'], best_value])


def visualize_study_results(best_params, best_value, study, output_fig_dir):
    """
    Optunaの最適化結果を可視化し、画像として保存する関数。
    """
    print(study.best_trial)

    # ① 最適化履歴の可視化
    print("最適化履歴を保存します...")
    fig = vis.plot_optimization_history(study)
    fig.write_image(f"{output_fig_dir}/optimization_history.png")

    # 最適なパラメータペアと性能値をグラフに記載
    print("最適なパラメータペアと性能値をグラフに記載します...")
    fig.add_annotation(
        text=f"Best Params: {best_params}<br>Best Value: {best_value:.4f}",
        xref="paper", yref="paper",
        x=1.2, y=1.2,  # グラフの右上外側に配置
        showarrow=False,
        font=dict(size=12, color="black"),
        align="center",
        bordercolor="black", borderwidth=1
    )
    fig.write_image(f"{output_fig_dir}/optimization_history_ver2.png")

    # ③ パラメータごとの目的関数値の分布
    print("パラメータごとの目的関数値の分布を保存します...")
    fig = vis.plot_slice(study)
    fig.write_image(f"{output_fig_dir}/slice_plot.png")

    # ④ ハイパーパラメータ間の相関関係
    print("ハイパーパラメータ間の相関関係を保存します...")
    fig = vis.plot_parallel_coordinate(study)
    fig.write_image(f"{output_fig_dir}/parallel_coordinate.png")

    # ⑤ 最適パラメータ探索空間を2D/3Dで可視化
    print("最適パラメータ探索空間を保存します...")
    fig = vis.plot_contour(study)
    fig.write_image(f"{output_fig_dir}/contour_plot.png")

def main():
    # # 実行回数
    # counts = 1
    # # 試行回数
    # trials = 10

    # # 最適化を実行
    # measurements_normal_optuna(counts, trials)
    measurements_normal_optuna(10, 25)
    measurements_normal_optuna(10, 50)
    measurements_normal_optuna(10, 100)

    print("全ての最適化が完了しました。")

if __name__ == "__main__":
    main()