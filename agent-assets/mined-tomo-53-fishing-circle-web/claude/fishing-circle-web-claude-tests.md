# src/tests — Pest テスト

Pest 3 によるフィーチャー・ユニットテスト。ACL の境界値テストが最重要。

## 責務

| ディレクトリ | 責務 |
|---|---|
| `Feature/` | HTTP レベルの統合テスト。コントローラ・認可・画面遷移を検証 |
| `Unit/` | 単体テスト。Enum・ValueObject・ビジネスロジック等 |

## ACL 境界テスト（必須）

グループ権限が関わる操作には以下を必ずテストする：

- **Level 未満のユーザー** → `assertForbidden()` (403)
- **`is_approved = false`（承認待ち）** → `assertForbidden()` (403)
- **別グループのユーザー** → アクセス不可（403 または適切なリダイレクト）

## 主要コマンド

```bash
docker-compose exec app php artisan test                        # 全テスト
docker-compose exec app php artisan test --filter=<TestName>    # 絞り込み
docker-compose exec app php artisan test tests/Feature/Auth     # ディレクトリ指定
```

## 参照

- テスト規約 → `.cursor/rules/testing.mdc`（Pest の書き方・AAA・RefreshDatabase）
- セキュリティ規約 → `.cursor/rules/security.mdc`（ACL 設計）
- ルート CLAUDE.md → `/CLAUDE.md`

## 更新ルール

新しいサブシステムのテストを追加した場合、このファイルの責務表に反映すること。
規約の本体は `.cursor/rules/` とルート `CLAUDE.md` にあるため、ここには重複させず参照に留める。
矛盾を見つけたらルート / rules 側を正とし、本ファイルを修正する。
