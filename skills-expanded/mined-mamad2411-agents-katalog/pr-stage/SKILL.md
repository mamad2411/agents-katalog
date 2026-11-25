---
name: pr-stage
description: Only use when the user explicitly invokes /pr-stage (or $pr-stage in Codex). Never auto-invoke. 既にステージ済み（git add 済み）の変更だけをコミットし、必要ならフィーチャーブランチ作成・push・PR 作成まで行う。手順と安全ガードの正本は pr スキルにあり、本スキルはその差分（ステージ済み変更のみを扱う）だけを定義する薄型ラッパー。
disable-model-invocation: true
argument-hint: "[commit-message]"
metadata:
  tags: [git, commit, pull-request, staging, workflow, github]
---

# pr-stage（ステージ済み変更のコミット〜PR 作成）

既にユーザーが `git add` でステージした変更を、そのままコミットして PR まで運ぶ薄型ラッパースキル。判断ロジック・安全ガードの正本は `pr` スキルにあり、本スキルは差分だけを定義する（重複記述を持つと改訂時に食い違うため）。

## 明示起動限定

このスキルはコミット・push・PR 作成という不可逆かつ外部（リモート・GitHub）に影響する副作用を実行する。ユーザーが明示的に `/pr-stage`（Codex では `$pr-stage`）を起動した場合のみ実行する。会話の流れから自動発動してはならない。

## 手順

1. `pr` スキルの SKILL.md を Read する。パス解決: `~/.agents/skills/pr/SKILL.md`、無ければ checkout 側 `~/ghq/github.com/efoo-team/skills/skills/pr/SKILL.md`
2. 読み込んだ `pr` の「重要事項（ブランチ運用の絶対ルール）」「前提: プロジェクト規約への準拠」「実行フロー」「副作用実行前の確認」「PR 文章の作成」に、下記の差分を適用して従う

## pr との差分（本スキルの本義）

- **対象は「既にステージ済みの変更」のみ**。`git add` を新たに実行せず、ステージされていない変更・untracked ファイルは対象外として残す。ユーザーがステージした範囲はユーザーの選別結果であり、勝手に広げることはその選別を上書きする事故になる
- 実行冒頭に `git diff --staged --stat` でステージ内容を確認し、**ステージが空の場合は何もコミットせず停止**してユーザーに確認する
- 現在のブランチが保護ブランチ（develop / main / master）の場合は、`pr` の手順どおりフィーチャーブランチを作成してからコミットする（ステージ済み変更はブランチ切替後も保持される）
- 引数 `[commit-message]` が与えられた場合はコミットタイトルとして優先使用する

## 完了条件

- ステージ済み変更のみがコミットされ、push・PR 作成まで完了している（PR 本文は `pr` の手順に従い `pr-body` の実行フローで生成する）
- 作成した PR の URL をユーザーへ報告している
