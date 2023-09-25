import multiprocessing
import pandas as pd
from tqdm import tqdm

from graphs import create_graphs
from job import job


def main():
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    data_frames = list(
        tqdm(pool.imap_unordered(job, range(50)), total=50, desc="Processing")
    )

    pool.close()
    pool.join()

    final_data_frame = pd.concat(data_frames)
    final_data_frame.to_csv("./frames/constants.csv", index=False)

    create_graphs()


if __name__ == "__main__":
    main()
