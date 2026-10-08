---
name: doc-ship
description: .claude/ への変更をブランチ作成 → PR 作成（open）で反映する。マージは GitHub 上でユーザーが行う。グローバル（~/.claude/）とプロジェクト（.claude/）の両方に対応。
---

# Doc Ship Skill

## Overview

`/retro` で承認された `.claude/` への変更を GitHub 経由で安全に反映する。
PR は **open のまま作成**し、マージは GitHub 上でユーザーが行う。

```
変更ファイルを確認
  ↓
対象リポジトリを判定（グローバル / プロジェクト）
  ↓
ブランチ作成
  ↓
コミット
  ↓
PR 作成（open のまま）
  ↓
URL を報告して終了
```

---

## Step 1: 変更ファイルの確認

変更対象がどちらに属するかを確認する：

| 変更先 | リポジトリ | 作業ディレクトリ |
|--------|-----------|----------------|
| `~/.claude/` 以下 | `claude-config` | `~/.claude/` |
| プロジェクトの `.claude/` 以下 | そのプロジェクトの src リポジトリ | `~/Documents/dev/{name}/src/` |

両方に変更がある場合は、グローバルとプロジェクトで**それぞれ別に**ブランチ・PR を作成する。

---

## Step 2: グローバル変更の ship（~/.claude/ が対象の場合）

```bash
git -C ~/.claude status
```

ブランチ名は `retro/YYYY-MM-DD/{slug}` 形式：

```bash
git -C ~/.claude checkout -b retro/2026-04-25/fix-something
```

```bash
git -C ~/.claude add {変更ファイル}
```

```bash
git -C ~/.claude commit -m "retro: （変更内容の要約）"
```

```bash
git -C ~/.claude fetch origin
git -C ~/.claude rebase origin/main
```

```bash
git -C ~/.claude push -u origin retro/2026-04-25/fix-something
```

PR を作成（open のまま）：

```bash
gh pr create --repo katsushigematsuyama2548/claude-config \
  --title "retro: （変更内容の要約）" \
  --body "## 変更内容\n\n（/retro で承認された提案の内容）" \
  --base main \
  --head retro/2026-04-25/fix-something
```

main に戻る：

```bash
git -C ~/.claude checkout main
```

---

## Step 3: プロジェクト変更の ship（.claude/ が対象の場合）

現在のプロジェクト名を確認し、作業ディレクトリに移動する。

ブランチ名は `claude/retro/YYYY-MM-DD/{slug}` 形式：

```bash
cd ~/Documents/dev/{PROJECT_NAME}/src
git checkout -b claude/retro/2026-04-25/fix-something
```

```bash
git add .claude/{変更ファイル}
```

```bash
git commit -m "claude: retro（変更内容の要約）"
```

```bash
git fetch origin
git rebase origin/main
```

```bash
git push -u origin claude/retro/2026-04-25/fix-something
```

```bash
gh pr create \
  --title "claude: retro（変更内容の要約）" \
  --body "## 変更内容\n\n（/retro で承認された提案の内容）" \
  --base main \
  --head claude/retro/2026-04-25/fix-something
```

```bash
git checkout main
```
