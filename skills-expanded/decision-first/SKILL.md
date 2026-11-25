---
name: decision-first
description: |
  Makes an architectural / project / scope decision using a 5-part model
  INSTEAD of asking the user. Structure: 🎯 Decision / Why / 🛡 Security /
  📈 Scalability / Alternatives / Plain-language analogy.
  1 question = 1 atomic artifact.

  Use when: the agent is about to ask an architectural / scope question;
  "/decision-first", "decide it yourself", "apply the decision model"
---

# Decision-First Protocol

Makes a decision **on behalf of** the user via a 5-section model with full reasoning and alternatives. Invoked whenever the agent is about to ask an architectural / project / scope question — instead of asking, the skill is called.

**Core idea:** the user prefers autonomous decisions with transparent reasoning over back-and-forth Q&A. A decision can be contested post-hoc (round 2) — cheaper than a synchronous pause-and-ask.

**When to call:** exists **2+ reasonable alternatives** and a justified selection is required. If one option is obviously correct — do not call, just act.

## Input

An ambiguous architectural, scope, or design question the agent is about to ask the user.

## Output

`decision-{NN}.md` capturing the choice via a 5-part model (🎯 Decision / Why / 🛡 Safety / 📈 Scalability / Alternatives / In plain language).

## Hands off to

Returns control to the calling skill (typically `arch-first`, `plan-first`, or `library-first`).

---

## Step 0 — Task context

Ensure `{log_dir}` and `{slug}` are known. Otherwise resolve from the latest task log folder.

---

## Step 1 — Identify decision(s)

**Auto-mode** — pick the last unresolved question from the current conversation. If related questions cluster (e.g. "flatten + format" = 2 decisions) — handle all in one invocation, one artifact per decision.

**Manual mode** (`/decision-first`) — either process the questions the user described, or ask "which questions?".

**Cutoff:** obvious choice → skip the skill, just act.

---

## Step 2 — Apply the 5-section model

Per decision:

```markdown
# D{N} — {short title}

🎯 **Decision:** {chosen option in one sentence}

**Why this option:**
- {specific reason 1}
- {specific reason 2}

**🛡 Security:** {security analysis. If N/A — explicit `not applicable`}

**📈 Scalability:** {scaling impact. If N/A — explicit `not applicable`}

| Alternative | Why rejected |
|---|---|
| {option 1} | {concrete drawback} |
| {option 2} | {concrete drawback} |

**Plain-language analogy:** {real-world analogy without technical jargon}
```

Rules:
- 🎯 Decision — one sentence, no "possibly X"
- Why — 2 to 5 concrete reasons
- 🛡 Security + 📈 Scalability — always present (even if `not applicable` with rationale)
- At least 2 real alternatives (no straw men)
- Analogy — from real life (warehouse / shop / kitchen)

---

## Step 3 — Numbering

Per-task auto-numbering scoped to `{log_dir}`:

```bash
NEXT_NN=$(( $(ls "{log_dir}"/decision-*.md 2>/dev/null | wc -l) + 1 ))
```

Format `decision-{NN}.md` (zero-padded). Retry → `decision-{NN}.R2.md`.

---

## Step 4 — Write and register

Each decision = one file `{log_dir}/decision-{NN}.md`. Add a row to `task.md` `## Task files` section + a link block at the end.

Register in `task_artifacts` (one row per decision):

```bash
sqlite3 {routing_db} \
  "INSERT INTO task_artifacts
     (task_id, block_num, round_num, artifact_type, file_name, file_path, created_by, created_at)
   VALUES ('{slug}', {block_num or NULL}, 1, 'decision', 'decision-{NN}.md',
           '{log_dir}/decision-{NN}.md', 'decision-first', '{date}');"
```

---

## Step 5 — Output summary

Group decisions inline in chat:

```
✅ Decision-first — N decisions taken:

[D{NN}] 🎯 {chosen} — {1-line reasoning}
[D{NN+1}] 🎯 {chosen} — {1-line reasoning}
```

After output — **continue working**. Do not wait for approval (user objects → "rewrite D{NN}" triggers round 2).

---

## Principles

1. **Do not ask** — call the skill instead of asking the user
2. **All 5 sections mandatory** — even `not applicable` must be explicit
3. **Real alternatives only** — no straw men
4. **Analogy mandatory** — makes the decision accessible to non-technical stakeholders
5. **1 question = 1 artifact** — for analytics and typing
6. **Flag unknowns** — insufficient data → mark as `⚠️ requires validation`

---

## Anti-patterns

### ❌ Asking a question instead of the skill
2+ alternatives + no clear winner → call the skill. Do not ask.

### ❌ Skipping Security or Scalability
UI/cosmetic doesn't excuse silence. Write `not applicable` with a reason.

### ❌ Straw-man alternatives
Alternatives must be viable choices in the same value system.

### ❌ Silent choice under insufficient data
Explicitly flag `⚠️ requires validation` — do not hide the uncertainty.

### ❌ Bundling multiple decisions in one file
1 question = 1 file = 1 row in task_artifacts. Group visually in chat only.

### ❌ Inlining instead of `Skill()`
Always via the Skill tool — otherwise version drift + no artifact registration.

---

## Example — reference decision (public form)

```markdown
# D1 — `producer_id` in draft: denormalize or JOIN?

🎯 **Decision:** denormalize — copy `producer_id` from source into draft at INSERT.

**Why this option:**
- Analytics queries filter by producer often. JOIN on millions of rows is slow.
- INTEGER (4 bytes) — cheap in storage.
- Source is immutable after processing — single source of truth preserved.

**🛡 Security:** validated by the catalog FK trigger at INSERT — no forgery. Deactivating the producer blocks new INSERTs, keeps old audit trail.

**📈 Scalability:** 1M rows → SELECT without JOIN = O(log n) with an index. With JOIN — double scan. On 10M rows — seconds vs milliseconds.

| Alternative | Why rejected |
|---|---|
| JOIN on every analytics | Degrades on large volumes |
| Materialized view | SQLite has no MV. VIEW = same JOIN under the hood |
| Periodic refresh job | Sync complexity. Denormalization at INSERT is simpler |

**Plain-language analogy:** imagine an archive of invoices. Storing only supplier id → building a report by supplier is slow (JOIN with registry). Storing a small copy of the supplier label right next to the invoice → report is instant. Registry updates don't affect the archive because the archive is history, not the present.
```

---

## Related skills

- **plan-first** — plans execution steps (after decisions are made)
- **note-first** — saves a free-form note (after user request)
- **arch-first** — multi-block architectural tasks (invokes decision-first at forks)
