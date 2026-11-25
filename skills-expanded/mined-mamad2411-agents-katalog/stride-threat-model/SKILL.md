---
name: stride-threat-model
description: Model a system with STRIDE; writes docs/threat-models/<slug>.md with frontmatter validated by the ThreatModel artifact schema.
---

# stride-threat-model

> Frame a threat model around the six STRIDE categories, decompose the scope by data flow, list threats with mitigations.

## When to use

- A workflow invokes `polymath-security:stride-threat-model`.
- A new feature handles authentication, payments, PII, or any trust boundary.
- The user says "let's threat-model this" or "STRIDE this".

## Inputs

- System name + scope (required).
- PRD path if available (grounds the data classification).
- Existing threat models or ADRs in the area.

## Procedure

1. Read [`Threat-model.md`](../../templates/Threat-model.md).
2. Compute slug from system name (kebab-case).
3. **Summary-first checkpoint.** Show a one-screen skeleton — the
   scope boundary, the trust boundaries found, the 2–3 highest-risk
   STRIDE candidates — and confirm scope before the full model.
4. Draft `docs/threat-models/<slug>.md`:
   - **Scope** — explicit boundary; what is and isn't covered.
   - **Data flow** — mermaid or ASCII diagram showing every trust boundary the system spans (user → API → DB, internal → external, etc).
   - **Assumptions** — what the platform already protects.
   - **Threats by STRIDE** — one table per category. For each: threat description, mitigation, owner.
5. Frontmatter must satisfy the `ThreatModel` artifact schema (`registry/schemas/artifacts/Threat-model.schema.json`): `artifact: ThreatModel`, `system`, `scope`, `owner`, `created`, `stride_categories` (subset of the six STRIDE values).

## Quality bar

- Every threat has a named owner (a team, not a person) and a mitigation that is observable in the system.
- At least one threat in each of the six STRIDE categories. If a category genuinely doesn't apply (e.g., no auth on a publicly read-only endpoint), say so explicitly under that section instead of leaving it blank.
- No mitigation that boils down to "be careful" or "review carefully".

## Output

- File: `docs/threat-models/<slug>.md`.
- Summary listing total threat count by category.

## Verifying in a workflow

If you author a workflow that invokes this skill, add a `mustPass` check:

```yaml
mustPass:
  - id: threat-model-valid
    type: artifactValid
    path: docs/threat-models/${workflow.slug}.md
    artifact: ThreatModel
```
