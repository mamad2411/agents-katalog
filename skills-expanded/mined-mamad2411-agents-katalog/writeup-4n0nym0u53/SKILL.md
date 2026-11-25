<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-4n0nym0u53
description: CTF writeups and security challenges by 4n0nym0u53.
---

# Writeups by 4n0nym0u53

Source repository: `/repos/4n0nym0u53`

## Repository Index

- dir-create-bash/README.md

## Writeup Content


### File: dir-create-bash/README.md

# Directory Generation - Bash

## Dependencies:

> tree

## Summary

Simple bash script to automate directory creation for more structured pentest reports, prompts user for company name and generates nested directories for each stage of the report. Directory structure is based on HackTheBox's Directory list in GettingStarted/StayingOrganized module.

## Example Output:

```
Enter Company Name: JimTech
Generating Directories...
mkdir: created directory 'JimTech/EPT'
mkdir: created directory 'JimTech/EPT/evidence'
mkdir: created directory 'JimTech/EPT/logs'
mkdir: created directory 'JimTech/EPT/scans'
mkdir: created directory 'JimTech/EPT/scope'
mkdir: created directory 'JimTech/EPT/tools'
mkdir: created directory 'JimTech/IPT'
mkdir: created directory 'JimTech/IPT/evidence'
mkdir: created directory 'JimTech/IPT/logs'
mkdir: created directory 'JimTech/IPT/scans'
mkdir: created directory 'JimTech/IPT/scope'
mkdir: created directory 'JimTech/IPT/tools'
mkdir: created directory 'JimTech/EPT/evidence/credentials'
mkdir: created directory 'JimTech/EPT/evidence/data'
mkdir: created directory 'JimTech/EPT/evidence/screenshots'
mkdir: created directory 'JimTech/IPT/evidence/credentials'
mkdir: created directory 'JimTech/IPT/evidence/data'
mkdir: created directory 'JimTech/IPT/evidence/screenshots'
mkdir: created directory 'JimTech/Documents'
mkdir: created directory 'JimTech/Documents/writeUps'
mkdir: created directory 'JimTech/Documents/reports'
mkdir: created directory 'JimTech/Documents/appendicies'
mkdir: created directory 'JimTech/Documents/summary'
Directory created successfully else echo Error
Generating README...
# JimTech - Pentest Report Introduction\n## Author - An0nyM0u53\n
JimTech
├── Documents
│   ├── appendicies
│   ├── README.md
│   ├── reports
│   ├── summary
│   └── writeUps
├── EPT
│   ├── evidence
│   │   ├── credentials
│   │   ├── data
│   │   └── screenshots
│   ├── logs
│   ├── scans
│   ├── scope
│   └── tools
└── IPT
    ├── evidence
    │   ├── credentials
    │   ├── data
    │   └── screenshots
    ├── logs
    ├── scans
    ├── scope
    └── tools

24 directories, 1 file


```

