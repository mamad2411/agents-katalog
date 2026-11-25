---
name: gemini-subagent
description: >
  Delegate expensive work to the local Gemini CLI (`gemini`) as a worker
  subagent to save Claude's token budget. Use this skill whenever a task
  involves web search / online lookup, reading or scanning large files,
  bulk code analysis, writing long files, running tests or scripts, or any
  chore that would otherwise burn a lot of Claude context. Claude stays
  the orchestrator — planning, deciding, verifying — while Gemini does the
  heavy I/O-bound or context-heavy work. Trigger on phrases like "丟給 gemini",
  "用 gemini 查", "gemini 搜一下", "gemini 分析", "dispatch to
  gemini", "delegate to gemini", whenever the user hints they want to
  conserve Claude's tokens or offload work, or whenever Claude is stuck
  and wants a second pass with a fresh context.
user-invocable: true
---

# Gemini as Worker Subagent

Claude is the **orchestrator**. Gemini is a **worker subagent** with its own
fresh context window, its own network access, and its own code execution environment. You hand Gemini a well-scoped task and take back a short answer.
Gemini's thinking, tool calls, and file reads happen **in Gemini's context,
not yours** — that is where the token savings come from.

## Thin-forwarder contract

Treat each Gemini call like a function call:

- You write the prompt (the "arguments")
- Gemini runs its own full agent loop inside its own context
- You take Gemini's stdout as the **authoritative return value**
- No Claude-side freelancing — don't "edit" what Gemini said in your head
  and then act on a phantom version. If Gemini's answer is wrong or under-
  specified, **resume the session** with a follow-up or dispatch a fresh
  call with a better prompt. Do not pretend you know what it meant.

## When to delegate

Delegate when any of these apply:

- **Network needed.** Web search, fetching docs, scraping an API,
  checking a package version, `gh api`, `npm view`, `pip install`. You
  (Claude) pay steep token cost for WebFetch/WebSearch; Gemini's network
  calls happen in its own context.
- **Large reads.** Scanning a repo, digesting a long file/log, cross-
  referencing many sources.
- **Long output that just needs a conclusion.** E.g. "find all TODOs and
  tell me which are stale" — Gemini emits the list internally and returns
  only the verdict.
- **Writing long files.** Gemini writes in its isolated context; you only see
  "wrote foo.py (240 lines)".
- **Running tools you'd rather not stream.** Tests, builds, linters,
  data-processing scripts.
- **You're stuck.** If your own attempt has stalled or you want a fresh
  second pass with no prior context, dispatch Gemini with a clean problem
  statement. That's explicitly the best-case use — "rescue" mode.

## When NOT to delegate

- Quick decisions you can make from existing context.
- Tasks that depend tightly on conversation state that would be painful
  to re-explain.
- One-line edits you could `Edit` directly with less overhead than
  composing a Gemini prompt.
- The user is clearly expecting *you* to do it interactively ("let's walk
  through this together").

Gut check: if the task would cost you more than ~3k tokens of reads/
searches, delegate. If it's under ~1k, just do it.

## Command shape

Canonical invocation:

```bash
filename=$(openssl rand -hex 4)
gemini --approval-mode <MODE> \
  [-C <DIR>] \
  [--model <MODEL>] \
  "<PROMPT>" \
  2>>"/tmp/gemini-${filename}.log"
```

Flag meanings:

- `--approval-mode <MODE>` — see the adaptive ladder below.
- `-C <DIR>` — run Gemini with a specific working directory. Pass this
  whenever the task is scoped to a specific project folder; saves Gemini
  a `cd` round-trip.
- `--model <MODEL>` — override Gemini's model if needed (e.g.
  `gemini-2.5-pro`, `gemini-2.5-flash`). Don't override the user's
  default model unless they asked.
- Prompt as the **last positional argument**, quoted. For long/multi-
  line prompts, use heredoc on stdin:

  ```bash
  filename=$(openssl rand -hex 4)
  gemini --approval-mode auto_edit \
    2>>"/tmp/gemini-${filename}.log" <<'EOF'
  Your multi-line
  prompt here.
  EOF
  ```

### Why the `openssl rand` log pattern instead of `2>/dev/null`

`2>/dev/null` throws away stderr, so when a call fails you have nothing
to diagnose. The alternative is:

1. Generate a random per-call filename.
2. Redirect stderr to `/tmp/gemini-<name>.log` instead of `/dev/null`.
3. On **success**, ignore the log (temp file, OS cleans it up later).
4. On **failure** (non-zero exit or suspicious output), read the log to
   see Gemini's thinking stream and real error messages.

You get clean stdout for happy path **and** full debugging info on
failure, without ever bloating Claude's context on the happy path.

## Approval ladder (adaptive, no-prompt)

The user has authorized adaptive escalation: **default to auto_edit mode,
escalate to YOLO mode whenever the task actually needs it, without
stopping to ask.** Don't over-escalate — use the minimum that gets the
job done.

| Task shape | Mode | Flag |
| --- | --- | --- |
| Read-only analysis inside workspace | plan mode | `--approval-mode plan` |
| Local edits / file writes inside a project | auto_edit mode | `--approval-mode auto_edit` |
| **Anything needing network** (web search, fetch, `pip install`, `npm view`, `curl`, `gh api`, remote access) | yolo mode | `--yolo` |
| Operating outside the workspace (system paths, `~/.config`, other drives) | yolo mode | `--yolo` |
| Installing global tools, modifying global state | yolo mode | `--yolo` |

**Do tell the user** in your one-line status update *which* mode you
picked and *why* — so they can correct you if your read was wrong. No
approval needed, but transparency yes.

**Truly destructive ops** (`rm -rf` outside workspace, dropping a
database, force-push, rewriting git history) — stop and confirm with the
user first regardless of mode. The mode protects the
filesystem; it does not divine the user's intent.

## Reasoning effort by task class

Default to Gemini's configured defaults. Override with model selection
only when the task class warrants it:

| Task class | Model | Why |
| --- | --- | --- |
| Quick lookup, version check, single-file read | (default / flash) | Not worth the extra tokens |
| Normal code edits and refactors | (default) | Gemini's default is tuned for this |
| Audit, security review, "find all bugs" | `gemini-2.5-pro` | Needs exhaustive exploration |
| Debugging a subtle failure | `gemini-2.5-pro` | Needs careful reasoning |
| Bulk scan / pattern matching over many files | (default) | Balance speed and coverage |

Don't ask the user which model to use — pick a sensible default and
mention it in the status line. If they want different, they'll say so.

## Writing prompts for Gemini

Gemini is a capable coding agent, not a dumb shell. Treat it like a
competent colleague who just walked into the room — no memory of your
conversation, no context on why the task matters.

A good Gemini prompt has:

1. **The goal.** What "done" looks like.
2. **Scope hints.** Which directory, which files, which language.
3. **Return format.** What you want back. "Reply with just the version
   number." "Return a markdown table." "Keep total output
   under 200 words." Gemini is very willing to be terse if asked — and
   terseness is token savings.
4. **Guardrails**, when non-obvious. "Don't modify tests.", "Don't touch
   anything outside src/api/.".

Example — bad:

```
"check what version of react we're on"
```

Example — good:

```
"Read package.json in the current directory and report just the 'react'
 version string. No other output."
```

Example — web-search delegation:

```bash
filename=$(openssl rand -hex 4)
gemini --yolo \
  2>>"/tmp/gemini-${filename}.log" <<'EOF'
Search the web for the current stable version of Bun (as of today).
Check bun.sh and the GitHub releases page. Return a single line:
  bun <version> released <date>
EOF
```

Example — bulk analysis with structured return:

```bash
filename=$(openssl rand -hex 4)
gemini --approval-mode auto_edit -C /path/to/repo \
  --model gemini-2.5-pro \
  2>>"/tmp/gemini-${filename}.log" <<'EOF'
Find every TODO/FIXME comment under src/. For each, judge whether it
looks stale (references removed code, completed work, or is >1 year old
based on git blame). Return a markdown table:
  | file:line | comment | stale? | reason |
No prose. Just the table.
EOF
```

## Resume-first pattern

Before launching a **new** call, consider: is there a recent Gemini
session still relevant to what you're about to ask? Gemini keeps session
state. Resume is cheap; a new session discards everything Gemini already
learned.

Resume syntax (prompt via stdin, no flags):

```bash
filename=$(openssl rand -hex 4)
echo "Your follow-up prompt" | gemini --resume latest \
  2>>"/tmp/gemini-${filename}.log"
```

Or with heredoc:

```bash
filename=$(openssl rand -hex 4)
gemini --resume latest \
  2>>"/tmp/gemini-${filename}.log" <<'EOF'
Follow-up: now also check the peerDependencies field and flag mismatches.
EOF
```

Resume rules:

- Feed the follow-up prompt via **stdin** (echo pipe or heredoc), not as
  a positional argument — `resume` doesn't accept a prompt positional.
- **Don't re-specify** flags like `--approval-mode`, `--model` on resume.
  The resumed session inherits from the original. Passing them causes
  errors.
- Resume is the right tool for: iterative refinement, "now also do X",
  disagreement discussions, fed-back corrections.
- If you need a clean slate (different project, unrelated task, or last
  session was derailed), start fresh instead.

## Parallel batch dispatch

When you have multiple **independent** subtasks, fire them in parallel
instead of sequentially. Use Bash with `run_in_background: true`, then
collect via `TaskOutput` on each task_id. This is a token-savings
multiplier — each subagent runs in its own context, all in wall-clock
parallel, and you only see the summaries.

Good candidates for parallel batch:

- Analyzing N independent files/packages/repos
- Cross-checking an answer from two different angles
- Running lint + tests + build in parallel

Bad candidates:

- Sequential dependencies (step B needs step A's output)
- Tasks that should share context — use resume instead

## Background lifecycle for long runs

Long Gemini calls (>30s, big analyses, audits, large writes) should go
into the background rather than blocking your turn:

1. Dispatch with Bash `run_in_background: true`. You get a task_id
   immediately and can continue other work.
2. Do other useful work while it runs — read a related file, plan the
   next step, write a helper.
3. When you need the result, call `TaskOutput` on the task_id with
   `block: true`. You'll either get the finished output or wait for it.
4. If the user wants to cancel, use `TaskStop`.

## Handling the outcome

Gemini's stdout is your return value. Before you act on it, classify it:

- **`success`** — call exited 0, stdout answers the prompt, nothing
  looks off. Proceed. Ignore the stderr log.
- **`partial`** — call exited 0 but stdout is empty, truncated, asks
  clarifying questions back at you, or hits a known failure mode
  (refused to run, couldn't find file, hit a permission wall). Check
  the stderr log for why, then either: (a) fix the prompt and dispatch
  fresh, (b) escalate the approval mode and retry, or (c) resume with a
  clarification.
- **`error`** — non-zero exit. **Don't silently retry.** Read the
  stderr log first and diagnose. Common failures and fixes:

  | Symptom | Likely cause | Fix |
  |---|---|---|
  | `operation not permitted` / approval mode denial | Need higher approval mode | Escalate approval mode |
  | `network unreachable` / DNS failure | Approval mode restricting network | Use `--yolo` |
  | `127` command not found | `gemini` not on PATH | Surface to user, don't retry |
  | Gemini asked a clarifying question in output | Under-specified prompt | Rewrite prompt with clearer goal / return format |
  | Empty output / hit timeout | Task too big for one call | Split into subtasks, or raise timeout |

## Using Gemini's answer

Once you have a `success` result:

1. **Read carefully.** Don't parrot stdout back to the user verbatim —
   extract what they actually need and summarize.
2. **Verify when it matters.** Gemini runs on Google models with their own
   cutoffs and can be wrong — especially about recent library versions,
   model names, APIs, or post-cutoff changes. If the answer is load-
   bearing and you have reason to doubt, cross-check (your own
   knowledge, a second Gemini call with a different phrasing, or a
   direct tool).
3. **Disagree explicitly and resume.** If Gemini is wrong, don't just
   quietly ignore it. Resume the session and push back with evidence.
   Frame it as peer discussion, not correction — either AI could be
   wrong:

   ```bash
   filename=$(openssl rand -hex 4)
   echo "This is Claude following up. I disagree with [X] because \
   [evidence]. What's your take?" | \
   gemini --resume latest \
     2>>"/tmp/gemini-${filename}.log"
   ```

4. **Trust file ops.** If Gemini said it wrote a file, it wrote it — its
   shell actually ran the write. A quick `ls -la` or targeted
   Read is enough to confirm; don't re-read the whole file.
5. **Summarize for the user.** One or two sentences: what you delegated,
   what came back, what you did with it. Don't dump Gemini's stdout into
   the chat unless the user asked — that re-inflates the context you
   were trying to save.

## Status updates to the user

Before dispatch — one line, in your normal chat voice:

- "Dispatching to gemini for the web lookup (yolo mode for network)."
- "Delegating the repo scan to gemini — auto_edit mode, pro model, read-
  only workload."
- "Gemini rescue: I'm stuck, handing off with a fresh context."

After — short result summary. One or two sentences. What changed, what's
next.

## Token-budget sanity checks

This skill only earns its keep if it actually saves tokens. Gut checks
before dispatching:

- Prompt you'd send Gemini is <1k tokens — usually worth it if the work
  Gemini avoids is >3k tokens.
- About to delegate something you could answer in 2 sentences from
  memory — just answer it.
- About to delegate 5 tiny independent questions — batch them into one
  Gemini call with a structured return format, not 5 calls. (Or
  parallel-batch them if each is big enough to warrant its own context.)

## What this skill is NOT

- Not a replacement for `Edit`/`Read` on small, known targets. Direct
  tools are cheaper for tiny ops.
- Not a way to offload thinking. Claude still owns planning, decisions,
  and judgment. Gemini is a worker, not a co-pilot.
- Not a reason to avoid your own tools. If `Grep` finds the answer in
  200ms, use Grep.
- Not a silent fallback. Every dispatch is announced in one line so the
  user knows what's happening and can course-correct.
