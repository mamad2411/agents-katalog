---
name: luno
description: Work with a connected LUNO project via MCP (luno-prod by default). Use when the user wants to build, operate, or inspect a LUNO backend. If MCP is disconnected, send them to `npx @luno-cms/mcp setup`. If 401 / expired / placeholder, send them to `npx @luno-cms/mcp login`.
argument-hint: "[status|prod|stg|dev|help]"
---

# LUNO

ユーザー引数: `$ARGUMENTS`

接続済みの LUNO を MCP で操作する。キーはチャットに出さない。フルキーを復唱しない（末尾数文字のみ確認可）。

## 未接続のとき

キーを聞かない。チャットに `sk-agent-` を出させない。

- **設定ファイルが無い**（初回）→ `npx -y @luno-cms/mcp setup`（ブラウザで確認。キーは聞かない）
- **401・期限切れ・プレースホルダ・clone 後にキーだけ無い** → `npx -y @luno-cms/mcp login`（ブラウザで確認。MCP 設定は作り直さない）

```bash
npx -y @luno-cms/mcp login
```

明示環境（アクセスがある人だけ）:

```bash
npx -y @luno-cms/mcp login --env stg
```

JSON の手書きや `.mcp.json` 解説を主経路にしない。

## 公開デフォルト

一般ユーザーが届くのは **prod**（`luno-prod` / `https://api.luno.rest/admin`）。
dev / stg は消さない。ユーザーが明示したときだけ使う。

- prod → `https://api.luno.rest/admin` → `luno-prod`
- stg → `https://stg-api.luno.rest/admin` → `luno-stg`（内部 / Benchmark / Partner）
- dev → `http://127.0.0.1:8787/admin` → `luno-dev`（ローカル）

アクティブ確認: `npx -y @luno-cms/mcp env active`

## 引数

空なら作業を続ける（セットアップウィザードを始めない）。

| 引数 | 動作 |
|------|------|
| （空） | 接続済み前提でユーザーの依頼を進める |
| `status` | `npx -y @luno-cms/mcp env status` を説明 |
| `prod` / `stg` / `dev` | `env has-key` が成功なら `env switch`。失敗なら login へ（設定が無ければ setup。キーを聞かない） |
| `help` または不明 | 下の使い方。推測でコマンドを増やさない |

```text
/luno              作業を続ける（接続済み前提）
/luno status       状態表示
/luno prod|stg|dev 環境切替（キーが無ければ login へ）
```

`/luno` はショートカット。入場券ではない。

## 最初の成功

最初の依頼は **一覧か下書き**。`publish` / スキーマ変更 / prod 公開は初回にしない。

## 作業ルール

1. 質問は 1 つずつ。
2. Form Set / Contact Form の削除や課金・メンバー管理はエージェントキーでは不可。
3. エントリ保存前に `get_form_set_schema` の `snapshotShape.example` を使い、`{ [formKey]: { [fieldKey]: value } }` で `save_revision` する。
4. 公開確認は `get_public_api_info` の `/public/p/{projectId}/v1`。
5. 以降の MCP ツールは **`luno-<active>`**（未指定なら **luno-prod**）を使う。
6. 必要なら「MCP を再接続してください（Claude: `/mcp`、Cursor: Reload / Tools & MCP）」と一言。

## やってはいけないこと

- キーを git にコミットする
- チャットで API キーを要求する
- プレースホルダ `sk-agent-xxxxxxxx` のまま接続成功にする
- ユーザーが選んでいない環境のキーを要求し続ける
- prod を黙って publish / 破壊する
- 届かない dev / stg を推奨する
