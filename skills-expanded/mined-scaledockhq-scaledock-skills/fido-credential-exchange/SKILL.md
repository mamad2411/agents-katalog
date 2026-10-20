---
name: fido-credential-exchange
description: >-
  FIDO Credential Exchange: This document defines the data structures and format of credentials being passed or referenced between two applications during credential exchange. Covers Credential Exchange Format 1.0, Credential Exchange Protocol 1.0 (build). Use when exchanging passkeys between providers. Triggers: CXP, CXF, credential exchange.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# FIDO Credential Exchange

This document defines the data structures and format of credentials being passed or referenced between two applications during credential exchange.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging passkeys between providers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Credential Exchange Format 1.0 (default); Credential Exchange Protocol 1.0 (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.3. Terminology.** "The exporting provider MUST ensure the data is transferred securely by either encrypting it themselves or by relying on an orchestrator’s security guarantees, see more information in section § 5.1 Orchestrating Party Requirements ."
2. **1.3. Terminology.** "Identifiers MUST be unique for a given exchanged Account and have a maximum of 64 bytes in length."
3. **1.3. Terminology.** "Identifiers SHOULD NOT have any personally identifying information contained as they will be shared in clear text during any given [CXP] exchange sessions."
4. **1.3. Terminology.** "An identifier for a given entity SHOULD be the same across different creations of a CXF document."
5. **1.3. Terminology.** "This transfer protocol MUST ensure confidentiality between the providers following the § 5.1 Orchestrating Party Requirements ."
6. **1.3. Terminology.** "The preferred transfer protocol SHOULD be [CXP] ."
7. **2.1. Encoding Considerations.** "Conforming participants MUST support encoding the types defined in this format to [JSON] ."
8. **2.1.1. Enumerations as recommended.** "Should the importing provider encounter an unknown enumeration value, the importing provider SHOULD follow these RECOMMENDATIONS: If the field member holding the unknown enumeration is OPTIONAL, the field member SHOULD be ignored as though the field was not provided at all."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Credential Exchange Format 1.0](https://fidoalliance.org/specs/cx/cxf-v1.0-ps-errata-20260309.html): Proposed Standard errata, CXF 1.0 Proposed Standard errata 2026-03-09 (Proposed Standard errata, 2026-03-09), checked 2026-10-06.
- [Credential Exchange Protocol 1.0](https://fidoalliance.org/specs/cx/cxp-v1.0-wd-20241003.html): Working Draft, CXP 1.0 Working Draft 2024-10-03 (Working Draft, 2024-10-03), checked 2026-10-06.
