---
name: cognitive-accessibility
description: >-
  Making Content Usable for People with Cognitive and Learning Disabilities: This document is for people who make web content (web pages) and web applications. Covers Making Content Usable for People with Cognitive and Learning Disabilities (track), Cognitive Accessibility Roadmap and Gap Analysis (track), Cognitive Accessibility User Research (track). Use when making content usable for people with cognitive and learning disabilities. Triggers: COGA, cognitive accessibility, Making Content Usable.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Making Content Usable for People with Cognitive and Learning Disabilities

This document is for people who make web content (web pages) and web applications. It gives advice on how to make content usable for people with cognitive and learning disabilities . This includes, but is not limited to: cognitive disabilities, learning disabilities (LD), neurodiversity , intellectual disabilities, and specific learning disabilities. This document has content about: people with cognitive and learning disabilities, aims and objectives for usable content, design patterns (ways) to make content usable, including users in design and testing activities, and personas (examples) and user needs. The objectives and patterns presented here provide supplemental guidance beyond the requ

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when making content usable for people with cognitive and learning disabilities.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Making Content Usable for People with Cognitive and Learning Disabilities (default, posture track); Cognitive Accessibility Roadmap and Gap Analysis (default, posture track); Cognitive Accessibility User Research (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1 How to Use this Document.** "It should be noted that all teams should try to involve users with cognitive and learning disabilities throughout the design and development process."
2. **2.3 Building the User into the Development Process.** "Some aspects of making web content and applications usable by people with cognitive and learning disabilities should be dealt with as part of the overall design process."
3. **2.3 Building the User into the Development Process.** "Most organizations should include scope for a user-centered design process."
4. **2.3 Building the User into the Development Process.** "Key parts of this process for people with cognitive and learning disabilities should be: Including the needs of users with cognitive and learning disabilities in the context of user needs and requirements."
5. **3.1.1 Clear Purpose (User Story).** "This user story also includes the following user needs: I need to know what the web site offers, or if I should move on."
6. **3.1.1 Clear Purpose (User Story).** "I need to know what features and content are on this page or if I should move on."
7. **3.6.3 Voice Menus (User Story).** "I need help identifying the right words to say in a voice menu and the words should be the ones I would use."
8. **4.2.3.3 How it Helps.** "Once learned, the elements should be used throughout the site."

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

- [Making Content Usable for People with Cognitive and Learning Disabilities](https://www.w3.org/TR/coga-usable/): Note, coga-usable NOTE-coga-usable-20210429 (Note, 2021-04-29), checked 2026-10-06.
- [Cognitive Accessibility Roadmap and Gap Analysis](https://www.w3.org/TR/coga-gap-analysis/): Working Draft, coga-gap-analysis WD-coga-gap-analysis-20171207 (Working Draft, 2018-12-11), checked 2026-10-06.
- [Cognitive Accessibility User Research](https://www.w3.org/TR/coga-user-research/): First Public Working Draft, coga-user-research WD-coga-user-research-20150115 (First Public Working Draft, 2015-01-15), checked 2026-10-06.
- [Cognitive Accessibility Research Modules](https://www.w3.org/TR/coga-research-modules/): Draft Note, coga-research-modules (Draft Note, 2026-02-05), checked 2026-10-06.
- [Cognitive Accessibility Research Modules - Online Safety and Wellbeing (Algorithms and Data)](https://www.w3.org/TR/coga-safety/): Draft Note, coga-safety (Draft Note, 2026-02-05), checked 2026-10-06.
- [Cognitive Accessibility Research Modules - Supported Decision-Making Online](https://www.w3.org/TR/coga-sdm/): Draft Note, coga-sdm (Draft Note, 2026-02-05), checked 2026-10-06.
- [Cognitive Accessibility Research Modules - Voice Systems and Conversational Interfaces](https://www.w3.org/TR/coga-voice/): Draft Note, coga-voice (Draft Note, 2026-02-05), checked 2026-10-06.
- [Cognitive Accessibility Research Modules - Technology Assisted Indoor Navigation / Wayfinding](https://www.w3.org/TR/coga-wayfinding/): Draft Note, coga-wayfinding (Draft Note, 2026-02-05), checked 2026-10-06.
