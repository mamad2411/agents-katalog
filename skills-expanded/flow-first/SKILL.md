---
name: flow-first
description: |
  Understanding-alignment protocol before library-first. Asks the user for 2-3 anchors
  (file, table, route, service), reads only those (not the whole project), fills a 4×3
  table (Landscape / Problem / Solution / Result × UI / DB / Integrations), waits for
  approval — and only then hands off to library-first.

  Use when: automatically as a step between task creation and library analysis;
  manually before any task that needs an understanding check
---

# Flow-First Protocol

## Input

The block's task description plus 2-3 anchors (file / DB table / route / service / UI component) from the user.

## Output

A 4×3 table (Landscape / Problem / Solution / Result across UI / DB / Integrations) saved as `flow-first-{N}.{R}.md`.

## Hands off to

`library-first` (auto-invoked after user approval).

---

## Introduction

An **understanding-alignment** protocol before moving to library-first.

**Why it's needed:** library-first assumes the agent already understands what is being done and at which levels. Without that understanding, library-first is built on guesses — wrong layer searched, wrong LOC estimate, wrong "ready-made" solution. flow-first closes that gap in 5-10 minutes before planning begins.

**Key principle:** the agent reads **only what the user specified** — 2-3 anchors (file, table, route, service). No project-wide scanning.

---

## Step 0 — Check task context

Check: are `{log_dir}` and `{slug}` known in the current session?

If yes — continue. If no — list latest task folders under `{tasks_root}/log/`, ask which is current, set `{slug}` and `{log_dir}`. Cannot skip — without `{log_dir}` the artifact won't be saved.

---

## Step 0.5 — Incoming-artifact calibration

flow-first can be invoked inside a per-block cycle or manually. Read earlier artifacts if present:

```bash
ls "{log_dir}"/idea-first-*.md 2>/dev/null | head -1
ls "{log_dir}"/habit-first-*.md 2>/dev/null | head -1
ls "{log_dir}"/research-doc.md 2>/dev/null | head -1
```

- `idea-first-*.md` → extract task type (product/feature/fix) and scope
- `habit-first-*.md` → behavioural context for new-product tasks
- `research-doc.md` → ready comparison "as is vs should be"

If none found — continue. flow-first works without them.

### Step 0.5.0 — UPDATE block status pending → open

Move current block from `pending` to `open`:

```bash
sqlite3 {routing_db} \
  "UPDATE task_blocks SET status='open'
   WHERE task_id='{slug}' AND block_num={N} AND status='pending';"
```

The `AND status='pending'` clause is mandatory — guards against overwriting `done` on retry and against overwriting `open` if the block came from plan-first. `{N}` or `{slug}` unknown → silently skip.

---

## Step 1 — Get the task and the anchors

Before asking — check if the anchor is in the block title or task.md:

- **Block title** contains a file/skill/section → use it as anchor, go to Step 2
- **task.md** contains an explicit file or path → use it as anchor
- Nothing found → ask the user

### Launch format

```
Got the task. Before going into code — give me 2-3 anchors:
file, table, route, service or any entry point to the task.
```

### What counts as an anchor

| Type | Example |
|---|---|
| File | `services/email_service.py`, `routes/oauth.py` |
| DB table | `meetings`, `company_processes` |
| Route / endpoint | `POST /api/webhook`, `/admin/settings` |
| Service / module | `session_manager`, `whisper_service` |
| UI component | `modal-meeting.js`, `analytics-panel` |

### If the user doesn't know

Ask one guiding question — not five. If really unknown — grep for a keyword and show the found files as candidates. If entirely new module — anchor by analogy to a similar existing one.

Never start reading code without at least one anchor.

---

## Step 2 — Research by anchors

Read only the anchors. No more.

### Reading algorithm

1. Read each anchor file fully (or key part if large)
2. DB table anchor → find CREATE TABLE + every read/write site
3. Route anchor → read handler + one-level-deep service it calls
4. UI anchor → read js file + the template/html rendering it

**One level deep — and stop.** Found a function call → read the function. That function calls another — don't chase further unless critical.

### Pointed-question rule

```
❌ "It's unclear how email_service works, tell me more"
✅ "In email_service.py I see two encryption variants (ssl/tls). Which one is in production?"
```

One question = one specific fact that can't be established from the code.

### What to capture

For each of 3 levels (UI / DB / Integrations):
- **Landscape** — what currently exists
- **Problem** — where the task is, what's wrong or missing
- **Solution** — what specifically we're changing
- **Result** — what will change after

If a level isn't involved — explicitly mark `not involved`.

### Forbidden during research

- Reading files outside the anchors without an explicit question
- `grep` across the whole project to "see what else is there"
- Opening neighbouring files out of curiosity

If another file is clearly needed — **ask**, don't decide silently.

---

## Step 3 — 4×3 table

Fill four three-column tables. This is the only output format of flow-first.

### Landscape

| UI | DB | Integrations |
|---|---|---|
| what currently exists | what currently exists | what currently exists |

### Problem

| UI | DB | Integrations |
|---|---|---|
| what's wrong | what's wrong | what's wrong |

### Solution

| UI | DB | Integrations |
|---|---|---|
| what we change | what we change | what we change |

### Result

| UI | DB | Integrations |
|---|---|---|
| user impact | DB state change | behavior change |

**The "not involved" rule:** if a level isn't engaged — write `not involved` explicitly. An empty cell = "forgot to check". `not involved` = "checked, out of scope".

---

## Step 4 — Show the picture

Output the four tables, then one summary line, then the approval question.

### Summary line format

```
Affected: UI (partial) / DB (not involved) / Integrations (email_service.py).
flow-first done. Understanding table ready. Waiting for "ok" → launching library-first.
```

### What NOT to output

- Retelling of the code you read — only conclusions
- List of files you read — unless asked
- Predictions about library-first — that's the next step
- Questions inside the table — the table = statements

### If the table is incomplete

Show it with `?` in the uncertain cell + one clarifying question after the table. Don't block the table output for one clarification.

---

## Step 5 — Write to task.md

The table is written to log **simultaneously** with the output, before approval. If the user edits a cell — the corrected version is recorded.

**1. Round number:**

```bash
R=$(( $(ls "{log_dir}"/flow-first-{N}.*.md 2>/dev/null | wc -l) + 1 ))
```

**2. Write** `{log_dir}/flow-first-{N}.{R}.md` via Write tool with header referencing task.md and the four tables.

**3. Append** a link to task.md via Edit tool:

```
> 📋 Flow-First block {N}.{R}: flow-first-{N}.{R}.md
```

If `{log_dir}` unknown → return to Step 0. Don't tell the user "wrote to task.md" — technical step.

---

## Step 6 — Approval → library-first

Wait for explicit approval. Do nothing until user responds.

| Response | Action |
|---|---|
| "ok" / "go" / "yes" | Approval accepted → automatically launch library-first |
| Cell edit | Update cell → update log → show corrected table → wait again |
| Clarifying question | Answer briefly → wait again |
| "stop" / "wait" | Stop, wait for further instructions |

Transition to library-first is **automatic** — no phrase "ok, moving to library-first". Just start the library-first protocol. Pass `{log_dir}` and `{slug}` explicitly.

**Approval means:** the agent understood the task correctly across all three levels. It's not approval of a solution — it's approval of **understanding**.

---

## Anti-patterns

### ❌ Going into code without anchors

User described the task — agent immediately started reading files of its own choosing. Rule: anchors from the user first, then reading.

### ❌ Asking broad questions instead of pointed ones

"Tell me how email works in the project" instead of the specific ssl/tls-in-prod question. Rule: one question = one specific fact that can't be established from the code.

### ❌ Silently skipping levels

Task touches integrations only — agent filled only Integrations, left UI and DB empty. Rule: every untouched cell = `not involved`. Silence not allowed.

### ❌ Moving to library-first without approval

Showed the table and immediately started library-first — "since the task is clear". Rule: explicit "ok"/"go" is mandatory. Agent's understanding ≠ user's understanding.

### ❌ Going deeper than one level

Anchor is `oauth.py` → agent reads oauth → _store_token → token_storage → encrypt → crypto_utils. Rule: one level deep and stop. Deeper needed → ask.

### ❌ Picking the anchor yourself

Task "add email validation" → agent decided anchor is `email_service.py` and started reading. User had a different entry point in mind. Rule: anchors come only from the user or explicit task context. No explicit anchor → ask.

### ❌ Inlining the skill instead of using the Skill() tool

Executed the protocol manually from memory — outdated version, no accuracy guarantee. Always launch via `$flow-first`.

---

## Related skills

- **library-first** — receives control after approval, builds LOC table
- **plan-first** — invoked after library-first
- **arch-first** / **audit-first** — parent orchestrators that may invoke flow-first per block

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'flow-first', datetime('now'))" 2>/dev/null || true
```
