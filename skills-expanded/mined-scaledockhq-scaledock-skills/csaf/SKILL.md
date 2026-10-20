---
name: csaf
description: >-
  OASIS CSAF 2.0 security advisories: write, validate, convert and distribute
  Common Security Advisory Framework JSON documents, including CSAF VEX. Use
  when producing or consuming machine-readable security advisories or VEX
  statements: document metadata and tracking (version, revision_history,
  status), product_tree with branches, full_product_names, relationships and
  product identification helpers (purl, CPE, hashes, SBOM URLs), vulnerabilities
  with cve, cwe, notes, product_status, remediations, CVSS scores, threats and
  flags; the profiles csaf_base, csaf_security_incident_response,
  csaf_informational_advisory, csaf_security_advisory and csaf_vex; mandatory,
  optional and informative tests and validators; and distribution through
  provider-metadata.json, /.well-known/csaf/, security.txt, ROLIE feeds,
  hashes, signatures and TLP, with the provider, lister and aggregator roles. Targets CSAF 2.0 (OASIS Standard with
  Errata 01), tracks the CSAF 2.1 draft (CSD03), and upgrades from CVRF 1.2 XML.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# CSAF

The Common Security Advisory Framework (CSAF) is the OASIS CSAF TC's JSON language for security advisories: which products are affected by which vulnerabilities, and what to do about it. It also carries Vulnerability Exploitability eXchange (VEX) statements through its VEX profile. This skill pins CSAF 2.0 (OASIS Standard, 18 November 2022, with Errata 01) and produces CSAF documents, validators, converters, and provider or aggregator setups that meet its normative rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Section numbers are CSAF 2.0 unless the rule says CSAF 2.1 or CVRF 1.2. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: document producer (a direct producer, converter, translator or modifier), consumer (a viewer, management or asset matching system), validator (basic, extended or full), or distributor (CSAF publisher, provider, trusted provider, lister or aggregator).
- Profile: `csaf_security_advisory`, `csaf_vex`, `csaf_informational_advisory`, `csaf_security_incident_response`, or `csaf_base`.
- Distribution: directory-based or ROLIE-based, and the TLP labels in use.
- Target version: CSAF 2.0 (current, the default). CSAF 2.1 is a preview at Committee Specification Draft 03 (posture: track): never emit `"csaf_version": "2.1"`. CVRF 1.2 is legacy XML: read it and convert from it, never author it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the `v2.1/` index on docs.oasis-open.org for a new stage (CS or OASIS Standard), check `known_issues.md` and the release tags in the TC repository, and update the pins.

## Invariants

1. **Only `document` is mandatory.** `product_tree` and `vulnerabilities` are optional at the schema level; `document.csaf_version` is `2.0` (§3, §3.2.1.4). The JSON schema is normative where the prose has a gap (§2).
2. **Every document satisfies CSAF Base.** It has `category`, `csaf_version`, `publisher` (`category`, `name`, `namespace`), `title` and `tracking` (`current_release_date`, `id`, `initial_release_date`, `revision_history[]` with `date`, `number`, `summary`, `status`, `version`). `document.category` selects the profile; values starting with `csaf_` are reserved for the standard (§4, §4.1).
3. **Product IDs are defined once and resolve.** Every referenced Product ID or Product Group ID has exactly one definition in `product_tree`, and relationships are not circular (§6.1.1 to §6.1.5).
4. **Product status does not contradict itself.** Within one vulnerability, the affected, not affected, fixed and under investigation groups are pairwise disjoint (§6.1.6).
5. **Versions are versions, ranges are ranges.** A `product_version` branch name never contains a range; a `product_version_range` name is canonical `vers` (with `vers:all/*` for all versions) or the fallback `vls` (§3.1.2.3.1, §3.1.2.3.2, §6.1.31).
6. **Released versions are immutable.** A document uses one versioning scheme, integer or semantic; a released version is never modified; `final` documents carry no `0` or `0.y.z` revision items and no pre-release suffix (§3.1.11, §3.2.1.12.6, §6.1.14 to §6.1.22, §6.1.30).
7. **Remediations and flags name their products.** Each item carries `product_ids` or `group_ids` (§3.2.3.5, §3.2.3.12, §6.1.29, §6.1.32).
8. **VEX statements are complete.** In `csaf_vex`, every `known_not_affected` product has an impact statement (a flag, or a threat of category `impact`), and every `known_affected` product has a remediation as an action statement (§4.5).
9. **The filename comes from `tracking.id`.** Lowercase it, replace each run of characters outside `[+\-a-z0-9]` with one `_`, append `.json` (§5.1).
10. **`publisher.namespace` plus `tracking.id` is the global identity.** The ID is unique within the issuer and has no leading or trailing white space or line break (§3.2.1.8.5, §3.2.1.12.4).
11. **Translations say so.** `source_lang` is set when `publisher.category` is `translator`, and absent when the document was not translated (§3.2.1.10).
12. **TLP decides access.** Documents are served over TLS; TLP:WHITE documents are freely accessible; TLP:AMBER and TLP:RED documents are access protected, on a different path (§7.1.3 to §7.1.5).
13. **Content is untrusted input.** Producers put HTML and code only in Markdown code blocks; consumers use a hardened Markdown processor, disable or sanitize HTML, and never run a value as code (§8).
14. **Valid means schema plus mandatory tests.** A CSAF document conforms to section 3, satisfies at least one profile, and fails no mandatory test (§9.1.1).

## Workflow

1. **Pick the version.** Target CSAF 2.0. Read CSAF 2.1 drafts only to prepare, and treat CVRF 1.2 XML as converter input.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy or preview line.
2. **Choose the profile and fill `document`.** Pick the profile from the use case, then set publisher, tracking, distribution (TLP), notes and references.
   -> [`references/profiles-and-vex.md`](references/profiles-and-vex.md), [`references/document-model.md`](references/document-model.md)
   ✓ `document.category` is the profile's exact value, and every element the profile requires is present.
3. **Build the product tree.** Use branches `vendor` → `product_name` → `product_version` where possible, give each product a `product_identification_helper` (purl, CPE, hashes, model or serial numbers, SKUs, SBOM URLs), and use relationships for combinations.
   -> [`references/document-model.md`](references/document-model.md)
   ✓ Every Product ID referenced elsewhere is defined once, and no `product_version` name holds a range.
4. **Describe each vulnerability.** Set `cve` (or `ids`), `cwe`, `notes`, `product_status`, `remediations`, `scores`, `threats` and `flags`, each tied to Product IDs or groups.
   -> [`references/document-model.md`](references/document-model.md)
   ✓ No product sits in two contradicting status groups, and every remediation names its products.
5. **Write VEX statements** (for `csaf_vex`). Give each `known_not_affected` product a justification flag or impact threat, and each `known_affected` product an action statement.
   -> [`references/profiles-and-vex.md`](references/profiles-and-vex.md)
   ✓ The profile tests 6.1.27.4 to 6.1.27.11 pass.
6. **Version and release.** Bump `tracking.version` by the semantic or integer rules, add a `revision_history` item, set `status`, and update `current_release_date`.
   -> [`references/document-model.md`](references/document-model.md)
   ✓ `tracking.version` equals the latest `revision_history` number, and a change that needs a new asset comparison bumps the major version.
7. **Validate.** Check against the CSAF 2.0 JSON schema, then run the mandatory tests (errors), optional tests (warnings) and informative tests (information).
   -> [`references/tests-and-conformance.md`](references/tests-and-conformance.md)
   ✓ Schema validation and every mandatory test pass; optional test failures are reviewed.
8. **Name, sign and distribute.** Derive the filename, add hash and OpenPGP signature files, publish `provider-metadata.json`, and serve the documents through year folders or ROLIE feeds for the chosen role.
   -> [`references/distribution.md`](references/distribution.md)
   ✓ `/.well-known/csaf/provider-metadata.json` (or the security.txt `CSAF` field, or the DNS path) resolves to valid metadata, and every feed entry links its hash and signature.
9. **Retrieve and consume** (consumers, listers, aggregators). Find `provider-metadata.json`, prefer ROLIE, check hash and signature, validate, then run mandatory tests before use.
   -> [`references/distribution.md`](references/distribution.md)
   ✓ A document with a bad signature or a failed mandatory test is not processed further.
10. **Upgrade** (only when asked). Convert CVRF 1.2 XML to CSAF 2.0 with the CVRF CSAF converter rules; plan CSAF 2.0 to CSAF 2.1 only when 2.1 reaches a final stage.
    -> [`references/versions.md`](references/versions.md)
    ✓ The converted document validates against the target version and keeps the same products, statuses and remediations.

## Verify before done

- [ ] The document validates against `https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json` and `csaf_version` is `2.0`.
- [ ] All mandatory tests in §6.1 pass, including the profile tests in §6.1.27 for the chosen category.
- [ ] Every Product ID and Product Group ID referenced is defined exactly once, and every defined Product ID is used (optional test 6.2.1).
- [ ] For `csaf_vex`: each `known_not_affected` product has a flag or `impact` threat, and each `known_affected` product has a remediation.
- [ ] The filename follows §5.1, and the year folder matches `initial_release_date` when directory-based distribution is used.
- [ ] Hash (`.sha256` or `.sha512`) and signature (`.asc`) files exist for trusted providers and are listed in the ROLIE entry with `rel` `hash` and `signature`.
- [ ] TLP:AMBER and TLP:RED documents are not on the public path.
- [ ] Nothing emits `csaf_version` `2.1` or a CSAF 2.1-only field or profile.

## Reference index

- **`references/versions.md`**: CSAF 2.0, the CSAF 2.1 draft and CVRF 1.2, which to use, what changed, the CVRF to CSAF 2.0 conversion, and what a CSAF 2.0 to 2.1 upgrade will involve. Load for steps 1 and 10.
- **`references/document-model.md`**: the `document`, `product_tree` and `vulnerabilities` properties, product identification helpers, versioning rules, filename and sorting conventions, and common mistakes. Load for steps 2 to 4 and 6.
- **`references/profiles-and-vex.md`**: the five CSAF 2.0 profiles, category naming rules, the VEX profile with its justification flags, a VEX example, and the CSAF 2.1 profiles to watch. Load for steps 2 and 5.
- **`references/tests-and-conformance.md`**: mandatory, optional and informative tests, the 17 conformance targets, and validator levels. Load for step 7 and when building tools.
- **`references/distribution.md`**: the 23 distribution requirements, the five roles, `provider-metadata.json`, `aggregator.json`, ROLIE feeds, integrity and signatures, retrieval rules, and security considerations. Load for steps 8 and 9.

## Related skills

- `openvex`, for the OpenVEX format, an alternative to CSAF VEX: `npx skills add ScaleDockHQ/scaledock-skills --skill openvex`
- `cyclonedx`, for SBOMs referenced from `sbom_urls` and `x_generic_uris`, and CycloneDX VEX: `npx skills add ScaleDockHQ/scaledock-skills --skill cyclonedx`
- `purl`, for the package URLs in `product_identification_helper.purl` and the `vers` ranges: `npx skills add ScaleDockHQ/scaledock-skills --skill purl`
- `osv`, for the OSV vulnerability format used by open source databases: `npx skills add ScaleDockHQ/scaledock-skills --skill osv`
- `eu-cra`, for the EU Cyber Resilience Act vulnerability handling and reporting duties that advisories support: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-cra`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Common Security Advisory Framework Version 2.0](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html): OASIS Standard, 18 November 2022, checked 2026-10-05.
- [CSAF Version 2.0 Errata 01](https://docs.oasis-open.org/csaf/csaf/v2.0/errata01/os/csaf-v2.0-errata01-os.html): OASIS Approved Errata, 26 January 2024 (aggregator schema fix only), checked 2026-10-05.
- [CSAF 2.0 latest stage](https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html): OASIS Standard with Approved Errata 01; this URL now serves the Errata 01 document, checked 2026-10-05.
- [CSAF 2.0 JSON schema](https://docs.oasis-open.org/csaf/csaf/v2.0/csaf_json_schema.json): OASIS Standard, 2.0 (JSON Schema draft 2020-12), checked 2026-10-05.
- [CSAF 2.0 provider metadata JSON schema](https://docs.oasis-open.org/csaf/csaf/v2.0/provider_json_schema.json): OASIS Standard, 2.0, checked 2026-10-05.
- [CSAF 2.0 aggregator JSON schema](https://docs.oasis-open.org/csaf/csaf/v2.0/aggregator_json_schema.json): OASIS Approved Errata, 2.0 Errata 01, checked 2026-10-05.
- [CSAF 2.0 known issues](https://github.com/oasis-tcs/csaf/blob/master/csaf_2.0/known_issues.md): TC repository note, master at e0da5a9 (2026-09-13), checked 2026-10-05.
- [Common Security Advisory Framework Version 2.1 (CSD03)](https://docs.oasis-open.org/csaf/csaf/v2.1/csd03/csaf-v2.1-csd03.html): Committee Specification Draft 03, 11 September 2026; Draft posture: track, checked 2026-10-05.
- [CSAF 2.1 stage index](https://docs.oasis-open.org/csaf/csaf/v2.1/): stage listing, latest stage is CSD03 (csd01, csd02, csd03; no CS), checked 2026-10-05.
- [CSAF 2.1 JSON schema](https://docs.oasis-open.org/csaf/csaf/v2.1/schema/csaf.json): Committee Specification Draft 03, 2026-09-11; Draft posture: track, checked 2026-10-05.
- [oasis-tcs/csaf](https://github.com/oasis-tcs/csaf): TC repository, master at e0da5a9 (2026-09-13), release tag csaf-2.1-csd-03-20260911-rc1, checked 2026-10-05.
- [CSAF Common Vulnerability Reporting Framework (CVRF) Version 1.2](https://docs.oasis-open.org/csaf/csaf-cvrf/v1.2/csaf-cvrf-v1.2.html): Committee Specification 01, 13 September 2017, checked 2026-10-05.
- [CSAF documentation site](https://oasis-open.github.io/csaf-documentation/): TC documentation site, as of 2026-10-05, checked 2026-10-05.
