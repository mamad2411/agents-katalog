---
name: kyc-screener
description: Run a Codex KYC screening workflow that parses an onboarding packet, applies the rules grid, and stages an escalation workbook with explicit screening and verification notes.
---

# KYC Screener Task Pack

Use this task pack when the user needs a reviewed onboarding or investor packet screened into an escalation-ready output.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../finance-modeling-office-pro/references/source-inventory.md`](../finance-modeling-office-pro/references/source-inventory.md) for provenance
- use the reusable skill content under `codex/skills/operations/`
- use [`docs/runtime/spreadsheets.md`](../finance-modeling-office-pro/references/runtime-spreadsheets.md) for workbook output discipline

## Inputs

Minimum inputs:

- onboarding or investor packet identifier
- local packet files
- applicable KYC or AML rules grid

Optional inputs:

- risk appetite or escalation threshold
- enhanced due-diligence checklist
- prior screening result for the same subject

## Output Contract

Primary artifacts:

- `./out/escalation-<packet>.xlsx`
- `./out/kyc-review-<packet>.md`

Supporting scratch files are allowed under:

- `./out/tmp/kyc-screener/`

## Connector Gate

Preferred connector:

- `screening`

If the screening connector is unavailable, continue only if sanctions, PEP, and adverse-media evidence is already present in local reviewed materials. State that limitation explicitly.

## Task-Pack Flow

1. Scope the packet and applicable rules.
2. Parse the onboarding materials.
3. Apply the rules grid and screening results.
4. Write the escalation workbook.
5. Verify and stop for compliance review.

## Phase 1: Scope The Packet

- Confirm the subject, entity, and beneficial-owner scope.
- Confirm which files are untrusted onboarding documents.
- Confirm the rules grid version.

## Phase 2: Parse The Packet

Target artifact:

- `./out/tmp/kyc-screener/parsed-packet.md`

Use:

- `kyc-doc-parse`

Capture:

- identity fields
- ownership and control structure
- source-of-funds data
- missing or inconsistent documents

If delegation is available and explicitly authorized, this phase maps to `kyc-doc-reader`.

## Phase 3: Apply Rules And Screening

Target artifact:

- `./out/tmp/kyc-screener/rules-result.md`

Use:

- `kyc-rules`

Rules:

- cite the rule basis for every pass, fail, or escalation flag
- separate missing-data flags from true risk hits
- state whether sanctions, PEP, and adverse-media results came from the connector or supplied evidence

If delegation is available and explicitly authorized, this phase maps to `kyc-rules-engine`.

## Phase 4: Write The Escalation Workbook

Write:

- `./out/escalation-<packet>.xlsx`

The workbook should contain:

- subject summary
- rules outcome table
- missing-document list
- escalation reasons
- recommended next action

If delegation is available and explicitly authorized, this phase maps to `kyc-escalator`.

## Phase 5: Verify And Stop

Run:

- `python scripts/verify_xlsx.py ./out/escalation-<packet>.xlsx`

Write the review memo to:

- `./out/kyc-review-<packet>.md`

The review memo must state:

- output paths
- rules version
- connector availability
- whether any sanctions, PEP, or adverse-media hit was found
- what remains unresolved for compliance sign-off

Do not present the output as a final compliance decision.
