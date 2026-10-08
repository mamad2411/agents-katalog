---
name: secret-extraction
description: |
  This skill activates when the user mentions "extract secrets", "find credentials",
  "hardcoded passwords", "API keys", "embedded keys", "connection strings", "tokens",
  "secret scanning", "credential extraction", "extract crypto keys", "private keys",
  "certificate extraction", "config extraction", "encryption keys", "AES key",
  "RSA key", "HMAC secret", "JWT secret", "bearer token", "OAuth token",
  "AWS access key", "Azure key", "GCP key", "cloud credentials", "database password",
  "admin password", "default credentials", "service account", "FLOSS", "stack strings",
  "obfuscated strings", "decoded strings", "string analysis", "binary strings",
  "base64 decode", "hex decode", "XOR decode", "entropy analysis", "high entropy",
  "embedded certificate", "PEM key", "PKCS", "keystore", "wallet address",
  "crypto wallet", "bitcoin address", "ethereum address", "extract URLs",
  "extract IPs", "C2 addresses", "callback URLs", "exfiltration endpoints",
  "registry keys", "file paths", "UNC paths", "findcrypt", "signsrch",
  "crypto constants", "magic bytes", "binwalk extract", "firmware secrets",
  "PE resources secrets", "ELF sections", ".rodata secrets", "resource extraction",
  "anti-analysis bypass", "deobfuscate", "decrypt config", "decode payload",
  "RC4 decrypt", "XOR brute force", "string decryption routine", "unpacked strings",
  "credential harvesting from binary", "secret in binary", "sensitive data in executable",
  "password in firmware", "key material", "symmetric key", "asymmetric key",
  "initialization vector", "IV extraction", "salt extraction", "YARA crypto",
  "find secrets in malware", "credential dumping", "embedded config",
  "configuration block", "hardcoded URL", "API endpoint extraction",
  "Slack token", "GitHub token", "Stripe key", "SendGrid key", "Twilio key",
  "Firebase key", "Telegram bot token", "Discord token", "npm token",
  "PyPI token", "NuGet key", "Docker registry token", "Kubernetes secret",
  "HashiCorp Vault token", "Artifactory token", "LDAP password",
  "SMTP credentials", "S3 bucket credentials", "SAS token",
  "password hash", "NTLM hash", "shadow file", "passwd extraction",
  or discusses finding sensitive data, credentials, keys, or secrets in compiled
  binaries, firmware, or executables.
version: 2.0.0
---

# Secret & Credential Extraction

Extract hardcoded credentials, API keys, cryptographic material, certificates, configuration secrets, and sensitive data from compiled binaries. This skill covers the full pipeline: string extraction, pattern matching, entropy analysis, crypto identification, format-specific extraction, and anti-analysis bypass.

## Why This Matters

Hardcoded secrets in binaries are among the highest-impact findings in both penetration testing and malware analysis. A single embedded AWS key grants cloud access. A hardcoded database password opens the entire backend. An extracted C2 encryption key lets you decrypt all traffic. Developers embed secrets assuming compilation hides them -- it does not.

## Methodology Overview

Execute these phases in order. Each phase feeds the next.

### Phase 1 — Triage and Hash

Before touching strings, identify what you have. File type determines extraction strategy.

```bash
file <binary>
sha256sum <binary>
node ${CLAUDE_PLUGIN_ROOT}/scripts/binary-hasher.js hash <binary>
```

Record the hash. Check if this binary was already analyzed:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/analysis-tracker.js check <sha256> string-extraction
```

### Phase 2 — Static String Extraction

Extract all readable strings. Start broad, then filter.

```bash
# ASCII strings, 6+ chars (reduces noise vs default 4)
strings -a -n 6 <binary> > strings_ascii.txt

# UTF-16 LE (Windows wchar_t, most common for Windows binaries)
strings -a -n 6 -el <binary> > strings_utf16.txt

# Combine and deduplicate
cat strings_ascii.txt strings_utf16.txt | sort -u > strings_all.txt
```

Count and triage:

```bash
wc -l strings_all.txt
# < 500 lines: review manually
# 500-5000: filter with patterns below
# > 5000: use targeted extraction only
```

### Phase 3 — Obfuscated String Recovery

FLOSS recovers strings that `strings` cannot see: stack-built strings, tight loops, and runtime-decoded strings. This is where the real secrets hide.

```bash
# Full analysis (slow but thorough)
floss <binary>

# Stack strings only (fast, catches char-by-char construction)
floss --only stack <binary>

# Decoded strings (emulation-based, slowest, highest value)
floss --only decoded <binary>

# JSON output for automated processing
floss -j <binary> > floss_output.json
```

### Phase 4 — Pattern Matching

Apply regex patterns to extracted strings. See `references/credential-patterns.md` for the full pattern library.

**Critical patterns to always check:**

```bash
# Cloud provider keys
grep -E 'AKIA[0-9A-Z]{16}' strings_all.txt              # AWS Access Key
grep -E 'AIza[0-9A-Za-z_-]{35}' strings_all.txt          # GCP API Key
grep -E 'AZURE[A-Za-z0-9+/=]{30,}' strings_all.txt       # Azure tokens

# Authentication
grep -iE '(password|passwd|pwd)\s*[=:]\s*\S+' strings_all.txt
grep -E 'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.' strings_all.txt  # JWT
grep -iE 'bearer\s+[A-Za-z0-9_\-\.]+' strings_all.txt

# Connection strings
grep -iE '(mysql|postgres|mongodb|redis)://[^"'\'']+' strings_all.txt
grep -iE 'Server=.*;.*Password=' strings_all.txt

# Private keys
grep -E 'BEGIN.*(PRIVATE KEY|RSA|EC|DSA|OPENSSH)' strings_all.txt

# API tokens (service-specific)
grep -E 'xox[bpsar]-[0-9a-zA-Z-]+' strings_all.txt       # Slack
grep -E 'ghp_[0-9a-zA-Z]{36}' strings_all.txt             # GitHub PAT
grep -E 'sk_live_[0-9a-zA-Z]{24,}' strings_all.txt        # Stripe
```

### Phase 5 — Entropy Analysis

High-entropy regions indicate encrypted data, compressed payloads, or embedded keys. Entropy above 7.5 bits/byte in a data section signals crypto material or packed content.

```bash
# Section-level entropy (radare2)
r2 -qc 'iS' <binary>
# Look for: .data or .rdata sections with entropy > 7.0

# Binwalk entropy visualization
binwalk -E <binary>
# Generates entropy graph — look for flat high-entropy plateaus (embedded encrypted blobs)

# Byte frequency analysis for specific offsets
r2 -qc 'p= 256 @ <offset>' <binary>
```

Entropy interpretation:
- **0-1**: Null/zero-filled regions
- **1-4**: Structured data, code, ASCII text
- **4-6**: Compressed data or moderately random content
- **6-7.5**: Likely compressed or encrypted
- **7.5-8.0**: Strong encryption, truly random data, or crypto keys

### Phase 6 — Cryptographic Material Identification

Find embedded crypto keys, constants, and algorithm signatures. See `references/crypto-material.md` for comprehensive constant tables.

```bash
# FindCrypt (radare2 plugin) — identifies crypto constants in binary
r2 -qc '/cr' <binary>

# YARA rules for crypto detection
yara -r crypto_signatures.yar <binary>

# Signsrch — finds known crypto/hash/compression signatures
signsrch <binary>

# Manual AES S-Box search (first 16 bytes of forward S-Box)
r2 -qc '/x 637c777bf26b6fc53001672bfed7ab76' <binary>

# Manual RSA public exponent search
r2 -qc '/x 010001' <binary>
```

### Phase 7 — Binary Format-Specific Extraction

Different binary formats store secrets in different locations. See `references/binary-format-extraction.md`.

**PE (Windows)**:
```bash
# Extract resources (configs, certs, embedded files)
r2 -qc 'ir' <binary>

# .rsrc section often contains XML configs, embedded binaries, certificates
# .rdata contains read-only strings, vtables, and often crypto constants
# Overlay data (appended after PE) may contain encrypted payloads
binwalk <binary>  # Shows overlay and embedded file signatures
```

**ELF (Linux)**:
```bash
# .rodata section contains string literals and constants
r2 -qc 'iS~.rodata' <binary>

# Extract .rodata content
objcopy -O binary --only-section=.rodata <binary> rodata.bin
strings -a -n 6 rodata.bin
```

**Firmware**:
```bash
# Extract embedded filesystems, certificates, configs
binwalk -e <binary>
# Recursively scan extracted directories for secrets
find _<binary>.extracted/ -type f | xargs strings -a -n 6 | grep -iE 'password|secret|key|token'
```

### Phase 8 — Anti-Analysis Bypass

When secrets are encrypted or obfuscated at rest in the binary, you must defeat the protection layer. See `references/anti-analysis-bypass.md`.

Common approaches:
1. **XOR encoding**: Try single-byte XOR brute force (256 iterations) looking for known plaintext
2. **Custom encryption**: Identify the decryption function in disassembly, extract the key
3. **Runtime decryption**: Set breakpoints after decryption routines to capture plaintext
4. **Config blobs**: Locate the encrypted config block, find the decryption routine, extract key + IV

```bash
# XOR brute force with known plaintext
r2 -qc 'woF 0x00 0xff @ <offset> !<size>' <binary>

# Find XOR loops in disassembly
r2 -qc 'aaa; /ai xor' <binary>
```

## Recording Findings

Log every extracted secret immediately. Use severity guidelines to classify.

```bash
# Add a secret finding
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "<binary-name>" "<type>" "<value>" "<severity>" "<title>" --db secrets
```

### Finding Types

| Type | Use For |
|------|---------|
| `api-key` | Cloud provider keys, service API keys, access tokens |
| `credential` | Usernames + passwords, connection strings, auth pairs |
| `crypto-key` | AES/RSA/EC keys, IVs, salts, HMAC secrets |
| `token` | JWT, OAuth, bearer, session tokens |
| `url` | C2 endpoints, callback URLs, API endpoints |
| `ip` | Hardcoded IP addresses (especially non-RFC1918) |
| `filepath` | Paths revealing internal infrastructure |
| `registry-key` | Windows registry persistence or config keys |
| `wallet` | Cryptocurrency wallet addresses |
| `certificate` | Embedded X.509 certs, PEM blocks, PKCS bundles |

### Severity Classification

| Severity | Criteria | Examples |
|----------|----------|----------|
| `CRITICAL` | Direct access to systems/data, no additional auth needed | Private keys, admin passwords, DB connection strings with creds, cloud root keys |
| `HIGH` | Significant access, may need context to exploit | API keys with broad permissions, JWT signing secrets, encryption keys, service account creds |
| `MEDIUM` | Limited access or requires chaining | Scoped API keys, internal URLs, email addresses, infrastructure hints |
| `LOW` | Informational value, minimal direct impact | File paths, registry keys, version strings, debug info |
| `INFO` | Requires further analysis to determine impact | Encoded blobs, high-entropy regions, unidentified crypto material |

## Output Template

Report each finding in this format:

```
### [SEVERITY] Finding: <title>
- **Type**: <finding-type>
- **Value**: <extracted-value> (truncated if > 80 chars)
- **Location**: Offset 0x<hex> in <section/resource>
- **Context**: <how it was found, what tool, what pattern matched>
- **Impact**: <what access this grants, what an attacker could do>
- **Confidence**: High | Medium | Low
```

## Tool Reference

| Tool | Purpose | Install |
|------|---------|---------|
| `strings` | Static ASCII/Unicode string extraction | Pre-installed |
| `floss` | Obfuscated/stack/decoded string recovery | `pip install flare-floss` |
| `binwalk` | Entropy analysis, embedded file extraction | `apt install binwalk` |
| `yara` | Pattern matching with crypto/secret rules | `apt install yara` |
| `signsrch` | Crypto/compression signature finder | Manual install |
| `r2` (radare2) | Disassembly, hex search, findcrypt plugin | `apt install radare2` |
| `objcopy` | Section extraction from ELF binaries | Pre-installed (binutils) |
| `xxd` | Hex dump for manual inspection | Pre-installed |
| `openssl` | Certificate/key parsing and validation | Pre-installed |

## References

- `references/credential-patterns.md` — Regex patterns for 50+ secret types across cloud, SaaS, auth, crypto, and infrastructure
- `references/string-analysis.md` — Deep guide to string extraction: static, stack, obfuscated, FLOSS, filtering, and noise reduction
- `references/crypto-material.md` — Identifying crypto keys, constants, S-Boxes, and algorithm signatures in binaries
- `references/binary-format-extraction.md` — Format-specific extraction: PE resources, ELF sections, firmware blobs, overlay data
- `references/anti-analysis-bypass.md` — Defeating encryption, encoding, and obfuscation protecting embedded secrets
