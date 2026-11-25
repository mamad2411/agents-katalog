---
name: web-share
description: >-
  Web Share API: This specification defines an API for sharing text, links and other content to an arbitrary destination of the user's choice. Covers Web Share API. Use when sharing data from a page to another app. Triggers: Web Share, navigator.share.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Web Share API

This specification defines an API for sharing text, links and other content to an arbitrary destination of the user's choice. The available share targets are not specified here; they are provided by the user agent. They could, for example, be apps, websites or contacts.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sharing data from a page to another app.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Web Share API (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1.2.** "The user agent SHOULD show intermediary UI through which the user can verify the shared content (if the OS-level UI does not provide this functionality)."
2. **3..** "However, it MUST have the ability to receive data that matches some or all of the concepts exposed in ShareData ."
3. **3..** "To convert data to a format suitable for ingestion into the target , the user agent SHOULD map the members of ShareData onto equivalent concepts in the target."
4. **7. Conformance.** "The key words MAY , MUST , OPTIONAL , and SHOULD in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
5. **2.1.2.** "Content that is previewed and authorized by a user might be safe to forward, however it is not always possible for a person to identify when information should be confidential, so forwarding any content presents a risk."
6. **2.1.3.** "If an object contains additional members, it should be destructured to only test the defined members individually."

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

- [Web Share API](https://www.w3.org/TR/web-share/): Recommendation, web-share REC-web-share-20230530 (Recommendation, 2023-05-30), checked 2026-10-06.
