---
name: act-rules-format
description: >-
  Accessibility Conformance Testing (ACT) Rules Format: Accessibility Conformance Testing (ACT) Rules Format 1.1 defines a format for writing accessibility test rules. Covers Accessibility Conformance Testing (ACT) Rules Format 1.1. Use when writing or running an ACT rule. Triggers: ACT Rules Format, accessibility conformance testing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Accessibility Conformance Testing (ACT) Rules Format

Accessibility Conformance Testing (ACT) Rules Format 1.1 defines a format for writing accessibility test rules. The test rules can be used for developing automated testing tools and manual testing methodologies. This document provides a common format that allows anyone involved in accessibility testing to document and share their testing procedures in a robust and understandable manner. This enables transparency and harmonization of testing methods, including methods implemented by accessibility test tools.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or running an ACT rule.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Accessibility Conformance Testing (ACT) Rules Format 1.1 (default); Accessibility Conformance Testing (ACT) Rules Format 1.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Document conventions.** "The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in the normative parts of this document are to be interpreted as described in RFC 2119."
2. **4. ACT Rule Structure.** "An ACT Rule must consist of at least the following items: Descriptive Title Rule Identifier Rule Description Rule Type Accessibility Requirements Mapping Rule Input , which is one of the following: Input Aspects (for atomic rules) OR Input Rules (for composite rules) Applicability Expectations Background Assumptions Accessibility Support Related Rules (optional) Other Resources (optional)…"
3. **4. ACT Rule Structure.** "However, ACT Rules must be written in a document that conforms to the Web Content Accessibility Guidelines [WCAG22] or a comparable accessibility standard."
4. **4. ACT Rule Structure.** "If any example contains accessibility issues listed in WCAG 2.2 Section 5.2.5 Non-Interference , users must be warned of this in advance."
5. **4. ACT Rule Structure.** "ACT Rules should use a localizable format, such that a rule can contain multiple language representations or so that translations of the rule can be created."
6. **4.1. Rule Identifier.** "An ACT Rule must have an identifier that is unique within its ruleset."
7. **4.1. Rule Identifier.** "Identifiers that are also used as filenames; They include a technology directory, followed by a handle that includes an element name or attribute: html+svg/video-alternative html+svg/meta-no-refresh html+svg/unique-id In addition to the identifier, each new release of an ACT Rule must be versioned with either a date or a number."
8. **4.1. Rule Identifier.** "A reference to the previous version of that rule must be available."

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

- `wcag`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill wcag`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Accessibility Conformance Testing (ACT) Rules Format 1.1](https://www.w3.org/TR/act-rules-format-1.1/): Recommendation, act-rules-format-1.1 REC-act-rules-format-1.1-20260205 (Recommendation, 2026-02-05), checked 2026-10-06.
- [Accessibility Conformance Testing (ACT) Rules Format 1.0](https://www.w3.org/TR/act-rules-format-1.0/): Recommendation, act-rules-format-1.0 REC-act-rules-format-1.0-20191031 (Recommendation, 2019-10-31), checked 2026-10-06.
