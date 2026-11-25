---
name: instructions-authoring
description: Use when creating or editing .instructions.md files, including policy-domain scoping, applyTo correction, and deterministic rule tightening.
---

# Instructions Authoring

## Specialization

Author and maintain `.instructions.md` artifacts only.

This skill is strictly for always-on policy assets. It does not author `.agent.md` files.

## Prerequisites

- REQUIRED: Keep execution self-contained within this skill. Do not delegate execution to sibling skills.
- REQUIRED BACKGROUND: Understand that instructions are loaded automatically by `applyTo` scope and must contain policy rules only.

## Frontmatter Rules

All fields are required:

```yaml
---
name: <policy-domain>
description: '<One sentence describing the enforced policy area.>'
applyTo: '<glob pattern from workspace root>'
---
```

- `name`: lowercase kebab-case matching the policy domain.
- `description`: concise policy-scope sentence.
- `applyTo`: no broader than required by policy scope.

## Content Rules

- Use mandate language: `Use`, `Do not`, `Always`.
- Keep one policy domain per file.
- Do not embed multi-step workflows or routing logic.
- Keep wording concise and deterministic.

## Trigger Conditions

Invoke this skill when any of the following is true:

- A `.instructions.md` file must be created or edited.
- `applyTo` or policy-domain scope needs correction.
- Instruction wording needs deterministic tightening or brevity cleanup.

## Inputs

- User request context and target `.instructions.md` scope.
- Growth-governance baseline: scope-first changes, reuse-before-create, concise deltas, and explicit reviewability.

## Required Outputs

- A concrete `.instructions.md` result aligned with workspace standards and requested policy boundaries.

## Workflow

1. Confirm the target artifact is an instruction file.
2. Run a pre-authoring growth gate and capture any exception decision: avoid duplicate policy blocks, keep scope singular, and make outputs auditable.
3. Apply frontmatter and scope requirements.
4. Ensure content is policy-only and testable.
5. Remove duplication and narrative padding.
6. Route post-change quality checks to this skill.

## Hard Constraint

- Never create root-level folders in any workspace.
- Never create top-level reference folders; keep references under the owning asset path (for example `.github/skills/<skill>/references/`).
- Instruction files MUST NOT embed skill names or cross-skill delegation in their policy content. Policy scope is rules only; no execution routing to skills.
- Prefer canonical shared references for growth-policy guidance rather than embedding duplicate policy blocks in multiple files.

## Done Criteria

Authoring is complete when:

- The target `.instructions.md` file exists at the correct path.
- Frontmatter is valid and complete.
- `applyTo` scope matches policy intent.
- Content is policy-only and passes deterministic checks.
- this skill routing is included for post-change review.
