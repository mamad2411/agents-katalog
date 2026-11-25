<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aaroong
description: CTF writeups and security challenges by aaroong.
---

# Writeups by aaroong

Source repository: `/repos/aaroong`

## Repository Index

- metasploitable2-writeup-aaroong/README.md

## Writeup Content


### File: metasploitable2-writeup-aaroong/README.md

# 
# aaroong (Aarón Garrido Silvera)
# 

- Target Machine: Metasploitable 2  
- OS: Linux Ubuntu Server  
- Objective: Fully compromise the target machine through multiple attack vectors   
- Tools used:  
        - Nmap (port scanning and service detection)  
        - Searchsploit (finding exploits)  
        - Telnet (default credential login)  
        - Metasploit (automated exploitation)  

# 
# Scanning
# 

- Full port scan using Nmap  
- Open ports discovered: (view /screenshots/nmapscan for more information)  
        - 21/tcp (FTP - vsFTPd 2.3.4)  
        - 22/tcp (SSH - OpenSSH 4.7p1)  
        - 23/tcp (Telnet)  
        - 25/tcp (SMTP)  
        - 80/tcp (HTTP - Apache 2.2.8)  
        - 445/tcp (SMB - Samba 3.0.20)  
        - Others...  

- Service & version enumeration revealed:  
        - Outdated and vulnerable software  
        - Potential attack surface on FTP, SMB, and Web services  
        
# 
# Exploitation
# 

# FTP – vsFTPd 2.3.4

- Exploited with a backdoor using `exploit/unix/ftp/vsftpd_234_backdoor`  
- Backdoor opened on port 6200  
- Root shell obtained (view /screenshots/ftp for more information) 

(Now I can search for users, hashes and passwords, this will help with the next attack vector, Telnet)

# Telnet

- From the previous exploitation, I discovered that the users and passwords were set to default values
- I accessed with `telnet` and tried with the default user and password
- Valid login and basic shell access (view /screenshots/telnet for more information)

# SMB – Samba 3.0.20 (CVE-2007-2447)

- I used `--script smb-os-discovery` to search more information about the service version
- I found a exploit available for the service version (Samba 3.0.20-Debian) using the `search` command in Metasploit
- Exploited it using Metasploit (the exploit: `exploit/multi/samba/usermap_script`)
- No meterpreter available, so I used: `cmd/unix/reverse_netcat`
- Root shell obtained (view /screenshots/smb for more information)

# 
# Post-Exploitation
# 

- /etc/passwd and /etc/shadow retrieved  
- Valid users and password hashes identified  
- Sensitive files found:  
        - `/var/www/mutillidae/passwords/accounts.txt`:  
            - Plain-text credentials:  
               - `admin:adminpass`  
               - `ed:pentest`  
               - `john:monkey`  

- System information, users, and configuration files enumerated

# 
# Conclusion
# 

- I compromised the machine through 3 attack vectors  
- Sensitive credentials and configuration files exposed  
- Root access achieved on multiple services  

# 
# Recommendations:
# 

- Remove default users or change passwords  
- Patch and upgrade vulnerable services (vsFTPd, Samba, Apache)  
- Secure web directories and remove sensitive files from production

# 
# 🧠 What I learned
# 

- How to enumerate services and ports efficiently
- How to identify and exploit real vulnerabilities
- How to perform post-exploitation and extract useful data
- How to write and present a professional pentest report  

# 
# Notes
# 

- This exercise was done as part of my cybersecurity learning path. This is my first machine that I try to exploit, I am very happy with the result that I have achieved and I hope that over time I will improve my pentesting skills to be able to expose more advanced machines and to improve my writeups as well.

