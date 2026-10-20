---
name: png
description: >-
  Portable Network Graphics (PNG): This document describes PNG (Portable Network Graphics), an extensible file format for the lossless , portable, well-compressed storage of static and animated raster images. Covers Portable Network Graphics (PNG) Specification (Third Edition) Level 3. Use when writing or decoding PNG. Triggers: PNG, PNG 3.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Portable Network Graphics (PNG)

This document describes PNG (Portable Network Graphics), an extensible file format for the lossless , portable, well-compressed storage of static and animated raster images. PNG provides a patent-free replacement for GIF and can also replace many common uses of TIFF. Indexed-color , greyscale , and truecolor images are supported, plus an optional alpha channel. Sample depths range from 1 to 16 bits. PNG is designed to work well in online viewing applications, such as the World Wide Web, so it is fully streamable with a progressive display option. PNG is robust, providing both full file integrity checking and simple detection of common transmission errors. Also, PNG can store color space data

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or decoding PNG.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Portable Network Graphics (PNG) Specification (Third Edition) Level 3 (default); Portable Network Graphics (PNG) Specification (Second Edition) Level 2 (legacy: read and upgrade, never author); Portable Network Graphics (PNG) Specification Level 1 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **5.7.1 General.** "All chunks, private and public, SHOULD be listed at [ PNG-EXTENSIONS ]."
2. **5.7.2 Defining public chunks.** "A proposed public chunk type SHALL not be used in publicly available software or datastreams until defined as such."
3. **5.7.3 Defining private chunks.** "A private chunk SHOULD NOT be defined merely to carry textual information of interest to a human user."
4. **5.7.3 Defining private chunks.** "Instead iTXt chunk SHOULD BE used and corresponding keyword SHOULD BE used and a suitable keyword defined."
5. **5.7.3 Defining private chunks.** "If a private chunk type is used, additional identifying information SHOULD BE be stored at the beginning of the chunk data to further reduce the risk of conflicts."
6. **5.7.3 Defining private chunks.** "An ancillary chunk type, not a critical chunk type, SHOULD be used for all private chunks that store information that is not absolutely essential to view the image."
7. **5.7.3 Defining private chunks.** "Private critical chunks SHOULD NOT be defined because PNG datastreams containing such chunks are not portable, and SHOULD NOT be used in publicly available software or datastreams."
8. **5.7.3 Defining private chunks.** "If a private critical chunk is essential for an application, it SHOULD appear near the start of the datastream, so that a standard decoder need not read very far before discovering that it cannot handle the datastream."

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

- [Portable Network Graphics (PNG) Specification (Third Edition)](https://www.w3.org/TR/png-3/): Recommendation, png-3 REC-png-3-20250624 (Recommendation, 2025-06-24), checked 2026-10-06.
- [Portable Network Graphics (PNG) Specification (Second Edition)](https://www.w3.org/TR/PNG/): Recommendation, png-2 REC-png-3-20250624 (Recommendation, 2003-11-10), checked 2026-10-06.
