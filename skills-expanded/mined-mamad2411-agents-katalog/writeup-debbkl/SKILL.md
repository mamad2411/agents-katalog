<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-debbkl
description: CTF writeups and security challenges by DEBBKL.
---

# Writeups by DEBBKL

Source repository: `/repos/DEBBKL`

## Repository Index

- Pentesting/README.md
- Pentesting/report.md

## Writeup Content


### File: Pentesting/README.md

<a name="top"></a>
<h1>PENTESTING - Zico2 Challenge</h1>

<p><a href="https://e.pcloud.link/publink/show?code=XZixOTZB0TRkqylNWHCpGd6m2If3yUSDE4y">### Download the virtual machine</a></p>

<h2>Description</h2>
<p>
This project documents the pentesting process of a vulnerable virtual machine called <b>Zico2</b>. The goal is to practice reconnaissance, scanning, directory enumeration, and exploitation of a web vulnerability (Remote Code Execution). <b>Kali Linux</b> was used as the attack environment along with analysis and exploitation tools such as <b>Nmap</b>, <b>Nikto</b>, <b>Dirb</b>, <b>Searchsploit</b>, and <b>Metasploit</b>.
</p>

<h2>Languages and Tools Used</h2>
<ul>
  <li><b>Kali Linux</b></li>
  <li><b>Nmap</b></li>
  <li><b>Netdiscover</b></li>
  <li><b>Nikto</b></li>
  <li><b>Dirb</b></li>
  <li><b>Searchsploit</b></li>
  <li><b>Metasploit</b></li>
</ul>

<h2>Environment Used</h2>
<ul>
  <li><b>Attacker system:</b> Kali Linux</li>
  <li><b>Target system:</b> Zico2 Virtual Machine (10.0.2.5)</li>
  <li><b>Network mode:</b> NAT + Internal Network (VirtualBox)</li>
</ul>

<h2>Analysis Process</h2>

<h3>1. Detecting the target machine:</h3>
<p>Command used:</p>
<pre><code>netdiscover -r 10.0.2.0/24</code></pre>
<div style="text-align:center; margin-bottom: 1em;">
  <img src="screenshots/1.PNG" alt="Netdiscover - Network discovery" width="40%" />
  <br /><i>Using <b>netdiscover</b> to identify the target machine’s IP.</i>
</div>

<h3>2. Service scanning with Nmap:</h3>
<pre><code>nmap -Pn -A -T4 10.0.2.5</code></pre>
<p>Services detected:</p>
<ul>
  <li>22/tcp - SSH</li>
  <li>80/tcp - HTTP</li>
  <li>111/tcp - RPCBind</li>
</ul>
<div style="text-align:center; margin-bottom: 1em;">
  <img src="screenshots/2.PNG" alt="Nmap - Port scanning" width="40%" />
  <br /><i>Nmap scan revealing open ports (22, 80, 111).</i>
</div>

<h3>3. Web security analysis with Nikto:</h3>
<pre><code>nikto -h http://10.0.2.5</code></pre>
<p>Potentially vulnerable directories and configurations are identified.</p>
<div style="text-align:center; margin-bottom: 1em;">
  <img src="screenshots/3.PNG" alt="Nikto - Web server analysis" width="40%" />
  <br /><i>Analysis with <b>nikto</b> detecting possible vulnerabilities.</i>
</div>

<h3>4. Directory brute forcing with Dirb:</h3>
<pre><code>dirb http://10.0.2.5/ /usr/share/dirb/wordlists/common.txt</code></pre>
<p>Important result: discovery of the <code>/dbadmin</code> directory.</p>
<div style="text-align:center; margin-bottom: 1em;">
  <img src="screenshots/4.PNG" alt="Dirb - Directory brute force" width="40%" />
  <br /><i>Directory enumeration with <b>dirb</b>, discovering <code>/dbadmin</code>.</i>
</div>

<h3>5. Manual inspection of the directory:</h3>
<p>Accessing <code>http://10.0.2.5/dbadmin</code> reveals the <b>phpLiteAdmin</b> application.</p>

<h3>6. Vulnerability search with Searchsploit:</h3>
<pre><code>searchsploit -t phpliteadmin</code></pre>
<p>Match found:</p>
<i>PHPLiteAdmin 1.9.3 – Remote PHP Code Injection</i>
<pre><code>searchsploit -x php/webapps/24044.txt</code></pre>

<h3>7. Exploitation attempt:</h3>
<p>Attempting access to phpLiteAdmin using default passwords documented in the exploit.</p>

<h2>Screenshot of phpLiteAdmin Access</h2>
<div style="text-align:center; margin-bottom: 1em;">
  <img src="screenshots/5.PNG" alt="phpLiteAdmin Accessed" width="40%" />
  <br /><i>Access to <b>phpLiteAdmin</b>, potential exploitation via Remote Code Execution.</i>
</div>

<p style="text-align:right;">
  <a href="#top">🔝 Back to top</a>
</p>

<h2>Lessons Learned</h2>
<ul>
  <li>Improved skills in network scanning and service enumeration.</li>
  <li>Identification and exploitation of known vulnerabilities.</li>
  <li>Manual and automated analysis of web applications.</li>
  <li>Use of dictionaries for directory brute forcing.</li>
  <li>Consulting and practical use of public exploits.</li>
</ul>

<pre>
pentesting-zico2/
├── screenshots/
│   └── 1.png
│   └── 2.png
│   └── 3.png
│   └── 4.png
│   └── 5.png
├── report.md
└── index.html (this file)
</pre>

<h2>Author</h2>

<p>
  <b>Déborah Loisel</b><br />
  Vulnerability Analyst & Blue Team Junior<br />
  <a href="https://www.linkedin.com/in/deborahloisel/">LinkedIn</a> · <a href="https://github.com/tuusuario">GitHub</a>
</p>



### File: Pentesting/report.md

# Pentesting Report - Zico2 Challenge

## 1. Introduction

This document details the pentesting process performed on the vulnerable virtual machine **Zico2**.  
The objective was to practice reconnaissance, service scanning, directory enumeration, and exploitation of a Remote Code Execution (RCE) vulnerability on a web application.  
The attacker environment was **Kali Linux**, using tools like Nmap, Nikto, Dirb, Searchsploit, and Metasploit.

## 2. Tools Used

- Kali Linux  
- Netdiscover  
- Nmap  
- Nikto  
- Dirb  
- Searchsploit  
- Metasploit  

## 3. Environment Setup

- **Attacker Machine:** Kali Linux  
- **Target Machine:** Zico2 virtual machine, IP: 10.0.2.5  
- **Network Mode:** NAT + Internal Network (VirtualBox)  

## 4. Reconnaissance

We started by identifying the victim machine's IP address on the subnet using:

```bash
netdiscover -r 10.0.2.0/24
```

Next, we scanned the victim machine's open ports and services with:

```bash
nmap -Pn -A -T4 10.0.2.5
```
Open ports detected were: 
  22/tcp - SSH
  80/tcp - HTTP
  111/tcp - RPCBind

Using Nikto to analyze the HTTP server for vulnerabilities and directories:
```bash
nikto -h http://10.0.2.5
```
Nikto revealed some directories and potential misconfigurations.

To find interesting directories, we used Dirb with the common wordlist:
```bash
dirb http://10.0.2.5/ /usr/share/dirb/wordlists/common.txt
```
This uncovered the directory /dbadmin.

Manual inspection of http://10.0.2.5/dbadmin revealed the presence of phpLiteAdmin.

We searched for known exploits related to phpLiteAdmin:
```bash
searchsploit -t phpliteadmin
```
A matching vulnerability was found:
**PHPLiteAdmin 1.9.3 – Remote PHP Code Injection**

To review the exploit details:
```bash
searchsploit -x php/webapps/24044.txt
```
We attempted to log into phpLiteAdmin using documented default passwords.
Upon successful access, we could exploit the Remote Code Execution vulnerability.

(Screenshot attached in the screenshots folder)

## 5. Evidence
Screenshot showing successful access to phpLiteAdmin interface.

## 6. Lessons Learned
- Improved network scanning and service enumeration skills.
- Identification and exploitation of known vulnerabilities.
- Combined manual and automated web application analysis.
- Use of directory brute forcing to find hidden paths.
- Practical use of public exploit databases and tools.

## 7. Recommendations
- Update phpLiteAdmin to the latest secure version or remove if unnecessary.
- Harden web server configurations to prevent directory enumeration.
- Use strong, non-default credentials for web applications.
- Monitor logs for unusual access patterns.
- Implement web application firewalls to block exploitation attempts.

Report generated by
Déborah Loisel
Vulnerability Analyst & Blue Team Junior
LinkedIn · GitHub

