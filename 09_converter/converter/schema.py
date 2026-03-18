"""
schema.py

JSONスキーマの読み込みと、DataFrame への型適用を担当する。

関数の対応関係:
    schema_to_dataframe(df, schema)  : JSON Schema → DataFrame に型を適用
    schema_from_dataframe(df)        : DataFrame   → JSON Schema を生成

対応するJSONスキーマの型:
    string  → str
    integer → Int64  (pandas nullable integer)
    number  → float
    boolean → bool
    ["string", "null"] のような nullable 型にも対応
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)

# JSON Schema の type → pandas の dtype マッピング
_JSON_TYPE_TO_DTYPE: Dict[str, Any] = {
    "string":  str,
    "integer": "Int64",   # nullable integer
    "number":  float,
    "boolean": bool,
}


def load_schema(path: Union[str, Path, None]) -> Optional[Dict[str, Any]]:
    """
    JSONスキーマファイルを読み込む。
    path が None の場合は None を返す。
    """
    if path is None:
        return None
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def schema_from_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    DataFrame の dtypes から JSON Schema を自動生成する。
    Mapper が output_schema を自動生成する際に使用する（ケース2フォールバック）。
    対: schema_to_dataframe()
    """
    dtype_to_json: Dict[str, str] = {
        "object":  "string",
        "int64":   "integer",
        "Int64":   "integer",
        "float64": "number",
        "bool":    "boolean",
    }
    properties = {}
    for col, dtype in df.dtypes.items():
        json_type = dtype_to_json.get(str(dtype), "string")
        properties[col] = {"type": json_type}

    return {
        "type": "object",
        "properties": properties,
    }


def schema_to_dataframe(df: pd.DataFrame, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """
    JSON Schema に従い DataFrame の各カラムの型をキャストする。
    schema が None の場合はそのまま返す。
    対: schema_from_dataframe()
    """
    if schema is None:
        return df

    df = df.copy()
    for col, info in schema.get("properties", {}).items():
        if col not in df.columns:
            continue
        json_type = info.get("type")
        # ["string", "null"] のような nullable 型を解決
        if isinstance(json_type, list):
            json_type = next((t for t in json_type if t != "null"), None)
        dtype = _JSON_TYPE_TO_DTYPE.get(json_type)
        if dtype is None:
            continue
        try:
            df[col] = df[col].astype(dtype)
        except (ValueError, TypeError) as e:
            logger.warning(f"型変換失敗: col='{col}' type='{json_type}': {e}")

    return df