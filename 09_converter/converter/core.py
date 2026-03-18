"""
core.py

Converter クラスと convert() 関数を提供する。

output_schema の決定ルール（優先順位）:
    1. dst_schema_path が指定されている → そのスキーマを使う（ケース1・推奨）
    2. dst_schema_path が省略されている → mapping の type から自動生成（ケース2・フォールバック）
    3. どちらもない                     → 型変換なしでそのまま書き出す

cache_path について:
    指定すると読み込んだ DataFrame を parquet としてストレージに保存する。
    次回以降は parquet から復元するため、元ファイルの再読み込みをスキップできる。
    大容量ファイルや同一入力から複数出力を生成する場合に有効。
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import pandas as pd

from .mapper import Mapper, load_mapping
from .readers import get_reader
from .schema import load_schema
from .writers import get_writer

logger = logging.getLogger(__name__)


class Converter:
    """
    ファイル変換の中心クラス。

    Args:
        src_path        : 変換元ファイルパス
        src_schema_path : 変換元 JSON スキーマパス（省略可）
        cache_path      : 中間データを parquet で保存するパス（省略時はメモリ保持）

    使用例:
        # 1回読み込み → 複数形式で保存
        c = Converter("data.csv", src_schema_path="schema/input.json")
        c.save("output/data.xlsx",
               dst_schema_path="schema/output.json",
               mapping_path="schema/mapping.json")
        c.save("output/data.geojson",
               mapping_path="schema/mapping_geo.json")
    """

    def __init__(
        self,
        src_path: Union[str, Path],
        src_schema_path: Union[str, Path, None] = None,
        cache_path: Union[str, Path, None] = None,
    ):
        self.src_path    = Path(src_path)
        self.src_schema  = load_schema(src_schema_path)
        self.cache_path  = Path(cache_path) if cache_path else None
        self._data: Optional[pd.DataFrame] = None

    @property
    def data(self) -> pd.DataFrame:
        """
        入力ファイルを DataFrame として返す（遅延読み込み）。
        cache_path が指定されていれば parquet から復元し、
        なければ元ファイルを読み込んで parquet に保存する。
        """
        if self._data is not None:
            return self._data

        if self.cache_path and self.cache_path.exists():
            logger.info(f"キャッシュから復元: {self.cache_path}")
            self._data = pd.read_parquet(self.cache_path)
            return self._data

        logger.info(f"ファイル読み込み: {self.src_path}")
        reader = get_reader(self.src_path.suffix)
        self._data = reader.read(self.src_path, self.src_schema)

        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._data.to_parquet(self.cache_path, index=False)
            logger.info(f"キャッシュ保存: {self.cache_path}")

        return self._data

    def save(
        self,
        dst_path: Union[str, Path],
        dst_schema_path: Union[str, Path, None] = None,
        mapping_path: Union[str, Path, None] = None,
        transform_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    ) -> None:
        """
        変換して保存する。

        Args:
            dst_path        : 出力ファイルパス
            dst_schema_path : 出力 JSON スキーマパス
                              指定あり → スキーマで型を確定（推奨）
                              省略    → mapping の type から型を自動生成（フォールバック）
            mapping_path    : フィールドマッピング定義ファイルパス（JSON）
                              省略時は DataFrame をそのまま出力（パススルー）
            transform_fn    : DataFrame を受け取り DataFrame を返す任意の変換関数
                              mapping 適用後、output_schema 適用前に実行される
        """
        dst_path = Path(dst_path)
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        dst_schema = load_schema(dst_schema_path)
        field_defs = load_mapping(mapping_path)

        mapper = Mapper(
            field_defs=field_defs,
            transform_fn=transform_fn,
            output_schema=dst_schema,
        )
        result = mapper.apply(self.data)

        writer = get_writer(dst_path.suffix)
        writer.write(result, dst_path)
        logger.info(f"保存完了: {dst_path}")
        print(f"[Converter] saved: {dst_path}")


def convert(
    src_path: Union[str, Path],
    dst_path: Union[str, Path],
    src_schema_path: Union[str, Path, None] = None,
    dst_schema_path: Union[str, Path, None] = None,
    mapping_path: Union[str, Path, None] = None,
    transform_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    cache_path: Union[str, Path, None] = None,
) -> None:
    """
    一発変換関数。全引数を渡して変換・保存する。

    Args:
        src_path        : 変換元ファイルパス
        dst_path        : 変換先ファイルパス
        src_schema_path : 変換元 JSON スキーマパス（省略可）
        dst_schema_path : 変換先 JSON スキーマパス（省略可）
        mapping_path    : フィールドマッピング定義ファイルパス（JSON）（省略可）
        transform_fn    : 任意の変換関数（省略可）
        cache_path      : 中間データの parquet キャッシュパス（省略可）

    使用例:
        convert(
            src_path="data.csv",
            dst_path="output/data.json",
            src_schema_path="schema/input.json",
            dst_schema_path="schema/output.json",
            mapping_path="schema/mapping.json",
        )
    """
    c = Converter(src_path, src_schema_path, cache_path)
    c.save(dst_path, dst_schema_path, mapping_path, transform_fn)
