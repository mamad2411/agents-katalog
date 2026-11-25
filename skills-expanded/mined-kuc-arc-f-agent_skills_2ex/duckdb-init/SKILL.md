---
name: duckdb_init
description: ローカルに、duckdbファイル作成する。
disable-model-invocation: true
---

CSVファイルをduckdbにインポートする:


1.以下のSQLコマンド実行して、CSVファイルをduckdbにインポートする

```
duckdb ./my_database.db -c "CREATE TABLE my_table AS SELECT * FROM 'work/input.csv'"
```
