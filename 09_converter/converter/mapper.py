"""
mapper.py

mapping.json の定義に従い DataFrame のフィールドを変換する。

mapping.json の構造:
{
  "fields": [
    {
      "src": "name",           // 変換元フィールド名（str / list / null）
      "dst": "fullName",       // 変換先フィールド名
      "type": "string",        // 変換先の型（省略可。省略時はoutput_schema.jsonの型を使用）
      "transform": "join",     // 変換方法（join のみ現在対応）
      "separator": " "         // join 時のセパレータ（デフォルト: " "）
    },
    {
      "src": ["first", "last"],  // 複数フィールドを結合
      "dst": "fullName",
      "transform": "join",
      "separator": " "
    },
    {
      "src": null,             // src が null → 固定値を追加
      "dst": "entityType",
      "type": "string",
      "default": "Place"
    }
  ]
}

マッピングルール:
    - src が文字列  → 単一フィールドのコピー（+ 型変換）
    - src がリスト  → 複数フィールドの結合（transform: "join"）
    - src が null   → 固定値を追加（default: "..." が必須）
    - フィールド名を変えたくない場合は src == dst にする
    - mapping.json に書かれたフィールドだけが出力される（未記載は削除扱い）
    - mapping_path が None の場合は DataFrame をそのまま返す（パススルー）

output_schema との関係:
    - mapping の type と output_schema の両方が指定された場合、output_schema を優先する
    - mapping の type だけが指定された場合、それに従い型変換する（ケース2フォールバック）
    - どちらも指定されない場合、型変換は行わない
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd

from .schema import schema_to_dataframe, schema_from_dataframe

logger = logging.getLogger(__name__)


def load_mapping(path: Union[str, Path, None]) -> Optional[List[Dict[str, Any]]]:
    """
    mapping.json を読み込む。
    path が None の場合は None を返す（パススルー動作）。
    """
    if path is None:
        return None
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("fields", [])


class Mapper:
    """
    mapping定義と transform_fn に従い DataFrame を変換する。

    処理順序:
        1. mapping.json によるフィールド変換（名前変更・結合・固定値追加・削除）
        2. mapping の type による型変換（output_schema がない場合のフォールバック）
        3. transform_fn による追加変換（任意の Python 関数）
        4. output_schema による型の最終確定（最優先）

    Args:
        field_defs    : load_mapping() で読み込んだフィールド定義リスト
        transform_fn  : DataFrame を受け取り DataFrame を返す任意の変換関数
        output_schema : 出力スキーマ（型の最終確定に使用）
    """

    def __init__(
        self,
        field_defs: Optional[List[Dict[str, Any]]],
        transform_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
    ):
        self.field_defs   = field_defs
        self.transform_fn = transform_fn
        self.output_schema = output_schema

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # ── Step1: フィールド変換 ────────────────────────────────
        result = self._apply_field_defs(df)

        # ── Step2: mapping の type でフォールバック型変換 ─────────
        # output_schema がない場合のみ mapping の type を使う（ケース2フォールバック）
        if self.output_schema is None and self.field_defs is not None:
            fallback_schema = self._build_fallback_schema()
            if fallback_schema:
                result = schema_to_dataframe(result, fallback_schema)

        # ── Step3: transform_fn による追加変換 ───────────────────
        if self.transform_fn is not None:
            result = self.transform_fn(result)

        # ── Step4: output_schema で型を最終確定（最優先）──────────
        if self.output_schema is not None:
            result = schema_to_dataframe(result, self.output_schema)

        return result

    # ---------------------------------------------------------------- #

    def _apply_field_defs(self, df: pd.DataFrame) -> pd.DataFrame:
        """mapping定義に従いフィールドを変換する。"""
        if self.field_defs is None:
            return df  # パススルー

        result = pd.DataFrame(index=df.index)

        for field in self.field_defs:
            src     = field.get("src")
            dst     = field.get("dst")
            trans   = field.get("transform")
            sep     = field.get("separator", " ")
            default = field.get("default")

            if dst is None:
                logger.warning(f"dst が未指定のフィールド定義をスキップします: {field}")
                continue

            # 固定値
            if src is None:
                result[dst] = default
                continue

            # 複数フィールド結合
            if isinstance(src, list):
                missing = [s for s in src if s not in df.columns]
                if missing:
                    logger.warning(f"結合元フィールドが見つかりません: {missing}")
                    continue
                if trans == "join":
                    result[dst] = df[src].astype(str).agg(sep.join, axis=1)
                else:
                    result[dst] = df[src[0]]
                continue

            # 単一フィールド
            if src not in df.columns:
                logger.warning(f"フィールドが見つかりません: '{src}'")
                if default is not None:
                    result[dst] = default
                continue

            result[dst] = df[src]

        return result

    def _build_fallback_schema(self) -> Optional[Dict[str, Any]]:
        """
        mapping の type フィールドから output_schema 相当の JSON Schema を生成する。
        output_schema が指定されていない場合のフォールバック（ケース2）。
        """
        if not self.field_defs:
            return None

        properties = {}
        for field in self.field_defs:
            dst = field.get("dst")
            typ = field.get("type")
            if dst and typ:
                properties[dst] = {"type": typ}

        if not properties:
            return None

        return {"type": "object", "properties": properties}