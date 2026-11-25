---
name: installing-project-mcps
description: Install MCP servers into the current project scope using claude mcp add. Use when setting up a new project, when user mentions MCP setup, project MCP, MCPインストール, MCPセットアップ, or /installing-project-mcps.
allowed-tools: Bash
---

# Installing Project MCPs

プロジェクトスコープにMCPサーバーをインストールするワークフロー。

## ワークフロー

```
1. レジストリ読み込み
   ↓
2. ユーザーにインストール対象を確認（AskUserQuestion）
   ↓
3. claude mcp add --scope project で追加
   ↓
4. 検証（.mcp.json 確認）
```

## 実行手順

### Step 1: レジストリ読み込み

`references/mcp-registry.md` を読み込み、利用可能なMCPサーバー一覧を把握する。

### Step 2: ユーザーに選択させる

AskUserQuestionを使って、インストールするMCPを確認する。

提示する選択肢（カテゴリ別）:

**ブラウザ・フロントエンド開発:**

- next-devtools（Next.js開発）

**コード分析・開発支援:**

- serena（セマンティックコード分析）
- maestro（マルチエージェント）

### Step 3: インストール実行

選択されたMCPに対して `claude mcp add` を実行する。

#### stdio方式のMCP

```bash
claude mcp add --scope project <name> -- <command> [args...]
```

具体例:

```bash
# next-devtools
claude mcp add --scope project next-devtools -- npx next-devtools-mcp@latest

# serena
claude mcp add --scope project serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server

# maestro
claude mcp add --scope project maestro -- maestro-mcp-server
```

### Step 4: 検証

インストール完了後、以下を確認:

1. `.mcp.json` がプロジェクトルートに生成されていること
2. `claude mcp list` で追加したMCPが表示されること

```bash
# プロジェクトの .mcp.json を確認
cat .mcp.json

# インストール済みMCP一覧
claude mcp list
```

## エラーハンドリング

### `claude mcp add` が失敗する場合

1. コマンドのパスを確認（`npx`, `uvx` 等が利用可能か）
2. ネットワーク接続を確認
3. 既に同名のMCPが登録されている場合は `claude mcp remove <name>` してから再追加

### npxコマンドが見つからない場合

Node.jsがインストールされていることを確認:

```bash
node --version
npx --version
```

### uvxコマンドが見つからない場合

uv（Python パッケージマネージャー）がインストールされていることを確認:

```bash
uv --version
```

## チェックリスト

- [ ] レジストリを読み込んだ
- [ ] ユーザーにインストール対象を確認した
- [ ] `claude mcp add --scope project` でインストールした
- [ ] `.mcp.json` が正しく生成されたことを確認した
- [ ] `claude mcp list` で追加を確認した
