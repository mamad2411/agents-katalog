# Standard Vulnerability Exposure Analysis Prompts

## Prompt: Analyze A CVE/Advisory

```
Analyze [CVE-ID or advisory] for this repository using BC Gov standardized process.

Mandatory steps:
1. Read docs/security/app-context.md, docs/security/architecture.md, docs/security/threat-model.md first.
2. Determine real exposure from repository context. Do not assume internet-facing.
3. Evaluate exploitability, exposure, and business criticality using 1-5 scoring.
4. Apply formula:
   Risk = (Exploitability * 0.4) + (Exposure * 0.3) + (Criticality * 0.3)
5. Map to OCIO class and patch timeline.
6. Provide patch steps when possible.

Return exactly these sections:
1. Application Overview
2. Vulnerability Summary
3. Scoring (Exploitability / Exposure / Criticality)
4. Risk Calculation
5. OCIO Classification (with patch timeline)
6. Key Interpretation
7. Required Actions
8. Justification Statement
```

## Prompt: Validate Missing Context

```
Before scoring [CVE-ID], validate whether docs/security/app-context.md, docs/security/architecture.md,
and docs/security/threat-model.md contain enough evidence for exposure and business criticality.

If any fields are missing:
- list missing data explicitly
- state temporary assumptions
- provide best-effort provisional scoring
- mark confidence as low/medium/high
```

## Prompt: Patch Plan

```
Create a patch plan for [CVE-ID] using repository context and the standardized risk model.

Include:
- impacted dependency and current version
- fixed version options
- compatibility notes (Node.js 24, NestJS 11.x)
- test plan: npm test, npm run test:e2e, npm run lint, npm run build
- rollback plan
- required timeline based on OCIO classification
```

## Prompt: Audit-Ready Summary

```
Produce a concise, one-page, audit-ready vulnerability summary for [CVE-ID].

Rules:
- use repository docs as primary source
- do not over-assume internet exposure
- separate external exposure and internal lateral movement exposure
- include whether risk acceptance is required if timeline is unlikely
```

## Worked Example: CVE-2026-5079

```
Use CVE-2026-5079 as the reference example for repeatable analysis in this repository.

Classification:
- This is a transitive runtime dependency case.

Repository-specific expectations:
- Runtime exposure is internal-only and VPN-restricted per docs/security/app-context.md.
- Do not describe this service as internet-facing unless those docs change.
- package.json declares @nestjs/platform-express directly, while package-lock.json shows multer is inherited transitively from that package.
- The patch decision must explicitly distinguish:
   1. direct dependency updates to @nestjs/platform-express
   2. transitive dependency resolution for multer
   3. the option of an npm override if upstream NestJS has not yet adopted a fixed multer version

Expected analysis shape:
- Exploitability should remain relatively high because one crafted multipart request can trigger the DoS.
- Exposure should be scored as internal/VPN-only, not public internet.
- Criticality should remain moderate-to-low unless new data sensitivity or production criticality evidence is introduced.
- Waiting for upstream can be discussed only as a time-boxed risk decision, not as remediation by itself.

Expected patch discussion:
- Check whether the latest compatible @nestjs/platform-express version still declares vulnerable multer.
- If yes, explain why a direct dependency bump alone is insufficient.
- If recommending an override, state the supportability tradeoff and the removal condition once upstream is fixed.
```

## Worked Example Pattern: Direct Runtime Dependency CVE

```
Use this pattern when the vulnerable package is declared directly in package.json and is used at runtime.

Classification:
- This is a direct runtime dependency case.

Expected analysis shape:
- Confirm the package appears directly in package.json.
- Determine whether the vulnerable feature is actually exercised by this repository.
- Score exposure from repository context, not from generic CVSS assumptions.
- Treat patching as simpler than the transitive case unless the fix requires a breaking major upgrade.

Expected patch discussion:
- Prefer updating the direct dependency to the minimum fixed compatible version.
- Explain whether the fix can stay within the current semver line or requires a larger upgrade.
- Call out any code-level regression risks caused by API changes.
- Validate with npm test, npm run test:e2e, npm run lint, and npm run build.
```

## Worked Example Pattern: Dev-Tooling or Non-Runtime Dependency CVE

```
Use this pattern when the vulnerable package is only used in development, testing, build tooling, or repository automation.

Classification:
- This is a dev-tooling or non-runtime dependency case.

Expected analysis shape:
- Prove the dependency is dev-only from package.json or the dependency tree.
- Do not inflate exposure by describing the production runtime as directly vulnerable if the package is not shipped there.
- Evaluate whether the vulnerable component still affects CI, local development, code generation, or artifact integrity.
- Score criticality and exposure separately for developer/CI environments versus deployed service runtime.

Expected patch discussion:
- Prefer a routine dependency update when no production runtime path exists.
- Escalate only if the tooling touches privileged CI/CD, release artifacts, secrets, or code execution in trusted pipelines.
- State clearly why the classification differs from a runtime package CVE.
```

## Repeatability Triage

```
Before writing the final analysis, classify the CVE into one of these buckets:
1. Direct runtime dependency
2. Transitive runtime dependency
3. Dev-tooling or non-runtime dependency
4. Infrastructure or environment component not proven from this repository

Then apply these rules:
- If bucket 1: focus on direct package upgrade path and runtime feature usage.
- If bucket 2: prove the dependency chain and distinguish upstream fix, override, and wait options.
- If bucket 3: avoid overstating runtime exposure and assess CI/developer impact separately.
- If bucket 4: state that repository evidence is insufficient for a package-level patch plan and identify the missing owner or platform evidence.
```

## Scoring Guidance

- Exploitability (1-5): ease of exploit, active exploitation, required preconditions
- Exposure (1-5): reachability from internet and/or internal networks based on actual architecture
- Criticality (1-5): business impact, service criticality, data sensitivity

## OCIO Mapping Guidance

- CRITICAL -> 72 hours
- HIGH -> 14 days
- MEDIUM -> 30 to 90 days
- LOW -> based on routine patch cycle with strong controls

If deadline cannot be met, include a risk acceptance recommendation.
