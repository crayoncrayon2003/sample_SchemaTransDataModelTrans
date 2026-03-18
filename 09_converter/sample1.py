"""
main.py

converter パッケージの使用例。

ファイル構成:
    sample/
    ├── data/
    │   └── input.csv              # 変換元データ
    ├── schema/
    │   ├── input_schema.json      # 入力スキーマ
    │   ├── mapping.json           # フィールドマッピング定義
    │   └── output_schema.json     # 出力スキーマ（ケース1用）
    ├── output/                    # 変換結果の出力先
    └── main.py                    # このファイル

スキーマの対応関係:
    input_schema.json     mapping.json          output_schema.json
    ─────────────────     ────────────────────  ──────────────────
    first (string)   ─┐
                       ├─[join]──→ fullName      fullName (string)
    last  (string)   ─┘
    age   (integer)  ──────────→ age             age      (integer)
    score (number)   ──────────→ score           score    (number)
    city  (string)   ──────────→ location        location (string)
    ※なし            ──[固定値]→ entityType      entityType (string)
"""

import os
import pandas as pd
from converter import Converter, convert

# ------------------------------------------------------------------ #
#  パス定義
# ------------------------------------------------------------------ #
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
SCHEMA_DIR  = os.path.join(BASE_DIR, "schema")
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")

SRC         = os.path.join(DATA_DIR,   "input.csv")
SRC_SCHEMA  = os.path.join(SCHEMA_DIR, "input_schema.json")
MAPPING     = os.path.join(SCHEMA_DIR, "mapping.json")
DST_SCHEMA  = os.path.join(SCHEMA_DIR, "output_schema.json")

# ------------------------------------------------------------------ #
#  ケース1：出力スキーマを外部から明示（推奨）
#
#  - output_schema.json で型を厳密に確定する
#  - mapping.json の type は無視される（output_schema が優先）
#  - スキーマを明示するため、意図しない型変換が起きない
# ------------------------------------------------------------------ #
def example_case1():
    print("=" * 50)
    print("ケース1：出力スキーマを外部から明示（推奨）")
    print("=" * 50)

    c = Converter(SRC, src_schema_path=SRC_SCHEMA)
    c.save(
        os.path.join(OUTPUT_DIR, "case1_output.json"),
        mapping_path=MAPPING,
        dst_schema_path=DST_SCHEMA,   # ← 出力スキーマを外部から明示
    )


# ------------------------------------------------------------------ #
#  ケース2：output_schema を省略 → mapping の type から自動生成
#
#  - output_schema.json が不要なケースで使う
#  - mapping.json の各フィールドに "type" を書いておく必要がある
#  - "type" が書かれていないフィールドは型変換なし
# ------------------------------------------------------------------ #
def example_case2():
    print("=" * 50)
    print("ケース2：output_schema を省略（mapping の type から自動生成）")
    print("=" * 50)

    c = Converter(SRC, src_schema_path=SRC_SCHEMA)
    c.save(
        os.path.join(OUTPUT_DIR, "case2_output.json"),
        mapping_path=MAPPING,
        # dst_schema_path を省略 → mapping の type を使う
    )


# ------------------------------------------------------------------ #
#  transform_fn 併用：複雑な変換が必要なケース
#
#  処理順序:
#    1. mapping.json によるフィールド変換
#    2. transform_fn による追加変換  ← ここでカスタム処理
#    3. output_schema による型の最終確定
#
#  transform_fn でできること:
#    - 条件分岐による値の書き換え
#    - 数値計算・文字列加工
#    - 外部データとの結合
#    - mapping では表現できない複雑なロジック
# ------------------------------------------------------------------ #
def my_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    mapping 適用後の DataFrame をさらに加工する。
    score が NaN（欠損）の場合は 0.0 で補完し、
    fullName を大文字に変換する例。
    """
    df = df.copy()
    df["score"]    = df["score"].fillna(0.0)
    df["fullName"] = df["fullName"].str.upper()
    return df

def example_transform_fn():
    print("=" * 50)
    print("transform_fn 併用（複雑な変換）")
    print("=" * 50)

    c = Converter(SRC, src_schema_path=SRC_SCHEMA)
    c.save(
        os.path.join(OUTPUT_DIR, "case_transform_output.json"),
        mapping_path=MAPPING,
        dst_schema_path=DST_SCHEMA,
        transform_fn=my_transform,    # ← カスタム変換関数を渡す
    )


# ------------------------------------------------------------------ #
#  1回読み込み → 複数形式に保存
#
#  Converter は data プロパティが遅延読み込みのため、
#  save() を複数回呼んでも元ファイルの読み込みは1回だけ。
#  cache_path を指定すると parquet としてストレージに保存し、
#  次回以降はそこから復元する。
# ------------------------------------------------------------------ #
def example_multi_output():
    print("=" * 50)
    print("1回読み込み → 複数形式に保存")
    print("=" * 50)

    c = Converter(
        SRC,
        src_schema_path=SRC_SCHEMA,
        cache_path=os.path.join(OUTPUT_DIR, "cache.parquet"),  # 中間データをストレージ保存
    )

    # JSON で出力
    c.save(
        os.path.join(OUTPUT_DIR, "multi_output.json"),
        mapping_path=MAPPING,
        dst_schema_path=DST_SCHEMA,
    )

    # Excel で出力（同じ読み込み結果を再利用）
    c.save(
        os.path.join(OUTPUT_DIR, "multi_output.xlsx"),
        mapping_path=MAPPING,
        dst_schema_path=DST_SCHEMA,
    )

    # CSV で出力（transform_fn も追加）
    c.save(
        os.path.join(OUTPUT_DIR, "multi_output.csv"),
        mapping_path=MAPPING,
        dst_schema_path=DST_SCHEMA,
        transform_fn=my_transform,
    )


# ------------------------------------------------------------------ #
#  convert() 関数：一発変換（引数をすべて渡すシンプルな使い方）
# ------------------------------------------------------------------ #
def example_convert_fn():
    print("=" * 50)
    print("convert() 関数：一発変換")
    print("=" * 50)

    convert(
        src_path=SRC,
        dst_path=os.path.join(OUTPUT_DIR, "convert_fn_output.json"),
        src_schema_path=SRC_SCHEMA,
        dst_schema_path=DST_SCHEMA,
        mapping_path=MAPPING,
    )


# ------------------------------------------------------------------ #
#  メイン
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    example_case1()        # ケース1：推奨
    example_case2()        # ケース2：フォールバック
    example_transform_fn() # transform_fn 併用
    example_multi_output() # 複数形式出力
    example_convert_fn()   # convert() 一発変換