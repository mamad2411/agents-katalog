---
name: swarm-review
description: Milestone review sweep — a strong model audits everything since the last sweep against the spec: requirement fulfillment, standards, simplification, risk. Use when a milestone's tickets are done, before opening the next milestone, or when asked to review/audit/validate completed work.
---

# swarm-review — the milestone gate

Reviews against the **spec**, not just the code — that is the difference between this and
a linter. Expect a top-tier model; warn if the session runs less. Milestone cadence only
(token economy): not per-commit.

**Scope:** the milestone's diff (git log since last sweep), its tickets, and its FR specs.

## The four lenses, in order

1. **Fulfillment** (the one that matters most): every Must-FR of the milestone,
   individually — no sampling. Are the acceptance criteria actually met? Do the tests
   *assert the criteria* (not just execute the code)? Is the FR → ticket → commit → test
   chain intact?
2. **Standards:** naming, error handling (exceptions handled, not swallowed), comment
   discipline (light, constraint-stating), test quality (behavior asserted, not
   implementation), commit hygiene — audited against swarm-implement's
   `references/clean-code.md` where available, **including its dogma traps**: fragment soup,
   one-implementation abstractions, pattern theater, and SRP shrapnel are findings, not
   compliance. **End-user text** shipped in the
   milestone (UI strings, README, release notes, marketing) is audited against the project's
   `voice.md` and the audience firewall — load swarm-write for the criteria.
3. **Simplification:** duplicated logic to merge, needless abstraction to delete, blocks
   that could be simpler or generalized. If a fix is obvious and small, still ticket it —
   see the rule below.
4. **Risk:** input validation gaps, security smells, and a devil's-advocate pass — "what
   assumption, if wrong, hurts most?"

## Findings

One per issue, compact (machine lane): severity (`blocker/major/minor`), FR link,
`file:line` evidence, concrete suggested fix. Write the report to
`30 Plans/<P>/reviews/M<N>-sweep.md` (human-lane summary + machine-lane findings), then
**one ticket per accepted finding** — findings that stay chat messages die in scrollback.

**Never auto-fix.** Reporting and fixing in the same pass corrupts the review; fixes are
swarm-implement's job via the tickets.

## Closing the gate

- **Gated mode:** present the report; the user decides what's waived; milestone closes on
  their word.
- **Auto mode:** the sweep IS the gate — `blocker`/fulfillment findings must be fixed and
  re-swept before the next milestone opens; the user reads the report in the vault at
  their leisure. Minor findings may carry forward as open tickets.

Update flow-state either way (J1).

---
*Influences: Pocock's code-review (two-axis); Jeffallan's code-reviewer &
security-reviewer & the-fool; superpowers verification-before-completion; euxx
code-simplifier — see CREDITS.md.*
