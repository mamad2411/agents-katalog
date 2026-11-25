---
name: prune
description: >
  Review diffs for over-engineering only. One line per finding: location, what
  to cut, what replaces it. Hard gate before /review in aiops delivery. Use
  when the user says prune, simplify review, what can we delete, or
  over-engineered.
---

# Prune

Hunt unnecessary complexity in the diff. One line per finding. Goal: shorter diff.

## Format

`L<line>: <tag> <what>. <replacement>.`

Tags: `delete`, `stdlib`, `native`, `yagni`, `shrink`

## Scoring

End with `net: -<N> lines possible.` or `Lean already. Ship.`

## Boundaries

Complexity only — correctness and security belong in `/review`. Pre-delivery constraint: `/lean`. List cuts; do not apply unless asked.
