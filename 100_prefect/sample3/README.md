```
python3.12 -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

```
deactivate
rm -rf env
```

etl-framework/
├── scripts/                        # 共通フレームワーク
│   ├── __init__.py
│   ├── core/                       # フレームワーク本体
│   │   ├── __init__.py
│   │   ├── orchestrator/           # Prefectベースのオーケストレーション
│   │   │   ├── __init__.py
│   │   │   ├── flow_executor.py    # メインフロー実行器
│   │   │   └── task_wrapper.py     # プラグインのPrefectタスク化
│   │   ├── pipeline/               # パイプライン定義・実行エンジン
│   │   │   ├── __init__.py
│   │   │   ├── pipeline_parser.py  # YAML設定解析
│   │   │   ├── step_executor.py    # ステップ実行管理
│   │   │   └── dependency_resolver.py # 依存関係解決
│   │   ├── plugin_manager/         # プラグイン管理システム
│   │   │   ├── __init__.py
│   │   │   ├── manager.py          # プラグイン管理メインクラス
│   │   │   ├── registry.py         # プラグイン登録・発見
│   │   │   └── interfaces.py       # 抽象基底クラス定義
│   │   ├── data_container/         # データコンテナ定義
│   │   │   ├── __init__.py
│   │   │   ├── container.py        # DataContainerクラス
│   │   │   └── formats.py          # サポートフォーマット定義
│   │   └── config/                 # 設定管理
│   │       ├── __init__.py
│   │       ├── loader.py           # 設定ファイル読み込み
│   │       └── validator.py        # 設定バリデーション
│   │
│   ├── plugins/                    # プラグイン群
│   │   ├── __init__.py
│   │   ├── extractors/             # データ取得プラグイン
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # BaseExtractor抽象クラス
│   │   │   ├── from_local_file.py  # ローカルファイル取得（既存コード活用）
│   │   │   ├── from_local_json.py  # ローカルJSON取得（既存コード活用）
│   │   │   ├── from_http.py        # HTTP API取得
│   │   │   ├── from_ftp.py         # FTP取得
│   │   │   ├── from_scp.py         # SCP取得
│   │   │   └── from_database.py    # データベース取得
│   │   ├── cleansing/              # データクレンジングプラグイン
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # BaseCleanser抽象クラス
│   │   │   ├── archive_extractor.py # ZIP/圧縮ファイル展開
│   │   │   ├── encoding_converter.py # 文字コード変換
│   │   │   ├── format_detector.py  # ファイル形式自動判定
│   │   │   ├── duplicate_remover.py # 重複データ除去
│   │   │   └── null_handler.py     # NULL値処理
│   │   ├── transformers/           # データ変換プラグイン
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # BaseTransformer抽象クラス
│   │   │   ├── with_duckdb.py      # DuckDB変換（既存コード活用）
│   │   │   ├── with_jinja2.py      # Jinja2変換（既存コード活用）
│   │   │   ├── to_ngsi.py          # NGSI形式変換
│   │   │   ├── csv_processor.py    # CSV処理
│   │   │   ├── json_processor.py   # JSON処理
│   │   │   ├── gtfs_processor.py   # GTFS処理
│   │   │   └── shapefile_processor.py # シェープファイル処理
│   │   ├── validators/             # バリデーションプラグイン
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # BaseValidator抽象クラス
│   │   │   ├── json_schema.py      # JSONスキーマ検証（既存コード活用）
│   │   │   ├── data_quality.py     # データ品質チェック
│   │   │   ├── ngsi_validator.py   # NGSI形式検証
│   │   │   └── business_rules.py   # ビジネスルール検証
│   │   └── loaders/                # データ登録プラグイン
│   │       ├── __init__.py
│   │       ├── base.py             # BaseLoader抽象クラス
│   │       ├── to_local_file.py    # ローカルファイル出力（既存コード活用）
│   │       ├── to_http.py          # HTTP POST/PUT
│   │       ├── to_ftp.py           # FTP アップロード
│   │       ├── to_scp.py           # SCP アップロード
│   │       ├── to_context_broker.py # Context Broker登録
│   │       └── to_database.py      # データベース登録
│   │
│   └── utils/                      # ユーティリティ（既存コード活用・拡張）
│       ├── __init__.py
│       ├── config_loader.py        # 設定読み込み（既存utils.pyを拡張）
│       ├── sql_template.py         # SQLテンプレート処理（既存utils.pyを拡張）
│       ├── file_utils.py           # ファイル操作ユーティリティ
│       └── logger.py               # ログ設定
│
├── ETL1/                           # CSV to Parquet and Report（既存）
│   ├── 00_flows/                   # フロー定義
│   │   ├── .gitkeep
│   │   └── etl_flow.py             # 既存のフロー（scriptsを使用するよう修正）
│   ├── 01_data/                    # データディレクトリ
│   │   ├── input/
│   │   │   ├── .gitkeep
│   │   │   └── source_data.csv
│   │   ├── working/
│   │   │   └── .gitkeep
│   │   └── output/
│   │       └── .gitkeep
│   ├── 02_cleansing/               # クレンジング用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # クレンジングルール設定
│   │   └── schemas/                # クレンジング前後のスキーマ
│   │       ├── raw_data_schema.json
│   │       └── cleansed_data_schema.json
│   ├── 03_validation/              # バリデーション用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # バリデーションルール設定
│   │   └── schemas/                # バリデーション用スキーマ
│   │       ├── input_schema.json   # 既存のスキーマファイル
│   │       └── output_schema.json  # 既存のスキーマファイル
│   ├── 04_templates/               # Jinja2テンプレート
│   │   ├── .gitkeep
│   │   └── report.html.j2          # 既存テンプレート
│   ├── 05_queries/                 # DuckDB SQLクエリ
│   │   ├── .gitkeep
│   │   └── add_timestamp.sql       # 既存クエリ
│   └── config.yml                  # パイプライン設定
│
├── ETL2/                           # CSV to NGSI-v2 JSON（既存）
│   ├── 00_flows/
│   │   ├── .gitkeep
│   │   └── etl_flow.py
│   ├── 01_data/
│   │   ├── input/
│   │   │   ├── .gitkeep
│   │   │   └── measurements.csv
│   │   ├── working/
│   │   │   └── .gitkeep
│   │   └── output/
│   │       └── .gitkeep
│   ├── 02_cleansing/               # クレンジング用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # クレンジングルール設定
│   │   └── schemas/                # クレンジング前後のスキーマ
│   │       ├── raw_data_schema.json
│   │       └── cleansed_data_schema.json
│   ├── 03_validation/              # バリデーション用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # バリデーションルール設定
│   │   └── schemas/                # バリデーション用スキーマ
│   │       ├── input_schema.json
│   │       └── output_schema.json
│   ├── 04_templates/               # Jinja2テンプレート
│   │   ├── .gitkeep
│   │   └── to_ngsiv2.json.j2
│   ├── 05_queries/                 # DuckDB SQLクエリ
│   │   ├── .gitkeep
│   │   ├── 01_validate_source.sql
│   │   └── 02_structure_to_ngsi.sql
│   └── config.yml
│
├── ETL3/                           # Validated JSON to NGSI-v2（既存）
│   ├── 00_flows/
│   │   ├── .gitkeep
│   │   └── etl_flow.py
│   ├── 01_data/
│   │   ├── input/
│   │   │   ├── .gitkeep
│   │   │   └── device_logs.json
│   │   ├── working/
│   │   │   └── .gitkeep
│   │   └── output/
│   │       └── .gitkeep
│   ├── 02_cleansing/               # クレンジング用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # クレンジングルール設定
│   │   └── schemas/                # クレンジング前後のスキーマ
│   │       ├── raw_data_schema.json
│   │       └── cleansed_data_schema.json
│   ├── 03_validation/              # バリデーション用スキーマ・設定
│   │   ├── .gitkeep
│   │   ├── rules.yml               # バリデーションルール設定
│   │   └── schemas/                # バリデーション用スキーマ
│   │       ├── input_schema.json   # 既存のスキーマファイル
│   │       └── output_schema.json  # 既存のスキーマファイル
│   ├── 04_templates/               # Jinja2テンプレート
│   │   ├── .gitkeep
│   │   └── to_ngsiv2_entity.json.j2
│   ├── 05_queries/                 # DuckDB SQLクエリ
│   │   ├── .gitkeep
│   │   └── transform_device_logs.sql
│   └── config.yml
│
├── ETL_Weather/                    # 新規ETL例：気象データ処理
│   ├── 00_flows/
│   │   └── weather_etl_flow.py
│   ├── 01_data/
│   │   ├── input/
│   │   ├── working/
│   │   └── output/
│   ├── 02_cleansing/               # クレンジング用スキーマ・設定
│   │   ├── rules.yml               # 気象データ固有のクレンジングルール
│   │   └── schemas/
│   │       ├── weather_raw_schema.json
│   │       └── weather_cleansed_schema.json
│   ├── 03_validation/              # バリデーション用スキーマ・設定
│   │   ├── rules.yml               # 気象データ固有のバリデーションルール
│   │   └── schemas/
│   │       ├── weather_api_schema.json
│   │       └── ngsi_weather_schema.json
│   ├── 04_templates/               # Jinja2テンプレート
│   │   ├── weather_entity.json.j2
│   │   └── weather_report.html.j2
│   ├── 05_queries/                 # DuckDB SQLクエリ
│   │   ├── cleanse_weather_data.sql
│   │   └── transform_to_weather_entity.sql
│   └── config.yml
│
├── ETL_Traffic/                    # 新規ETL例：交通データ処理
│   ├── 00_flows/
│   │   └── traffic_etl_flow.py
│   ├── 01_data/
│   │   ├── input/
│   │   ├── working/
│   │   └── output/
│   ├── 02_cleansing/               # クレンジング用スキーマ・設定
│   │   ├── rules.yml               # 交通データ固有のクレンジングルール
│   │   └── schemas/
│   │       ├── gtfs_raw_schema.json
│   │       └── gtfs_cleansed_schema.json
│   ├── 03_validation/              # バリデーション用スキーマ・設定
│   │   ├── rules.yml               # 交通データ固有のバリデーションルール
│   │   └── schemas/
│   │       ├── gtfs_schema.json
│   │       └── ngsi_traffic_schema.json
│   ├── 04_templates/               # Jinja2テンプレート
│   │   └── traffic_entity.json.j2
│   ├── 05_queries/                 # DuckDB SQLクエリ
│   │   ├── process_gtfs_data.sql
│   │   └── create_traffic_entities.sql
│   └── config.yml
│
├── tests/                          # テストコード
│   ├── unit/                       # ユニットテスト
│   │   ├── test_core/
│   │   ├── test_plugins/
│   │   └── test_utils/
│   ├── integration/                # 統合テスト
│   │   ├── test_etl1/
│   │   ├── test_etl2/
│   │   └── test_etl3/
│   └── fixtures/                   # テストデータ
│
├── docs/                           # ドキュメント
│   ├── architecture.md
│   ├── plugin_development.md
│   ├── etl_creation_guide.md
│   └── user_guide.md
│
├── requirements.txt                # 依存関係（既存）
├── setup.py                        # パッケージ設定
├── README.md                       # 既存README更新
└── .gitignore