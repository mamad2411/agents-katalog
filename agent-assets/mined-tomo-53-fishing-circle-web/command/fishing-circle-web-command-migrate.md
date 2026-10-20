---
description: マイグレーションの状態確認・適用を行う。引数 status / up（apply）を指定。
disable-model-invocation: true
---

Docker コンテナ `app` 内でマイグレーション操作を行います。

引数: `$ARGUMENTS`

- `status`（または空）: `docker-compose exec app php artisan migrate:status`
- `up` / `apply`: `docker-compose exec app php artisan migrate`

`migrate:fresh` / `migrate:reset` / `migrate:rollback` は破壊的なため、このコマンドからは実行しません。
必要な場合はリスクを説明し、ユーザーの明示的な確認を得てください。
適用後はスキーマと対応モデル（`$fillable` 等）の整合を確認してください。
