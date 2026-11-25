---
name: consent-receipt
description: >-
  Kantara Consent Receipt 1.1: issue human-readable and JSON records of the consent a PII Principal gave a PII Controller. Covers Consent Receipt Specification 1.1.0 (KI-CR-v1.1.0). Use when recording consent for personal data processing, building a consent management system that hands out receipts, or validating a consent receipt JSON document. Triggers: consent receipt, Kantara consent receipt, KI-CR-v1.1.0, CISWG, proof of consent.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Consent Receipt

The Kantara Initiative Consent Receipt Specification 1.1.0 (2018-02-20), a Technical Specification Recommendation from the Consent & Information Sharing Work Group. It defines the fields of a consent receipt, its JSON encoding and schema, and how the receipt is presented to the PII Principal.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: PII Controller or consent management system issuing receipts, or a consumer validating them.
- Target version: Consent Receipt 1.1.0 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 4.2.** "A Consent Receipt MUST include the fields defined as REQUIRED below."
2. **§ 4.2.** "When using JSON, the Consent Receipt MUST also be valid per the Consent Receipt schema in Section 4.8."
3. **§ 4.3.1.** "The value MUST be “KI-CR-v1.1.0” for this version of the specification."
4. **§ 4.3.3.** "The JSON value MUST be expressed as the number of seconds since 1970-01-01 00:00:00 GMT."
5. **§ 4.4.3.** "For Sensitive PII, the PII Controller MUST be specified with legally required explicit notice to the PII Principal."
6. **§ 4.5.6.** "If consent was not explicit, a description of the consent method MUST be provided."
7. **§ 4.5.11.** "MUST be supplied if Third Party Disclosure is TRUE and MUST contain a non-empty string."
8. **§ 4.5.13.** "The field MUST contain a non-empty string if Sensitive PII is TRUE."
9. **§ 4.7.** "Although a CR can be provisioned in any manner that is feasible or expected based on the context, a CR MUST be provided to the PII Principal in a human-readable format either on screen or delivered to the PII Principal, or both."
10. **§ 5.3.1.** "Since Consent Receipts can contain PII, it is a requirement that transmission of Consent Receipts does not take place in the clear and that secure communications be used, e.g., HTTPS."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] A JSON receipt validates against the schema in § 4.8 and carries `version` KI-CR-v1.1.0.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `gdpr`, `json-schema`, `jwt`, `iab-tcf`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Kantara Consent Receipt Specification 1.1.0](https://kantarainitiative.org/download/consent-receipt-specification/): Kantara Initiative Technical Specification Recommendation, Version 1.1.0, 2018-02-20, checked 2026-10-06.
