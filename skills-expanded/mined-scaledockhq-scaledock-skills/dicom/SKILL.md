---
name: dicom
description: >-
  DICOM: PS3.1 introduction and overview of medical image exchange. Covers
  DICOM PS3.1. Use when exchanging medical images.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DICOM

DICOM PS3.1 is the introduction and overview of the DICOM standard.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exchanging medical images.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: DICOM PS3.1 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **DICOM PS3.1 2026d - Introduction and Overview.** "Anyone using this document should rely on his or her own independent judgment or, as appropriate, seek the advice of a competent professional in determining the exercise of reasonable care in any given circumstances."
2. **DICOM PS3.1 2026d - Introduction and Overview.** "Information that must be supplied with an implementation for which conformance to the Standard is claimed."
3. **DICOM PS3.1 2026d - Introduction and Overview.** "DICOM explicitly describes how an implementor must structure a Conformance Statement to select specific options."
4. **DICOM PS3.1 2026d - Introduction and Overview.** "A Profile can add requirements but should not contradict DICOM requirements, as that would make it impossible to comply with both DICOM and the Profile."
5. **Note.** "For devices to interact, there must be standards on how devices are expected to react to Commands and associated data, not just the information that is to be moved between devices."
6. **Note.** "In particular, a conformance statement must specify enough information to determine the functions for which interoperability can be expected with another device claiming conformance."
7. **Note.** "PS3.2 specifies the general requirements that must be met by any implementation claiming conformance."
8. **Note.** "It specifies the information that must be present in a Conformance Statement."

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

- [DICOM PS3.1](https://dicom.nema.org/medical/dicom/current/output/html/part01.html): Standard, DICOM PS3.1 current HTML (Standard, 2026-10-06), checked 2026-10-06.
