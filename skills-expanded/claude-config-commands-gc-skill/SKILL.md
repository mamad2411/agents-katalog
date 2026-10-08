---
name: gc
description: ~/.claude/ とプロジェクト .claude/ の陳腐化ファイルを検出し、削除提案 PR を 1 ファイル 1 PR で GitHub に作成する。PR マージ = 削除承認、クローズ = 保持。
---

# GC (Garbage Collection) Skill

## 概要

長期間**使われていない** skills / commands / agents ファイルを検出し、GitHub PR を通じて削除を提案する。

```
最終使用日を取得（ログ優先 → git log フォールバック）
  ↓
閾値超過ファイルを一覧表示
  ↓
ユーザー確認
  ↓
1 ファイル 1 PR を作成
（マージ → 削除・ブランチ自動削除 / クローズ → 保持）
```

---

## Step 1: 使用日の取得方法

### ローカル実行時（推奨）

`~/.claude/skill-usage.jsonl` が存在する場合はこちらを優先する。
各行は `{"skill":"retro","timestamp":"2026-04-25T04:35:00Z"}` 形式。

```bash
# skill-usage.jsonl から特定スキルの最終使用日を取得
grep '"skill":"retro"' ~/.claude/skill-usage.jsonl | tail -1 | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['timestamp'][:10])"
```

ログにエントリがないスキルは「一度も使われていない」とみなし、git log の初回コミット日を使用日とする。

### リモートエージェント実行時（フォールバック）

`skill-usage.jsonl` はローカルファイルのため、リモートでは参照不可。git の最終コミット日で代替する：

```bash
git log -1 --format="%ai" -- {FILE_PATH}
```

---

## Step 2: 対象ディレクトリと閾値

### グローバル（~/.claude/）

| ディレクトリ | 閾値 |
|-------------|------|
| `skills/` | 60日 |
| `commands/` | 60日 |
| `agents/` | 90日 |

### プロジェクト（.claude/）

| ディレクトリ | 閾値 |
|-------------|------|
| `skills/` / `commands/` / `rules/` / `docs/` | 60日 |
| `agents/` | 90日 |

### 対象外（常に除外）

- `CLAUDE.md`, `settings.json`, `README.md`, `.gitignore`, `templates/`
- `commands/gc/`, `commands/retro/`, `commands/doc-ship/`, `commands/newproject/`

---

## Step 3: 検出結果の表示

```
## GC 候補一覧

### グローバル (~/.claude/)
| ファイル | 最終使用日 | 経過 | 判定根拠 | 閾値 |
|---------|-----------|------|---------|------|
| skills/vercel-react-native-skills | 2025-10-01 | 206日 | usage log | 60日 |
| agents/expo-mobile-engineer.md   | 2025-11-15 | 161日 | git log  | 90日 |

### プロジェクト (.claude/)
（なし）

PR を作成しますか？ (y / n / 個別指定)
```

0 件の場合は「陳腐化ファイルはありませんでした」と伝えて終了する。

---

## Step 4: PR の作成（1 ファイル 1 PR）

承認されたファイルそれぞれに対して実行する。

### グローバルファイルの場合

ブランチ名: `gc/{YYYY-MM-DD}/{sanitized-path}`
（sanitized-path = パスの `/` を `-` に置換。例: `skills-vercel-react-native-skills`）

```bash
cd ~/.claude
git checkout main
git pull
git checkout -b gc/2026-05-01/skills-vercel-react-native-skills
```

```bash
cd ~/.claude
git rm -r skills/vercel-react-native-skills/
```

```bash
cd ~/.claude
git commit -m "gc: remove stale skills/vercel-react-native-skills (206 days unused)"
```

```bash
cd ~/.claude
git push -u origin gc/2026-05-01/skills-vercel-react-native-skills
```

```bash
gh pr create \
  --repo katsushigematsuyama2548/claude-config \
  --title "gc: remove stale skills/vercel-react-native-skills" \
  --body "## 削除提案

**ファイル**: \`skills/vercel-react-native-skills/\`
**最終使用日**: 2025-10-01（206日前）
**判定根拠**: usage log
**閾値**: 60日

- **マージ** → 削除（ブランチ自動削除）
- **クローズ** → 保持（使い続ける場合は内容を更新してください）" \
  --base main \
  --head gc/2026-05-01/skills-vercel-react-native-skills
```

```bash
cd ~/.claude
git checkout main
```

### プロジェクトファイルの場合

ブランチ名: `claude/gc/{YYYY-MM-DD}/{sanitized-path}` で同様に実行する。`gh pr create` 時に `--repo` は不要。

---

## Step 5: 完了報告

```
## GC 完了

作成した PR：
- https://github.com/katsushigematsuyama2548/claude-config/pull/XX
- https://github.com/katsushigematsuyama2548/claude-config/pull/YY

各 PR をレビューして：
- マージ → 削除（ブランチ自動削除）
- クローズ → 保持

次回 /gc 推奨: {今日から60日後}
```

---

## 補足: skill-usage.jsonl について

- 場所: `~/.claude/skill-usage.jsonl`（ローカルのみ・git 管理外）
- 書き込み: `Skill` ツール実行後に `PostToolUse` フックが自動追記
- フォーマット: `{"skill":"retro","timestamp":"2026-04-25T04:35:00Z"}`
- リモートエージェント（月次スケジュール）では参照不可のため git log で代替
