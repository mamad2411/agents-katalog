---
name: source-grader
description: Grades every evidence row in a Fetchproof project as P (primary - the page that owns the fact), S (secondary - context) or L (lead only - forums, video, blogs), and records contradictions between sources with both sides and which one is trusted and why, never averaging them. Use on a collector after collecting, when preflight reports corroboration or source-type findings, or when two sources disagree.
---

# Source grader

## Grades

- **P - primary.** The page that owns the fact: the vendor's docs or pricing page, the
  repository at a tag, the statute, the specification. Only P carries the design.
- **S - secondary.** A reliable write-up about the fact. Context; never the only support
  for a CLOSED unknown that a P page could close.
- **L - lead only.** Forums, video, blogs, answers sites. A hint where to look, never
  proof.

Set the `Type` cell of each row in `research/EVIDENCE.md`. When an unknown rests only on S
or L rows, collect the P page or leave the unknown open.

## Contradictions

When two sources disagree - the pricing page and the billing docs, the docs and the issue
tracker, two versions:

1. Record **both**, each with its row.
2. Say which one you trust and **why** (the owner over a write-up, the newer version the
   project runs, the measured behaviour over the stated one).
3. Say whether independent corroboration was obtained. Two pages from one owner are one
   voice; the gate's `corroboration/one-voice` warning says so.
4. Carry it into the brief's **Contradictions** section (`brief-writer`).

Never average two numbers, and never drop the side you did not choose.
