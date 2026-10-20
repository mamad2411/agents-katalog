---
name: cldr
description: >-
  Unicode Locale Data Markup Language (UTS #35): This document describes an XML format ( vocabulary ) for the exchange of structured locale data. Covers UTS #35 LDML. Use when reading CLDR locale data. Triggers: CLDR, LDML, UTS 35.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Unicode Locale Data Markup Language (UTS #35)

This document describes an XML format ( vocabulary ) for the exchange of structured locale data. This format is used in the Unicode Common Locale Data Repository .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading CLDR locale data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UTS #35 LDML (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **U Extension Data Files.** "<!ELEMENT keyword ( key* )> <!ELEMENT key ( type* )> <!ATTLIST key extension NMTOKEN #IMPLIED> <!ATTLIST key name NMTOKEN #REQUIRED> <!ATTLIST key description CDATA #IMPLIED> <!ATTLIST key deprecated ( true | false ) "false"> <!ATTLIST key preferred NMTOKEN #IMPLIED> <!ATTLIST key alias NMTOKEN #IMPLIED> <!ATTLIST key valueType (single | multiple | incremental | any) #IMPLIED > <!ATTLIST key…"
2. **Validity Data.** "<!ELEMENT idValidity (id*) > <!ELEMENT id ( #PCDATA ) > <!ATTLIST id type NMTOKEN #REQUIRED > <!ATTLIST id idStatus NMTOKEN #REQUIRED > The directory common/validity contains machine-readable data for validating the language, region, script, and variant subtags, as well as currency, subdivisions and measure units."
3. **Parent Locales.** "<!ELEMENT parentLocales ( parentLocale* ) > <!ATTLIST parentLocales component NMTOKENS #IMPLIED > <!ELEMENT parentLocale EMPTY > <!ATTLIST parentLocale parent NMTOKEN #REQUIRED > <!ATTLIST parentLocale localeRules NMTOKENS #IMPLIED > <!ATTLIST parentLocale locales NMTOKENS #REQUIRED > When the component does not occur, that is referred to as the ‘main’ component."
4. **Likely Subtags.** "<!ELEMENT likelySubtag EMPTY > <!ATTLIST likelySubtag from NMTOKEN #REQUIRED> <!ATTLIST likelySubtag to NMTOKEN #REQUIRED> There are a number of situations where it is useful to be able to find the most likely language, script, or region."
5. **Language Matching.** "<!ELEMENT languageMatching ( languageMatches* ) > <!ELEMENT languageMatches ( paradigmLocales*, matchVariable*, languageMatch* ) > <!ATTLIST languageMatches type NMTOKEN #REQUIRED > <!ELEMENT languageMatch EMPTY > <!ATTLIST languageMatch desired CDATA #REQUIRED > <!ATTLIST languageMatch supported CDATA #REQUIRED > <!ATTLIST languageMatch percent NMTOKEN #REQUIRED > <!ATTLIST languageMatch…"
6. **XML Format.** "An element that has value attributes MUST NOT also have have child elements."
7. **Element alias.** "<!ELEMENT alias (special*) > <!ATTLIST alias source NMTOKEN #REQUIRED > <!ATTLIST alias path CDATA #IMPLIED> The contents of any element in root can be replaced by an alias, which points to the path where the data can be found."
8. **Introduction.** "Implementations should consider converting LDML data into a more compact format prior to use."

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

- `messageformat`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill messageformat`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [UTS #35 LDML](https://www.unicode.org/reports/tr35/): Unicode Technical Standard, UTS #35 (Unicode Technical Standard, 2026-10-06), checked 2026-10-06.
