import os
import time
import ray
import duckdb
import json
from dbt.cli.main import dbtRunner

ray.init(ignore_reinit_error=True)

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
PATH_DBT_PROJECT = os.path.join(DIRECTORY, "project", "test_project")
PATH_DUCKDB = os.path.join(PATH_DBT_PROJECT, "duckdb", "database.duckdb")
PATH_OUTPUT_JSON = os.path.join(PATH_DBT_PROJECT, "output", "my_model.json")
PATH_OUTPUT_CLEAN = os.path.join(PATH_DBT_PROJECT, "output", "my_model_clean.json")

# run dbt seed, run, and export
@ray.remote
def run_dbt():
    os.chdir(PATH_DBT_PROJECT)
    runner = dbtRunner()

    print("Running dbt seed...")
    runner.invoke(["seed", "--project-dir", PATH_DBT_PROJECT], cwd=PATH_DBT_PROJECT)

    print("Running dbt run...")
    result = runner.invoke(["run", "--project-dir", PATH_DBT_PROJECT], cwd=PATH_DBT_PROJECT)
    if not result.success:
        print("dbt run failed.")
        return False

    print("Exporting JSON using dbt run-operation...")
    args = {
        "table_name": "main.csv_format_1_transformation",
        "file_path": PATH_OUTPUT_JSON,
        "format": "json"
    }
    result_op = runner.invoke([
        "run-operation",
        "copy_to_file",
        "--args", json.dumps(args)
    ], cwd=PATH_DBT_PROJECT)

    if not result_op.success:
        print("dbt run-operation failed.")
        return False

    return True

# flatten json_result and save
def clean_json_output():
    if not os.path.exists(PATH_OUTPUT_JSON):
        print(f"File not found: {PATH_OUTPUT_JSON}")
        return

    with open(PATH_OUTPUT_JSON, encoding="utf-8") as f:
        raw = json.load(f)

    if "json_result" not in raw:
        print("Expected 'json_result' key not found in output.")
        return

    flattened = raw["json_result"]
    print(json.dumps(flattened, ensure_ascii=False, indent=2))

    with open(PATH_OUTPUT_CLEAN, "w", encoding="utf-8") as f_out:
        json.dump(flattened, f_out, ensure_ascii=False, indent=2)


def scheduler():
    while True:
        success = ray.get(run_dbt.remote())
        if success:
            clean_json_output()
        else:
            print("DBT run or export failed.")
        time.sleep(30)

if __name__ == "__main__":
    scheduler()
