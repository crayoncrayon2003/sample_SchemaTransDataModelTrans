import os
import time
import ray
import duckdb
import json
from dbt.cli.main import dbtRunner

ray.init(ignore_reinit_error=True)

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PATH_DBT_PROJECT = os.path.join(DIRECTORY, "project", "test_project")
PATH_DUCKDB = os.path.join(DIRECTORY, "project", "test_project", "duckdb", "database.duckdb")

# run dbt
@ray.remote
def run_dbt():
    os.chdir(PATH_DBT_PROJECT)
    runner = dbtRunner()
    runner.invoke(["seed", "--project-dir", PATH_DBT_PROJECT], cwd=PATH_DBT_PROJECT)
    result = runner.invoke(["run", "--project-dir", PATH_DBT_PROJECT], cwd=PATH_DBT_PROJECT)
    print(result)
    return result.success

# run dbt
@ray.remote
def get_transformed_data():
    con = duckdb.connect(PATH_DUCKDB)
    df = con.execute("SELECT * FROM main.csv_format_1_transformation").fetchdf()
    con.close()
    return df

def scheduler():
    while True:
        success = ray.get(run_dbt.remote())
        if success:
            df = ray.get(get_transformed_data.remote())
            print(json.dumps(json.loads(df['json_result'][0]), ensure_ascii=False, indent=2))
        else:
            print("DBT run failed.")
        time.sleep(30)

if __name__ == "__main__":
    scheduler()
