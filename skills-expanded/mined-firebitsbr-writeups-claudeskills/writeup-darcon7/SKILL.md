<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-darcon7
description: CTF writeups and security challenges by Darcon7.
---

# Writeups by Darcon7

Source repository: `/repos/Darcon7`

## Repository Index

- bug_bounty_nmap_automation/README.md

## Writeup Content


### File: bug_bounty_nmap_automation/README.md

# bug_bounty_nmap_automation
Automates Nmap scans for bug bounty hunting. Reads targets from a CSV, runs tailored scans for web vulnerabilities (SQLi, XSS, misconfigurations), and generates reports (TXT, XML, HTML). Creates a final summary report of findings for all scanned targets. Ideal for recon and pentesting.
Bug Bounty Nmap Automation Script
Hi and welcome to my first saved automation!
As I dive deeper into the world of bug bounty hunting and penetration testing, I'll be saving my tools and scripts here as I continue to practice and hone my skillset. Not all the tools I create will be perfect, and that’s part of the journey. Feedback is always welcome—whether to improve, refine, or rethink my approach.

The goal of my scripts is to be useful to others or at least spark new ideas on how to write your own tools. I’m excited to contribute to the security community as I grow into a confident hacker. Stay tuned for more as I master new techniques and tools!

Bug Bounty Nmap Automation Script
This Python script automates Nmap scans for bug bounty hunting and penetration testing. It reads a list of targets from a CSV file (such as scope files from platforms like HackerOne or Bugcrowd), runs tailored Nmap scans, and generates detailed reports for each target.

What the Script Does:
Automates Nmap Scanning: Reads a list of domains or IPs from a CSV and runs Nmap scans on each target.
In-Scope Web Vulnerability Detection: Focuses on real-world vulnerabilities like:
SQL Injection (SQLi)
Cross-Site Scripting (XSS)
Sensitive file exposure (backup files, directory listings)
Report Generation: Saves Nmap scan results in multiple formats (TXT, XML, HTML) for every target.
Unique Reports for Each Target: Ensures no overwriting by saving reports with target-specific filenames.
Final Summary Report: Compiles a report summarizing key findings such as open ports and vulnerabilities across all targets.
Outputs for Further Enumeration and Vulnerability Testing:
The script generates detailed reports that can be used for further analysis and vulnerability testing. These reports can serve as a solid foundation for:

Manual Testing: Use the identified open ports and services for deeper manual enumeration and testing.
Further Automation: These outputs can be integrated into other scripts or tools for advanced testing (e.g., using Burp Suite or other vulnerability scanning tools).
More scripts and updates will follow as I continue mastering new tools and techniques. Stay tuned for future additions!

Requirements:
Python 3.x
Nmap (with sudo/root access)
xsltproc (for converting XML to HTML)
Nmap scripts used:
http-sql-injection
http-xssed
http-enum
vulners


Planned Features:
Add more Nmap scripts to cover a broader range of services and vulnerabilities.
Integrate with other tools for post-Nmap enumeration and testing.
Continue refining the automation as I develop more skills and explore new techniques.
Thanks for checking out my work! Feel free to fork the repo, send in feedback, or just keep an eye out for future scripts and improvements.

