---
name: dns-over-https-basics
description: >
  Deploy and troubleshoot DNS over HTTPS (DoH) / DNS over TLS (DoT): resolver choice,
  enterprise split-DNS impact, privacy tradeoffs, and detection notes. Use when enabling
  DoH clients/resolvers on owned networks or apps — not for covertly bypassing corporate
  controls you are not authorized to change.
---

# DNS over HTTPS Basics

## Scope And Authorization

- **In scope:** Clients, resolvers, and networks you administer; privacy design for your users.
- **Out of scope:** Helping users evade lawful monitoring on networks you do not control without authorization; attacking public DoH providers.
- Prefer enterprise-managed DoH endpoints when split-DNS and security filtering are required.
- Redact client IPs and query names from shared logs per policy.
- Pair with `dns-latency-triage`, enterprise proxy skills, and `code-quality-standards` for app DoH clients.

## When To Use

- Enabling DoH/DoT on browsers, OS, or mobile MDM.
- Running a corporate DoH/DoT resolver (dnsdist, Unbound, cloud gateway).
- Debugging apps that hardcode public DoH and break internal names.
- Privacy review: who sees query streams (ISP vs DoH provider vs enterprise).
- Migrating from cleartext :53 on untrusted networks.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General DNS latency | `dns-latency-triage` |
| DNSSEC validation ops | `dnssec-deployment-basics` |
| DNS rebinding app defense | `dns-rebinding-defense-design` |
| TLS cert ops for DoH endpoint | TLS/cert skills |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Protocol | Port / transport | Notes |
| --- | --- | --- |
| Do53 | UDP/TCP 53 | Cleartext queries on path |
| DoT | TCP 853 TLS | Often easier to allow/block as DNS |
| DoH | HTTPS 443 | Blends with web; RFC 8484 |
| DoQ | QUIC | Emerging |

**Privacy tradeoff:** DoH encrypts on-path to resolver; the **resolver operator** still sees queries. Browser “secure DNS” to a third party may bypass enterprise resolvers and split-horizon.

## Workflow

### 1. Confirm scope and success criteria

1. Goals: privacy on untrusted Wi-Fi, enterprise policy enforcement, or both.
2. Success: clients resolve internal + public names correctly; filtering/logging policy met; latency acceptable.
3. Decide managed DoH vs public provider vs opportunistic.

### 2. Inventory current resolution

```bash
# Client view
cat /etc/resolv.conf
# systemd-resolved
resolvectl status
# Windows
Get-DnsClientServerAddress
# Browser: check Secure DNS settings (UI)
```

1. Map split-DNS zones (corp internal).
2. Find apps with hardcoded DoH URLs.

### 3. Choose architecture

| Model | Pros | Cons |
| --- | --- | --- |
| Public DoH (Cloudflare/Google/…) | Easy privacy vs local ISP | Bypasses corp DNS; third party sees queries |
| Enterprise DoH/DoT | Keep split-DNS + DLP/filter | Must operate endpoint + certs |
| DoT to corp | Clear port 853 policy | Some networks block 853 |
| Mixed | Laptops remote vs office | Complexity |

1. For enterprises: publish **own** DoH URI template and push via MDM/GPO/Firefox enterprise policies.
2. Disable user-selectable public DoH if policy requires inspection—**only on managed devices you own**.

### 4. Stand up or configure resolver (owned)

```text
# Conceptual dnsdist / nginx / cloud DoH gateway
# - TLS cert for doh.example.com
# - Backend recursive (Unbound) with corp forward zones
# - Auth optional (mTLS or IP allowlist for employees)
# - Logging/retention per privacy policy
```

```bash
# Smoke: DoH POST/GET (owned endpoint)
curl -sH 'accept: application/dns-message' \
  'https://doh.example.com/dns-query?dns=...' | xxd | head
# Or use kdig/dog/drill with DoT/DoH flags if installed
```

1. Forward internal zones to AD/internal auth DNS.
2. Enable DNSSEC validation policy as org requires.
3. Rate-limit and authenticate to reduce abuse.

### 5. Client rollout

1. **Firefox/Chrome/Edge** enterprise policy for URI template.
2. **Windows 11** DoH templates / policy.
3. **systemd-resolved** `DNSOverTLS=yes` or DoH packages per distro.
4. **Mobile** MDM private DNS (Android) / configuration profiles.
5. Test: internal hostname resolves only when enterprise path used.

### 6. Troubleshoot

| Issue | Check |
| --- | --- |
| Internal NXDOMAIN | Client using public DoH |
| High latency | `dns-latency-triage`; DoH HTTP path; HTTP/2 |
| Intermittent fail | Middlebox MITM; cert pin; captive portal |
| Double encrypt | Proxy + DoH interactions |
| App break | Hardcoded 1.1.1.1 DoH |

### 7. Privacy, detection, hand off

1. Document who can see queries and retention.
2. Network detection of DoH (for **your** SOC on **your** network) is imperfect on 443—prefer managed devices policy over brittle DPI alone.
3. Metrics: DoH success rate, latency, fallback to Do53.
4. Runbooks for cert expiry on DoH endpoint.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Enterprise | Managed DoH + split DNS | Force public DoH on corp laptops only |
| Privacy claim | Encrypted to resolver | “Nobody can see DNS ever” |
| Rollout | MDM policy + test hosts | Random browser toggles |
| Security filter | Same policy as Do53 recursive | Lose all filtering unintentionally |
| Ops | Cert monitoring | Forgotten DoH gateway cert |
| Scope | Owned nets | Teaching evasion of others’ networks |

## Output Checklist

- [ ] Goals (privacy vs control) explicit
- [ ] Split-DNS requirements mapped
- [ ] Architecture chosen (public vs enterprise)
- [ ] Resolver TLS and backend forward zones verified
- [ ] Client policy deployed on managed fleet sample
- [ ] Internal + public resolve tests pass
- [ ] Latency acceptable
- [ ] Logging/retention policy documented
- [ ] App hardcoded DoH inventory ticketed
- [ ] Owners and cert expiry alerts set

## Rules

- Encrypting DNS is good; bypassing required security controls on managed fleets needs governance.
- Resolver trust is central—choose operators deliberately.
- DoH is not anonymity.
- Authorized networks and devices only.
- Topic is DoH/DoT deployment and tradeoffs, not DNS rebinding exploits.
