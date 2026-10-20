# src/database — マイグレーション / ファクトリ / シーダ

スキーマ定義とテストデータ生成を担う。スキーマ変更は必ず**新規マイグレーションで前進**させる。

## 責務

| ディレクトリ | 責務 |
|---|---|
| `migrations/` | DB スキーマの変更履歴。既存ファイルの破壊的編集は禁止 |
| `factories/` | テスト用モデルファクトリ（`UserFactory` 等）。テストデータ生成の唯一の手段 |
| `seeders/` | 初期データ投入。本番 DB への `migrate:fresh` / `migrate:rollback` は禁止 |

## 重要な原則

- スキーマ変更は `php artisan make:migration` で新規ファイルを作成し、常に前進させる。
- `migrate:fresh` は開発環境専用。本番・共有 DB には絶対に実行しない。
- **第3章の Enum 導入で int 値はそのまま維持**。`PermissionLevel` / `Grade` の Enum 値は既存 DB の int/string と一致するため、マイグレーション追加不要だった。

## 主要コマンド

```bash
docker-compose exec app php artisan migrate          # マイグレーション適用
docker-compose exec app php artisan migrate:status   # 適用状態確認
docker-compose exec app php artisan make:migration <name>  # 新規マイグレーション作成
```

## 参照

- PHP/Laravel 規約 → `.cursor/rules/php-laravel.mdc`（マイグレーション禁止事項）
- テスト規約 → `.cursor/rules/testing.mdc`（ファクトリの使い方）
- ルート CLAUDE.md → `/CLAUDE.md`

## 更新ルール

このディレクトリ配下に新しいマイグレーションや重要なファクトリを追加・変更した場合、このファイルに特記事項があれば更新すること。
規約の本体は `.cursor/rules/` とルート `CLAUDE.md` にあるため、ここには重複させず参照に留める。
矛盾を見つけたらルート / rules 側を正とし、本ファイルを修正する。
