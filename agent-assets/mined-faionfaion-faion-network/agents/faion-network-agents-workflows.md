---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
applies_to: skills/faion/workflows/
---

# Workflows + Workflow Playbooks Conventions

Authoritative spec for entities under `skills/faion/workflows/<slug>/`. For the sibling **tier-playbook** entity at `skills/faion/playbooks/<tier>/<group>/<slug>/`, see `../playbooks/playbook-spec.md`.

## What lives here

| File | Read when |
|------|-----------|
| `workflow-spec.md` | Authoring a new workflow (orchestration pattern) or auditing an existing one. Reference + explanation. |
| `playbook-spec.md` | Authoring a new per-surface playbook for an existing workflow. How-to. |
| `../playbooks/playbook-spec.md` | Authoring a tier playbook (per-task, per-tier how-to under `skills/faion/playbooks/`). Different entity, same word. |

## Reading order

1. `workflow-spec.md` § 1–3 — what a workflow is + folder shape (one screen).
2. `playbook-spec.md` § 1–5 — what a playbook is + required sections (one screen).
3. Drill into specific phase / front-matter / versioning sections only when authoring.

## Boundary

- Workflow owns phase order, output contract grammar, tool allowlist budget, idempotency class, failure-routing classes.
- Playbook adapts per-surface choices (verify command, test runner, deploy mechanism, file-grouping heuristics, deploy gates) — never phase order.
- Failure routing lives only inside `<phase>` XML. Top-level routing tables are forbidden.

## Knowledge link

- Playbooks MUST cite ≥1 methodology from `skills/faion/knowledge/` in a required `## Methodologies` table (surface-specific HOW).
- Workflows MAY cite methodologies for cross-cutting concerns (semantic-xml-content for prompts, sdd-conventions for lifecycle).
- Both kinds of citation are validated: path must resolve; tier of citation ≤ tier of citer.

## Live skeletons

- `skills/faion/workflows/sdd-batch-orchestrator/templates/playbook-skeleton.md` — playbook template.
- `skills/faion/workflows/sdd-batch-orchestrator/templates/prompt-skeleton.md` — phase-prompt template.
- `skills/faion/workflows/sdd-batch-orchestrator/` — first concrete workflow, reference impl.

## Validation

- XML files: `python3 scripts/validate-methodology-xml.py <path>`.
- Spec compliance: 8-item checklist at end of each spec doc.

## Related

- `docs/skill-authoring.md` — methodology folder shape, token budgets.
- `skills/faion/workflows/AGENTS.md` — workflow index + adding a new workflow.
- `rules/skill-authoring.md` — mandatory pre-edit reading.
