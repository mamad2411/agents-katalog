---
name: grill
description: "Challenge plans by extracting every open decision from the PRD and resolving them one by one — skip none. Interview relentlessly about every aspect of the plan, walking down each branch of the design tree until shared understanding is reached. Use after think to validate the plan against the existing domain model, sharpen terminology, update CONTEXT.md and ADRs. Trigger words: challenge, 细化和验证, deep dive, question the plan, grill, validate plan, 这个方案行不行, 审查设计, find holes, stress test."
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Interview me relentlessly about every aspect of this plan until we reach shared understanding — every branch of the design tree. For each question, provide your recommended answer.

Finding facts is your job, never the user's: if the codebase or a sub-agent can answer it, look it up instead of asking. Only decisions reach the user.

Ask **exactly one question per message, always** — never a batch, never a pre-computed list, no piggyback riders (anti-patterns #3, #4). The next question is derived from the user's last answer; keep asking until the decision tree is **exhausted** — every branch walked to a settled decision. Tree-walk mechanics and the message template: [REFERENCE.md §Question Pacing](REFERENCE.md).

## Outcome Contract

- **Outcome**: Validated PRD aligned with the domain model, CONTEXT.md sharpened, significant decisions recorded as ADRs
- **Done when**: Every open decision resolved, terminology consistent with CONTEXT.md, ADRs created where the 3 conditions are met
- **Evidence**: Updated `docs/prd/PRD-NNNN-<title>.md` (status → Grilled), updated `CONTEXT.md`, created `docs/adr/<NNNN>-*.md` (where warranted)
- **Output**: Parent Issue synced (if created by `/think`), next step to `/story`

## Before You Start

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) — it locates the PRD and `CONTEXT.md` and checks upstream artifacts. If no PRD exists or it's too thin, suggest `/think` first — don't grill vapor.

## The Work

1. **Extract everything unresolved.** Read the PRD with hostile eyes: Open Questions, unvalidated Assumptions, vague terms, unexplained scope boundaries, shaky technical approach, edge cases, conflicts with `CONTEXT.md`. Skip none.
2. **Work the checklist one question at a time.** Pick the highest-value unresolved item, ask it as a single question with your recommended answer, and wait. After the answer lands, update the tree — resolved items close, new findings may open children — and pick the next question from what the answer just made askable (see [REFERENCE.md §Question Pacing](REFERENCE.md)).
3. **Resolve as you go, not in a batch at the end.** Update files inline:
   - **Terminology resolved** → update `CONTEXT.md` now (glossary only, no implementation details).
   - **Significant decision** → offer an ADR when the three conditions in [ADR-FORMAT.md §创建条件](ADR-FORMAT.md) are all met (hard to reverse, surprising without context, result of a real trade-off — full definitions live there, single source). Otherwise skip. **Decide eligibility once, the moment the decision lands**: either create the ADR inline, or record "no ADR — <which condition failed>" in the PRD. Never re-adjudicate a decision's ADR eligibility at completion — a flip between "declined inline" and "created at wrap-up" means the inline judgment was never made.
   - **Code can answer it** → grep/read the code instead of asking the user.
   - **Only running a demo can answer it** (options that reasoning and reading can't separate — which is faster, does the model hold up, what should it look like) → park the item, suggest `/have-a-try`; fold the verdict back as an ADR / PRD update and resume the checklist.
4. **Run the exhaustiveness gate** before declaring complete: Open Questions, Assumptions, terms, scope, code cross-check — all resolved.
5. **Fill the PRD `## Traceability` `Grilled by` field** so downstream skills know the plan was validated.
6. **Sync the parent Issue (if it exists).** Update its body to reflect scope changes (sharpened terms, confirmed boundaries, new ADRs). Do **not** change title or close it. If the `## Issue` field is empty, check the PRD's `Created by` field — if `/story`, skip (expected); if `/think`, warn the user that the parent Issue was not created (see REFERENCE.md for exact message).

## What Goes Where

| Situation | Action |
|---|---|
| Goal statement itself needs to change, or fundamental approach invalidated | Send back to `/think` — too big for grill |
| Only terminology sharpened, scope confirmed, approach validated with refinements | Proceed to `/story` |

For the challenge types (terminology conflict, fuzzy language, scope boundary, edge case, code cross-check), the file layout (single vs multi-context via `CONTEXT-MAP.md`), and a worked example, see [REFERENCE.md](REFERENCE.md).

## Gotchas

| What happened | Rule |
|---|---|
| Skipped an unresolved assumption | Extract every open item first, then resolve each |
| Updated CONTEXT.md in a batch at the end | Update inline, the moment each term resolves |
| Created an ADR for a trivial decision | Only when all 3 conditions met |
| ADR flipped at completion (declined inline, created at wrap-up — or vice versa) | Decide ADR eligibility once, inline, when the decision lands; record the failed condition when declining |
| CONTEXT.md gained implementation details | It is a glossary, nothing more |
| Asked the user something the code could answer | Explore the codebase instead |
| Batched questions into one message, or worked a pre-computed list | One question per message, always — the next question is derived from the last answer (anti-patterns #3, #4; see Question Pacing) |
| Forced a decision that reasoning couldn't settle | Park the item and suggest `/have-a-try` — a minimal demo settles it (selects or eliminates); fold the verdict back as an ADR |
| PRD not updated after interview | Update `docs/prd/PRD-NNNN-<title>.md` and set `Status` to `Grilled` before declaring complete |
| Declared complete without the exhaustiveness gate | Run the 5-point gate first |
| Parent Issue body stale after grill changed scope | Sync the parent Issue (if `## Issue` field present) — reflect sharpened terms, scope, ADRs; don't change title or close |

## Output

```
Grill complete.

Resolved <N> items:
- <term>: <resolution>
- <assumption>: <validated/converted>
- <decision>: <ADR created | recorded in PRD>

Updated:
- docs/prd/PRD-NNNN-<title>.md — Status → Grilled
- CONTEXT.md — <count> terms sharpened/added
- docs/adr/<NNNN>-<title>.md — created (if any)

Exhaustiveness gate: passed
Parent Issue: #<num> synced | ⚠️ missing (/think didn't create one) | skipped (no parent, direct /story path)

Next: /story to break PRD into Issues | /think if scope changed significantly
```
