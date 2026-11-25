---
name: hashcat
description: >
  Operate hashcat — the world's fastest CPU/GPU-based password recovery tool. Use when
  cracking password hashes obtained during a pentest, CTF, or red team engagement, when the
  user asks about offline password cracking, hash identification, rule-based attacks, mask
  attacks, combinator attacks, or integrating hashcat with secretsdump/mimikatz output.
  Covers installation with GPU drivers, all attack modes (-a 0/1/3/6/7), hash types (-m),
  rule engines, mask charsets, potfile management, session control, brain server, distributed
  cracking, and end-to-end AD credential cracking workflows.
license: MIT
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/hashcat/hashcat
---

# hashcat Agent Skill

## When to Use This Skill

Use this skill when:
- Cracking hashes captured from an AD environment (NTLM, NetNTLMv2, Kerberoast, AS-REP)
- The user asks about offline password recovery or wordlist/rule/mask attacks
- Integrating hashcat with impacket secretsdump, Responder, or mimikatz lsadump output
- Benchmarking GPU hash speeds or optimizing cracking performance
- Building custom rule sets or mask policies for targeted campaigns

## What hashcat Does

hashcat is an advanced CPU and GPU accelerated password recovery utility supporting over 300
hash types. It is the de-facto standard offline cracker used in penetration testing to
recover plaintext credentials from captured hashes, enabling pass-the-hash, lateral movement,
and further AD compromise. It supports six attack modes ranging from pure dictionary to
hybrid mask attacks and includes a powerful rule engine for wordlist mutation.

## Installation

### Pre-built binary (recommended)

```bash
# Download latest release
wget https://hashcat.net/files/hashcat-6.2.6.tar.gz
tar xf hashcat-6.2.6.tar.gz
cd hashcat-6.2.6/
./hashcat --version

# Or install via package manager (Kali/Parrot)
sudo apt install hashcat
```

### GPU drivers (critical for performance)

```bash
# NVIDIA — install CUDA toolkit
sudo apt install nvidia-driver nvidia-cuda-toolkit
# Verify GPU is detected
./hashcat -I

# AMD — install ROCm or AMDGPU-PRO with OpenCL
sudo apt install rocm-opencl-runtime
# Or use the AMDGPU-PRO driver with opencl component

# CPU-only fallback (10-100x slower, no driver required)
./hashcat --force   # suppress GPU errors, runs on CPU
```

### Docker (CPU-only)

```bash
docker run --rm -it dizcza/docker-hashcat hashcat --version
# GPU passthrough (NVIDIA)
docker run --rm --gpus all -v $(pwd):/data dizcza/docker-hashcat hashcat \
  -m 1000 /data/hashes.txt /data/rockyou.txt
```

## Core Concepts

### Attack Modes (-a)

| Mode | Name | Description |
|------|------|-------------|
| `-a 0` | Dictionary | Wordlist ± rules |
| `-a 1` | Combinator | Concat two wordlists |
| `-a 3` | Brute-force/Mask | Positional charsets |
| `-a 6` | Hybrid wordlist+mask | Word then mask suffix |
| `-a 7` | Hybrid mask+wordlist | Mask prefix then word |

### Hash Types (-m) — Common Pentest Values

| `-m` | Hash Type | Example context |
|------|-----------|-----------------|
| `0` | MD5 | Web app databases |
| `100` | SHA-1 | Legacy apps |
| `1000` | NTLM | Windows SAM / NTDS |
| `1400` | SHA-256 | Linux shadow ($5$) |
| `1800` | sha512crypt | Linux shadow ($6$) |
| `3200` | bcrypt | Modern web apps |
| `5500` | NetNTLMv1 | Responder capture |
| `5600` | NetNTLMv2 | Responder capture |
| `13100` | Kerberoast (TGS-REP) | SPN ticket cracking |
| `18200` | AS-REP Roasting | No-preauth accounts |
| `19600` | Kerberos 5 TGT (etype 17) | AES-128 TGT |
| `19700` | Kerberos 5 TGT (etype 18) | AES-256 TGT |
| `22000` | WPA-PBKDF2-PMKID | Wi-Fi |
| `2500` | WPA/WPA2 (old format) | .hccapx |

### Mask Charsets

| Token | Charset |
|-------|---------|
| `?l` | abcdefghijklmnopqrstuvwxyz |
| `?u` | ABCDEFGHIJKLMNOPQRSTUVWXYZ |
| `?d` | 0123456789 |
| `?s` | Special characters (32 symbols) |
| `?a` | `?l` + `?u` + `?d` + `?s` (all printable) |
| `?h` | 0-9a-f (hex lowercase) |
| `?H` | 0-9A-F (hex uppercase) |

## CLI Reference

### Dictionary Attack (-a 0)

```bash
# Basic dictionary attack
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# With rule file
hashcat -m 1000 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Multiple rule files (stacked)
hashcat -m 1000 hashes.txt rockyou.txt \
  -r rules/best64.rule -r rules/toggles1.rule

# With OneRuleToRuleThemAll
hashcat -m 1000 hashes.txt rockyou.txt \
  -r /opt/OneRuleToRuleThemAll/OneRuleToRuleThemAll.rule

# dive.rule (2.3M rules — slow, thorough)
hashcat -m 1000 hashes.txt rockyou.txt -r rules/dive.rule
```

### Mask Attack (-a 3)

```bash
# 8-char all lowercase
hashcat -m 1000 hashes.txt -a 3 ?l?l?l?l?l?l?l?l

# 8-char mixed: upper, lower, digit, special
hashcat -m 1000 hashes.txt -a 3 ?u?l?l?l?l?d?d?s

# Variable length with --increment
hashcat -m 1000 hashes.txt -a 3 --increment --increment-min 6 \
  --increment-max 10 ?a?a?a?a?a?a?a?a?a?a

# Corporate password pattern: Word + 4 digits
hashcat -m 1000 hashes.txt -a 3 -1 ?u?l ?1?l?l?l?l?l?d?d?d?d

# Custom charset with -1 through -4
hashcat -m 1000 hashes.txt -a 3 -1 "?u?l" -2 "?d!" ?1?1?1?1?2?2
```

### Combinator Attack (-a 1)

```bash
# Combine two wordlists: word1 + word2 concatenated
hashcat -m 1000 hashes.txt -a 1 words1.txt words2.txt

# With rules on left/right wordlist
hashcat -m 1000 hashes.txt -a 1 words1.txt words2.txt \
  -j 'c' -k '$1'   # capitalize left, append '1' to right
```

### Hybrid Attacks (-a 6 / -a 7)

```bash
# Wordlist + mask suffix (Password123!)
hashcat -m 1000 hashes.txt -a 6 rockyou.txt ?d?d?d?s

# Mask prefix + wordlist (123!Password)
hashcat -m 1000 hashes.txt -a 7 ?d?d?d?s rockyou.txt
```

### Performance Flags

```bash
# Optimized kernels (limits password length to 31 chars)
hashcat -m 1000 hashes.txt rockyou.txt -O

# Workload profile (1=minimal, 2=default, 3=high, 4=nightmare)
hashcat -m 1000 hashes.txt rockyou.txt -w 3

# Specify device (GPU 1 only)
hashcat -m 1000 hashes.txt rockyou.txt -d 1

# Limit GPU utilization
hashcat -m 1000 hashes.txt rockyou.txt --gpu-temp-abort 90

# Status update interval
hashcat -m 1000 hashes.txt rockyou.txt --status --status-timer 10
```

### Session Management

```bash
# Named session
hashcat -m 1000 hashes.txt rockyou.txt --session mysession

# Restore interrupted session
hashcat --session mysession --restore

# List restore files
ls ~/.local/share/hashcat/sessions/
# or on Windows: %AppData%\hashcat\sessions\
```

### Potfile Management

```bash
# Default potfile location: ~/.local/share/hashcat/hashcat.potfile
# Show cracked hashes from potfile
hashcat -m 1000 hashes.txt --show

# Output cracked results to file
hashcat -m 1000 hashes.txt rockyou.txt -o cracked.txt

# Output format: hash:plain (default 3), or just plain (2)
hashcat -m 1000 hashes.txt rockyou.txt -o cracked.txt --outfile-format 2

# Disable potfile (re-crack everything)
hashcat -m 1000 hashes.txt rockyou.txt --potfile-disable

# Use custom potfile
hashcat -m 1000 hashes.txt rockyou.txt --potfile-path ./engagement.potfile
```

### Benchmark Mode

```bash
# Benchmark all hash types
hashcat -b

# Benchmark specific hash type
hashcat -b -m 1000
hashcat -b -m 3200   # bcrypt is always slow (~100 H/s even on GPU)
```

## Rule-Based Attacks

Hashcat rules are single-character transformations applied to each word in a wordlist.

### Built-in Rule Files (Kali: /usr/share/hashcat/rules/)

| File | Rules | Use Case |
|------|-------|----------|
| `best64.rule` | 64 | Fast, high-value mutations |
| `rockyou-30000.rule` | 30k | Broad coverage |
| `dive.rule` | 99k+ | Exhaustive, slow |
| `toggles1-5.rule` | varies | Case toggling |
| `leetspeak.rule` | ~20 | e→3, a→@, etc. |
| `unix-ninja-leetspeak.rule` | ~60 | Extended leet |

### OneRuleToRuleThemAll

```bash
git clone https://github.com/NotSoSecure/password_cracking_rules /opt/OneRuleToRuleThemAll
hashcat -m 1000 hashes.txt rockyou.txt \
  -r /opt/OneRuleToRuleThemAll/OneRuleToRuleThemAll.rule
```

### Custom Rule Syntax

```
:       No-op (identity)
l       Lowercase all
u       Uppercase all
c       Capitalize first
C       Lowercase first, uppercase rest
t       Toggle all
T N     Toggle char at position N
r       Reverse
d       Duplicate
p N     Append word N times
$X      Append character X
^X      Prepend character X
[ ]     Delete first / last char
{ }     Rotate left / right
D N     Delete char at position N
i N X   Insert char X at position N
o N X   Overwrite char at position N with X
```

### Generate rules with hashcat --generate-rules

```bash
hashcat --generate-rules 1000 --generate-rules-seed 12345 > custom.rule
hashcat -m 1000 hashes.txt rockyou.txt -r custom.rule
```

## Common Workflows

### AD Credential Cracking Pipeline (secretsdump → hashcat)

```bash
# 1. Dump NTDS with secretsdump
impacket-secretsdump -just-dc-ntlm DOMAIN/admin@dc01.corp.local \
  -outputfile ntds_dump

# 2. Extract NTLM hashes (user:rid:lmhash:nthash format)
cut -d: -f4 ntds_dump.ntds > ntlm_hashes.txt

# 3. Phase 1 — fast dictionary
hashcat -m 1000 ntlm_hashes.txt rockyou.txt -O -w 3

# 4. Phase 2 — dictionary + best rules
hashcat -m 1000 ntlm_hashes.txt rockyou.txt \
  -r rules/best64.rule -r rules/d3ad0ne.rule -O -w 3

# 5. Phase 3 — targeted corporate mask (Word + year + !)
hashcat -m 1000 ntlm_hashes.txt -a 6 \
  /usr/share/wordlists/rockyou.txt ?d?d?d?d?s -O

# 6. Show results
hashcat -m 1000 ntlm_hashes.txt --show | tee cracked_ntlm.txt
```

### Kerberoasting Crack

```bash
# Hashes from GetUserSPNs.py (Impacket) or Rubeus
impacket-GetUserSPNs -request DOMAIN/user:pass@dc01 \
  -outputfile kerberoast_hashes.txt

# Crack TGS-REP (etype 23 = RC4-HMAC)
hashcat -m 13100 kerberoast_hashes.txt rockyou.txt \
  -r rules/best64.rule -O -w 3

# AES-256 TGS (etype 18) — much slower
hashcat -m 19700 kerberoast_hashes.txt rockyou.txt -O
```

### AS-REP Roasting Crack

```bash
# Hashes from GetNPUsers.py
hashcat -m 18200 asrep_hashes.txt rockyou.txt \
  -r rules/best64.rule -O -w 3
```

### NetNTLMv2 (Responder Capture)

```bash
# Responder captures: /usr/share/responder/logs/*.txt
hashcat -m 5600 responder_hashes.txt rockyou.txt \
  -r rules/best64.rule -O -w 3
```

### bcrypt Cracking (slow but necessary)

```bash
# bcrypt is rate-limited — use targeted wordlists
hashcat -m 3200 bcrypt_hashes.txt targeted_wordlist.txt \
  -r rules/best64.rule -w 3
# ~100-500 H/s even on high-end GPU
```

## Advanced Techniques

### Brain Server (deduplication across distributed clients)

```bash
# Start brain server
hashcat --brain-server --brain-password secret123

# Client connects to brain (avoids re-cracking same candidates)
hashcat -m 1000 hashes.txt rockyou.txt \
  --brain-client --brain-server 192.168.1.10 \
  --brain-client-features 3 --brain-password secret123
```

### Distributed Cracking (keyspace splitting)

```bash
# Split mask keyspace across 4 nodes using --keyspace
hashcat -m 1000 hashes.txt -a 3 ?a?a?a?a?a?a?a?a \
  --keyspace    # prints total keyspace (e.g., 96^8 = 7.2T)

# Node 1: first quarter
hashcat -m 1000 hashes.txt -a 3 ?a?a?a?a?a?a?a?a \
  --skip 0 --limit 1800000000000

# Node 2: second quarter
hashcat -m 1000 hashes.txt -a 3 ?a?a?a?a?a?a?a?a \
  --skip 1800000000000 --limit 1800000000000
```

### Prince Attack (with princeprocessor)

```bash
# princeprocessor generates PRINCE algorithm candidates
git clone https://github.com/hashcat/princeprocessor
cd princeprocessor/src && make
./pp64.bin --pw-min 6 --pw-max 10 < wordlist.txt | \
  hashcat -m 1000 hashes.txt --stdin
```

### Loopback Attack (crack → feed cracked back as wordlist)

```bash
# hashcat 6.x supports loopback natively
hashcat -m 1000 hashes.txt rockyou.txt \
  -r rules/best64.rule --loopback
# Cracked plaintexts fed back through rules until exhausted
```

### Create Targeted Wordlist from OSINT

```bash
# CeWL — crawl target website for wordlist
cewl https://target.corp.com -d 2 -m 6 -w target_words.txt

# Combine with rules
hashcat -m 1000 hashes.txt target_words.txt \
  -r rules/best64.rule -r rules/leetspeak.rule
```

## Integration with Other Tools

### secretsdump (Impacket)

```bash
# Remote NTDS dump (DCSync equivalent)
impacket-secretsdump DOMAIN/admin@dc01.corp.local -just-dc-ntlm \
  -outputfile dump
# Output: dump.ntds — format user:rid:lmhash:nthash

# Local SYSTEM+NTDS extraction
impacket-secretsdump -system SYSTEM -ntds ntds.dit LOCAL
```

### mimikatz NTLM output

```bash
# mimikatz sekurlsa::logonpasswords outputs:
#   NTLM : aad3b435b51404eeaad3b435b51404ee  (LM blank)
# Extract NTLM values to file, then:
hashcat -m 1000 ntlm_from_mimi.txt rockyou.txt -O
```

### Responder integration

```bash
# Responder logs: /usr/share/responder/logs/
cat /usr/share/responder/logs/*NTLMv2*.txt > all_netntlmv2.txt
hashcat -m 5600 all_netntlmv2.txt rockyou.txt \
  -r rules/best64.rule -O -w 3
```

### Identify hash type with hashid / haiti

```bash
pip install hashid
hashid '$6$rounds=656000$Gu6bJBZMKOwf1T8c$...'  # SHA-512 crypt
hashid 'aad3b435b51404eeaad3b435b51404ee'          # LM Hash

# haiti (more accurate)
gem install haiti-hash
haiti '5f4dcc3b5aa765d61d8327deb882cf99'  # → MD5
```

## Troubleshooting

**No OpenCL devices found / clGetPlatformIDs() failed**
```bash
# Install OpenCL runtime
sudo apt install ocl-icd-opencl-dev opencl-headers
# For NVIDIA, ensure nvidia-opencl-dev is installed
hashcat -I   # list devices; add --force only as last resort
```

**Token length exception**
```bash
# Hash format wrong — check delimiter and format
# NetNTLMv2 must have full challenge field:
# user::domain:challenge:HMAC:blob
hashcat -m 5600 hash.txt wordlist.txt --hex-salt
```

**Cracked but --show shows nothing**
```bash
# Potfile may be disabled or wrong path
hashcat -m 1000 hashes.txt --show --potfile-path ./engagement.potfile
```

**Speed drops during attack**
```bash
# GPU thermal throttling — monitor temps
nvidia-smi -l 1
# Reduce workload: -w 2 instead of -w 3/4
# Set --gpu-temp-abort 85
```

**Status: Exhausted with 0 cracked**
```bash
# Wordlist may be wrong encoding — convert to UTF-8
iconv -f latin1 -t utf8 wordlist.txt -o wordlist_utf8.txt
# Or the hash type may be wrong — re-identify with hashid
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [5 Active Directory Misconfigurations We See in Every Engagement](https://redhound.us/ad-misconfigurations)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
