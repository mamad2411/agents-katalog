---
name: eu-dsa
description: >-
  Digital Services Act: Regulation (EU) 2022/2065 sets duties for intermediary services. Covers Regulation (EU) 2022/2065. Use when applying the Digital Services Act. Triggers: DSA, 2022/2065.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Digital Services Act

Regulation (EU) 2022/2065 of 19 October 2022 on a Single Market for Digital Services (Digital Services Act), published in Official Journal L 277 of 27 October 2022.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when applying the Digital Services Act.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a provider of an intermediary service.
- Target version: Regulation (EU) 2022/2065 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Article 2.** "This Regulation shall apply to intermediary services offered to recipients of the service that have their place of establishment or are located in the Union, irrespective of where the providers of those intermediary services have their place of establishment."
2. **text.** "The Digital Services Coordinator shall, where applicable, specify in the certificate: (a) the particular issues to which the body’s expertise relates, as referred to in point (b) of the first subparagraph;"
3. **Article 21.** "The Board, in cooperation with the Commission, shall publish comprehensive reports, once a year."

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

- `eu-dma`, when the provider is also a gatekeeper under Regulation (EU) 2022/1925: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-dma`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Regulation (EU) 2022/2065](https://publications.europa.eu/resource/celex/32022R2065.ENG): Official Journal, OJ L 277, 27 October 2022, checked 2026-10-06.
