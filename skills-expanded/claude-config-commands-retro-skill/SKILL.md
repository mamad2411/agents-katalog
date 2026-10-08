---
name: retro
description: セッション終了時に振り返りを行い、~/.claude/ またはプロジェクト .claude/ への更新を提案する。継続的に Claude Code を育てるための自己強化ループ。
---

# Retro Skill

## Overview

このスキルは知識の複利ループを自動化する：

```
セッション作業（調査・実装・バグ修正など）
  ↓
Retro: 今日何を学んだか？
  ↓
Propose: どの .claude/ ファイルを更新すべきか？+ どこに置くか？
  ↓
Approve: ユーザーが各提案を承認 / 却下 / 配置先変更
  ↓
Apply: 承認された変更を実際に適用
```

---

## Step 1: セッション文脈の収集

会話履歴を振り返り、以下を検出する：

| 検出項目 | 具体例 |
|---------|--------|
| ハマった・時間を使った箇所 | 「Supabase の RLS ポリシーで20分詰まった」 |
| 新しく使った技法・パターン | 「NativeWind で動的スタイルを inline style で解決」 |
| ワークフローのギャップ | 「EAS Submit の手順がドキュメント化されていない」 |
| 毎回説明が必要だった知識 | 「このプロジェクトの Supabase ref は〇〇」 |
| 繰り返し実行した手順 | 「同じデプロイコマンドを3回実行した」 |
| エージェント・スキルへの改善点 | 「supabase-engineer がこのパターンを知らなかった」 |
| 3回繰り返した判断・手順 | → Skill 化を提案する |

---

## Step 2: 提案の生成

各学びに対して、具体的なファイル編集と**配置先**を提案する。

### 配置先の判断基準

| 条件 | 提案先 |
|------|--------|
| どのプロジェクトでも使える汎用的な知識・手順 | グローバル `~/.claude/` |
| 特定のプロジェクト固有の手順・設定・知識 | プロジェクト `.claude/` |

### 提案の形式

各提案を以下の形式で出力する：

```
---
【提案 N】
種別: [新規スキル / スキル更新 / エージェント更新 / CLAUDE.md 追記]
タイトル: （何をするか一言で）
配置先: グローバル (~/.claude/skills/) または プロジェクト (.claude/skills/)
理由: （なぜその配置先か）
内容:
（追加・変更するMarkdownの具体的な内容）
---
```

### 提案の対象ファイル

- `~/.claude/skills/` または `.claude/skills/` — 繰り返し作業を新スキル化
- `~/.claude/agents/` — エージェント定義の改善・知識追加
- `~/.claude/commands/` または `.claude/commands/` — 新コマンドの追加
- `.claude/rules/` — ファイルパスに応じて自動ロードされるルール（例: `rules/supabase.md`）
- `.claude/docs/` — ドメイン知識・設計書・注意事項など参照用ドキュメント
- `.claude/CLAUDE.md` — プロジェクト固有の注意事項・コンテキスト追加
- `~/.claude/CLAUDE.md` — 全プロジェクト共通のルール追加（3行を超えないよう注意）

---

## Step 3: 差分プレビューとユーザー承認

全提案を出力した後、以下を確認する：

1. 各提案に対してユーザーが「承認 / 却下 / 配置先変更」を選択
2. 承認された提案のみを適用する
3. 提案が0件の場合は「今日のセッションで記録すべき学びはありませんでした」と伝える

---

## Step 4: 適用（提案ごとに個別 PR）

承認された提案を **1 つずつ** 処理する。PR は open のまま作成し、マージは GitHub 上でユーザーが行う。

### グローバル変更（~/.claude/）の場合

ブランチ名: `retro/YYYY-MM-DD/{proposal-slug}`
（proposal-slug = 提案を表す短い英語。例: `fix-doc-ship-pr-merge`）

```bash
# 1. ファイルを適用（Write / Edit ツール）

# 2. ブランチ作成
git -C ~/.claude checkout -b retro/2026-04-25/fix-doc-ship-pr-merge

# 3. ステージ・コミット
git -C ~/.claude add {変更ファイルパス}
git -C ~/.claude commit -m "retro: （提案タイトル）"

# 4. コンフリクト確認（push 前に rebase）
git -C ~/.claude fetch origin
git -C ~/.claude rebase origin/main
# コンフリクトが出た場合は解消してから続行

# 5. プッシュ
git -C ~/.claude push -u origin retro/2026-04-25/fix-doc-ship-pr-merge

# 6. PR 作成（open のまま — GitHub でユーザーがマージ）
gh pr create --repo katsushigematsuyama2548/claude-config \
  --title "retro: （提案タイトル）" \
  --body "## 変更内容\n\n（提案の内容）" \
  --base main \
  --head retro/2026-04-25/fix-doc-ship-pr-merge

# 6. main に戻る
git -C ~/.claude checkout main
```

→ **次の提案へ繰り返す**

### プロジェクト変更（.claude/）の場合

ブランチ名: `claude/retro/YYYY-MM-DD/{proposal-slug}`

```bash
cd ~/Documents/dev/{PROJECT_NAME}/src
git checkout -b claude/retro/2026-04-25/fix-something
git add .claude/{変更ファイル}
git commit -m "claude: retro（提案タイトル）"
git fetch origin
git rebase origin/main
git push -u origin claude/retro/2026-04-25/fix-something
gh pr create --title "claude: retro（提案タイトル）" \
  --body "## 変更内容\n\n（提案の内容）" \
  --base main \
  --head claude/retro/2026-04-25/fix-something
git checkout main
```

→ **次の提案へ繰り返す**

全提案の PR を作成したら URL 一覧を報告する。

---

## Step 5: GC チェック

全提案の適用が完了したら、Skill ツールで `gc` スキルを呼び出す。

- 候補なし → セッション完了
- 候補あり → GC スキルの指示に従い、ユーザー確認の上 PR を作成する
