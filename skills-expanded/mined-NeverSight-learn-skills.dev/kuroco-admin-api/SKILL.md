---
name: kuroco-admin-api
metadata:
  author: Diverta inc.
  version: "2.0.0"
  lastUpdated: "2026-03-04"
description: >
  Kuroco管理API（admin_api）をCLI（kuroco-admin）で操作するスキル。
  Bashツールからコマンド一発でAPI実行・探索・スキーマ取得が可能。
  使用キーワード：「admin_api」「管理API」「管理APIゲートウェイ」
  「admin API」「management API」「CLIでAPI実行」
  「管理画面操作」「管理画面でデータ操作」「記事を作成して」
  「コンテンツをAPIで」「APIモデル一覧」「メソッド一覧」
  「discover」「llms.txt」「管理APIを実行」
  「Topics作成」「Member登録」「コンテンツ定義一覧」
  「kuroco-admin」「admin CLI」「管理API CLI」。
  admin_apiの実行、API探索、スキーマ取得に関する質問で使用。
---

# Kuroco Admin API Skill

## 概要

Kuroco管理API（admin_api）を `kuroco-admin` CLIで操作するスキル。

**admin_apiの5つのモード:**
- **whoami**: セッション情報の取得 — member_id, name, group_ids を返す
- **discover**: 利用可能なモジュール・コントローラの探索
- **schema**: コントローラ/サービスのリクエスト・レスポンススキーマ取得
- **advise**: 自然言語でやりたいことを伝えると、呼ぶべきAPIと手順をAIが回答
- **execute**: APIの実行（GET/POST） — `--columns`でレスポンスカラム選択可能

**認証方式:** `kuroco-admin login` でセッションCookieを `~/.kuroco-admin/cookies.txt` に永続化。以降のコマンドは自動的にCookieを送信。

**前提条件:**
- Bun ランタイムがインストール済み
- `kuroco-admin` CLI がビルド済みまたはPATHに追加済み
- `kuroco-admin login --url <管理画面URL>` でログイン済み
- すべての操作はログイン中ユーザーの権限で実行される

> **最小操作フロー（読み取り: 2-3回、書き込み: 3-4回の tool call）:**
> 1. `Bash`: 認証チェック（`kuroco-admin whoami --json`）
> 2. `Bash`: API構造把握（`kuroco-admin discover --json` または `kuroco-admin advise "やりたいこと" --json`）
> 3. **（書き込み時）** `Bash`: スキーマ取得（`kuroco-admin help topics/topics_edit --json`）
> 4. `Bash`: API実行（`kuroco-admin exec ...`）
>
> **advise が最も効率的。** やりたいことを自然言語で伝えるだけで、呼ぶべきAPI・手順・パラメータをAIが回答する。mt/ctが不明な場合はまず advise を使う。

---

## セットアップ

### インストール

```bash
# CLI ソースディレクトリ
cd /path/to/admin_cli

# ビルド（スタンドアロンバイナリ）
bun build --compile kuroco-admin.ts --outfile kuroco-admin

# PATHに追加（任意）
cp kuroco-admin /usr/local/bin/
```

### ログイン

```bash
kuroco-admin login --url https://example.g.kuroco-mng.app
# → メールアドレスとパスワードを対話的に入力
# → ~/.kuroco-admin/config.json と cookies.txt が保存される
```

---

## 操作フロー

**すべてのAPI操作はこのフローに従うこと。**

### Step 1: 認証チェック

```bash
kuroco-admin whoami --json
```

- **成功（exit 0）** → `{"success":true,"data":{"member_id":...}}` が返る → Step 2 へ
- **失敗（exit 2）** → セッション切れ。`kuroco-admin login --url <URL>` で再ログイン

### Step 2: API構造把握

目的に応じて3つの方法を使い分ける:

#### 方法A: advise（AI支援、推奨）

やりたいことを自然言語で伝えると、呼ぶべきAPIと手順をAIが回答:

```bash
kuroco-admin advise "記事を新しく作成したい" --json
```

レスポンスの `steps` にmt/ct/http_method/mode/endpointが含まれる。`endpoint` と `api_spec` はシステム自動生成（ハルシネーションなし）。`summary`, `description`, `body_example` はAI生成。

#### 方法B: discover（モジュール・コントローラ一覧）

```bash
# 全モジュール一覧
kuroco-admin discover --json

# 特定モジュールのコントローラ一覧
kuroco-admin discover --mt topics --json
```

#### 方法C: help（スキーマ取得）

特定コントローラのリクエスト/レスポンススキーマ:

```bash
kuroco-admin help topics/topics_edit --json
```

> **使い分け:**
> | 方法 | 用途 |
> |------|------|
> | **advise**（推奨） | やりたいことからAPI手順をAIが提案（mt/ctが不明な場合） |
> | **discover** | プログラム的にモジュール/コントローラを列挙 |
> | **help** | 特定コントローラのフィールド定義・型・必須項目を確認 |

### Step 3: スキーマ取得（書き込み操作では必須）

書き込み操作（INSERT/UPDATE）では必ずスキーマを取得してフィールド構造を確認:

```bash
kuroco-admin help topics/topics_edit --json
```

レスポンスはJSON Schema形式。`data.request.properties` にフィールド定義、`data.request.required` に必須フィールドが格納される。

**ext_colを含むスキーマが必要な場合:**

`help` コマンドでは `topics_group_id` を指定できないため、`exec` で直接取得:

```bash
kuroco-admin exec --param MODE=schema --mt topics --ct topics_edit --param topics_group_id=99 --json
```

> **注意:**
> - `topics_group_id` を省略すると汎用フィールドのみ（ext_colが含まれない）
> - `topics_group_id` を指定するとブロックエディタ・拡張項目のフィールド名（`ext_1`, `ext_14` 等）、型、必須フラグが取得できる
> - list系コントローラ（`topics_list`等）はスキーマが空を返すため、書き込み用コントローラ（`topics_edit`）を指定すること
> - レスポンスの `x-kuroco-type` でフィールドの種類（`wysiwyg`, `json`, `checkbox`, `file` 等）がわかる

### Step 4: API実行

認証確認・構造把握が完了したら、[API実行パターン](#api実行パターン)に従ってAPIを実行する。

### Step 5: 認証失敗・セッション切れ対応

exit code 2（AUTH_ERROR / SESSION_EXPIRED / LOGIN_REQUIRED）が返った場合:
1. ユーザーに再ログインが必要な旨を伝える
2. `kuroco-admin login --url <URL>` を実行
3. ログイン後に再度操作

複数ステップの操作中に認証エラーが発生した場合:
1. **即座に操作を停止**
2. どこまで成功したかをユーザーに報告
3. 再ログインを案内
4. 再認証後、未完了の操作から再開

---

## API実行パターン

### パラメータ形式

`kuroco-admin exec` では `module/controller` のショートハンド形式、または `--mt`/`--ct` 個別指定が使える。

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `mt` | モジュール名（小文字） | `topics`, `member`, `inquiry` |
| `ct` | コントローラ名 | `topics_list`, `topics_edit`, `member_list` |

```bash
# ショートハンド形式（推奨）
kuroco-admin exec topics/topics_list --json

# 個別指定
kuroco-admin exec --mt topics --ct topics_list --json
```

> **注意**: `model/method` 形式は使用しないこと。HTMLが返却される場合がある。必ず `mt/ct` 形式を使用する。

### GETリクエスト（一覧取得・検索）

```bash
# 基本的な一覧取得（columns + cnt で最小限のレスポンス）
kuroco-admin exec topics/topics_list \
  --param "topics_group_id[]=1" \
  --param cnt=10 \
  --columns topics_id,subject,ymd \
  --json

# 検索・フィルタリング
kuroco-admin exec topics/topics_list \
  --param "topics_group_id[]=1" \
  --param keyword=検索語 \
  --param cnt=20 \
  --columns topics_id,subject \
  --json

# ページネーション
kuroco-admin exec topics/topics_list \
  --param "topics_group_id[]=1" \
  --param pageID=2 \
  --param cnt=20 \
  --json
```

> **columns原則**: GETリクエストでは常に `--columns` を指定。対応エンドポイントではサーバー側フィルタリング、非対応でも無視されるだけなので常に指定して問題ない。

### POSTリクエスト（作成・更新・削除）

```bash
# 新規作成（INSERT）
kuroco-admin exec topics/topics_edit_api \
  --MODE INSERT \
  --data '{"subject":"タイトル","contents":"本文","topics_group_id":1}' \
  --json

# 更新（UPDATE）
kuroco-admin exec topics/topics_edit_api \
  --MODE UPDATE \
  --data '{"topics_id":123,"subject":"更新後タイトル"}' \
  --json

# 削除（DELETE）
kuroco-admin exec topics/topics_edit_api \
  --MODE DELETE \
  --data '{"topics_id":123}' \
  --json
```

### dry-run（プレビュー）

実行前にリクエスト内容を確認:

```bash
kuroco-admin exec topics/topics_edit_api \
  --MODE INSERT \
  --data '{"subject":"テスト"}' \
  --dry-run
```

### サービス呼び出し

コントローラ（小文字開始）とサービス（大文字開始）を自動判別:

```bash
# コントローラ: 小文字開始
kuroco-admin exec topics/topics_list --json

# サービス: 大文字開始（PHP側で自動検出）
kuroco-admin exec Email/send --data '{"to":"user@example.com","subject":"件名"}' --json
```

### 重要なルール

| ルール | 説明 |
|--------|------|
| **--json フラグ** | AI agent からの呼び出しでは常に `--json` を指定 |
| **GET配列パラメータ** | `--param "topics_group_id[]=1"` のように `[]` suffix必須 |
| **POST配列パラメータ** | `--data` 内でネイティブJSON配列（例: `{"topics_group_id": [1]}`） |
| **件数制限** | レスポンスが大きい場合は `--param cnt=N` で制限 |
| **columns指定** | `--columns col1,col2` でレスポンスカラムを最小限にする |
| **変更操作の確認** | INSERT/UPDATE/DELETEは**実行前にユーザーに確認**すること |
| **dry-run活用** | 書き込み操作の前に `--dry-run` でリクエスト内容を確認 |

> 詳細は [references/cli-commands.md](references/cli-commands.md) を参照

---

## レスポンス構造

### 成功レスポンス（--json）

```json
{
  "success": true,
  "data": { ... },
  "errors": []
}
```

### エラーレスポンス（--json）

```json
{
  "success": false,
  "data": null,
  "errors": [{ "code": "API_ERROR", "message": "..." }]
}
```

### リストレスポンスのキー

レスポンス内のリスト配列のキーは `ct` に対応:

| ct | レスポンスのリストキー |
|----|---------------------|
| `topics_list` | `data.topics_list` |
| `topics_group_list` | `data.topics_group_list` |
| `member_list` | `data.member_list` |

### ページネーション

```json
{
  "pageInfo": {
    "totalCnt": 150,
    "perPage": 20,
    "totalPageCnt": 8,
    "pageNo": 1
  }
}
```

---

## エラーハンドリング

### Exit Codes

| Code | 意味 | 対処 |
|------|------|------|
| **0** | 成功 | — |
| **1** | 一般エラー（INVALID_PARAM, NETWORK_ERROR, API_ERROR） | エラーメッセージ確認、パラメータ修正 |
| **2** | 認証エラー（AUTH_ERROR, SESSION_EXPIRED, LOGIN_REQUIRED） | `kuroco-admin login` で再ログイン |

> 詳細は [references/error-handling.md](references/error-handling.md) を参照

---

## モジュール関係マップ

主要な親子関係。親のIDが子の操作に必須:

```
TopicsGroup → Topics         (topics_group_id 必須)
MemberGroup → Member         (group_id 必須)
InquiryForm → InquiryMessage (inquiry_id 必須)
TagCategory → Tag            (tag_category_id 必須)
```

操作前に親のlistで利用可能なグループを確認:

```bash
kuroco-admin exec topics/topics_group_list --columns topics_group_id,group_nm --json
```

> 詳細は [references/api-discovery.md](references/api-discovery.md) を参照

---

## セキュリティ注意事項

- **Cookie値を表示・ログ出力しないこと** — `~/.kuroco-admin/cookies.txt` はmode 0o600で保護
- **`--verbose` の出力をユーザーに見せない** — HTTPヘッダーにCookie値が含まれる
- **変更操作は必ずユーザー確認後に実行** — INSERT/UPDATE/DELETEは取り消しが困難
- **`--dry-run` を活用** — 書き込み前にリクエスト内容をプレビュー
- **APIレスポンスのファイル保存はユーザー同意必須** — 個人情報を含む可能性

---

## アンチパターン

| やりがち | 問題 | 推奨 |
|---------|------|------|
| `--json` を付けずに実行 | 人間向けフォーマットでパースしにくい | AI agentでは常に `--json` |
| `--columns` を指定せずにGET | レスポンスが巨大 | 常に `--columns` を指定 |
| exit code を確認しない | 認証切れに気づかない | exit code 2 なら再ログイン |
| schema なしで書き込み | 必須フィールド漏れ | `help` でスキーマ確認後に実行 |
| `--verbose` 出力をログに残す | Cookie値が漏洩する | デバッグ時のみ使用、出力は共有しない |
| `model/method` 形式でAPI指定 | HTMLが返却される場合がある | 必ず `mt/ct` 形式を使用 |

---

## 並列実行

独立したAPI呼び出しは複数の Bash tool call を同時に発行して並列実行可能:

```bash
# 別々のBash tool callで同時発行
kuroco-admin exec topics/topics_group_list --columns topics_group_id,group_nm --json
kuroco-admin exec member/member_group_list --columns group_id,group_nm --json
```

---

## 他スキルとの連携

| スキル | 用途 | 使い分け |
|--------|------|----------|
| `/kuroco-api-content` | フロントエンドAPI設計・認証パターン、コンテンツCRUDパターン | エンドユーザー向けAPI |
| `/kuroco-frontend-integration` | Nuxt.js/Next.js統合、AI自動デプロイ | フロントエンド実装 |
| `/kuroco-docs` | Kurocoドキュメント参照 | 公式ドキュメント検索 |

**本スキルはCLI経由のadmin_api実行に特化。** フロントエンドAPI（`*.g.kuroco.app`）の操作には上記の関連スキルを使用。
