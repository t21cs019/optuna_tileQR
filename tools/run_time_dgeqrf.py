import subprocess
import re
import os

# コマンドを実行してGFLOPS値を取得
def run_time_dgeqrf(num_threads, size, nb_value, ib_value):
    command = [
        '/home/kubota/Library/plasma-17.1/test/test',
        'dgeqrf',
        f'--m={size}',
        f'--n={size}',
        f'--nb={nb_value}',
        f'--ib={ib_value}'
    ]
    
    # 環境変数のコピーを作成して OMP_NUM_THREADS を追加
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(num_threads)
    
    # 環境変数OMP_NUM_THREADSを設定してコマンドを実行
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env  # 環境変数を使用
    )
    
    # コマンドの出力内容をプリント
    # print(result.stdout)
    
    # GFLOPSの値を正規表現で抽出
    match = re.search(
        r"pass\s+([-\d.e]+)\s+([-\d.e]+)\s+([\d.]+)",  # パターンを必要に応じて調整
        result.stdout
    )
    
    if match:
        gflops_value = match.group(3)  # GFLOPSは3番目のグループにあります
        return float(gflops_value)  # floatに変換して返す
    else:
        print(f"threads={num_threads}, nb={nb_value}, ib={ib_value} のGFLOPS値が見つかりませんでした")
        return 0.0  # デフォルト値を返す

