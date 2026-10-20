---
description: 新しい案件（エピック）ノートを作成する。1 エピック = 1 機能（基本は 1 feature/ ブランチ）。例: /epic-new 釣果投稿機能
disable-model-invocation: true
---

新しい案件ノートを作成します。案件名: `$ARGUMENTS`

手順:
1. **ブランチ確認**: `git rev-parse --abbrev-ref HEAD` で現在のブランチを確認する。`main`/`dev` 上なら、先に `dev` から `feature/<内容>` を切るよう促す（`.claude/rules/git-workflow.md`）。
2. **slug 決定**: 案件名から半角英小文字・数字・ハイフンの `<slug>` を決める（例: `釣果投稿機能` → `catch-post`）。可能なら現在の `feature/` ブランチ名に合わせる。
3. **生成**: `.claude/epics/_TEMPLATE.md` を元に `.claude/epics/<slug>/_epic.md` を作成し、`<案件名>`・`<slug>`・`feature/<内容>`・作成日（今日）・概要を埋める。`.claude/epics/<slug>/tasks/` も用意する。
4. **報告**: 作成したパスと、ユーザーに確認したい未確定の前提・未解決事項があれば最小限だけ質問する。

機密（個人情報・釣果座標・`.env` 値）は書かないこと（`.claude/rules/security.md`）。詳細は `epic-knowledge` スキル参照。
