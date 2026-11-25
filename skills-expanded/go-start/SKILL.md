---
name: go-start
description: |
  Session startup skill. Reads platform docs, builds context, asks which project we're
  working on, reads project docs — and is ready to work. Also handles continuation of a
  stuck task by restoring context from the interrupted session.

  Use when: start of a new terminal session, load context, resume interrupted work
---

# Go-Start — Session Start

Loads platform and project context in a single run. One command, agent is ready.

**Three phases:**
1. Platform — read common platform docs
2. Project — read docs of the selected project
3. Session type — new task or resuming a stuck session

## Input

The session-start signal (user invoking `/go-start` in a fresh terminal).

## Output

Loaded platform + project context in-session; numbered project menu shown; session type resolved to new or continuation.

## Hands off to

`go-fast` (new session), or resumes the interrupted task's per-block cycle (continuation).

---

## Phase 1 — Platform

### Step 1.1 — Read platform files

Read all five sequentially:

- `{tasks_root}/README.md`
- `{tasks_root}/docs/core/WORKFLOW.md`
- `{tasks_root}/docs/core/DEPLOY.md`
- `{tasks_root}/docs/core/PLATFORM_KNOWLEDGE.md`
- `{tasks_root}/projects.yml`

**Rule:** read all five — do not skip even if you think you already know the content. Each session starts from a clean slate.

### Step 1.1.5 — Cleanup stale git locks

Before the summary — silently run a helper that scans active projects and clears stale `.git/index.lock` files (>5 min old). Idempotent. Capture stdout for use in the summary line.

**Why:** background git commands can hang for hours, hold `.git/index.lock` and block the repo. The helper kills the offending process and removes the file.

### Step 1.2 — Output platform summary

A compact block (no more than 8 lines):

```
✅ Platform loaded.

Servers: {msk_vds} | {nl_vds}
Deploy: git push origin main → post-receive → auto-backup
Skills: {skills_project}/.agents/skills/ → sync-agents.sh → all projects
Artifacts: task_artifacts in routing.db
Git locks: {helper result}
```

Do not retell files in full — only operationally important information.

### Step 1.3 — Project menu

Take only `status: active` from `projects.yml`. Output a numbered list with id / name / domain. Wait for explicit user selection — do not guess, do not proceed to Phase 2 without it.

---

## Phase 2 — Project

### Step 2.1 — Determine project path

Take `path` from `projects.yml` for the selected `id`. Partial name match on `name` or `id` is allowed. If the entry has `claude_path` — use it as `{claude_root}`; otherwise `{claude_root}={path}`.

**Save to session context** for subsequent skills:
- `{project_id}` = slug from projects.yml
- `{project_path}` = full path
- `{project_name}` = display name

These are read by the fast-track skill's Step 1 — if set, re-asking for the project is not needed.

### Step 2.2 — Read project docs (by priority)

| Priority | File | What it provides |
|---|---|---|
| 1 | `{path}/CLAUDE.md` | Project rules, stack, push policy |
| 2 | `{claude_root}/.agents/skills/project-knowledge/SKILL.md` | Architecture, patterns, DB schema |
| 3 | `{path}/README.md` | General project overview |

**If multiple found** — read all. **If none found** — output a warning and continue without project context.

### Step 2.3 — Project summary

One line: `✅ Project loaded: {name} ({domain}). [key facts]`.

### Step 2.4 — Launch Flow Web UI (optional)

If a local Flow Web UI launcher script exists — start it and print clickable URLs scoped to `{project_id}`. If not installed — silently skip.

**Anti-pattern:** blocking `go-start` if the launcher errors. Print the error line and continue to Phase 3. Session start is more important than the UI.

---

## Phase 3 — Session type

### Step 3.1 — Ask session type

```
New session or continuing a task?
1. New — starting from a clean slate
2. Continuation — context was consumed, resuming a stuck task
```

Wait for response. Do not guess.

### Step 3.2a — New session

User selected "new" → **immediately** call `$go-fast` without any intermediate text or questions. The fast-track skill's Step 1 will substitute the project from session context.

**Anti-pattern:** outputting "Ready. What are we doing?" before `$go-fast`. This breaks the chain — the session context transfer relies on going directly to go-fast.

### Step 3.2b — Resuming a stuck task

User selected "continuation" → ask for a task number, title, or a paste from the interrupted session.

### Step 3.3 — Find task

- Multi-line input → treat as paste from terminal. Extract `task_id` by pattern (first match): slug with `--`, "task N" reference, log folder path
- Short input → search directly (by number or by partial name match) in the routing DB

Verify the extracted `task_id` exists in `artifacts`. Not found → ask to clarify.

### Step 3.4 — Read blocks

```bash
sqlite3 {routing_db} \
  "SELECT block_num, title, status, commit_hash
   FROM task_blocks WHERE task_id='{task_id}' ORDER BY block_num;"
```

No records → fallback: find the task file and read the `## Blocks` section. Not found either → ask user to describe where they stopped.

### Step 3.5 — Show blocks and review last

Status mapping:

| DB status | Symbol |
|---|---|
| `done` | ✅ |
| `in_progress` / `open` (current) | 🔄 |
| `open` (future) | ⏳ |

List the blocks, then read the last `report-NN.md` from the log folder via Read tool. From its `## Next` section extract what's left → output "Done / Left / Continue?".

No reports → show blocks from DB and ask to describe where they stopped.

---

## Anti-patterns

### ❌ Reading files outside the Phase 1 list

Agent decided to also read some other doc "while at it". Rule: Phase 1 reads exactly the five listed files. Everything else — only if the user explicitly asked.

### ❌ Guessing project without menu

User wrote `/go-start` and agent picked a project itself. Rule: menu is mandatory. Explicit selection every time, even if the previous session was in the same project.

### ❌ Skipping Phase 2 when "it's obvious"

Agent knows the project stack from past sessions and skips CLAUDE.md. Rule: every session starts from zero. CLAUDE.md may have changed. Phase 2 is mandatory always.

### ❌ Outputting full file summaries

Agent read WORKFLOW.md and reproduced it in full in the chat. Rule: summary is only operationally important info, no more than 8 lines per phase. Details stay in the read files.

---

## Related skills

- **go-fast** — invoked at Step 3.2a for a new session
- **project-knowledge** — read at Step 2.2 for architecture/patterns

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'go-start', datetime('now'))" 2>/dev/null || true
```
