---
description: Review recent work and capture what deserves to go into lessons-*, architecture, operations, and the current plan.
disable-model-invocation: true
---

# Capture lessons

You're called at the end of non-trivial work to do a capture-and-update pass on the docs. You don't capture everything — apply the relevance filters below aggressively and propose concrete, actionable additions.

## Project overlay

Before anything else, check whether this project provides an overlay for this command at `.claude/armature/capture-lessons.md` (relative to the project root).

- **If it exists**, read it and announce: "**Surcharge projet active** (`.claude/armature/capture-lessons.md`)". It holds named markdown sections that extend this command:
  - `## before` / `## after` — reserved lifecycle hooks: run `## before` now (before the process below), and `## after` at the very end.
  - a section whose name matches a `[project anchor: <id>]` marker placed in this skill — inject its content at that marker's location.
  - any section matching neither a reserved hook nor a declared anchor: ignore it.
  - Execute the `## before` section now if present.
- **If it does not exist**, proceed normally — this command behaves exactly as its base, with nothing injected.

## Common targets (non-exhaustive)

The targets below cover most cases. **This isn't a closed list**: if another file is the right place (`CLAUDE.md`, a sub-folder README, a feature-specific doc, an `accepted` ADR to supersede, or even a new file to create), go there. Choose the target based on the nature of what you're capturing; don't force information into a box it doesn't belong in.

| File | When to write there |
|---|---|
| `docs/lessons-technical.md` | Non-obvious technical traps: framework/library quirks, tooling traps, subtle runtime behavior |
| `docs/lessons-domain.md` *(if this project has one)* | Business rules, domain invariants, semantics that can't be guessed from code alone |
| `docs/architecture.md` | Changes affecting "how the system works today" (new relationship between components, newly adopted pattern) |
| `docs/operations.md` | Commands, workflows, prerequisites for setup / build / run / deploy / migrations |
| `docs/plans/<slug>.md` (in-progress) | Progress log (lot shipped), follow-ups surfaced during implementation, remaining open questions |
| *other* | If the right place isn't in this table, propose it to the user with a justification |

> `[project anchor: capture-targets]` — if a project overlay defines a `## capture-targets` section, fold its project-specific targets/examples into the routing above (e.g. domain areas, stack-specific traps, a per-file supersede example).

## Relevance criteria — aggressive filter

### Capture **if and only if**:
- **Not derivable from code** — no contributor could reconstruct this by reading the files. If the answer is "grep + 5 min of reading", skip.
- **Non-obvious** — an experienced developer wouldn't guess it on the first try. If it's a common idiom of the language/framework, skip.
- **Actionable** — the lesson says what to do or avoid. A pure description helps no one.
- **Stable** — it'll stay true for at least 6 months. A specific bug fix doesn't belong in lessons — the commit message is enough.
- **Costly to rediscover** — the next person who hits this will visibly lose time (> 30 min) if the lesson doesn't exist.

### Never capture:
- Solutions to specific bugs (commit + PR are enough)
- Conventions already visible in the code (naming, formatting)
- Things a test already covers
- Volatile details (library versions, env config)
- A restatement of an existing lesson (update it instead)

## Process

### 1. Frame the scope

Re-read the last commits (`git log -20 --oneline`) and/or the current conversation. If scope is unclear, ask the user briefly.

### 2. List candidates

Build two mental columns:
- **Pass**: items that check *every* box in the "capture if" list.
- **Rejected**: close-but-not-quite items that miss one criterion — mention them in 1 line to show you didn't forget them.

Target: **2 to 4 items to capture** per typical pass. If you have more, you're filtering poorly — tighten up.

### 3. Write following the target file's format

#### `lessons-technical.md` / `lessons-domain.md` (append-only, add at top)

```markdown
## [Actionable title in one sentence]

[Body: 2-3 paragraphs. Start with the context/situation where the trap shows up. Follow with the rule or pattern to apply. End with a concrete example from this repo if relevant.]

_Captured YYYY-MM-DD._
```

- **Don't rewrite old entries.**
- If an old lesson needs invalidating, add a new one at the top AND mark the old one *superseded*, preserving its body as a blockquote.

#### `architecture.md` / `operations.md` (directly editable)

These two files are **not** append-only. Edit the precise section concerned, avoid mass rewrites. Keep the existing tone and structure.

#### `docs/plans/<slug>.md` in-progress

> Skip `docs/plans/template.md`: it is the shipped stub, and its `in-progress` frontmatter is the correct starting value for a real plan — not a signal that one is open.

- **Progress log**: if a lot shipped, add a line to the *Progress* section with the merge commit's SHA.
- **Follow-ups**: anything surfaced that's out of the current plan's scope → *Follow-ups surfaced during implementation* section, dated.

### 4. Propose before committing

Before editing, present the short list (passed + rejected) to the user for validation. This avoids capturing noise or missing something important.

### 5. Separate commit

This whole pass is **one `docs:` commit**. Never mix with code.

### Final — project `after` hook

If a project overlay defined a `## after` section, apply its instructions as the closing step — including any project-specific commit/VCS convention, which takes precedence over the generic `docs:` commit above. No overlay ⇒ skip.

## Before proposing each item, ask yourself

- *"Would a new contributor really lose time if this info didn't exist?"* — if unsure, drop it.
- *"Could an LLM guess this info by reading the repo's code?"* — if yes, drop it.

## What you do NOT do

- Capture "everything that happened in the conversation" — you're a filter, not a log.
- Write descriptive lessons ("here's how X works") instead of actionable ones ("when you hit X, do Y").
- Touch code in this pass — docs only.
- Rewrite or summarize an existing lesson to "clarify" it — it's in the history, leave it alone or supersede it explicitly.
- Capture when the session produced nothing non-obvious — it's perfectly fine to conclude "nothing to capture".
