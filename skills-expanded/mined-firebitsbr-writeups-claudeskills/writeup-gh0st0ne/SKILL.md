<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gh0st0ne
description: CTF writeups and security challenges by Gh0st0ne.
---

# Writeups by Gh0st0ne

Source repository: `/repos/Gh0st0ne`

## Repository Index

- PenTest_Report_Template/README.md
- PenTest_Report_Template/Template.md

## Writeup Content


### File: PenTest_Report_Template/README.md

A PenTest Report template for use with pandoc conversion to PDF with a basis from the official OSCP template for reporting.

-- Download the `awesomebox.sty` file and place within the same direcotry of the md file you're converting. This is part of the header-includes so you don't need to specify it in the command line  
-- `Template.pdf` shows example output



### File: PenTest_Report_Template/Template.md

---
title: "Penetration Test Report | Client Name"
author: [Ghost Exploit | @gh0stxplt]
date: "date"
subject: "Penetration Test Report"
keywords: [Report, Penetration Test, Client Name]
subtitle: "Client Name"
lang: "en"
titlepage: true
titlepage-color: "1E90FF"
titlepage-text-color: "FFFAFA"
titlepage-rule-color: "FFFAFA"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
header-includes:
- |
  ```{=latex}
  \usepackage{awesomebox}
  ```
pandoc-latex-environment:
    noteblock: [note]
    tipblock: [tip]
    warningblock: [warning]
    cautionblock: [caution]
    importantblock: [important]
---
# Executive Summary

## Overview 

Discuss at a high level what, why, how, who, and when. Target audience is Executives who may not care for all the details

## Summary of Results

Give an overview of the most important findings from the penetration test

## Overall Risk Rating

lorem ipsum

::: note
Note Example: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam aliquet libero
quis lectus elementum fermentum.

Fusce aliquet augue sapien, non efficitur mi ornare sed. Morbi at dictum
felis. Pellentesque tortor lacus, semper et neque vitae, egestas commodo nisl.
:::

## Prioritized Remediation Efforts

What findings need to be remediated first and foremost

# Scope of Work

## Overall Scope

Explain the scope of the assessment

## Risk Appetite

Discuss client's risk appetite; how much risk are they willing to accept? [More information](https://en.wikipedia.org/wiki/Risk_appetite)

## Attack Persona

Define how you are attacking the system (e.g. black box, APT, internal) as defined by the client

## Target Assets

Summarize assets in scope; this is expanded upon in the Findings section for each asset  

|Asset     	| Value (1 - 5) 	| IP Address (if known) 	|
|:----: 	  |:-------------:	|:---------------------:	|
| Web Server    	| 2             	| 192.168.x.x           	|
| AD Server     	| 5             	| 192.168.x.x           	|
| Workstation 1 	| 1             	| 192.168.x.x           	|


# Methodologies
Explain your methodology when apporaching the assessment

## Information Gathering & Enumeration
Reiterate what the scope of the test was and provide enumeration steps taken (e.g. automated scan results or manual testing findings)

*Enumeration information*

## Findings

The penetration testing portions of the assessment focus heavily on gaining access to a variety of systems.
During this penetration test, I was able to successfully gain access to **X** out of the **X** systems.

### System IP: 192.168.x.x
Copy this section down to the `\newpage` for each system within the test scope. If multiple vulnerabilities are found, copy the `Vulnerability Findings to Severity` as needed.

#### Service Enumeration

**Nmap Scan Results:**

**Vulnerability Finding 1:**

**Vulnerability Fix:**

**Severity:**

**Vulnerability Finding 2:**

**Vulnerability Fix:**

**Severity:**

#### Privilege Escalation Achieved? (Y/N)
If you achieved privilege escalation on the machine this section can be used. Otherwise the informational sections can be ommited.

*Additional Priv Esc info*

**Vulnerability Exploited:**

**Vulnerability Explanation:**

**Vulnerability Fix:**

**Severity:**

**Exploit Code:**

**Proof Screenshot:**

![Image Placeholder](placeholder-image-300x225.png)

\newpage

## Maintaining Access

Discuss how access can be maintained within the compromised environment and show POC

## House Cleaning

Explain what items were cleaned up after the test and show proof screenshots that the items no longer exist within the client environment

# Additional Items

## Appendix A - Descriptive Title:

Lorem

## Appendix B - Code Used:

```
code here
```

## Appendix C - Tools Utilized:

