---
name: aoda
description: >-
  AODA: apply Ontario's accessibility law and the Integrated Accessibility Standards (O. Reg. 191/11) to websites, web content, kiosks, feedback, accessible formats, training and accessibility reports. Covers the Accessibility for Ontarians with Disabilities Act, 2005 and O. Reg. 191/11 as consolidated from March 30, 2026. Use when an organization that provides goods, services or facilities in Ontario must meet WCAG 2.0 Level AA for its website, handle requests for accessible formats, run an accessible feedback process or file an accessibility report. Triggers: AODA, Ontario accessibility, IASR, O. Reg. 191/11, Integrated Accessibility Standards, accessibility compliance report, WCAG 2.0 AA Ontario.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Accessibility for Ontarians with Disabilities Act (AODA)

The Accessibility for Ontarians with Disabilities Act, 2005 (AODA) and its Integrated Accessibility Standards Regulation (O. Reg. 191/11, IASR), read from the Ontario e-Laws consolidated text. The quotes cover the parts that touch digital products: websites and web content, self-service kiosks, feedback, accessible formats, training, customer service and accessibility reports.

**Scope.** This is law, not legal advice. Obligations depend on the organization type and size defined in O. Reg. 191/11, s. 2, and many sections carry compliance dates that have passed. The transportation, employment, design of public spaces and built environment standards are not quoted.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Obligated organization (Government of Ontario, Legislative Assembly, designated public sector organization, large organization with 50 or more employees in Ontario, or small organization), or a vendor building for one.
- Target version: AODA 2005 with O. Reg. 191/11 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **O. Reg. 191/11, s. 14 (2).** "Designated public sector organizations and large organizations shall make their internet websites and web content conform with the World Wide Web Consortium Web Content Accessibility Guidelines (WCAG) 2.0, initially at Level A and increasing to Level AA, and shall do so in accordance with the schedule set out in this section."
2. **O. Reg. 191/11, s. 14 (4).** "By January 1, 2021, all internet websites and web content must conform with WCAG 2.0 Level AA, other than,"
3. **O. Reg. 191/11, s. 14 (5).** "to websites and web content, including web-based applications, that an organization controls directly or through a contractual relationship that allows for modification of the product; and"
4. **O. Reg. 191/11, s. 12 (1).** "Except as otherwise provided, every obligated organization shall upon request provide or arrange for the provision of accessible formats and communication supports for persons with disabilities,"
5. **O. Reg. 191/11, s. 12 (2).** "The obligated organization shall consult with the person making the request in determining the suitability of an accessible format or communication support."
6. **O. Reg. 191/11, s. 11 (1).** "Every obligated organization that has processes for receiving and responding to feedback shall ensure that the processes are accessible to persons with disabilities by providing or arranging for the provision of accessible formats and communications supports, upon request."
7. **O. Reg. 191/11, s. 7 (1).** "Every obligated organization shall ensure that training is provided on the requirements of the accessibility standards referred to in this Regulation and on the Human Rights Code as it pertains to persons with disabilities to,"
8. **AODA, s. 14 (1).** "A person or organization to whom an accessibility standard applies shall file an accessibility report with a director annually or at such other times as the director may specify."

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
- [ ] Public websites and web content conform with WCAG 2.0 Level AA (live captions and pre-recorded audio description excepted for large organizations under s. 14 (4)).
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `wcag`, `en-301-549`, `section-508`, `eu-accessibility-act`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [O. Reg. 191/11: Integrated Accessibility Standards](https://www.ontario.ca/laws/regulation/110191): Ontario regulation (consolidated), Consolidation period from 2026-03-30, last amendment O. Reg. 69/26, checked 2026-10-06.
- [Accessibility for Ontarians with Disabilities Act, 2005, S.O. 2005, c. 11](https://www.ontario.ca/laws/statute/05a11): Ontario statute (consolidated), Consolidation period from 2016-04-19, last amendment 2016, c. 5, Sched. 1, checked 2026-10-06.
