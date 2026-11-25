---
name: html-media-capture
description: >-
  HTML Media Capture: The HTML Media Capture specification defines an HTML form extension that facilitates user access to a device's media capture mechanism , such as a camera, or microphone, from within a file upload control. Covers HTML Media Capture. Use when capturing media from a file input. Triggers: HTML Media Capture, capture attribute.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# HTML Media Capture

The HTML Media Capture specification defines an HTML form extension that facilitates user access to a device's media capture mechanism , such as a camera, or microphone, from within a file upload control.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when capturing media from a file input.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: HTML Media Capture (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words MUST , MUST NOT , and SHOULD are to be interpreted as described in [ RFC2119 ]."
2. **5..** "The capture IDL attribute MUST reflect the respective content attribute of the same name."
3. **5..** "When the capture attribute is specified, the user agent SHOULD invoke a file picker of the specific capture control type ."
4. **5..** "When the capture attribute is specified, the user agent MUST NOT save the captured media to any data storage, local or remote."
5. **5..** "If the accept attribute's value is set to a MIME type that has no associated capture control type , the user agent MUST act as if there was no capture attribute."
6. **2. Conformance.** "Implementations that use ECMAScript to implement the APIs defined in this specification must implement them in a manner consistent with the ECMAScript Bindings defined in the Web IDL specification [ WEBIDL-1 ], as this specification uses that specification and terminology."
7. **4..** "Implementors should take care to prevent additional leakage of privacy-sensitive data from captured media."

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

- [HTML Media Capture](https://www.w3.org/TR/html-media-capture/): Recommendation, html-media-capture REC-html-media-capture-20180201 (Recommendation, 2018-02-01), checked 2026-10-06.
