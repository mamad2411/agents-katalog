---
name: cyclonedx
description: >-
  CycloneDX 1.7 (ECMA-424 2nd edition) Bill of Materials: produce, validate, sign and consume SBOM, SaaSBOM, HBOM,
  CBOM, ML-BOM, OBOM, MBOM, VDR and VEX documents in JSON, XML or Protobuf. Use when generating or reviewing a
  CycloneDX BOM in CI, modelling components, services, dependencies and compositions, writing vulnerabilities with VEX
  analysis states and justifications, linking objects with bom-ref and BOM-Link (urn:cdx:), identifying components by
  purl, CPE, SWID, OmniBOR or SWHID, adding formulation, annotations, declarations and attestations (CDXA),
  definitions or citations, validating against the JSON Schema or XSD, or signing with JSF. Targets CycloneDX 1.7
  (schema 1.7.2); CycloneDX 1.6 (ECMA-424 1st edition) is supported; CycloneDX 1.5, 1.4 and 1.0-1.3 are legacy, upgrade
  from them; the CycloneDX 2.0 draft is tracked as a preview. Triggers: bom.json, *.cdx.json, bom.xml,
  application/vnd.cyclonedx+json, bomFormat, specVersion, serialNumber, OWASP CycloneDX, ECMA-424.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# CycloneDX

CycloneDX is the OWASP full-stack Bill of Materials standard, published by Ecma International TC54 as ECMA-424. One object model covers software, services, hardware, cryptographic assets, ML models, build processes, vulnerabilities and attestations. With this skill the agent produces, validates, signs and consumes CycloneDX BOMs, and upgrades older ones.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Citations: "ECMA-424 §" is the 2nd edition (CycloneDX v1.7). "Schema `x`" is the definition or property `x` in `bom-1.7.schema.json` at tag 1.7.2, which the standard names as its reference implementation (ECMA-424 § 6, Table 1 note).

## Inputs (fill in, or ask before starting)

- Role: producer (generates or enriches BOMs), consumer (ingests, analyses or gates on them), or both (ECMA-424 § 2).
- Target version: CycloneDX 1.7 (default, schema 1.7.2). CycloneDX 1.6 is supported for consumers that cannot read 1.7. CycloneDX 1.5, CycloneDX 1.4 and CycloneDX 1.0-1.3 are legacy: read them and upgrade from them, never author them. The CycloneDX 2.0 draft is a preview (posture: track): never emit it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- BOM type: SBOM, SaaSBOM, HBOM, CBOM, ML-BOM, OBOM, MBOM, VDR, VEX or CDXA, and the lifecycle phase the data comes from. See [`references/bom-types.md`](references/bom-types.md).
- Serialization: JSON (default; the reference implementation), XML or Protobuf.
- Signing: none, or JSF with a named key and algorithm.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, run `gh api repos/CycloneDX/specification/releases` for a newer patch or minor, check the ECMA-424 page for a new edition, check the `2.0-dev` branch, and update the pins.

## Invariants

1. **Root identity.** `bomFormat` is `"CycloneDX"` and `specVersion` is the version string, both required in JSON (ECMA-424 § 6.1, § 6.2; schema `required`). XML carries the version in the namespace `http://cyclonedx.org/schema/bom/1.7`; Protobuf in `spec_version` (package `cyclonedx.v1_7`).
2. **Serial number and version.** Every generated BOM SHOULD get a new `serialNumber`, even if the content did not change; it matches `^urn:uuid:` plus a lowercase RFC 4122 UUID. Each modification SHOULD increment `version` (integer, minimum 1, default 1); a consumer with several BOMs of one serial number SHOULD use the highest version (ECMA-424 § 6.3, § 6.4).
3. **`bom-ref` is unique.** Every `bom-ref` is unique within the BOM and SHOULD NOT start with `urn:cdx:` (schema `refType`). The XSD enforces uniqueness with `xs:unique`; the JSON Schema does not, so check it yourself.
4. **References resolve.** `dependencies[].ref` and `dependsOn` point to a `bom-ref` in the same BOM (schema `refLinkType`). `compositions[].assemblies`, `vulnerabilities[].affects[].ref` and `annotations[].subjects` may also hold a BOM-Link element `urn:cdx:<serial>/<version>#<bom-ref>` (schema `bomLinkElementType`).
5. **Empty dependencies are explicit.** A component or service with no dependencies is declared as an entry with no `dependsOn`. A component missing from the graph has unknown dependencies, not none (schema `dependency`; ECMA-424 § 6.9).
6. **Components.** `type` and `name` are required. `version` and `versionRange` are mutually exclusive, and `versionRange` (vers syntax) is only allowed when `isExternal` is `true` (schema `component`, `allOf`).
7. **Identifiers are valid.** A `purl` must conform to the purl specification; a `cpe` must conform to CPE 2.2 or 2.3; a `swid` needs `tagId` and `name` (schema `component.purl`, `component.cpe`, `swid`).
8. **Licenses use SPDX.** `license.id` is an SPDX license ID and `expression` a valid SPDX license expression (schema `license`, `licenseChoice`). 1.7 allows several expressions mixed with licenses; 1.6 allows either a list of licenses or exactly one expression.
9. **VEX analysis is justified.** `analysis.state` is one of `resolved`, `resolved_with_pedigree`, `exploitable`, `in_triage`, `false_positive`, `not_affected`; every `not_affected` SHOULD carry a `justification`, and `exploitable` is strongly encouraged to carry a `response` (schema `impactAnalysisState`, `vulnerability.analysis`).
10. **Producers stay conformant.** A producer's BOMs conform to the standard, and enriching or modifying a BOM introduces no non-conforming content. A consumer does not raise an error on a conforming BOM, SHOULD warn on a non-conforming one, and need not process every field (ECMA-424 § 2).
11. **No deprecated fields in new BOMs.** Do not emit the legacy `tools` array, `component.author`, `metadata.manufacture`, `component.modified`, a single-object `evidence.identity`, or the CBOM fields deprecated in 1.7 (schema `deprecated` marks; 1.6 and 1.7 release notes).
12. **JSF signatures cover the canonical form.** A `signature` is a JSF 0.82 object; the signed data is the JCS (RFC 8785) canonicalization of the enclosing object with `value` removed and `excludes` properties left out (JSF § 6, § 7; schema `signature`). Only the JSON schema defines `signature`.

## Workflow

1. **Pick the version.** Use CycloneDX 1.7 unless a named consumer reads only 1.6.
   -> [`references/versions.md`](references/versions.md)
   ✓ `specVersion` (or the XML namespace) is `1.7` or `1.6`, never a legacy or preview line.
2. **Pick the BOM type and lifecycle.** Decide which inventory the BOM holds and set `metadata.lifecycles` to the phase the data was captured in (schema `metadata.lifecycles`).
   -> [`references/bom-types.md`](references/bom-types.md)
   ✓ The BOM type maps to the root elements it needs, and the lifecycle phase is recorded.
3. **Write the root and metadata.** Set `bomFormat`, `specVersion`, a fresh `serialNumber`, `version`, `metadata.timestamp`, `metadata.tools` (object with `components`/`services`), `metadata.component` (the subject) and `supplier` or `manufacturer`.
   -> [`references/object-model.md`](references/object-model.md)
   ✓ Invariants 1, 2 and 11 hold.
4. **Inventory components and identify them.** Add every first- and third-party component with `type`, `name`, `version`, `bom-ref`, `purl` (or CPE, SWID, OmniBOR, SWHID), `hashes`, `licenses` and `scope`.
   -> [`references/identifiers-and-links.md`](references/identifiers-and-links.md)
   ✓ Invariants 3, 6, 7 and 8 hold; every component has at least one identifier a consumer can match.
5. **Add services, dependencies and compositions.** Describe services and data flows, build the dependency graph from `metadata.component` down, and state completeness with `compositions[].aggregate`.
   -> [`references/object-model.md`](references/object-model.md)
   ✓ Invariants 4 and 5 hold; every composition has an `aggregate`, and `complete` is used only when nothing is missing.
6. **Add vulnerabilities or VEX** (when the BOM type needs them). Record `id`, `source`, `ratings`, `affects` and `analysis`, inline or in a separate BOM that links with BOM-Link.
   -> [`references/vulnerabilities-and-vex.md`](references/vulnerabilities-and-vex.md)
   ✓ Invariant 9 holds, and every `affects[].ref` resolves.
7. **Add provenance and assurance** (optional). Formulation for how it was built, annotations, declarations with definitions for attestations, and citations for who supplied which field.
   -> [`references/object-model.md`](references/object-model.md)
   ✓ Every `subjects`, `assessor`, `requirement`, `attributedTo` and `process` reference resolves.
8. **Serialize, validate and sign.** Write `bom.json` or `*.cdx.json` (or XML or Protobuf), validate against the 1.7 schema, run the semantic checks the schema cannot do, then sign.
   -> [`references/validation-and-signing.md`](references/validation-and-signing.md)
   ✓ Schema validation passes with the SPDX, JSF and cryptography-defs schemas loaded, and the signature verifies.
9. **Consume** (consumer role). Detect format and version, validate, pick the highest `version` per serial number, follow BOM-Links, and treat absent dependency entries as unknown.
   -> [`references/validation-and-signing.md`](references/validation-and-signing.md)
   ✓ A conforming BOM never raises an error; a non-conforming one raises a warning or error.
10. **Upgrade** (only when asked). Follow the upgrade section for each step from the source version to the target.
    -> [`references/versions.md`](references/versions.md)
    ✓ The upgraded BOM validates against the target schema and describes the same inventory.

## Verify before done

- [ ] The BOM validates against the target `bom-1.x.schema.json` (or XSD, or `.proto`) at the pinned patch.
- [ ] `serialNumber` is a lowercase `urn:uuid:` UUID and `version` is an integer of at least 1 (ECMA-424 § 6.3, § 6.4).
- [ ] Every `bom-ref` is unique, and every reference resolves to a `bom-ref` or a well-formed BOM-Link.
- [ ] Every component in `components` appears in `dependencies`, with an empty entry when it has none.
- [ ] No component has both `version` and `versionRange`; `versionRange` appears only with `isExternal: true`.
- [ ] Every `purl` parses, every license ID and expression is valid SPDX, and every `not_affected` analysis has a `justification`.
- [ ] No deprecated field is emitted (invariant 11).
- [ ] A JSF signature, if present, verifies over the JCS canonical form.
- [ ] Nothing from the CycloneDX 2.0 draft (`specFormat`, `signatures`, `$schema` 2020-12) is emitted.

## Reference index

- **`references/versions.md`**: every line from 1.0 to 1.7 and the 2.0 draft, with ECMA-424 editions, what changed, and upgrade checklists. Load for steps 1 and 10.
- **`references/bom-types.md`**: SBOM, SaaSBOM, HBOM, CBOM, ML-BOM, OBOM, MBOM, BOV, VDR, VEX and CDXA, the elements each uses, and lifecycle phases. Load for step 2.
- **`references/object-model.md`**: root, metadata, components, services, dependencies, compositions, formulation, annotations, declarations, definitions, citations and properties, with a minimal example. Load for steps 3, 5 and 7.
- **`references/identifiers-and-links.md`**: purl, CPE, SWID, OmniBOR, SWHID, hashes, `bom-ref`, BOM-Link, external references, media types and file names. Load for step 4.
- **`references/vulnerabilities-and-vex.md`**: the vulnerability object, ratings, affects, analysis states, justifications and responses, and VEX and VDR patterns. Load for step 6.
- **`references/validation-and-signing.md`**: schema validation per format, semantic checks, JSF signing and verification, CI production and consumption. Load for steps 8 and 9.

## Related skills

- `spdx` for the other SBOM format and SPDX license expressions: `npx skills add ScaleDockHQ/scaledock-skills --skill spdx`.
- `purl` for building and parsing Package URLs: `npx skills add ScaleDockHQ/scaledock-skills --skill purl`.
- `openvex` for VEX statements in the OpenVEX format: `npx skills add ScaleDockHQ/scaledock-skills --skill openvex`.
- `csaf` for security advisories and CSAF VEX profiles: `npx skills add ScaleDockHQ/scaledock-skills --skill csaf`.
- `eu-cra` for Cyber Resilience Act SBOM and vulnerability-handling obligations: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-cra`.
- `slsa` for build provenance and in-toto attestations that can carry a CycloneDX BOM: `npx skills add ScaleDockHQ/scaledock-skills --skill slsa`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ECMA-424: CycloneDX Bill of materials specification](https://ecma-international.org/publications-and-standards/standards/ecma-424/): Ecma Standard, 2nd edition December 2025 (CycloneDX v1.7); 1st edition June 2024 archived, checked 2026-10-05.
- [ECMA-424 2nd edition (PDF)](https://ecma-international.org/wp-content/uploads/ECMA-424_2nd_edition_december_2025.pdf): Ecma Standard, 2nd edition December 2025, defines CycloneDX v1.7, checked 2026-10-05.
- [ECMA-424 1st edition (PDF)](https://ecma-international.org/wp-content/uploads/ECMA-424_1st_edition_june_2024.pdf): Ecma Standard (superseded edition), 1st edition June 2024, defines CycloneDX v1.6, checked 2026-10-05.
- [CycloneDX Specification Overview](https://cyclonedx.org/specification/overview/): Released, current version 1.7 (2025-10-21), checked 2026-10-05.
- [CycloneDX v1.7 JSON Reference](https://cyclonedx.org/docs/1.7/json/): Released, 1.7, checked 2026-10-05.
- [CycloneDX specification releases](https://github.com/CycloneDX/specification/releases): Released, latest 1.7.2 (2026-09-17); 1.6.2 and 1.5.1 (2026-06-02), checked 2026-10-05.
- [CycloneDX 1.7 JSON Schema](https://raw.githubusercontent.com/CycloneDX/specification/1.7.2/schema/bom-1.7.schema.json): Released, tag 1.7.2, checked 2026-10-05.
- [CycloneDX 1.7 XML Schema](https://raw.githubusercontent.com/CycloneDX/specification/1.7.2/schema/bom-1.7.xsd): Released, tag 1.7.2, checked 2026-10-05.
- [CycloneDX 1.7 Protobuf schema](https://raw.githubusercontent.com/CycloneDX/specification/1.7.2/schema/bom-1.7.proto): Released, tag 1.7.2, checked 2026-10-05.
- [CycloneDX 1.6 JSON Schema](https://raw.githubusercontent.com/CycloneDX/specification/1.6.2/schema/bom-1.6.schema.json): Released, tag 1.6.2, checked 2026-10-05.
- [CycloneDX schema directory (1.0 to 1.7)](https://github.com/CycloneDX/specification/tree/1.7.2/schema): Released, tag 1.7.2 (includes 1.5.1, 1.4, 1.3, 1.2 JSON and 1.0, 1.1 XSD), checked 2026-10-05.
- [CycloneDX specification README](https://github.com/CycloneDX/specification/blob/1.7.2/README.md): Released, tag 1.7.2 (media types, file names, release history), checked 2026-10-05.
- [CycloneDX BOM-Link](https://cyclonedx.org/capabilities/bomlink/): Capability page, checked 2026-10-05.
- [CycloneDX VEX](https://cyclonedx.org/capabilities/vex/): Capability page, checked 2026-10-05.
- [CycloneDX VDR](https://cyclonedx.org/capabilities/vdr/): Capability page, checked 2026-10-05.
- [JSF: JSON Signature Format](https://cyberphone.github.io/doc/security/jsf.html): Specification, version 0.82 (2020-10-10), as referenced by `jsf-0.82.schema.json`, checked 2026-10-05.
- [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli): Released, v0.33.1 (2026-07-23), checked 2026-10-05.
- [CycloneDX 2.0 schemas (development branch)](https://github.com/CycloneDX/specification/tree/2.0-dev/schema/2.0): Draft, `2.0-dev` at 7a3ab08 (2026-10-05); Draft posture: track, checked 2026-10-05.
