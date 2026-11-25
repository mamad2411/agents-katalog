---
name: skill-compiler
description: "Automatic solved-to-skill compiler — detects novel task completions and autonomously drafts new SKILL.md files. Stolen from Hermes Agent's learning loop (NousResearch, 2026-05-11)."
vibe: "Every hard problem you solve once, you never solve again."
context_trigger: "novel, breakthrough, new pattern, first time, never done before, complex task"
auto-invoke: false
model: default
source: "NousResearch/hermes-agent (143K ★) — 'The agent that grows with you'"
stolen_date: "2026-05-11"
---

# Skill Compiler — Solved-to-Skill Automation

> **Source:** Hermes Agent by Nous Research (May 2026)
> **Core Claim:** "It's the only agent with a built-in learning loop — it creates skills from experience."
> **Athena Adaptation:** Hermes does this via Python (`agent/curator.py` + `tools/skill_usage.py`). Athena does it via workflow-level pattern detection + markdown SKILL.md generation.

## The Problem This Solves

Athena currently relies on **manual insight filing** during `/end` sessions. The `[S]` and `[V]` markers in session logs capture learnings, but they remain trapped in session logs — they don't **become** reusable skills automatically.

Hermes solved this: when the agent completes a novel task, it automatically creates a new skill from the solution, so the same problem class never requires re-derivation.

## When to Use

### Automatic Trigger (Post-Task Detection)

After any task completion where **ALL** of the following are true:

1. **Novelty**: The task required a solution path not covered by any existing skill
2. **Complexity**: Task took ≥5 agent turns OR involved ≥3 tool calls
3. **Success**: User confirmed the solution worked (explicit or implicit — no corrections in final 2 turns)
4. **Reusability**: The solution generalizes beyond this specific instance

### Manual Trigger

User says: "compile this into a skill", "save this as a skill", "I want to remember how we did this"

## Execution Flow

### Phase 1: Pattern Extraction (Analysis)

Perform private analysis in `<analysis>` tags (not written to files):

```
<analysis>
1. What was the PROBLEM CLASS? (Not the specific instance)
   - e.g., "Pairs trading dashboard with cointegration analysis"
   - NOT "Dashboard 4-decimal rounding fix"

2. What was the SOLUTION ARCHITECTURE?
   - Key steps in order
   - Tools/APIs used
   - Decision points and their resolution criteria

3. What were the FAILURE MODES encountered?
   - What went wrong initially?
   - What heuristics resolved it?

4. What is the REUSE SURFACE?
   - When would someone encounter this problem class again?
   - What context_trigger keywords would match?

5. OVERLAP CHECK
   - Which existing skills partially cover this?
   - Is this better as a new skill or a subsection of an existing one?
</analysis>
```

### Phase 2: Skill Draft Generation

Generate a complete SKILL.md with Athena-standard 5W1H frontmatter:

```markdown
---
name: [kebab-case-name]
description: "[One-line description of what the skill does]"
vibe: "[One-line emotional hook]"
context_trigger: "[comma-separated trigger keywords]"
auto-invoke: false
model: default
source: "Compiled from session [SESSION_ID] on [DATE]"
compiled_from: "[session log path]"
---

# [Skill Name] — [Subtitle]

> **Compiled**: [DATE] from session [SESSION_ID]
> **Problem Class**: [Description of the general problem this solves]

## When to Use

[Trigger conditions — when should the agent invoke this skill?]

## Solution Architecture

### Step 1: [Phase Name]
[What to do, with specifics]

### Step 2: [Phase Name]
[What to do, with specifics]

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| [What can go wrong] | [How to recover] |

## Validated Patterns

- [V] [Pattern]: [Why it works] | Reapply: [When]

## References

- Session log
- [Related skill](../../therapeutic-ifs/SKILL.md)
```

### Phase 3: Integration

1. **Write** the skill to `.agent/skills/[name]/SKILL.md` (or `examples/skills/[category]/[name]/SKILL.md` for public)
2. **Update** skill index with the new entry
3. **Update** `AGENTS.md` skill table (if context_trigger present)
4. **Notify** user: "📦 Compiled new skill: `[name]` from this session. Review at [path]."

## Curator Integration (Stolen: Hermes `agent/curator.py`)

### Lifecycle States

Compiled skills follow a lifecycle identical to Hermes' curator model:

| State | Criteria | Action |
|-------|----------|--------|
| **active** | Created or used within 30 days | Normal operation |
| **stale** | No invocation for 30+ days | Flag for review at next `/audit` |
| **archived** | No invocation for 90+ days | Move to archive directory |

### Invariants (from Hermes)

- **Never auto-delete** — maximum destructive action is archive
- **Pinned skills are exempt** — manual pin via `pinned: true` in frontmatter
- **Only touch compiled skills** — bundled/manual skills are off-limits
- **Archive is recoverable** — archive directory with successor mapping in README.md

### Umbrella Consolidation Rule (Stolen: Hermes Curator Prompt)

> "A collection of hundreds of narrow skills where each one captures one session's specific bug is a FAILURE of the library — not a feature."

When compiling a new skill, first check if it belongs as a **subsection** of an existing umbrella skill rather than a standalone entry:

1. **PREFIX CLUSTER CHECK**: Does the new skill share a first word or domain keyword with 2+ existing skills?
2. **CLASS-LEVEL CHECK**: Would a maintainer write this as one skill with labeled subsections, or N separate skills?
3. If the answer is "one skill", absorb into the existing umbrella and add a `references/` entry instead.

## Anti-Patterns

- ❌ Compiling trivial tasks (< 5 turns, single tool call)
- ❌ Compiling tasks that are already covered by existing skills
- ❌ Creating overly specific skills tied to one instance (use umbrella pattern instead)
- ❌ Compiling without user confirmation of success
- ❌ One-session-one-skill micro-entries — consolidate into class-level umbrellas

## Hermes Comparison

| Feature | Hermes | Athena |
|---------|--------|--------|
| Skill creation | Automatic (Python `skill_manage`) | Workflow-triggered (this SKILL.md) |
| Skill lifecycle | `curator.py` (7-day review cycle) | `/audit` + archive directory |
| Skill evolution | DSPy + GEPA (self-evolution repo) | Manual via `/steal` + session learnings |
| Skill storage | `~/.hermes/skills/` (SQLite telemetry) | `.agent/skills/` (git-tracked) |
| Consolidation | LLM-driven umbrella-ification pass | Manual during `/audit` |

**Athena advantage**: Skills are version-controlled in git, not SQLite. Every skill change has a commit hash, blame, and diff history. Hermes can't `git blame` a skill edit.

## References

- [Hermes Agent Curator](https://github.com/NousResearch/hermes-agent/blob/main/agent/curator.py) — Source of lifecycle states + umbrella consolidation pattern
- [Hermes Self-Evolution](https://github.com/NousResearch/hermes-agent-self-evolution) — DSPy + GEPA evolutionary optimization (future steal candidate)
