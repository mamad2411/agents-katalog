---
name: openvex
description: >-
  OpenVEX v0.2.0: write, validate and consume VEX documents that say whether a
  product is affected by a vulnerability. Covers the document (@context, @id,
  author, role, timestamp, version, tooling, statements), statements with a
  vulnerability struct, products and subcomponents identified by @id, purl or
  CPE and hashes, the four status labels (not_affected, affected, fixed,
  under_investigation), the five not_affected justifications, impact_statement,
  action_statement and status_notes, timestamp and product inheritance,
  updating documents, the JSON Schema, embedding as an in-toto attestation
  predicate, and how OpenVEX maps to the CISA Minimum Requirements for VEX.
  Use when an agent turns off a scanner false positive, publishes VEX next to
  an SBOM, attests VEX, or reads an older OpenVEX v0.0.2 document. Triggers:
  OpenVEX, VEX, vexctl, openvex.dev/ns, not_affected justification,
  vulnerable_code_not_in_execute_path, false positive CVE, VEX attestation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OpenVEX

OpenVEX is a minimal, embeddable JSON-LD implementation of Vulnerability Exploitability eXchange (VEX), published by the OpenVEX community (an OpenSSF project) in the `openvex/spec` repository. With this skill the agent writes and reads OpenVEX documents whose statements tell scanners and people whether a product is affected by a vulnerability, and embeds them in attestations.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

The OpenVEX spec has no section numbers, so citations name the file and the heading: "Spec" is `OPENVEX-SPEC.md`, "Attesting" is `ATTESTING.md`, "Schema" is `openvex_json_schema.json`, and "CISA" is the Minimum Requirements for VEX (which does have numbers).

## Inputs (fill in, or ask before starting)

- Role: producer (author of VEX for software you ship or assess), consumer (scanner, policy engine or dashboard that reads VEX), or attester (wraps VEX in an in-toto attestation).
- Target version: OpenVEX v0.2.0 (default, the only line to author). OpenVEX v0.0.2 is legacy: read it and upgrade from it, never author it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the `openvex/spec` releases page for a new tag and `main` for a new spec heading or `ns/` context directory, and update the pins.
- Products: the software the statements are about, with a purl (preferred), CPE or IRI for each, and hashes when known.
- Vulnerabilities: the identifier for each (CVE, GHSA, OSV or an internal id understood across the supply chain), plus aliases.
- Delivery: a standalone `.json` document, an in-toto attestation predicate, or VEX data inside another format (CSAF, CycloneDX).

## Invariants

1. **Required document fields.** `@context`, `@id`, `author`, `timestamp`, `version` and `statements` are required; files are UTF-8 (Spec, Document Struct Fields; Spec, Document). The schema forbids any other top-level field (Schema).
2. **Versioned context.** `@context` is `https://openvex.dev/ns/v0.2.0`; an unversioned `https://openvex.dev/ns` means v0.0.1 (Spec, Document Struct Fields).
3. **`@id` is an IRI** (Spec, Document Struct Fields; Spec, VEX Extensions). The shared `https://openvex.dev/docs/public/...` and `.../example/...` namespaces are for demos and docs only (Spec, Public IRI Namespaces).
4. **`author` is an individual or organization**, not a tool; tools go in `tooling`. Its identity SHOULD be cryptographically bound to the signature (Spec, Document Struct Fields; CISA § 2.2.3).
5. **`version` goes up on every content change**, including any change to a statement (Spec, Document Struct Fields). It is an integer of at least 1 (Schema).
6. **Every statement is complete.** It has one `vulnerability` with a `name`, a `status`, at least one product and a timestamp, where product and timestamp may be inherited from the document or the encapsulating format. A document with incomplete statements is not valid (Spec, Data Inheritance).
7. **`status` is one of `not_affected`, `affected`, `fixed`, `under_investigation`** (Spec, Status Labels; Schema).
8. **`not_affected` needs a `justification` or an `impact_statement`.** Issuers SHOULD use the machine-readable `justification` and MAY add an `impact_statement`; a lone impact statement is highly discouraged because it breaks automation (Spec, Note on `justification` and `impact_statement`).
9. **`affected` needs an `action_statement`** that SHOULD say how to remediate or mitigate (Spec, Statement Fields; Schema).
10. **Products are addressable.** Each product and subcomponent has an `@id` or `identifiers` (Schema); purls are recommended (Spec, Product Data Structure). `identifiers` keys are `purl`, `cpe22`, `cpe23` (Spec, Appendix B); `hashes` keys come from Appendix A.
11. **One status per statement for all its products.** If the status differs for some products, write another statement (CISA § 2.7.1, § 3.1.2).
12. **Updates keep old statements intact.** When the document `timestamp` changes, statements that inherited the old one get it written in explicitly (Spec, Updating Statements with Inherited Data).

## Workflow

1. **Pick the version.** Author OpenVEX v0.2.0. If the input has `"@context": "https://openvex.dev/ns"`, a string `vulnerability` or string `products`, it is v0.0.2 or older: plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ `@context` is `https://openvex.dev/ns/v0.2.0`.
2. **Identify products and vulnerabilities.** Give each product an `@id` (a purl works) plus `identifiers` and `hashes`; list subcomponents (the dependency where the vulnerability lives) inside the product. Give each vulnerability a `name` and `aliases`.
   -> [`references/document-and-statements.md`](references/document-and-statements.md)
   ✓ Every product and subcomponent has `@id` or `identifiers`, and identifiers match the SBOM.
3. **Choose status and justification.** Pick the status from the evidence; for `not_affected` pick the narrowest justification, for `affected` write the action.
   -> [`references/status-and-justifications.md`](references/status-and-justifications.md)
   ✓ Every `not_affected` has a justification (or at least an impact statement), and every `affected` has an `action_statement`.
4. **Assemble the document.** Fill the document fields, group statements that share status and vulnerability, and let statements inherit the document `timestamp` when issued together.
   -> [`references/document-and-statements.md`](references/document-and-statements.md)
   ✓ The document validates against the JSON Schema.
5. **Update or merge.** For a new finding, add a statement (newer statements override older ones for the same product and vulnerability), bump `version`, set `last_updated`, and pin inherited timestamps on untouched statements.
   -> [`references/producing-and-consuming.md`](references/producing-and-consuming.md)
   ✓ No earlier statement changed meaning or timestamp.
6. **Embed or sign** (when attesting). Move products into the attestation `subject`, or repeat them there; sign with the identity named in `author`.
   -> [`references/producing-and-consuming.md`](references/producing-and-consuming.md)
   ✓ Every product left in a statement also appears as a subject.
7. **Consume.** Resolve inheritance, match statements to findings by product identifier and vulnerability name or alias, order by timestamp, and apply the latest status.
   -> [`references/producing-and-consuming.md`](references/producing-and-consuming.md)
   ✓ Statements whose products do not include the attested subject are ignored.
8. **Upgrade** (only when asked). Follow the v0.0.2 to v0.2.0 steps.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded document validates against the schema and says the same thing about the same products.

## Verify before done

- [ ] The document validates against `openvex_json_schema.json` (no extra fields, integer `version` ≥ 1, `statements` not empty).
- [ ] `@context` is `https://openvex.dev/ns/v0.2.0` and `@id` is an IRI (not under `public` or `example` outside demos and docs).
- [ ] Every statement has a vulnerability `name`, a status, and a product and timestamp, either set or inherited (Spec, Data Inheritance).
- [ ] `not_affected` statements carry a `justification` from the five labels; `affected` statements carry an `action_statement`.
- [ ] `identifiers` uses only `purl`, `cpe22`, `cpe23`; `hashes` uses only Appendix A names.
- [ ] After an update, `version` is higher, and statements that inherited the old document timestamp now carry it explicitly.
- [ ] In an attestation, every product in a statement is also a subject, and the signer matches `author` where possible.

## Reference index

- **`references/versions.md`**: OpenVEX v0.2.0 and v0.0.2, what changed, the upgrade steps, and why there is no preview. Load for steps 1 and 8.
- **`references/document-and-statements.md`**: every document, statement, product, component and vulnerability field, inheritance, JSON-LD, the hash and identifier tables, a full example, and schema-versus-text gaps. Load for steps 2 and 4.
- **`references/status-and-justifications.md`**: the four statuses, the five justifications, impact, action and status notes, and how to choose. Load for step 3.
- **`references/producing-and-consuming.md`**: updating and merging documents, embedding in in-toto attestations, signing, consumer matching, the CISA minimum elements mapping, and common mistakes. Load for steps 5 to 7.

## Related skills

- `purl` for building product identifiers: `npx skills add ScaleDockHQ/scaledock-skills --skill purl`.
- `in-toto` for the attestation Statement and envelope that carry OpenVEX as a predicate: `npx skills add ScaleDockHQ/scaledock-skills --skill in-toto`.
- `csaf` for the CSAF VEX profile, an encapsulating format with product trees: `npx skills add ScaleDockHQ/scaledock-skills --skill csaf`.
- `cyclonedx` for CycloneDX VEX and the SBOMs products point into: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`.
- `osv` for OSV vulnerability ids and aliases: `npx skills add ScaleDockHQ/scaledock-skills --skill osv`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenVEX Specification (OPENVEX-SPEC.md)](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md): draft specification, v0.2.0 text at commit 61b5f88 (2026-09-09), checked 2026-10-05.
- [OpenVEX spec releases](https://github.com/openvex/spec/releases): released, v0.2.0 is latest (2023-08-22), checked 2026-10-05.
- [OpenVEX Specification v0.0.2](https://github.com/openvex/spec/blob/v0.0.2/OPENVEX-SPEC.md): released, superseded by v0.2.0, tag v0.0.2 (2023-07-18), checked 2026-10-05.
- [Attesting OpenVEX Documents (ATTESTING.md)](https://github.com/openvex/spec/blob/main/ATTESTING.md): draft, commit 61b5f88 (2026-09-09), checked 2026-10-05.
- [OpenVEX JSON Schema](https://github.com/openvex/spec/blob/main/openvex_json_schema.json): JSON Schema 2020-12 for v0.2.0, commit 61b5f88, checked 2026-10-05.
- [OpenVEX JSON-LD context v0.2.0](https://github.com/openvex/spec/blob/main/ns/v0.2.0/context.json): context for `https://openvex.dev/ns/v0.2.0`, commit 61b5f88, checked 2026-10-05.
- [openvex.dev](https://openvex.dev): project site, redirects to the `openvex/spec` repository, checked 2026-10-05.
- [OPEV-0014: Expansion of the VEX Product Field](https://github.com/openvex/community/blob/main/enhancements/opev-0014.md): accepted enhancement, merged into v0.2.0, checked 2026-10-05.
- [OPEV-0015: Expansion of the Vulnerability Field](https://github.com/openvex/community/blob/main/enhancements/opev-0015.md): accepted enhancement, merged into v0.2.0, checked 2026-10-05.
- [CISA Minimum Requirements for VEX](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf): published by CISA (VEX Working Group), requirements version 1.0.0 (April 2023), checked 2026-10-05.
