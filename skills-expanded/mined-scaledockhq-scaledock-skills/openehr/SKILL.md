---
name: openehr
description: >-
  openEHR: The openEHR Foundation is an independent, non-profit foundation, facilitating the sharing of health records by consumers and clinicians via open specifications, clinical models and open platform implementations. Covers openEHR Architecture Overview. Use when modeling an openEHR record. Triggers: openEHR.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# openEHR

The openEHR Foundation is an independent, non-profit foundation, facilitating the sharing of health records by consumers and clinicians via open specifications, clinical models and open platform implementations.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when modeling an openEHR record.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: openEHR Architecture Overview (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1. Purpose.** "This document is the key technical overview of openEHR, and should be read before all other technical documents."
2. **6.4.1.1. Ontology of Entry Types.** "Note that even if the ontology shown in Figure 24 is not correct (undoubtedly it is not), archetypes will be constructed to account for each improved idea of what such categories should really be."
3. **7.1.1. Privacy, Confidentiality and Consent.** "A widely accepted principle is that information provided (either directly or due to observation or testing of specimens etc.) in confidence by a patient to health professionals during an episode of care should only be passed on or otherwise become available to other parties if the patient agrees; put more simply: data sharing must be controlled by patient consent ."
4. **7.1.3. Specifying Access Control.** "In theory, it should be easy for the patient or some clinical professional to specify who can see the patient record."
5. **7.1.3. Specifying Access Control.** "The advent of e-prescribing and e-pharmacy will bring even larger numbers of health and allied health workers into the e-Health matrix, making the problem of individual identification of who should see the patient’s data infeasible."
6. **7.1.4. The Problem of Roles.** "Realistically, the evaluation of a role category such as "care deliverer" into particular identities such as those of nurses on the ward on a particular day must be done in each care delivery environment, not in the EHR."
7. **7.2. Threats to Security and Privacy.** "Any model of how security and privacy are supported in the health record must be based on some notion of assumed threats."
8. **7.3.2.2. Access Control.** "Access list the overriding principle of access control must be "relevance" both in terms of user identity (who is delivering care to the patient) and time (during the current episode of care, and for some reasonable, limited time afterward)."

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

- [openEHR Architecture Overview](https://specifications.openehr.org/releases/BASE/latest/architecture_overview.html): Specification, openEHR BASE Architecture Overview, latest release (Specification, 2026-10-06), checked 2026-10-06.
