import os
import random
import string
import pandas as pd
import ray
import time
from datetime import datetime

ray.init(ignore_reinit_error=True)

def generate_random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

def generate_random_data1():
    num_rows = random.randint(1, 10)
    data = []

    for idx in range(1, num_rows + 1):
        row = {
            "id": idx,
            "name": generate_random_name(),
            "created_at": f"2024-01-{random.randint(1, 31):02d} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        }
        data.append(row)

    return data

def generate_random_data2():
    num_rows = random.randint(1, 10)
    data = []

    for idx in range(1, num_rows + 1):
        row = {
            "id": idx,
            "name": generate_random_name(),
            "created_at": f"2024-01-{random.randint(1, 31):02d}"
        }
        data.append(row)

    return data


@ray.remote
def update_csv(csv_path, data):
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"CSV updated at {datetime.now()}")
    return f"CSV written to {csv_path}"

def scheduler():
    directory = os.path.dirname(os.path.abspath(__file__))
    csv_path1 = os.path.join(directory, "project", "test_project", "seeds", "csv_format_1.csv")
    csv_path2 = os.path.join(directory, "project", "test_project", "seeds", "csv_format_2.csv")

    while True:
        # generate csv data
        csv_format_1_data = generate_random_data1()
        csv_format_2_data = generate_random_data2()

        # update csv data
        ray.get(update_csv.remote(csv_path1, csv_format_1_data))
        ray.get(update_csv.remote(csv_path2, csv_format_2_data))

        # wait
        time.sleep(30)

if __name__ == "__main__":
    scheduler()
