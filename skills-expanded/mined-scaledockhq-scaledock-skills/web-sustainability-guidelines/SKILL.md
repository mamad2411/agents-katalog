---
name: web-sustainability-guidelines
description: >-
  Web Sustainability Guidelines (WSG): Web Sustainability Guidelines ( WSG ) provide actionable recommendations to help digital teams make informed, sustainable decisions. Covers Web Sustainability Guidelines (WSG) (track). Use when reviewing a site or product against the Web Sustainability Guidelines and impact ratings. Triggers: WSG, Web Sustainability Guidelines, impact ratings.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Sustainability Guidelines (WSG)

Web Sustainability Guidelines ( WSG ) provide actionable recommendations to help digital teams make informed, sustainable decisions. In considering different aspects of work and the web, these guidelines address the planet, people, and prosperity ( PPP ) impacts of digital products and services. They are interdisciplinary and cover artificial intelligence and emerging web technologies. Some guidelines reference existing documents and specifications from W3C and other organizations. This approach highlights the importance of intersectionality and collaboration, rather than reinterpreting established recommendations. While WSG prioritizes web technologies, it can also support broader organizat

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reviewing a site or product against the Web Sustainability Guidelines and impact ratings.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Sustainability Guidelines (WSG) (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Introduction.** "The guidance and metrics may change over time, and other considerations - including non-digital factors - beyond carbon should be accounted for."
2. **1.1 Background on WSG.** "The WSG are based on the values of the United Nations Sustainable Development Goals [ SDGs ]: They reflect an understanding that sustainable development everywhere must integrate economic growth, social well-being and environmental protection."
3. **1.2 WSG layers of guidance.** "Readers should review all sections , even those not nominally related to their assumed responsibilities."
4. **1.3.1 Challenges in measurement.** "For example, deploying energy-efficient hardware may reduce energy consumption and have the side-benefit of local noise reduction, but that hardware must be manufactured, and that in turn necessitates the mining of rare earth metals."
5. **1.3.1 Challenges in measurement.** "Implementers should do what they can and mitigate remaining negative impacts to improve their overall impact."
6. **1.3.1 Challenges in measurement.** "Material use, electronic waste, water consumption, and chemical pollution associated with digital infrastructure should also be considered wherever the data and methodologies are available [ VARIABLES ]."
7. **1.3.1 Challenges in measurement.** "Implementers should evaluate potential trade-offs carefully to ensure improvements in one area do not unintentionally cause harm in another."
8. **1.3.3 Call to action.** "Note Tools or user agents that provide WSG insights must avoid fingerprinting risks ."

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

- [Web Sustainability Guidelines (WSG)](https://www.w3.org/TR/web-sustainability-guidelines/): Draft Note, web-sustainability-guidelines DNOTE-web-sustainability-guidelines-20260924 (Draft Note, 2026-09-24), checked 2026-10-06.
- [Web Sustainability Guidelines (WSG) Impact Ratings](https://www.w3.org/TR/wsg-ir/): Draft Note, wsg-ir (Draft Note, 2026-08-20), checked 2026-10-06.
