---
name: cisa-kev
description: >-
  CISA KEV: prioritize vulnerability fixes with the Known Exploited Vulnerabilities catalog. Covers CISA KEV. Use when checking the Known Exploited Vulnerabilities catalog. Triggers: KEV.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# CISA KEV

The CISA Known Exploited Vulnerabilities (KEV) catalog: the fields of each catalog entry from the KEV JSON schema in the cisagov/kev-data repository at a pinned commit, the remediation requirements of Binding Operational Directive 26-04, which now governs the catalog, and the catalog's inclusion and removal criteria.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Vulnerability management owner, a tool that ingests the KEV feed, or a Federal Civilian Executive Branch agency subject to BOD 26-04.
- Target version: CISA KEV (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **cveID.** "The CVE ID of the vulnerability in the format CVE-YYYY-NNNN, note that the number portion can have more than 4 digits"
2. **BOD 26-04 Phase I.** "Monitor KEV Catalog updates and aggressively mitigate vulnerabilities in accordance with the KEV remediation timelines."
3. **BOD 26-04 Phase III.** "Remediate each vulnerability as quickly as possible and no later than the timelines set forth in Table 1: Remediation Timelines."
4. **BOD 26-04 Appendix A.** "The text “& forensic triage” means that the agency must complete remediation or mitigation action within the timeline (three days) and carry out a forensic triage of the asset to assess whether the system is compromised."
5. **BOD 22-01 FAQ.** "There are three criteria for adding a vulnerability to the KEV: (1) a CVE ID; (2) clear remediation guidance, and (3) reliable evidence of exploitation in the wild."

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
- [ ] The KEV feed is parsed against the pinned schema, and each matched CVE records its `dateAdded`, `dueDate`, `requiredAction` and `forensicTriage` values.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `ssvc`, `epss`, `cvss`, `cve-json`, `cwe`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [KEV catalog JSON schema (cisagov/kev-data)](https://raw.githubusercontent.com/cisagov/kev-data/b244ed1a640323565afba92100d7308d51c6614e/known_exploited_vulnerabilities_schema.json): CISA data schema, Commit b244ed1a6403 (2026-10-04), checked 2026-10-06.
- [BOD 26-04: Prioritizing Security Updates Based on Risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk): Binding Operational Directive, Issued June 10, 2026, checked 2026-10-06.
- [BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked)](https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities): Binding Operational Directive (revoked), Issued November 3, 2021; revoked June 10, 2026, checked 2026-10-06.
