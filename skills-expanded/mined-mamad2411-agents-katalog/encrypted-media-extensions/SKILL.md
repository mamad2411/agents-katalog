---
name: encrypted-media-extensions
description: >-
  Encrypted Media Extensions: This proposal extends HTMLMediaElement [ HTML51 ] providing APIs to control playback of encrypted content. Covers Encrypted Media Extensions Level 1, Encrypted Media Extensions Level 2 (track preview). Use when playing encrypted media. Triggers: EME, requestMediaKeySystemAccess.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Encrypted Media Extensions

This proposal extends HTMLMediaElement [ HTML51 ] providing APIs to control playback of encrypted content. The API supports use cases ranging from simple clear key decryption to high value video (given an appropriate user agent implementation). License/key exchange is controlled by the application, facilitating the development of robust playback applications supporting a range of content decryption and protection technologies. This specification does not define a content protection or Digital Rights Management system. Rather, it defines a common API that may be used to discover, select and interact with such systems as well as with simpler content encryption systems. Implementation of Digita

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when playing encrypted media.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Encrypted Media Extensions Level 1 (default); Encrypted Media Extensions Level 2 (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Definitions.** "User agents MUST support the Common Key Systems ."
2. **2. Definitions.** "Other MediaKeys objects, CDM instances, and media elements MUST NOT access the key session or use its key(s)."
3. **2. Definitions.** "All license(s) and key(s) associated with a Key Session which have not been explicitly stored MUST be destroyed when the Key Session is closed."
4. **2. Definitions.** "Key IDs MUST be unique within a session."
5. **2. Definitions.** "Each Session ID SHALL be unique within the browsing context in which it was created."
6. **2. Definitions.** "algorithm returns true , Session IDs MUST be unique within the origin over time, including across browsing sessions."
7. **2. Definitions.** "(The same key may be present in multiple sessions.) Such keys MUST only be provided to the CDM via an update() call."
8. **2. Definitions.** "(They may later be loaded by load() as part of the stored session data.) Note Authors SHOULD encrypt each set of stream(s) that requires enforcement of a meaningfully different policy with a distinct key (and key ID)."

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

- [Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media-1/): Recommendation, encrypted-media-1 REC-encrypted-media-20170918 (Recommendation, 2017-09-18), checked 2026-10-06.
- [Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media-2/): Working Draft, encrypted-media-2 REC-encrypted-media-20170918 (Working Draft, 2026-07-07), checked 2026-10-06.
- [Encrypted Media Extensions Initialization Data Format Registry](https://www.w3.org/TR/eme-initdata-registry/): Draft Registry, eme-initdata-registry (Draft Registry, 2026-07-07), checked 2026-10-06.
- [Encrypted Media Extensions Stream Format Registry](https://www.w3.org/TR/eme-stream-registry/): Draft Registry, eme-stream-registry (Draft Registry, 2026-07-07), checked 2026-10-06.
