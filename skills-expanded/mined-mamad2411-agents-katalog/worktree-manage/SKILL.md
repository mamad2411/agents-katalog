---
name: worktree-manage
description: "Manage git worktrees for parallel member work. Use when captain needs to create worktrees for parallel task execution, or when merging completed worktree branches."
user-invocable: false
---

# Worktree Management

## Task

並行タスク実行のための git worktree の作成・マージ・クリーンアップを管理する。

## Instructions

### 1. Worktree 判断基準

| 条件 | worktree | 理由 |
|------|----------|------|
| 複数memberが同一リポの異なるファイルを編集 | 推奨 | ファイルシステム分離で安全 |
| 同一ファイルへの書き込みが必要 | 不要（blocked_byで逐次） | worktreeでも解決しない |
| 編集ファイルが完全に分離 | 任意 | なくても可だがあると安全 |
| 異なるリポジトリを編集 | 不要 | そもそも競合しない |

### 2. Worktree 作成（隊長の責任）

```bash
scripts/worktree_manager.sh create <member_name> <branch_name>
# 例:
scripts/worktree_manager.sh create mika cmd_052/mika/auth-api
```

- cmd 開始時に並行作業が確定した段階で、全 worktree を一括作成する
- タスク YAML の `worktree_path` フィールドにパスを記載

### 3. ブランチ命名規則

```
cmd_{cmd_id}/{agent_id}/{short_description}
```

例: `cmd_052/mika/auth-api`, `cmd_160/hana/web-scripts`

### 4. 隊員側の手順

タスク YAML に `worktree_path` がある場合:
```bash
cd ${worktree_path}
```
worktree_path がない場合は通常のブランチ作成手順に従う。

### 5. マージ手順（隊長の責任）

```bash
# 1. レビュー
git log main..BRANCH --oneline && git diff main..BRANCH --stat

# 2. マージ（コンフリクト確認）
git merge --no-commit --no-ff BRANCH
# OK → git commit で確定
# コンフリクト → git merge --abort + 隊員に修正指示

# 3. Worktree クリーンアップ
scripts/worktree_manager.sh cleanup member_name

# 4. ブランチ削除
git branch -d BRANCH
```

### 6. main 直接作業の禁止

**全エージェント共通**: main ブランチでの直接作業は絶対禁止。
作業開始前に `git branch --show-current` で確認すること。

## Notes

- Worktree の作成・マージ・クリーンアップは隊長の責任。隊員は `cd` するだけ。
- RACE-001: 複数隊員が同一ファイルに書き込むことは禁止。worktree でも解決しない。
- main にいることに気づいた場合の緊急対応: `git stash` → 新ブランチ作成 → `git stash pop`
