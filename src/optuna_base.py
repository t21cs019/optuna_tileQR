"""
optuna_base.py — Optuna チューニング結果の保存・可視化共通関数
"""
import csv
import os
import optuna
import optuna.visualization as vis


def debug_print(best_params: dict, best_value: float, elapsed: float) -> None:
    print(f"最適パラメータ : nb={best_params['nb']}, ib={best_params['ib']}")
    print(f"最適 GFLOPS   : {best_value:.4f}")
    print(f"実行時間       : {elapsed:.1f} 秒")


def save_best_trial(
    count: int,
    elapsed: float,
    best_params: dict,
    best_value: float,
    output_file: str,
) -> None:
    """最適試行の結果を CSV に追記する"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    write_header = not os.path.exists(output_file)

    with open(output_file, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Trial", "Execution Time (s)", "nb", "ib", "Objective Value"])
        writer.writerow([count, f"{elapsed:.2f}", best_params["nb"], best_params["ib"], best_value])


def visualize_study_results(
    best_params: dict,
    best_value: float,
    study: optuna.Study,
    output_dir: str,
) -> None:
    """
    Optuna の最適化結果を可視化して output_dir に PNG として保存する。

    Parameters
    ----------
    best_params : dict
    best_value  : float
    study       : optuna.Study
    output_dir  : str  保存先ディレクトリ
    """
    os.makedirs(output_dir, exist_ok=True)

    annotation = dict(
        text=f"Best nb={best_params['nb']}, ib={best_params['ib']}<br>GFLOPS={best_value:.4f}",
        xref="paper", yref="paper",
        x=1.05, y=1.05,
        showarrow=False,
        font=dict(size=11, color="black"),
        align="center",
        bordercolor="black", borderwidth=1,
    )

    # ① 最適化履歴
    fig = vis.plot_optimization_history(study)
    fig.add_annotation(**annotation)
    fig.write_image(os.path.join(output_dir, "optimization_history.png"))

    # ② スライスプロット（パラメータごとの目的関数分布）
    fig = vis.plot_slice(study)
    fig.write_image(os.path.join(output_dir, "slice_plot.png"))

    # ③ 平行座標プロット
    fig = vis.plot_parallel_coordinate(study)
    fig.write_image(os.path.join(output_dir, "parallel_coordinate.png"))

    # ④ コンタープロット
    fig = vis.plot_contour(study)
    fig.write_image(os.path.join(output_dir, "contour_plot.png"))

    print(f"  可視化結果を保存しました: {output_dir}")
