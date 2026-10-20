---
name: bsi-tr-03183
description: >-
  BSI TR-03183 Cyber Resilience Requirements: CRA-aligned risk assessment, SBOMs and vulnerability reporting for manufacturers. Covers Part 1 General requirements 1.0.0, Part 2 SBOM 2.1.0 (CycloneDX 1.6 or SPDX 3.0.1, with 2.0.0 and 1.1 legacy), and Part 3 Vulnerability Reports and Notifications 1.0.0. Use when producing a TR-03183-compliant SBOM, setting up security.txt, a CVD policy and PSIRT contacts, or running a CRA cybersecurity risk assessment. Triggers: BSI TR-03183, TR-03183-2, BSI SBOM, CRA SBOM, coordinated vulnerability disclosure, security.txt, PSIRT.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# BSI TR-03183

BSI Technical Guideline TR-03183, Cyber Resilience Requirements for Manufacturers and Products, from the German Federal Office for Information Security. Part 1 sets general requirements and a CRA risk-assessment process, Part 2 sets the content and format of Software Bills of Materials, and Part 3 sets how manufacturers receive and handle vulnerability reports.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Manufacturer of a product with digital elements (risk assessment, SBOM, CVD process), or a tool that generates or checks TR-03183 SBOMs.
- Target version: TR-03183-1 1.0.0 (current); TR-03183-2 2.1.0 (current); TR-03183-2 2.0.0 (legacy); TR-03183-2 1.1 (legacy); TR-03183-3 1.0.0 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 5.8.1.1.3.** "The manufacturer MUST identify all assets of the PwDE."
2. **§ 5.12.3.** "The manufacturer MUST document the results of the risk assessment in a comprehensive manner."
3. **§ 5.13.3.** "The manufacturer MUST update the risk assessment when the risk context of the PwDE changes and treat new unaccepted risks accordingly."
4. **§ 3.1.** "A separate SBOM MUST be generated for each software version."
5. **§ 3.1.** "An SBOM MUST NOT contain vulnerability information, because SBOM data is static with respect to software that is not changing."
6. **§ 4.** "A newly generated or updated SBOM MUST be in JSON-or XML-format and a valid SBOM according to one of the following specifications in one of the specified versions:"
7. **§ 6.1.** "Licences MUST be referred to (in the sense of “named”) by their appropriate SPDX licence identifier or licence expression based on such an identifier."
8. **§ 4.2.** "To make it easier for the reporting entity to find the right contact for vulnerability reports, a security.txt in accordance with RFC 9116 MUST be created and made available on the manufacturer's website."
9. **§ 4.2.10.** "The manufacturer MUST digitally sign its security.txt using OpenPGP according to RFC 958022."
10. **§ 4.3.1.** "The manufacturer MUST create at least two roles of responsible cybersecurity contacts, its PSIRT and its CSIRT."
11. **§ 4.4.8.** "The manufacturer MUST ensure that a simple response to a vulnerability report or an update of an existing report is provided within five working days, unless a vulnerability was reported anonymously."
12. **§ 4.4.10.** "The manufacturer MUST ensure that validated and verified vulnerabilities are publicly disclosed within 90 days, unless the manufacturer becomes aware of a vulnerability and fixes it before the affected product is placed on the market."

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
- [ ] A TR-03183-2 SBOM validates as CycloneDX 1.6+ or SPDX 3.0.1+ and has every field in § 5.2.1 and § 5.2.2.
- [ ] security.txt is at /.well-known/security.txt, OpenPGP-signed, and lists English as a preferred language.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `eu-cra`, `cyclonedx`, `spdx`, `security-txt`, `csaf`, `openpgp`, `purl`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [BSI TR-03183-1: General requirements](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile): Technical Guideline, Version 1.0.0, 2025-07-31, checked 2026-10-06.
- [BSI TR-03183-2: Software Bill of Materials (SBOM)](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile): Technical Guideline, Version 2.1.0, 2025-08-20, checked 2026-10-06.
- [BSI TR-03183-3: Vulnerability Reports and Notifications](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile): Technical Guideline, Version 1.0.0, 2025-08-20, checked 2026-10-06.
