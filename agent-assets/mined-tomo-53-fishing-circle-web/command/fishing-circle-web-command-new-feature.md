---
description: 新機能を end-to-end で開発するワークフロー。dev からブランチを切り、専門エージェントに分担して実装→テスト→レビュー→監査まで進める。
disable-model-invocation: true
---

新機能「`$ARGUMENTS`」を開発します。以下のワークフローで進めてください。

1. **ブランチ**: 現在のブランチを確認し、未作成なら `dev` から `feature/<内容>` を切る。
2. **案件ノート**: `/epic-new <内容>` で案件ノート `.claude/epics/<slug>/_epic.md` を作成し、概要・前提を記録する（`epic-knowledge` スキル）。
3. **計画**: 要件を自己完結タスクに分解する。不明点があれば最小限の質問で確定する。
4. **DB**: スキーマ変更が必要なら `db-migrator` エージェントへ（新規マイグレーションで前進）。
5. **実装**: バックエンドは `laravel-backend`、画面は `frontend-blade` に分担。同一ファイルの同時編集は避ける。
6. **テスト**: `pest-tester` で Pest テストを追加・実行。ACL の境界（権限不足/承認待ち/別グループ）を必ず網羅。
7. **検証**: `code-reviewer`（品質）と `security-auditor`（認可・入力・機密）でレビュー。指摘を反映。
8. **整形**: `docker-compose exec app ./vendor/bin/pint` で整形。
9. **ドキュメント**: 仕様変更があれば `docs-writer` で README/SETUP を更新。
10. **知識昇格**: `/epic-done` で決定/前提/学び/未解決を案件ノートへ昇格し、完了タスクを整理する。
11. **報告**: 変更概要・テスト結果・レビュー結果・残課題をまとめる。

大規模で並行性が高い場合は、Agent Team（リード＝あなた、または `commander` エージェント）の利用を検討してください。
`.claude/rules/` のセキュリティ・コーディング・テスト規約を厳守すること。
