---
name: overlap

description: Find skills with similar or overlapping responsibilities. Use when the skill set feels redundant, two skills seem to do the same thing, or you want to check whether a skill should be merged, renamed, or kept separate.

metadata:

  disable-model-invocation: true

---

# Overlap

Do these skills do the same thing?

This skill identifies skills whose responsibilities, triggers, or intended outcomes overlap.

The goal is to distinguish between:

- Skills that are genuinely different but related
- Skills with partially overlapping responsibilities
- Skills that are sufficiently redundant that they may be better merged

It is a **skill-set consistency check**, not a general similarity search.

## Step 1 — Discover available skills

Build a fresh inventory of the skills currently available to the agent.

Prefer the agent's native skill discovery or listing mechanism when available. If necessary, fall back to filesystem discovery using the current environment's skill locations.

For each skill, inspect at least:

- `name`
- `description`

Read the full skill definition when necessary to understand its actual boundaries and behavior.

Do not rely on a cached skill inventory.

## Step 2 — Compare responsibilities

Compare skills based on their actual responsibility, not just similar wording or names.

Consider:

- Primary purpose
- Trigger conditions
- Expected input
- Expected output
- Main decision being made
- Scope of responsibility
- Explicit boundaries
- Natural position in a workflow

Do not classify two skills as overlapping merely because they operate in the same general area.

For example:

> `ask` and `skill-gap` both reason about available skills, but they answer different questions.

That is related functionality, not necessarily redundancy.

## Overlap levels

Classify each meaningful relationship as one of:

### Related

The skills operate in the same area but have clearly different responsibilities.

They should generally remain separate.

### Partial overlap

The skills share meaningful responsibility or can trigger in similar situations, but each still has a distinct purpose.

Recommend clarifying their boundaries when useful.

### Redundant

The skills have substantially the same purpose, trigger, and outcome.

They may be better merged, or one may be unnecessary.

Do not recommend merging solely because two descriptions contain similar words.

## Identify the strongest overlaps

Prioritize overlaps that could cause real confusion.

Examples:

- A user would reasonably choose either skill for the same request.
- The agent could route to either skill without a clear distinction.
- The skills produce substantially the same output.
- One skill's responsibility is mostly contained inside another.
- The distinction between them depends only on wording rather than behavior.

Ignore trivial similarities.

## Recommend an action

For each significant overlap, recommend one of:

- **Keep separate** — responsibilities are sufficiently distinct.
- **Clarify boundaries** — keep both, but make their responsibilities more explicit.
- **Merge** — responsibilities are too redundant to justify separate skills.
- **Rename** — the functionality is distinct, but the names make the overlap appear worse than it is.

Do not recommend changes when the existing separation is already clear.

## How to answer

Format every reply as:

### Overlaps

For each meaningful relationship:

**`skill-a` ↔ `skill-b`** — `Related`, `Partial overlap`, or `Redundant`

<one or two sentence explanation>

### Recommendation

<Keep separate / Clarify boundaries / Merge / Rename>

If there are multiple significant overlaps, rank them from most important to least important.

If no meaningful overlap exists:

### Overlaps

None.

### Recommendation

The current skill boundaries are sufficiently distinct.

Stop after that.

## Important boundaries

This skill does not:

- Modify any skill
- Merge skills automatically
- Rename skills automatically
- Remove skills
- Create new skills
- Judge whether a skill is useful in isolation

Its purpose is to identify **redundancy and unclear boundaries between existing skills**.

## Maintenance

This skill should remain focused on detecting meaningful responsibility overlap between available skills.

Only update this file when its comparison criteria, overlap levels, or output format need to change.