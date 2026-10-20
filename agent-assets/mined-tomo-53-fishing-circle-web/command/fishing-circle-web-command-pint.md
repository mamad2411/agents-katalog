---
description: Laravel Pint でコードを整形する。--test を付けると確認のみ（変更しない）。
disable-model-invocation: true
---

Docker コンテナ `app` 内で Laravel Pint を実行します。

引数: `$ARGUMENTS`（例: 空＝全体整形 / `--test`＝確認のみ / ファイルパス＝対象限定）

`docker-compose exec app ./vendor/bin/pint $ARGUMENTS`

整形結果（変更ファイル数・スタイル違反の有無）を報告してください。
