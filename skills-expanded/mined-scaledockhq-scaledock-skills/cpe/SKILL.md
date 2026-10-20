---
name: cpe
description: >-
  CPE 2.3: name and match IT platforms, software and hardware with Common Platform Enumeration identifiers. Covers CPE 2.3. Use when naming IT products with CPE. Triggers: CPE.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# CPE

Common Platform Enumeration (CPE) Naming Specification Version 2.3 (NIST IR 7695): well-formed CPE names (WFNs) with eleven attributes, and their URI binding (backward compatible with CPE 2.2) and formatted string binding (`cpe:2.3:...`).

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when naming IT products with CPE.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer of CPE names (for example a vulnerability feed or inventory tool) or consumer that parses, binds or matches them.
- Target version: CPE 2.3 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 4.** "If the implementation produces (i.e., generates as an output) CPE names, it MUST produce syntactically correct formatted string bindings as needed to describe or identify applications, operating systems, and hardware devices (cf. 6.2)."
2. **§ 5.1.** "Lexical case SHALL NOT distinguish attributes from one another, e.g., the attributes Foo, foo, FOO, etc., SHALL be considered equivalent."
3. **§ 5.2.** "If an attribute is not used in a WFN, it is said to be unspecified, and its value SHALL default to the logical value ANY (cf. 5.3.1)."
4. **§ 6.2.1.** "Note that all eleven (11) attribute values MUST appear in the formatted string binding."

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
- [ ] Every emitted part attribute value is "a" (applications), "o" (operating systems) or "h" (hardware devices), as § 5.3.3.1 lists.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CPE 2.3](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7695.pdf): NIST IR, NIST IR 7695, fetched 2026-10-06 (NIST IR, 2026-10-06), checked 2026-10-06.
