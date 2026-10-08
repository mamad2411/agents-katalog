---
name: bye
description: 終業時のWBS更新と引き継ぎメモ生成。task.mdを元にWBSを更新し、確認後に原本を上書きする。
---

# /bye — 終業処理

## Overview

終業時の「今日やったことをWBSに反映する」作業を自動化するスキル。

**なぜ draft → 確認 → 上書きという2段階か**
WBS の origin ファイルはチーム共有の Excel（`/mnt/r/...`）。
自動で即上書きすると誤更新が全員に影響するため、
デスクトップに draft を作って目視確認してから上書きという設計にしている。

**引き継ぎメモの考え方**
中途半端に終わったタスクのみ記録する。完了タスクは WBS に状態が入るので不要。
翌朝の `/ohayo` がこのメモを読んで「昨日どこで止まったか」を計画に反映する。

**この3スキルのセット設計**
`/ohayo`（朝：計画）→ `/tf`（随時：進捗記録）→ `/bye`（夕：WBS反映・引き継ぎ）
の 1日サイクルで回す想定。

## Step 1: task.md を読む

Read ツールで `/mnt/c/Users/kmatuyama/Desktop/task.md` を読む。

完了タスク（`[x]`）と未完了タスク（`[ ]`）を把握する。

## Step 2: 各案件の WBS を読み込む

```bash
find ~/claude/dev/active -name "CLAUDE.md" -maxdepth 2
```

各 CLAUDE.md を Read ツールで読み込み、`origin:` パスを取得する。

各 origin パスに対して:

```bash
python3 ~/.claude/scripts/read_wbs.py "{origin_path}"
```

## Step 3: 更新箇所を判断する

task.md の完了タスク（`[x]`）と WBS を照合し、進捗ステータスを更新すべき行を特定する。

## Step 4: draft WBS をデスクトップに作成

```bash
python3 ~/.claude/scripts/update_wbs.py \
  "{origin_path}" \
  "/mnt/c/Users/kmatuyama/Desktop/wbs.xlsm" \
  '{updates_json}'
```

## Step 5: 変更箇所を報告してユーザー確認を取る

以下の形式で報告する:

```
WBS 更新内容（{PROJECT_NAME}）:
- {タスク名}: {old_status} → {new_status}

デスクトップに wbs.xlsm を作成しました。
確認して「OK」と言っていただければ原本を上書きします。
```

ユーザーが「OK」と回答するまで待機する。

## Step 6: 原本を上書きコピー

```bash
cp "/mnt/c/Users/kmatuyama/Desktop/wbs.xlsm" "{origin_path}"
```

## Step 7: 引き継ぎメモを生成

未完了タスク（`[ ]` のまま）があれば `~/claude/daily/YYYY-MM-DD.md` に書き込む:

```markdown
## 引き継ぎメモ

### 未完了タスク
- {PROJECT_NAME}: {タスク名} — {どこまでやったか}
```

完了タスクのみであれば引き継ぎメモは不要（ファイル作成不要）。
