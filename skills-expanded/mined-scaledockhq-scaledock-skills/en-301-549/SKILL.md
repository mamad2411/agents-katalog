---
name: en-301-549
description: >-
  EN 301 549: apply the European accessibility requirements for ICT products and services, including web, documents and software. Covers EN 301 549 V4.1.1, EN 301 549 V3.2.1 (supported). Use when applying European ICT accessibility requirements. Triggers: EN 301 549.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# EN 301 549

EN 301 549, the harmonised European standard published by ETSI, CEN and CENELEC that sets accessibility requirements for ICT products and services: functional performance criteria, hardware, two-way communication, video, web content (by reference to WCAG), non-web documents and software, documentation and support services.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when applying European ICT accessibility requirements.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: supplier designing or evaluating ICT for conformance, or a buyer writing ICT procurement requirements.
- Target version: EN 301 549 V4.1.1 (default); EN 301 549 V3.2.1 (supported). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 14.1.** "Conformance to the present document is achieved by meeting all the applicable requirements."
2. **§ 14.1.** "Applicable requirements are requirements whose preconditions are true for an ICT."
3. **§ 4.2.1.** "Where ICT provides visual modes of operation, the ICT shall provide at least one mode of operation that does not require vision."
4. **§ 9.1.1.1.** "Where ICT is, or includes, a web page, the web page shall satisfy WCAG 2.2 Success Criterion 1.1.1 Non-text content."
5. **§ 11.6.2.** "Where ICT is, or includes, non-web software, the non-web software shall not disrupt documented platform accessibility features except when requested to do so by the user during the operation of the software."

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
- [ ] The precondition ("Where ICT ...") of each clause was checked before the clause was treated as applicable.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

- `wcag`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [EN 301 549 V4.1.1](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.01_60/en_301549v040101p.pdf): Harmonised European Standard, EN 301 549 V4.1.1 (2026-09), fetched 2026-10-06 (Harmonised European Standard, 2026-10-06), checked 2026-10-06.
- [EN 301 549 V3.2.1](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf): Harmonised European Standard, EN 301 549 V3.2.1 (2021-03), fetched 2026-10-06 (Harmonised European Standard, 2026-10-06), checked 2026-10-06.
