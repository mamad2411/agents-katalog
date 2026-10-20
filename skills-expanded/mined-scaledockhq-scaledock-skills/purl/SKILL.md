---
name: purl
description: >-
  Package URL (purl) ECMA-427 1st Edition: build, parse, validate and normalize
  pkg:type/namespace/name@version?qualifiers#subpath identifiers, with the
  per-component percent-encoding and case rules, the registered PURL type
  definitions (npm, pypi, maven, golang, cargo, nuget, gem, docker, oci, github,
  deb, rpm, generic and the rest) and their normalizations, the recommended
  qualifiers (repository_url, download_url, vcs_url, file_name, checksum, vers),
  and VERS 1.2 version ranges (vers:npm/>=1.0.0|<2.0.0). Covers ECMA-427 1st
  Edition (purl-spec 1.0.1, current), the ECMA-427 2nd Edition draft (preview,
  track) and upgrades from the pre-ECMA purl-spec text. Use when emitting purls
  in an SBOM, vulnerability advisory or dependency graph, writing or reviewing a
  purl parser or builder, mapping package coordinates to purls, comparing purls,
  or expressing affected version ranges. Triggers: purl, package-url, pkg:,
  ECMA-427, PURL type, canonical purl, qualifiers, vers:, version range
  specifier.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Package URL (purl)

Package-URL (PURL) is a URL string that identifies a software package independently of its ecosystem or distribution channel. Ecma TC54 publishes the core syntax as ECMA-427; the package-url community maintains the registered PURL type definitions, the implementation guides, the test suite, and the companion VERS version range specification. With this skill the agent builds, parses, validates and compares canonical purls, and writes VERS ranges.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: builder (emits purls, for example an SBOM generator), parser or validator (reads purls), or both. VERS producer or consumer if version ranges are in scope.
- Ecosystems: which PURL types are involved (npm, pypi, maven, …). Each registered type adds its own rules.
- Strictness: strict (reject anything non-canonical, used by validators and test `required` cases) or lenient (accept and normalize malformed input on a best-effort basis, never emit it).
- Target version: ECMA-427 1st Edition (default; purl-spec release 1.0.1 carries the type definitions and tests). ECMA-427 2nd Edition is a preview (posture: track): read it to prepare, emit nothing that only it allows. The purl-spec pre-ECMA text is legacy: read purls written to it and upgrade them, never author against it. VERS 1.2 is the current line of the separately versioned VERS spec (posture: build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the Ecma ECMA-427 page for a new edition, the purl-spec and vers-spec releases for a new tag, and the `types/` folder for new or changed types, and update the pins.

## Invariants

1. **Seven components, fixed order.** `scheme:type/namespace/name@version?qualifiers#subpath`; scheme, type and name are required; there is no URL authority (no user, password, host or port) (ECMA-427 § 5, § 5.1).
2. **Scheme is `pkg` followed by an unencoded `:`.** Builders never emit `pkg://`; parsers accept and strip slashes after `pkg:` (1st Edition § 5.6.1: shall; 2nd Edition draft: should).
3. **Type is lowercase ASCII letters, digits, `.` and `-`, starts with a letter, never percent-encoded** (§ 5.6.2).
4. **Encode per component, never the whole string.** Percent-encode the UTF-8 bytes of every character outside the alphanumerics and `.-_~`; never encode those, separators used as separators, or the colon `:` anywhere; a space is `%20` (§ 5.4).
5. **Namespace and subpath segments are non-empty after decoding and contain no `/`;** subpath segments are never `.` or `..`; leading and trailing slashes are not significant (§ 5.6.3, § 5.6.7).
6. **Qualifier keys are lowercase ASCII `[a-z0-9._-]`, start with a letter, are unique and never encoded;** a pair with an empty value is the same as no pair; values are percent-encoded (§ 5.6.6).
7. **Version is an opaque string.** Compare or sort versions only with the type's own rules or through VERS (§ 5.6.5; purl-spec FAQ, Version).
8. **Registered types win.** A purl with a registered type that breaks that type's definition is invalid; an unregistered type that follows § 5.6.2 is valid with a warning (2nd Edition draft § 5.7, test suite `required` group).
9. **Type-level case and normalization rules apply.** When a component's `case_sensitive` is `false`, the form is lowercased; `normalization_rules` are applied by code (ECMA-427 Clause 6).
10. **Builders emit canonical form only.** Lenient input is accepted by parsers, never produced (purl-spec lenient grammar).
11. **A VERS is `vers:<type>/<constraints>`** with `|`-separated constraints sorted by version, unique versions, and a valid comparator sequence; `*` stands alone (VERS § 5.3, § 5.4).

## Workflow

1. **Pick the version.** Use ECMA-427 1st Edition with the type definitions and tests at purl-spec 1.0.1 or later. If input comes from the pre-ECMA purl-spec era, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded, and it is not the legacy or preview line.
2. **Map the package to components.** Look up the registered type; fill namespace, name, version, qualifiers and subpath from the ecosystem's native coordinates (`native_name`), respecting the type's required and prohibited components.
   -> [`references/types.md`](references/types.md)
   ✓ Every required component is present, no prohibited component is set, and the type is registered (or the warning is surfaced).
3. **Normalize per type.** Apply `case_sensitive: false` lowercasing and every `normalization_rules` entry (for example pypi `_` to `-`), then the core rules.
   -> [`references/types.md`](references/types.md)
   ✓ The components equal what the type's tests expect, such as `pkg:pypi/django-package@1.11.1.dev1` for `Django_package`.
4. **Choose qualifiers sparingly.** Use only the keys needed for identification or location; prefer the recommended keys and the type's own keys.
   -> [`references/types.md`](references/types.md)
   ✓ No key duplicates information in another component, and `vers` is never combined with a version.
5. **Build the string.** Follow the build algorithm: lowercase scheme and type, encode each segment, sort qualifiers by key, drop empty values and empty subpath segments.
   -> [`references/parsing-and-building.md`](references/parsing-and-building.md), [`references/syntax-and-encoding.md`](references/syntax-and-encoding.md)
   ✓ The output matches the canonical grammar, and building the parsed result returns the same string.
6. **Parse and validate.** Parse right to left, decode each component once, apply type normalization, and reject what the standard rejects.
   -> [`references/parsing-and-building.md`](references/parsing-and-building.md)
   ✓ The implementation passes the `required` cases of `tests/spec/` and `tests/types/`; `recommended` cases pass if lenient parsing is offered.
7. **Express ranges with VERS** (only when version ranges are needed). Write `vers:<type>/…` with sorted constraints, or put it in the `vers` qualifier with no version.
   -> [`references/vers.md`](references/vers.md)
   ✓ The VERS parses, its constraints are sorted and unique, and its comparator sequence is valid.
8. **Upgrade** (only when asked). Re-normalize stored pre-ECMA purls with the 1st Edition rules: re-encode, lowercase keys, drop `+` from types, encode `,` in checksums.
   -> [`references/versions.md`](references/versions.md)
   ✓ Every upgraded purl round-trips through a 1st Edition parser and builder unchanged and identifies the same package.

## Verify before done

- [ ] Every emitted purl starts with `pkg:` (no slashes) and uses a lowercase type (§ 5.6.1, § 5.6.2).
- [ ] No component is encoded as a whole string; alphanumerics, `.-_~` and `:` are never encoded; `/` inside a qualifier value is `%2F`; space is `%20` (§ 5.4).
- [ ] Qualifiers are lowercase, unique, non-empty, and sorted by key (§ 5.6.6; how to build).
- [ ] Subpath has no empty, `.` or `..` segments and no leading or trailing slash (§ 5.6.7).
- [ ] Type-specific requirements, case rules and normalizations are applied for every registered type used (Clause 6; `types/`).
- [ ] Parsers and builders pass the purl-spec test suite `required` cases.
- [ ] VERS constraints are sorted and unique, use bare versions or `<`, `<=`, `>`, `>=`, `!=` (never a leading `=`), and `*` only alone (VERS § 5.3.3, § 5.4).
- [ ] Nothing only the 2nd Edition draft allows (schema 1.1 `registered_values`, `recommended` qualifier requirement) is relied on for conformance.

## Reference index

- **`references/versions.md`**: ECMA-427 1st Edition, the 2nd Edition draft, the pre-ECMA purl-spec, VERS 1.2; what changed and the upgrade steps. Load for steps 1 and 8.
- **`references/syntax-and-encoding.md`**: components, permitted and separator characters, percent-encoding, case folding, per-component rules, the ABNF, and common mistakes. Load for steps 5 and 6.
- **`references/parsing-and-building.md`**: the parse and build algorithms, lenient parsing, equivalence, and the test suite. Load for steps 5 and 6.
- **`references/types.md`**: the type definition schema, the registered types with their namespace, case and normalization rules, and the recommended qualifiers. Load for steps 2 to 4.
- **`references/vers.md`**: VERS syntax, comparators, validation, containment and VERS types. Load for step 7.

## Related skills

- `cyclonedx` for the `purl` field of CycloneDX components: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `spdx` for purl as an SPDX external reference or package identifier: `npx skills add ScaleDockHQ/scaledock-skills --skill spdx`.
- `osv` for purl and version ranges in OSV vulnerability records: `npx skills add ScaleDockHQ/scaledock-skills --skill osv`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ECMA-427: Package-URL (PURL) specification](https://ecma-international.org/publications-and-standards/standards/ecma-427/): Ecma Standard, 1st edition, December 2025, checked 2026-10-05.
- [ECMA-427 1st Edition source text](https://github.com/Ecma-TC54/ECMA-427/blob/v1.0/spec.html): Ecma Standard source, tag v1.0 (dated 2025-12-06), checked 2026-10-05.
- [ECMA-427 2nd Edition draft source text](https://github.com/Ecma-TC54/ECMA-427/blob/main/spec.html): draft (status: draft, dated 2026-12-08), main at 33b680c (2026-09-30), checked 2026-10-05. Draft posture: track.
- [ECMA-427 2nd Edition release notes](https://github.com/package-url/purl-spec/blob/main/docs/specification/ECMA-427-2nd_Edition-Release_notes.md): draft release notes, purl-spec main at 7cd2d34 (2026-09-29), checked 2026-10-05.
- [purl-spec release v1.0.1](https://github.com/package-url/purl-spec/releases/tag/v1.0.1): Released, v1.0.1 (2026-08-03), checked 2026-10-05.
- [purl-spec Clause 5 (2nd Edition working copy)](https://github.com/package-url/purl-spec/blob/main/docs/specification/standard/Clause-5-Package-URL-Specification.md): draft working copy, main at 7cd2d34, checked 2026-10-05.
- [Annex B Recommended Qualifiers](https://github.com/package-url/purl-spec/blob/main/docs/specification/standard/Annex-B-Recommended-Qualifiers.md): draft informative annex, main at 7cd2d34, checked 2026-10-05.
- [Annex C ABNF Grammar](https://github.com/package-url/purl-spec/blob/main/docs/specification/standard/Annex-C-ABNF-Grammar.md): draft informative annex, main at 7cd2d34, checked 2026-10-05.
- [PURL qualifiers guidance](https://github.com/package-url/purl-spec/blob/main/docs/specification/common-qualifiers.md): specification documentation, main at 7cd2d34, checked 2026-10-05.
- [How to parse a PURL](https://github.com/package-url/purl-spec/blob/main/docs/specification/how-to-parse.md): specification documentation, main at 7cd2d34, checked 2026-10-05.
- [How to build a PURL](https://github.com/package-url/purl-spec/blob/main/docs/specification/how-to-build.md): specification documentation, main at 7cd2d34, checked 2026-10-05.
- [Lenient PURL grammar](https://github.com/package-url/purl-spec/blob/main/docs/specification/lenient-ABNF-grammar.md): specification documentation, main at 7cd2d34, checked 2026-10-05.
- [Registered PURL type definitions](https://github.com/package-url/purl-spec/tree/main/types): 42 JSON definitions on purl-type-definition schema 1.0, main at 7cd2d34, checked 2026-10-05.
- [PURL test suite](https://github.com/package-url/purl-spec/blob/main/docs/tests/test-suite.md): test documentation and `tests/` on purl-test schema 0.2, main at 7cd2d34, checked 2026-10-05.
- [purl-spec FAQ](https://github.com/package-url/purl-spec/blob/main/faq.md): FAQ, main at 7cd2d34, checked 2026-10-05.
- [Pre-ECMA purl specification](https://github.com/package-url/purl-spec/blob/4f7d28e1d1343a38bc8d7537ac60d390ae64a772/PURL-SPECIFICATION.rst): superseded community text "v1.0.X", commit 4f7d28e (2024-11-21), checked 2026-10-05.
- [VERS specification, Clause 5](https://github.com/package-url/vers-spec/blob/v1.2.0/docs/specification/standard/Clause-5-VERS-Specification.md): Released (submitted to TC54 as the VERS 1st Edition draft), v1.2.0 (2026-09-09), checked 2026-10-05.
- [How to parse and validate VERS](https://github.com/package-url/vers-spec/blob/v1.2.0/docs/specification/how-to-parse.md): Released, v1.2.0, checked 2026-10-05.
- [VERS types](https://github.com/package-url/vers-spec/blob/v1.2.0/docs/types/vers-types.md): Released, v1.2.0, checked 2026-10-05.
- [vers-spec release v1.2.0](https://github.com/package-url/vers-spec/releases/tag/v1.2.0): Released, v1.2.0 (2026-09-09), checked 2026-10-05.
