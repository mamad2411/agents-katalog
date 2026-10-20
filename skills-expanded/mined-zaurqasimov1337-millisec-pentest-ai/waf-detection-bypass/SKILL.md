---
name: waf-detection-bypass
description: Detect a Web Application Firewall and apply vendor-specific evasion so injection/exploitation payloads get through. Use early (right after recon) and whenever a payload is blocked (403/406/429/challenge). Covers ModSecurity/CRS, Cloudflare, Imperva/Incapsula, F5 BIG-IP, Akamai, AWS WAF, Sucuri, Barracuda. Learned from 0xInfection/Awesome-WAF.
---

# WAF Detection & Bypass

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`

## 1. Fingerprint the WAF
```bash
dr wafw00f $U -a          # identify vendor(s)
```
Also infer from behaviour: block page wording, `Server`/`cf-ray`/`x-iinfo`/`x-sucuri` headers,
status on a canary payload (`?q=<script>alert(1)</script>` → 403/406/429/999/503 = WAF).

## 2. Establish the block signal (baseline)
Send a benign request and a known-malicious canary; compare status/length/body. That tells you
exactly what the WAF blocks, so you can measure when an evasion succeeds.
```bash
curl -s -o /dev/null -w "%{http_code}\n" "$U/?q=benign"
curl -s -o /dev/null -w "%{http_code}\n" "$U/?q=' OR 1=1-- -"
```

## 3. Iterate evasion technique-by-technique (until it passes or is exhausted)
General techniques (try in order, re-test the block signal after each):
- **Case toggling:** `SeLeCt`, `UnIoN`
- **Inline comments / keyword splitting:** `/**/`, `UN/**/ION`, MySQL versioned `/*!50000UNION*/`
- **Whitespace alternatives:** `%09 %0a %0c %0d %a0`, `+`, `/**/`, parentheses
- **Encoding:** URL-encode, **double-URL-encode**, unicode/overlong, hex, HTML entities
- **HTTP Parameter Pollution (HPP):** `?id=1&id=2`, split payload across duplicates
- **Null bytes / junk:** `%00`, padding, large bodies, chunked transfer-encoding
- **Header spoofing:** `X-Forwarded-For`, `X-Originating-IP`, `X-Real-IP`, `X-Client-IP`,
  `X-Forwarded-Host` set to `127.0.0.1` / trusted origin
- **Method override:** `X-HTTP-Method-Override`, switch GET↔POST, JSON vs form body
- **User-Agent rotation** (`--random-agent`), request pacing (avoid rate rules)

## 4. Vendor-specific priorities
| WAF | Prefer |
|---|---|
| **ModSecurity / OWASP-CRS** | inline comments `/**/`, versioned `/*!...*/`, keyword split, case, whitespace `%0a/%09`, encoding |
| **Cloudflare** | casing, unicode/URL/double-URL encoding, UA rotation, chunked bodies, **origin-IP discovery** (test the origin directly, bypassing CF) |
| **Imperva / Incapsula** | double-encoding, HPP, null bytes, header spoofing, cookie/JS-challenge handling |
| **F5 BIG-IP ASM** | HPP, mixed case, encoding, `X-Forwarded-*` spoofing, method override |
| **Akamai** | double-URL-encode, header spoofing, path/case tricks |
| **AWS WAF** | encoding, HPP, size/regex-evasion (split tokens), header injection |
| **Sucuri / Barracuda** | double-encoding, null bytes, UA rotation, header spoofing |

## 5. Origin-IP discovery (bypass the WAF entirely)
If the site is behind a reverse-proxy WAF (Cloudflare/Sucuri/Akamai), try to reach the origin
directly (historical DNS, subdomains, SPF/MX records, `Host`-header routing). Only if in scope.

## 6. Injection tools with evasion
```bash
# sqlmap with tamper chain + random UA — try combinations until the WAF is bypassed
dr sqlmap -u "$U/page?id=1" --batch --random-agent \
   --tamper=space2comment,between,randomcase,charencode
# escalate tampers: modsecurityversioned, versionedmorekeywords, apostrophemask, equaltolike ...
```

## 7. Record & feed forward
Note the WAF vendor + which evasion worked in `recon.md`. Re-use the working evasion for every
later injection payload. In the report, note the WAF and that its ruleset was **bypassed** for
the affected class (defence-in-depth failed — fix at the app layer).

## Adaptive
On 429/503/challenge floods → slow down, rotate UA, pace requests. Never brute the WAF into
blocking the whole engagement.
