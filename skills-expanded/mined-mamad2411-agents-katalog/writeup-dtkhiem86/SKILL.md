<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dtkhiem86
description: CTF writeups and security challenges by dtkhiem86.
---

# Writeups by dtkhiem86

Source repository: `/repos/dtkhiem86`

## Repository Index

- WordPress-Pentesting-Report/README.md

## Writeup Content


### File: WordPress-Pentesting-Report/README.md

# WordPress-Pentesting-Report
Pentesting Report
1. (Required) Vulnerability Name or ID: User Enumeration, WordPress 4.2
  - [X] Summary: 
    - Vulnerability types:  Enumerate a list of valid user names
    - Tested in version: 4.2
    - Fixed in version: 4.10
  - [X] GIF Walkthrough: ![wordpress username enumeration](https://user-images.githubusercontent.com/31055092/38160112-f15e04c6-346c-11e8-8029-a21ca9a37db6.gif)
  - [X] Steps to recreate: 
  This vulnerability that allows anyone the ability to enumerate a list of valid user names on a WordPress. 
  Although more a design flaw than that of a technical flaw in code, this creates an easier brute force attack for any malicious hacker.
  - [ ] Affected source code:
   
2. (Required) Vulnerability Name or ID: XSS, CVE-2018-9061
  - [X] Summary: 
    - Vulnerability types: XSS
    - Tested in version: WordPress 4.7.4
    - Fixed in version: WordPress 4.7.5
  - [X] GIF Walkthrough: ![wordpress xss2](https://user-images.githubusercontent.com/31055092/38160134-2cc4edcc-346d-11e8-96bd-8a17b8cb44e2.gif)
  - [X] Steps to recreate: 
 If a wordpress admin is tricked into attempting to load a bogus media file exceeding maximum allowed file size through upload.php, a carefully crafted file name will allow the execution of cross site scripting. This is due to the lack of file name sanitation.
  - [ ] Affected source code:
    
3. (Required) Vulnerability Name or ID: XSS, CVE-2016-7168
  - [X] Summary: 
    - Vulnerability types: XSS 
    - Tested in version: WordPress 4.5.3
    - Fixed in version: WordPress 4.6.1
  - [X] GIF Walkthrough: ![wordpress xss](https://user-images.githubusercontent.com/31055092/38160131-27313424-346d-11e8-96b8-d4abfff4e839.gif)
  - [X] Steps to recreate: 
  This vulnerability that allows users with editor or author privileges to run XSS on a WordPress site, running versions prior to 4.2.3. All that is required, is any user with the above privileges, who may proceed to embed cross site scripting on their post. This may be used for privilege escalation if users of admin privileges were to view the pages.
  - [ ] Affected source code:


