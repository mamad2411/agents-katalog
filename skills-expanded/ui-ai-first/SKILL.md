---
name: ui-ai-first
description: |
  Final audit of a large task before closure — finds which operations
  are available only via code / curl / SQL and decides per each:
  automate with a skill or AI agent (A) or create a UI task (B).
  Protects against invisible usability debt.

  Walks through each implemented block: reads task.md + reports +
  guides + code → forms a sub-table with operations → A/B
  classification → master table + phased roadmap. Does not implement
  findings — records them as roadmap items.

  Use when: final step of an arch-first task before closure; review
  of a closed large task; "/ui-ai-first", "usability audit",
  "what's still only via code"
---

# UI/AI-First Protocol

Final protocol of the `*-first` family. Launched **after** implementing a large task — before formal closure. Protects against invisible usability debt: features implemented in code but unavailable to a non-developer (everything via curl / SQL / Claude Code).

## Input

A completed `arch-first` task near closure; its `task.md`, block reports, guides, and code changes.

## Output

`ui-ai-first-report.md` with operations classified A (automate via skill / AI agent) or B (build UI), and a phased roadmap of B items.

## Hands off to

`ship-first` (called from ship-first Step 0.6 when `run_ui_ai_first=true`).

---

## Introduction

### Why it's needed

Every large task leaves "code-only" operations. In reports this doesn't sound like a problem — "feature works", "endpoint in prod". But when an operator wants to use the capability — they hit curl with admin_password in JSON or SQL INSERT into several tables.

3 months later these capabilities effectively exist only on paper — no one but the task author uses them. This is **technical debt that looks like "everything's ready"**.

### A/B classification principle

For each "code-only" operation — one of two:

- **A — skill / AI agent** for rare or technical operations. Quick to build, cheap to run
- **B — UI task** for frequent operator operations where a skill is insufficient — need a form, button, dashboard

Not every feature needs UI. Not every operation needs a skill.

### What it does NOT do

Does not implement findings. Only classifies and forms a prioritized roadmap. Implementation — separate work streams with their own library-first / plan-first.

---

## Step 1 — Get task_path

If passed as argument — use. If not — ask user or propose the last closed task from routing DB.

Verify task is **actually closed**:
- task.md has blocks with ✅
- ≥1-2 `report-NN.md` in task log

If not — stop: "Task is not yet closed. Audit is premature."

---

## Step 2 — Gather list of implemented blocks

Read task.md → all blocks with ✅ or "Done" mark. Ignore planned or cancelled.

For each block record: number/name, `report-NN.md`, related guides, commits.

---

## Step 3 — Propose sub-table structure for approval

Rule: **1 task block = 1 sub-table**.

**Exception:** if a block has significant sub-blocks with many separate operations — extract them as **separate Sub-tables**. Don't merge — focus is lost.

Show user numbered list of S1 → Sn with expected volume. Mark hot zones with ⭐. Wait for approval.

---

## Step 4 — Pin structure in the master file

Create `{log_dir}/ui-ai-first-master.md` with skeleton:

```markdown
# UI/AI-First Audit — {task_slug}

**Start date:** YYYY-MM-DD

## Structure
[approved sub-table list]

## Sub-tables
See: ui-ai-first-b1.md, ui-ai-first-b2.md, ...

## Master table
[placeholder — Step 6]

## Roadmap
[placeholder — Step 7]

## Summary
[placeholder — Step 8]
```

This is the **index** and final aggregation.

---

## Step 5 — For each block: build sub-table (iteratively)

Cycle: S1 → Sn. Per S:

1. Read sources: `report-NN.md`, guides, key code files
2. Form sub-table per template:

```markdown
## Sub-table S{N} — Block {X} ({name})

**Sources:** {list}

**What the block brought:** {1-3 sentences}

### Operation groups

| # | Operation | Currently how | Frequency | Decision (A/B/–) | Skill/task |
|---|-----------|---------------|-----------|-------------------|------------|
| 1 | ... | ... | ... | A | /skill-name — description |
| 2 | ... | ... | ... | B | UI task — description |

### Result S{N}

- UI tasks: {N}
- Skills: {M}
- Main takeaway: {1-3 sentences}
```

3. Show user → approve → write to `ui-ai-first-b{N}.md`
4. Next block

### Frequency categories

| Level | When |
|---|---|
| High | Daily / several times per week |
| Medium | Weekly / monthly |
| Low | Quarterly, ad-hoc, debugging |
| Very low | One-off, GDPR / incident-only |

### Decisions

| Code | When |
|---|---|
| **A** | Rare/technical — skill/agent faster to build |
| **B** | Frequent operator — needs UI |
| **A + B** | Skill as stopgap, UI mid-term as stable solution |
| **–** | Neither needed — explain why |

---

## Step 6 — Master table

Merge all operations. Sort by priority:

1. **High ⭐** — frequent operator ops without A/B + critical blockers + HIGH bugs
2. **Medium** — frequent ops with A + medium-frequency ops
3. **Low** — rare, maintenance, optional
4. **Architectural TODO** — cross-cutting system improvements

Format:

```markdown
## Master table

### High priority ⭐
| # | Operation | Sub-table | Decision | Skill/task |

### Medium priority
[same shape]

### Low priority (backlog)
[same]

### Architectural TODO
| TODO | Referenced in |
```

Show user → approve → append to master.

---

## Step 7 — Phased roadmap

Group master table into 6 stages:

| Stage | What | When |
|---|---|---|
| **0 — Prerequisites** | Blockers — without them next stages don't work | Immediately after task closure |
| **1 — Burning pain points** | 3-5 high-priority skills + HIGH bugs | After Stage 0 |
| **2 — Basic automation** | Medium A skills for routine ops | After Stage 1 |
| **3 — UI tasks (mid-term)** | Main B tasks | After Stage 2 |
| **4 — GDPR + long-tail maintenance** | Compliance + rare ops | As client base grows |
| **5 — Backlog** | Low-priority A skills + long-term UI | When there's time |
| **6 — Architectural TODO** | System improvements (lifecycle, audit-log, signed URLs) | Separate streams |

For each Stage — short list of concrete items (skill names + descriptions / UI task names).

---

## Step 8 — Summary by category

```markdown
## Summary

| Category | Count |
|---|---|
| Skills Stage 1 (burning) | ... |
| Skills Stage 2 (basic automation) | ... |
| UI tasks Stage 3 | ... |
| GDPR + maintenance Stage 4 | ... |
| Backlog Stage 5 | ... |
| Architectural TODO Stage 6 | ... |
| **Total skills** | ~N |
| **Total UI tasks** | M |

**Main takeaways:**
- {where the main pain is}
- {what to do first}
- {which risks if not doing}

---

**Audit finished YYYY-MM-DD.**
```

---

## Step 9 — Optional: create backlog items

Ask: "Create separate files in `tasks/backlog/` for each roadmap item? (1=yes / 2=no)"

**If 2 (no):** roadmap stays only in master file. Done.

**If 1 (yes):** for each item create `tasks/backlog/{type}--{slug}.md`:

```markdown
---
type: backlog
created: YYYY-MM-DD
source: ui-ai-first audit of task {task_slug}
priority: high|medium|low
category: skill|ui|architecture
stage: 0-6
---

# {Item name}

**What:** {description}
**Why:** {rationale from audit}
**Source:** see master file — Stage {N}
**Next step:** library-first → plan-first → code (separate pass)
```

---

## Anti-patterns

### ❌ Audit only by guides

Guides cover user-facing aspects. Technical operations (SQL migrations, ad-hoc scripts) are often not mentioned. Without reading reports and code — operations will be missed.

**Rule:** for each block mandatory read `report-NN.md` + key code files.

### ❌ Classify everything as B (UI)

UI is slow and expensive. Most rare/technical operations should be A — much faster and cheaper.

**Rule:** B only when operation is **frequent operator** — otherwise A.

### ❌ Classify everything as A (skill)

Frequent operator operations must be in UI — otherwise the operator is stuck on CLI and Claude Code.

**Rule:** if the operation runs daily or several times per week — it's B.

### ❌ Not extracting sub-blocks as separate S

Hot zones get lost in parent block's sub-table. Gives false signal "parent is routine" while sub-block is the hottest part.

**Rule:** if a block has a sub-block with many separate operations — extract as separate S.

### ❌ Implement findings immediately

`ui-ai-first` is audit, not implementation. If mid-audit you want to write a skill — stop. Breaks focus, triples audit length.

**Rule:** all findings → roadmap items. Implementation — separate streams.

### ❌ Create backlog items automatically

Step 9 is optional. Not every user wants to split a roadmap into 25 files. Ask, don't do by default.

---

## File structure

```
{log_dir}/
├── ui-ai-first-master.md        # structure + master + roadmap + summary
├── ui-ai-first-b1.md            # sub-table S1
├── ui-ai-first-b2.md
└── ui-ai-first-b{N}.md
```

One protocol = one file per iteration.

---

## Launch triggers

- Direct: `/ui-ai-first <task_path>` or `/ui-ai-first` without arguments
- From `arch-first` — automatically as final block of a large task (5+ blocks)
- From `ship-first` — automatically as Step 0.5 before formal closure

---

## When NOT to launch

- Task is not yet closed (no blocks with ✅)
- Small task (1-2 blocks) — audit is more expensive than findings
- Purely refactoring task without new endpoints / tables / operations — nothing to audit

---

## Related skills

- **arch-first** — decomposes and drives large multi-block tasks; may invoke ui-ai-first as final block
- **ship-first** — invokes ui-ai-first at Step 0.5 before formal task closure
- **library-first** — parallel protocol, but for planning code reuse before implementation
- **flow-first** — parallel protocol, for landscape alignment before library-first

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'ui-ai-first', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
