"""
writers.py

Writer の基底クラス・レジストリ・組み込み実装。

新しいフォーマットを追加する場合:
    1. BaseWriter を継承したクラスを作る
    2. @register_writer(".拡張子") デコレータを付ける
    3. write() メソッドを実装する

例（TSV を追加する場合）:
    @register_writer(".tsv")
    class TsvWriter(BaseWriter):
        def write(self, df: pd.DataFrame, path: Path) -> None:
            df.to_csv(path, sep="\\t", index=False, encoding="utf-8-sig")
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Type

import pandas as pd

# geopandas はオプション依存
try:
    import geopandas as gpd
    HAS_GEO = True
except ImportError:
    HAS_GEO = False


# ================================================================== #
#  基底クラス & レジストリ
# ================================================================== #

class BaseWriter(ABC):
    """
    Writer の基底クラス。
    write() を実装する。型適用済みの DataFrame を受け取り、ファイルに書き出す。
    型変換は Mapper / schema.py が責務を持つため、Writer は書き出しのみを担当する。
    """

    @abstractmethod
    def write(self, df: pd.DataFrame, path: Path) -> None:
        ...


_REGISTRY: Dict[str, Type[BaseWriter]] = {}


def register_writer(*extensions: str):
    """Writer クラスを拡張子に紐づけるデコレータ。"""
    def decorator(cls: Type[BaseWriter]):
        for ext in extensions:
            _REGISTRY[ext.lower()] = cls
        return cls
    return decorator


def get_writer(ext: str) -> BaseWriter:
    """拡張子に対応する Writer インスタンスを返す。"""
    cls = _REGISTRY.get(ext.lower())
    if cls is None:
        raise NotImplementedError(
            f"Writer が未登録です: '{ext}'\n"
            f"登録済み拡張子: {list(_REGISTRY.keys())}"
        )
    return cls()


# ================================================================== #
#  組み込み Writer
# ================================================================== #

@register_writer(".csv")
class CsvWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_csv(path, index=False, encoding="utf-8-sig")


@register_writer(".xlsx")
class ExcelWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_excel(path, index=False)


@register_writer(".json")
class JsonWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_json(path, orient="records", force_ascii=False, indent=2)


@register_writer(".parquet")
class ParquetWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_parquet(path, index=False)


@register_writer(".geojson")
class GeoJsonWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        if not HAS_GEO:
            raise ImportError("GeoJSON の書き出しには geopandas が必要です: pip install geopandas")
        if not isinstance(df, gpd.GeoDataFrame):
            raise TypeError("GeoJSON の書き出しには GeoDataFrame が必要です。")
        df.to_file(path, driver="GeoJSON")


@register_writer(".shp")
class ShapefileWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        if not HAS_GEO:
            raise ImportError("Shapefile の書き出しには geopandas が必要です: pip install geopandas")
        if not isinstance(df, gpd.GeoDataFrame):
            raise TypeError("Shapefile の書き出しには GeoDataFrame が必要です。")
        df.to_file(path)


@register_writer(".gpkg")
class GeoPackageWriter(BaseWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        if not HAS_GEO:
            raise ImportError("GeoPackage の書き出しには geopandas が必要です: pip install geopandas")
        if not isinstance(df, gpd.GeoDataFrame):
            raise TypeError("GeoPackage の書き出しには GeoDataFrame が必要です。")
        df.to_file(path, driver="GPKG")
