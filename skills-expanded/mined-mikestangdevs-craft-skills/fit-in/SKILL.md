---
name: fit-in
description: "Use before writing new code into an existing codebase. Reads the surrounding code first and matches its idioms — error style, test layout, naming, imports, existing helpers — instead of importing a generic house style. Use when AI-generated code is correct but doesn't look like the rest of the repo, or when starting in an unfamiliar repo."
---

# Fit In

## The failure mode this fixes

Agents write correct code in the wrong dialect. The repo uses result types; the agent throws. Tests live next to the source; the agent creates `__tests__/`. Everything is `snake_case`; the new file is `camelCase`. None of it is a bug, and all of it is cost: every divergence is a seam a reader must mentally translate across, and a codebase edited by agents long enough becomes a patchwork of five house styles with no house.

The deepest version of this failure is solving a problem the codebase has *already solved* — writing a second retry helper, a second date formatter, a second pagination pattern — because the agent never looked. This skill makes reading the neighborhood a mandatory first step: match the local idiom, reuse the local solutions, and treat "improving" the style as a separate, deliberate act.

## When to Use This Skill

- Writing new code (function, file, module, test) into an existing codebase
- Reviewing AI-generated code that is correct but stylistically foreign
- Starting work in an unfamiliar repo where your defaults would otherwise win
- A reviewer keeps saying "we don't do it that way here"

**Don't use when:** the repo is greenfield with no established conventions (pick good ones; there's nothing to match), or when the local pattern is itself a failure mode a sibling skill exists to fix — don't replicate swallowed errors to fit in (`loud-errors` wins), and don't copy vague naming to match the neighbors (`name-things` wins). Convention never outranks correctness.

## Instructions

### 1. Read the neighborhood before writing a line

Open the files that will surround your change — siblings in the same directory, the module that will call yours, one or two recent files doing similar work. You're extracting the local dialect:
- **Error handling** — exceptions, result types, error returns? How are errors wrapped and reported?
- **Tests** — framework, location (`*.test.ts` beside source vs `tests/`), naming, fixture style
- **Naming & casing** — file names, identifiers, suffix conventions (`Service`, `Repo`, `Handler`?)
- **Structure** — how files are laid out, how imports are ordered and grouped, how modules expose their API
- **Existing solutions** — utilities, helpers, and patterns already solving pieces of your problem

If `CONTEXT.md` exists, start from its Conventions section — then verify against the code. If they disagree, trust the code and flag the drift.

### 2. Reuse before you write

For each piece of your task, check whether the codebase already has the solution — the retry wrapper, the validation helper, the test factory. Grep before you build. The second implementation of a solved problem is the patchwork's first stitch.

### 3. Write in the local dialect, even where you'd choose differently

Your preference for a different error style, test layout, or naming scheme is not a reason to diverge. The reader's cost of a mixed-dialect file outweighs the marginal elegance of your habit. Match what's there.

### 4. When the local idiom is genuinely harmful, don't silently replicate it

If matching would mean copying a real defect pattern — swallowed errors, untested I/O-fused logic, ban-list names — don't propagate it and don't unilaterally "fix the house style" either. Write the new code right, note the divergence explicitly (one line in the summary or PR: "new code uses X; existing files use Y — flagging the inconsistency"), and let the human decide whether a deliberate migration is worth opening.

### 5. Park the style crusade

If reading the neighborhood made you want to restyle it: that's not this task. A small touched-code improvement is a `boyscout` call; a sweeping migration is its own proposal. Fitting in and improving the style are both legitimate — they're just never the same change.

## Output format

```
NEIGHBORHOOD READ
  error style:   <observed pattern + example file>
  tests:         <framework, location, naming>
  naming/casing: <conventions observed>
  structure:     <layout & import conventions>

REUSED (instead of rewritten)
  - <existing helper/pattern> @ <file> — used for <which part of the task>

DIVERGENCES (deliberate, flagged)
  - <where new code differs and why> — local idiom was <pattern>; not replicated because <harm>

DRIFT (CONTEXT.md vs code, if any)
  - <what the glossary/conventions claim> vs <what the code does>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Importing your house style | The code is fine and foreign. Every divergence is a translation cost for the next reader. |
| Writing before reading | You can't match a dialect you never heard. The neighborhood read is the skill. |
| Re-solving a solved problem | A second retry helper means every future reader must learn both and guess which is canonical. |
| Matching the worst file | "Fit in" means the prevailing convention, not the one rotten file nearby. Match the pattern the team is moving *toward*. |
| Silently replicating a defect to conform | Consistency never outranks correctness — write it right and flag the inconsistency out loud. |
| Restyling the file while you're there | That's a crusade wearing a task's clothes. Park it (`boyscout` for small, a proposal for big). |

## Mental Model

> Code that fits in reads like it was always there. Match the campsite's dialect; improving the dialect is a real job, but it's a different one.
