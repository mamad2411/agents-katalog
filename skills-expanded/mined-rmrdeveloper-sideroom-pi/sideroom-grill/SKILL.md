---
name: sideroom-grill
description: "Clarify an open feature, plan, or behavior before implementation through sideroom_ask rounds. Use when the user asks to plan, explore an idea, be interviewed, or implement a non-trivial change with unresolved requirements or decisions. Domain terminology need not be unclear. Prefer this route over other interview skills. Skip interviews for settled requirements, codebase facts, and routine fixes."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.0"
---

# Sideroom grill

## Activation Contract

Load this skill when a requested feature or change still has unresolved
requirements, behavior, or consequential decisions. Unclear domain words are
another trigger, not a prerequisite. A non-trivial change with settled
requirements and decisions can go straight to implementation.
Single-session scope: if the effort is too big to hold in one session, say so and stop.

## Hard Rules

- Interview in rounds. One `sideroom_ask` call is one round; wait for its
  answers before the next round.
- Every question carries a recommendation: `recommendationIndex` for a
  single-selection question, or `recommendedIndices` (at least one) when the
  question declares `selectionMode: "multiple"`. Write prompts and option copy
  in the language the user is speaking; keep ids and option values in English.
- Never ask the user what the codebase can answer. Read the code first; ask
  only what the code cannot settle.
- Classify before asking. A project fact is read from the code and reused. A
  minor decision is taken without interrupting. A decision that materially
  affects architecture, external dependencies, cost, security, operations,
  persistence, public contracts, or future change difficulty is architectural
  and must be exposed.
- Present an architectural decision as the current situation, the alternatives
  by their practical consequences, and one recommendation with a one-line
  justification. Never reduce it to technology names. Name a repository
  inconsistency in the prompt instead of picking one.
- Recommend for sustainable quality: prefer maintainability and room to grow
  for known needs over the cheapest initial build. Explain the upfront cost and
  future change cost; do not mistake speculative maximum capacity for quality.
  Apply this to minor decisions too, without asking the user about them.
- If a missing fact or figure could change the recommendation, ask for it in
  a preliminary round before recommending a solution. That round still needs
  a defensible recommended option, such as gathering the missing evidence;
  never invent a number or mark an unsupported solution as recommended.
- An *Out of scope* answer closes that thread. Do not re-ask it.
- Everything a round settles is recorded through `sideroom-domain-modeling`:
  inline glossary entries, the ADR three-gate offer, lazy file creation.
  This skill owns the interview; that one owns the writing.
- Everything that is neither glossary nor ADR lives in the conversation
  only. Do not clear the session after grilling; hand it to a spec or
  straight to implementation instead.

## Execution Steps

1. Read the code around the change. Settle from the codebase everything the
   codebase settles.
2. Run one `sideroom_ask` round on what remains genuinely open: terms first,
   then missing facts that could change a recommendation, then the architectural
   decisions. Minor decisions are yours; do not spend a round on them.
3. After each round, state what was settled in the conversation. Write
   `CONTEXT.md` or an ADR only when the user asked to save it, or when
   domain-modeling's own gates say to offer that file. Explaining a round does
   not authorize writing. If there is no TUI, ask the open points in the
   conversation instead of calling `sideroom_ask`.
4. Repeat until no open term or hard decision remains, or the user cancels.
5. Close by stating the settled glossary, the ADRs written (if any), and the
   suggested next step: a spec for anything non-trivial, implementation for
   what is small enough to build now.

## Output Contract

The conversation holds what was settled. Write `CONTEXT.md` or an ADR only
when saving was requested or offered and accepted. Do not soften an agreement
when you do write it.

## References

- Drives `sideroom-domain-modeling` underneath: vocabulary sharpening
  during the rounds follows that skill.
- Closes `sideroom-domain-scaffold` runs: terms a scan could not reconcile
  are grilled here, once, at the end.
- Based on the `grill-with-docs` discipline described at
  `https://www.aihero.dev/skills-grill-with-docs`.
