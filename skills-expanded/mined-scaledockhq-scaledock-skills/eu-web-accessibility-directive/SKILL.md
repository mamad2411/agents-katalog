---
name: eu-web-accessibility-directive
description: >-
  Web Accessibility Directive: Directive (EU) 2016/2102 covers public-sector websites and mobile applications. Covers Directive (EU) 2016/2102. Use when applying the public-sector web accessibility rules. Triggers: 2016/2102, WAD.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Accessibility Directive

Directive (EU) 2016/2102 of 26 October 2016 on the accessibility of the websites and mobile applications of public sector bodies, published in Official Journal L 327 of 2 December 2016.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when making a public-sector website or mobile application accessible.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a public-sector body or its supplier.
- Target version: Directive (EU) 2016/2102 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "They describe what must be achieved in order for the user to be able to perceive, operate, interpret and understand a website, a mobile application and related content."
2. **Article 4.** "Those technical specifications shall meet the accessibility requirements set out in Article 4 and shall ensure at least a level of accessibility equivalent to that ensured by European standard EN 301 549 V1.1.2 (2015-04)."
3. **Article 11.** "By 23 December 2018, the Commission shall adopt the first such implementing act."

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

- `wcag`, when the directive's requirements are met through a web content standard: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`
- `en-301-549`, when an ICT procurement also cites EN 301 549: `npx skills add ScaleDockHQ/scaledock-skills --skill en-301-549`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Directive (EU) 2016/2102](https://publications.europa.eu/resource/celex/32016L2102.ENG): Official Journal, OJ L 327, 2 December 2016, checked 2026-10-06.
