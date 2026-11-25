---
name: setup-post-tool-use-hooks
description: プロジェクトの .claude/settings.json にPostToolUseフック（prettier, eslint等）を設定する。Use when user mentions hooks設定/フック設定/formatter hooks/PostToolUse/setup-hooks/setup-post-tool-use-hooks.
allowed-tools: Bash, Read, Write, Edit, Glob
---

# PostToolUse Hooks 設定スキル

プロジェクトごとに適切なPostToolUseフックを `.claude/settings.json` に設定する。

## 前提条件チェック（必須）

設定前に必ず以下を確認すること：

### 1. フォーマッタ・リンターの検出

プロジェクトルートで以下を確認し、存在するツールだけをフックに追加する。

| ツール | 検出方法 |
|--------|---------|
| prettier | `package.json` の devDependencies、または `.prettierrc*` の存在 |
| eslint | `package.json` の devDependencies、または `eslint.config.*` / `.eslintrc*` の存在 |
| biome | `package.json` の devDependencies、または `biome.json` の存在 |
| ruff | `pyproject.toml` の `[tool.ruff]`、または `ruff.toml` の存在 |
| black | `pyproject.toml` の `[tool.black]` |
| gofmt | `go.mod` の存在 |

### 2. 既存設定の確認

`.claude/settings.json` が既に存在する場合は、既存の設定を壊さないようにマージする。

## 設定テンプレート

### JavaScript/TypeScript プロジェクト（prettier）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

### JavaScript/TypeScript プロジェクト（eslint + prettier）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "npx eslint --fix \"$CLAUDE_FILE_PATH\" 2>/dev/null; npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

### JavaScript/TypeScript プロジェクト（biome）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "npx biome check --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

### Python プロジェクト（ruff）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "ruff format \"$CLAUDE_FILE_PATH\" 2>/dev/null; ruff check --fix \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

### Python プロジェクト（black）

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "black \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

### Go プロジェクト

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "gofmt -w \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
      }
    ]
  }
}
```

## ワークフロー

1. プロジェクトルートの `package.json`、`pyproject.toml`、`go.mod` 等を読み取る
2. 使用しているフォーマッタ・リンターを特定する
3. 適切なテンプレートを選択する
4. `.claude/settings.json` に書き込む（既存設定があればマージ）
5. 設定内容をユーザーに報告する

## 注意事項

- 検出できたツールだけを設定する。推測で追加しない
- `2>/dev/null || true` を必ず付けて、エラーでClaudeの作業が止まらないようにする
- 既存の `.claude/settings.json` の他の設定（permissions等）を消さない
