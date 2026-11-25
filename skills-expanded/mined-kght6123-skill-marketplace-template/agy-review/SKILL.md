---
name: agy-review
description: Use this skill when the user asks to run a code review using agy or
  Antigravity CLI, review changed files with agy, perform agy code review, or
  check code quality with agy. Triggers on "agyでレビュー", "agy review", "agy を使ってレビュー",
  "agy でコードレビューしてください", or "run agy review on this code".
argument-hint: <path/to/file.ts or empty for git diff>
---

# agy コードレビュー

`agy`（Antigravity CLI）を使ってコードレビューを実行するスキルです。

## 手順

### 1. レビュー対象ファイルの決定

引数がある場合はそのファイルを対象にする。引数が空の場合は下記コマンドで変更ファイルを取得する:

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

### 2. ファイル内容の読み込み

対象ファイルをすべて Read ツールで読み込む。

### 3. レビュープロンプトの構築と実行

以下の内容を `/tmp/agy_review_prompt.txt` に Write ツールで書き出す:

```
以下のコードをレビューしてください。

観点:
- 型安全性・TypeScriptの使い方（any の乱用・型アサーションの適切さなど）
- 関数・変数・型の命名
- 処理の効率・重複コード
- エラーハンドリング（例外の捕捉・エラーメッセージの品質）
- コメント・ドキュメントの適切さ
- バグ・潜在的な問題
- セキュリティ上の懸念

レビュー結果は問題点と改善提案を箇条書きでまとめ、深刻度（高/中/低）も付けてください。

=== レビュー対象ファイル ===

{読み込んだ各ファイルのパスと内容}
```

次のコマンドを Bash ツールで実行する（timeout: 600000ms）:

```bash
agy --print "$(cat /tmp/agy_review_prompt.txt)" --print-timeout 10m
```

### 4. 結果の提示

agy の出力をユーザーに提示する。指摘が複数ある場合は「修正しますか？」と確認する。

## 注意事項

- `agy` コマンドが PATH に存在しない場合はインストールを促す
- レビュー対象ファイルが存在しない場合はエラーを表示する
- プロンプトが長大になりすぎる場合はファイルを分割してレビューする
