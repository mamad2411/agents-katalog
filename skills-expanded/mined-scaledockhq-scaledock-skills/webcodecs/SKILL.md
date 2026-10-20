---
name: webcodecs
description: >-
  WebCodecs: This specification defines interfaces to codecs for encoding and decoding of audio, video, and images. Covers WebCodecs (track). Use when encoding or decoding media in the browser. Triggers: WebCodecs, VideoDecoder, AudioEncoder.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebCodecs

This specification defines interfaces to codecs for encoding and decoding of audio, video, and images. This specification does not specify or require any particular codec or method of encoding or decoding. The purpose of this specification is to provide JavaScript interfaces to implementations of existing codec technology developed elsewhere. Implementers are free to support any combination of codecs or none at all.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encoding or decoding media in the browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebCodecs (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Definitions.** "The underlying codec implementation MUST emit all outputs in response to a flush."
2. **1. Definitions.** "Such resources MAY be quickly exhausted and SHOULD be released immediately when no longer in use."
3. **3.1. Internal Slots.** "[[key chunk required]] A boolean indicating that the next chunk passed to decode() MUST describe a key chunk as indicated by [[type]] ."
4. **3.5. Methods.** "Implementers SHOULD inspect the chunk ’s [[internal data]] to verify that it is truly a key chunk ."
5. **4.1. Internal Slots.** "[[key chunk required]] A boolean indicating that the next chunk passed to decode() MUST describe a key chunk as indicated by type ."
6. **5.6. Algorithms.** "The User Agent MUST ensure that the provided description could be used to correctly decode output."
7. **6.6. Algorithms.** "The User Agent MUST ensure that the configuration is completely described such that outputConfig could be used to correctly decode output ."
8. **7.4. Codec String.** "A valid codec string MUST meet the following conditions."

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

- [WebCodecs](https://www.w3.org/TR/webcodecs/): Working Draft, webcodecs WD-webcodecs-20260921 (Working Draft, 2026-09-21), checked 2026-10-06.
- [WebCodecs Codec Registry](https://www.w3.org/TR/webcodecs-codec-registry/): Draft Registry, webcodecs-codec-registry (Draft Registry, 2026-09-24), checked 2026-10-06.
