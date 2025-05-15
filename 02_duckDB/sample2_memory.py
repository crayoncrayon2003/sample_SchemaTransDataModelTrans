import os
import re
import json
import glob
from typing import List
import pandas as pd
import duckdb

class DuckETLPipeline:
    def __init__(self, sql_dir: str = None):
        if (sql_dir is None):
            raise ValueError("sql_dir is none")

        # DuckDB open(in-memory)
        self.conn = duckdb.connect(database=":memory:")
        # DuckDB Table name
        self.TEMP_TABLE = "tmpTable"

        self.sql_dir = sql_dir

    def __del__(self):
        self.conn.close()

    def _load_json_schema(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_sql(self, filename: str) -> str:
        path = os.path.join(self.sql_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _list_sql_files(self) -> List[str]:
        files = glob.glob(os.path.join(self.sql_dir, "*.sql"))
        filtered_files = [f for f in files if re.match(r"^[0-9]{3,}.*\.sql$", os.path.basename(f))]

        return sorted(filtered_files)

    def exec_all(self, df: pd.DataFrame) -> pd.DataFrame:
        ordered_files = self._list_sql_files()

        for sql_file in ordered_files:
            query = self._load_sql(sql_file)
            df = self._execute_sql(df, query)
        return df

    def _execute_sql(self, df: pd.DataFrame, query: str) -> pd.DataFrame:
        self.conn.register(self.TEMP_TABLE, df)
        return self.conn.execute(query).fetch_df()

    def exec_chg_columnname(self, df) -> pd.DataFrame:
        query = self._load_sql("001_chgColumnName.sql")
        return self._execute_sql(df, query)

    def exec_add_entityid(self, df) -> pd.DataFrame:
        query = self._load_sql("002_addEntityID.sql")
        return self._execute_sql(df, query)

    def exec_add_entitytype(self, df) -> pd.DataFrame:
        query = self._load_sql("003_addEntityType.sql")
        return self._execute_sql(df, query)

    def exec_to_ngsi(self, df) -> pd.DataFrame:
        query = self._load_sql("004_toNGSI.sql")
        return self._execute_sql(df, query)


def test1():
    print("---- test1 ----")
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(os.path.dirname(directory), "00_data", "data.csv")
    df = pd.read_csv(file_path)

    sql_dir = os.path.join(directory, "sql")
    pipeline = DuckETLPipeline(sql_dir=sql_dir)

    df = pipeline.exec_chg_columnname(df)
    df = pipeline.exec_add_entityid(df)
    df = pipeline.exec_add_entitytype(df)
    df = pipeline.exec_to_ngsi(df)

    print(json.dumps(json.loads(df['json_result'][0]), ensure_ascii=False, indent=2))

    pass

def test2():
    print("---- test2 ----")
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(os.path.dirname(directory), "00_data", "data.csv")
    df = pd.read_csv(file_path)

    sql_dir = os.path.join(directory, "sql")
    pipeline = DuckETLPipeline(sql_dir=sql_dir)

    df = pipeline.exec_all(df)

    print(json.dumps(json.loads(df['json_result'][0]), ensure_ascii=False, indent=2))

    pass


if __name__ == "__main__":
    test1()
    test2()