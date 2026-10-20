---
name: media-session
description: >-
  Media Session: This specification enables web developers to show customized media metadata on platform UI, customize available platform media controls, and access platform media keys such as hardware keys found on keyboards, headsets, remote controls, and software keys found in notification areas and on lock screens of mobile devices. Covers Media Session (track). Use when exposing media metadata and controls. Triggers: Media Session, navigator.mediaSession.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Media Session

This specification enables web developers to show customized media metadata on platform UI, customize available platform media controls, and access platform media keys such as hardware keys found on keyboards, headsets, remote controls, and software keys found in notification areas and on lock screens of mobile devices.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when exposing media metadata and controls.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Session (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **4.1. Playback State.** "In order to make play and pause actions work properly, the user agent SHOULD be able to determine if a browsing context of the active media session is playing media or not, which is called the guessed playback state ."
2. **4.1. Playback State.** "Other information SHOULD also be considered, such as WebAudio and plugins."
3. **4.1. Playback State.** "When the actual playback state of the active media session changes, the user agent MUST run the media session actions update algorithm ."
4. **4.2. Routing.** "The user agent MUST select at most one of the MediaSession objects to present to the user, which is called the active media session ."
5. **4.2. Routing.** "The selection is up to the user agent and SHOULD be based on preferred user experience."
6. **4.2. Routing.** "Note that the playbackState attribute MUST not affect media session routing."
7. **4.2. Routing.** "Whenever the active media session is changed, the user agent MUST run the media session actions update algorithm and the update metadata algorithm ."
8. **4.3. Metadata.** "Whenever the active media session changes or setting metadata of the active media session , the user agent MUST run the update metadata algorithm ."

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

- [Media Session](https://www.w3.org/TR/mediasession/): Working Draft, mediasession WD-mediasession-20260605 (Working Draft, 2026-06-05), checked 2026-10-06.
