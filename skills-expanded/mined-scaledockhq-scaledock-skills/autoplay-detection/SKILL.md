---
name: autoplay-detection
description: >-
  Autoplay Policy Detection: This specification provides web developers the ability to detect if automatically starting the playback of a media file is allowed in different situations. Covers Autoplay Policy Detection (track). Use when detecting whether autoplay is allowed. Triggers: autoplay, navigator.getAutoplayPolicy.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Autoplay Policy Detection

This specification provides web developers the ability to detect if automatically starting the playback of a media file is allowed in different situations.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when detecting whether autoplay is allowed.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Autoplay Policy Detection (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 2.2.1.** "When getAutoplayPolicy(type) method is called, the user agent MUST run the following steps:"
2. **§ 2.2.1.** "If type is mediaelement, return a result that represents the current status for HTMLMediaElement and its extensions, such as HTMLVideoElement and HTMLAudioElement, which exist in the document contained in the Window object associated with the queried Navigator object."
3. **§ 2.2.1.** "If type is audiocontext, return a result that represents the current status for AudioContext, which exist in the document contained in the Window object associated with the queried Navigator object."
4. **§ 2.2.2.** "In addition, if authors make an inaudible media element audible right after it starts playing, then it is recommended for a user agent to pause that media element immediately because it’s no longer inaudible."
5. **§ 2.2.2.** "If the result of querying by a media type is different from the result of querying by an element, authors should take the latter one as the correct result."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Autoplay Policy Detection](https://www.w3.org/TR/autoplay-detection/): Working Draft, autoplay-detection WD-autoplay-detection-20250904 (Working Draft, 2025-09-04), checked 2026-10-06.
