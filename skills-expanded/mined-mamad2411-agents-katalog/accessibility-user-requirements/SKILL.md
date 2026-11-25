---
name: accessibility-user-requirements
description: >-
  W3C accessibility user requirements: This document presents the accessibility requirements users with disabilities have with respect to audio and video on the web. Covers Media Accessibility User Requirements (track), XR Accessibility User Requirements (track), RTC Accessibility User Requirements (track), Collaboration Tools Accessibility User Requirements (track), Synchronization Accessibility User Requirements (track), Natural Language Interface Accessibility User Requirements (track). Use when gathering user requirements for media, XR, RTC, collaboration, synchronization or natural language interfaces. Triggers: MAUR, XAUR, RAUR, CTAUR, SAUR, NAUR.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# W3C accessibility user requirements

This document presents the accessibility requirements users with disabilities have with respect to audio and video on the web. It first provides an introduction to the needs of users with disabilities in relation to audio and video. Then it explains what alternative content technologies have been developed to help such users gain access to the content of audio and video. A third section explains how these content technologies fit in the larger picture of accessibility, both technically within a web user agent and from a production process point of view. This document is most explicitly not a collection of baseline user agent or authoring tool requirements. It is important to recognize that n

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when gathering user requirements for media, XR, RTC, collaboration, synchronization or natural language interfaces.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Accessibility User Requirements (default, posture track); XR Accessibility User Requirements (default, posture track); RTC Accessibility User Requirements (default, posture track); Collaboration Tools Accessibility User Requirements (default, posture track); Synchronization Accessibility User Requirements (default, posture track); Natural Language Interface Accessibility User Requirements (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.8 Sign translation.** "Acknowledging that not all devices will be capable of handling multiple video streams, this is a SHOULD requirement for browsers where hardware is capable of support."
2. **3.7 Requirements on the use of the viewport.** "It is also a " SHOULD " level requirement, since it does not account for limitations of various devices."
3. **1.2 Visual: Low vision.** "This means that they will only be viewing a portion of the screen, and so must manage tracking media content via their AT ."
4. **1.2 Visual: Low vision.** "They may be using an AT that adjusts all the colors of the screen, such as inverting the colors, so the media content must be viewable through the AT ."
5. **1.7 Physical impairment.** "The media player must be usable with only a keyboard, including access to all player controls and methods for selecting alternative content."
6. **1.8 Cognitive disabilities.** "Individuals with some conditions may process information aurally better than by reading text; therefore, information that is presented as text embedded in a video should also be available as audio descriptions."
7. **1.8 Cognitive disabilities.** "Overall, the media experience for people on the autism spectrum should be customizable and well designed so as to not be overwhelming."
8. **1.8 Cognitive disabilities.** "Care must be taken to present a media experience that focuses on the purpose of the content and provides alternative content in a clear, concise manner."

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

- [Media Accessibility User Requirements](https://www.w3.org/TR/media-accessibility-reqs/): Note, media-accessibility-reqs NOTE-media-accessibility-reqs-20151203 (Note, 2015-12-03), checked 2026-10-06.
- [XR Accessibility User Requirements](https://www.w3.org/TR/xaur/): Note, xaur NOTE-xaur-20210825 (Note, 2021-08-25), checked 2026-10-06.
- [RTC Accessibility User Requirements](https://www.w3.org/TR/raur/): Note, raur NOTE-raur-20210525 (Note, 2021-05-25), checked 2026-10-06.
- [Collaboration Tools Accessibility User Requirements](https://www.w3.org/TR/ctaur/): Note, ctaur NOTE-ctaur-20250121 (Note, 2025-01-21), checked 2026-10-06.
- [Synchronization Accessibility User Requirements](https://www.w3.org/TR/saur/): Note, saur NOTE-saur-20230628 (Note, 2023-06-28), checked 2026-10-06.
- [Natural Language Interface Accessibility User Requirements](https://www.w3.org/TR/naur/): Draft Note, naur DNOTE-naur-20220903 (Draft Note, 2022-09-03), checked 2026-10-06.
