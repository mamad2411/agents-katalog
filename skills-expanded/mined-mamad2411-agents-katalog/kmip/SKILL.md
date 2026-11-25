---
name: kmip
description: >-
  KMIP 3.0: manage cryptographic keys and objects over the OASIS Key Management Interoperability Protocol. Covers KMIP 3.0. Use when managing cryptographic keys over KMIP. Triggers: KMIP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# KMIP

https://docs.oasis-open.org/kmip/kmip-spec/v3.0/csd02/kmip-spec-v3.0-csd02.docx (Authoritative)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when managing cryptographic keys over KMIP.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: KMIP 3.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Terminology.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [ RFC2119 ]."
2. **2.** "All objects within the key management system SHALL have a minimum set of attributes."
3. **2.** "Attribute REQUIRED Unique Identifier Yes Short Unique Identifier Yes Object Class Yes Object Type Yes Initial Date Yes Table SEQ Table \* ARABIC 2 : Minimum required Object attributes"
4. **2.1 System Objects.** "All System Objects SHALL have an Object Class of System."
5. **2.1 System Objects.** "Special authentication and authorization SHOULD be enforced when creating or destroying System Objects or when setting, modifying or deleting attributes of System Objects."
6. **2.1.1 User.** "Attribute REQUIRED Unique Identifier Yes Short Unique Identifier Yes Object Class Yes Object Type Yes Initial Date Yes Name Yes Credential Link Yes Table SEQ Table \* ARABIC 3 : Required User Aattributes"
7. **2.1.2 Group.** "Attribute REQUIRED Unique Identifier Yes Short Unique Identifier Yes Object Class Yes Object Type Yes Initial Date Yes Name Yes Table SEQ Table \* ARABIC 4 : Required Group Attributes"
8. **2.1.3.1 Password Credential.** "· The Salted Password and Password Salt Algorithm combined with the optional Password Salt provides an algorithm-based comparison mechanism One of the above methods SHALL be specified."

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

- [KMIP 3.0](https://docs.oasis-open.org/kmip/kmip-spec/v3.0/kmip-spec-v3.0.html): OASIS Standard, KMIP 3.0, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
