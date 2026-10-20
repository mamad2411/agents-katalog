<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ch4os1
description: CTF writeups and security challenges by Ch4os1.
---

# Writeups by Ch4os1

Source repository: `/repos/Ch4os1`

## Repository Index

- Demo-Pentest-Reports/README.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/README.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Admin/Admin Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Deliverables/Deliverables Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Retest/Retest Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Findings/Finding Template.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Findings/Findings Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Logging output/Logging Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Misc files/Misc Files Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/1. Administrative Information.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/10. AD Enumeration Research.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/11. Attack Path.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/12. Findings.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/2. Scoping Information.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/3. Activity Log.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/4. Payload Log.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/5. OSINT Data.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/6. Credentials.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/7. Web Application Research.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/8. Vulnerability Scan Research.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/9. Service Enumeration Research.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/Notes Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/OSINT/OSINT Gist.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Wireless/Wireless Scan.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/AD Enumeration/AD Enumeration.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Service/Service Enumeration.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Vuln/Vuln Scan.md
- Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Web/Web Enumeration.md

## Writeup Content


### File: Demo-Pentest-Reports/README.md

# Demo-Pentest-Reports



### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/README.md

# Penetration-Testing-Report-Template

## 🎯 Purpose
This template provides a standardized structure for:
- Organizing evidence systematically during engagements
- Maintaining consistent documentation across multiple testers
- Streamlining report generation with pre-structured findings
- Tracking engagement progress through detailed note-taking
- Facilitating peer reviews with clear organization
## 📁Template Folder Structure 

```bash
.
└── {Client-Name} Penetration Test/
    ├── Admin/                          # Administrative documents
    ├── Deliverables/                   # Final client deliverables
    ├── Evidence/                       # All engagement evidence
    │   ├── Findings/                   # Individual vulnerability write-ups
    │   │   ├── H1 - Kerberoasting.md
    │   │   ├── H2 - ASREPRoasting.md
    │   │   ├── H3 - LLMNR&NBT-NS Response Spoofing.md
    │   │   └── H4 - Tomcat Manager Weak Credentials.md
    │   ├── Logging output/             # Tool logs and outputs
    │   ├── Misc files/                 # Miscellaneous evidence
    │   ├── Notes/                      # Engagement documentation
    │   │   ├── 1. Administrative Information.md
    │   │   ├── 2. Scoping Information.md
    │   │   ├── 3. Activity Log.md
    │   │   ├── 4. Payload Log.md
    │   │   ├── 5. OSINT Data.md
    │   │   ├── 6. Credentials.md
    │   │   ├── 7. Web Application Research.md
    │   │   ├── 8. Vulnerability Scan Research.md
    │   │   ├── 9. Service Enumeration Research.md
    │   │   ├── 10. AD Enumeration Research.md
    │   │   ├── 11. Attack Path.md
    │   │   └── 12. Findings.md
    │   ├── OSINT/                      # Open Source Intelligence
    │   ├── Scans/                      # Scan results organized by type
    │   │   ├── AD Enumeration/
    │   │   ├── Service/
    │   │   ├── Vuln/
    │   │   └── Web/
    │   └── Wireless/                   # Wireless testing evidence
    └── Retest/                         # Retest evidence and documentation
```

## 🚀 Usage
1. Clone this repository
```bash
git clone https://github.com/your-username/Penetration-Testing-Report-Template.git
```
2. Create a new engagement folder
```bash
cp -r "Inlanefreight Penetration Test" "{New-Client} Penetration Test"
```
3. Customize for your engagement
	- Update administrative documents in Admin/
	- Modify scoping information in Evidence/Notes/
	- Adapt finding templates as needed
4. Populate during testing
	- Add evidence to appropriate subdirectories
	- Maintain detailed notes in chronological order
	- Document findings as they're discovered

## 🔒 Security Note
- Never store actual client data in this template
- Use placeholder data for demonstration purposes only
- Always follow responsible disclosure practices
- Ensure proper encryption for sensitive engagement data

## 🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests for:
- Additional template structures
- Improved documentation
- New finding categories
- Automation scripts

## 🙏 Acknowledgments
Inspired by CPTS [Documentation & Reporting Module](https://academy.hackthebox.com/module/details/162)




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Admin/Admin Gist.md

Admin: Scope of Work (SoW) that you're working off of, your notes from the project kickoff meeting, status reports, vulnerability notifications, etc


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Deliverables/Deliverables Gist.md

Deliverables: Folder for keeping your deliverables as you work through them. This will often be your report but can include other items such as supplemental spreadsheets and slide decks, depending on the specific client requirements.

Final client-facing materials:
- Executive Summary
- Technical Report
- Presentation decks
- Remediation tracking sheets


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Findings/Finding Template.md

# H1 - Vulnerability Name

**Risk Rating:** High  
**CVSS Score:** 7.5  
**Affected Systems:** [System/Application Name]

## Description
Brief description of the vulnerability...

## Proof of Concept
1. Step-by-step reproduction steps
2. Commands used
3. Screenshots/outputs

## Impact
What an attacker could achieve...

## Remediation Recommendations
- Specific, actionable fixes
- Code snippets if applicable
- Configuration changes

## References
- [OWASP Guide](https://example.com)
- [CVE Details](https://example.com)


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Findings/Findings Gist.md

- After the Executive Summary, the Findings section is one of the most important. This section gives us a chance to show off our work, paint the client a picture of the risk to their environment, give technical teams the evidence to validate and reproduce issues and provide remediation advice. 
- Primary objective should be present evidence in a way that is understandable and actionable to the client 

### Breakdown of a Finding
- Findings should cater towards each client's specific circumstances
- If a finding is written to suit several different scenarios or protocols, the finial version should be adjusted to only reference the particular circumstances we have identified 
- At a minimum the following information should be include for every finding:
	- Description of the finding and what platform(s) the vulnerability affects
	- Impact if the finding is left unresolved
	- Affected systems, networks, environments, or applications
	- Recommendation for how to address the problem
	- Reference links with additional information about the finding and resolving it
- Some additional, optional fields include:
	- CVE
	- OWASP, MITRE IDs
	- CVSS or similar score 
	- Ease of exploitation and probability of attack
	- Any other information that might help learn about and mitigate the attack 

### Findings Naming Scheme
- Ensure the findings reflect the risk-based naming scheme
```bash
Evidence/Findings/
├── Critical - Kerberoasting Attack.md
├── High - ASREPRoasting Attack.md
├── Medium - LLMNR_NBT-NS Poisoning.md
└── Medium - Tomcat Weak Credentials.md
```


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Logging output/Logging Gist.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Misc files/Misc Files Gist.md

Misc Files: Web shells, payloads, custom scripts, and any other files generated during the assessment that are relevant to the project.


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/1. Administrative Information.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/10. AD Enumeration Research.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/11. Attack Path.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/12. Findings.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/2. Scoping Information.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/3. Activity Log.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/4. Payload Log.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/5. OSINT Data.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/6. Credentials.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/7. Web Application Research.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/8. Vulnerability Scan Research.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/9. Service Enumeration Research.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Notes/Notes Gist.md

 A folder to keep your notes in.


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/OSINT/OSINT Gist.md

- OSINT: Any OSINT output from tools like Intelx and Maltego that doesn't fit well in your notes document.


### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/AD Enumeration/AD Enumeration.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Service/Service Enumeration.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Vuln/Vuln Scan.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Scans/Web/Web Enumeration.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Evidence/Wireless/Wireless Scan.md




### File: Demo-Pentest-Reports/Shibuya/Penetration-Testing-Report-Template/Retest/Retest Gist.md

Evidence from remediation validation:
- Retest results
- Verification of fixes
- Updated risk assessments
