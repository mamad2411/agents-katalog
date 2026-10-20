---
name: swid
description: >-
  SWID tags: identify installed software with ISO/IEC 19770-2 tags, following NIST IR 8060. Covers NIST IR 8060. Use when tagging software with SWID. Triggers: SWID.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SWID

Software identification (SWID) tags as profiled by NIST IR 8060, Guidelines for the Creation of Interoperable Software Identification (SWID) Tags: numbered guidelines for corpus, primary, patch and supplemental tags on top of ISO/IEC 19770-2:2015.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when tagging software with SWID.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: authoritative tag creator (software provider), non-authoritative tag creator (discovery tool), or tag consumer.
- Target version: NIST IR 8060 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **GEN-1.** "When producing SWID tags, tag creators MUST produce SWID tags that conform to all requirements defined in the ISO/IEC 19770-2:2015 specification."
2. **GEN-4.** "Every `<Entity>` element MUST provide an explicit (i.e., non-default) @regid attribute value."
3. **GEN-19.** "Whenever a `<Payload>` element is included in a tag, every `<File>` element contained therein MUST provide a hash value based on the SHA-256 hash function."
4. **GEN-26.** "When it is necessary to update a tag to correct errors in or add data elements to that tag, the tag's `<SoftwareIdentity>` @tagVersion attribute MUST be changed."
5. **PRI-1.** "To indicate that a tag is a primary tag, the `<SoftwareIdentity>` @corpus, @patch, and @supplemental attributes MUST be set to "false"."

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

- [NIST IR 8060](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8060.pdf): NIST IR, NIST IR 8060, fetched 2026-10-06 (NIST IR, 2026-10-06), checked 2026-10-06.
