---
description: Pest テスト規約（テスト・ファクトリ編集時に適用、ACL境界必須）
globs: src/tests/**/*.php,src/database/factories/**/*.php
alwaysApply: false
---

# テスト規約（Pest）

テストやファクトリを書くときに適用する。

## フレームワーク

- **Pest 3** を使う。`it('...', function () { ... })` / `test('...')` 形式。
- DB を使うテストは `uses(RefreshDatabase::class)`（テストは SQLite in-memory）。
- 既存の `tests/Feature` `tests/Unit` の書き方に倣う。Auth 系テストは `tests/Feature/Auth/` を参照。

## 方針

- 機能追加・バグ修正には必ず対応するテストを追加する。
- **ACL（4段階権限）の境界を必ずテストする**：Level未満は403、承認前(`is_approved=false`)は403、別グループのユーザーはアクセス不可。
- HTTP テストは `actingAs($user)` でログイン状態を作り、`assertStatus` / `assertRedirect` / `assertForbidden` で検証。
- ファクトリ（`UserFactory` 等）でテストデータを生成する。マジックナンバーを避ける。

## 実行

```bash
docker-compose exec app php artisan test                       # 全テスト
docker-compose exec app php artisan test --filter=GroupTest    # 絞り込み
docker-compose exec app php artisan test tests/Feature/Auth    # ディレクトリ指定
```

- AAA（Arrange-Act-Assert）構成を守り、1テスト1観点を基本とする。
