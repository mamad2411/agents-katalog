---
name: gs1-digital-link
description: >-
  GS1 Digital Link: Enabling consistent representation of GS1 identification keys within web addresses to link to online information and services Covers GS1 Digital Link URI Syntax. Use when encoding a GS1 identifier in a URI. Triggers: GS1 Digital Link.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# GS1 Digital Link

Enabling consistent representation of GS1 identification keys within web addresses to link to online information and services

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encoding a GS1 identifier in a URI.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: GS1 Digital Link URI Syntax (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Conformance to GS1 Digital Link URI Syntax.** "Applications SHALL NOT assume that a URL that follows the syntax defined in this standard will point to a resolver."
2. **GS1 Digital Link URI Syntax.** "It has no negation option (string SHALL NOT contain “xyz”) and it does not support non-greedy matching."
3. **GS1 Digital Link URI Syntax.** "This means that the value of a GTIN-8, GTIN-12 or GTIN-13 SHALL be prefixed with leading zeroes serving as filler digits to reach a total of 14 digits, exactly as explained in section 2.1.1.10 of the GS1 General Specifications."
4. **GS1 Digital Link URI Syntax.** "Important :For reasons of backwards compatibility, only existing infrastructure for GS1 Digital Link SHOULD continue to support legacy expressions of GS1 Digital Link URIs."
5. **Primary identification key formats.** "gtin-value = 14DIGIT ; GTIN-8, GTIN-12 and GTIN-13 SHALL be expressed as 14 digits, with leading zeroes serving as filler digits itip-value = 14DIGIT 2DIGIT 2DIGIT ; 14 digits then 2 digits then 2 digits gmn-value = 1*25 XCHAR ; 1-25 characters from 82-chr subset cpid-value = 1*30 YCHAR ; 1-30 characters from 39-chr subset gln-value = 13DIGIT ; exactly 13 digits payTo-value = 13DIGIT ; exactly 13…"
6. **Data attributes.** "Data attributes and their values SHALL be expressed via the URI query string as key=value pairs."
7. **Data attributes.** "Where it is necessary to encode more than one GS1 identifier in a single GS1 Digital Link URI, one GS1 identifier SHALL be expressed as the primary identification key (with any relevant key qualifiers) in the path and the remaining GS1 identifier (with any relevant key qualifiers) SHALL be expressed as a data attribute in the query string."
8. **Extension mechanism and reserved keywords.** "Any key=value pairs used for extension data SHALL NOT use all-numeric keys to avoid conflict with existing and future keys used for GS1 Application Identifiers either in terms of semantics or syntax; nor should they be used to express a value (such as a value for net weight) if that value can be expressed using GS1 Application Identifiers as data attributes."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [GS1 Digital Link URI Syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/): Standard, GS1 Digital Link Standard: URI Syntax (Standard, 2026-10-06), checked 2026-10-06.
