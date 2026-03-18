"""
converter パッケージ

公開 API:
    convert()   : 一発変換関数
    Converter   : 読み込みと保存を分離したクラス

拡張 API（新しいフォーマットを追加する場合）:
    register_reader : Reader を拡張子に登録するデコレータ
    register_writer : Writer を拡張子に登録するデコレータ
    BaseReader      : Reader の基底クラス
    BaseWriter      : Writer の基底クラス
"""

from .core import Converter, convert
from .readers import BaseReader, register_reader
from .writers import BaseWriter, register_writer

__all__ = [
    "convert",
    "Converter",
    "BaseReader",
    "register_reader",
    "BaseWriter",
    "register_writer",
]
