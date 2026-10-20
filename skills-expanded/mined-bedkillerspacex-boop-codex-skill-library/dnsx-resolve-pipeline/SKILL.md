---
name: dnsx-resolve-pipeline
description: >
  Build owned/authorized DNS resolution pipelines with ProjectDiscovery dnsx: bulk resolve,
  record types, rate limits, retries, JSON output, and chaining with subdomain lists for recon
  or inventory. Use when dnsx, bulk DNS resolve, dnsx pipeline, A/AAAA/CNAME/NS enumeration
  for assets you own or have written authorization to map — not for unsolicited scanning of
  third-party infrastructure.
---

# dnsx Resolve Pipeline

## Scope And Authorization

- **In scope:** Domains and IP ranges you own, labs/CTFs, or engagements with written authorization.
- **Out of scope:** Mass scanning unrelated internet domains; using results to attack systems.
- Prefer rate limits and provider-friendly resolvers you are allowed to use.
- Redact customer hostnames in public samples; keep raw outputs access-controlled.
- Pair with `recon-and-methodology`, `dns-latency-triage`, and `code-quality-standards` for scripts.

## When To Use

- Resolving large wordlists/subdomain lists for **authorized** asset inventory.
- Validating which names return A/AAAA/CNAME/NS/TXT quickly.
- Building CI to detect unexpected public DNS for internal brands (owned monitoring).
- Filtering live hosts before port scanning **in scope**.
- Normalizing DNS output to JSON for pipelines.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Engagement planning / RoE | `recon-and-methodology` |
| DNS latency root cause | `dns-latency-triage` |
| DNSSEC operations | `dnssec-deployment-basics` |
| Email auth records content | `dmarc-spf-dkim-hardening` |
| HTTP probing | httpx-oriented skills if present |
| Code quality baseline | `code-quality-standards` |

## Tool role

**dnsx** (ProjectDiscovery) is a fast multi-purpose DNS toolkit: resolve, wildcard filter helpers, record type queries, JSON lines output—designed for bulk workflows.

```bash
# Install (owned workstation; pin versions in CI)
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
# or release binaries per org policy
dnsx -version
```

## Workflow

### 1. Confirm scope and success criteria

1. In-scope root domains; max QPS; output retention.
2. Success: resolved inventory file with types needed; wildcards handled; no out-of-scope queries.
3. Written authorization path for non-owned targets.

### 2. Prepare inputs

```bash
# hosts.txt — one name per line (authorized list only)
# example.com
# api.example.com
```

1. Generate candidates from owned CMDB, certificate transparency **for your domains**, or approved wordlists.
2. Deduplicate; lowercase; strip schemes.

### 3. Basic resolve pipeline

```bash
# A records, silent, rate-limited
dnsx -l hosts.txt -a -resp -rate-limit 100 -o resolved-a.txt

# Multiple types
dnsx -l hosts.txt -a -aaaa -cname -resp -json -o resolved.jsonl

# Custom resolvers file (org recursive)
dnsx -l hosts.txt -a -r resolvers.txt -retry 2
```

1. Prefer org resolvers when querying internal zones.
2. Respect `-rate-limit` to avoid abusing shared infra.

### 4. Wildcard and noise handling

1. Detect wildcard DNS (random subdomain resolves)—filter before treating all as real assets.
2. dnsx/httpx ecosystem often pairs with wildcard detection scripts; document method used.
3. Note CDN multi-A responses as normal.

### 5. Chain for authorized recon

```bash
# Conceptual pipeline (all in-scope)
# subdomains → dnsx → live IPs → (authorized) httpx/naabu
cat subs.txt | dnsx -silent -a -resp-only | sort -u > ips.txt
```

1. Gate each stage on scope files.
2. Do not auto-scan IPs outside agreed ranges (shared hosting!).

### 6. CI / continuous inventory (owned brands)

```yaml
# Scheduled job sketch
# - build domain list from inventory
# - dnsx resolve
# - diff against previous; alert on unexpected public records
```

1. Alert on new public A records for sensitive names.
2. Store outputs in restricted bucket; retention policy.

### 7. Verify and hand off

1. Spot-check with `dig` for sample of results.
2. Document resolvers, flags, QPS, and scope file location.
3. Sanitize dashboards; apply `code-quality-standards` to wrappers.

## Command cheat sheet

| Goal | Flags (illustrative) |
| --- | --- |
| Exists? | `dnsx -l list -silent` |
| Answers | `-resp` / `-resp-only` |
| Types | `-a -aaaa -cname -ns -txt -mx` |
| JSON | `-json` |
| Rate | `-rate-limit N` |
| Resolvers | `-r file` or `-resolver` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Owned/authorized list | Top 1M domains unsolicited |
| Rate | Limited QPS | Max blast on public resolvers |
| Output | Restricted storage | Paste full corp DNS to Slack |
| Wildcards | Filtered | 50k false “assets” |
| Chain | Scope at each hop | Resolve → scan entire cloud ASN |
| CI | Diff expected inventory | Silent unlimited wordlist |

## Output Checklist

- [ ] Authorization and domain list documented
- [ ] Input sanitized and deduped
- [ ] dnsx run with rate limits and resolver choice
- [ ] Required record types collected
- [ ] Wildcards handled
- [ ] Outputs stored securely
- [ ] Spot-check with dig
- [ ] Pipeline scope gates verified
- [ ] Alerts for inventory drift if continuous
- [ ] Residual risk / false positives noted

## Rules

- Authorized DNS recon only.
- Rate-limit and use appropriate resolvers.
- DNS presence ≠ permission to exploit.
- Keep pipelines evidence-friendly and redaction-aware.
- Focus on dnsx bulk resolve workflows.
