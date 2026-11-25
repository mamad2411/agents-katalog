---
name: cold-shower
description: |
  Reality-check toolkit for vibe-coded apps. Four auto-triggering modes, no commands to memorize.
  AUDIT — 6 parallel scans (LLM cost, AI security, code health, deps, prod readiness, git/devops) → Vibe Score 0-100.
  PLAN-GATE — structured plan, then blocks all edits until the user types APPROVED.
  RECALL — save decisions/bugs/fragile-files to a local brain; recall across sessions.
  DAILY BRIEF — session-start recap of what you left off.
  Trigger on: "audit my codebase", "is this ready to ship", "cold shower", "reality check",
  "LLM bill too high", "is my AI secure", "clean up my deps", "app crashed under traffic",
  "implement X", "add X", "fix X", "refactor X", "build X", "remember this", "what did we decide".
tools: Read, Write, Bash, Grep, Glob
---

# cold-shower — Reality Check for Vibe-Coded Apps

This file is the **router**. Heavy detail (all audit bash, fix sprints, emergency code) lives in
`references/` and is loaded **only when that mode actually runs** — this keeps the context small.

| Mode | Fires on | Where the detail is |
|------|----------|---------------------|
| 📅 DAILY BRIEF | auto at session start after a gap/new day | inline below |
| 🔥 EMERGENCY | "app crashed", "500s", "too many connections", traffic spike | `references/sprints.md` → EMERGENCY MODE |
| 🔍 AUDIT | "audit", "ready to ship", "reality check", "LLM bill", "clean up deps" | `references/audits.md` |
| 🔧 FIX SPRINT | after an audit, when a sprint is chosen | `references/sprints.md` |
| 📋 PLAN-GATE | "implement/add/fix/refactor/build X" | inline below |
| 🧠 RECALL | "remember this", "what did we decide" | inline below |
| 📉 CONTEXT DIET | "hitting token limit", "reduce tokens", "too many skills" | `references/token-audit.md` + `scripts/context-diet.js` |

**Progressive disclosure (important):** For AUDIT, FIX SPRINT, or EMERGENCY, **`Read` the matching
reference file first** — it has the exact commands. The file is in this skill's directory:
`~/.claude/skills/cold-shower/references/audits.md` and `.../references/sprints.md`
(or `$CLAUDE_PLUGIN_ROOT/skills/cold-shower/references/…` when run as a plugin). Do not guess the bash.

---

## 📅 DAILY BRIEF MODE

When a `DAILY BRIEF` block appears in your session context, **lead your first response with it** — even if the user just said "hi".

If in-progress items exist:
```
Welcome back. Last session you were working on [specific item].
Best first task: [concrete next action]. Want me to open [file]?
```
If none captured yet:
```
Welcome back to [project]. Last session: [time ago] on branch [branch].
No tasks captured yet — what are you building today?
```

**Never** just say "Hey."/"Hi." when a brief is present, and never wait for the user to ask about prior work.

If the user says **"what should I work on today"**: check `~/.claude/projects/<project>/brain/` (decisions.md, bugs.md, context.md) and output a prioritized plan.

---

## 🔥 EMERGENCY CHECK — run this first

Before anything, check if the app is actively on fire: user mentions 500s, timeouts, "too many connections", DB overload, app down, crashing under traffic, HN/Product Hunt spike.

**If yes → `Read references/sprints.md` and jump to EMERGENCY MODE.** Stop the bleeding first, full audit after it's stable.

---

## 🔍 AUDIT MODE

Order: **Phase 0** detect stack → **Phase 1** run audits A–F in parallel → **Phase 2** compute Vibe Score (0-100) + write report → **Phase 3** pick a fix sprint.

- A — LLM cost (if HAS_AI)  · B — AI security (if HAS_AI) · C — code health (always)
- D — dependencies (always) · E — prod readiness (if HAS_DB) · F — git/devops hygiene (always)

**`Read references/audits.md`** for every command, the Vibe Score formula, the report template, and score-history saving. Save each score to `.cold-shower/score-history.json`.

After a sprint, tell the user to type **`re-audit`** — a sprint without a re-audit is unverified.

---

## 📋 PLAN-GATE MODE

Auto-activates on "implement/add/fix/create/refactor/build X". While active, the `gate.js` PreToolUse hook **blocks all Edit/Write/MultiEdit** until the user types `APPROVED`. Generate this plan first (store at `.plan-gate/plan.md`):

```markdown
## Plan: [task name]

### Understanding
- Problem (the WHY), definition of done (behavior), out of scope

### Files to Touch      | File | Lines | Change | Reason |
### Files NOT to Touch  | File | Reason |   (check recall avoid.md for fragile files)
### Contracts That Cannot Change   (API sigs, response codes, DB columns callers depend on)
### Dependency Order   1. first change (unlocks others) 2. ...
### Risk Assessment    HIGH/MEDIUM — specific failure mode
### Pre-Mortem         "If this fails, the most likely cause is..."
### Rollback           exact undo steps — migration rollback? backfill?
```

Then ask: **"Review the plan. Type `APPROVED` to proceed."** Write no code until APPROVED.
After implementation, remind: **"Type `re-audit` to verify the Vibe Score didn't drop."**
User can bypass with "skip plan" or by deleting `.plan-gate/ACTIVE`.

---

## 🧠 RECALL MODE — persistent second brain

Brain files (local only — never commit; add `.claude/` to .gitignore):
```
~/.claude/brain/preferences.md                     ← global: coding style, tools
~/.claude/projects/<project>/brain/
  decisions.md  ← architectural choices + WHY + rejected alternatives
  avoid.md      ← fragile files — gate.js warns before editing these
  bugs.md       ← fixed bugs + how to detect regression
  context.md    ← domain/business context
  patterns.md   ← project-specific code patterns
```

Entry format (always include WHY + date):
```markdown
## YYYY-MM-DD · [one-line summary]
**Decision/Pattern/Bug/Context:** [the WHAT]
**Why:** [reason — constraints, rejected alternatives, incidents]
**Source:** [commit sha, issue #, or "session decision"]
```

Commands: `"remember [X]"` → classify + append to the right file · `"what did we decide about [X]"` → grep brain files · `"show avoid list"` · `"/recall review"` → memories >90 days · `"forget [X]"`.

Classify on save: architecture→decisions.md · file to avoid→avoid.md · bug→bugs.md · domain→context.md · code pattern→patterns.md · personal style→~/.claude/brain/preferences.md.

**Hard limits:** each brain file ≤50 lines (archive oldest to `brain/archive/` when full) · session injection ≤15 headlines · never inject full file content at session start — headers only, full content on demand.

---

## 📉 CONTEXT DIET MODE — trim your Claude Code token tax

Different target from AUDIT: this fixes the **Claude Code setup** (installed-skill bloat, model/effort, hooks, MCP), not the project code. Use when the user hits token/5-hour limits, says "reduce tokens" / "too many skills", or Claude feels slow/expensive.

A deterministic script does the measuring + pruning (no LLM guessing, cheap to re-run):

1. **Report first — `Read references/token-audit.md`** then run `scripts/context-diet.js` (no flags). Show the Context Tax: skills loaded, ~tokens/session, KEEP vs PRUNE, model/effort, hooks, MCP.
2. **Prune on approval:** `--list` to review, then `--prune` moves unused skills to `~/.claude/skills-disabled/` (reversible with `--restore`). Never deletes.
3. **Config fixes:** recommend the exact settings.json edits (effort→medium, drop [1m]) — apply only if the user says yes.

Savings land on the next session (context is built at session start).
