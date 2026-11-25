---
name: qa-answer-review-business
description: >-
  Business lens of qa-answer-review: check a prepared meeting answer against the real process and
  who owns which decision — roles (regulator · customer · operator · our team), the document or
  data flow, scope, commitments and timelines, and consistency across all answers in the tab.
  Use WHENEVER the work is "business review of a prepared answer", "does this answer promise too
  much", "does this contradict the process", "คำตอบนี้รับปากเกินไหม", or when qa-answer-review fans
  out its lenses. Read-only.
---

# Business lens

Per row: **is this ours to say, and does it hold together with the process and the other answers?**

## Check, in order

1. **Process truth.** Write down the real flow (which step produces which document or record, and
   in what order) from the project's docs or wiki before judging any row. Answers that place data
   before/after a step must match it.
2. **Who decides.** A rule only the regulator or the customer can set (tolerances, legal formats,
   deadlines) must not be answered as if we decided it → `OPEN`, name the decider.
3. **Commitments.** Dates, "can do", "already have", "supported" are promises. Anything not backed by
   the program lens or a signed scope is `ADJUST` with a holding phrase ("being defined in the
   technical design").
4. **Consistency.** Read the whole tab once before judging a row. Flag pairs that contradict (an
   option offered in one row that another row or a team Remark says does not exist).
5. **Team Remark.** An existing Remark is a reviewer's objection — answer it in the note.
6. **Audience.** The customer hears this. Wording that blames them or exposes internals → `ADJUST`
   with a phrasing.

`N/A` only for rows that are purely technical with no process or commitment content (rare).
Output contract and tone rules: `answer-review/SKILL.md` §1.
