---
name: file-api
description: >-
  File API: This specification provides an API for representing file objects in web applications, as well as programmatically selecting them and accessing their data. Covers File API (track). Use when reading local files in the browser. Triggers: File API, Blob, FileReader.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# File API

This specification provides an API for representing file objects in web applications, as well as programmatically selecting them and accessing their data. This includes: A FileList interface, which represents an array of individually selected files from the underlying system. The user interface for selection can be invoked via <input type="file"> , i.e. when the input element is in the File Upload state [HTML] . A Blob interface, which represents immutable raw binary data, and allows access to ranges of bytes within the Blob object as a separate Blob . A File interface, which includes readonly informational attributes about a file such as its name and the date of the last modification (on di

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading local files in the browser.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: File API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **1. Introduction.** "Web applications should have the ability to manipulate as wide as possible a range of user input, including files that a user may wish to upload to a remote server or manipulate inside a rich web application."
3. **1. Introduction.** "File or Blob reads should happen asynchronously on the main thread, with an optional synchronous API used within threaded web applications."
4. **2. Terminology and Algorithms.** "When this specification says to terminate an algorithm the user agent must terminate the algorithm after finishing the step it is on."
5. **2. Terminology and Algorithms.** "It must act as follows: Let originalSize be blob ’s size ."
6. **2. Terminology and Algorithms.** "The start parameter, if non-null, is a value for the start point of a slice blob call, and must be treated as a byte-order position, with the zeroth position representing the first byte."
7. **2. Terminology and Algorithms.** "User agents must normalize start according to the following: If start is null, let relativeStart be 0."
8. **2. Terminology and Algorithms.** "User agents must normalize end according to the following: If end is null, let relativeEnd be originalSize ."

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

- [File API](https://www.w3.org/TR/FileAPI/): Working Draft, FileAPI WD-FileAPI-20260912 (Working Draft, 2026-09-12), checked 2026-10-06.
