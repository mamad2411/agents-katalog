---
name: build
description: Deliver a feature or ticket end to end through requirements, exploration, test-driven implementation, documentation sync, verification, and a merged pull request. Use when the user asks to "build" or "implement" work end to end. Use $implement or $ship for only part of the lifecycle.
---

# Build

Read every applicable `AGENTS.md` before starting. More specific nested instructions override broader ones, and every stage defers to them.

1. **Requirements** — Gather the request and linked ticket. Distill them into an explicit list of observable behaviors that becomes the contract for `$implement` and the acceptance criteria for `$verify`. Explore the codebase instead of asking questions it can answer. If requirements remain ambiguous, contradictory, or materially larger than stated, run `$grill-me` in an interactive session. If the user is unavailable, stop and report the unresolved decisions rather than building a guess.
2. **Explore** — Spawn a read-only collaboration subagent to identify affected files, patterns and utilities to reuse, test conventions, and risks. Keep its concise brief, not its transcript. Establish the branch according to repository convention.
3. **Implement** — Invoke `$implement` with the behavior list and this explicit constraint: **do not commit or push; leave a verified working diff so `$pr` owns staging and commits**. Use `$tdd` at agreed seams, then run `$simplify` over the resulting diff.
4. **Synchronize docs** — Run `$docs` before shipping so documentation fixes land in the same PR.
5. **Ship** — Run `$ship` to verify the behavior, check UI changes, open the PR, and babysit it through the authorized terminal condition.

Treat artifacts, not conversational memory, as the contract between stages: the behavior list, exploration brief, implementation report, verification evidence, and diff. Re-read the diff whenever earlier state is uncertain.

- Use collaboration subagents for noisy independent stages such as exploration, verification, and PR monitoring when available.
- If `$verify` finds a required behavior missing, return to `$implement` with a failing test first, preserving the no-commit constraint, then resume.
- Re-run requirements when they change midstream.
- Trust observed code over a ticket's claim about current implementation and report the discrepancy.
- Keep surrounding cleanup out of the feature. Suggest a separately scoped `$improve-vibecode` pass when broader consolidation is justified.
