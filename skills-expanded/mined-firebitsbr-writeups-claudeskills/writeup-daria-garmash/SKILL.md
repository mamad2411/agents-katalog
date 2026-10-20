<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-daria-garmash
description: CTF writeups and security challenges by daria-garmash.
---

# Writeups by daria-garmash

Source repository: `/repos/daria-garmash`

## Repository Index

- pentest-rekall/README.md

## Writeup Content


### File: pentest-rekall/README.md

# pentest-rekall

This pentest report was created as part of Monash Cybersecurity Bootcamp Project 2.

The purpose of the project was participating in the 3-day Capture The Flag challange attacking a fictional organisation called Rekall. The scope of attack was Rekall's website, its Linux and Windows servers. Objectives involved exfiltrating any sensitive information within the domain, compromising several machines and escalating privileges.

After finalising the attacks the report was created. Please read the full report <a href="https://docs.google.com/document/d/1GIGT835JR3B0Do8UZOzbl1CAKGNr1eAjsTX09VM-st4/edit?usp=sharing"> here</a>. It highlights found vulnerabilities, records steps that were taken and suggests mitigation strategies.

# Executive Summary

Secure Bits Company (SBC) started the assessment by examining REKALL’s web application and trying out the most common web attacks. Tested the web pages for various types of XSS and found that Welcome.php and Memory-Planner.php were vulnerable to reflected XSS, i.e. the malicious code could be executed but not stored on a server. At the same time it was possible to execute stored XSS attacks on page comments.php. Besides, Memory-Planner.php was also vulnerable to local file inclusion. Tried searching for publicly available information on the website and found that the file robots.txt exposed web application file structure by listing several files and directories required for the application. While examining the Login.php page administrative username and password were found in HTML. These credentials were used to login and access advanced admin networking tools. It was also possible to execute a directory traversal attack on a disclaimer.php page using an attribute called ‘page’ and access information about users on the server. Tried to access a shadow file which contains password hashes in a similar way but failed.

Next step was attacking Linux servers on the network provided by Rekall. Found 5 hosts in total. Inspected one of the hosts in NESSUS and found one critical vulnerability in Apache Struts. Tried to exploit this vulnerability using a Metasploit module and succeeded in accessing the host. After that SBC exploited another Linux machine on the network through the vulnerability in Apache Tomcat version and obtained a shell to execute remote commands. Another Linux host was exploited through the weakness in the Drupal version. One more Linux host was vulnerable to a remote code execution attack known as Shellshock, which is connected to unpatched Linux Bash. As for the last Linux host, an SSH user ‘alice’ which was found by searching the public information on Rekall, had a weak password that was guessed in several attempts. SBC was able to login to the host as user ‘alice’ and escalate privileges to user ‘root’.

To attack Windows servers on the network provided by Rekall SBC executed the following steps. In Rekall’s GitHub account called ‘totalrekall’ found credentials for user ‘trivera’ and used them to login. Was able to exploit the vulnerability in the SLMail version and open a shell for remote execution of code. Identified valuable information including NTLM hash for one of the users. Moved laterally to another Windows host which was a domain controller, searched for information there and extracted NTLM hash for user ‘Administrator’. 

