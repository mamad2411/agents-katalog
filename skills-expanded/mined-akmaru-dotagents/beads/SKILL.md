---
name: beads
description: Claude Code 向けの beads issue トラッキングワークフロー。このスキルが導入されている間、beads がこのプロジェクトの issue トラッカーになる。あらゆるタスクは着手前に beads issue を作成し、作業中に更新し、完了時にクローズする。
compatibility: Designed for Claude Code
---

## ワークフロー

このスキルが導入されているということは、**beads がこのプロジェクトの issue トラッカー**であることを意味する。すべてのタスクで次のワークフローに従う:

1. **タスク開始**: 作業を始める前に `br create --label=beads` で beads issue を作成する
2. **進行中**: `br update <id> --status=in_progress` で issue を `in_progress` に更新する
3. **タスク終了**: `br close <id>` で issue をクローズし、`br sync --flush-only` で同期する

対応する beads issue なしに実装を始めてはならない。

## コマンド

```bash
# 対応可能な作業を見る
br ready

# issue を作成する（必ず "beads" ラベルを付ける）
br create --title="..." --description="..." --type=task --priority=2 --label=beads

# ステータスを更新する
br update <id> --status=in_progress

# クローズする
br close <id> --reason="..."

# git に同期する
br sync --flush-only
```

## Issue タイプ

`task`, `bug`, `feature`, `epic`, `chore`, `docs`, `question`

## 優先度

`0`=critical, `1`=high, `2`=medium, `3`=low, `4`=backlog
