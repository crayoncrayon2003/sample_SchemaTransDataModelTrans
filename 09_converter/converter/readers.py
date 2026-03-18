"""
readers.py

Reader の基底クラス・レジストリ・組み込み実装。

新しいフォーマットを追加する場合:
    1. BaseReader を継承したクラスを作る
    2. @register_reader(".拡張子") デコレータを付ける
    3. read() メソッドを実装する

例（TSV を追加する場合）:
    @register_reader(".tsv")
    class TsvReader(BaseReader):
        def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
            df = pd.read_csv(path, sep="\\t", encoding="utf-8-sig")
            return schema_to_dataframe(df, schema)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Type

import pandas as pd

from .schema import schema_to_dataframe

# geopandas はオプション依存
try:
    import geopandas as gpd
    HAS_GEO = True
except ImportError:
    HAS_GEO = False


# ================================================================== #
#  基底クラス & レジストリ
# ================================================================== #

class BaseReader(ABC):
    """
    Reader の基底クラス。
    read() を実装し、入力スキーマで型を確定した DataFrame を返す。
    """

    @abstractmethod
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        ...


_REGISTRY: Dict[str, Type[BaseReader]] = {}


def register_reader(*extensions: str):
    """Reader クラスを拡張子に紐づけるデコレータ。"""
    def decorator(cls: Type[BaseReader]):
        for ext in extensions:
            _REGISTRY[ext.lower()] = cls
        return cls
    return decorator


def get_reader(ext: str) -> BaseReader:
    """拡張子に対応する Reader インスタンスを返す。"""
    cls = _REGISTRY.get(ext.lower())
    if cls is None:
        raise NotImplementedError(
            f"Reader が未登録です: '{ext}'\n"
            f"登録済み拡張子: {list(_REGISTRY.keys())}"
        )
    return cls()


# ================================================================== #
#  組み込み Reader
# ================================================================== #

@register_reader(".csv")
class CsvReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.read_csv(path, encoding="utf-8-sig")
        return schema_to_dataframe(df, schema)


@register_reader(".xlsx", ".xls")
class ExcelReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.read_excel(path)
        return schema_to_dataframe(df, schema)


@register_reader(".json")
class JsonReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.read_json(path)
        return schema_to_dataframe(df, schema)


@register_reader(".parquet")
class ParquetReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.read_parquet(path)
        return schema_to_dataframe(df, schema)


@register_reader(".geojson")
class GeoJsonReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        if not HAS_GEO:
            raise ImportError("GeoJSON の読み込みには geopandas が必要です: pip install geopandas")
        gdf = gpd.read_file(path)
        return schema_to_dataframe(gdf, schema)


@register_reader(".shp")
class ShapefileReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        if not HAS_GEO:
            raise ImportError("Shapefile の読み込みには geopandas が必要です: pip install geopandas")
        gdf = gpd.read_file(path)
        return schema_to_dataframe(gdf, schema)


@register_reader(".gpkg")
class GeoPackageReader(BaseReader):
    def read(self, path: Path, schema: Optional[Dict[str, Any]]) -> pd.DataFrame:
        if not HAS_GEO:
            raise ImportError("GeoPackage の読み込みには geopandas が必要です: pip install geopandas")
        gdf = gpd.read_file(path)
        return schema_to_dataframe(gdf, schema)