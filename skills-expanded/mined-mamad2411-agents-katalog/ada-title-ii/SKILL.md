---
name: ada-title-ii
description: >-
  ADA Title II: 28 CFR Part 35 is nondiscrimination on the basis of disability in state and local government services. Covers 28 CFR Part 35. Use when applying ADA Title II. Triggers: ADA Title II, 28 CFR 35.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# ADA Title II

Title II of the Americans with Disabilities Act as implemented by the U.S. Department of Justice in 28 CFR Part 35: nondiscrimination by state and local governments in their services, programs and activities, including program accessibility, new construction, effective communication, and the web content and mobile app requirements of subpart H.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when applying ADA Title II to a state or local government service.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a public entity (state or local government, or one of its departments or instrumentalities), or a contractor building web content, mobile apps or facilities for one.
- Target version: 28 CFR Part 35 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 35.130(a).** "No qualified individual with a disability shall, on the basis of disability, be excluded from participation in or be denied the benefits of the services, programs, or activities of a public entity, or be subjected to discrimination by any public entity."
2. **§ 35.130(b)(7)(i).** "A public entity shall make reasonable modifications in policies, practices, or procedures when the modifications are necessary to avoid discrimination on the basis of disability, unless the public entity can demonstrate that making the modifications would fundamentally alter the nature of the service, program, or activity."
3. **§ 35.160(a)(1).** "A public entity shall take appropriate steps to ensure that communications with applicants, participants, members of the public, and companions with disabilities are as effective as communications with others."
4. **§ 35.200(a).** "A public entity shall ensure that the following are readily accessible to and usable by individuals with disabilities: (1) Web content that a public entity provides or makes available, directly or through contractual, licensing, or other arrangements; and (2) Mobile apps that a public entity provides or makes available, directly or through contractual, licensing, or other arrangements."
5. **§ 35.200(b)(1).** "Beginning April 26, 2027, a public entity, other than a special district government, with a total population of 50,000 or more shall ensure that the web content and mobile apps that the public entity provides or makes available, directly or through contractual, licensing, or other arrangements, comply with Level A and Level AA success criteria and conformance requirements specified in WCAG 2.1, unless the public entity can demonstrate that compliance with this section would result in a fundamental alteration in the nature of a service, program, or activity or in undue financial and administrative burdens."

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
- [ ] For web content and mobile apps, the § 35.200(b) compliance date that applies to the entity's population and type was recorded.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

- `section-508`, when the same service is also federal ICT under the Revised 508 Standards: `npx skills add ScaleDockHQ/scaledock-skills --skill section-508`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [28 CFR Part 35](https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-28?part=35): eCFR, current title 28 part 35, fetched 2026-10-06, checked 2026-10-06.
