---
name: plan-readiness-review
description: "Use right before publishing or handing off a large plan, and for every revision — one knock-down pass on the sections added after the draft, then a mechanical checklist that blocks publishing while any finding is unowned, any decision was answered by the planner instead of its owner, anything is used before it is defined, or the body mixes decisions with execution logs. Produces READINESS.md with the final YES/NO. Skip for chat-only sketches that will not be executed."
author: SamuelStefano
tags: [planning, review, checklist, decisions]
---

# Readiness review — the final verdict

**Core principle:** readiness is a checklist run by B (who did not write phases
3–4) or a fresh agent — never A. One ✗ blocks publishing.

*(Plans were published under an expiring publish window, four times in one hour,
to a tracker with no delete. Their holes were structural and checkable.)*

## Step 1 — Knock-down on phases 3–4

The gates and PR table were added after the draft verdict. Run the knock-down
prompt from `plan-dual-draft/prompts.md` once on those sections, writing
`review-2.md` / `dialog-2.md` with IDs `R#N` (never overwrite the phase-2 files).

## Step 2 — Checklist → `READINESS.md`

Template: `complex-plan/templates/READINESS.md`. Each line ✓/✗ + evidence.

**Coverage**
- [ ] `COVERAGE.md`: no source item without a section or `dropped because`.
- [ ] Every review finding ID (`B#N` from the draft, `R#N` from step 1) maps to a PR row, Q-N, or "won't do + consequence".
- [ ] MVP = floor + ordered "if time" list, each with a fallback; the requester's #1 quality word is in the floor.

**Decisions**
- [ ] Every decision owned by someone else is a posted question (`templates/QUESTION.md`), not an answer in the body.
- [ ] Option space complete, including the decider's likely view.
- [ ] Labels read back from the plan tracker after posting (if there is one).
- [ ] No answer came from the planner's own account minutes after posting.
- [ ] No preference question flipped by a reviewer without evidence.
- [ ] Every answer that overrides an ADR is applied to the body.
- [ ] One representation per decision (question or body section, linked).

**Gates** (`plan-acceptance-gates`, `complex-plan` hard gates 3–10)
- [ ] Flags: flip row, owner, date, exit. Test/temporary choices: promotion row.
- [ ] Every phase accepted on the running build; every `MATRIX.md` row filled, or MATRIX declared N/A with a reason (no UI).
- [ ] Unknown limits measured in Phase 0.
- [ ] Every output has a consumer, a place, a single sender.
- [ ] Human gates and external manual steps named and dated, scheduled first.
- [ ] Secrets table complete; no grant to a public role without a threat line.

**Structure**
- [ ] `format-check.md` from `plan-dual-draft` prints no finding.
- [ ] Every PR row and phase has done-when (observed live) · depends-on · owner.
- [ ] Header lists what was not read (`sources/NOT-READ.md`).
- [ ] Body ≤ 60 KB (or a one-line reason); decisions and criteria only. Progress goes to `EXECUTION-LOG.md`.
  *(A plan grew from 43 KB to 184 KB of logs; its own lead said "I don't know what's going on anymore".)*

**Hygiene**
- [ ] Live state re-read just now (PRs merged while planning); every new reader or writer of the data the plan changes has a PR row; the header names the commit the citations are true at.
- [ ] Every output artifact classified public / internal / personal; nothing internal or personal goes public.
- [ ] Audience and visibility match the decider.
- [ ] Tasks created from the PR table, linked to the plan, each with an owner.

End: `Verdict: YES|NO` + at most 3 residual risks, each with an owner. On YES,
copy the body to `PLAN.md`.

## Publishing

Draft and review locally; publish once, after YES. If the tracker has a
time-limited publish permission, open it only then. Afterwards read the plan back
through the tracker and confirm owner, extracted decisions and question count.
No tracker: the plan file in git is the record.

Before asking for a publish window:
- **Count the writes** — body, appendices, one per question — and say the number.
  *(A three-write window met a plan with eight questions; the body went out with
  none of them.)*
- Read how the tracker parses decisions (its docs or tool description), write the
  ADR fields in that exact shape, and clear every `warn:` about field punctuation
  before the first publish; then compare **extracted count with ADR count** on that
  publish, before posting anything else.
- Make one **read** against the tracker right before the first write. *(A
  rate-limit error consumed one of three authorisations and published nothing.)*
- A body that points to local files is unreadable to the decider. Publish the
  appendices with it, or keep that content in the body. The size budget is for what
  the decider reads; it is not a reason to move decisions out of their sight.
  Going over 60 KB for this is a valid one-line reason.
- Keep a copy of the body exactly as published (`PLAN-v<n>-published.md`).
- Log every publish at once in `EXECUTION-LOG.md` (create it now): version, what
  changed, any base hash the tracker wants on the next write, what is still only
  local. *(Three publishes in one evening; the log was the only record of which
  version the decider was reading.)*

## Revisions

Re-run `plan-ground-truth` steps 3 and 7 against the sources, add
`decided in vN → still valid today?`, list "changed since vN", reconcile task
statuses before rewriting, and turn every answered question into a task the same day.

**When the decider's review adds scope** (the common first revision): quote the
request verbatim in `COVERAGE.md` and in the plan header; audit the code the new
scope touches before writing a row; edit the body; then run one knock-down **on the
diff against the published copy**, by an agent that did not write it, and apply it
before republishing. New decisions inside the added scope are new questions. If
the decider says a request is specific to this plan, it stays in this plan: do not
copy it into a skill, template or retro rule.
*(Three requests from the decider became two ADRs and seven rows; the knock-down on
that diff alone returned 24 findings — a token leak through the test report, a
false premise about which secrets existed, and a panel placed on the launch's
critical path.)*
