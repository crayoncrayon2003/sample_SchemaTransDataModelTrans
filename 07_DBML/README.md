# 1. DBML
Database Markup Language

# 2. Tools
* 2.1. VS CODE Extension
* 2.2. dbdiagram.io
* 2.3. dbml-cli
* 2.4. python dbml

## 2.1. VS CODE Extension
vscode-dbml is
* DBML Syntax Highlighting  ✅
* Autocompletion / Snippets ✅
* Syntax Error Detection    ✅
* ER Diagram Preview        ❌
* SQL Generation            ❌
* Export Diagram as Image   ❌
* Collaboration / Sharing   ❌
* GitHub Integration        ❌
* Offline Editing           ✅


## 2.2. dbdiagram.io
https://dbdiagram.io

dbdiagram is
* DBML Syntax Highlighting  ✅
* Autocompletion / Snippets ✅
* Syntax Error Detection    ✅
* ER Diagram Preview        ✅
* SQL Generation            ✅
* Export Diagram as Image   ✅
* Collaboration / Sharing   ✅
* GitHub Integration        ✅
* Offline Editing           ❌

## 2.3. dbml-cli
node version 16.x or higher
npm  version 8.x or higher

* mysql                     ✅
* postgres                  ✅
* sqlserver                 ✅
* others                    ❌

### install
```
$ node -v
$ v18.19.1
$ npm -v
$ 9.2.0
$
$ npm install -g @dbml/cli
$ dbml2sql --help
```

### How to use
```
$ dbml2sql gtfsjp_schema.dbml --postgres -o schema.sql
```

## 2.4. python dbml
```
$ pip install dbml
$ python dbml_to_dbt_seed_config.py
```