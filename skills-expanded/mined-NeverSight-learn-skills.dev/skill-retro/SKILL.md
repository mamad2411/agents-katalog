---
name: skill-retro
description: Post-use retrospective for any skill. Captures what worked, what was corrected, and what's missing — then proposes SKILL.md improvements. Drives continuous skill evolution.
version: 1.0.0
triggers:
  - skill retro
  - skill retrospective
  - review skill usage
  - improve this skill
  - what did we learn about this skill
auto_load:
  - ./reference/retro-template.md
  - ./reference/signal-capture-protocol.md
effort: normal
---

# Skill Retro

Transform skill usage into skill improvement. Every correction, workaround, and success pattern is a signal that the skill definition should capture for future sessions.

## Two Modes

### Inline Mode (End of Session)

Run after significant skill usage within the current session. Captures signals while conversation context is fresh.

**When to trigger:**
- A skill was used and the human corrected the output
- A skill was used and a workaround was needed (missing instruction, wrong default, unclear guidance)
- A skill was used successfully 3+ times and patterns are emerging
- The human says "remember this for next time" or similar after skill usage
- End of a session with heavy skill usage (2+ invocations of the same skill)

**Process:**
1. Identify which skill(s) were used in this session
2. For each skill, extract signals (see Signal Capture Protocol)
3. Write a retro entry to the skill's local `retro/` directory
4. Propose specific SKILL.md edits (present to human, don't auto-apply)

### Batch Mode (Periodic Review)

Run periodically (weekly, or when `/consolidate-memory` flags skill patterns). Reads accumulated retro entries across multiple sessions and proposes structural improvements.

**When to trigger:**
- The human explicitly asks to review a skill's retro history
- `/consolidate-memory` identifies recurring patterns in daily notes related to a specific skill
- A skill has 3+ retro entries that haven't been synthesized
- Before a major skill version bump

**Process:**
1. Read all entries in the skill's `retro/` directory
2. Identify patterns: recurring corrections, consistent gaps, emerging best practices
3. Propose SKILL.md changes: new sections, revised instructions, new quality criteria
4. Optionally propose additions to skill reference docs or examples
5. After human approves changes, archive processed retro entries

---

## Signal Types

| Signal | Description | Source | SKILL.md Impact |
|--------|-------------|--------|-----------------|
| **Correction** | Human corrected the output or approach | Conversation | Add instruction or constraint |
| **Workaround** | Output required manual post-processing | Conversation | Add step or automation |
| **Gap** | Skill didn't address a needed aspect | Conversation | Add section or quality criterion |
| **Success** | Pattern worked well, worth codifying | Conversation | Add to "What Works" or examples |
| **Context miss** | Skill needed information it didn't load | Conversation | Update auto_load or add context step |
| **Interaction** | Skill interacted with another skill in useful/problematic ways | Conversation | Add cross-reference or integration note |

---

## Retro Entry Format

Write each retro entry to: `[skill-dir]/retro/YYYY-MM-DD-[topic].md`

```markdown
---
date: YYYY-MM-DD
skill: [skill name]
mode: inline | batch
sessions_covered: 1 | [date range for batch]
status: raw | synthesized
---

## Signals

### Corrections
- [What was corrected and why. Include the before/after if useful.]

### Workarounds
- [What manual steps were needed that the skill should have handled.]

### Gaps
- [What the skill didn't cover that it should have.]

### Successes
- [What worked well and should be preserved or codified.]

### Context Misses
- [What information was needed but not available to the skill.]

## Proposed Changes

| # | Change | Type | SKILL.md Section | Priority |
|---|--------|------|-----------------|----------|
| 1 | [description] | correction / gap / enhancement | [section name] | high / medium / low |
| 2 | ... | ... | ... | ... |

## Raw Notes
[Any additional observations, quotes from the human, or context that might be useful later.]
```

---

## Inline Retro Process (Step by Step)

### Step 1: Identify Skill Usage

Scan the current session for:
- Explicit `/skill-name` invocations
- Auto-loaded skill triggers
- Skill-guided work (e.g., writing that followed voice-editor patterns)

### Step 2: Extract Signals

For each skill used, review the session for:
- **Corrections:** Where did the human say "no, not that" or redirect the approach?
- **Workarounds:** Where did the output need manual fixing?
- **Gaps:** What questions came up that the skill didn't anticipate?
- **Successes:** What parts of the output did the human accept without changes?
- **Context misses:** Was information needed that wasn't in the auto-loaded context?

**Follow the Signal Capture Protocol** in `./reference/signal-capture-protocol.md` for detailed extraction patterns.

### Step 3: Write Retro Entry

Write to `[skill-dir]/retro/YYYY-MM-DD-[topic].md` using the format above.

**Important:** Retro files are gitignored (they live in `retro/` which is in `.gitignore`). They contain session-specific details that should stay local. The *improvements* get applied to the shared SKILL.md; the *evidence* stays private.

### Step 4: Propose Changes

Present proposed SKILL.md edits to the human:
- Show the specific text to add/modify
- Reference which signal(s) drive each change
- Mark priority (high = blocks correct usage, medium = improves quality, low = nice to have)

**Do not auto-apply changes.** The human approves SKILL.md modifications because they affect the shared skill library.

---

## Batch Retro Process (Step by Step)

### Step 1: Gather Retro Entries

Read all entries in `[skill-dir]/retro/` where `status: raw`.

### Step 2: Pattern Analysis

Look for:
- **Recurring corrections** (same issue across 2+ sessions → high-priority fix)
- **Consistent gaps** (same missing capability → add to skill)
- **Converging successes** (same pattern works every time → codify as best practice)
- **Escalating workarounds** (workaround complexity increasing → structural fix needed)

### Step 3: Synthesize Improvements

Group findings into categories:
1. **Instruction changes** — add, modify, or remove SKILL.md instructions
2. **Quality criteria** — new or revised quality checks
3. **Reference docs** — new reference files or examples
4. **Auto-load changes** — files that should be loaded with the skill
5. **Trigger updates** — new trigger phrases based on actual usage

### Step 4: Present Improvement Plan

Format as a change proposal:

```
## Skill Improvement Proposal: [skill-name]

Based on [N] retro entries from [date range].

### High Priority
1. [Change] — Evidence: [which retro entries]

### Medium Priority
1. [Change] — Evidence: [which retro entries]

### Low Priority
1. [Change] — Evidence: [which retro entries]

### Recommended Version Bump
[patch (bug fix/clarification) | minor (new capability) | major (structural change)]
```

### Step 5: Apply and Archive

After human approval:
1. Apply approved changes to SKILL.md
2. Update skill version number
3. Add changelog entry
4. Mark processed retro entries as `status: synthesized`
5. Log the improvement to the daily note via `log-to-daily`

---

## Integration with Other Systems

### Proactive Signal Capture (MEMORY.md Protocol)

The memory system already mandates capturing corrections on first instance. Skill-retro extends this:
- When a correction is skill-related, write to the skill's retro directory (not just MEMORY.md)
- MEMORY.md captures behavioral rules; retro captures skill-specific improvements
- If a pattern spans multiple skills, it belongs in MEMORY.md. If it's specific to one skill, it belongs in retro.

### Consolidate Memory Integration

`/consolidate-memory` should check for:
- Skills with 3+ raw retro entries (suggest running batch retro)
- Daily note patterns that reference skill usage but don't have corresponding retro entries (suggest inline retro)

### Lessons Learned Relationship

`/lessons-learned` handles incidents and failures. `/skill-retro` handles ongoing improvement from normal usage. They overlap when a skill causes an incident — in that case, run lessons-learned for the incident and skill-retro for the skill fix.

---

## Constraints

- **Never auto-apply SKILL.md changes.** Always present for human approval.
- **Retro entries stay local** (gitignored). SKILL.md improvements are shared.
- **One retro entry per session per skill.** Don't fragment into micro-entries.
- **Batch mode requires 3+ raw entries** before synthesis. Don't over-synthesize from small samples.
- **Version bumps follow semver:** patch for clarifications, minor for new capabilities, major for structural changes.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Run inline retro for current session | `/skill-retro` or "let's do a skill retro" |
| Run batch retro for a specific skill | `/skill-retro batch [skill-name]` |
| Check which skills have pending retros | "which skills need retro review?" |
| Review a skill's retro history | "show retro history for [skill-name]" |
