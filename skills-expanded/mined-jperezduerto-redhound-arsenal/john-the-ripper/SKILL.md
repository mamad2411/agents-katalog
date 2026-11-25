---
name: john-the-ripper
description: >
  Build, extend, and operate John the Ripper — a fast password cracking tool supporting
  hundreds of hash types. Use when cracking password hashes, extracting hashes from archives
  or documents, performing wordlist or rule-based attacks, or recovering credentials during
  a penetration test. Covers community vs jumbo builds, supported formats, auto-detect, wordlist
  mode, rule sets (Jumbo, KoreLogic, All), incremental mode, mask mode, *2john extraction
  utilities, session management, potfile, and comparison with Hashcat.
license: GPLv2
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/openwall/john
  language: C
---

# john-the-ripper Agent Skill

## When to Use This Skill

Use this skill when:
- Cracking password hashes obtained during a penetration test
- Extracting crackable hashes from ZIP, RAR, PDF, SSH keys, KeePass, or BitLocker
- The user asks about john, JtR, or john the ripper
- Choosing between wordlist, rules, incremental, or mask attack modes
- Managing crack sessions, restoring interrupted jobs, or reading the potfile
- Deciding whether to use John or Hashcat for a specific hash type

## What John the Ripper Does

John the Ripper is an open-source password cracking tool that supports hundreds of hash types
and five primary attack modes. The Jumbo community release significantly extends the core
version with additional formats, rule sets, and *2john extraction utilities. It is used when
Hashcat is unavailable (CPU-only environments) or when its rule syntax or format auto-detection
is more convenient.

## Installation

```bash
# Community (core) — Kali / Debian
sudo apt install john

# Jumbo (recommended — adds formats, rules, *2john tools)
sudo apt install john                   # Kali ships Jumbo by default

# From source (Jumbo)
sudo apt install build-essential libssl-dev yasm libgmp-dev libpcap-dev pkg-config libbz2-dev
git clone https://github.com/openwall/john -b bleeding-jumbo
cd john/src && ./configure && make -s clean && make -sj$(nproc)
# Binary at: john/run/john

# Install to PATH
sudo ln -s $(pwd)/john/run/john /usr/local/bin/john

# Docker
docker pull ghcr.io/openwall/john
docker run --rm -v $(pwd):/data ghcr.io/openwall/john /data/hashes.txt

# Verify
john --list=build-options
john --version
```

## Supported Hash Formats

```bash
# List all supported formats
john --list=formats

# List formats matching a keyword
john --list=formats | grep -i ntlm
john --list=formats | grep -i bcrypt
john --list=formats | grep -i sha256

# Common format names
# md5crypt        — $1$ Linux MD5
# sha512crypt     — $6$ Linux SHA-512 (/etc/shadow modern)
# sha256crypt     — $5$
# bcrypt          — $2b$ (slow, GPU-friendly via Hashcat instead)
# NT              — Windows NTLM (unsalted MD4)
# lm              — Windows LM (very weak, splits into 7-char halves)
# mscash          — MS-CACHE v1 (DCC)
# mscash2         — MS-CACHE v2 (DCC2)
# krb5asrep       — Kerberos AS-REP hash (AS-REProasting)
# krb5tgs         — Kerberos TGS hash (Kerberoasting)
# zip             — ZIP encrypted archives
# rar5            — RAR5 encrypted archives
# pdf             — PDF encrypted files
# SSH             — SSH private key passphrases
# KeePass         — KeePass database master password
# BitLocker       — BitLocker recovery key / password
# WPA             — WPA/WPA2 handshake (PMKID or 4-way)
# PKZIP           — Legacy PKZIP encryption
# office          — Microsoft Office 2007–2019 documents
# pgpdisk         — PGP/GPG disk encryption
```

## Hash Extraction (*2john Utilities)

```bash
# ZIP archive
zip2john secret.zip > zip.hash
zip2john -S secret.zip > zip.hash          # Skip checksum validation

# RAR archive
rar2john secret.rar > rar.hash

# 7-Zip
7z2john secret.7z > 7z.hash

# PDF
pdf2john.pl secret.pdf > pdf.hash          # Perl version
pdf2john secret.pdf > pdf.hash             # Binary version

# SSH private key
ssh2john id_rsa > ssh.hash

# KeePass 1.x / 2.x
keepass2john keepass.kdbx > keepass.hash
keepass2john -k keyfile.key keepass.kdbx > keepass.hash   # with keyfile

# BitLocker
bitlocker2john -i disk.img > bitlocker.hash

# Microsoft Office
office2john secret.docx > office.hash

# WPA/WPA2 (from pcap)
hccapx2john capture.hccapx > wpa.hash
wpapcap2john capture.pcap > wpa.hash

# PGP / GPG private key
gpg2john private.gpg > gpg.hash

# /etc/shadow (Linux)
sudo cat /etc/shadow > shadow.txt
# John reads shadow directly — no conversion needed
john shadow.txt

# NTLM from secretsdump output (impacket)
# secretsdump.py -outputfile dump domain/admin:pass@dc.local
# Results in dump.ntds; extract NTLM column:
cut -d: -f4 dump.ntds > ntlm.hash

# Combine passwd + shadow
unshadow /etc/passwd /etc/shadow > combined.txt
john combined.txt
```

## Attack Modes

### Auto-Detect (Single-Crack) Mode

```bash
# John auto-detects format and applies GECOS rules first
john hashes.txt

# Force specific format
john --format=NT hashes.txt
john --format=sha512crypt shadow.txt

# Auto-detect format without cracking (just identify)
john --show=left hashes.txt    # show uncracked
```

### Wordlist Mode

```bash
# Basic wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# With format
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT hashes.txt

# With pipe from stdin
cat wordlist.txt | john --stdin hashes.txt
```

### Rules-Based Attack

Rules mutate wordlist candidates. John Jumbo ships many built-in rulesets.

```bash
# Built-in rulesets
john --wordlist=rockyou.txt --rules=Jumbo hashes.txt         # Jumbo default rules
john --wordlist=rockyou.txt --rules=KoreLogic hashes.txt     # KoreLogic rules (extensive)
john --wordlist=rockyou.txt --rules=All hashes.txt           # All known rules (slow)
john --wordlist=rockyou.txt --rules=Best64 hashes.txt        # Top 64 Hashcat-equivalent rules
john --wordlist=rockyou.txt --rules=T0XlC hashes.txt         # T0XlC specialized rules
john --wordlist=rockyou.txt --rules=Single hashes.txt        # GECOS/username mangling

# Custom rules in john.conf / john.ini
# [List.Rules:MyRules]
# Az"[0-9]"             — append digit
# A0"[!@#$]"            — prepend symbol
# c                     — capitalize first char
# r                     — reverse word
# d                     — duplicate word
# l                     — lowercase all

# List available rulesets
john --list=rules
```

### Incremental Mode (Brute Force)

```bash
# Full brute force with built-in character sets
john --incremental hashes.txt              # Default charset (all printable)
john --incremental=Alpha hashes.txt        # a-z only
john --incremental=Digits hashes.txt       # 0-9 only
john --incremental=Alnum hashes.txt        # a-z 0-9
john --incremental=ASCII hashes.txt        # All 95 printable ASCII

# Limit length
john --incremental=Alpha --min-length=6 --max-length=8 hashes.txt
```

### Mask Mode (Hybrid Brute Force)

```bash
# Mask syntax: ?l=lowercase ?u=upper ?d=digit ?s=symbol ?a=all ?w=word
john --mask='?u?l?l?l?d?d?d?d' hashes.txt       # Aaaa1234 pattern
john --mask='Password?d?d' hashes.txt             # Password followed by 2 digits
john --mask='?w?d?d' --wordlist=rockyou.txt hashes.txt  # word + 2 digits

# Define custom charset
john --mask='?1?1?1?d?d' --1='[aeiou]' hashes.txt

# Combine with rules
john --mask='?w?d?d?s' --wordlist=rockyou.txt --rules hashes.txt
```

### Prince Mode (PRINCE algorithm)

```bash
# Generates combinations from wordlist elements
john --prince=wordlist.txt hashes.txt
john --prince=wordlist.txt --rules=Jumbo hashes.txt
```

## Session Management

```bash
# Start named session
john --session=myengagement --wordlist=rockyou.txt hashes.txt

# Restore interrupted session
john --restore=myengagement

# Restore default session
john --restore

# List active / interrupted sessions
ls ~/.john/

# Show progress without interrupting
kill -USR1 $(pidof john)         # sends SIGUSR1 — prints status to stdout
```

## Potfile and Showing Cracked Passwords

```bash
# Cracked passwords are stored in ~/.john/john.pot by default
cat ~/.john/john.pot

# Show cracked passwords for a hash file
john --show hashes.txt
john --show --format=NT ntlm.hash

# Show uncracked
john --show=left hashes.txt

# Use a custom potfile location
john --pot=./engagement.pot --wordlist=rockyou.txt hashes.txt
john --pot=./engagement.pot --show hashes.txt

# Clear potfile (reset cracked state)
> ~/.john/john.pot
```

## Cracking Specific Hash Types

### Linux /etc/shadow

```bash
unshadow /etc/passwd /etc/shadow > combined.txt
john --wordlist=rockyou.txt --rules=Jumbo combined.txt
john --show combined.txt
```

### Windows NTLM (from secretsdump / mimikatz)

```bash
# secretsdump output: user:rid:lmhash:nthash
# Extract NT hashes:
cut -d: -f4 dump.ntds | sort -u > ntlm_hashes.txt
john --format=NT --wordlist=rockyou.txt --rules=Jumbo ntlm_hashes.txt
```

### Kerberoasting (TGS Hashes)

```bash
# Hashes from Impacket GetUserSPNs.py or Rubeus
john --format=krb5tgs --wordlist=rockyou.txt --rules=Jumbo kerb_hashes.txt
```

### AS-REP Roasting

```bash
john --format=krb5asrep --wordlist=rockyou.txt asrep_hashes.txt
```

### SSH Key Passphrase

```bash
ssh2john id_rsa > id_rsa.hash
john --wordlist=rockyou.txt --rules id_rsa.hash
john --show id_rsa.hash
```

### KeePass Database

```bash
keepass2john database.kdbx > keepass.hash
john --wordlist=rockyou.txt --rules=Jumbo keepass.hash
```

## Common Workflows

### Post-Compromise Credential Harvesting

```bash
# 1. Extract hashes from domain controller
impacket-secretsdump domain/admin:pass@dc.local -outputfile dump

# 2. Extract NT hashes
cut -d: -f4 dump.ntds | sort -u > ntlm.hash

# 3. Fast wordlist attack
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt ntlm.hash

# 4. Rules pass
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt --rules=Jumbo ntlm.hash

# 5. Review results
john --format=NT --show ntlm.hash | tee cracked.txt
```

### CTF Hash Cracking Pipeline

```bash
# 1. Identify hash type
echo '$6$rounds=5000$salt$hash...' | john --stdin --format=auto --show

# 2. Quick crack attempt
john --wordlist=/usr/share/wordlists/rockyou.txt --format=sha512crypt target.hash

# 3. Rules pass
john --wordlist=/usr/share/wordlists/rockyou.txt --rules=All target.hash

# 4. Incremental fallback (short passwords only)
john --incremental=Alnum --min-length=1 --max-length=6 target.hash
```

## John vs Hashcat

| Feature | John the Ripper | Hashcat |
|---|---|---|
| GPU acceleration | Limited (OpenCL) | Excellent (CUDA/OpenCL) |
| CPU performance | Strong | Strong |
| Rule syntax | John rules (verbose) | Hashcat rules (compact) |
| Format support | Wider (many *2john utils) | Fewer, but major types covered |
| Auto-detect format | Yes | No (must specify -m mode) |
| Incremental (brute) | Built-in | Built-in |
| Mask attack | `--mask` | `-a 3` |
| Prince mode | Built-in | Separate binary |
| Best for | CPU-only, broad format support, CTF convenience | GPU rig, maximum speed on common types |

```bash
# Equivalent commands
# John: wordlist + rules
john --wordlist=rockyou.txt --rules=Jumbo hashes.txt

# Hashcat equivalent
hashcat -m 1000 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

## Advanced Techniques

### Loopback Mode (feed cracked passwords back)

```bash
# Feed cracked passwords as new wordlist candidates
john --wordlist=rockyou.txt --rules hashes.txt
john --loopback hashes.txt          # use john.pot as wordlist + apply rules again
```

### Custom Wordlist Generation

```bash
# Generate targeted wordlist with crunch
crunch 8 10 abcdefghijklmnopqrstuvwxyz0123456789 -o custom.txt
john --wordlist=custom.txt hashes.txt

# Use CeWL to generate wordlist from target site
cewl https://target.example.com -d 3 -m 6 -w site_words.txt
john --wordlist=site_words.txt --rules=Jumbo hashes.txt
```

### Distributed Cracking

```bash
# Split hash file across multiple john instances
split -n l/4 hashes.txt chunk_
john --wordlist=rockyou.txt --rules chunk_aa &
john --wordlist=rockyou.txt --rules chunk_ab &
john --wordlist=rockyou.txt --rules chunk_ac &
john --wordlist=rockyou.txt --rules chunk_ad &

# Merge potfiles afterward
cat node1.pot node2.pot node3.pot node4.pot | sort -u > combined.pot
```

## Troubleshooting

| Issue | Fix |
|---|---|
| `No password hashes loaded` | Wrong `--format=`; use `--list=formats` to find correct name |
| Very slow bcrypt/scrypt | Switch to Hashcat with GPU; these are inherently slow |
| Potfile already contains all hashes | Delete or move `~/.john/john.pot` |
| `Segmentation fault` on large file | Split hash file into chunks |
| Format auto-detect wrong | Force with `--format=`; run `john --test --format=X` to validate |
| Rules not found | Ensure using Jumbo build; check `john --list=rules` |
| Session restore fails | Check `~/.john/` for `.rec` file; use `--restore=sessionname` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [5 Active Directory Misconfigurations We See in Every Engagement](https://redhound.us/ad-misconfigurations)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
