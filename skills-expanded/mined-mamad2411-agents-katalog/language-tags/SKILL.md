---
name: language-tags
description: >-
  BCP 47 language tags (RFC 5646, RFC 4647): build, validate and match language tags. Covers RFC 5646 Tags for Identifying Languages, RFC 4647 Matching of Language Tags. Use when matching BCP 47 language tags. Triggers: BCP 47, RFC 5646, language tag.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Tags for Identifying Languages

Tags for Identifying Languages

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when matching BCP 47 language tags.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 5646 Tags for Identifying Languages (default); RFC 4647 Matching of Language Tags (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 5646 § 2.1.1.** "At all times, language tags and their subtags, including private use and extensions, are to be treated as case insensitive: there exist conventions for the capitalization of some of the subtags, but these MUST NOT be taken to carry meaning."
2. **RFC 5646 § 2.2.** "Sequences of private use and extension subtags MUST occur at the end of the sequence of subtags and MUST NOT be interspersed with subtags defined elsewhere in this document."
3. **RFC 5646 § 2.2.3.** "There MUST be at most one script subtag in a language tag, and the script subtag SHOULD be omitted when it adds no distinguishing value to the tag or when the primary or extended language subtag's record in the subtag registry includes a 'Suppress-Script' field listing the applicable script subtag."
4. **RFC 5646 § 2.2.5.** "The same variant subtag MUST NOT be used more than once within a language tag."
5. **RFC 5646 § 2.2.6.** "Each singleton subtag MUST appear at most one time in each tag (other than as a private use subtag)."
6. **RFC 5646 § 2.2.9.** "Users MUST NOT assign language tags that use subtags that do not appear in the registry other than in private use sequences (such as the subtag 'personal' in the tag "en-x-personal")."
7. **RFC 5646 § 4.4.1.** "Protocols or specifications that specify limited buffer sizes for language tags MUST allow for language tags of at least 35 characters."
8. **RFC 5646 § 4.5.** "Since a particular language tag can be used by many processes, language tags SHOULD always be created or generated in canonical form."
9. **RFC 4647 § 2.** "Matching of language tags to language ranges MUST be done in a case-insensitive manner."
10. **RFC 4647 § 3.** "Protocols and specifications requiring conformance to this specification MUST clearly indicate the particular mechanism used in selecting or matching language tags."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
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

- [RFC 5646 Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646.html): BEST CURRENT PRACTICE, RFC 5646 (BEST CURRENT PRACTICE, September ), checked 2026-10-06.
- [RFC 4647 Matching of Language Tags](https://www.rfc-editor.org/rfc/rfc4647.html): BEST CURRENT PRACTICE, RFC 4647 (BEST CURRENT PRACTICE, September ), checked 2026-10-06.
