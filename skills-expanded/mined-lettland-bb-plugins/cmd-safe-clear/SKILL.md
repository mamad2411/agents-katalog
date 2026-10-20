---
name: cmd-safe-clear
description: Command — Safely flush context and resume fresh - distills session state before clearing
---

Persist session state then seamlessly resume work. The user should not notice this happening.

**Tool scope (rm constraint):** the `Bash(rm:*)` grant permits any `rm` invocation at the runtime level. **You MUST only call `rm` against files inside `.claude/logs/`** — never any other path. The Step 0 invocation is the only sanctioned `rm` call in this command; do not improvise additional cleanups.

**Emergency mode** (compacting/prompt-too-long): Skip the Step 1 reads — distill from in-context memory only (Step 2), then persist to memory.md (Step 3).

---

## Steps

### Step 0: Reset gate + get date

```bash
date +"%m%d%y %H:%M" && rm -f ".claude/logs/.quality-gate-active" ".claude/logs/.session-blocks-$(date +"%m%d-%H")" ".claude/logs/.tool-call-count" ".claude/logs/.compaction-occurred"
```

### Step 1: Read state (skip in emergency)

Read `.claude/memory.md` — the single session-state anchor.

### Step 2: Distill session (from in-context memory)

Extract and compress using **restorable compression** — preserve retrieval paths so the resumed session can restore full context from compressed form:

1. **Task** — one sentence
2. **Done/remaining** — 2-4 bullets, conclusions not process
3. **Decisions** — one line each, WHAT+WHY not HOW
4. **Learnings** — rules/facts for knowledge-nominations
5. **Files touched** — full paths of every file read or modified (not just modified — include key files _read_ that informed decisions). These are retrieval anchors for the resumed session.
6. **Active references** — URLs, API endpoints, external resources consulted. Drop content, keep the pointer.
7. **Next action** — precise, actionable instruction including which file(s) to read first

### Step 3: Persist handoff to memory.md

Edit `.claude/memory.md` so the resumed session can restore from it. Fold the distilled
session into the existing sections (Now ← Task + Next, Open Threads ← Remaining, Recent
Decisions ← Decisions, Blockers ← anything blocking), then append a `## Session Handoff`
block that carries the retrieval anchors a compact narrative would otherwise lose:

```markdown
## Session Handoff — HH:MM

**Task:** [one sentence]
**Done:** [bullets]
**Remaining:** [bullets]
**Decisions:** [bullets]
**Files:** [full paths — both modified and key reads]
**Refs:** [URLs, external resources — pointers only, no content]
**Next:** [precise action + which file(s) to read first]
```

Use `Edit` (not `Write`) so the 100-line completeness cap on `memory.md` Writes does not
apply; prune any stale prior handoff block as you go.

### Step 4: Promote and nominate learnings (only if discovered)

**Two-tier promotion:**

**Tier 1: Immediate promotion to `knowledge-base.md`** (high-confidence rules):

- User overrides (explicitly corrected something)
- Empirical facts (verified through testing or data)

Write directly with `[Source: User directive MMDDYY]` or `[Source: Empirical MMDDYY]`.

**Tier 2: Nominate to `knowledge-nominations.md`** (lower-confidence):

- Agent inferences (patterns observed but not confirmed)
- Hypotheses (things that seem true but need more evidence)

Append: `- [MMDDYY] /safe-clear: [learning] | Evidence: [source]`

**Rule: When in doubt, promote. A rule in knowledge-base.md that gets corrected later is better than a rule in nominations that never gets seen.**

### Step 5: Auto-resume (restorable decompression)

Do NOT output a resumption prompt. Do NOT ask the user anything. Instead:

1. Re-read `.claude/memory.md` and `.claude/knowledge-base.md` (compressed context reload — the Session Handoff block you just wrote carries the **Next** action)
2. **Restore from retrieval anchors** — re-read the file(s) specified in the **Next** field and any critical files from the **Files** list that the next action depends on. This is the decompression step: the handoff told you _what_ happened; re-reading the files restores _how_ to continue.
3. **Immediately execute the Next action** — pick up exactly where you left off

The user should experience a brief pause, then work continuing seamlessly. No visible "clearing" or "resuming" messages. Just keep working.

Target: 5-7 tool calls, <30 seconds. Emergency: 2-3 calls, <15 seconds.
