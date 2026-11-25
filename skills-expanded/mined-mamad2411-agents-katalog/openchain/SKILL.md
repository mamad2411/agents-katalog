---
name: openchain
description: >-
  OpenChain (ISO/IEC 5230, ISO/IEC 18974): run open source license compliance and security assurance programs. Covers OpenChain ISO 5230, OpenChain ISO 18974. Use when conforming to OpenChain license or security assurance. Triggers: OpenChain, ISO 5230, ISO 18974.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OpenChain

The OpenChain Project's two program specifications: ISO/IEC 5230:2020 (OpenChain Specification 2.1, open source license compliance) and ISO/IEC 18974:2023 (OpenChain security assurance), read from the project's public Markdown texts at pinned commits.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Owner of an organization's open source program: policy, roles, bill of materials, license compliance or known-vulnerability handling for supplied software.
- Target version: OpenChain ISO 5230 (current); OpenChain ISO 18974 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **ISO/IEC 5230 § 3.1.1.** "A written open source policy shall exist that governs open source license compliance of the supplied software."
2. **ISO/IEC 5230 § 3.3.1.** "A process shall exist for creating and managing a bill of materials that includes each open source component (and its identified licenses) from which the supplied software is comprised."
3. **ISO/IEC 18974 § 4.1.1.** "A written policy shall be created that governs open source software security assurance of supplied software."
4. **ISO/IEC 18974 § 4.3.2.** "A process shall exist to ensure each open source software component to be included in the software bill of materials for the supplied software will have some security assurance activities applied."
5. **ISO/IEC 18974 § 4.2.1.** "To accomplish this, it shall publicly identify a means for third parties to inquire about how a known vulnerability impacts a software offering."

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
- [ ] For each targeted specification, every clause quoted in `references/requirements.md` has a named verification record (policy, procedure or bill of materials), cited by clause number.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `spdx`, `cyclonedx`, `reuse`, `s2c2f`, `openvex`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ISO/IEC 5230:2020, OpenChain Specification 2.1 (public text)](https://raw.githubusercontent.com/OpenChain-Project/License-Compliance-Specification/968092c97da81a750f03c7b1becbd25bd088b2cb/ISO-5230-2020/en/ISO-5230-2020.md): International Standard (ISO/IEC 5230:2020), ISO/IEC 5230:2020 (OpenChain 2.1), commit 968092c97da8 (2025-01-08), checked 2026-10-06.
- [ISO/IEC 18974:2023, OpenChain security assurance specification (public text)](https://raw.githubusercontent.com/OpenChain-Project/Security-Assurance-Specification/5bb0a024ce967720301bfa0e1d4d9e834690066d/Security-Assurance-Specification/ISO-18974/en/ISO-18974.md): International Standard (ISO/IEC 18974:2023), ISO/IEC 18974:2023, commit 5bb0a024ce96 (2024-11-08), checked 2026-10-06.
