import subprocess

def find_best_ib(nb, min_ib, max_ib, noflush_path="./NoFlush"):
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
    best_ib = None
    best_time = float('inf')

    for ib in range(min_ib, max_ib + 1):
        if nb % ib != 0:
            continue

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

if __name__ == "__main__":
    # Example usage
    nb = 100  # Replace with the desired nb value
    min_ib = 20
    max_ib = 50
    noflush_path = "/home/kubota/Work/optuna_turing/tools/Tune_SSRFB-master/NoFlush"  # Correct path to NoFlush executable

    best_ib, best_time = find_best_ib(nb, min_ib, max_ib, noflush_path)
    
    if best_ib is not None:
        print(f"The best ib for nb={nb} is {best_ib} with time {best_time:.6f} seconds.")
    else:
        print(f"No valid ib found for nb={nb}.")