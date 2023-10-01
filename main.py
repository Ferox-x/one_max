import multiprocessing
from tqdm import tqdm

from job import job
from utils import ENV_CONSTANTS


def main():
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    list(
        tqdm(
            pool.imap_unordered(
                job,
                range(int(ENV_CONSTANTS.get("TOTAL_JOBS", 5))),
            ),
            total=int(ENV_CONSTANTS.get("TOTAL_JOBS", 5)),
            desc="Processing",
        )
    )

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
