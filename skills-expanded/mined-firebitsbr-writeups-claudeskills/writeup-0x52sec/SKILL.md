<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0x52sec
description: CTF writeups and security challenges by 0x52sec.
---

# Writeups by 0x52sec

Source repository: `/repos/0x52sec`

## Repository Index

- report-templates/Appendix_Methodology.md
- report-templates/Executive_Summary.md
- report-templates/Findings_Template.md
- report-templates/README.md

## Writeup Content


### File: report-templates/README.md


# Penetration Test Report Templates

- Executive_Summary.md — business-readable overview
- Findings_Template.md — per-finding structure with CVSS & remediation
- Appendix_Methodology.md — scope, rules, tooling

Feel free to adapt; keep client data anonymized.



### File: report-templates/Appendix_Methodology.md


# Methodology (Appendix)

- Standards: OWASP WSTG, ASVS, NIST SP 800-115
- Approach: Recon → Threat modeling → Exploitation (authorized) → Post-exploitation (as scoped) → Reporting
- Tools: Burp Suite, custom Python, Docker labs



### File: report-templates/Executive_Summary.md


# Executive Summary

**Engagement**: <Client / System>  
**Dates**: <Start–End>  
**Scope**: <Hosts/Apps/APIs>  
**Overall Risk**: <Low/Med/High>

## Key Risks
- <Finding A>
- <Finding B>

## Recommendations
- <Priority 1>
- <Priority 2>



### File: report-templates/Findings_Template.md


# <Finding Title>

**Severity**: <Low/Med/High/Critical> (CVSS: <vector>)  
**Category**: <e.g., AuthZ / Crypto / Config>  
**Affected**: <host/app endpoint>

## Description
<What, where, impact>

## Evidence (sanitized)
<Requests/responses, screenshots from lab when possible>

## Reproduction (lab)
<Steps against a local reproduction or redacted details>

## Remediation
<Actionable fix, secure-by-default config>

## References
- <OWASP/WSTG/CWE link>

