---
name: cyberchef
description: >
  Use CyberChef for data encoding, decoding, encryption, deobfuscation, and
  transformation workflows. Use when the user needs to decode Base64/hex payloads,
  decrypt malware strings, deobfuscate PowerShell or JavaScript, parse certificates,
  extract IOCs, or chain complex data transformations. Covers the recipe concept,
  key operations, chaining, the Magic auto-detect feature, CLI usage (cc),
  self-hosting via Docker, API automation, URL-shareable recipes, and real-world
  malware deobfuscation and CTF workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://github.com/gchq/CyberChef
---

# cyberchef Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to decode, decode, or transform data (Base64, hex, URL encoding, etc.)
- Analyzing obfuscated malware payloads (PowerShell, JavaScript, VBScript)
- Decrypting strings or blobs (XOR, AES, RC4) found in malware samples
- Parsing network packet data, certificates, or JWT tokens
- Extracting IOCs (URLs, IPs, hashes) from blob data
- Decompressing embedded payloads (Gunzip, Brotli, Deflate)
- CTF challenges involving encoding/encryption puzzles
- The user needs to automate transformations via CLI or API

## What CyberChef Does

CyberChef is a web-based Swiss Army knife for data transformations, built by GCHQ.
Users assemble "recipes" by chaining operations from a library of 300+ functions
covering encoding, hashing, encryption, data extraction, formatting, compression,
network protocol parsing, and more. Recipes can be saved, shared via URL, and
executed via CLI or programmatic API — making it equally useful for quick manual
analysis and automated pipelines.

## Installation and Hosting

```bash
# Official hosted instance (no install)
# https://gchq.github.io/CyberChef/

# Self-host via Docker (air-gapped / sensitive data)
docker pull ghcr.io/gchq/cyberchef:latest
docker run -d -p 8080:80 ghcr.io/gchq/cyberchef:latest
# Access: http://localhost:8080

# Build from source
git clone https://github.com/gchq/CyberChef.git
cd CyberChef
npm install
npm run build
# Output: build/prod/ — serve with any HTTP server
npx serve build/prod/ -l 8080

# CyberChef CLI (cc) — Node.js based
npm install -g cyberchef
# Usage: cc --recipe '[{"op":"From Base64","args":[...]}]' --input "SGVsbG8="
```

## Core Concept: Recipes

A recipe is an ordered list of operations applied sequentially to the input.
Each operation transforms the output of the previous step into the input for the next.

```json
[
  { "op": "From Base64", "args": ["A-Za-z0-9+/=", true] },
  { "op": "Gunzip", "args": [] },
  { "op": "From Hex", "args": ["Auto"] },
  { "op": "XOR", "args": [{"option":"Hex","string":"41"}, "Standard", false] }
]
```

Recipes are shareable as URL-encoded strings appended to the CyberChef URL:
```
https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)Gunzip()
```

## Commonly Used Operations

### Encoding / Decoding
| Operation | Purpose |
|-----------|---------|
| From Base64 / To Base64 | Standard and URL-safe base64 |
| From Base32 / To Base32 | Base32 encoding |
| From Hex / To Hex | Hex string to/from bytes |
| URL Decode / URL Encode | Percent-encoding |
| HTML Entity Decode | `&amp;` → `&` |
| From Charcode | Character code arrays to string |
| From Binary | Binary string to bytes |
| Escape String / Unescape String | `\x41` → `A` |
| From Base58 | Bitcoin-style encoding |
| Rot13 | Caesar cipher rotate |

### Compression
| Operation | Purpose |
|-----------|---------|
| Gunzip / Gzip | zlib gzip |
| Inflate / Deflate | Raw deflate |
| Brotli Decompress | Modern web compression |
| Unzip | Extract ZIP archives |
| XZ Decompress | `.xz` streams |

### Hashing
| Operation | Purpose |
|-----------|---------|
| MD5, SHA1, SHA2, SHA3 | Standard hash algorithms |
| HMAC | Keyed hash |
| Bcrypt | Password hash |
| Fletcher Checksum | Simple checksum |

### Encryption / Decryption
| Operation | Purpose |
|-----------|---------|
| AES Decrypt / Encrypt | CBC, GCM, ECB, CFB, OFB modes |
| XOR | Single byte or key XOR |
| RC4 | RC4 stream cipher |
| Blowfish | Legacy symmetric cipher |
| DES / Triple DES | Legacy block cipher |
| ChaCha20 | Modern stream cipher |
| RSA Decrypt | Private key decryption |

### Extraction and Analysis
| Operation | Purpose |
|-----------|---------|
| Extract URLs | Find URLs in blob |
| Extract IP Addresses | Extract IPv4/IPv6 |
| Extract Email Addresses | Email extraction |
| Regular Expression | Regex find/extract/replace |
| Strings | Extract printable strings (like `strings` binary) |
| Magic | Auto-detect encoding and suggest recipes |
| Entropy | Calculate Shannon entropy |

### Network and Certificate
| Operation | Purpose |
|-----------|---------|
| Parse X.509 Certificate | Decode PEM/DER certificate |
| Parse JWT | Decode JWT header/payload |
| HTTP Request | Fetch URL content |
| DNS over HTTPS | Resolve hostname |
| Parse IPv6 Address | IPv6 expansion |

### Defang / Refang
```
Defang URL:   http://evil.com → hxxp://evil[.]com
Defang IP:    192.168.1.1    → 192.168[.]1[.]1
Refang URL:   hxxp://evil[.]com → http://evil.com
```
These are critical for safely handling IOCs in reports and emails.

## Magic Auto-Detect

The **Magic** operation analyzes the input and recursively tries decoding operations,
scoring each by the printable character ratio of the output. It suggests the most
likely encoding chain.

Usage: Input → drag `Magic` operation → run
- Set "Depth" (1–6; higher = slower but finds multi-layer encoding)
- Enable "Extensive language support" for better text scoring
- Enable "Crib" to search for a known plaintext string in the output

Magic is the fastest way to start analyzing an unknown encoded blob.

## Malware Deobfuscation Workflows

### PowerShell Payload (Base64 → Gunzip → Code)
Common pattern: `powershell -enc <base64>`
```
Recipe:
1. From Base64 (alphabet: A-Za-z0-9+/=)
2. Decode Text (UTF-16LE)   ← PowerShell uses UTF-16LE
3. Extract Strings (optional)
4. Regular Expression (filter for URLs/IPs)
```

### XOR-Encrypted Shellcode
```
Recipe:
1. From Hex (if hex-encoded)
2. XOR (key: 0x41 in Hex mode) ← or try keys 1-255
3. Disassemble x86/x64 (to verify shellcode)
```

### Base64 in JavaScript (eval/atob chains)
```
Input: eval(atob('SGVsbG8gV29ybGQ='))
Recipe:
1. Regular Expression: [A-Za-z0-9+/=]{20,} (extract base64)
2. From Base64
3. JavaScript Beautify (optional)
```

### Multi-layer Encoding (CTF common)
```
Recipe:
1. From Base64
2. Reverse
3. From Hex
4. XOR (key: deadbeef)
5. Gunzip
```

### VBScript / Hex-escaped Payload
```
Input: Chr(80)&Chr(111)&Chr(119)...
Recipe:
1. Regular Expression: \d+ (extract numbers)
2. From Charcode (comma separated, decimal)
```

### RC4-Encrypted C2 Config
```
Recipe:
1. From Base64 (get ciphertext bytes)
2. RC4 Decrypt (key: from malware config string)
3. Extract URLs
```

## CLI Usage (cc)

```bash
# Basic decode
echo "SGVsbG8gV29ybGQ=" | cc --recipe "From Base64"

# From file
cc --recipe "From Base64" --input encoded.txt

# Multi-operation recipe (JSON)
cc --recipe '[{"op":"From Base64","args":["A-Za-z0-9+/=",true]},{"op":"Gunzip","args":[]}]' \
   --input payload.b64

# Output to file
cc --recipe "From Hex" --input hex_payload.txt --output decoded.bin

# Quiet mode (output only)
cc --recipe "MD5" --input file.txt -q

# Use .ccr recipe file
cc --recipe-file deobfuscate.ccr --input malware.txt
```

## API Usage (JavaScript / Node.js)

```javascript
const chef = require('cyberchef');

// Simple operation
const result = chef.fromBase64('SGVsbG8gV29ybGQ=');
console.log(result.value);  // Hello World

// Chained recipe
const result2 = chef.bake({
    input: 'SGVsbG8=',
    recipe: [
        { op: 'From Base64', args: ['A-Za-z0-9+/=', true] },
        { op: 'To Hex', args: ['Space', 0] }
    ]
});
console.log(result2.value);  // 48 65 6c 6c 6f
```

## Python Automation via Subprocess

```python
import subprocess
import json

def cyberchef_decode(input_data: str, recipe: list) -> str:
    result = subprocess.run(
        ['cc', '--recipe', json.dumps(recipe), '--input', input_data],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Decode Base64 then XOR
output = cyberchef_decode(
    "encoded_payload",
    [
        {"op": "From Base64", "args": ["A-Za-z0-9+/=", True]},
        {"op": "XOR", "args": [{"option": "Hex", "string": "2b"}, "Standard", False]}
    ]
)
print(output)
```

## Sharing Recipes via URL

CyberChef recipes are URL-shareable — the entire recipe + input is URL-encoded
into the fragment:

```
https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)Gunzip()XOR({'option':'Hex','string':'41'},'Standard',false)&input=SGVsbG8=
```

Generate a shareable URL programmatically:
```javascript
const base = 'https://gchq.github.io/CyberChef/';
const recipe = encodeURIComponent("From_Base64('A-Za-z0-9+/=',true)");
const input = btoa(inputString);
const url = `${base}#recipe=${recipe}&input=${input}`;
```

## CTF Workflow

1. Paste unknown blob into CyberChef input
2. Run **Magic** operation (depth 3) to auto-detect encoding
3. If Magic fails, check: is it Base64? Hex? ROT13? Binary?
4. Look for headers: `PK` = ZIP, `1f 8b` = gzip, `MZ` = PE
5. Use **Entropy** to check if data appears encrypted (>7.5 bits = likely)
6. Try common CTF patterns: multiple Base64 layers, XOR with key in challenge text
7. Use **Strings** operation to find hidden flags in binary blobs

## Common Mistakes

**UTF-16LE encoding**: PowerShell `-EncodedCommand` produces UTF-16LE. After
`From Base64`, add `Decode Text (UTF-16LE)` before parsing.

**Recipe order matters**: Unlike parallel tools, CyberChef applies operations
strictly left-to-right. Wrong order = garbage output.

**Magic with deep encoding**: Set Magic depth ≥ 3 for multi-layer obfuscation.
Depth 1 only tries one level.

**AES key/IV format**: AES operation expects key as Hex by default. If you have
the key as ASCII, change the "Key format" dropdown to UTF-8.

**Large inputs slow Magic**: For files >1MB, Magic becomes very slow. Extract a
representative chunk first.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Building a High-Fidelity Detection Library in Splunk: From Noisy Alerts to Actionable Intelligence](https://redhound.us/splunk-detection-library)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
