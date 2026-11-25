---
name: threat-modeling
description: STRIDE threat modeling per feature - actors, attacks, mitigations, residual risk. MANDATORY TRIGGERS - "threat model", "STRIDE", "risk", "attack", "abuse case", "security review", "what could go wrong".
allowed-tools: Read, Grep, Glob, Edit
---

# Skill: threat-modeling

## When to use

New feature touches auth, network, storage, deep links, file
pickers, WebViews, or third-party SDKs. Invoked by
`/security-review`.

## Inputs

- feature slug
- spec.md and the diff

## Steps

1. List **assets** the feature handles: tokens, PII, content,
   money equivalents (post karma / influence), session state.
2. List **actors**: anonymous user, authenticated user, content
   moderator, malicious peer, network attacker, compromised device.
3. For each (actor, asset), walk **STRIDE**:
   - **S**poofing — can identity be faked?
   - **T**ampering — can data be modified in transit / at rest?
   - **R**epudiation — can the actor deny an action?
   - **I**nformation disclosure — can secrets / PII leak?
   - **D**oS — can the actor exhaust a resource?
   - **E**levation of privilege — can the actor escalate role?
4. For each applicable threat, record:
   - existing mitigation
   - residual risk: L / M / H
   - follow-up ticket if M or H

## Output template

```
# Threat model: <feature>

| # | actor | asset | category | attack | mitigation | residual | follow-up |
|---|-------|-------|----------|--------|------------|----------|-----------|
| 1 | malicious peer | post content | T | edit replayed | server-side auth + ETag | L | - |
```

Append the "Security note" (<= 120 words) to the PR body.

## See also

- `secure-storage`, `docs/ai-sdlc/security-checklist.md`
