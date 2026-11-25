---
name: load-session
description: Load context from a previous Claude Code session into the current one — browse sessions, choose compact summary or full transcript, with smart template auto-selection.
metadata:
  author: Biswajit Sahoo (https://github.com/IamBiswajitSahoo)
  license: Apache-2.0
argument-hint: "[session-name]"
---

# Load Session

Load a previous Claude Code session as a compact summary (default) or full transcript.

**Design:** the transcript never flows through main context. The parser writes it to a temp file, the `session-summarizer` sub-agent reads the file directly, and the file is deleted afterward. Cost is roughly constant regardless of session size.

## Phase 1 — Prereqs & browse

Check Python: `python3 --version 2>/dev/null || python --version 2>/dev/null`. Store the working command as `{PY}`. If neither works, stop.

If `$ARGUMENTS` is non-empty, treat it as a session name and skip to Phase 2. Otherwise list sessions:

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/list-sessions.py" --page 1 --compact
```

Returns `{page, total_pages, total, sessions: [{i, uuid, jsonl_path, name, project, branch, msgs, size, last}]}`.

Render as a table via `AskUserQuestion`:

> **Select a session** (page {page}/{total_pages}, {total} total)
>
> | # | Session | Project | Branch | Msgs | Size | Last |
> |---|---------|---------|--------|------|------|------|
>
> Enter a number, **N/P** for next/prev page, or **C** to cancel.

On selection, extract that row's `uuid` and `jsonl_path` directly — no second resolve call needed. `N`/`P` → re-run with updated `--page`. `C` → stop.

## Phase 2 — Estimate & choose mode

If we arrived from `$ARGUMENTS` (no `jsonl_path` in hand), resolve:

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/resolve-session.py" "<name-or-uuid>"
```

Stop on `error`. **Refuse to load the current session into itself** — if resolved `uuid` matches `${CLAUDE_SESSION_ID}`, stop with "Cannot load the current session into itself."

Estimate cost:

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/estimate-context.py" "<jsonl_path>"
```

Returns `{file_size_human, user_messages, assistant_messages, estimated_tokens_text, context_pct_full, duration_minutes, budget_warning}`.

Ask via `AskUserQuestion`:

> **Session:** {name}
> **Messages:** {user_messages} user + {assistant_messages} assistant | **Duration:** {duration_minutes} min | **Size:** {file_size_human}
>
> 1. **Compact summary** (recommended) — ~500–1000 tokens
> 2. **Full transcript** — ~{estimated_tokens_text} tokens{warning}
> 3. **Cancel**

If `budget_warning` is true, append `⚠ uses {context_pct_full}% of context window` to option 2.

`1` → Phase 3a · `2` → Phase 3b · `3` → stop.

## Phase 3a — Compact mode

**Detect template:**

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/detect-template.py" "<jsonl_path>"
```

Returns `{recommended_template, confidence, reason}`.

**Pick template** via `AskUserQuestion` (mark `recommended_template` with "← recommended ({reason})"):

1. **Quick** — fast single-pass gist
2. **Default** — Chain-of-Density entity-dense summary
3. **Decisions** — architectural choices and trade-offs
4. **Actions** — files changed, what was done, why
5. **Discussion** — questions, findings, open threads
6. **Timeline** — chronological phases
7. **Handoff** — goals/actions/assessment/next steps
8. **Custom** — provide your own prompt

For 1–7, read `${CLAUDE_SKILL_DIR}/templates/summary-{template_name}.md` as `{template_text}`. For 8, ask for a path or inline text; if it's an existing file path, read it, otherwise use verbatim.

**Write transcript to temp file:**

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/parse-session.py" "<jsonl_path>" --out-file auto
```

Returns `{transcript_path, char_count, estimated_tokens, entries}`. **Do not print the transcript.** Capture `transcript_path`.

**Delegate to sub-agent** via **Agent** tool with `subagent_type: "bix-session:load-session:summarizer"`, `description: "Summarize session: {name}"`, and prompt:

```
transcript_path: {transcript_path}

Read the transcript file and summarize it using the template below. After summarizing, delete the transcript file with `rm -f`.

---
TEMPLATE:

{template_text}
```

The fully-qualified `bix-session:load-session:` prefix is required — without it the call silently falls back to `general-purpose` on the parent model.

**Standalone install** (no `bix-session:load-session:summarizer` agent available): launch `general-purpose` with `model: "sonnet"` and the same prompt, prefixed with "Read `${CLAUDE_SKILL_DIR}/references/agents/summarizer.md` and follow it as your instructions."

On error or empty result, run `rm -f "<transcript_path>"` yourself and suggest a different template or full mode.

**Inject:**

> ---
> **Loaded session:** {name} (compact — {template_name})
>
> {summary_text}
>
> ---

Proceed to Phase 4.

## Phase 3b — Full mode

Full transcript must reach main context (that's the point), but still write through a temp file so cleanup is uniform:

```bash
{PY} "${CLAUDE_SKILL_DIR}/scripts/parse-session.py" "<jsonl_path>" --out-file auto
```

Read the file with the **Read** tool, output its contents to the user, then `rm -f "<transcript_path>"`.

## Phase 4 — Summary

> **Session loaded:** {name}
> **Mode:** compact ({template_name}) | full
> **Estimated tokens added:** ~{N}

## Rules

- **Never load the current session into itself** — compare resolved UUID against `${CLAUDE_SESSION_ID}`.
- **Never print the transcript via Bash** — always use `--out-file`, consumed by the sub-agent (compact) or Read tool (full).
- **Always delegate** compact summarization to `bix-session:load-session:summarizer`. Never inline. Never via `claude --resume`.
- **Always clean up the temp file** — sub-agent does it in compact mode; skill does it in full mode. SessionStart hook is a safety net for crashes. A standalone install has no hook, so in Phase 1 run `find "${TMPDIR:-/tmp}" -maxdepth 1 -type f -name 'bix-load-session-*.md' -mmin +60 -delete 2>/dev/null` instead.
- **Always show token estimates** before full mode and require confirmation.
- Scripts return JSON with an `error` field — check and surface it.
