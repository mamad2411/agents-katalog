---
name: media-source-extensions
description: >-
  Media Source Extensions: This specification extends HTMLMediaElement [ HTML51 ] to allow JavaScript to generate media streams for playback. Covers Media Source Extensions™ Level 1, Media Source Extensions™ Level 2 (track preview). Use when feeding media segments to a media element. Triggers: Media Source Extensions, MediaSource.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Media Source Extensions

This specification extends HTMLMediaElement [ HTML51 ] to allow JavaScript to generate media streams for playback. Allowing JavaScript to generate streams facilitates a variety of use cases like adaptive streaming and time shifting live streams.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when feeding media segments to a media element.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Source Extensions™ Level 1 (default); Media Source Extensions™ Level 2 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.2 Definitions.** "For video and text, the duration indicates how long the video frame or text SHOULD be displayed."
2. **1.2 Definitions.** "If frames can be decoded out of presentation order , then the decode timestamp MUST be present in or derivable from the byte stream."
3. **1.2 Definitions.** "The user agent MUST run the append error algorithm if this is not the case."
4. **1.2 Definitions.** "Implementations MUST report the actual buffered range, regardless of this allowance."
5. **1.2 Definitions.** "The presentation timestamp in a coded frame indicates when the frame SHOULD be rendered."
6. **1.2 Definitions.** "Implementations MUST support at least 1 MediaSource object with the following configurations: A single SourceBuffer with 1 audio track and/or 1 video track."
7. **1.2 Definitions.** "MediaSource objects MUST support each of the configurations above, but they are only required to support one configuration at a time."
8. **1.2 Definitions.** "The user agent MUST run the append error algorithm if the Track ID is not unique within the initialization segment ."

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

- [Media Source Extensions™](https://www.w3.org/TR/media-source-1/): Recommendation, media-source-1 REC-media-source-20161117 (Recommendation, 2016-11-17), checked 2026-10-06.
- [Media Source Extensions™](https://www.w3.org/TR/media-source-2/): Working Draft, media-source-2 REC-media-source-20161117 (Working Draft, 2026-08-07), checked 2026-10-06.
- [Media Source Extensions Byte Stream Format Registry](https://www.w3.org/TR/mse-byte-stream-format-registry/): Draft Registry, mse-byte-stream-format-registry (Draft Registry, 2026-06-04), checked 2026-10-06.
