---
name: search-history
description: Only use when the user explicitly invokes /search-history (or $search-history in Codex). Never auto-invoke. Claude Code / Codex CLI のローカルチャット履歴（JSONL）をキーワードで横断検索し、該当するセッションと会話断片を提示する。履歴ファイルは読み取り専用で扱う。
disable-model-invocation: true
argument-hint: "[keyword] [--claude | --codex | --all] [--days N]"
metadata:
  tags: [search, history, chat-history, claude-code, codex, jsonl]
---

# search-history - チャット履歴検索

## 目的

Claude Code および Codex CLI のローカル履歴ファイル（JSONL）からキーワード検索を行い、該当するセッションと会話断片を提示する。両ツールの履歴を対等な検索対象として扱う。

## 引数の扱い

このスキルの起動時に渡される引数を以下のように分解する。

- **keyword**: 検索キーワード（必須）。スペース区切りで複数指定時は AND 検索
- **--claude**: Claude Code 履歴のみを対象にする
- **--codex**: Codex CLI 履歴のみを対象にする
- **--all**: 両方を対象にする（デフォルト）
- **--days N**: 直近 N 日間に絞る（デフォルト: 30）

引数は任意とし、キーワードが渡されていない場合はユーザーにキーワードの入力を求める。対象ツールの指定がない場合は両方（`--all`）を検索する。

## 検索対象パスとフォーマット

Claude Code と Codex CLI の履歴を対等に扱う。それぞれ以下のインデックスとセッション本体を持つ。

### Claude Code

- **インデックス**: `~/.claude/history.jsonl`
  - 各行: `{"display": "...", "timestamp": <unix_ms>, "project": "...", "sessionId": "..."}`
- **セッション本体**: `~/.claude/projects/<encoded-path>/<sessionId>.jsonl`
  - encoded-path はプロジェクトのフルパスの `/` や `.` 等の非英数字を `-` に変換したもの（例: `/Users/foo/myapp` → `-Users-foo-myapp`、`github.com` → `github-com`）。検索は find + grep で行うため、この規則からパスを再構成する必要はない
  - 各行: `{"type": "user"|"assistant"|..., "message": {"role": "...", "content": "..."}, "timestamp": "...", "sessionId": "..."}`

### Codex CLI

- **インデックス**: `~/.codex/history.jsonl`
  - 各行: `{"session_id": "...", "ts": <unix_sec>, "text": "..."}`
- **セッション本体**: `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl`
  - 各行: `{"type": "session_meta"|"response_item", "timestamp": "...", "payload": {"role": "user"|"developer"|"assistant", "content": [...]}}`
  - `session_meta` 行に `cwd`、`model_provider`、`cli_version` 等のメタ情報

## 基本方針

- **読み取り専用**: 履歴ファイルの編集・削除は行わない
- **効率的検索**: `grep` で絞り込んでから必要最小限を読む。大量のファイルを一括読み込みしない
- **センシティブ情報への配慮**: 出力はキーワード周辺の文脈に限定する

## 検索の進め方

### Step 1: キーワードと対象を確認

引数を解析し、検索キーワード・対象ツール・日数を確定させる。

### Step 2: Claude Code 履歴の検索（対象の場合）

1. `~/.claude/history.jsonl` から keyword を含む行を `grep -i` で抽出し、該当する sessionId と project を取得
2. `~/.claude/projects/` 配下の JSONL ファイルを `find` + `grep -l` で keyword にマッチするセッションファイルを特定
3. マッチしたセッションファイルから、keyword を含む行の前後 2 行を含めて抽出し、会話の文脈を確認

### Step 3: Codex CLI 履歴の検索（対象の場合）

1. `~/.codex/history.jsonl` から keyword を含む行を grep で抽出し、該当する session_id を取得
2. `--days` に基づき `~/.codex/sessions/YYYY/MM/DD/` の対象ディレクトリを絞り込む
3. 対象ディレクトリ内の JSONL ファイルに対して `grep -rl` でキーワードマッチするファイルを特定
4. マッチしたファイルの `session_meta` 行から cwd と timestamp を抽出しコンテキスト情報を付加
5. keyword を含む行の前後を抽出して会話断片を取得

### Step 4: 結果の整理と出力

マッチ結果を以下のフォーマットで提示する。ファイルが大量の場合は上位 20 件に絞る。

## 出力フォーマット

```
## 検索結果: "[keyword]"

### 検索条件
- 対象: Claude Code / Codex CLI / 両方
- 期間: 直近 N 日間
- ヒット数: Claude X 件 / Codex Y 件

### Claude Code セッション

#### 1. [プロジェクト名] - [日時]
- **Session ID**: `xxxx-xxxx-xxxx`
- **ファイル**: `~/.claude/projects/.../<id>.jsonl`
- **マッチ箇所**:
  > [keyword を含む会話の抜粋（前後の文脈付き）]

### Codex CLI セッション

#### 1. [作業ディレクトリ] - [日時]
- **ファイル**: `~/.codex/sessions/YYYY/MM/DD/rollout-....jsonl`
- **マッチ箇所**:
  > [keyword を含む会話の抜粋（前後の文脈付き）]

### ヒント
- Claude セッション再開: `claude --resume <sessionId>`
- Codex セッション再開: `codex resume <sessionId>`（直近のセッションは `codex resume --last`。`--resume` というフラグは存在しない）
- 詳細確認: 該当 JSONL ファイルを直接参照
```

## 制約

- 履歴ファイルの編集・削除は絶対に行わない（読み取り専用）
- 大量のファイルを一括 cat しない。`grep` で絞り込んでから必要最小限を読む
- セッション内容にはセンシティブ情報が含まれうるため、出力は検索キーワード周辺の文脈に限定する
- JSONL の各行を個別にパースできる前提で処理する（壊れた行はスキップ）
