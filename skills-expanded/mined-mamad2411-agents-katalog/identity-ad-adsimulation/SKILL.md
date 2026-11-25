---
name: identity-ad-adsimulation
description: "Identity Ad Adsimulation."
domain: cybersecurity
---

|
| **Kerberoasting** | Requesting Kerberos TGS tickets for accounts with Service Principal Names and cracking them offline to recover the service account's plaintext password |
| **AS-REP Roasting** | Requesting Kerberos AS-REP responses for accounts without pre-authentication enabled and cracking the encrypted timestamp offline |
| **DCSync** | Using Directory Replication Service privileges (DS-Replication-Get-Changes-All) to replicate password data from a domain controller, mimicking the behavior of a DC |
| **BloodHound** | Graph-based Active Directory analysis tool that maps privilege relationships and identifies attack paths from any user to high-value targets like Domain Admin |
| **Unconstrained Delegation** | A Kerberos delegation configuration where a service can impersonate any user to any other service, allowing TGT capture from connecting users |
| **Pass-the-Hash** | Authentication technique using an NTLM hash directly instead of the plaintext password, exploiting Windows NTLM authentication |
| **AD CS Abuse** | Exploiting misconfigured Active Directory Certificate Services templates to request certificates that grant elevated privileges or impersonate other users |
| **NTLM Relay** | Forwarding captured NTLM authentication to a different service to authenticate as the victim, effective when SMB signing is not enforced |

## Tools & Systems

- **BloodHound**: Attack path analysis tool that ingests AD data collected by SharpHound to visualize and identify privilege escalation paths through object relationships
- **Impacket**: Python toolkit for network protocol interactions including Kerberos attacks (GetUserSPNs, GetNPUsers), credential dumping (secretsdump), and remote execution (psexec, wmiexec)
- **Mimikatz**: Post-exploitation tool for extracting plaintext credentials, NTLM hashes, and Kerberos tickets from Windows memory (LSASS process)
- **CrackMapExec**: Multi-protocol attack tool for Active Directory environments supporting SMB, LDAP, WinRM, and MSSQL with built-in modules for password spraying and enumeration
- **Certipy**: Python tool for enumerating and exploiting Active Directory Certificate Services (AD CS) misconfigurations

## Common Scenarios

### Scenario: Domain Compromise Assessment for a Healthcare Organization

**Context**: A hospital network with a single Active Directory forest containing 5,000 user accounts, 800 computer objects, and 15 domain controllers across 3 sites. The tester starts with a single low-privilege domain user account. The goal is to determine if an attacker with stolen employee credentials could escalate to Domain Admin.

**Approach**:
1. Run SharpHound to collect AD relationship data and import into BloodHound
2. BloodHound reveals a path: owned user -> member of IT-Support group -> GenericAll on SVC-SQL account -> SVC-SQL has SPN -> Kerberoast -> SVC-SQL is local admin on DB-SERVER-01 -> DB-SERVER-01 has a Domain Admin session
3. Kerberoast SVC-SQL, crack the weak password (Summer2023!) in 12 minutes using hashcat
4. Use SVC-SQL credentials to access DB-SERVER-01 via psexec
5. Extract Domain Admin credentials from LSASS memory on DB-SERVER-01
6. Validate domain compromise by performing DCSync to dump all domain hashes
7. Report the complete attack chain with remediation: set 25+ character passwords on service accounts, enable AES-only Kerberos encryption, remove unnecessary local admin rights, implement tiered administration

**Pitfalls**:
- Running SharpHound with noisy collection methods during peak hours, alerting the SOC via excessive LDAP queries
- Password spraying without checking the domain lockout policy first, locking out hundreds of accounts
- Forgetting to test for AD CS vulnerabilities which often provide the fastest path to Domain Admin
- Not checking for stale computer accounts that may still have cached credentials or active sessions

## Output Format

```
## Finding: Service Account Vulnerable to Kerberoasting with Weak Password

**ID**: AD-002
**Severity**: Critical (CVSS 9.1)
**Affected Object**: SVC-SQL@corp.example.com (Service Account)
**Attack Technique**: MITRE ATT&CK T1558.003 - Kerberoasting

**Description**:
The service account SVC-SQL has a Service Principal Name (MSSQLSvc/db-server-01.corp.example.com:1433)
registered in Active Directory and uses a weak password that was cracked in 12 minutes
using hashcat with the rockyou.txt wordlist. This account has local administrator
privileges on DB-SERVER-01, which had an active Domain Admin session at the time of
testing.

**Attack Chain**:
1. Requested TGS ticket: impacket-GetUserSPNs corp.example.com/testuser:password -request
2. Cracked hash: hashcat -m 13100 hash.txt rockyou.txt (cracked in 12m: Summer2023!)
3. Lateral movement: impacket-psexec corp.example.com/SVC-SQL:Summer2023!@db-server-01
4. Credential extraction: mimikatz sekurlsa::logonpasswords -> Domain Admin NTLM hash

**Impact**:
Complete domain compromise from a single low-privilege domain user account. An attacker
could access all 5,000 user accounts, 800 computer objects, and all data within the domain.

**Remediation**:
1. Set a 25+ character randomly generated password for SVC-SQL and all service accounts
2. Migrate to Group Managed Service Accounts (gMSA) which rotate 120-character passwords automatically
3. Enable AES256 encryption for Kerberos and disable RC4 (DES) encryption
4. Remove SVC-SQL from local administrator groups on DB-SERVER-01
5. Implement Protected Users group for privileged accounts to prevent credential caching
6. Deploy Microsoft Defender for Identity to detect Kerberoasting and DCSync attacks
```
