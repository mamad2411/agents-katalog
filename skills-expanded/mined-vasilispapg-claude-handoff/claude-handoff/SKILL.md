---
name: claude-handoff
description: "Session handoffs & standing project memory from Claude Code history, via the chf CLI. Use when the user wants to continue or hand off work in another model or a fresh session, recover a crashed or usage-limited session, export or summarize a past session, find a session by content ('where did we talk about X'), or refresh/curate the project memory brief. Trigger: /claude-handoff"
trigger: /claude-handoff
---

# /claude-handoff

Drives **`chf`** (claude-handoff) — turns Claude Code JSONL sessions into
paste-anywhere handoff documents and standing project memory (`--brief`).
Deterministic and offline by default, zero tokens; redaction always on.

## Usage

```
/claude-handoff                                    # THIS session → clipboard, paste-ready
/claude-handoff <words>                            # newest session whose title/first prompt matches
/claude-handoff --grep X [--grep Y]                # newest session that TALKED about X (AND)
/claude-handoff --list [--grep X]                  # list sessions (date · id · first prompt)
/claude-handoff --fit 32k                          # size to a token budget (deterministic only)
/claude-handoff --llm claude-cli                   # real summary via Pro/Max login — no API key
/claude-handoff --full | --last N | --since 2h     # verbatim turns / only the tail
/claude-handoff --project NAME --merge             # whole project → ONE handoff
/claude-handoff --anonymize                        # public-safe: ~ paths, no emails/IPs/username
/claude-handoff --brief                            # refresh project memory (free, factual)
/claude-handoff --brief --llm claude-cli           # re-distill memory (cached — new sessions only)
/claude-handoff --brief --keep SPEC | --exclude ID # curate what feeds the memory (sticky)
/claude-handoff --brief --grep X -o -              # thematic memory (export-only)
/claude-handoff -o graphify | --brief -o graphify  # file it into graphify's raw/ corpus (≥ 0.20)
/claude-handoff conversations.json [--brief]       # claude.ai / ChatGPT export as input
/claude-handoff --install-hook | --install-brief-hook   # automation hooks (explicit ask only)
```

## What You Must Do When Invoked

If the user invoked `/claude-handoff --help` or `-h`: print the `## Usage`
block above verbatim and stop.

**Step 1 — ensure installed.** `chf --version`. Missing →
`brew install Vasilispapg/tap/claude-handoff` (or `pipx install claude-handoff`).

**Step 2 — flags, not subcommands.** There is no `chf brief` / `chf export`
/ `chf list`. A bare word argument is a NAME SEARCH (`chf "login bug"`).
Everything else is a flag: `--brief`, `--list`, `-o`, `--llm`.

**Step 3 — pick the mode.**
- Hand off / export / summarize one session → handoff (the default mode).
- "where / which session was it…" → `chf --list --grep "X"` and show the
  matches; export only when asked.
- memory / brief / "remember this across sessions" → `--brief` mode.
- Hooks, MCP, config — only on explicit request (hooks edit
  `~/.claude/settings.json`; check there what is already installed before
  offering).

**Step 4 — which session?** Run from inside a live session, bare `chf`
picks the CURRENT session — the newest file IS this conversation.
- "hand THIS off / continue elsewhere" → bare `chf` is correct.
- "the crashed / previous / yesterday's session" → `chf --list` first (top
  entry = this session), then target explicitly: `chf --name <id-prefix>`
  (8-hex id from `--list` or a brief citation), or `--name "title words"`,
  or `--grep "content"`.
- NEVER use `-i` or bare `--exclude` — they need a TTY you don't have and
  exit with "-i needs a terminal". Use `--list` + explicit ids instead.
- Several sessions into one document: pass several paths, or `--merge`
  (whole scope), oldest → newest.

**Step 5 — route the output.**
- To paste into another model → `-o clipboard`; tell the user it's
  paste-ready.
- As a file → default `handoff.md`, or the path the user named. To read in
  chat → `-o -`. Machine-readable → `--format json`.
- Always relay chf's stderr result line (chars, ≈tokens) back to the user.

**Step 6 — LLM only when asked.** Deterministic is the default and costs
nothing.
- Subscription / "no API key" → `--llm claude-cli`. NOT `--llm claude` —
  that is the ANTHROPIC_API_KEY API path. `ollama` = fully local; `claude`
  / `openai` / `gemini` need keys (`--model` overrides the model id).
- `--fit` refuses to combine with `--llm` — deterministic sizing only, by
  design.
- Big sessions map-reduce with a progress bar; `claude-cli` and `ollama`
  run chunks sequentially and can take minutes → run the command in the
  background and report when done. It works from inside a Claude Code
  session (the nested CLI's env is scrubbed).
- `--focus "…"` steers the summary; `--with-transcript` appends the
  cleaned transcript.

**Step 7 — brief specifics.**
- The standing brief lives at `~/.claude/briefs/<project>.md`; with the
  brief hooks installed, SessionStart injects it and SessionEnd/PreCompact
  refresh the factual part for free. No LLM ever runs from a hook.
- Refresh facts: `chf --brief`. Re-distill: `chf --brief --llm claude-cli`
  — per-session notes are cached, only NEW sessions are paid for.
- Curation is sticky across refreshes: `--exclude a1b2c3d4[,…]`,
  `--keep first:2,last:20`, `--keep since:30d`; clear with
  `--exclude none` / `--keep all`.
- Thematic (`--brief --grep X`) and web-export (`conversations.json
  --brief`) briefs REQUIRE an explicit `-o` and never touch the standing
  brief. Keep it that way.
- In-project copies are refresh-only: once `raw/project-memory.md` (via
  `-o graphify`) or a root `BRIEF.md` the user created exists, every brief
  refresh rewrites them; deleting the file stops it. Never create either
  yourself unless asked.

## Rules

- Redaction stays ON in every output. Never add `--no-redact` unless the
  user literally typed it.
- Anything headed somewhere public (issue, forum, post) → add
  `--anonymize`.
- `-o graphify` needs chf ≥ 0.20 — if `chf --help` doesn't mention
  graphify, don't use it (older versions would write a literal file named
  `graphify`).
- Something silently did nothing → re-run with `--debug` before concluding
  anything.
- Store scoping: cwd inside a project → that project's sessions; a parent
  "master folder" → every project under it; `--any` → everything;
  `CLAUDE_HOME` relocates the store. Web exports (`conversations.json`)
  work as input anywhere.
