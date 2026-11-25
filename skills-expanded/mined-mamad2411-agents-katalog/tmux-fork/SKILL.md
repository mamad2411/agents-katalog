---
name: tmux-fork
description: Fork a new tmux window to spawn a parallel terminal session. Use when the user requests 'fork terminal', 'tmux fork', 'new terminal', 'fork session', 'open a new tmux window', or wants to run a command or AI agent in a separate tmux window.
allowed-tools: Write, Read, Bash
---

# tmux-fork

在新的 tmux 視窗中啟動 AI coding agent 或執行 CLI 命令。
依循 `Instructions` 指示，執行 `Workflow`，根據 `Cookbook` 選擇對應流程。

## Variables

ENABLE_RAW_CLI_COMMANDS: true
ENABLE_GEMINI_CLI: true
ENABLE_CODEX_CLI: true
ENABLE_CLAUDE_CODE: true
AGENTIC_CODING_TOOLS: claude-code, codex-cli, gemini-cli

## Instructions

- 根據使用者的請求，依照 `Cookbook` 判斷應使用哪個工具。

### Context Handoff（對話摘要）

- IF: 使用者請求 fork terminal 時附帶 summary。僅適用於 `AGENTIC_CODING_TOOLS` 中的工具，且該工具必須為啟用狀態。
- THEN:
  - 讀取 `prompts/fork-summary.md` 模板。
  - **在記憶體中**填入對話歷史摘要和下一步請求。
  - 將填好的 prompt 傳給對應的 agentic coding tool。
  - **重要**：不要修改模板檔案本身，僅在記憶體中使用。
- EXAMPLES:
  - "fork terminal use claude code to <xyz> summarize work so far"
  - "開一個新視窗用 claude code 做 <xyz>，附上摘要"
  - "fork terminal use gemini to <xyz> with summary"

## Workflow

1. 理解使用者的請求。
2. 讀取 `tools/fork_tmux.py` 了解工具能力。
3. 依照 `Cookbook` 判斷應使用哪個工具。
4. 執行 `tools/fork_tmux.py` 啟動新的 tmux 視窗。

## Cookbook

### 原始 CLI 命令

- IF: 使用者請求的不是 agentic coding tool，且 `ENABLE_RAW_CLI_COMMANDS` 為 true。
- THEN: 讀取並執行 `cookbook/cli-command.md`
- EXAMPLES:
  - "開一個新視窗跑 npm run dev"
  - "fork terminal run pytest"
  - "new terminal: watch -n 2 'ls -la'"

### Claude Code

- IF: 使用者請求使用 Claude Code agent，且 `ENABLE_CLAUDE_CODE` 為 true。
- THEN: 讀取並執行 `cookbook/claude-code.md`
- EXAMPLES:
  - "fork terminal use claude code to <xyz>"
  - "開一個新視窗用 claude code 重構 auth 模組"
  - "fork terminal use claude code fast to fix the typo"

### Codex CLI

- IF: 使用者請求使用 Codex CLI agent，且 `ENABLE_CODEX_CLI` 為 true。
- THEN: 讀取並執行 `cookbook/codex-cli.md`
- EXAMPLES:
  - "fork terminal use codex to <xyz>"
  - "開一個新視窗用 codex 寫測試"
  - "fork terminal use codex fast to review code"

### Gemini CLI

- IF: 使用者請求使用 Gemini CLI agent，且 `ENABLE_GEMINI_CLI` 為 true。
- THEN: 讀取並執行 `cookbook/gemini-cli.md`
- EXAMPLES:
  - "fork terminal use gemini to <xyz>"
  - "開一個新視窗用 gemini 產生文件"
  - "fork terminal use gemini fast to analyze code"
