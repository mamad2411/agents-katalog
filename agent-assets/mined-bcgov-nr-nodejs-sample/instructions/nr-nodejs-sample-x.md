# NestJS Sample Application - Vulnerability Analysis Instructions

## Objective

Use a standardized BC Government vulnerability exposure analysis process aligned to OCIO Patch Guidelines.

## Source Of Truth

Always read repository security context first. These files are authoritative:

1. `docs/security/app-context.md`
2. `docs/security/architecture.md`
3. `docs/security/threat-model.md`

Do not assume internet-facing exposure unless `docs/security/app-context.md` explicitly states it.

## Mandatory Analysis Rules

1. Repository documentation is primary evidence.
2. Distinguish external exposure from internal/lateral movement risk.
3. Evaluate technical severity and business context together.
4. If context is missing, state assumptions clearly.

## Risk Model

Score each factor from 1 to 5:

- Exploitability (likelihood)
- Exposure (reachability based on architecture)
- Criticality (business impact)

Risk formula:

`Risk = (Exploitability * 0.4) + (Exposure * 0.3) + (Criticality * 0.3)`

## OCIO-Aligned Classification

- CRITICAL: active exploitation, or high-impact RCE/high exposure -> patch within 72 hours
- HIGH: serious vulnerability with mitigations or restricted exposure -> patch within 14 days
- MEDIUM: authenticated or limited-impact scenarios -> patch within 30 to 90 days
- LOW: minimal impact or strong mitigating controls

If patch timelines are missed, documented risk acceptance is required.

## Required Output Structure

Every vulnerability analysis response must use this exact section order:

1. Application Overview
2. Vulnerability Summary
3. Scoring (Exploitability / Exposure / Criticality)
4. Risk Calculation
5. OCIO Classification (with patch timeline)
6. Key Interpretation
7. Required Actions
8. Justification Statement

## Patch Analysis Workflow

1. Read `docs/security/app-context.md`, `docs/security/architecture.md`, `docs/security/threat-model.md`.
2. Determine deployment model, real exposure, data sensitivity, and business criticality.
3. Analyze CVE/advisory details (exploitability, attack preconditions, impact).
4. Apply the 3-factor scoring model.
5. Map to OCIO classification and timeline.
6. Provide concise, audit-ready summary.
7. Provide step-by-step patch instructions when feasible.

## Repository Technical Context

- Framework: NestJS 11.x
- Language: TypeScript
- Runtime: Node.js 24
- Package manager: npm
- CI workflows: `.github/workflows/test.yaml`, `.github/workflows/deploy-nodejs-sample.yaml`

## Patch Implementation Checklist

1. Identify vulnerable package and fixed versions.
2. Choose compatible update version for Node.js 24 and NestJS 11.x.
3. Update `package.json` and refresh `package-lock.json` via `npm install`.
4. Run validation:
   - `npm test`
   - `npm run test:e2e`
   - `npm run lint`
   - `npm run build`
5. Verify resolved findings with `npm audit` or Dependabot alert status.
6. Document CVE, scoring rationale, OCIO timeline, and any risk acceptance requirement.
