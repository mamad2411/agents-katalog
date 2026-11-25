---
name: codex
description: Run OpenAI's Codex CLI as a secondary AI agent from within Claude Code to verify thinking, double-check implementations, hunt for bugs, review diffs, or get a second opinion from a different model. Use this skill whenever the user wants to "ask Codex", "verify with Codex", "have Codex check", "get a second opinion", "sanity-check this", "review with Codex", "find bugs with Codex", or any reference to the Codex CLI. Also trigger when the user wants an independent review of recently written code or reasoning.
---

# Codex CLI Skill

Run OpenAI's Codex CLI (`codex`) as a secondary AI agent directly from Claude Code. The CLI is installed at `/opt/homebrew/bin/codex` and is authenticated via ChatGPT login.

This skill exists primarily to **verify Claude's own work** — a second pair of eyes from a different model family to catch reasoning errors, missed edge cases, and bugs before the user sees them.

## When to Use This

The core purpose is to **challenge Claude's work** — stress-test a plan, find problems in an implementation, catch reasoning errors that Claude itself won't see because they share a model family.

- Claude produced a plan or implementation and you want it challenged before shipping
- Specific concern about a piece of code Claude wrote ("does this handle concurrent writes?")
- Independent review of uncommitted/staged changes
- The user explicitly asks Codex to answer or do the task directly
- You want Codex to do something while Claude orchestrates

## When NOT to Use Codex

Codex takes 10–15 minutes per run and consumes real budget. Use it when there's a concrete Claude artefact (plan, diff, reasoning) to pressure-test — not as a generic "maybe it'll find something" pass.

Specific anti-patterns:

- **Generating new code from scratch** — Claude writes, Codex challenges. There's nothing to challenge if Claude hasn't produced anything yet.
- **Trivial refactors** (rename, extract, reformat) — no substantive decision for Codex to push back on.
- **Speculative invocations** — "review the codebase" or "check for bugs" without naming a specific file or concern. Codex wanders, reports shallow findings, and the 15 minutes were wasted.
- **Style / formatting** — biome, golangci-lint, rustfmt cover this.
- **Small diffs (<20 lines)** — not enough surface for a second opinion to find anything the first opinion missed.
- **Duplicating what Claude already verified** — if Claude already ran tests/linters/type checks, don't ask Codex to run them again.

The user asking for Codex directly always overrides these — when the user says "ask codex", just do it.

## MCP-Enabled Information Retrieval

Codex has MCP servers configured that let it pull context from external systems. This is useful when Claude needs information from these sources as input to a task:

- **Linear** — look up ticket details, read comments, check status (`linear-server` MCP)
- **Google Drive** — read Google Docs, Sheets, or Slides for context (`google-drive` MCP)
- **Slack** — read channel history, threads, or search messages for context (`slack@openai-curated` plugin)
- **GitHub** — read PRs, issues, comments (`github@openai-curated` plugin)

MCP tools are available regardless of `--sandbox` mode since they don't go through the sandboxed shell. Use `--sandbox read-only` as normal for these tasks.

### Examples

```bash
# Get context from a Linear ticket
codex exec --sandbox read-only \
  "Look up Linear ticket ENG-650. Summarise the description, acceptance criteria, and any comments."

# Read a Google Doc for context
codex exec --sandbox read-only \
  "Read the Google Doc titled 'Q2 Migration Plan' and summarise the key decisions and open questions."

# Find what was discussed in a Slack thread
codex exec --sandbox read-only \
  "Search Slack for recent messages about 'auth middleware' in #engineering. Summarise what was discussed and any decisions made."

# Pull context from a GitHub PR
codex exec --sandbox read-only \
  "Read the comments on PR #342 in myorg/myrepo. Summarise the review feedback."
```

These are **read-only retrieval tasks** — codex should not post messages, create tickets, or write to these systems when invoked from Claude.

## Core: Running Prompts (Non-Interactive)

Always use `codex exec` for non-interactive use from Claude Code. Never launch the interactive TUI — it will hang waiting for input.

```bash
codex exec "your prompt here"
```

For verification tasks where Codex only needs to read files (no edits), use `--sandbox read-only`. This is the safest default and matches most verification workflows.

```bash
codex exec --sandbox read-only "check whether the retry logic in src/client.rs correctly handles the case where the server returns 429 with a Retry-After header"
```

### Choosing the Right Flags

Build the command by combining these flags as needed:

| Flag | Purpose | Values |
|------|---------|--------|
| `"prompt"` | The task for Codex (positional arg) | Any string |
| `-m model` | Model selection | Depends on account; omit for default |
| `-s, --sandbox` | Sandbox policy | `read-only`, `workspace-write`, `danger-full-access` |
| `--full-auto` | Low-friction sandboxed auto execution | Flag only (sets `workspace-write`) |
| `--dangerously-bypass-approvals-and-sandbox` | No sandbox, no approvals | Flag only — use sparingly |
| `-C, --cd DIR` | Working root for the agent | Directory path |
| `--add-dir DIR` | Extra writable directory | Repeatable |
| `--skip-git-repo-check` | Run outside a git repo | Flag only |
| `--ephemeral` | Don't persist session to disk | Flag only |
| `--json` | Emit JSONL events to stdout | Flag only |
| `-o FILE` | Write the final message to a file | Path |
| `-i, --image FILE` | Attach image(s) to the prompt | Repeatable |
| `--output-schema FILE` | JSON Schema for structured final response | Path |

### Sandbox Mode Selection

Pick the least privilege that lets Codex do the job:

- **`read-only`** — Codex can read files and run read-only commands but cannot write or execute arbitrary shell. Use this for **verification, review, bug hunting, and code reading tasks** — i.e. the primary use case of this skill.
- **`workspace-write`** (via `--full-auto`) — Codex can edit files inside the working directory and run sandboxed commands. Use when you want Codex to actually fix something it finds.
- **`danger-full-access`** / `--dangerously-bypass-approvals-and-sandbox` — No restrictions. Only use when explicitly requested by the user, or for a short, clearly-bounded task that requires network or system access.

### Piping Input

Pipe file contents, diffs, or notes as context. Stdin is read when the prompt is `-`:

```bash
git diff | codex exec --sandbox read-only - "review this diff for bugs and logic errors"
cat reasoning.txt | codex exec --sandbox read-only - "is this reasoning sound? point out any flaws"
```

For long or multi-file context, prefer letting Codex read the files itself from disk inside `read-only` sandbox rather than stuffing everything through stdin.

## Writing Good Codex Prompts

The biggest lever for runtime and signal quality is prompt scope. Focused prompts finish in ~5 minutes with concrete findings; vague prompts drift to 15+ minutes and often return generic hand-wavy output.

**Good prompts:**
- Name specific files: *"Read `src/auth/session.ts` and `src/auth/session.test.ts`. Check the token-refresh logic for race conditions."*
- Ask specific questions: *"Does the offset calculation in `paginate()` correctly handle the edge case where `total < offset`?"*
- Specify output format: *"Return findings as BLOCKER / SHOULD-FIX / CONSIDER with `file:line`. If clean, say LGTM."*
- State what NOT to review: *"Don't comment on style or formatting — biome handles those."*
- Hand it the diff when reviewing changes, not "the repo" — narrower surface = faster and sharper.

**Bad prompts:**
- *"Review this codebase"* — wanders for 20 minutes, surface-level findings.
- *"Is this good?"* — no criteria, no scope.
- *"Check for bugs"* without naming files or concerns — grep-and-shrug output.

A one-sentence specific prompt usually beats a multi-paragraph general one.

## Common Patterns

### Verify Claude's Implementation

After Claude writes new code, ask Codex to look for bugs and logic errors:

```bash
codex exec --sandbox read-only -C /path/to/repo \
  "I just modified src/auth/session.ts to add token refresh. Read the file and the tests in src/auth/session.test.ts. Look for: race conditions, missed edge cases, incorrect error handling, and bugs. Be specific — cite line numbers. If it looks correct, say so."
```

### Verify Claude's Reasoning

When Claude has worked through a problem and wants an independent check:

```bash
codex exec --sandbox read-only "Here is my reasoning about X: [paste reasoning]. Do you agree? Point out any flaws or missed considerations."
```

Prefer piping the reasoning from a file for anything longer than a paragraph:

```bash
cat /tmp/reasoning.md | codex exec --sandbox read-only - "critique this reasoning — is it sound?"
```

### Review Uncommitted Changes

Codex has a dedicated review subcommand. Use it to review the working tree:

```bash
codex exec review --uncommitted
```

Other review targets:

```bash
codex exec review --base main          # Review current branch vs main
codex exec review --commit HEAD        # Review a specific commit
codex exec review --uncommitted "focus on concurrency and error handling"
```

The review subcommand is purpose-built for diff review and produces structured feedback. Prefer it over generic `codex exec` when the task is "review these changes".

### Hunt for a Specific Bug

When Claude suspects a bug but can't pin it down:

```bash
codex exec --sandbox read-only -C /path/to/repo \
  "There's a bug where the dashboard shows stale data after a refresh. The relevant files are src/store/dashboard.ts and src/hooks/useDashboard.ts. Trace the data flow and find the cause."
```

### Let Codex Fix Something It Finds

When you want Codex to both find and fix:

```bash
codex exec --full-auto -C /path/to/repo \
  "Find and fix any TypeScript errors in src/api/. Run tsc after to verify."
```

### Resume a Previous Session

When Codex flagged issues and you want it to re-check after a fix — without re-explaining context or re-reading the same files — resume the session:

```bash
codex exec resume --last "I addressed items 2 and 3. Re-check src/auth/session.ts and confirm the race condition is gone."
```

Or by explicit session id (printed in the `session id:` header of the original run):

```bash
codex exec resume 019da8e8-5d6f-7383-aa51-0c5a3ada947f "<follow-up prompt>"
```

Faster and cheaper than a fresh run — Codex already has the files read and the view formed. Prefer this for any "now check my fix" iteration. Falls back to a fresh run if the session expired.

### Running Outside a Git Repo

Codex refuses to run outside a git repo by default. Add `--skip-git-repo-check` when Claude invokes it from `~/dev` or another non-repo directory:

```bash
codex exec --sandbox read-only --skip-git-repo-check "explain this concept"
```

### Structured Output

When Claude needs to parse Codex's response programmatically, define a schema:

```bash
SCHEMA=/tmp/codex-schema-$$-$(date +%s).json
OUT=/tmp/codex-result-$$-$(date +%s).json
codex exec --sandbox read-only \
  --output-schema "$SCHEMA" \
  -o "$OUT" \
  "review src/foo.rs and return findings"
```

## Web Search Is Enabled By Default

`codex exec` ships with a built-in `web` tool that can search the internet, open pages, and fetch structured data (finance/weather/sports/time). It is **on by default** — no flag needed. Codex will decide when to reach for it based on the prompt.

Useful when the task needs current information Claude's context doesn't have:

```bash
codex exec --sandbox read-only --skip-git-repo-check \
  "What's the latest stable release of Encore's Go framework? Check the official site or GitHub releases and summarise what's new since v1.40."
```

To tune or disable web search, edit `~/.codex/config.toml`:

```toml
web_search = "live"       # default — query each time
# web_search = "cached"   # prefer cached results when available
# web_search = "disabled" # turn off entirely
```

The older `--enable web_search` flag still works but prints a deprecation warning — don't add it to new invocations.

## Runtime and Timeouts

Codex exec runs are routinely **10–15 minutes**, sometimes longer for multi-file reviews or deep reasoning. Plan the invocation around that — do **not** treat it like a quick shell command.

### Background by default

For anything beyond a trivial prompt, background the run and pick up the output when it completes.

```bash
OUT=/tmp/codex-out-$$-$(date +%s).txt
codex exec --sandbox read-only -o "$OUT" "..." &
```

From Claude Code: invoke Bash with `run_in_background: true`. Claude will be notified when it exits — do **not** poll with `sleep`, and do **not** use Bash's default 2-minute foreground timeout (the run will be killed mid-reasoning).

### When foreground is safe

Foreground Bash is only appropriate when all three hold:

1. The prompt is very narrow ("summarise this one file", "is this regex correct").
2. `-C` and `--sandbox read-only` are set so Codex doesn't wander.
3. You pass `timeout: 600000` (10 min, the Bash tool's ceiling) — not the default.

For anything broader, background it.

### Silence is normal

`codex exec` does not emit steady progress. It streams agent activity (tool calls, reasoning, file reads) in bursts, and the final message only arrives at the end. Several minutes of no output is not a hang.

To confirm a background run is actually working:

```bash
stat -f%z "$OUT"           # output file grows as partial events arrive
ps -p <pid>                # process still alive
```

### When to give up

If a background run exceeds **~25 minutes** with no growth in the output file, kill the PID and report the partial result to the user. Don't auto-retry — retrying a complex prompt with the same wording is usually slower than rethinking it and sending a tighter one.

### Cost awareness

`codex exec` consumes ChatGPT Pro credits (or OpenAI API tokens, depending on auth). A 15-minute run with heavy reasoning + MCP calls is not free. Use Codex for **independent verification** and **second opinions** — not for work Claude can just do directly. If you catch yourself reaching for Codex because "it might find something", the prompt probably isn't focused enough to be worth the spend.

## Interpreting Output

`codex exec` streams a lot of agent activity (tool calls, reasoning, file reads) to stdout before the final response. For Claude's purposes, the most reliable way to capture just the final answer is:

```bash
OUT=/tmp/codex-out-$$-$(date +%s).txt
codex exec --sandbox read-only -o "$OUT" "..."
cat "$OUT"
```

The `-o` flag writes only the final message to the specified file. Use this when you want to cleanly extract Codex's conclusion without parsing streamed events.

**Always pick a unique output path.** Concurrent Claude sessions on the same machine collide if they all write to a fixed `/tmp/codex-out.txt` — one session's output overwrites another's, and you may end up reading a stale or unrelated answer. The `$$-$(date +%s)` pattern (PID + epoch seconds) gives a per-invocation unique name that's easy to clean up later. Same applies to `--output-schema` files when batching multiple calls.

For programmatic consumption, add `--json` to get JSONL events, but prefer `-o` + schema for most cases.

## Tips

- **Default to `--sandbox read-only` for verification tasks.** It's faster (no approval prompts), safer (can't modify files), and sufficient for review/analysis.
- **Use `-C /absolute/path`** when running from Claude Code, since Claude's working directory may not match the target repo.
- **Prefer `codex exec review`** over generic prompts when the task is "review this diff".
- **Avoid the bare `codex` command** (no subcommand) — it launches the interactive TUI and will hang.
- **MCP tools are for reading, not writing** — when invoking codex from Claude, use MCP integrations (Linear, Slack, Drive, GitHub) to pull context, not to post messages or create tickets. Explicitly tell codex to report findings back rather than take action in external systems.
- **Codex sees its own project context** — it reads `AGENTS.md` / `CODEX.md` files in the target directory, similar to how Claude reads `CLAUDE.md`. Point it at the right `-C` directory so it gets the right context.
- **Don't pipe Claude's full conversation** — summarise the specific question first. Codex is more useful when given a focused prompt than a dump of context.
- **Be explicit about the format you want back** ("list bugs with file:line", "say APPROVE or REJECT and explain"). Codex, like any agent, benefits from clear output instructions.
- **For quick sanity checks, consider `--ephemeral`** so the session isn't persisted.

## CLI Management (Occasional)

These don't need `exec` — they're direct CLI operations:

```bash
codex login status               # Check auth state
codex login                      # Interactive login (user must run)
codex logout                     # Remove credentials

codex mcp list                   # List MCP servers configured for Codex
codex mcp add <name> <cmd>       # Add an MCP server
codex mcp remove <name>          # Remove one

codex resume --last              # Interactive: resume most recent session
codex resume <session-id>        # Interactive: resume specific session
```

Interactive subcommands (`resume`, bare `codex`) should be suggested to the user to run themselves via `! codex ...` in the prompt — Claude Code cannot drive a TUI.

## Exit Codes

After running a Codex command, check the exit code:

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Read the output or `-o` file |
| non-zero | Error | Report to the user; common causes: auth expired, sandbox violation, bad args, git-repo-check failure |

If Codex fails with an auth error, tell the user to run `codex login` themselves — Claude can't drive the interactive login flow.
