---
name: media-capabilities
description: >-
  Media Capabilities: This specification intends to provide APIs to allow websites to make an optimal decision when picking media content for the user. Covers Media Capabilities (track). Use when querying decoding or encoding support. Triggers: mediaCapabilities, Media Capabilities.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Media Capabilities

This specification intends to provide APIs to allow websites to make an optimal decision when picking media content for the user. The APIs will expose information about the decoding and encoding capabilities for a given format but also output capabilities to find the best match based on the device’s display.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when querying decoding or encoding support.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Capabilities (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1.1. MediaConfiguration.** "For a MediaConfiguration to be a valid MediaConfiguration , all of the following conditions MUST be true: audio and/or video MUST exist ."
2. **2.1.1. MediaConfiguration.** "audio MUST be a valid audio configuration if it exists ."
3. **2.1.1. MediaConfiguration.** "video MUST be a valid video configuration if it exists ."
4. **2.1.1. MediaConfiguration.** "For a MediaDecodingConfiguration to be a valid MediaDecodingConfiguration , all of the following conditions MUST be true: It MUST be a valid MediaConfiguration ."
5. **2.1.1. MediaConfiguration.** "If keySystemConfiguration exists : The type MUST be media-source or file ."
6. **2.1.1. MediaConfiguration.** "If keySystemConfiguration.audio exists , audio MUST also exist ."
7. **2.1.1. MediaConfiguration.** "If keySystemConfiguration.video exists , video MUST also exist ."
8. **2.1.1. MediaConfiguration.** "For a MediaDecodingConfiguration to describe [ENCRYPTED-MEDIA] , a keySystemConfiguration MUST exist ."

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

- [Media Capabilities](https://www.w3.org/TR/media-capabilities/): Working Draft, media-capabilities WD-media-capabilities-20260609 (Working Draft, 2026-06-09), checked 2026-10-06.
