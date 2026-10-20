---
name: cds-hooks
description: >-
  CDS Hooks 2.0: call clinical decision support services from an EHR workflow and return cards. Covers CDS Hooks 2.0. Use when a clinical system calls decision support. Triggers: CDS Hooks.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# CDS Hooks

This is the current published release of the CDS Hooks specification. All stable releases are available at https://cds-hooks.hl7.org/.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when a clinical system calls decision support.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: CDS Hooks 2.0 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Conformance Language.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in RFC2119 ."
2. **Conformance Language.** "Further, the key word "CONDITIONAL" indicates that a particular item is either REQUIRED or OPTIONAL, based upon another item."
3. **Use of JSON.** "All data exchanged through production RESTful APIs MUST be sent and received as JSON (JavaScript Object Notation) structures and are transmitted over HTTPS."
4. **Use of JSON.** "Null and empty JSON elements JSON elements SHALL NOT be null, unless otherwise specified."
5. **Use of JSON.** "JSON elements SHALL NOT be empty, unless otherwise specified (e.g."
6. **Use of JSON.** "If a JSON attribute is defined as OPTIONAL, and does not have a value, implementers MUST omit it."
7. **Use of JSON.** "Unless otherwise specified, JSON attribute values SHALL NOT be null or empty, so null , "" , [] , or {} are prohibited."
8. **Use of JSON.** "If a JSON attribute is defined with as OPTIONAL, and does not have a value, implementers SHALL omit it."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CDS Hooks 2.0](https://cds-hooks.hl7.org/2.0/): Specification, CDS Hooks 2.0 (Specification, 2026-10-06), checked 2026-10-06.
