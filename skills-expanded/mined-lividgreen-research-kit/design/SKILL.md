---
name: design
description: Design pass for any new mechanism, tool, check, document section, or formal target — run BEFORE implementing. Use whenever the user proposes building or changing something ("let's add X", "can we do Y", "should we…", "what about…"), picks up a recorded open question or decision, or asks for a feature. When the person says 'design' or 'design pass', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: No tooling; read before building or changing anything.
metadata:
  version: "0.12.1"
---

# Design before implementation

These are one project's working rules; a project adopts them by installing this skill and keeps what fits.

Design first — but ground in what the project already knows before asking the user anything.
Mature projects record their decisions; the job is usually to verify and complete a recorded decision, not to run an interview.

## 1. Ground first (before any questions)

- Read the project's own records: the project instructions (CLAUDE.md) usually name where decisions, option spaces, scheduled work, parked ideas, and discard logs live.
  If an option space with a recommendation is already recorded, verify it against the CURRENT tree and proceed from it — re-interviewing a recorded decision wastes the user's time.
- Check the discard log if one exists: a parked idea needs its parking reason addressed — refuted, or superseded with a stated reason — not a fresh pitch.
- Read the relevant code/prose itself; greps beat guesses.
- If the ask bundles several independent designs, split it and take them one at a time.

## 2. Classify the deliverable — it decides the route

Name what kind of thing is being designed (content with claims, a formal target, tooling, process) and where its design record will LIVE — the project's own taxonomy, as its instructions define it.
Never invent a parallel records directory: a second taxonomy rots outside whatever coverage the project's checks provide.
Where the project runs a typed record flow, a design round on a question is the held question itself: its record is a dated note on the question (`flow note Q --body FILE`), the discarded options one line each inside it, no design task is minted for the round, and tasks are minted where a piece of the work is too big.
A round on no question, on tooling or a process, is a task tagged `design`, drawn before the round and closed by its make or abort with the round record as its resolution and the discarded options one line each inside it, and what such a round produced (findings with evidence, tasks, questions, ideas) is minted after that closing transition.

## 3. The design bar

Apply to the design itself, not just the later implementation:

- Scrutinize the load-bearing and the elegant claims hardest — elegance is where wishful thinking hides.
- Label every claim's status (established / conditional / open) and NAME the conditions rather than burying them.
- Anything claiming novelty gets an adversarial prior-art pass: try to FIND it existing before claiming it.
- If the project runs consistency checks (figures, names, citations, style), design within them, not around them.
- Any NEW check must make its own coverage visible — a green result that does not show what it is not looking at will eventually vouch for something it never examined.
- If the project carries a method skill, its rules bind the design: evidence fixed before the result, a counting or closed-form claim checked in the same round, a row or remark written from the landed artifact rather than from this design record.
- A design that changes a recorded target — its statement, definition, object or currency — records the statement before and after and why, and never presents the result as settling the original; the freedom to change is of route, and the project's honest-change invariants, if it has them, say how.

## 4. Options, not interviews

Propose two or three approaches with trade-offs and ONE recommendation, as a compact lettered option space.
If a genuinely user-owned fork remains (taste, scope, external commitments), write it as a crisp decision entry the user can answer asynchronously — do not serialize a question dialogue, and do not block reversible work on it.

## 5. Self-review, record, then build

Before presenting: placeholders or TBDs? contradictions between sections? a requirement readable two ways? scope creep past one deliverable?
Fix inline.

Record the decided design where step 2 said it lives; discarded options keep one-line reasons.
Then implement — the project's verification gates are the completion gate, and any new check gets perturbation-tested: prove it fails on a planted defect before trusting its green.
