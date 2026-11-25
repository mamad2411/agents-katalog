---
name: control-mapping
description: Guides mapping one finding or control across ISO 27001, NIST CSF/800-53, SOC 2 and CIS Controls so it is assessed once and satisfies many. Use when the user asks how a control or finding maps between frameworks, wants a crosswalk, or needs to report one assessment against several standards.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Control mapping (assess once, report many)

A finding implicates the same control under every framework. Map it once so you
don't reassess per-standard, and so one fix can close N audit line items.

This skill is framework↔framework. To map a finding to the regulatory/OT obligations
it touches (IEC 62443-3-3 SRs, EU CRA Annex I, NIS2 Art. 21(2)), `load_skill finding-control-crosswalk`.

## Workflow

1. Take the finding: `read_file /work/findings.md` (or a single `report_finding` entry).
   Identify the control _intent_ (e.g. "user input isn't validated" -> input validation /
   secure development).
2. Anchor on the CWE the finding already carries; it's your pivot into framework controls.
3. Pull the equivalent control id in each in-scope framework. Versions change ids and
   wording: `load_skill control-frameworks` for the current catalogues and web-fetch the current text; the table
   below is a starting pointer, confirm the live id before you cite it in a deliverable.
4. Write the mapping row. One fix recommendation, tagged with every framework id it satisfies.

## Pivot table (verify ids against current versions)

| Theme (CWE pivot)                            | ISO 27001:2022 Annex A | NIST CSF 2.0 | NIST 800-53      | SOC 2 (TSC)  | CIS v8.1 |
| -------------------------------------------- | ---------------------- | ------------ | ---------------- | ------------ | -------- |
| Access control / least priv (CWE-284/639)    | A.5.15, A.5.18, A.8.3  | PR.AA        | AC-2, AC-3, AC-6 | CC6.1-6.3    | 5, 6     |
| Authentication (CWE-287/798)                 | A.5.17, A.8.5          | PR.AA-01/02  | IA-2, IA-5       | CC6.1        | 5, 6     |
| Crypto / data protection (CWE-311/327)       | A.8.24, A.5.34         | PR.DS        | SC-13, SC-28     | CC6.7        | 3        |
| Input validation / injection (CWE-79/89/918) | A.8.28, A.8.26         | PR.PS        | SI-10, SC-7      | CC7.1, CC8.1 | 16       |
| Vuln & patch mgmt (CWE-1104)                 | A.8.8                  | ID.RA, PR.PS | RA-5, SI-2       | CC7.1        | 7        |
| Logging & monitoring (CWE-778)               | A.8.15, A.8.16         | DE.CM        | AU-2, AU-6       | CC7.2        | 8        |
| Secure config / hardening (CWE-16)           | A.8.9                  | PR.PS-01     | CM-6, CM-7       | CC7.1        | 4        |
| Secrets exposure (CWE-798/200)               | A.8.24, A.5.10         | PR.DS, PR.AA | IA-5, SC-12      | CC6.1        | 3, 16    |
| Network segmentation (CWE-668)               | A.8.20, A.8.22         | PR.IR        | SC-7             | CC6.6        | 12, 13   |
| Backup / resilience (CWE-...)                | A.8.13, A.5.29         | RC.RP, PR.IR | CP-9, CP-10      | A1.2         | 11       |

## Output

`write_file /work/control-map.md`:

| Finding/risk ref | CWE | Theme | ISO | NIST CSF | SOC 2 | CIS | One remediation | Status |
| ---------------- | --- | ----- | --- | -------- | ----- | --- | --------------- | ------ |

- Write one remediation as a single fix line, then the list of control ids it
  closes, so auditors for different standards each see their id satisfied.
- Roll up: count distinct controls touched per framework to show coverage from the
  engagement ("these findings touch 14 of ISO Annex A's controls").

## Rules

- Map by control _intent_, not keyword. A CWE can land in two themes; list both rows.
- Don't claim a framework id you haven't read the current text of; mark unverified rows.
- A divergent finding severity vs control criticality is signal; note it, don't smooth it.
