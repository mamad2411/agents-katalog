---
name: subagent-cli
description: >-
  A skill for non-interactively executing external AI agent CLIs in Bash. Provides procedures for delegating coding work via codex exec or cursor-agent.
  Use when: Use when: delegating complex implementations, code reviews, multi-file batch changes, or launching sub-agents from Bash.
---


# subagent-cli

Executes external AI agent CLIs as subprocesses via Bash to delegate complex coding tasks.
Use it as a "power tool" to extend execution capability while maintaining your own identity, judgment, and memory.

## Relationship with Framework Execution Modes

This skill applies only **when the Bash tool is available**.

| Mode | Implementation | Bash | Applicability of this skill |
|--------|------|------|------------------|
| **Mode S** | `core/execution/engines/claude/executor.py` (Claude Agent SDK) | Available by default | Applies. Read/Write/Edit/Bash/Grep/Glob/WebFetch/WebSearch + MCP (send_message, etc.) + Task/Agent are available within the Claude Code subprocess. The cwd during Bash execution is anima_dir |
| **Mode C** | `core/execution/engines/codex/executor.py` (Codex SDK) | Depends on the Codex CLI toolset | **codex exec is not needed** — the framework runs Codex directly. cursor-agent / claude -p can be invoked via Bash (if Bash is available) |
| **Mode D** | Cursor Agent (cursor-agent subprocess) | Depends on the Cursor CLI toolset | **cursor-agent -p is not needed** — the framework runs cursor-agent directly. MCP integration. Tool access is similar to Mode S, but the actual binary is cursor-agent. codex exec / claude -p can be invoked via Bash (if Bash is available) |
| **Mode G** | Gemini CLI (gemini subprocess) | Depends on the Gemini CLI toolset | **Manual startup of Gemini CLI is not needed** — the framework runs it directly. MCP integration, stream-json output. Other CLIs can be invoked via Bash (if Bash is available) |
| **Mode A/B** | LiteLLM + tool_use / 1-shot | Only when permitted by permissions.json | Applies if Bash is permitted |

**Important**: For Anima in Mode C (`codex/*`), Mode D (`cursor/*`), and Mode G (`gemini/*`), the framework runs each engine directly. In this case, you do not need to invoke `codex exec` (Mode C), `cursor-agent -p` (Mode D), or Gemini CLI (Mode G) yourself via Bash. Only refer to the relevant section of this skill when you explicitly want to use a different CLI (cursor-agent / claude -p / codex exec, etc.).

**Windows exception**: In a native Windows environment, if shell execution becomes `policy blocked`, or if `codex exec exited with code 1` occurs repeatedly, stop retrying the local `codex exec`. Escalate shell-required tasks to the supervisor (`supervisor`).

## Tool Selection Priority

**Select in order of cost efficiency.**

| Priority | Tool | Cost | Strengths |
|--------|--------|--------|----------|
| 1 | `codex exec` | Cheapest (Codex) | Code generation, editing, review |
| 2 | `cursor-agent -p` | Low (Cursor) | Code generation, editing, multi-file |
| 3 | `claude -p` | High (Claude API) | Last resort. Only when the above two do not resolve the issue |

**Principle**: In non-Windows environments or where shell execution is healthy, try `codex exec` first. In native Windows where shell execution is blocked or unstable, skip `codex exec` and escalate to the supervisor (`supervisor`). For other failures or tasks outside its strengths, fall back in the order cursor-agent → claude.

## When to Use

- Code changes spanning multiple files
- Test creation and test fixes
- Code review
- Refactoring
- Bug fix investigation and implementation
- New feature implementation

## When Not to Use

- Small single-file edits (do them directly yourself)
- Memory read/write (use your own tools)
- External API calls (use dedicated tools)
- Information search or research only (web_search or Read is sufficient)

---

## 1. codex exec (Recommended)

**Applicability**: Mode S or when Mode A/B（Bash is permitted). In Mode C, the framework executes Codex, so this section is not needed. In Mode D/G, the framework also executes each engine, so no need to refer to this unless you need to use codex as an alternative.

### Basic Syntax

```bash
codex exec --full-auto -C /path/to/workspace "プロンプト"
```

For the working directory `-C`, specify the absolute path of the target project. During Bash execution in Mode S, `ANIMAWORKS_ANIMA_DIR` (Anima's data directory) and `ANIMAWORKS_PROJECT_DIR` (AnimaWorks framework root) are set as environment variables. If developing AnimaWorks itself, `-C "$ANIMAWORKS_PROJECT_DIR"` can be used.

### Important Options

| Option | Description |
|-----------|------|
| `--full-auto` | Auto-approve + sandbox (workspace-write) |
| `-C /path` | Working directory specification (**required**) |
| `-m model` | Model specification (e.g., `o4-mini`, `o3`) |
| `--sandbox workspace-write` | Workspace write permission (included in full-auto) |
| `--json` | Output in JSONL format |
| `-o file` | Write the final message to a file |
| `--ephemeral` | Do not save session files |

### Execution Examples

#### Code Generation

```bash
codex exec --full-auto --ephemeral -C /home/user/dev/myproject \
  "src/utils/parser.py にMarkdownパーサーを実装して。既存のテストを壊さないこと。"
```

#### Code Review

```bash
codex exec --full-auto --ephemeral -C /home/user/dev/myproject \
  review
```

#### Test Creation

```bash
codex exec --full-auto --ephemeral -C /home/user/dev/myproject \
  "src/utils/parser.py のユニットテストを tests/test_parser.py に作成して。"
```

#### Save Results to a File

```bash
codex exec --full-auto --ephemeral -C /home/user/dev/myproject \
  -o /tmp/codex_result.txt \
  "このプロジェクトのアーキテクチャを分析して改善案を出して。"
```

---

## 2. cursor-agent -p (Alternative)

**Applicability**: Mode S or when Mode A/B（Bash is permitted). Also applicable in Mode C/G if Bash is available. In Mode D, the framework executes cursor-agent, so manual `cursor-agent -p` in this section is generally not needed.

### Basic Syntax

```bash
cursor-agent -p --trust --force --workspace /path/to/workspace "プロンプト"
```

### Important Options

| Option | Description |
|-----------|------|
| `-p` / `--print` | Non-interactive mode (**required**) |
| `--trust` | Auto-trust the workspace |
| `--force` | Auto-approve commands |
| `--workspace /path` | Working directory specification (**required**) |
| `--model model` | Model specification (e.g., `sonnet-4`, `gpt-5`) |
| `--output-format text\|json` | Output format |
| `--mode plan\|ask` | Read-only mode (for research) |

### Execution Examples

#### Code Generation

```bash
cursor-agent -p --trust --force \
  --workspace /home/user/dev/myproject \
  "src/api/routes.py にPOST /users エンドポイントを追加して。バリデーション付き。"
```

#### Read-Only Research

```bash
cursor-agent -p --trust --mode ask \
  --workspace /home/user/dev/myproject \
  "この認証フローにセキュリティ上の問題はある？"
```

#### Save Results to a File

```bash
cursor-agent -p --trust --force \
  --workspace /home/user/dev/myproject \
  --output-format text \
  "テストカバレッジが低いモジュールを特定して改善して" > /tmp/cursor_result.txt
```

---

## 3. claude -p (Fallback)

**Applicability**: Mode S or when Mode A/B（Bash is permitted). Also applicable in Mode C/D/G if Bash is available.

Use only when codex/cursor-agent cannot handle the task. API costs are high.

### Basic Syntax

```bash
claude -p --dangerously-skip-permissions --output-format text "プロンプト"
```

### Important Options

| Option | Description |
|-----------|------|
| `-p` / `--print` | Non-interactive mode (**required**) |
| `--dangerously-skip-permissions` | Skip permission checks |
| `--model model` | Model specification (e.g., `sonnet`, `haiku`) |
| `--allowedTools "tools"` | Restrict allowed tools (e.g., `"Read Edit Bash(git:*)"`) |
| `--output-format text\|json` | Output format |
| `--max-budget-usd N` | Cost limit (USD) |
| `--no-session-persistence` | Do not save session |

### Execution Example

```bash
claude -p --dangerously-skip-permissions --no-session-persistence \
  --model haiku --max-budget-usd 0.5 \
  --output-format text \
  "src/core/parser.py のエラーハンドリングを改善して"
```

---

## How to Write Prompts

Sub-agents have no context about AnimaWorks. Write clear, self-contained prompts.

### Good Prompt

```
以下の要件でPythonモジュールを実装して:

ファイル: src/utils/validator.py

要件:
- Pydantic v2のBaseModelを使ったバリデータ
- email, username, passwordフィールド
- パスワードは8文字以上、英数字混合
- バリデーションエラー時にカスタム例外を投げる

制約:
- from __future__ import annotations を先頭に
- Google-style docstring
- 既存のテストを壊さないこと
```

### Bad Prompt

```
いい感じにバリデーションを直して
```

→ No context, and "nice" is unclear.

---

## Handling Output

### Capture Standard Output

```bash
RESULT=$(codex exec --full-auto --ephemeral -C /path "プロンプト" 2>/dev/null)
echo "$RESULT"
```

### Via File (Recommended for codex)

```bash
codex exec --full-auto --ephemeral -C /path \
  -o /tmp/result.txt "プロンプト"
# 結果を読む
cat /tmp/result.txt
```

### Determine Success or Failure by Exit Code

```bash
codex exec --full-auto --ephemeral -C /path "プロンプト"
if [ $? -eq 0 ]; then
  echo "成功"
else
  echo "失敗 — cursor-agentにフォールバック"
  cursor-agent -p --trust --force --workspace /path "同じプロンプト"
fi
```

---

## Background Execution (Important)

Sub-agent execution can take **5 to 20 minutes or more**.
Waiting in the foreground blocks the session, so **always run in the background**.

### Basic Pattern: nohup + Result File

```bash
nohup codex exec --full-auto --ephemeral -C /path/to/workspace \
  -o /tmp/codex_result.txt \
  "プロンプト" > /tmp/codex_stdout.log 2>&1 &
echo "PID: $!"
```

For cursor-agent:

```bash
nohup cursor-agent -p --trust --force \
  --workspace /path/to/workspace \
  "プロンプト" > /tmp/cursor_result.txt 2>&1 &
echo "PID: $!"
```

### Completion Check

```bash
# プロセスがまだ動いているか確認
ps -p <PID> > /dev/null 2>&1 && echo "実行中" || echo "完了"

# 結果を読む（完了後）
cat /tmp/codex_result.txt
# または
cat /tmp/cursor_result.txt
```

### Execution with Timeout

Use `timeout` to prevent runaway execution:

```bash
nohup timeout 30m codex exec --full-auto --ephemeral -C /path \
  -o /tmp/codex_result.txt \
  "プロンプト" > /tmp/codex_stdout.log 2>&1 &
```

- Recommended timeout: **30 minutes** (`30m`)
- Small tasks: **10 minutes** (`10m`)
- Large refactoring: **60 minutes** (`60m`)

### Continue Other Work While Running

After starting background execution, you may proceed with other tasks without waiting for completion.
Periodically check whether the process is still alive, and once complete, read the results and record them in episodes/.

---

## Safety Guidelines

1. **Always specify the working directory** — if not specified, execution happens in the current directory
2. **Do not include sensitive information in prompts** — API keys, passwords, etc.
3. **codex runs in a sandbox with `--full-auto`** — writes outside the workspace are restricted
4. **Check changes with git diff after execution** — verify there are no unintended changes
5. **Use --ephemeral** — prevent unnecessary accumulation of session files

---

## Fallback Strategy

```
1. codex exec で試行
   ↓ 失敗 or 品質不足
2. cursor-agent -p で再試行
   ↓ 失敗 or 品質不足
3. claude -p（--max-budget-usd でコスト制限）で最終試行
   ↓ それでも失敗
4. 自分で実行を試みるか、上司に報告する
```

## Notes

- Subagents cannot access AnimaWorks memory or tools. They are merely "coding hands."
- Record execution results in your own episodes/ and accumulate learned patterns in knowledge/.
- Execution takes 5 to 20+ minutes. Always run in the background and set a timeout.
- Work in a git-managed repository (for easy change tracking and rollback).
- In Mode S, `ANIMAWORKS_ANIMA_DIR` (Anima's data directory) and `ANIMAWORKS_PROJECT_DIR` (AnimaWorks framework root) are set as environment variables during Bash execution (injected via `core/execution/engines/claude/executor.py`'s `_build_env()`).
