---
name: encoding
description: >-
  Encoding: The Encoding Standard defines encodings and their JavaScript API. Covers Encoding Living Standard. Use when encoding or decoding text. Triggers: TextEncoder, TextDecoder.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Encoding

The Encoding Standard defines encodings and their JavaScript API.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encoding or decoding text.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Encoding Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Encoding.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **3. Terminology.** "For logical right shifts operands must have at least twenty-one bits precision."
3. **4.2. Names and labels.** "The table below lists all encodings and their labels user agents must support."
4. **4.2. Names and labels.** "User agents must not support any other encodings or labels ."
5. **4.2. Names and labels.** "Authors must use the UTF-8 encoding and must use its ( ASCII case-insensitive ) " utf-8 " label to identify it."
6. **4.2. Names and labels.** "New protocols and formats, as well as existing formats deployed in new contexts, must use the UTF-8 encoding exclusively."
7. **4.2. Names and labels.** "If these protocols and formats need to expose the encoding ’s name or label , they must expose it as " utf-8 "."
8. **7. API.** "Browser user agents must support this API."

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

- [Encoding Living Standard](https://encoding.spec.whatwg.org/review-drafts/2025-06/): Review Draft, Review Draft 2025-06 (Review Draft, 2025-06), checked 2026-10-06.
