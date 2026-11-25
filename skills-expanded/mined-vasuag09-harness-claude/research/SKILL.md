---
name: research
description: Reuse-first research before writing new code. Search existing libraries, registries, and codebases for something that already solves the problem. Use after /spec, before /plan. Mandatory for non-trivial implementation.
---

# /research — reuse before you build

Goal: never hand-roll what a proven solution already does well. Find the 80%-fit and
adopt/port it.

## Do this (in order)
1. **In-repo first** — does this codebase already solve a near-identical problem? Use
   the knowledge graph / `mgrep` (or `Grep`/`Glob` if those are unavailable) to find
   existing patterns, utilities, and conventions.
2. **Library docs** — use **context7** (or the library's primary docs / web if context7
   is unavailable) to confirm current API/behavior of candidate libraries (don't answer
   from memory; versions drift).
3. **Code & registries** — search GitHub and the relevant package registry (npm / PyPI)
   for battle-tested implementations or templates that fit ≥80%. When several candidates fit,
   compare them on fit %, maintenance/activity, license, and footprint — pick deliberately and
   note the runner-up; don't just grab the first hit.
4. **Broader web** — only if the above are insufficient (`mgrep --web "..."`, or
   `WebSearch` if mgrep is unavailable).

For LLM/agent work, read the harness's relevant references before choosing an approach.

## Output
```
## Reuse decision
- Adopt / port / wrap: <library or repo>  — why it fits
- Build new: <only the genuinely novel part>  — why nothing fits
## Key API facts (from context7) that the plan must respect
## Risks of the chosen dependency (maintenance, license, size)
```

## Exit criterion
A documented build-vs-reuse decision with evidence. Fold it into the spec. Then `/harness-claude:plan`.
