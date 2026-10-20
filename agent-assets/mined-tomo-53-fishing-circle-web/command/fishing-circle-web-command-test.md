---
description: Pest テストを Docker 内で実行する。引数でフィルタ名やパスを指定可（例: /test Auth）。
disable-model-invocation: true
---

Docker コンテナ `app` 内で Pest テストを実行します。

引数: `$ARGUMENTS`

手順:
- 引数が空なら全テスト: `docker-compose exec app php artisan test`
- 引数がディレクトリ風（`/` を含む）ならパス指定: `docker-compose exec app php artisan test $ARGUMENTS`
- それ以外はフィルタ: `docker-compose exec app php artisan test --filter=$ARGUMENTS`

結果を要約し、失敗があれば該当テストとエラーの原因・修正方針を示してください。
アサーションを甘くしてテストを通す「ごまかし」は禁止です。
