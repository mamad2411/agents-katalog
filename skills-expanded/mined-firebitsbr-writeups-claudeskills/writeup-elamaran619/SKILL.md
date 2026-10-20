<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-elamaran619
description: CTF writeups and security challenges by elamaran619.
---

# Writeups by elamaran619

Source repository: `/repos/elamaran619`

## Repository Index

- hackerone_wordlist/ANALYTICS.md
- hackerone_wordlist/README.md
- hackerone_wordlist/sourcecode/README.md
- hackerone_wordlist/.github/ISSUE_TEMPLATE/bug_report.md

## Writeup Content


### File: hackerone_wordlist/README.md


<h1 align="center">
  <br>
  <a href="https://www.hackerone.com/"><img src="https://github.com/xyele/hackerone_wordlist/blob/master/images/hackeronelogo.png?raw=true" alt="hackerone_logo"></a>
  <br>
  HackerOne Wordlist
  <br>
</h1>
<h4 align="center">The wordlists that have been compiled using disclosed reports at the HackerOne bug bounty platform.</h4>
<p align="center">
  <a href="https://github.com/xyele/hackerone_wordlist/stargazers">
    <img src="https://img.shields.io/github/stars/xyele/hackerone_wordlist">
  </a>
  <a href="https://github.com/xyele/hackerone_wordlist/releases">
      <img src="https://img.shields.io/github/release/xyele/hackerone_wordlist">
  </a>
</p>

## Match Cases
Here is the match cases how it extracts all these data.
#### URLs
I've used [urlextract](https://github.com/lipoja/URLExtract) library for extracting URLs based on TLDs. Eventhough it works awesome, there might be false matches rarely. 
#### Raw HTTP Requests
It extracts the raw http requests which is in three backticks (\`\`\`). Her are the example:
````
Hey team! I've found an SQL Injection issue with your website.

## Request
```
POST /xyele/hackerone_wordlist HTTP/1.1
Host: github.com

star_repo=true'
```
````
So it extracts the request and parsing it.
```
POST /xyele/hackerone_wordlist HTTP/1.1
Host: github.com

star_repo=true'
```

#### Parameter names
Besides the getting parameters from requests and URLs, it gets parameter names with regex again. Here are the examples:
```
LFI throught the filename parameter                 --> filename
SQL Injection on blabla domain via userid parameter --> userid
<?php echo $_GET['makesense']; ?>                   --> makesense
```

## To Do
- Develop own URL extracting library
- Extract json and parse parameters from markdown code block.
- Extract json and parse parameters from raw http response.

## Known Issues
- It downloads reports each by each but nothing to do for getting it faster because HackerOne has rate-limit.

## Support Me
Reach out to me at one of the following places!
- https://github.com/xyele
- https://hackerone.com/zeroxyele
- https://twitter.com/zeroxyele



### File: hackerone_wordlist/sourcecode/README.md

## Installation
```
python3 -m pip install -r requirements.txt
```

## Usage
#### Download Reports (download_reports.py)
Arguments:
```
--idrange - ID Range
--output - Output Directory (the reports will be saved there)
```
Example usage:
```
mkdir reports
python3 download_reports.py --idrange 25,10000 --output reports/
```

#### Process Reports (process_reports.py)
Arguments:
```
--reports - Reports Directory
--output - Output Filename (csv)
```
Example usage:
```
python3 process_reports.py --reports reports/ --output dataset.csv
```
#### Create Wordlist (create_wordlist.py)
Arguments:
```
--reports - Reports Directory
--output - Output Filename (csv)
--entropy - Maximum Entropy (Default: 4.2)
```
Example usage:
```
python3 create_wordlist.py --dataset dataset.csv --output wordlists/ --entropy 4
```

## Tested With
- Ubuntu 20.04 & Python 3.8.2



### File: hackerone_wordlist/.github/ISSUE_TEMPLATE/bug_report.md

---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**Your Enviroement**
 - OS [e.g. Ubuntu 20.04]
 - Version [e.g. 1.0]
 - Python Version [e.g. 3.8]



### File: hackerone_wordlist/ANALYTICS.md



