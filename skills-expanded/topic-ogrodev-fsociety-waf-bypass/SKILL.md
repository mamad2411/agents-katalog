---
name: waf-bypass
description: |
  This skill should be used when the user mentions "WAF", "web application firewall", "WAF bypass",
  "WAF evasion", "WAF detection", "WAF fingerprint", "wafw00f", "firewall bypass", "firewall evasion",
  "request filtering", "request blocked", "payload blocked", "blocked by WAF", "403 forbidden",
  "406 not acceptable", "429 too many requests", "rate limit", "rate limiting", "IP ban", "IP block",
  "IP reputation", "IP blacklist", "CDN bypass", "origin IP", "origin discovery",
  "Cloudflare", "Cloudflare bypass", "CF bypass", "Cloudflare WAF",
  "AWS WAF", "AWS Shield", "AWS managed rules",
  "Akamai", "Akamai Kona", "Akamai WAF",
  "Imperva", "Incapsula", "Imperva WAF",
  "ModSecurity", "OWASP CRS", "Core Rule Set", "ModSec", "paranoia level",
  "Sucuri", "Sucuri WAF", "F5 BIG-IP", "F5 ASM", "Barracuda WAF",
  "Fortinet FortiWeb", "FortiWeb", "Citrix WAF", "Azure WAF", "Azure Front Door",
  "payload encoding", "double encoding", "URL encoding bypass", "Unicode normalization",
  "Unicode bypass", "null byte injection", "comment injection", "obfuscation",
  "mixed encoding", "hex encoding", "HTML entity encoding", "overlong UTF-8",
  "HTTP verb tampering", "method tampering", "HTTP/2 smuggling", "request smuggling",
  "chunked transfer", "chunked encoding", "content-type switching", "multipart abuse",
  "multipart boundary", "transfer-encoding", "HTTP parameter pollution", "HPP",
  "tamper script", "sqlmap tamper", "WAF rule bypass", "WAF rule evasion",
  "managed rules bypass", "custom rules bypass", "regex bypass", "regex evasion",
  "WAF fingerprinting", "WAF identification", "WAF detection technique",
  "nmap http-waf-detect", "nmap http-waf-fingerprint", "WAF error page",
  "WAF signature", "WAF response analysis", "security header analysis",
  "X-Forwarded-For bypass", "header injection bypass", "path normalization",
  "path confusion", "path traversal bypass", "directory traversal bypass".
version: 2.0.0
---

# WAF Bypass

Web Application Firewalls inspect HTTP traffic and block requests matching known attack signatures. Every commercial WAF has implementation gaps — regex engine limits, encoding blind spots, protocol handling quirks, and normalization inconsistencies. Exploiting these gaps requires methodical identification of the WAF technology, understanding its rule engine, and crafting payloads that bypass detection without altering exploit semantics.

WAFs log aggressively. Every blocked request is recorded with your source IP, the matched rule ID, and the full request. Careless testing burns your IP, triggers escalating defenses (CAPTCHA, tarpit, permanent block), and alerts blue teams. Approach WAF bypass as a precision operation.

## Triage Workflow

Follow this sequence. Each phase builds on the previous one.

### Phase 1 — WAF Detection and Fingerprinting

Identify whether a WAF exists and which product it is. Do not skip this — blind bypass attempts waste time and generate noise.

Load: `ToolSearch` → `select:mcp__hexstrike-ai__wafw00f_scan`

```bash
# Primary detection — wafw00f identifies 150+ WAFs
wafw00f https://target.com

# Verbose mode reveals detection method
wafw00f https://target.com -v

# Scan all URLs in scope
wafw00f -i urls.txt -o waf-results.json
```

```bash
# Secondary — nmap NSE scripts
nmap -p 443 --script http-waf-detect target.com
nmap -p 443 --script http-waf-fingerprint target.com
```

Manual fingerprinting when tools are inconclusive:
- Send a benign request, note response headers (Server, X-Powered-By, Via, X-CDN)
- Send a clearly malicious request (`?id=1' OR 1=1--`), note the block response
- Compare block page HTML, status code, and headers against known WAF signatures
- Check `Set-Cookie` names — Cloudflare uses `__cf_bm`, Incapsula uses `visid_incap_*`, AWS WAF returns `awsalb`

Log the WAF identification immediately:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add target.com defense waf-type "Cloudflare Business" --source wafw00f
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add wafw00f target.com "waf-fingerprint" success --notes "Identified Cloudflare Business plan WAF"
```

See `references/waf-fingerprinting.md` for the complete fingerprinting reference.

### Phase 2 — Origin IP Discovery (CDN Bypass)

If the target sits behind a CDN-based WAF (Cloudflare, Akamai, Incapsula, AWS CloudFront), finding the origin server IP bypasses the WAF entirely. This is the highest-value bypass — all WAF protections are eliminated.

**Historical DNS records** — check for A records that predate CDN adoption:
- SecurityTrails API, ViewDNS.info, DNS Dumpster, Wayback Machine DNS
- `subfinder_scan` + `httpx_probe` to find subdomains resolving to non-CDN IPs
- Mail servers (MX records), FTP servers, staging/dev subdomains often bypass CDN

**Certificate transparency** — search CT logs for certificates issued to the domain. Origin hosting providers issue certificates that reveal server IPs when cross-referenced with Censys/Shodan.

**Email header analysis** — trigger outbound emails (password reset, signup confirmation). `Received:` and `X-Originating-IP` headers reveal origin server IPs.

**Censys/Shodan** — search for the same SSL certificate SHA256, HTTP title, or favicon hash on non-CDN IP ranges.

**Once the origin IP is found**:
```bash
# Bypass CDN entirely — direct origin access
curl -H "Host: target.com" https://ORIGIN_IP/ --resolve target.com:443:ORIGIN_IP

# Or add to /etc/hosts for all tools
echo "ORIGIN_IP target.com" >> /etc/hosts
```

Log the origin IP discovery:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add target.com network origin-ip "203.0.113.42" --source "cert-transparency"
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add target.com config "cdn-bypass" MEDIUM "Origin IP exposed — WAF completely bypassed via direct access"
```

See `references/cloudflare-bypass.md` for Cloudflare-specific origin discovery.

### Phase 3 — WAF Rule Analysis

Before crafting bypass payloads, understand what the WAF blocks and what it allows. Map the rule surface:

1. **Baseline**: Send normal requests and record responses (status, headers, body length, response time)
2. **Trigger known signatures**: Send common attack strings one at a time — `<script>`, `' OR 1=1--`, `{{7*7}}`, `../../../etc/passwd`, `; ls`
3. **Record block behavior**: Note status codes (403, 406, 429, 503), block page content, response headers, and response time per blocked pattern
4. **Test encoding**: Repeat blocked payloads with URL encoding, double encoding, Unicode, case variation
5. **Identify rule granularity**: Determine if the WAF blocks on keywords, regex patterns, or semantic analysis

```bash
# Use httpx to probe with various payloads and record status codes
# Log each bypass attempt
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add "manual" target.com "waf-rule-probe" partial --notes "403 on <script>, 200 on <ScRiPt>"
```

Load: `ToolSearch` → `select:mcp__hexstrike-ai__http_repeater`

Use `http_repeater` to replay requests with modified payloads systematically. Use `http_intruder` to fuzz with encoding variations.

### Phase 4 — Bypass Technique Selection

Select bypass strategy based on WAF type. Each WAF has known weaknesses.

#### Decision Tree

| WAF | Primary Strategy | Reference |
|-----|-----------------|-----------|
| **Cloudflare** | Origin IP discovery, chunked encoding, Unicode normalization, HTTP/2 | `references/cloudflare-bypass.md` |
| **AWS WAF** | Regex engine limits, managed rule gaps, content-type switching | `references/aws-waf-bypass.md` |
| **ModSecurity + CRS** | Paranoia level targeting, comment injection, HPP, CRS version-specific bypasses | `references/modsecurity-bypass.md` |
| **Akamai** | Payload fragmentation, slow requests, encoding chains | `references/encoding-evasion.md` |
| **Imperva/Incapsula** | Protocol-level tricks, multipart abuse, header manipulation | `references/protocol-level-bypass.md` |
| **F5 BIG-IP ASM** | Parameter pollution, content-type abuse, verb tampering | `references/protocol-level-bypass.md` |
| **Sucuri** | Path-based bypasses, REST route alternatives, alternate HTTP methods | `references/encoding-evasion.md` |
| **Generic/Unknown** | Start with encoding evasion, escalate to protocol-level | `references/encoding-evasion.md` |

### Phase 5 — Payload Crafting

Load: `ToolSearch` → `select:mcp__hexstrike-ai__advanced_payload_generation`

Generate WAF-evasion payloads with context about the specific WAF:
- `advanced_payload_generation` — specify WAF type, blocked signatures, and allowed encodings
- `ai_generate_payload` — context-aware generation for specific vulnerability + WAF combination

For SQLi with WAF evasion, use sqlmap tamper scripts:
```bash
# Common tamper script chains by WAF
# Cloudflare:
sqlmap -u "URL" --tamper=between,randomcase,space2comment,charencode

# ModSecurity CRS:
sqlmap -u "URL" --tamper=space2comment,between,randomcase,equaltolike

# AWS WAF:
sqlmap -u "URL" --tamper=charunicodeencode,space2mssqlblank,between

# Generic:
sqlmap -u "URL" --tamper=apostrophemask,randomcase,space2comment,charencode,percentage
```

Use `http_set_rules` to apply automatic evasion headers to all subsequent requests:
```
Load: ToolSearch → select:mcp__hexstrike-ai__http_set_rules

Apply rules:
- X-Forwarded-For: 127.0.0.1
- X-Originating-IP: 127.0.0.1
- X-Real-IP: 127.0.0.1
- X-Remote-Addr: 127.0.0.1
- User-Agent: Mozilla/5.0 (legitimate browser UA)
```

See `references/encoding-evasion.md` for the complete encoding technique reference.
See `references/protocol-level-bypass.md` for HTTP-layer bypass techniques.

### Phase 6 — Validation and Confirmation

A bypass is only valid when the payload reaches the application and produces the intended effect:

1. Confirm the payload was not modified/sanitized by the WAF (check response for reflected payload)
2. Confirm the exploit logic executed (verify SQLi data extraction, XSS DOM change, RCE output)
3. Test the bypass multiple times — some WAFs learn and adapt (ML-based rules)
4. Record the working bypass technique and the exact payload

```bash
# Log successful bypass
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add "manual" target.com "waf-bypass-cloudflare-chunked" success \
  --notes "Cloudflare managed rules bypassed via chunked transfer encoding with double URL-encoded payload"

# Log the finding
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add target.com config "waf-bypass" HIGH \
  "WAF bypass via chunked encoding — Cloudflare managed rules ineffective against split payloads"
```

## OPSEC Considerations

WAF bypass is the noisiest phase of a web engagement. Every blocked request is logged with full request details.

| Concern | Mitigation |
|---------|------------|
| **IP reputation** | Use VPN/proxy rotation. Burned IPs get escalating blocks (CAPTCHA → tarpit → permanent ban) |
| **Rate limiting** | Space requests 2-5s apart minimum. Burst scanning triggers instant blocks |
| **Signature accumulation** | WAFs correlate multiple blocked requests from the same source. 10+ blocks may trigger permanent IP ban |
| **Adaptive rules** | ML-based WAFs (Cloudflare Bot Management, AWS WAF Bot Control) learn from bypass attempts |
| **Alert fatigue vs. stealth** | One or two blocks are noise. A flood of blocks triggers SOC investigation |
| **Log retention** | WAF logs persist 30-90 days typically. All bypass attempts are recorded even if successful |
| **Request fingerprinting** | WAFs fingerprint TLS (JA3), HTTP/2 settings, header order. Tools have distinct signatures |

Scan profile guidance:
- **loud** — full-speed scanning, no evasion delays. Lab/CTF only
- **normal** — 2-3s delays between probes, basic header rotation
- **stealth** — 5-10s delays, realistic browser TLS fingerprint, header randomization
- **paranoid** — proxy rotation per request, 10-30s delays, browser-mimicking TLS

## Report Template

```
## WAF Bypass Assessment: <target>

### WAF Identification
- Product: <WAF name and version/plan>
- Detection method: <wafw00f / manual / headers>
- Block behavior: <status code, block page, headers>

### Origin Discovery
- Origin IP: <IP or "not found">
- Discovery method: <technique>
- Direct access: <confirmed/denied>

### Bypass Techniques Attempted
| Technique | Payload | Result | Notes |
|-----------|---------|--------|-------|
| <technique> | <payload summary> | success/blocked | <details> |

### Working Bypasses
1. <bypass description with exact payload>
2. <bypass description with exact payload>

### OPSEC Impact
- Blocked requests generated: <count>
- IP status: <clean/flagged/banned>
- Estimated detection risk: <LOW/MEDIUM/HIGH>

### Recommendations
- <remediation advice for the client>
```

## Tool Reference

| Tool | Install | Best For |
|------|---------|----------|
| `wafw00f` | `pip install wafw00f` | WAF identification (150+ WAFs) |
| `sqlmap` tamper scripts | included with sqlmap | Automated SQLi WAF evasion |
| `nuclei` | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` | WAF detection templates, bulk testing |
| `nmap` NSE | included with nmap | `http-waf-detect`, `http-waf-fingerprint` |
| `CloudFail` | `pip install cloudfail` | Cloudflare origin IP discovery |
| `CloudFlair` | `github.com/christophetd/CloudFlair` | Censys-based Cloudflare bypass |
| `bypass-firewalls-by-DNS-history` | `github.com/vincentcox/bypass-firewalls-by-DNS-history` | Historical DNS origin discovery |
| `CrimeFlare` | `github.com/HolyBugx/CrimeFlare` | Cloudflare origin IP database |
| `httpx` | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` | Response comparison, header analysis |
| `subfinder` | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` | Subdomain enumeration for origin discovery |

## References

| Reference | Coverage |
|-----------|----------|
| `references/waf-fingerprinting.md` | wafw00f, nmap NSE, manual fingerprinting, WAF-specific headers, error pages, response analysis |
| `references/cloudflare-bypass.md` | Origin IP discovery, Cloudflare-specific bypass techniques, managed vs custom rules, rate limit evasion |
| `references/encoding-evasion.md` | URL encoding, double encoding, Unicode normalization, HTML entities, hex encoding, null bytes, comment injection, mixed encoding chains |
| `references/protocol-level-bypass.md` | HTTP verb tampering, HTTP/2 smuggling, chunked transfer, content-type switching, multipart boundary abuse, parameter pollution |
| `references/aws-waf-bypass.md` | AWS WAF rule groups, managed rules bypass, regex engine limits, rate-based rule evasion, CloudFront integration |
| `references/modsecurity-bypass.md` | ModSecurity CRS rules, paranoia levels, rule ID targeting, version-specific bypasses, SecRule analysis |
