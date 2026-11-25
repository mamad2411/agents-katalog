---
name: ctf-crypto
description: Solve CTF cryptography challenges by identifying, analyzing, and exploiting weak crypto implementations in binaries to extract keys or decrypt data. Use for custom ciphers, weak crypto, key extraction, or algorithm identification.
---

# ctf crypto

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- **Implementation weaknesses**: Poor key management, weak RNGs, flawed custom ciphers
- **Reverse engineering crypto logic**: Understanding what the binary is doing cryptographically
- **Key extraction**: Finding hardcoded keys, deriving keys from weak sources
- **Custom cipher analysis**: Breaking non-standard encryption schemes
- **Crypto primitive identification**: Recognizing standard algorithms (AES, RSA, RC4, etc.)
- Search for crypto-related strings and constants
- Identify mathematical operation patterns (XOR, rotation, substitution)
- Recognize standard algorithm signatures (S-boxes, key schedules, magic constants)

## Available sections

- CTF Cryptography
- Purpose
- Conceptual Framework
- Phase 1: Crypto Detection
- Phase 2: Algorithm Identification
- Phase 3: Implementation Analysis
- Phase 4: Key Extraction or Breaking
- Core Methodologies
- Methodology 1: String and Constant Analysis
- Methodology 2: Pattern Recognition
- Methodology 3: Data Flow Analysis
- Methodology 4: Weakness Discovery

## Bundled resources

- patterns.md

Open these resources only if the current task needs deeper detail or executable helpers.
