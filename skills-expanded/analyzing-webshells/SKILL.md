---
name: analyzing-webshells
description: 'Analyzes suspected webshells (PHP, ASPX/ASP, JSP) by detecting dynamic-execution
  sinks, input-to-sink data flow, and common encoder/obfuscation chains, then decoding obvious
  layers to reveal the command interface. Activates for requests to analyze a webshell, identify a
  PHP/ASPX/JSP backdoor, or deobfuscate server-side malicious scripts.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - webshell
  - php
  - aspx
  - server-side
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1505.003
  - T1059
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'MITRE ATT&CK T1505.003 Web Shell — https://attack.mitre.org/techniques/T1505/003/'
  - 'OWASP web shell detection guidance — https://owasp.org/'
---

# Analyzing Webshells

## When to Use

- You found a suspicious server-side script (`.php`, `.aspx`, `.jsp`, `.asp`) and need to confirm
  it is a webshell and understand its command interface.
- You are triaging a web-server compromise and want to classify dropped scripts.

**Do not use** a live web server to execute the script to "test" it — that runs attacker code.
Analyze the source statically.

## Prerequisites

- The suspect script file(s), read inertly.

## Safety & Handling

- Read the file statically; never deploy or request it on a live server. Defang any URLs.

## Workflow

### Step 1: Detect execution sinks and input flow

```bash
python scripts/analyst.py scan shell.php
```

Flags dynamic-execution sinks (`eval`, `assert`, `system`, `exec`, `passthru`, `Runtime.exec`,
ASPX `eval()`/`Process.Start`) and whether request input (`$_GET`/`$_POST`/`Request`) reaches them.

### Step 2: Identify obfuscation/encoder chains

Detects `base64_decode`, `gzinflate`, `str_rot13`, `eval(chr(...))`, hex `\x` strings, and
`FromBase64String` chains commonly wrapping the payload.

### Step 3: Decode obvious layers

Apply base64/rot13/gzinflate where present to reveal the inner command interface (best-effort,
non-executing).

### Step 4: Classify and report

Note the language, the password/parameter gate (if any), and capabilities (file manager, command
exec, SQL, upload); defang IOCs.

## Validation

- A flagged file pairs an execution sink with attacker-controlled input.
- Encoder chains are identified and, where safe, decoded statically.
- Capability classification is backed by concrete code evidence.

## Pitfalls

- Legitimate admin tools that also use `eval`/`system` — corroborate with input flow.
- Multi-stage shells that fetch the real logic remotely.
- Deeply nested or runtime-built obfuscation that static decode only partly unwinds.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scanner.
- ATT&CK T1505.003 (linked in frontmatter).
