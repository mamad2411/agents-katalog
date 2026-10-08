---
name: review-context
description: Records which pull-request review comments a loop-spec role acted on, as a decision in its result. For roles.<role>.with on a role whose result has decisions (spec-writer, reviser).
---

Read `${CLAUDE_SKILL_DIR}/checklist.md` and apply it while you write your result.

Then add one entry to your result's `decisions`, with the id `D-PR-HELPER`. Its text
lists each review comment you acted on, as `path:line` for an inline comment or
`review` for a top-level one, then each one you did not act on with its reason. With
no pull request in your inputs, the text says `no pull request`. End the text with the
`checklist-version` line from the checklist.
