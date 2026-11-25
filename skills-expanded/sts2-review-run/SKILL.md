---
name: sts2-review-run
description: Review a Slay the Spire 2 fight or run, extract reusable lessons, and update the durable lesson ledger and current playbook.
---

# STS2 review run workflow

Use this skill when the task is to **learn from what just happened**.

## What this skill owns

- compact checkpoint reviews after elites, bosses, near-lethal fights, and build-defining pivots
- full post-run or post-swing reviews
- deciding whether a heuristic is candidate, validated, situational, or retired
- updating persistent memory files with the new evidence
- maintaining a detailed review archive at [../../sts2-memory/reviews/README.md](../../sts2-memory/reviews/README.md)
- reconciling the active run timeline with the final run outcome

## Review loop

1. Start from the actual run context
   - summarize the state, fight, reward, or route pivot that triggered review
   - identify the few decisions that materially changed the outcome

2. Distinguish tactical notes from durable lessons
   - the full, detailed review belongs in the archive under [../../sts2-memory/reviews/](../../sts2-memory/reviews/)
   - tactical notes belong in the current playbook at [../../sts2-memory/current-playbook.md](../../sts2-memory/current-playbook.md)
   - durable lessons belong in the ledger at [../../sts2-memory/lesson-ledger.md](../../sts2-memory/lesson-ledger.md)

3. Use the right review depth
   - for a compact checkpoint, produce 2 to 4 sentences covering decision quality, risk trade, and which lesson was validated or challenged
   - for a major swing, death, or win, use [review-template.md](./review-template.md)
   - every major review must include a deck autopsy that names the actual structural failure, not just the surface symptom
   - because STS2 is highly random, compare the review against 1 to 3 relevant prior runs or explicitly say that the sample is still too small
   - for any review that used retries or branch testing, explicitly record the baseline line, the best tested branch, the concrete gain from that branch, and why that branch was still enough or still not enough

4. Update lesson status explicitly
   - `candidate`: promising, lightly tested
   - `validated`: repeatedly useful and safe to trust
   - `situational`: only right with clear qualifiers
   - `retired`: no longer trusted

5. Update persistent memory
    - keep the full detail in the archive, not in battle memory
    - write near-term tactical adjustments into [../../sts2-memory/current-playbook.md](../../sts2-memory/current-playbook.md)
    - keep the recent-run index and active timeline in [../../sts2-memory/run-history.md](../../sts2-memory/run-history.md) and [../../sts2-memory/runs/](../../sts2-memory/runs/)
    - write durable heuristics into [../../sts2-memory/lesson-ledger.md](../../sts2-memory/lesson-ledger.md)
    - classify durable lessons clearly enough that future recall can separate `macro`, `deckbuilding`, `combat`, and `tooling` guidance
    - keep scope boundaries explicit when a rule is class-specific, matchup-specific, or tooling-specific
    - convert at least one structural finding from the deck autopsy into either a next-run checklist item or a durable lesson
    - compress the review into only a few battle-relevant reminders; do not dump the whole postmortem into the live loop
    - if the run just ended, mark the timeline entry as ended and make sure the final floor, result, and end timestamp are visible from the recent-run index
    - never leave the review as prose only

## Constraints

- Do not silently keep a disproven heuristic
- Separate general rules from class-specific or card-specific ones
- Do not stop at labels like "damage output was low" or "block was weak"; name the structural reason, such as missing second kill package, diluted premium attacks, weak draw support, or block cards that only solved hallway pressure
- Do not overlearn from one random run: a card that appears only once in five runs, or fails to appear in four straight runs, is usually a scope or sample-size issue rather than proof by itself
- Keep only lessons that would help a future run
