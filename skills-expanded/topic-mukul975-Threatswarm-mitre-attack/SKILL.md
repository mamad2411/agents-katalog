---
name: mitre-attack
description: MITRE ATT&CK framework reference — tactics, techniques, and tool-to-TTP mappings for pentest documentation and detection rule writing
allowed-tools: Read
---

## MITRE ATT&CK Enterprise Tactics (TA)

| Tactic ID | Tactic Name | Description |
|-----------|-------------|-------------|
| TA0001 | Initial Access | Entry point into target environment |
| TA0002 | Execution | Running malicious code |
| TA0003 | Persistence | Maintaining foothold across reboots |
| TA0004 | Privilege Escalation | Gaining higher-level permissions |
| TA0005 | Defense Evasion | Avoiding detection |
| TA0006 | Credential Access | Stealing credentials |
| TA0007 | Discovery | Learning about the environment |
| TA0008 | Lateral Movement | Moving through the network |
| TA0009 | Collection | Gathering data of interest |
| TA0010 | Exfiltration | Stealing data |
| TA0011 | Command and Control | Communicating with compromised systems |
| TA0040 | Impact | Disrupting availability or integrity |

## Top 50 ATT&CK Techniques

| TTP ID | Name | Tactic |
|--------|------|--------|
| T1595 | Active Scanning | Reconnaissance |
| T1592 | Gather Victim Host Information | Reconnaissance |
| T1593 | Search Open Websites/Domains | Reconnaissance |
| T1566 | Phishing | Initial Access |
| T1190 | Exploit Public-Facing Application | Initial Access |
| T1133 | External Remote Services | Initial Access |
| T1078 | Valid Accounts | Initial Access/Persistence/Defense Evasion |
| T1059.001 | PowerShell | Execution |
| T1059.003 | Windows Command Shell | Execution |
| T1059.004 | Unix Shell | Execution |
| T1053.005 | Scheduled Task | Execution/Persistence |
| T1204 | User Execution | Execution |
| T1547.001 | Registry Run Keys | Persistence |
| T1547.006 | Kernel Modules and Extensions | Persistence |
| T1543.003 | Windows Service | Persistence |
| T1548.002 | Bypass UAC | Privilege Escalation/Defense Evasion |
| T1068 | Exploitation for Privilege Escalation | Privilege Escalation |
| T1055 | Process Injection | Defense Evasion/Privilege Escalation |
| T1027 | Obfuscated Files or Information | Defense Evasion |
| T1562.001 | Disable or Modify Tools | Defense Evasion |
| T1070.001 | Clear Windows Event Logs | Defense Evasion |
| T1003.001 | LSASS Memory | Credential Access |
| T1003.003 | NTDS | Credential Access |
| T1110.001 | Password Guessing | Credential Access |
| T1110.003 | Password Spraying | Credential Access |
| T1558.003 | Kerberoasting | Credential Access |
| T1558.004 | AS-REP Roasting | Credential Access |
| T1040 | Network Sniffing | Credential Access/Discovery |
| T1087 | Account Discovery | Discovery |
| T1082 | System Information Discovery | Discovery |
| T1018 | Remote System Discovery | Discovery |
| T1046 | Network Service Discovery | Discovery |
| T1069 | Permission Groups Discovery | Discovery |
| T1021.001 | Remote Desktop Protocol | Lateral Movement |
| T1021.002 | SMB/Windows Admin Shares | Lateral Movement |
| T1021.006 | Windows Remote Management | Lateral Movement |
| T1550.002 | Pass the Hash | Lateral Movement |
| T1550.003 | Pass the Ticket | Lateral Movement |
| T1074 | Data Staged | Collection |
| T1056 | Input Capture | Collection/Credential Access |
| T1071.001 | Web Protocols (HTTP/S) | C2 |
| T1071.004 | DNS | C2 |
| T1095 | Non-Application Layer Protocol | C2 |
| T1572 | Protocol Tunneling | C2 |
| T1041 | Exfiltration Over C2 Channel | Exfiltration |
| T1048 | Exfiltration Over Alternative Protocol | Exfiltration |
| T1486 | Data Encrypted for Impact | Impact |
| T1490 | Inhibit System Recovery | Impact |
| T1489 | Service Stop | Impact |
| T1562 | Impair Defenses | Defense Evasion |

## Tool → ATT&CK Mapping

| Tool | ATT&CK TTP | Description |
|------|------------|-------------|
| nmap | T1046, T1595.001 | Network Service Discovery / Active Scanning |
| nuclei | T1595.002 | Vulnerability Scanning |
| subfinder/amass | T1596 | Search Open Technical Databases |
| theHarvester | T1593.001 | Social Media Search |
| mimikatz (sekurlsa) | T1003.001 | LSASS Memory Dump |
| mimikatz (dcsync) | T1003.006 | DCSync |
| bloodhound | T1069, T1482 | Permission Group Discovery, Domain Trust Discovery |
| impacket-GetUserSPNs | T1558.003 | Kerberoasting |
| impacket-GetNPUsers | T1558.004 | AS-REP Roasting |
| hashcat | T1110 | Brute Force / Password Cracking |
| crackmapexec | T1021.002, T1110 | SMB Lateral Movement, Password Spraying |
| impacket-psexec | T1021.002, T1569 | SMB Execution |
| impacket-wmiexec | T1047 | Windows Management Instrumentation |
| evil-winrm | T1021.006 | Windows Remote Management |
| sqlmap | T1190, T1059 | SQL Injection Exploitation |
| Metasploit | T1190, T1068 | Exploitation Framework |
| Sliver/Havoc/Cobalt Strike | T1071, T1573 | C2 Communication |
| msfvenom | T1587.001 | Develop Capabilities: Malware |
| responder | T1557.001 | LLMNR/NBT-NS Poisoning |
| ntlmrelayx | T1557.001 | NTLM Relay |
| certipy | T1649 | Steal or Forge Authentication Certificates |
| bloodhound-python | T1069.002 | Domain Group Discovery |
| feroxbuster/gobuster | T1595.003 | Wordlist Scanning |
| hydra | T1110.001 | Password Guessing |
| burpsuite | T1190 | Web Vulnerability Discovery |
| sqlmap | T1190 | SQL Injection |
| binwalk | T1592.002 | Firmware Analysis |
| frida | T1629, T1633 | Mobile Instrumentation |
| aircrack-ng | T1040 | Network Sniffing |
| john/hashcat | T1110.002 | Password Cracking |
| searchsploit | T1588.005 | Exploit Research |
