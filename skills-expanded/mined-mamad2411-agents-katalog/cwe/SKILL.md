---
name: cwe
description: >-
  CWE: classify software and hardware weaknesses with Common Weakness Enumeration ids. Covers CWE. Use when classifying software weaknesses. Triggers: CWE.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# CWE

This view is intended to facilitate research into weaknesses, including their inter-dependencies, and can be leveraged to systematically identify theoretical gaps within CWE. It is mainly organized according to abstractions of behaviors instead of how they can be detected, where they appear in code, or when they are introduced in the development life cycle. By design, this view is expected to include every weakness within CWE.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when classifying software weaknesses.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: CWE (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **CWE VIEW: Research Concepts.** "View ID: 1000 Vulnerability Mapping : PROHIBITED This CWE ID must not be used to map to real-world vulnerabilities Type: Graph Downloads: Booklet | CSV | XML Objective This view is intended to facilitate research into weaknesses, including their inter-dependencies, and can be leveraged to systematically identify theoretical gaps within CWE."
2. **CWE VIEW: Research Concepts.** "A chain is a set of weaknesses that must be reachable consecutively in order to produce an exploitable vulnerability."
3. **CWE VIEW: Research Concepts.** "While a composite is a set of weaknesses that must all be present simultaneously in order to produce an exploitable vulnerability."
4. **CWE VIEW: Research Concepts.** "This results in a conflict between the functional requirement that some addresses need to be writable by software during operation and the security requirement that the system configuration lock bit must be set during the boot process."
5. **CWE VIEW: Research Concepts.** "Least Privilege Violation - (272) 1000 (Research Concepts) > 284 (Improper Access Control) > 269 (Improper Privilege Management) > 271 (Privilege Dropping / Lowering Errors) > 272 (Least Privilege Violation) The elevated privilege level required to perform operations such as chroot() should be dropped immediately after the operation is performed."
6. **CWE VIEW: Research Concepts.** "Files or Directories Accessible to External Parties - (552) 1000 (Research Concepts) > 284 (Improper Access Control) > 285 (Improper Authorization) > 552 (Files or Directories Accessible to External Parties) The product makes files or directories accessible to unauthorized actors, even though they should not be."
7. **CWE VIEW: Research Concepts.** "Authorization Bypass Through User-Controlled SQL Primary Key - (566) 1000 (Research Concepts) > 284 (Improper Access Control) > 285 (Improper Authorization) > 863 (Incorrect Authorization) > 639 (Authorization Bypass Through User-Controlled Key) > 566 (Authorization Bypass Through User-Controlled SQL Primary Key) The product uses a database table that includes records that should not be…"
8. **CWE VIEW: Research Concepts.** "Weak Password Requirements - (521) 1000 (Research Concepts) > 284 (Improper Access Control) > 287 (Improper Authentication) > 1390 (Weak Authentication) > 1391 (Use of Weak Credentials) > 521 (Weak Password Requirements) The product does not require that users should have strong passwords."

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

- [CWE](https://cwe.mitre.org/data/definitions/1000.html): View, CWE research concepts view, fetched 2026-10-06 (View, 2026-10-06), checked 2026-10-06.
