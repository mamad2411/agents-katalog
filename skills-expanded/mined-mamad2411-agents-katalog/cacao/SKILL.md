---
name: cacao
description: >-
  CACAO 2.0: write machine-readable security playbooks in the OASIS CACAO JSON format. Covers CACAO 2.0. Use when writing security playbooks. Triggers: CACAO, security playbooks.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# CACAO

https://docs.oasis-open.org/cacao/security-playbooks/v2.0/cs01/security-playbooks-v2.0-cs01.docx (Authoritative)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing security playbooks.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: CACAO 2.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **document.** "Key words: The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " NOT RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here."
2. **2.1 Vocabularies.** "However, if a similar value is already in the vocabulary, that value MUST be used."
3. **2.1 Vocabularies.** "A closed vocabulary is effectively an enumeration and MUST be used as defined."
4. **2.2 Playbook Creator.** "� Entities that re-publish an object from another entity without making any changes to the object, and thus maintaining the original value in the id property, are not considered the object creator and MUST NOT change the created_by property."
5. **2.2 Playbook Creator.** "An entity that accepts objects and republishes them with modifications, additions, or omissions MUST create a new id and MUST change the created_by property for the object as they are now considered the object creator of the new object for purposes of versioning (see section 2.3 versioning for more information)."
6. **2.3 Versioning.** "The first version of a playbook MUST have the same timestamp for both the created and modified properties."
7. **2.3 Versioning.** "Implementations MUST consider the version of the playbook with the most recent modified value to be the most recent version of the playbook."
8. **2.3 Versioning.** "For every new version of a playbook, the modified property MUST be updated to represent the time that the new version was created."

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

- [CACAO 2.0](https://docs.oasis-open.org/cacao/security-playbooks/v2.0/security-playbooks-v2.0.html): OASIS Standard, CACAO Security Playbooks 2.0, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
