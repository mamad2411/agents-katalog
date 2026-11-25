---
name: pen-deslop
description: "Audit code, diffs, plans, and implementation proposals for AI-generated slop patterns in the Pen codebase: generic over-abstraction, fake robustness, guard-flag accretion, pipeline bypasses, sentinel leakage, noisy helpers, vague naming, decorative comments, and code that looks plausible but does not fit the local system. Use when the user asks to deslop, remove AI slop, de-AI a change, review for generated-code artifacts, or harden a change against maintainability smells introduced by coding agents."
---

# Pen Deslop

Find generated-code artifacts that make the codebase feel less intentional. The target is not style policing; the target is code that looks locally plausible but is generic, overbuilt, under-contextualized, or expensive to maintain.

Keep the audit sharp. Prefer a few high-confidence slop findings with concrete remedies over a broad checklist.

## Process

### 1. Learn the neighborhood

Read the relevant project instructions first: root `AGENTS.md`, `.cursor/rules/*.mdc`, the matching `spec/` documents, and nearby files.

Inspect caller, callee, sibling implementations, existing tests, and the owning package before judging a pattern. A thing is slop only when it fails the local system, not merely because it resembles a general smell. In Pen the local system is unusually explicit: the apply pipeline, extension seams, offset domains, and selection rules are specified with rule IDs in `spec/rules/` — cite them.

### 2. Load pattern rules lazily

Read [PATTERNS.md](references/PATTERNS.md) when you need the current slop taxonomy or want to add a new short rule. Keep rules terse:

```text
## Rule name
Signal: what to look for.
Fix: how to remove it.
```

Do not expand SKILL.md with every rule. The main file stays procedural; the rule catalog grows in the reference.

### 3. Use parallel audits for non-trivial scope

For a meaningful diff, broad module, or ambiguous signal, use [PARALLEL-AUDIT.md](references/PARALLEL-AUDIT.md). Spawn focused sub-agents in parallel only when a sub-agent tool is available and only after you have a concrete artifact to inspect.

Keep each sub-agent brief independent and evidence-based. Ask for findings, file/line references, and remedies; do not leak your suspected answer.

### 4. Classify slop

For each suspected issue, answer:

- **Local mismatch** — what nearby pattern, spec rule, or system contract does this violate?
- **Generated-code signal** — why does this look like AI slop rather than a valid local choice?
- **Maintenance cost** — what future reader, caller, test, or extension now pays for it?
- **Fix shape** — delete, inline, rename, move, tighten type, reuse local helper, or reshape the module.

If you cannot answer all four, do not present it as a finding. Mention it only as an open question if it matters.

### 5. Report or fix

When reviewing, lead with findings ordered by severity:

```text
[P1/P2/P3] [ID] Title
Files: path:line
Signal: generated-code smell and local mismatch.
Fix: concrete change.
```

When editing, make the smallest change that removes the slop. Favor deletion and alignment with local patterns over new abstractions. Run focused verification proportional to the touched surface.

## Add Rules

When the user identifies a new slop pattern, add or update exactly one short entry in [PATTERNS.md](references/PATTERNS.md). Preserve the `Signal` / `Fix` shape. Avoid examples unless they are compact and reusable.
