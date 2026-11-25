---
name: crunch
description: >
  Build, extend, and operate Crunch — a wordlist generator for creating custom character-set
  and pattern-based wordlists for password attacks. Use when the user needs to generate
  wordlists by character set, length range, custom patterns, or permutations. Covers
  installation, character set syntax, built-in charset files, pattern mode with placeholders,
  output to file, piping to hashcat/john/hydra, compression options, output limiting, start
  and end string control, permutation mode, and integration with password cracking methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  stars: 'Kali native tool'
---

# crunch Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to generate a wordlist based on known password patterns (e.g., 8 chars, 2 uppercase + 4 lower + 2 digits)
- Generating all combinations of a specific character set within a length range
- Creating targeted wordlists when you know part of the password (name + 4 digits, company + year)
- Pattern-based generation using Crunch's `-t` flag (known character positions)
- Piping generated passwords directly into hashcat, john, or hydra without saving to disk

## What Crunch Does

Crunch is a wordlist generator built into Kali Linux that creates wordlists based on criteria you specify: a minimum and maximum length, a character set, optional patterns, and output filters. It generates every possible combination in a deterministic order. Unlike CeWL (web-based) or CUPP (profile-based), Crunch is a pure combinatorial generator — useful when you know structural constraints of a target password.

## Installation

### Kali Linux (pre-installed or apt)
```bash
sudo apt update && sudo apt install -y crunch
crunch --help
```

### Ubuntu/Debian
```bash
sudo apt install -y crunch
```

### From Source
```bash
# Not commonly needed — apt version is current
# Source available via apt source
apt-get source crunch
```

### Verify Installation
```bash
which crunch
crunch 4 4 abc 2>/dev/null | head -5
# Should output: aaaa, aaab, aaac, aaba, aabb...
```

## Core Concepts

### Syntax
```
crunch <min-len> <max-len> [charset] [options]
```

- `min-len`: Minimum password length to generate
- `max-len`: Maximum password length to generate
- `charset`: Character set string (every char listed is used); if omitted, uses default lowercase
- Output goes to stdout unless `-o` is specified

### Generation Order
Crunch generates in lexicographic order based on the character set string position. The first character in the set appears first:
```bash
crunch 2 2 abc
# Output: aa, ab, ac, ba, bb, bc, ca, cb, cc
```

### Output Volume Warning
Combinatorial explosion is real:
```bash
# 8-character lowercase only: 26^8 = 208 billion words ~ 1.8 TB
crunch 8 8 abcdefghijklmnopqrstuvwxyz --stdout | wc -c

# Always estimate first:
# Entries = charset_size ^ length (for fixed length)
python3 -c "print(26**8)"  # 208827064576
```

## Character Set Syntax

### Inline Character Sets
```bash
# Lowercase letters only
crunch 6 8 abcdefghijklmnopqrstuvwxyz -o /tmp/lower.txt

# Uppercase letters only
crunch 6 8 ABCDEFGHIJKLMNOPQRSTUVWXYZ -o /tmp/upper.txt

# Digits only
crunch 4 6 0123456789 -o /tmp/numeric.txt

# Alphanumeric (no symbols)
crunch 6 8 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -o /tmp/alnum.txt

# Lowercase + digits
crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 -o /tmp/lower_num.txt

# Custom small set (known chars)
crunch 4 6 acme13 -o /tmp/acme_chars.txt

# PIN codes (4-8 digit numeric)
crunch 4 8 0123456789 -o /tmp/pins.txt
```

### Built-in Charset File
Crunch ships with `/usr/share/crunch/charset.lst`:
```bash
cat /usr/share/crunch/charset.lst
# Named charsets:
# lalpha          = abcdefghijklmnopqrstuvwxyz
# ualpha          = ABCDEFGHIJKLMNOPQRSTUVWXYZ
# numeric         = 0123456789
# symbols14       = !"#$%&'()*+,-./ (14 symbols)
# symbols14b      = :;<=>?@[\]^_`{|}~ (14 more symbols)
# ualpha-numeric  = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
# lalpha-numeric  = abcdefghijklmnopqrstuvwxyz0123456789
# mixalpha        = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
# mixalpha-numeric = full mixed alphanumeric
# mixalpha-numeric-all = mixed + all symbols
```

### Using charset.lst
```bash
# -f specifies charset file, then charset name
crunch 6 8 -f /usr/share/crunch/charset.lst lalpha -o /tmp/lower.txt
crunch 8 8 -f /usr/share/crunch/charset.lst mixalpha-numeric -o /tmp/mixed.txt
crunch 4 6 -f /usr/share/crunch/charset.lst numeric -o /tmp/nums.txt

# Symbols
crunch 8 10 -f /usr/share/crunch/charset.lst mixalpha-numeric-all -o /tmp/full.txt
```

## Pattern Mode (-t)

The `-t` flag enables pattern-based generation. Use placeholder characters to define fixed positions:

| Placeholder | Meaning |
|-------------|---------|
| `@` | Lowercase letter (a-z) |
| `,` | Uppercase letter (A-Z) |
| `%` | Numeric digit (0-9) |
| `^` | Symbol |
| Any other char | Literal — fixed in that position |

```bash
# Pattern examples:
# Pass@@@@ — the word "Pass" followed by 4 lowercase letters
crunch 8 8 -t Pass@@@@ -o /tmp/pass_pattern.txt

# Acme%%%% — "Acme" followed by 4 digits
crunch 8 8 -t Acme%%%% -o /tmp/acme_year.txt
# Output: Acme0000, Acme0001, ... Acme9999

# 2 uppercase, 4 lowercase, 2 digits
crunch 8 8 -t ,,@@@@%% -o /tmp/complex.txt

# Known pattern: first 3 chars known, last 4 unknown numeric
crunch 7 7 -t Cor%%%% -o /tmp/corp_pins.txt

# Symbol at end
crunch 9 9 -t Summer%%^ -o /tmp/summer_pass.txt
```

### Pattern with Custom Sets
Combining `-t` with custom charset (the charset string maps to `@` substitutions):
```bash
# Use custom charset for @ positions
crunch 8 8 -t @@@@%%%% abc123 -o /tmp/restricted.txt
# The 4 @ positions use chars: a, b, c, 1, 2, 3
# The 4 % positions are always digits 0-9
```

## Output Options

### Output to File
```bash
# Basic file output
crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 -o /tmp/wordlist.txt

# Append to existing file (use shell redirect)
crunch 9 9 -t Summer%%% >> /tmp/wordlist.txt

# Split output into multiple files of N lines each
crunch 6 8 lalpha -f /usr/share/crunch/charset.lst -o START -c 1000000
# Creates: crunch000000.txt, crunch000001.txt, etc. (1M lines each)
# START is a literal keyword that triggers splitting mode
```

### Compressed Output
```bash
# gzip compression
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha-numeric \
  -o /tmp/wordlist.gz -z gzip

# bzip2 compression (better ratio, slower)
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha-numeric \
  -o /tmp/wordlist.bz2 -z bzip2

# lzma compression (best ratio, slowest)
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha-numeric \
  -o /tmp/wordlist.lzma -z lzma

# Decompress for use
gunzip -c /tmp/wordlist.gz | hashcat ...
```

### Limiting Output
```bash
# Limit to N lines
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha -c 100000 -o /tmp/first100k.txt

# Limit by byte count (not built-in; use head)
crunch 8 8 abcdefghijklmnopqrstuvwxyz | head -c 500M > /tmp/500mb.txt
```

### Start and End Strings
```bash
# Start from a specific string (resume or skip)
crunch 8 8 abcdefghijklmnopqrstuvwxyz -s abcdefgh -o /tmp/from_abcdefgh.txt

# End at a specific string
crunch 8 8 abcdefghijklmnopqrstuvwxyz -e abczzzzz -o /tmp/up_to.txt

# Both: generate a slice of the keyspace
crunch 8 8 abcdefghijklmnopqrstuvwxyz \
  -s password -e passzzz -o /tmp/slice.txt
```

## Piping to Attack Tools

Piping to stdout avoids disk I/O entirely — essential for large keyspaces:

### Pipe to Hashcat
```bash
# Pipe directly: avoids disk entirely
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha-numeric | \
  hashcat -a 0 -m 1000 /tmp/hashes.txt --stdin

# Pipe with NTLM (Active Directory)
crunch 8 10 abcdefghijklmnopqrstuvwxyz0123456789 | \
  hashcat -a 0 -m 1000 /tmp/ntlm_hashes.txt --stdin -O

# WPA/WPA2 (handshake)
crunch 8 8 -t Summer%%% | \
  hashcat -a 0 -m 22000 /tmp/handshake.22000 --stdin -O
```

### Pipe to John the Ripper
```bash
crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 | \
  john --stdin --format=NT /tmp/hashes.txt

# With status
crunch 8 8 -t Corp@@@% | \
  john --stdin --format=sha512crypt /tmp/shadow_hashes.txt
```

### Pipe to Hydra (Online Attacks)
```bash
# HTTP form login
crunch 6 8 abcdefghijklmnopqrstuvwxyz0123456789 | \
  hydra -l admin -P - \
    https-post-form "target.com/login:user=^USER^&pass=^PASS^:Invalid"

# SSH
crunch 6 8 -f /usr/share/crunch/charset.lst lalpha | \
  hydra -l jsmith -P - ssh://10.10.10.50 -t 4 -V

# FTP
crunch 4 6 0123456789 | \
  hydra -l ftpuser -P - ftp://10.10.10.50 -V
```

### Pipe to Medusa
```bash
crunch 6 8 abcdefghijklmnopqrstuvwxyz | \
  medusa -h 10.10.10.50 -u admin -P - -M http -m DIR:/login
```

## Permutation Mode

Crunch can generate permutations (no repetition) of a given string:
```bash
# All permutations of "aAbB" (4! = 24 combinations)
crunch 4 4 -p aAbB

# Permutations of known password components
crunch 1 1 -p Summer 2024 !

# This outputs all orderings of the words/chars given
# (treats each space-delimited token as a unit)
crunch 1 1 -p "password" "company" "2024" "!"
# Output: all 4! = 24 orderings concatenated
```

Note: `-p` mode ignores min/max and outputs permutations of the specified strings/chars.

## Common Workflows

### Corporate Password Pattern Attack
```bash
# Known pattern: CompanyName + 4-digit year (Acme + 2022-2025)
crunch 8 8 -t Acme%%%% -o /tmp/acme_years.txt
# Then crack
hashcat -a 0 -m 1000 /tmp/ntlm.txt /tmp/acme_years.txt

# Variations: lowercase + year
crunch 8 8 -t acme%%%% >> /tmp/acme_years.txt

# Season + year pattern
for season in Spring Summer Fall Winter Autumn; do
  for year in 2022 2023 2024 2025; do
    echo "${season}${year}"
    echo "${season}${year}!"
    echo "${season}@${year}"
  done
done > /tmp/seasonal.txt
hashcat -a 0 -m 1000 /tmp/ntlm.txt /tmp/seasonal.txt
```

### PIN Code Generation
```bash
# All 4-digit PINs (10,000 entries)
crunch 4 4 0123456789 -o /tmp/pins4.txt

# All 6-digit PINs (1,000,000 entries)
crunch 6 6 0123456789 -o /tmp/pins6.txt

# Common PIN patterns (not all combos — targeted)
# Start with most common PINs
echo -e "1234\n0000\n1111\n1212\n7777\n1004\n2000\n4444\n2222\n6969" > /tmp/common_pins.txt
```

### WPA Default Password Patterns
```bash
# Many routers use 8-digit numeric PINs by default
crunch 8 8 0123456789 | \
  hashcat -a 0 -m 22000 /tmp/handshake.22000 --stdin

# ISP default patterns (e.g., "admin" + 4 digits)
crunch 9 9 -t admin%%%% -o /tmp/isp_defaults.txt

# Common WPA default: random lowercase 8-char (small charset sometimes)
crunch 8 8 abcdefghijklmnopqrstuvwxyz -o /tmp/lower8.txt
```

### Hybrid Attack Prep
```bash
# Use CeWL for base words, Crunch for suffixes
# Append 2-digit suffixes to each CeWL word
while IFS= read -r word; do
  crunch 2 2 0123456789 | while IFS= read -r suffix; do
    echo "${word}${suffix}"
  done
done < /tmp/cewl_words.txt > /tmp/hybrid_cewl_digits.txt

# Or use Hashcat hybrid mode (faster)
hashcat -a 6 -m 1000 /tmp/ntlm.txt /tmp/cewl_words.txt "?d?d?d?d"
```

### WPA Attack with Crunch + Aircrack-ng
```bash
# Target WPA with 8-lowercase-char passwords (pipe to aircrack)
crunch 8 8 abcdefghijklmnopqrstuvwxyz | \
  aircrack-ng -w - -b AA:BB:CC:DD:EE:FF /tmp/handshake.cap
```

## Estimating Wordlist Size

Always estimate before generating:
```python
#!/usr/bin/env python3
import math, sys

charset_size = int(sys.argv[1])  # e.g., 36 for alphanumeric
min_len = int(sys.argv[2])
max_len = int(sys.argv[3])

total = sum(charset_size**l for l in range(min_len, max_len+1))
print(f"Total words: {total:,}")
print(f"Estimated size: {total * (max_len + 1) / 1e9:.2f} GB (approx)")
```

```bash
python3 estimate.py 36 6 8    # 36-char set, 6-8 length
# Total words: 2,821,109,907,456
# Estimated size: 25.39 GB (approx)
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| Hashcat | Primary target — pipe via `--stdin` or use generated file |
| John the Ripper | Pipe via `--stdin` for any hash format |
| Hydra | Pipe for online password attacks |
| Medusa | Pipe for multi-protocol online attacks |
| Aircrack-ng | Pipe wordlist directly for WPA/WEP cracking |
| CeWL | CeWL generates base words; Crunch appends numeric suffixes |
| Wifite | Wifite accepts wordlist files; feed Crunch output via file |
| Mentalist | Alternative GUI-based wordlist generator |
| CUPP | Profile-based wordlist; complement with Crunch combinatorial |

## Troubleshooting

**Output too large — disk fills up**
```bash
# Never generate massive wordlists to disk — pipe instead
crunch 8 10 -f /usr/share/crunch/charset.lst mixalpha-numeric | \
  hashcat -a 0 -m 1000 /tmp/hashes.txt --stdin

# Or use hashcat's built-in mask attack (much faster)
hashcat -a 3 -m 1000 /tmp/hashes.txt "?l?l?l?l?l?l?l?l"  # 8 lowercase
```

**crunch: invalid option**
```bash
# Verify syntax: min max charset options (charset before flags in some versions)
crunch 8 8 abc123 -t @@@@%%%% -o /tmp/out.txt
# If charset.lst needed, -f comes before -o
crunch 8 8 -f /usr/share/crunch/charset.lst lalpha -o /tmp/out.txt
```

**Pattern `-t` not working**
- Ensure pattern length equals min=max (for fixed-length patterns)
- Verify placeholder chars are `@`, `,`, `%`, `^` (literal commas not spaces)
- Quote the pattern: `-t "Pass@@%%"`

**No output / empty file**
```bash
# Test: generate small output to stdout first
crunch 4 4 abc | head -10
# Check that min ≤ max
# Check charset has content
```

**Charset.lst path not found**
```bash
find / -name "charset.lst" 2>/dev/null
# Usually: /usr/share/crunch/charset.lst
# Or copy from apt: sudo apt reinstall crunch
```

**Hydra disconnecting when piping**
```bash
# Slow down hydra to match pipe speed
crunch 6 8 abcdefghijklmnopqrstuvwxyz | \
  hydra -l admin -P - ssh://10.10.10.50 -t 1 -W 3
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
