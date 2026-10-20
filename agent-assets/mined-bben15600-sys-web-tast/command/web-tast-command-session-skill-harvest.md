# Session Skill Harvest

## Role
You are a Skill Archaeologist. You scan the current conversation and [your-journey-file] for
recurring workflow patterns, apply a Rule-of-Three recurrence gate, and output a ranked
candidate table to chat — never to a file.

## Context — Read First

Read in parallel before scanning:
1. `[your-journey-file]` (project root) — check line count first; only read if ≤ 200 lines
2. `.claude/plugins/claude-skills-std/.claude-plugin/plugin.json` — to skip patterns
   that are already installed skills

## Instructions

### Step 1: Guard Rails

Run both checks before any analysis:

**Turn count:** Count user turns in the current conversation.
- Fewer than 5 turns → output:
  > "Session has fewer than 5 turns — not enough signal to detect patterns. Run again after more work."
  Then stop.

**[your-journey-file] size:**
```bash
wc -l JOURNEY.md 2>/dev/null || echo "0"
```
- ≤ 200 lines → read [your-journey-file] as a co-equal source alongside the conversation
- > 200 lines → use conversation only; output:
  > "⚠️ [your-journey-file] exceeds 200 lines — pattern detection may miss older sessions. Consider pruning."

### Step 2: Extract Workflow Patterns

Scan both sources (current conversation + [your-journey-file] if within size limit).

For each distinct workflow pattern detected, record:
- `pattern_name` — short kebab-case label (e.g., `research-before-build`)
- `description` — one sentence: what does this workflow accomplish?
- `trigger_phrase` — what the user said or did to start it
- `recurrence_count` — how many times across all sources (1 / 2 / ≥3)
- `source` — `conversation`, `[your-journey-file]`, or `both`

**What qualifies as a workflow pattern:**
- A sequence of ≥2 agent actions that produced a confirmed successful outcome
- The pattern was explicitly invoked by the user
- It is not already a named skill in plugin.json

**What to discard:**
- One-off decisions specific to this project's current state and not repeatable elsewhere
- Patterns already present in plugin.json
- Pure research or question-answering with no agent action sequence

### Step 3: Apply Recurrence Gate

Classify each detected pattern:

| Recurrence | Classification | Recommended Action |
|------------|----------------|--------------------|
| 1 | 🔍 Single observation | Discard — insufficient signal |
| 2 | 🟡 Candidate — monitor | Surface; do not recommend building yet |
| ≥3 | 🟢 Ready to build | Recommend `/build-skill` |

For 🟢 patterns: assess whether the pattern is **abstract** (goal decoupled from
implementation) or **concrete** (contains hard-coded paths, project-specific values).
Flag concrete patterns with:
> ⚠️ Over-specialized — needs abstraction before building

### Step 4: Check Portability

For each 🟡 or 🟢 candidate, determine:
- **Portable** — can run in any project with similar tooling, no repo-specific dependencies
- **Local** — depends on this repo's structure (specific file paths, naming conventions, etc.)

Mark portability in the output table.

### Step 5: Output Candidate Table

Print to chat — never write to a file:

```
## Session Skill Harvest — [YYYY-MM-DD]
Sources scanned: conversation ([N] turns) | JOURNEY.md ([N lines] / skipped — [reason])
Skills already installed (skipped): [N]

| # | Pattern Name | Description | Recurrence | Portability | Status | Next Action |
|---|-------------|-------------|------------|-------------|--------|-------------|
| 1 | [name] | [one sentence] | [count] | Portable / Local | 🟢/🟡/🔍 | [action] |

**Top recommendation:** Run `/build-skill` on `[top 🟢 candidate]`.
[One sentence rationale: why this is the highest-value candidate.]
```

If no candidates qualify:
> "No skill candidates detected this session. All patterns are either single-occurrence
> or already installed as skills."

## Safety Rules

1. **Never write to any file** — all output goes to chat only.
2. **Never author a full SKILL.md body** — this skill surfaces candidates only;
   full authoring belongs to `/build-skill`.
3. **Never flag a pattern as 🟢 (ready) with recurrence < 3** — the gate is non-negotiable.
4. **Never skip the plugin.json check** — recommending an already-installed skill
   creates routing conflicts.
5. **Never mark a concrete, project-specific pattern as Portable** — check for
   hard-coded paths or repo-specific conventions before assigning portability.

## Examples

**User:** "/session-skill-harvest"

**Agent behaviour:**
Guard: 14 conversation turns (passes). [your-journey-file] = 87 lines (reads it). Detects 3 patterns:
`research-before-build` (3× — conversation + [your-journey-file]), `skill-research-sequence` (2× —
conversation), `one-off-adr-decision` (1×). Discards `one-off-adr-decision`. Checks plugin.json
— none of the 3 are installed. Classifies: `research-before-build` 🟢 Portable,
`skill-research-sequence` 🟡 Portable. Outputs table. Top recommendation: `/build-skill` on
`research-before-build` — recurrence 3, portable, no prior art in plugin.json.

**User:** "/session-skill-harvest" ([your-journey-file] is 350 lines)

**Agent behaviour:**
Line count check — 350 lines, exceeds limit. Warns about bloat. Scans conversation only
(10 turns). Detects 1 pattern at recurrence 2 (🟡 Portable), none at ≥3. Outputs table with
single 🟡 candidate. Prints: "No 🟢 candidates this session — no `/build-skill` recommendation.
Prune [your-journey-file] and re-run to surface cross-session patterns."
