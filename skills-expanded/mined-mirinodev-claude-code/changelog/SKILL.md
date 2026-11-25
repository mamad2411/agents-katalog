---
name: changelog
description: Claude Codeの最新CHANGELOGを取得し、変更内容を日本語で解説する。ユーザーがClaude Codeの更新内容、最新バージョン、リリースノートについて聞いたときに使う。
argument-hint: [バージョン番号 例:2.1.33 | all]
allowed-tools: Bash(gh *), Bash(base64 *), Bash(awk *), WebFetch
disable-model-invocation: true
---

# /changelog

Claude Code の CHANGELOG を取得し、変更内容を日本語で解説する。

## ユーザーからの引数

$ARGUMENTS

## 実行フロー

### Step 1: CHANGELOG の取得

以下の優先順位でCHANGELOGを取得する：

**第一優先: GitHub API（gh CLI）**

```bash
gh api repos/anthropics/claude-code/contents/CHANGELOG.md --jq '.content' | base64 -d
```

**フォールバック: WebFetch**

gh CLI が使えない場合は WebFetch で以下のURLから取得：
`https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`

取得に失敗した場合はエラーメッセージを表示して終了する。

### Step 2: バージョンの抽出

CHANGELOG全文をコンテキストに入れない。必要なセクションのみ抽出する。

引数の解釈ルール：
- **引数なし** → 最新バージョン（最初の `## x.y.z` セクション）を抽出
- **バージョン番号指定**（例: `2.1.33`）→ 該当する `## 2.1.33` セクションを抽出
- **`all`** → 直近5バージョン分を抽出

抽出には以下のようなawkコマンドを使用する：

**最新バージョンの抽出:**
```bash
echo "$CHANGELOG" | awk '/^## [0-9]/{if(found) exit; found=1} found'
```

**特定バージョンの抽出:**
```bash
echo "$CHANGELOG" | awk '/^## TARGET_VERSION/{found=1} found && /^## [0-9]/ && !/^## TARGET_VERSION/{exit} found'
```

**直近5バージョンの抽出:**
```bash
echo "$CHANGELOG" | awk '/^## [0-9]/{count++; if(count>5) exit} count>=1'
```

指定バージョンが見つからない場合は、利用可能なバージョン一覧を表示して最新バージョンを提案する。

### Step 3: カテゴリ分類

抽出した変更内容を以下のカテゴリに分類する：

| カテゴリ | 判定キーワード |
|----------|---------------|
| 新機能 | Added, New, Now available, Introduced |
| 改善 | Improved, Updated, Changed, Enhanced, Better |
| バグ修正 | Fixed, Resolved, Corrected |
| 破壊的変更 | Breaking, Removed, Deprecated |

分類できないものは「その他」に入れる。

### Step 4: 日本語解説の出力

以下のフォーマットで出力する：

```
# Claude Code vX.Y.Z の変更点

## 新機能
- **機能名** (feature-name): ユーザーにとっての意味を解説
  - 技術的な補足があれば追記

## 改善
- **改善内容**: どう良くなったかを解説

## バグ修正
- **修正内容**: 何が直ったかを解説

## 破壊的変更
- **注目** **変更内容**: 影響範囲と対応方法を解説
```

### 出力ルール

- 単なる翻訳ではなく「ユーザーにとってどういう意味か」を解説する
- 技術用語は英語のまま残し、括弧で日本語補足を付ける
  - 例: `context window（コンテキストウィンドウ）`
- 特に重要な変更には「**注目**」マークを付ける
- 破壊的変更がある場合は冒頭に警告を出す

## エッジケース対処

| ケース | 対処 |
|--------|------|
| `gh` CLI未インストール | WebFetchにフォールバック |
| 指定バージョンが存在しない | 利用可能なバージョン一覧を表示し、最新バージョンを提案 |
| ネットワーク不可 | 「CHANGELOGの取得に失敗しました。ネットワーク接続を確認してください。」と表示 |

## 注意事項

- CHANGELOG全文をコンテキストに入れないこと。必要なセクションのみ抽出して処理する
- `all` 指定時でも直近5バージョンまでに制限する（コンテキスト節約のため）
