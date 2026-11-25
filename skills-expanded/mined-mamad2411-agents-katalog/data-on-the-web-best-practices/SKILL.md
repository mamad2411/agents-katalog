---
name: data-on-the-web-best-practices
description: >-
  Data on the Web Best Practices: This document provides Best Practices related to the publication and usage of data on the Web designed to help support a self-sustaining ecosystem. Covers Data on the Web Best Practices. Use when publishing data on the web. Triggers: Data on the Web Best Practices, DWBP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Data on the Web Best Practices

This document provides Best Practices related to the publication and usage of data on the Web designed to help support a self-sustaining ecosystem. Data should be discoverable and understandable by humans and machines. Where data is used in some way, whether by the originator of the data or by an external party, such usage should also be discoverable and the efforts of the data publisher recognized. In short, following these Best Practices will facilitate interaction between publishers and consumers.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing data on the web.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Data on the Web Best Practices (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Introduction.** "Not all data and metadata should be shared openly, however."
2. **1. Introduction.** "It is for data publishers to determine policy on which data should be shared and under what circumstances."
3. **1. Introduction.** "Although it is likely to be safe to share some of that information openly, and even more within a controlled environment, publishers should bear in mind that combining data from multiple sources may allow inadvertent identification of individuals."
4. **3. Scope.** "As noted above, whether a Best Practice has or has not been followed should be judged against the intended outcome , not the possible approach to implementation which is offered as guidance."
5. **4. Context.** "A relevant aspect of this is the identification principle that says that URIs should be used to identify resources."
6. **4. Context.** "All resources should be published with stable URIs, so that they can be referenced and make links, via URIs, between two or more resources."
7. **Intended Outcome.** "What it should be possible to do when a data publisher follows the Best Practice."
8. **8.1 Running Example.** "It is important that both humans and software agents can easily understand and process the data which should be kept up to date and be easily discoverable on the Web."

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

- [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/): Recommendation, dwbp REC-dwbp-20170131 (Recommendation, 2017-01-31), checked 2026-10-06.
- [Spatial Data on the Web Best Practices](https://www.w3.org/TR/sdw-bp/): Draft Note, sdw-bp (Draft Note, 2023-09-19), checked 2026-10-06.
