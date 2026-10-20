<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cyver-core
description: CTF writeups and security challenges by cyver-core.
---

# Writeups by cyver-core

Source repository: `/repos/cyver-core`

## Repository Index

- pentest-reporting-resources/readme.md
- pentest-reporting-resources/report_templates/PCI ASV Test Template - ATTESTATION OF SCAN COMPLIANCE.md
- pentest-reporting-resources/report_templates/PCI ASV Test Template - PCI EXECUTIVE REPORT.md
- pentest-reporting-resources/report_templates/PCI ASV Test Template - VULNERABILITY DETAILS.md
- pentest-reporting-resources/report_templates/pentest_report_template_OWASP_sample1.md

## Writeup Content


### File: pentest-reporting-resources/readme.md

# Welcome to Cyver Core Pentest Reporting Resources

Writing Pentest reporting can be a time consuming task. Our platform optimizes that process and removes most of the manual work. We share here some resources that are useful to pentesters to deliver quality reporting to their clients.



## Report Templates

The report templates are in Markdown (.md and .css) to be used in the platform.

* Sample Pentest Report Template

  * Sections:

    * Cover, Management Summary, Scope, Methodology, Summary of Findings

## Compliance norms

The compliance norms are in Excel and can be uploaded in the platform.

* OWASP ASVS 4.0 L1, L2, L3
* OWASP ASVS 5.0 L1, L2, L3
* OWASP ASVS IoT L3
* OWASP MASVS 1.2 L1, L2, L3 (Android + iOS)
* OWASP MASVS 2.1
* OWASP OTG 4
* OWASP API Security TOP 10 2019, 2023
* OWASP Mobile TOP 10 2023
* OWASP IoT TOP10
* OWASP TOP10 2017, 2021
* OWASP TOP10 for LLMs v1
* PCI DSS 3.2, 4.0.1
* SANS TOP 20
* Cyber Essentials Plus
* DigiD 2.0
* ISO27001
* PTES
* MITRE ATT\&CK®
* NIST Privacy Framework 1.0 Core

## Checklists

The checklists are in Excel and can be uploaded in the platform.

* OWASP ASVS 4.0 L1, L2, L3
* OWASP ASVS 5.0 L1, L2, L3
* OWASP ASVS IoT L3
* OWASP MASVS 1.2 L1, L2, L3 (Android + iOS)
* OWASP MASVS 2.1
* OWASP MASTG 1.7.0 L1, L2, L3 (Android + iOS)
* OWASP WSTG 4.2
* OWASP OTG 4
* OWASP API Security TOP 10 2019, 2023
* OWASP IoT TOP10
* OWASP Mobile TOP10 2023
* OWASP TOP 10 2017, 2021
* OWASP TOP 10 for LLMs v1
* OWASP TOP 25 CWE 2024
* PCI DSS 3.2, 4.0.1
* SANS TOP 20
* Cyber Essentials Plus
* DigiD 2.0
* ISO27001 2013, 2022
* VAPT
* Cyber Kill Chain
* CIS Critical Security Controls 8.1

## Finding Libraries

The checklists are in CSV and can be uploaded in the platform.

* MITRE ATT\&CK® Tactics
* MITRE ATT\&CK® Techniques
* MITRE ATT\&CK® Mitigations
* Common Weakness Enumeration (CWEs)



### File: pentest-reporting-resources/report_templates/PCI ASV Test Template - ATTESTATION OF SCAN COMPLIANCE.md

# ASV SCAN REPORT ATTESTATION OF SCAN COMPLIANCE

## A1. SCAN CUSTOMER INFORMATION

| **COMPANY** | {Client_Name} |
| --- | --- |
| **CONTACT NAME** | {Client_MainContact_Name} |
| **JOB TITLE** | {Client_MainContact_Function} |
| **E-MAIL** | {Client_MainContact_Email} |
| **TELEPHONE** | {Client_MainContact_Phone} |
| **BUSINESS ADDRESS** | {Client_Address_Street} |
| **COUNTRY** | {Client_Address_Country} |
| **CITY** | {Client_Address_City} |
| **STATE/PROVINCE** | {Client_Address_StateProvince} |
| **ZIP/POSTAL CODE** | {Client_Address_PostalCode} |
| **WEBSITE/ URL** | {Client_Website} |

A2. APPROVED SCANNING VENDOR INFORMATION

| **COMPANY** |   |
| --- | --- |
| **CONTACT NAME** |   |
| **JOB TITLE** |   |
| **E-MAIL** |   |
| **TELEPHONE** |   |
| **BUSINESS ADDRESS** |   |
| **COUNTRY** |   |
| **CITY** |   |
| **STATE/PROVINCE** |   |
| **ZIP/POSTAL CODE** |   |
| **WEBSITE/ URL** |   |

A3. SCAN STATUS

| DATE SCAN WAS COMPLETED |   |
| --- | --- |
| COMPLIANCE STATUS |   |
| SCAN EXPIRATION DATE (90 DAYS FROM THE DATE SCAN COMPLETED) |   |
| SCAN REPORT TYPE |   |

| NUMBER OF UNIQUE IN-SCOPE COMPONENTS SCANNED | ==0== |
| --- | --- |
| **NUMBER OF IDENTIFIED FAILING VULNERABILITIES** | ==**0**== |
| **NUMBER OF COMPONENTS FOUND BY ASV BUT NOT SCANNED BECAUSE SCAN CUSTOMER CONFIRMED THEY WERE OUT OF SCOPE** | ==**0**== |

## A4. SCAN STATUS

{Client_Name} attests on ==**DATE SCAN WAS COMPLETED**== that this scan (either by itself or combined with multiple, partial, or failed scans/rescans, as indicated in the above Section A.3, “Scan Status”) includes all components which  
should be in scope for PCI DSS, any component considered out of scope for this scan is properly segmented from my cardholder data environment, and any evidence submitted to the ASV to resolve scan exceptions—including compensating controls if applicable—is accurate and complete. {Client_Name} also acknowledges 1) accurate and complete scoping of this external scan is my responsibility, and 2) this scan result only indicates whether or not my scanned systems are compliant with the external vulnerability scan requirement of PCI DSS; this scan result does not  
represent my overall compliance status with PCI DSS or provide any indication of compliance with other PCI DSS requirements.

## A5. ASV ATTESTATION

This scan and report was prepared and conducted by ==Company== under certificate number ==XXXX-XX-XX==, according to internal processes that meet PCI DSS Requirement 11.2.2 and the ASV Program Guide.  
==Company== attests that PCI DSS scan process was followed, including a manual or automated Quality Assurance process with customer boarding and scoping practices, review of results for anomalies, and review and correction of 1) disputed or incomplete results, 2) false positives, 3) compensating controls (if applicable), and 4) active scan interference. This report and any exceptions were reviewed by RA ASV Support.



### File: pentest-reporting-resources/report_templates/PCI ASV Test Template - PCI EXECUTIVE REPORT.md

# PCI EXECUTIVE REPORT

## Part 1. Scan Information

| Scan Information |   |
| --- | --- |
| Scan Customer Company: | {Client_Name} |
| ASV Company: | ==Company== |
| Scan expiration date: | ==VALUE== |
| Date scan was completed: | ==VALUE== |

## Part 2. Component Compliance Summary

{PCICompliance_AssetsCompliance_Table}

## Part 3a. Vulnerabilities Noted for each IP Address

{PCICompliance_EvidenceCompliance_GroupByAsset_Table}

### Consolidated Solution/Correction Plan for the above IP Address:

**For HTTPS**

These vulnerabilities can be resolved by performing the following 2 steps. The total estimated time to perform all of these steps is 3 hours 30 minutes.

| Remediation Step | Estimated Time |
| --- | --- |
| Obtain a new certificate from your CA and ensure the server configuration is correct | 1 hour 30 minutes |
| Upgrade to the latest version of OpenSSL | 2 hours |

## Part 3b. Special Notes by IP Address

| Components | Special Note to Scan Customer | Item Noted | Per section 7.2 of the ASV Program Guide, scan customer’s description of action taken and declaration that software is either needed for business and implemented securely, or removed |
| --- | --- | --- | --- |
| N/A | N/A | N/A | N/A |
| Not any | Not any | Not any | Not any |

## Part 3c. Special Notes – Full Text

NOTE 1 - Note to scan customer: Browsing of directories on web servers can lead to information disclosure or potential exploit. Due to increased risk to the cardholder data environment, please 1) justify the business need for this configuration to the ASV, or 2) confirm that it is disabled. Please consult your ASV if you have questions about this Special Note.

NOTE 2 - Note to scan customer: Due to increased risk to the cardholder data environment when remote access software is present, please 1) justify the business need for this software to the ASV and confirm it is either implemented securely per Appendix D or disabled/removed. Please consult your ASV if you have questions about this Special Note.

NOTE 3 - Note to scan customer: Due to increased risk to the cardholder data environment when a point-of-sale system is visible on the Internet, please 1) confirm that this system needs to be visible on the Internet, that the system is implemented securely, and that original default passwords have been changed to complex passwords, or 2) confirm that the system has been reconfigured and is no longer visible to the Internet. Please consult your ASV if you have questions about this Special Note.

NOTE 4 - Note to customer: As you were unable to validate that the configuration of the environment behind your load balancers is synchronized, it is your responsibility to ensure that the environment is scanned as part of the internal vulnerability scans required by the PCI DSS.

Note 5 - Due to increased risk to the cardholder data environment when payment page scripts are present, 1) justify the business need for the script(s) to the ASV and confirm it is implemented securely, or 2) confirm it is disabled/removed. Consult your ASV if you have questions about this Special Note.

## Part 4a. Scope Submitted by Scan Customer for Discovery

{PCICompliance_Scope_Assets_List}

## Part 4b. Scan Customer Designated "In-Scope" Components (Scanned)

{PCICompliance_Scope_AssetsWithFindings_List}

## Part 4c. Scan Customer Designated "Out-of-Scope" Components (Not Scanned)

| IP Addresses/ranges/subnets, domains, URLs, etc. |
| --- |



### File: pentest-reporting-resources/report_templates/PCI ASV Test Template - VULNERABILITY DETAILS.md

# VULNERABILITY DETAILS

## Part 1. Scan Information

| Scan Information |   |
| --- | --- |
| Scan Customer Company: | {Client_Name} |
| ASV Company: | ==Company== |
| Scan expiration date: | ==VALUE== |
| Date scan was completed: | ==VALUE== |

## Part 2. Vulnerability Details

{Finding_Details?   
header_table.title=&   
header_table.fields=severity,cvss,impact,likelihood&  
header_table.cols=2&   
header_table.show_finding_title=true&   
group.1.fields=assets,description,occurrence&   
group.2.title=Classification&   
group.2.fields=impact,impact_description,likelihood,likelihood_description,vulnerability_types,cwes,cves,exploits&  
group.3.title=Recommendations&   
group.3.fields=background_information,remediation,external_url&  
group.4.title=Compliance&  
group.4.fields=compliance,compliance_status,pci_evidence_table&  
group.5.title=Evidences&  
group.5.fields=evidence_table,evidences&  setting.title.html_tag=h1&   
setting.title.display_severity=false&   
setting.title.show=true&    
setting.layout=headings&   
setting.evidences.layout=headings&   
setting.evidence_table.title=&    
setting.evidence_table.format=all&   
setting.assets.format=list1&   
setting.assets.display_count=30&  
setting.filter.type=Vulnerability   
}

{Finding_Details?   
group.1.fields=description&   
group.2.title=&   
group.2.fields=assets,occurrence&   
group.3.title=Classification&  
group.3.fields=severity,impact,impact_description,likelihood,likelihood_description,vulnerability_types,cwes,cves,exploits&    
group.4.title=Recommendations&   
group.4.fields=background_information,remediation,external_url&  
group.5.title=Compliance&  group.5.fields=compliance,compliance_status&  
group.6.title=Evidences&  group.6.fields=evidence_table,evidences&   
setting.title.html_tag=div&  setting.title.display_severity=true&  
setting.title.show=true&   
setting.layout=table&   
setting.evidences.layout=table&   
setting.evidence_table.title=Evidence Title&    
setting.evidence_table.format=all&   
setting.assets.format=list1&   
setting.assets.display_count=30&  
setting.filter.type=Observation   
}



### File: pentest-reporting-resources/report_templates/pentest_report_template_OWASP_sample1.md

![](https://cyver.io/wp-content/uploads/2022/01/cyver-light-bg.png)

# Findings Report
![](https://cyver.io/wp-content/uploads/2022/01/Rectangle-2.png)

## {Project_Name}
### COMMISSIONED BY {Client_Name}


EXECUTION DATES 	: {Project_TestingStartDate} - {Project_TestingEndDate} 

REPORT STATUS:  Final

VERSION	: {Report_Version}

DATE		: {Report_CreatedOn}

REVISION INFORMATION: 

EXECUTED BY: Mike Terhaar | Senior Ethical Hacker for CYVER BV

**THIS REPORT IS CONFIDENTIAL**

# 1. MANAGEMENT SUMMARY

## 1.1. GENERAL INFORMATION
A penetration test is a controlled attack on a computer or network system with the intent of finding security weaknesses and potentially gaining access to the system and its data. The process involves identifying target systems and setting a goal, then obtaining contextual and technical information, followed by vulnerability identification and validation phases. Potential solutions are then shared to assist in helping the organization mitigate any found vulnerabilities.

Ultimately, the organization conducting a pentest can reduce risk in a focused and cost-effective manner. Penetration tests also help in determining where general weaknesses exist in the digital environment, which leads to a more proactive approach in security management processes. For example, when control mechanisms are built into the policies and procedures driving daily operations. 

The main objective of the penetrating test is to provide input from a technical and real-world perspective. This input is designed to be valuable in helping the organization to determine and reduce business risk. We obtain that information by identifying system and infrastructure vulnerabilities, which could be used by an attacker to gain unauthorized access to systems or information, while providing sufficient information for the organization to understand associated business risks and potential impact of those vulnerabilities - so that the organization can assess actions and prioritize how to mitigate risks. 

This report covers the results of the {Project_Name} security investigation conducted by CYVER at the request of {Client_Name}.

This security investigation was conducted from {Project_TestingStartDate} - {Project_TestingEndDate}.
The research methodology used for a Web Security Assessment is in accordance with the OWASP Testing Guide.


## 1.2. RESULTS
The pentest identified a number of vulnerabilities. Found vulnerabilities are detailed below, organized by risk classification.

{Findings_Chart_Severity}

!!Description general view!!
It was possible to post messages in xxxxx conversations of other users. eConsult conversations were identified in the application by means of an ID. If a user guessed this ID, they could post in these conversations without being authorized to do so. The risk is that an attacker can carry out more targeted attacks against other users within the application.
The application made incomplete use of security features in browsers. The browser contains several security options that an application can invoke to protect the user. Not taking advantage of this increases the risk that a malicious person could perform actions in the context of another user. The risk is also increased that the appearance of the application is displayed in a modified way in the user's browser. This can lead to damage to the image of the organization. For more information,

The research was carried out with such complete coverage that a clear impression could be formed of the investigated systems and/or applications.


## 1.3. RECOMMENDATIONS
Based on the findings, CYVER has the following recommendations:
1. A
2. B
3. C
4. 

## 1.4. CONCLUSION

# 2. Assignment Details

This pentest is based on the agreed-upon proposal with reference ==reference== which includes the following description of the assignment:


## 2.2. Scope
The scope of the investigation is shown in the table below. Systems and applications not listed have not been pentested..

{Scope_Assets_List}

## 2.3. Purpose of this Assignment
Independently determining the security level of {Project_Name}, detecting vulnerabilities, and suggesting possible improvements.

==To determine that {Project_Name} satisfies==

## 2.4. Research Method
This study was conducted according to a ==grey-box application study==.

When investigating according to the ==grey-box-method== ==pre-known credentials== and limited information about the test objects are available.

The OWASP WSTG 4.2 was used for the research.

## 2.5. Reporting
The management summaries and technical summaries respectively serve as an overview of the research results for general and technical management. In subsequent chapters, the detailed results are described and supported by reproducible findings. These chapters are intended to guide technical personnel in reproducing and mitigating vulnerability findings.

## 2.6. Limitations
A Pentest provides valuable insight into the IT security of the target system or application. However, such an investigation is only a snapshot and does not guarantee the security of the IT environment and data. New attack techniques are constantly being developed and discovered. In addition, a small adjustment to the IT environment can easily introduce new vulnerabilities. The role of processes, procedures, and the human factor in information security are at least as important as technology used. This report only provides an overview of vulnerabilities found and is therefore not intended as a guarantee of security.

In addition, it is important to note that a Pentest is performed by people and that during the research period, choices are made in approach and use of tooling. Pentest results also heavily rely on the capabilities of the executive consultant. It is therefore possible that tests with a repetitive character may deviate in results.

# 3. TECHNICAL SUMMARY
      
This chapter provides an overview of key findings included in this report. For a detailed description, see the actual findings later in this report.

## 3.1. Findings Summary

{Findings_Vuln_Table}

{{ReportPdfPageBreak}}
## 3.2. OWASP Reference

{ComplianceNorm_Table}

{{ReportPdfPageBreak}}
## 3.3. Main Findings

{Findings_Vuln_High_SummaryList}

## 3.4. Observations

{Findings_Obs_Table}

# 4. Methodology

{Scope_Methodology}

Control objectives covered:
{ComplianceNorm_Name}

**Network port scanning and protocol identification**: We inventoried all open ports in order to detect every service provided by the servers in order to plan the vulnerability assessment.

**Software fingerprinting and identification**: Once services and applications were identified, we proceeded to identify known software and their versions in order to look for components with known vulnerabilities from public databases.

**Manual reconnaissance**: In order to identify information that could be subject to be used for the testing.

**Manual penetration testing**: Intrusion attempts based on OSSTTM and OWASP methodology.

IP ranges listed below were in scope for this assessment. Ranges were scanned using various automated tools to identify known vulnerabilities and service misconfigurations, such as those tracked by CVE and listed in the CIS Critical Security Controls. Targets were then assessed manually in order to validate scan results, determine their risk, and to improve coverage and quality of the test.

The test was done according to penetration testing best practices. The flow from start to finish is listed below.

Pre Engagement:
* Scoping
* Customer
* Documentation
* Information
* Discovery

Penetration Testing:
* Tool assisted assessment
* Manual assessment
* Exploitation
* Risk analysis
* Reporting

Post Engagement
* Prioritized remediation
* Best practice support
* Re-testing

### Risk Factors

Each finding is assigned two factors to measure its risk. Factors are measured on a scale of 1 (very low) through 5 (very high).

**Impact**

This indicates the finding's effect on technical and business operations. It covers aspects such as the confidentiality, integrity, and availability of data or systems; and financial or reputational loss.

**Likelihood**

This indicates the finding's potential for exploitation. It takes into account aspects such as skill level required of an attacker and relative ease of exploitation.

**Criticality Definitions**

Findings are grouped into three criticality levels based on their risk as calculated by their business impact and likelihood of occurrence, `risk = impact * likelihood`. This follows the [OWASP Risk Rating Methodology](https://www.owasp.org/index.php/OWASP_Risk_Rating_Methodology).

**High**

Vulnerabilities with a high or greater business impact and high or greater likelihood are considered High severity. Risk score minimum 16.

**Medium**

Vulnerabilities with a medium business impact and likelihood are considered Medium severity. This also includes vulnerabilities that have either very high business impact combined with a low likelihood or have a low business impact combined with a very high likelihood. Risk score between 5 and 15.

**Low**

Vulnerabilities that have either a very low business impact, maximum high likelihood, or very low likelihood, maximum high business impact, are considered Low severity. Also, vulnerabilities where both business impact and likelihood are low are considered Low severity. Risk score 1 through 4.

# 5. Findings
## 5.1. Summary

### 5.1.1. Vulnerability Summary

{Findings_Vuln_Table}

### 5.1.2. Observations Summary

{Findings_Obs_Table}

## 5.2. Vulnerability Details

{Findings_Vuln_DetailsList-v2}

## 5.3. Observations Details

{Findings_Obs_DetailsList}

