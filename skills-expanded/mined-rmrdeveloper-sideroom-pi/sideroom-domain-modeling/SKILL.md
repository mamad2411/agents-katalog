---
name: sideroom-domain-modeling
description: "Resolve ambiguous business terms, entity names, statuses, or relationships while designing or changing domain code. Use when one term has multiple meanings, code and glossary disagree, or a resolved term belongs in CONTEXT.md; also handles qualifying ADRs. A full interview is not required. Skip mechanical symbol renames and glossary lookups; use sideroom-domain-scaffold for a repository-wide glossary."
license: MIT
metadata:
  author: RMRdeveloper
  version: "1.0"
---

# Sideroom domain modeling

## Activation Contract

Load this skill when the _words_ are the problem: two people mean different
things by one term, one term is doing several jobs, or a statement about the
domain needs to survive longer than the conversation. This is the active
discipline — changing the model — not the passive habit of reading
`CONTEXT.md` to borrow a word. That read needs no skill; it is one line.

It runs underneath `sideroom-grill` through a grilling session, and it also
runs on its own when you want the discipline without the interview.

## Hard Rules

- Interrupt. When a term conflicts with the glossary, stop and ask which of
  the two things is meant instead of picking one and moving on. When a vague
  word appears where a precise one exists, force the precise word.
- Stress-test relationships with a concrete scenario until the boundaries
  are exact.
- Cross-check statements against the code. When the code and the sentence
  disagree, quote the code back and settle which one is right out loud,
  before changing either.
- A resolved term lands in `CONTEXT.md` the moment it resolves, inline, in
  the middle of the conversation. One or two sentences saying what the thing
  **is**, plus rejected synonyms under `_Avoid_`.
- `CONTEXT.md` is a glossary and nothing else. Never persist implementation
  details, spec prose, scratch notes, or general programming concepts there.
  Refuse the write and say why.
- An ADR under `docs/adr/` is offered, never assumed, and only when all
  three gates pass at once: hard to reverse, surprising without context, and
  the result of a real trade-off. When refusing, say which test failed.
- Create files lazily. Nothing exists until the first term or decision
  crystallises. In a repo with a `CONTEXT-MAP.md` at the root, terms go into
  the per-context `CONTEXT.md` the map points at instead.
- Keep the glossary lean. It gets shorter as often as it gets longer: split
  an overloaded term, drop a dead one, and when the file has absorbed detail
  that was never glossary material, offer to condense it.

## Decision Gates

| Situation | Move |
| --- | --- |
| Two meanings for one term | Pick the canonical term, list the other under `_Avoid_` |
| One term doing several jobs | Split it (e.g. `Account` into `Customer` and `User`) |
| A vague term became canonical | Write it to `CONTEXT.md` now |
| A hard-to-reverse choice clearing all three ADR gates | Offer an ADR under `docs/adr/` |
| The module's shape is the problem, not its words | This skill does not apply; that is module design |
| The whole plan needs interrogating before building | `sideroom-grill`, which drives this skill underneath |
| A term only needs looking up, not changing | Read `CONTEXT.md`. It is a file |

## Execution Steps

1. Read `CONTEXT.md` (and the ADRs, if any) before touching the model.
2. As terms settle, write each one inline with its `_Avoid_` list.
3. As hard choices surface, offer an ADR or refuse one with the failed
   test named.
4. Before finishing, re-read the touched entries: each defines what a thing
   is, in one or two sentences, with no implementation detail.

## Output Contract

The repo holds the shared vocabulary and the hard decisions, each entry
short enough to re-read. The glossary never becomes a running spec.

## References

- Driven by `sideroom-grill` during grilling sessions.
- Entry rules reused by `sideroom-domain-scaffold` for code-first
  scaffolding without interviews.
- Based on the `domain-modeling` discipline described at
  `https://www.aihero.dev/skills-domain-modeling`.
