---
name: identifying-cryptographic-routines-in-binaries
description: 'Identifies cryptographic algorithms embedded in a binary by scanning for well-known
  constants and tables (AES S-box, SHA-256/MD5 init constants, ChaCha sigma, CRC32 table, base64
  alphabet). Activates for requests to identify crypto in a binary, find AES/SHA constants, or
  detect which encryption algorithm a sample uses.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - cryptography
  - constants
  - aes
  - detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1486
  - T1573
d3fend:
  - D3-SDA
  - D3-DA
references:
  - 'FIPS 197 (AES) S-box — https://csrc.nist.gov/publications/detail/fips/197/final'
  - 'FIPS 180-4 (SHA-2) constants — https://csrc.nist.gov/publications/detail/fips/180/4/final'
---

# Identifying Cryptographic Routines in Binaries

## When to Use

- You need to determine which cryptographic algorithms a sample implements (ransomware crypto, C2
  encryption, config protection) by locating constant tables.
- You want fast triage before manually reversing the crypto routine.

**Do not use** constant detection as proof of a specific mode/usage — it identifies the primitive,
not how it is applied. This skill reads the binary statically and executes nothing.

## Prerequisites

- The binary (read inertly).

## Safety & Handling

- Read bytes statically; treat the sample as malicious data.

## Workflow

### Step 1: Scan for crypto constants

```bash
python scripts/analyst.py scan sample.bin
```

Searches for AES S-box/Te tables, SHA-256 H/K init constants, MD5 init, ChaCha/Salsa `expand
32-byte k` sigma, the CRC32 polynomial table, and the base64 alphabet, reporting offsets.

### Step 2: Corroborate with imports/strings

Pair constant hits with crypto API imports (`CryptDecrypt`, `BCryptEncrypt`, `EVP_*`) or library
strings to confirm.

### Step 3: Locate the routine

Use the constant offset to find the referencing function for deeper reversing/key extraction.

### Step 4: Document

Record which primitives are present and where, mapping to behavior (e.g., AES → file encryption).

## Validation

- Each hit references a real, named constant table (not a coincidental byte run).
- Detected primitives are corroborated by imports/strings where possible.
- Offsets point into the binary and can be navigated in a disassembler.

## Pitfalls

- Statically linked crypto libraries adding constants unused by the malware's logic.
- Custom/modified S-boxes evading exact-match detection.
- Assuming AES presence implies ransomware — corroborate with behavior.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scanner.
- FIPS 197 and FIPS 180-4 constant references (linked in frontmatter).
