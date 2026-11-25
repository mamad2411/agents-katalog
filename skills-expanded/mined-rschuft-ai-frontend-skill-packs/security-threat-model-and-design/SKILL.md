---
name: security-threat-model-and-design
description: "Assess and remediate threat models, abuse cases, architecture and secure design reviews in frontend and associated web services. Use for threat model, trust boundary, abuse case, design review, security architecture."
---

# Threat modeling and security design gaps

## Scope

Use when the task concerns **threat models, abuse cases, architecture and secure design reviews**. Common triggers include threat model, trust boundary, abuse case, design review, security architecture. Do not classify unrelated symptoms as this category or expand the authorized scope. A client-side implementation may not reveal server-side enforcement.

ASVS 5.0.0 chapters: **V2, V15**. For exact requirement wording and levels consult `../security-diagnose/references/asvs/5.0.0/index.json` and the version-pinned official ASVS source. Do not treat the index as the full standard. The local reference is `references/playbook.md`.

## Procedure

1. Establish the user action, attacker/actor, sensitive asset, trust boundary, affected runtime, and actual observed evidence.
2. Read `references/playbook.md` and the relevant ASVS chapter entries. Resolve baseline using `../security-diagnose/references/standard-selection.md` (explicit task > project policy > planning fallback).
3. Differentiate the underlying cause from superficial symptoms; select a specific applicable requirement only after checking the authoritative source text.
4. Implement or recommend the smallest verified control with the project’s existing security architecture. Prefer server-side enforcement when the failure crosses the browser trust boundary.
5. Test normal and denied paths with synthetic or approved fixtures, documenting exact methods and evidence. Record residual unknowns; route broad assessments to `security-review`, implementation to `security-build` and retesting to `security-validate`.

## Failure discipline

- A threat hypothesis is not a confirmed vulnerability.
- Do not infer server enforcement from frontend code alone.
- A single checklist cannot substitute for architecture-specific threat modeling.

No active probing of live systems, aggressive scanning, credential handling or cross-tenant requests without explicit authorization. Never report security certification from this skill alone.
