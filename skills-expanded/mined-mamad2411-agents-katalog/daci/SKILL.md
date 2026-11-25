---
name: daci
description: Run a DACI decision (Driver, Approver, Contributors, Informed) for a non-trivial decision; assigns one Approver, names the deadline.
---

# daci

> One Approver, one Driver, named Contributors, named Informed. Forces clarity about who's actually deciding.

## When to use

- A decision involves more than one team or function.
- Past decisions in this area got re-litigated because nobody could point to "who decided".
- A workflow needs a structured decision before implementation.

## Inputs

- The decision question (required).
- Candidate Driver + Approver names (the script will challenge them if either is missing).
- Deadline (required; "no deadline" is not acceptable for a real DACI).

## Procedure

1. Read [`DACI-decision.md`](../../templates/DACI-decision.md).
2. Compute the slug.
3. Write `docs/decisions/<slug>.md`:
   - **Driver** — one person. Not the Approver. Drives the process; doesn't get to decide.
   - **Approver** — one person (or one role). If you can't name a single Approver, the situation isn't decision-ready yet — escalate framing.
   - **Contributors** — people whose input is required. They don't approve; they prevent ignorance.
   - **Informed** — need-to-know after the fact.
   - **Context, Options, Recommendation** — Driver writes the draft.
   - **Decision, Rationale** — Approver fills in. Don't pre-fill these.
4. Set a real deadline. "By end of quarter" is a deadline; "soon" is not.

## Quality bar

- Exactly one Approver. Approver ≠ Driver.
- Contributors: 1–5. Beyond 5, the decision is probably actually a steering committee, not a DACI.
- Recommendation paragraph names the trade-off you'd accept (not "all upside").
- Decision section starts empty. The Driver MAY NOT pre-fill it.

## Output

- File: `docs/decisions/<slug>.md`.
- One-line summary listing Approver + deadline.

## Anti-patterns to avoid

- Approver = Driver (i.e., the same person runs the process and decides). Defeats the whole framework.
- "Approvers: alice + bob". Pick one.
- No deadline. Open DACI tickets live forever.
- Listing the whole team under Contributors. Pick the inputs that genuinely matter.
