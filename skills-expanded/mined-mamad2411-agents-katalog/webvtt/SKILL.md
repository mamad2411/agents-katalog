---
name: webvtt
description: >-
  WebVTT: This specification defines WebVTT, the Web Video Text Tracks format. Covers WebVTT: The Web Video Text Tracks Format Level 1 (build). Use when writing or parsing WebVTT cues. Triggers: WebVTT.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebVTT

This specification defines WebVTT, the Web Video Text Tracks format. Its main use is for marking up external text track resources in connection with the HTML <track> element. WebVTT files provide captions or subtitles for video content, and also text video descriptions [MAUR] , chapters for content navigation, and more generally any form of metadata that is time-aligned with audio or video content.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or parsing WebVTT cues.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebVTT: The Web Video Text Tracks Format Level 1 (default, posture build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY", and "OPTIONAL" in the normative parts of this document are to be interpreted as described in RFC2119."
2. **1.5. Comments in WebVTT.** "Some things to bear in mind: - I was lip-reading, so the cues may not be 100% accurate - I didn't pay too close attention to when the cues should start or end."
3. **2. Conformance.** "[RFC2119] Requirements phrased in the imperative as part of algorithms (such as "strip any leading space characters" or "return false and abort these steps") are to be interpreted with the meaning of the key word ("must", "should", "may", etc) used in introducing the algorithm."
4. **2.1. Conformance classes.** "The user agent must also be conforming implementations of the IDL fragments in this specification, as described in the Web IDL specification."
5. **2.1. Conformance classes.** "The user agent must instead only render the text inside WebVTT caption or subtitle cue text in an appropriate manner and specifically support the color classes defined in § 5 Default classes for WebVTT Caption or Subtitle Cue Components ."
6. **2.1. Conformance classes.** "User agents that support a full CSS engine must therefore limit the CSS styles they apply for WebVTT so as to enable identical rendering without bleeding in extra CSS styles that are beyond the WebVTT specification."
7. **2.1. Conformance classes.** "Conformance checkers Conformance checkers must verify that a WebVTT file conforms to the applicable conformance criteria described in this specification."
8. **2.1. Conformance classes.** "Authoring tools Authoring tools must generate conforming WebVTT files ."

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

- [WebVTT: The Web Video Text Tracks Format](https://www.w3.org/TR/webvtt1/): Candidate Recommendation Draft, webvtt1 CRD-webvtt1-20260520 (Candidate Recommendation Draft, 2026-05-20), checked 2026-10-06.
