<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-full-secure
description: CTF writeups and security challenges by full-secure.
---

# Writeups by full-secure

Source repository: `/repos/full-secure`

## Repository Index

- Pentest-Reports/README.md
- Pentest-Reports/Active-Directory-Assessment/README.md
- Pentest-Reports/Cloud-Security-Assessment/README.md
- Pentest-Reports/External-Network-Assessment/README.md
- Pentest-Reports/Internal-Network-Assessment/README.md
- Pentest-Reports/Mobile-Application-Assessment (Android-iOS)/README.md
- Pentest-Reports/Physical-Security-Assessment/README.md
- Pentest-Reports/Social-Engineering-Assessment/README.md
- Pentest-Reports/WebApp-Assessment/README.md

## Writeup Content


### File: Pentest-Reports/Active-Directory-Assessment/README.md

# Active Directory Assessment Report

This directory contains the penetration testing report, methodology, and supporting evidence for an **Active Directory (AD) security assessment**.  
The assessment focuses on identifying misconfigurations, privilege escalation paths, insecure policies, and attack vectors commonly exploited within Windows domain environments.

---

## 📁 Folder Structure

```
Active-Directory-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── output logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose of This Assessment

This assessment aims to:

- Evaluate the security posture of an Active Directory domain  
- Identify weaknesses enabling lateral movement, persistence, or privilege escalation  
- Demonstrate real-world attack paths from initial foothold to full domain compromise  
- Provide remediation guidance aligned with best practices  

---

## 🧪 Methodology

The assessment aligns with recognised security frameworks such as:

- **MITRE ATT&CK**  
- **NIST 800-115**  
- **PTES**  
- **AD privilege escalation path modelling (BloodHound)**  

Key activities included:

- Domain enumeration  
- Kerberos-based attack techniques  
- Password policy and authentication weakness review  
- Privilege escalation mapping  
- Lateral movement simulation  
- Persistence mechanism analysis  

---

## 📜 Report Contents

The `report.pdf` includes:

- Executive summary  
- Scope and objectives  
- Methodology  
- Technical findings  
- Evidence  
- Remediation guidance  

---

## 🛡 Legal and Ethical Notice

This assessment was conducted in an authorised lab environment or intentionally vulnerable domain.  
No unauthorised systems were accessed.

---

## 📬 Contact

**LinkedIn:** linkedin.com/in/johnrhodessec  
**Website:** fullsec.co.uk




### File: Pentest-Reports/Cloud-Security-Assessment/README.md

# Cloud Security Assessment Report

This directory contains the penetration testing report, methodology, and supporting evidence for a **Cloud Security Assessment**.  
The assessment evaluates security risks, misconfigurations, identity weaknesses, and attack paths within cloud environments such as AWS, Azure, and GCP.

---

## 📁 Folder Structure

```
Cloud-Security-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose of This Assessment

This assessment aims to:

- Identify misconfigurations within cloud infrastructure  
- Evaluate IAM policies and privilege boundaries  
- Assess public exposure of cloud assets and services  
- Analyse logging, monitoring, and incident response readiness  
- Demonstrate real-world attack paths and cloud exploitation techniques  
- Provide remediation aligned with industry best practices (CIS, NIST, vendor guidelines)  

---

## 🧪 Methodology

The assessment aligns with recognised cloud security frameworks:

- **CIS Benchmarks (AWS, Azure, GCP)**  
- **MITRE ATT&CK (Cloud Matrix)**  
- **NIST 800-53 & 800-171**  
- **OWASP Cloud Security Top 10**  

Testing activities included:

- Identity & Access Management (IAM) enumeration  
- Policy and permission boundary analysis  
- Misconfigured storage review (S3 buckets, Azure Blobs, GCP buckets)  
- Network exposure and security group inspection  
- Key, token, and credential leakage testing  
- Logging and monitoring validation  
- Privilege escalation path discovery  

---

## 📜 Report Contents

The included `report.pdf` provides:

- Executive summary  
- Scope and cloud environment overview  
- Detailed methodology  
- Technical findings  
- Impact analysis  
- Supporting evidence  
- Remediation guidance  

---

## 🛡 Legal and Ethical Notice

All testing was performed against authorised cloud accounts, sandboxes, or intentionally vulnerable lab environments.  
No unauthorised access to production systems occurred.

---

## 📬 Contact

**LinkedIn:** linkedin.com/in/johnrhodessec  
**Website:** fullsec.co.uk




### File: Pentest-Reports/External-Network-Assessment/README.md

# External Network Assessment Report

This directory contains the penetration testing report, methodology, and supporting evidence for an **External Network Security Assessment**.
The assessment focuses on evaluating publicly exposed services, external attack surfaces, and security risks from an unauthenticated outsider perspective.

---

## 📁 Folder Structure
```
External-Network-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose of This Assessment

- Identify externally exposed vulnerabilities  
- Evaluate misconfigurations in internet-facing services  
- Assess risks related to network perimeter security  
- Validate findings against real-world attacker behaviour  
- Provide mitigation recommendations aligned with best practice  

---

## 🧪 Methodology

Aligned with:
- **OWASP ASVS**
- **NIST 800-115**
- **MITRE ATT&CK (Initial Access)**

Techniques include:
- Port and service enumeration  
- External recon/OSINT  
- Vulnerability analysis  
- Exploitation validation  
- SSL/TLS configuration review  

---

## 🛡 Legal and Ethical Notice

All testing performed against authorised hosts only.

---

## 📬 Contact

LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk




### File: Pentest-Reports/Internal-Network-Assessment/README.md

# Internal Network Assessment Report

This directory contains the penetration testing report and supporting artefacts for an **Internal Network Security Assessment**.
The assessment evaluates risks present from an attacker with internal network access.

---

## 📁 Folder Structure
```
Internal-Network-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose of This Assessment

- Identify internal network weaknesses  
- Assess risks related to lateral movement  
- Evaluate device hardening, segmentation, and patch posture  
- Provide remediation focused on reducing internal compromise  

---

## 🧪 Methodology

Aligned with:
- **MITRE ATT&CK Enterprise**
- **NIST 800-53**
- **PTES**

Activities include:
- Network enumeration  
- SMB/LDAP/AD probing  
- Vulnerability identification  
- Credential harvesting  
- Lateral movement mapping  

---

## 🛡 Legal Notice

Performed only within authorised internal lab networks.

---

## 📬 Contact  
LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk




### File: Pentest-Reports/Mobile-Application-Assessment (Android-iOS)/README.md

# Mobile Application Security Assessment Report

This directory contains the penetration testing report and evidence for a **Mobile Application Security Assessment** (Android/iOS).

---

## 📁 Folder Structure
```
Mobile-Application-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose

- Evaluate mobile application security posture  
- Identify insecure data storage, authentication flaws, API weaknesses  
- Assess compliance with OWASP MASVS standards  

---

## 🧪 Methodology

Aligned with:
- **OWASP MASVS**
- **OWASP MASTG**

Activities include:
- Static analysis  
- Dynamic analysis  
- Network traffic inspection  
- API interaction review  
- Authentication & session testing  

---

## 🛡 Legal Notice

Testing restricted to authorised mobile applications and lab builds.

---

## 📬 Contact  
LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk




### File: Pentest-Reports/Physical-Security-Assessment/README.md

# Physical Security Assessment Report

This directory contains documentation and evidence for a **Physical Security Assessment**, evaluating on‑site controls and access vulnerabilities.

---

## 📁 Folder Structure
```
Physical-Security-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── photos...
│   ├── notes...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose

- Assess access control weaknesses  
- Identify bypass opportunities  
- Evaluate visitor, staff, and facility security posture  
- Provide practical improvements for physical defence  

---

## 🧪 Methodology

Includes:
- Perimeter inspection  
- Lock & access control review  
- CCTV & monitoring assessment  
- Social engineering resilience checks  

Aligned with:
- **NIST 800-53 Physical Controls**
- **PTES Physical Testing**

---

## 🛡 Legal Notice

All activities performed under explicit written authorisation.

---

## 📬 Contact  
LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk




### File: Pentest-Reports/README.md

# Pentest Reports

This repository is used to store a collection of penetration testing reports created to demonstrate methodology, documentation standards, and technical skills across different testing scenarios, including web applications, internal networks, mobile, cloud, and APIs.

## 📁 Repository Structure

```
pentest-reports/
│
├── 01-Web-Application/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 02-Internal-Network-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 03-External-Network-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 04-Mobile-Application-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 05-Cloud-Security-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 06-Active-Directory-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 07-Physical-Security-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
├── 06-Social-Engineering-Assessment/
│   ├── report.pdf
│   ├── evidence/
│   └── README.md
│
└── templates/
    └── pentest-report-template.md
```

## 🧭 Purpose

This repository is used to:

- Demonstrate penetration testing workflow and report-writing skills  
- Showcase the standard of documentation for technical and non-technical audiences  
- Track progress and development across different security domains  
- Maintain a professional portfolio for potential employers or clients

## 📜 Reporting Approach

Each report is designed to be:

- Clear and concise  
- Evidence-based and reproducible  
- Methodical and aligned with recognised testing frameworks  
- Understandable by technical and non-technical stakeholders  

A reusable report template is included in the `templates/` folder.

## 🛡 Legal and Ethical Notice

All reports in this repository are generated from authorised lab environments, intentionally vulnerable systems, or simulated assessments. No real-world systems were accessed.

## 🤝 Contributions

While primarily for personal development, contributions and suggestions to improve templates or structure are welcome.

## 📬 Contact

**LinkedIn:** linkedin.com/in/johnrhodessec  
**Website:** fullsec.co.uk  




### File: Pentest-Reports/Social-Engineering-Assessment/README.md

# Social Engineering Assessment Report

This directory contains documentation and evidence related to a **Social Engineering Assessment**, focused on human‑factor exploitation risk.

---

## 📁 Folder Structure
```
Social-Engineering-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── transcripts...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose

- Evaluate susceptibility to phishing, vishing, pretexting  
- Assess awareness, training gaps, and response behaviours  
- Provide actionable improvements  

---

## 🧪 Methodology

Aligned with:
- **MITRE ATT&CK (Initial Access – Phishing)**  
- **NCSC Social Engineering Guidance**

Includes:
- Email phishing campaigns  
- Payload analysis  
- Interaction logging  
- Behavioural response review  

---

## 🛡 Legal Notice

All activities were consensual, authorised, and controlled.

---

## 📬 Contact  
LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk




### File: Pentest-Reports/WebApp-Assessment/README.md

# Web Application Security Assessment Report

This directory contains the penetration testing report and supporting evidence for a **Web Application Security Assessment**.

---

## 📁 Folder Structure
```
WebApp-Assessment/
│
├── report.pdf
│
├── evidence/
│   ├── screenshots...
│   ├── logs...
│   └── artefacts...
│
└── README.md
```

---

## 🧭 Purpose

- Identify vulnerabilities in web applications  
- Assess authentication, input validation, access control, and session management  
- Provide remediation aligned with OWASP standards  

---

## 🧪 Methodology

Aligned with:
- **OWASP Web Security Testing Guide (WSTG)**
- **OWASP Top 10**

Activities include:
- Recon & enumeration  
- Authentication testing  
- Injection analysis  
- Access control evaluation  
- Business logic testing  
- Client-side security checks  

---

## 🛡 Legal Notice

Testing was conducted only against authorised applications.

---

## 📬 Contact  
LinkedIn: linkedin.com/in/johnrhodessec  
Website: fullsec.co.uk


