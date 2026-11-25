---
name: audit-ui-slop
description: Use when the user asks to audit, review, critique, inspect, or assess an existing UI for AI-slop, generic, or template-like design patterns without making changes. Strictly read-only; do not use when the user asks to fix or implement.
---

# Audit UI Slop

## Core contract

Audit against product evidence, not taste. Establish the **Read-only boundary** first. Do not attempt edits, create or delete files, run mutating commands, or change configuration. Do not install dependencies. Do not use the network. Do not write externally or take outward action. `changed_paths must be empty`, even when a sandbox would deny an attempt.

Never self-promote to Repair; route a later change request separately.

## Evidence setup

For every audit, apply [Craft and State Gates](../../references/craft-and-state-gates.md). Use [Source Priority and Design Contract](../../references/source-priority.md) to separate intent, rules, implementation, references, and assumptions.

When a reference is supplied, apply ownership limits; it is not product authority.

When evaluating visual signals, use [Anti-Slop Rules](../../references/anti-slop-rules.md). A signal alone is never a defect. Require evidence, product conflict, exceptions considered, and smallest correction.

When reporting findings or a verdict, follow [Evidence Contract](../../references/evidence-contract.md).

Inspect source and renders when available. Trace the originating cause. Deduplicate symptoms.

## Seven dimensions

Record applicability, essentiality, evidence sufficiency, and evidence:

1. **Intent and specificity** — product, audience, task, trust.
2. **Content and hierarchy** — truthful order, decisions.
3. **Structure and composition** — information-driven layout.
4. **System coherence** — traceable visual and motion roles.
5. **Interaction and feedback** — semantics, states, recovery.
6. **Responsive accessibility** — keyboard, focus, contrast, touch, semantics, reflow, reduced motion.
7. **Evidence and completeness** — checks, gaps, risk.

**Screenshot-only:** judge only the supplied viewport and state. Do not infer DOM, keyboard, responsive, hidden-state, runtime, or source behavior. Name **Unverified scope**.

**Source-only:** source cannot prove appearance or interaction. Missing essential render evidence requires `NOT READY - verification incomplete` unless a stronger finding requires `NOT READY`.

## Finding contract

Classify each originating cause as `Blocking`, `Important`, or `Optional`, with confidence `high`, `medium`, or `low`:

```text
ID - Blocking | Important | Optional - high | medium | low
Tell:
Where:
Evidence:
Why it conflicts with this product:
Smallest correction:
Exceptions considered:
Verification status:
Required outcome:
```

`Blocking` breaks a hard gate or essential use. `Important` weakens a required outcome. `Optional` is bounded.

## Verdict algorithm

Apply in order:

1. Return `NOT READY` for any Blocking finding or unresolved Important finding tied to a required outcome.
2. Otherwise return `NOT READY - verification incomplete` when an essential applicable dimension lacks sufficient evidence.
3. Return `READY` only when every essential applicable dimension has sufficient evidence and no Blocking or required-Important finding remains.
4. Keep optional gaps in **Unverified scope**; they do not independently block readiness.

Contextual signals are not automatic findings. Record no finding when evidence establishes an exception.

## Handoff

Return:

```text
Verdict:
Evidence inspected:
Seven-dimension coverage:
Findings:
Unverified scope:
Read-only receipt: changed_paths = []
```

Report corrections only as guidance; do not implement them.
