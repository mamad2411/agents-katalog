---
name: dev-daily
description: >
  開発者の日常ワークフロー支援。自分にアサインされたタスクの把握と、日報の自動生成を行う。
  使用タイミング: (1) 「自分のタスク」「何やればいい」「アサインされてる」などタスク確認
  (2) 「日報」「今日やったこと」「report」「slack」など日報作成
  (3) 朝の作業開始時や夕方の作業終了時
---

# Dev Daily Skill

開発者の日常を支援する。タスク把握と日報生成の2つの機能を持つ。

## 1. タスク把握

自分にアサインされているタスクをGitHub Projectから取得し、整理して表示する。

### 手順

1. `gh api graphql -f query='{ viewer { login } }'` で自分のユーザー名を取得
2. `gh repo view` で owner/repo を取得
3. `gh project item-list {number} --owner {owner} --format json` で全アイテムを取得
4. 自分がAssigneeのアイテムをStatus別に分類して表示

### 表示形式

```
## あなたのタスク

### In Progress
- #XX Issue名

### Ready
- #XX Issue名

### Backlog
- #XX Issue名
```

## 2. 日報生成

今日の活動をGitHub上のデータから自動収集し、Slackに貼れる日報を生成する。

### データ収集手順

以下を順番に収集する。**今日のコミットやPRがゼロでも日報をスキップしてはいけない。**
その場合、直近のgit活動・ワーキングツリーの変更・Issue状況から分かる範囲で記述する。

1. **今日のコミット**: `git log --author="{user}" --since="today 00:00" --format="%h %s" --reverse`
2. **今日のPR活動**: `gh pr list --author {user} --state all --search "created:>=YYYY-MM-DD" --json number,title,url,state`
3. **コミット/PRがない場合の補完情報**:
   - `git diff --stat` で未コミットの作業中ファイルを確認
   - `git log --author="{user}" --since="3 days ago" --format="%h %s %ad" --date=short --reverse` で直近の活動を確認
   - `git stash list` でスタッシュされた作業を確認
   - これらの情報から「今日取り組んでいた内容」を推定して記述する
4. **Issueのステータス変化**: Project itemsから自分のIn Progress / DoneのIssueを確認
5. **明日やること**: Ready / In ProgressのIssueから次のタスクを推定

### 日報フォーマット（Slack貼り付け用）

```
【日報】YYYY/MM/DD

■ やったこと
- #XX Issue名: やったことの要約（PR: リポジトリURL/pull/YY）
- コミット: リポジトリURL/commit/abc1234
- レビュー対応など

■ 困っていること / 相談
- （ユーザーに確認する）

■ 明日やること
- #XX Issue名
```

### 重要なルール

- 「やったこと」には、PRやコミットが存在する場合は必ずリンクを含める
  - PR: `https://github.com/{owner}/{repo}/pull/{number}`
  - コミット: `https://github.com/{owner}/{repo}/commit/{hash}`
- 「困っていること」は自動生成せず、ユーザーに確認する
- 「明日やること」はReady/In Progressから推定するが、ユーザーに確認してから確定する
- 日報は生成後、ユーザーに提示して修正の機会を与える。そのままコピペできる形で出力する
