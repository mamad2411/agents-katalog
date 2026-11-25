---
name: spdx
description: >-
  SPDX 3.0.1 SBOMs and license expressions: write, validate and upgrade SPDX
  documents and SPDX-License-Identifier tags. Covers the SPDX 3.0 model
  (Core, Software, Security, Licensing, SimpleLicensing, ExpandedLicensing,
  Dataset, AI, Build, Lite and Extension profiles; Element, Relationship,
  SpdxDocument, CreationInfo; JSON-LD), the supported SPDX 2.3 document format
  (creation info, packages, files, snippets, relationships, other licensing
  info; tag:value and JSON), SPDX license expressions (AND, OR, WITH, +,
  LicenseRef-, AdditionRef-) against SPDX License List 3.29, and SBOMs that
  cover the NTIA and CISA minimum elements. SPDX 3.1 (3.1-RC1) is tracked as
  a preview; SPDX 2.2 (ISO/IEC 5962:2021) and older are legacy, with a 2.3 to
  3.0 upgrade guide. Use when generating or reviewing an SBOM in SPDX, adding
  license headers to source files, choosing a license identifier, converting
  SPDX 2.x to 3.0, or checking .spdx, .spdx.json or spdx-context.jsonld files.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# SPDX

SPDX (System Package Data Exchange, formerly Software Package Data Exchange) is the Linux Foundation's open standard for bills of materials, licensing and provenance; SPDX 2.2.1 is ISO/IEC 5962:2021. With this skill the agent produces and checks SPDX 3.0 JSON-LD documents, SPDX 2.3 documents, SPDX license expressions and `SPDX-License-Identifier` tags, and upgrades SPDX 2.x to 3.0.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer (a tool or build that emits SPDX), consumer (a tool that reads or validates it), or source-tree maintainer (license tags only).
- Artifact: an SBOM document, license expressions only, or `SPDX-License-Identifier` tags in source files.
- Target version: SPDX 3.0 at 3.0.1 (default). SPDX 2.3 is supported: emit it only for a named consumer that cannot read 3.0. SPDX 2.2 and SPDX 2.1 and earlier are legacy: read and upgrade, never author. SPDX 3.1 is a preview (posture: track): never emit `specVersion` 3.1. License identifiers come from SPDX License List 3.29 (its own family). See [`references/versions.md`](references/versions.md).
- Serialization: SPDX 3.0 JSON-LD (default), or for 2.3 one of tag:value, JSON, YAML, RDF/XML or spreadsheet.
- Profiles: which SPDX 3.0 profiles the document claims in `profileConformance` (at least `core`; usually `software` and `simpleLicensing`).
- Minimum elements: whether the SBOM must cover the 2021 NTIA or 2026 CISA minimum elements.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the `spdx/spdx-spec` and `spdx/spdx-3-model` releases for a 3.1 final or a 2.3.1 release, check the License List version, and update the pins.

## Invariants

1. **One SpdxDocument per serialization.** A serialization must not contain or define more than one SpdxDocument (3.0.1 Serializations, Serialization information; model `SpdxDocument`).
2. **Every Element has `spdxId`, `type` and `creationInfo`.** `spdxId` is a URI, exactly one; `creationInfo` is exactly one CreationInfo (model `Element`). CreationInfo needs `specVersion`, `created` and at least one `createdBy` Agent (model `CreationInfo`).
3. **JSON-LD uses the SPDX global context.** Every 3.0.1 JSON-LD document references `https://spdx.org/rdf/3.0.1/spdx-context.jsonld` in a top-level `@context`, and must pass both the SPDX JSON Schema and the SPDX OWL ontology with its SHACL shapes (3.0.1 Serializations, JSON-LD context file and JSON-LD validation).
4. **Core is mandatory.** Every other profile builds on Core, and naming a profile in `profileConformance` claims every contained element meets that profile's restrictions (3.0.1 Conformance; model `ProfileIdentifierType`).
5. **Collections name their roots.** An ElementCollection with at least one `element` has at least one `rootElement`, and neither may be an SpdxDocument (model `ElementCollection`).
6. **Unknown is not none.** Use `NoAssertionElement` or `NoAssertionLicense` when no determination was made, and `NoneElement` or `NoneLicense` only for a positive "there is none"; `NoneElement` must be the only `to` (model `Relationship`, `NoAssertionElement`, `NoneElement`, `NoAssertionLicense`, `NoneLicense`). In 2.3 the same split is `NOASSERTION` and `NONE` (2.3 § 7.7, § 7.13, § 11.1).
7. **License expressions follow the ABNF.** Whitespace around `WITH`, whitespace or parentheses around `AND` and `OR`, no whitespace before `+`, one line in tag:value; precedence is `+`, `WITH`, `AND`, `OR` (3.0.1 Annex SPDX license expressions; 2.3 Annex D).
8. **Identifiers match case-insensitively, operators do not.** Write the canonical case from the License List; `LicenseRef-` and `AdditionRef-` prefixes are case-sensitive (3.0.1 license expressions, Case sensitivity).
9. **Every custom license is defined.** A `LicenseRef-` needs its text: `SimpleLicensingText` in 3.0, or License Identifier plus Extracted Text in 2.3 (2.3 § 10.1, § 10.2; model SimpleLicensing).
10. **2.3 documents are self-identifying.** `SPDXVersion: SPDX-2.3`, `DataLicense: CC0-1.0`, `SPDXID: SPDXRef-DOCUMENT`, a document name, a unique absolute namespace URI without `#` that changes with every new version, at least one Creator, and `Created` in `YYYY-MM-DDThh:mm:ssZ` (2.3 § 6.1 to § 6.9).

## Workflow

1. **Pick the version.** Use SPDX 3.0 (3.0.1) unless a named consumer only reads 2.3. Pin the License List version too.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target line and License List version are recorded; nothing targets 3.1 or 2.2.
2. **Choose identifiers and licenses.** Build each license expression from License List identifiers, exceptions with `WITH`, and `LicenseRef-` or `AdditionRef-` for anything unlisted. Prefer `-only` and `-or-later` GNU identifiers over the deprecated bare ones.
   -> [`references/license-expressions.md`](references/license-expressions.md)
   ✓ Every expression parses against the ABNF, and every custom reference has its text.
3. **Tag source files** (when asked). Put `SPDX-License-Identifier: <expression>` on its own line in a comment at or near the top of each file, and keep the full license text in the project.
   -> [`references/license-expressions.md`](references/license-expressions.md)
   ✓ Each tag is one line and uses a valid expression.
4. **Build an SPDX 3.0 document.** Write the `@context`, one CreationInfo blank node, the Agents, one SpdxDocument with `profileConformance` and `rootElement`, a `software_Sbom`, the Packages and Files, and Relationships (`contains`, `dependsOn`, `hasDeclaredLicense`, `hasConcludedLicense`).
   -> [`references/spdx3-model.md`](references/spdx3-model.md)
   ✓ The document validates against the 3.0.1 JSON Schema and the SHACL shapes, and every reference resolves in the graph or through `import`.
5. **Or build an SPDX 2.3 document** (supported consumers only). Fill the creation information, one section per package with its files after it, other licensing information for each `LicenseRef-`, and a `DESCRIBES` relationship from `SPDXRef-DOCUMENT`.
   -> [`references/spdx23-documents.md`](references/spdx23-documents.md)
   ✓ All required fields are present, and the JSON form validates against the 2.3 schema.
6. **Cover the minimum elements** when the SBOM must meet them. Map each NTIA 2021 or CISA 2026 element to its SPDX field or property, and fill it or record why it is `NOASSERTION`.
   -> [`references/sbom-minimum-elements.md`](references/sbom-minimum-elements.md)
   ✓ Each required element maps to a populated field; the author signature is supplied outside the document.
7. **Consume and validate.** Detect the version from `@context` and `specVersion` (3.0) or `SPDXVersion` (2.x); apply case-insensitive identifier matching; treat an omitted optional 2.3 field as `NOASSERTION`.
   -> [`references/versions.md`](references/versions.md)
   ✓ Legacy and preview inputs are flagged, not silently treated as 3.0.1.
8. **Upgrade** (only when asked). Follow the 2.3 to 3.0 checklist: creators to Agents, relationships to standalone elements with swapped directions, external document references to `import` and `namespaceMap`, `purl` to `packageUrl`, checksums to `verifiedUsing`.
   -> [`references/versions.md`](references/versions.md)
   ✓ The 3.0 document validates and carries the same packages, licenses and relationships as the 2.3 input.

## Verify before done

- [ ] 3.0: `@context` is `https://spdx.org/rdf/3.0.1/spdx-context.jsonld`, `specVersion` is `3.0.1`, and the document passes the JSON Schema and SHACL validation (Serializations, JSON-LD validation).
- [ ] 3.0: exactly one SpdxDocument; every Element has `type`, `spdxId` and `creationInfo`; `profileConformance` includes `core` and every profile whose classes are used.
- [ ] 3.0: every Package has a `name`; Lite-profile Packages also have `packageVersion`, `suppliedBy`, `copyrightText`, a `downloadLocation` or `packageUrl`, and exactly one `hasConcludedLicense` and one `hasDeclaredLicense` relationship (Annex SPDX Lite).
- [ ] 2.3: the seven creation-information fields are present, every Package has name, `SPDXRef-` identifier and download location, every File has name, identifier and a SHA1 checksum (§ 6, § 7, § 8).
- [ ] Every license expression parses; no deprecated License List identifier is newly written; every `LicenseRef-` has its text.
- [ ] `NONE` versus `NOASSERTION` (or their 3.0 individuals) reflects what was actually determined.
- [ ] Nothing claims SPDX 3.1, and no 2.2 or older document is newly authored.

## Reference index

- **`references/versions.md`**: every SPDX line and the License List family, which to use, what changed, the 2.3 to 3.0 translation tables, and the 3.1 preview. Load for steps 1, 7 and 8.
- **`references/spdx3-model.md`**: profiles, Element, CreationInfo, SpdxDocument, Sbom, Package, File, Snippet, Relationship types, licensing in 3.0, JSON-LD shape and a complete example. Load for step 4.
- **`references/spdx23-documents.md`**: the 2.3 sections and fields with cardinalities, formats, relationship types, and the 2.3.1 corrections. Load for step 5.
- **`references/license-expressions.md`**: the ABNF, operators and precedence, case rules, `LicenseRef-`, `AdditionRef-`, `DocumentRef-`, the License List and deprecated identifiers, and `SPDX-License-Identifier` tags. Load for steps 2 and 3.
- **`references/sbom-minimum-elements.md`**: SPDX's mappings of the NTIA 2021 and CISA 2026 minimum elements, and the SPDX Lite mandatory set. Load for step 6.

## Related skills

- `cyclonedx` for the other common SBOM format: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `purl` for the Package URL strings used in `packageUrl` and `PACKAGE-MANAGER purl` references: `npx skills add ScaleDockHQ/scaledock-skills --skill purl`.
- `eu-cra` for the EU Cyber Resilience Act SBOM obligations: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-cra`.
- `slsa` for build provenance alongside the SPDX Build profile: `npx skills add ScaleDockHQ/scaledock-skills --skill slsa`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SPDX Specification 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/): Released, 3.0.1 (2024-12-17), checked 2026-10-05.
- [SPDX 3 model releases](https://github.com/spdx/spdx-3-model/releases): Released 3.0.1 (2024-12-10); pre-release 3.1-rc1 (2026-01-24), checked 2026-10-05.
- [SPDX 3.0.1 JSON-LD context](https://spdx.org/rdf/3.0.1/spdx-context.jsonld): Released, 3.0.1, checked 2026-10-05.
- [SPDX Specification 2.3](https://spdx.github.io/spdx-spec/v2.3/): Released, 2.3 (2022-11-03); the URL now redirects to 2.3.1, checked 2026-10-05.
- [SPDX Specification 2.3.1](https://spdx.github.io/spdx-spec/v2.3.1/): maintenance release text published, tag v2.3.1, changelog dated 2026-10-30, no GitHub release yet, checked 2026-10-05.
- [SPDX specifications index](https://spdx.dev/use/specifications/): publisher index, lists 3.0 as current, checked 2026-10-05.
- [spdx/spdx-spec releases](https://github.com/spdx/spdx-spec/releases): release index, 3.0.1 latest, v3.1-RC1 pre-release, checked 2026-10-05.
- [SPDX Specification 3.1-RC1](https://spdx.github.io/spdx-spec/v3.1-RC1/): Release candidate, 3.1-RC1 (2026-01-24), checked 2026-10-05.
- [Differences from previous editions](https://github.com/spdx/using/blob/main/docs/diffs-from-previous-editions.md): Informative, main branch, checked 2026-10-05.
- [Getting started writing SPDX 3](https://github.com/spdx/using/blob/main/docs/getting-started.md): Informative, main branch, checked 2026-10-05.
- [SPDX License List](https://spdx.org/licenses/): Released, 3.29.0 (2026-09-16), checked 2026-10-05.
- [spdx/license-list-data releases](https://github.com/spdx/license-list-data/releases): Released, v3.29.0 (2026-09-16), checked 2026-10-05.
