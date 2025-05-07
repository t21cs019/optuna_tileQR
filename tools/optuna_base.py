import csv
import optuna.visualization as vis

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


def visualize_study_results(best_params, best_value, study):
    """
    Optunaの最適化結果を可視化し、画像として保存する関数。
    """

    print(study.best_trial)

    # ① 最適化履歴の可視化
    print("最適化履歴を保存します...")
    fig = vis.plot_optimization_history(study)
    fig.write_image("../result/optimization_history.png")
    # 最適なパラメータペアと性能値をグラフに記載
    print("最適なパラメータペアと性能値をグラフに記載します...")

    fig.add_annotation(
        text=f"Best Params: {best_params}<br>Best Value: {best_value:.4f}",
        xref="paper", yref="paper",
        x=1.05, y=1.05,  # グラフの右上外側に配置
        showarrow=False,
        font=dict(size=12, color="black"),
        align="center",
        bordercolor="black", borderwidth=1
    )

    fig.write_image("../result/optimization_history-ver2.png")

    # ③ パラメータごとの目的関数値の分布
    print("パラメータごとの目的関数値の分布を保存します...")
    fig = vis.plot_slice(study)
    fig.write_image("../result/slice_plot.png")

    # ④ ハイパーパラメータ間の相関関係
    print("ハイパーパラメータ間の相関関係を保存します...")
    fig = vis.plot_parallel_coordinate(study)
    fig.write_image("../result/parallel_coordinate.png")

    # ⑤ 最適パラメータ探索空間を2D/3Dで可視化
    print("最適パラメータ探索空間を保存します...")
    fig = vis.plot_contour(study)
    fig.write_image("../result/contour_plot.png")
