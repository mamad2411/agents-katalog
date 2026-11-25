---
name: reviewing-overengineering
description: >-
  Fires before a plan is accepted or a diff merged when its size, layer count, or abstraction
  budget is in question — and at the moment "simplify", "cut this down", a line-count target,
  or deadline pressure enters a review, because those are the moments a trust-boundary
  control gets deleted as bloat. Also fires when a remediation claims simplification: a
  remediated candidate is re-reviewed, never waved through. Produces an independent
  complexity, deletion, or remediation audit with a safety-preservation rebuttal. Not for a
  general correctness review or continuous style advice, and not for enumerating what
  threatens a trust boundary (sdlc-threat-model).
---

# Reviewing overengineering

Review complexity independently without confusing “less code” with “fewer guarantees.” The target is
the smallest implementation that preserves the candidate's required properties.

## Bind the candidate

Name an immutable snapshot: commit, tree/diff digest, or frozen plan bytes. Record the producer and,
when available, use a different model or independent perspective from the producer. State the
required behavior and non-negotiable boundaries before proposing deletions. A percentage or line
quota is pressure evidence, not an acceptance criterion.

## Run both passes

1. **Deletion pressure:** identify duplicate logic/prose, unused fields, speculative abstractions,
   unnecessary extension points, and presentation machinery that can be removed now.
2. **Safety-preservation rebuttal:** challenge every proposed deletion. Reject it if it weakens
   identity, consent, privacy, budgets, bounded execution, artifact integrity, or authority
   boundaries. Passing tests alone do not prove these properties survived.

Classify every proposal as exactly one of:

- **essential safety complexity** — keep, with the property it preserves;
- **accidental complexity removable now** — delete or consolidate, with the existing check that
  preserves behavior;
- **speculative functionality to defer** — remove scaffold and name the concrete trigger for adding
  it later.

Do not satisfy an arbitrary deletion target by reclassifying a safety property as presentation.
Prefer deletion over a new abstraction; a general framework is not remediation for one unsafe
feature.

## Report and loop

Emit a short **keep / delete / defer / remediate** report bound to the snapshot. Remediation creates
a new candidate and requires re-review; never pre-approve unseen changes or let the producer's
passing suite substitute for the independent pass. Stop when all accepted deletions have a
safety-preservation rebuttal and every retained mechanism names the property it protects.

Ponytail may complement this skill but is never a dependency.

## Admission rationale

This skill clears all four gates: the description distinguishes complexity audit from correctness
review; recurring use justifies its small selection cost; concrete overengineering reviews exist
now; and it is a bounded task, not an always-on style rule. It clears all five promotion signals:
**Recurs; needs sequencing; has repeated failure modes; has stable input/output; benefits from
explicit handoff**.
