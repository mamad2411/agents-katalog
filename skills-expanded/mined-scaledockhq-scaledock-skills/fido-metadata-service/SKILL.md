---
name: fido-metadata-service
description: >-
  FIDO Metadata Service: The FIDO Authenticator Metadata Specification defines so-called "Authenticator Metadata" statements. Covers FIDO Metadata Service 3.1.1, FIDO Metadata Service 3.1 (supported). Use when publishing or consuming FIDO authenticator metadata. Triggers: FIDO MDS, metadata statement.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# FIDO Metadata Service

The FIDO Authenticator Metadata Specification defines so-called "Authenticator Metadata" statements. The metadata statements contains the "Trust Anchor" required to validate the attestation object, and they also describe several other important characteristics of the authenticator. The metadata service described in this document defines a baseline method for relying parties to access the latest metadata statements.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing or consuming FIDO authenticator metadata.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: FIDO Metadata Service 3.1.1 (default); FIDO Metadata Service 3.1 (supported); FIDO Metadata Service 3.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Notation.** "WebIDL dictionary members MUST NOT have a value of null."
2. **1. Notation.** "Unless otherwise specified, if a WebIDL dictionary member is DOMString, it MUST NOT be empty."
3. **1. Notation.** "Unless otherwise specified, if a WebIDL dictionary member is a List, it MUST NOT be an empty list."
4. **1.1. Key Words.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC2119] ."
5. **3.1.1. Metadata BLOB Payload Entry dictionary.** "This field MUST be set if the authenticator implements FIDO UAF."
6. **3.1.1. Metadata BLOB Payload Entry dictionary.** "This field MUST be set if the authenticator implements FIDO2."
7. **3.1.1. Metadata BLOB Payload Entry dictionary.** "This value MUST be calculated according to method 1 for computing the keyIdentifier as defined in [RFC5280] section 4.2.1.2."
8. **3.1.1. Metadata BLOB Payload Entry dictionary.** "The hex string MUST NOT contain any non-hex characters (e.g."

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

- [FIDO Metadata Service 3.1.1](https://fidoalliance.org/specs/mds/fido-metadata-service-v3.1.1-ps-20260105.html): Proposed Standard, MDS 3.1.1 Proposed Standard 2026-01-05 (Proposed Standard, 2026-01-05), checked 2026-10-06.
- [FIDO Metadata Service 3.1](https://fidoalliance.org/specs/mds/fido-metadata-service-v3.1-ps-20250521.html): Proposed Standard, MDS 3.1 Proposed Standard 2025-05-21 (Proposed Standard, 2025-05-21), checked 2026-10-06.
- [FIDO Metadata Service 3.0](https://fidoalliance.org/specs/mds/fido-metadata-service-v3.0-ps-20210518.html): Proposed Standard, MDS 3.0 Proposed Standard 2021-05-18 (Proposed Standard, 2021-05-18), checked 2026-10-06.
