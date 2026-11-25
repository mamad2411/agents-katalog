---
name: github-actions-ops
description: GitHub Actions の運用と gh CLI を使ったワークフロー調査・復旧パターン。`gh run watch` / `gh run view --log-failed` / `gh run download`、actions/cache@v4 のキー戦略、workflow_dispatch のみ運用、失敗時 Issue 自動作成、`gh secret`、permissions ブロック。CI 失敗の調査・ワークフロー復旧・cache 設計・artifact ダウンロード時に参照する。
---

# github-actions-ops

この skill の詳細手順は `~/.agents/references/github-actions-ops.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
