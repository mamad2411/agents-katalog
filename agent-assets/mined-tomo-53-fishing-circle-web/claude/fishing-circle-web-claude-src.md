# src — Laravel アプリケーション全体

Laravel 12 本体のルートディレクトリ。`src/` が PHP/Node のパス基点。

## 責務

- `app/` … バックエンドロジック（Models / Controllers / Middleware / Requests / Enums / ValueObjects / Casts）
- `resources/views/` … Blade テンプレート（Tailwind + Alpine.js）
- `database/` … マイグレーション / ファクトリ / シーダ
- `tests/` … Pest フィーチャー・ユニットテスト
- `routes/` … ルート定義（`web.php` / `auth.php`）。規約は → `routes/README` ではなくルート CLAUDE.md 参照

## 主要コマンド

```bash
# Docker コンテナ内で実行
docker-compose exec app php artisan test          # テスト全実行
docker-compose exec app php artisan test --filter=<TestName>
docker-compose exec app ./vendor/bin/pint         # コード整形（コミット前必須）
docker-compose exec app ./vendor/bin/pint --test  # 整形チェックのみ（CI向け）
docker-compose exec app php artisan migrate       # マイグレーション適用
docker-compose exec app php artisan migrate:status
docker-compose exec app php artisan route:list    # ルート一覧
docker-compose exec app npm run dev               # フロントビルド（開発）
docker-compose exec app npm run build             # フロントビルド（本番）
```

## 参照

- ルート CLAUDE.md → `/CLAUDE.md`（プロジェクト全体の big picture・ACL 概要）
- PHP/Laravel 規約 → `.cursor/rules/php-laravel.mdc`
- Blade/フロントエンド規約 → `.cursor/rules/blade-frontend.mdc`
- テスト規約 → `.cursor/rules/testing.mdc`
- セキュリティ規約 → `.cursor/rules/security.mdc`

## 更新ルール

このディレクトリ配下のサブシステム構成を追加・変更・削除したら、このファイルも同じ変更で更新すること。
規約の本体は `.cursor/rules/` とルート `CLAUDE.md` にあるため、ここには重複させず参照に留める。
矛盾を見つけたらルート / rules 側を正とし、本ファイルを修正する。
