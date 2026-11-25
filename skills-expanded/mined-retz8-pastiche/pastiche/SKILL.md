---
name: pastiche
description: Use when implementing a frontend task — produces code that faithfully follows the project's design system and component library.
---

# Pastiche

Orchestrates `pastiche-implementer-round1`, `pastiche-reviewer`, and `pastiche-implementer-round2` in a bounded loop, then emits a single task report.

## Preflight

Run `ls pastiche/FACT.md pastiche/KNOWLEDGE.md pastiche/WISDOM.md`. If any are missing, stop and report:

> This project does not appear to have pastiche set up — expected `pastiche/{FACT,KNOWLEDGE,WISDOM}.md`. Run `/pastiche-init` to scaffold them.

## Workflow

1. Dispatch `pastiche-implementer-round1` with `{task}` → capture `{r1_report}`.
2. Dispatch `pastiche-reviewer` with `{task, r1_report}` → capture `{doubts}`. The reply is either one or more lines of `<path>#<line> | <comment>`, or the literal `(no doubts)`. If any line fails to match the record shape and the output isn't `(no doubts)`, stop and report:
   > Reviewer returned malformed output; expected `<path>#<line> | <comment>` records or the literal `(no doubts)`.
3. If `{doubts}` is `(no doubts)`, go to 6 (no `{r2_report}`).
4. Dispatch `pastiche-implementer-round2` with `{task, r1_report, doubts}` → capture `{r2_report}`.
5. **Failsafe.** For each record in `{r2_report}`'s `unresolved:` block (skip if `unresolved: -`): Read the file, then Edit to insert a comment in the file's native comment syntax above the targeted `<line>` (matching surrounding indentation). Comment text: `pastiche-unresolved-doubt: <comment from the unresolved: record>`.
6. **Build check.** Read `build_command` from `pastiche/config.yaml`. If null or absent, skip. Otherwise run it. For each error, patch using the build output as source of truth. Bounded to **3 patch attempts per error**. If an error persists after 3 attempts, leave it and note it in Follow-ups.
7. **Runtime review.** Scan the changed files for common sources of runtime and console errors. Patch any issues found. Bounded to **one pass**.
8. Emit the final response.

## Final response

```
## Summary
- **Files changed:** <paths> (omit if none)
- **Implementation:** <2–3 sentences describing the end result>

## Follow-ups
- <location> — <one-line description>
- ... (omit section if no follow-ups)
```

`Files changed` is the union of `files:` entries from `{r1_report}` and `{r2_report}`; omit the line if both are `-`.

Follow-up sources (each follow-up bullet must be self-describing; readers shouldn't need to know about rounds, dispositions, or the loop):

- Each scenario in `{r1_report}`'s `gaps:` line → `KNOWLEDGE.md — <scenario>`.
- Each `(knowledge-gap)`-tagged record in `{r2_report}`'s `defended:` block → `KNOWLEDGE.md — <reason>`.
- Each `(wisdom-gap)`-tagged record in `{r2_report}`'s `defended:` block → `WISDOM.md — <reason>`.
- Each record in `{r2_report}`'s `unresolved:` block → `<path>#<line> — <comment>`.
- Each failsafe comment written in step 5 → `<path>:<line> — <comment>`.
