---
name: commit
description: Execute semantic git commits with individual file staging, prefix selection, and split-commit enforcement. Use when committing code, managing git history, or when user mentions git/commit/push.
allowed-tools: Bash(git *), Read
---

# Git Commit

意味のあるコミット履歴を保つためのGitコミットスキル。

## 禁止事項

- `git add -A` / `git add .` 禁止（例外: `pnpx changeset version` の大量パッケージ更新時のみ）
- 以下をコミットメッセージに含めない:
  - `Generated with [Claude Code](https://claude.com/claude-code)`
  - `Co-Authored-By: Claude <noreply@anthropic.com>`

## ワークフロー

コピーして進捗を追跡:

Task Progress:

- [ ] Step 1: 状態確認
- [ ] Step 2: 変更分析・ファイル分類
- [ ] Step 3: Prefix選択・メッセージ生成
- [ ] Step 4: ユーザー確認
- [ ] Step 5: AskUserQuestionでコミット確認
- [ ] Step 6: 個別ステージング・コミット実行
- [ ] Step 7: 結果報告

### Step 1: 状態確認

```bash
git status
git diff
git diff --cached
git log --oneline -5
```

### Step 2: 変更分析・ファイル分類

変更ファイルを目的別にグループ化:

- テストコード
- 実装コード
- ドキュメント
- 設定ファイル

複数の目的が混在 → 分割コミットを提案。

### Step 3: Prefix選択・メッセージ生成

Prefix一覧は [prefix-reference.md](prefix-reference.md) を参照。

**メッセージフォーマット**:

```
<type>(<scope>): <subject>

<body>
```

- `<type>`: Prefix一覧から選択
- `<scope>`: 影響範囲（省略可）
- `<subject>`: 50文字以内
- `<body>`: 詳細（省略可、72文字折り返し）

### Step 4: ユーザー確認

以下を提示して確認:

- 提案するコミットメッセージ
- ステージング対象ファイル
- 分割が必要な場合はその提案

### Step 5: AskUserQuestionでコミット確認

この内容でコミットしていい？

1. OK. コミットして
2. NO. まだコミットしない
3. Type something.

### Step 6: 個別ステージング・コミット実行

```bash
git add path/to/file1.ts
git add path/to/file2.ts
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>
EOF
)"
```

### Step 7: 結果報告

コミット完了後に表示:

- コミットハッシュ
- コミットメッセージ
- 変更ファイル数

## 警告・中断

以下を検出した場合、**警告を表示し処理を中断**:

- `git add -A` / `git add .` の使用
- 不明確なコミットメッセージ（`update files`, `fix stuff`, `changes`, `wip`）
- 複数目的が混在するコミット

ユーザーが強制実行を明示しない限り続行しない。
