---
name: network-utils
description: IPv4/IPv6 subnet calculation, URL parsing, MAC address format, HTTP status lookup, and user-agent parsing. Use when debugging networking config, request metadata, or address planning.
---

# Network Utilities

Network helpers for day-to-day debugging — show the math, not just the answer. For cron scheduling, see `cron-builder`.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Subnet planning | "How many hosts in 10.0.0.0/22?" |
| IP conversion | "Convert 192.168.1.1 to integer" |
| URL debugging | "Parse this URL into components" |
| HTTP errors | "What does 502 mean vs 503?" |
| MAC addresses | "Validate and format this MAC" |
| Request metadata | "Parse this User-Agent string" |

## Phase Checklist

```
[ ] 1. Identify tool (subnet, URL, HTTP, MAC, UA)
[ ] 2. Validate input format before calculation
[ ] 3. Show intermediate values (binary, masks, parsed components)
[ ] 4. Flag security concerns (credentials in URL, spoofed UA)
[ ] 5. Warn about large outputs (/16 IP lists)
[ ] 6. Present structured table output
```

---

## IPv4 Subnet Calculator

### Inputs

- CIDR notation: `10.0.0.0/24`
- IP + netmask: `192.168.1.100` + `255.255.255.0`
- IP + wildcard: `10.1.1.50` + `0.0.0.255`

### Python Implementation

```python
import ipaddress

def subnet_info(cidr: str) -> dict:
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = list(net.hosts())
    return {
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "netmask": str(net.netmask),
        "wildcard": str(net.hostmask),
        "prefix": net.prefixlen,
        "total_addresses": net.num_addresses,
        "usable_hosts": max(net.num_addresses - 2, 0) if net.prefixlen < 31 else net.num_addresses,
        "first_host": str(hosts[0]) if hosts else "N/A",
        "last_host": str(hosts[-1]) if hosts else "N/A",
        "binary_netmask": ".".join(format(int(o), "08b") for o in net.netmask.packed),
    }

info = subnet_info("10.0.0.0/24")
for k, v in info.items():
    print(f"{k:20} {v}")
```

### Output Fields

| Field | Example (/24) |
|-------|---------------|
| Network address | 10.0.0.0 |
| Broadcast | 10.0.0.255 |
| Netmask | 255.255.255.0 |
| Wildcard mask | 0.0.0.255 |
| Usable hosts | 254 |
| First host | 10.0.0.1 |
| Last host | 10.0.0.254 |

### CIDR Quick Reference

| Prefix | Hosts | Common use |
|--------|-------|------------|
| /32 | 1 | Single host |
| /30 | 2 | Point-to-point link |
| /24 | 254 | Small LAN |
| /16 | 65,534 | Large internal network |
| /8 | 16M+ | Class A (legacy) |

**Warning:** Do not list individual IPs for prefixes larger than /22 (>1024 addresses) without explicit user request.

---

## IPv4 Range / Converter

```python
import ipaddress

def ip_conversions(ip_str: str) -> dict:
    ip = ipaddress.ip_address(ip_str)
    as_int = int(ip)
    return {
        "dotted_decimal": str(ip),
        "integer": as_int,
        "hex": hex(as_int),
        "binary": ".".join(format(b, "08b") for b in ip.packed),
        "is_private": ip.is_private,
        "is_loopback": ip.is_loopback,
        "is_multicast": ip.is_multicast,
        "is_reserved": ip.is_reserved,
        "reverse_dns": ip.reverse_pointer,
    }

print(ip_conversions("192.168.1.1"))
# integer: 3232235777
```

```python
# Integer to IP
import ipaddress
ipaddress.ip_address(3232235777)  # 192.168.1.1

# Expand small CIDR to list
net = ipaddress.ip_network("10.0.0.0/30")
print([str(ip) for ip in net.hosts()])
# ['10.0.0.1', '10.0.0.2']
```

---

## IPv6

```python
import ipaddress
import secrets

def ipv6_info(cidr: str) -> dict:
    net = ipaddress.ip_network(cidr, strict=False)
    return {
        "network": str(net.network_address),
        "prefix": net.prefixlen,
        "num_addresses": net.num_addresses,
        "is_private": net.is_private,
        "compressed": net.network_address.compressed,
        "exploded": net.network_address.exploded,
    }

print(ipv6_info("2001:db8::/32"))
```

### IPv6 ULA Generator (RFC 4193)

```python
import secrets

def generate_ula_prefix() -> str:
    # fd + 40-bit global ID + /48
    global_id = secrets.randbits(40)
    return f"fd{global_id:010x}/48"

prefix = generate_ula_prefix()
print(f"ULA prefix: {prefix}")
print(f"Example subnet: {prefix.replace('/48', '')}:1000::/64")
print("Note: ULAs are not globally routable — internal use only")
```

---

## URL Parser

```python
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

def parse_url(url: str) -> dict:
    p = urlparse(url)
    query = parse_qs(p.query, keep_blank_values=True)
    # Flatten single-value lists
    query_flat = {k: v[0] if len(v) == 1 else v for k, v in query.items()}
    return {
        "scheme": p.scheme,
        "hostname": p.hostname,
        "port": p.port,
        "default_port": {"http": 80, "https": 443}.get(p.scheme),
        "path": p.path,
        "query": query_flat,
        "fragment": p.fragment,
        "username": p.username,
        "password": "***" if p.password else None,
        "netloc": p.netloc,
    }

url = "https://user:secret@api.example.com:8443/v1/users?page=2&limit=10#section"
parsed = parse_url(url)
for k, v in parsed.items():
    print(f"{k:15} {v}")
```

### URL Security Checks

| Check | Action |
|-------|--------|
| Credentials in URL | ⚠ Warn — secrets in logs/history |
| Non-default port | Note explicitly |
| Punycode domain | Show decoded + encoded forms |
| Missing scheme | Assume https? Ask user |
| Double-encoded path | See `encode-decode` |

### Rebuild Canonical URL

```python
def canonical_url(scheme: str, host: str, path: str, port: int = None) -> str:
    default_ports = {"http": 80, "https": 443}
    netloc = host if port in (None, default_ports.get(scheme)) else f"{host}:{port}"
    return urlunparse((scheme, netloc, path, "", "", ""))

print(canonical_url("https", "example.com", "/api/v1", 443))
# https://example.com/api/v1
```

---

## HTTP Status Codes

### Lookup Table

| Code | Name | Typical cause | Fix hint |
|------|------|---------------|----------|
| 200 | OK | Success | — |
| 201 | Created | Resource created | Check Location header |
| 204 | No Content | Success, empty body | Expected for DELETE |
| 301 | Moved Permanently | URL changed forever | Update links, use new URL |
| 302 | Found | Temporary redirect | May change — don't cache as permanent |
| 304 | Not Modified | Cache valid | Conditional request worked |
| 400 | Bad Request | Invalid syntax/params | Validate request body |
| 401 | Unauthorized | Missing/invalid auth | Add/fix Authorization header |
| 403 | Forbidden | Auth OK but no permission | Check roles/policies |
| 404 | Not Found | Resource missing | Verify path and method |
| 405 | Method Not Allowed | Wrong HTTP verb | Check Allow header |
| 408 | Request Timeout | Client too slow | Retry with backoff |
| 409 | Conflict | State conflict | Resolve duplicate/version |
| 422 | Unprocessable Entity | Validation failed | Fix semantic errors |
| 429 | Too Many Requests | Rate limited | Respect Retry-After |
| 500 | Internal Server Error | Server bug | Check server logs |
| 502 | Bad Gateway | Upstream unreachable | Check proxy/upstream health |
| 503 | Service Unavailable | Overloaded/maintenance | Retry later, check status page |
| 504 | Gateway Timeout | Upstream timeout | Increase timeout or fix upstream |

### 401 vs 403 Decision Tree

```
Authentication provided?
├── No  → 401 Unauthorized (authenticate first)
└── Yes → Authorized for this resource?
          ├── No  → 403 Forbidden
          └── Yes → 200/201/...
```

### 502 vs 503

| | 502 Bad Gateway | 503 Service Unavailable |
|--|-----------------|-------------------------|
| Meaning | Proxy got bad response | Service intentionally down or overloaded |
| Common cause | Upstream crash, wrong port | Maintenance mode, rate limit |
| Client action | Check upstream config | Retry with backoff |

---

## MAC Address

```python
import re
import secrets

def normalize_mac(mac: str) -> str:
    clean = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(clean) != 12:
        raise ValueError(f"Expected 12 hex digits, got {len(clean)}")
    pairs = [clean[i:i+2] for i in range(0, 12, 2)]
    return ":".join(pairs).upper()

def validate_mac(mac: str) -> dict:
    normalized = normalize_mac(mac)
    octets = normalized.split(":")
    first_byte = int(octets[0], 16)
    is_multicast = bool(first_byte & 0x01)
    is_local = bool(first_byte & 0x02)
    is_global = not is_local
    return {
        "normalized": normalized,
        "formats": {
            "colon": normalized,
            "dash": normalized.replace(":", "-"),
            "dot": ".".join("".join(octets[i:i+2]) for i in range(0, 6, 2)),
            "plain": normalized.replace(":", ""),
        },
        "is_multicast": is_multicast,
        "is_local_administered": is_local,
        "is_global_unicast": is_global and not is_multicast,
        "oui": normalized[:8],
    }

print(validate_mac("aa-bb-cc-dd-ee-ff"))
```

### Generate Random Locally-Administered MAC

```python
def random_mac() -> str:
    # Set local bit (bit 1 of first octet), clear multicast bit (bit 0)
    first = secrets.randbelow(256) & 0xFE | 0x02
    rest = [secrets.randbelow(256) for _ in range(5)]
    octets = [first] + rest
    return ":".join(f"{b:02X}" for b in octets)

print(random_mac())  # e.g. 02:A3:F1:8B:22:C0
```

OUI lookup (vendor identification) requires external database — note vendor if known, otherwise report OUI prefix only.

---

## User-Agent Parsing

```python
import re

def parse_user_agent(ua: str) -> dict:
    result = {"raw": ua, "browser": "Unknown", "os": "Unknown", "device": "Desktop"}

    # Browser detection (simplified — not exhaustive)
    browsers = [
        (r"Edg/([\d.]+)", "Edge"),
        (r"Chrome/([\d.]+)", "Chrome"),
        (r"Firefox/([\d.]+)", "Firefox"),
        (r"Safari/([\d.]+)", "Safari"),
        (r"MSIE (\d+)", "Internet Explorer"),
    ]
    for pattern, name in browsers:
        m = re.search(pattern, ua)
        if m:
            result["browser"] = f"{name} {m.group(1)}"
            break

    # OS detection
    os_patterns = [
        (r"Windows NT 10", "Windows 10/11"),
        (r"Mac OS X ([\d_]+)", "macOS"),
        (r"Android ([\d.]+)", "Android"),
        (r"iPhone OS ([\d_]+)", "iOS"),
        (r"Linux", "Linux"),
    ]
    for pattern, name in os_patterns:
        m = re.search(pattern, ua)
        if m:
            result["os"] = name + (f" {m.group(1).replace('_', '.')}" if m.lastindex else "")
            break

    # Device type
    if re.search(r"Mobile|Android|iPhone|iPad", ua):
        result["device"] = "Mobile" if "iPad" not in ua else "Tablet"

    return result

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
print(parse_user_agent(ua))
```

**Disclaimer:** User-Agent strings are easily spoofed. Do not use for security decisions. For bot detection or auth, use proper server-side mechanisms.

---

## Worked Examples

### Example 1: Docker network sizing

```
Requirement: 300 containers per subnet
/24 = 254 usable → too small
/23 = 510 usable → sufficient
Recommendation: 172.20.0.0/23
```

### Example 2: URL with embedded credentials

```
URL: https://admin:password@internal.service:8080/health
⚠ Credentials exposed in URL
Action: Use Authorization header instead
See: hash-crypto for token-based auth
```

### Example 3: Cloudflare 502 investigation

```
Status: 502 Bad Gateway
Meaning: Edge proxy couldn't reach origin
Check: Origin server running, firewall, SSL mode, origin port
Not: 503 (which means origin refused/overloaded intentionally)
```

---

## Output Template

```markdown
## {tool}: {input}

| Field | Value |
|-------|-------|
| Network | 10.0.0.0/24 |
| Netmask | 255.255.255.0 |
| Usable hosts | 254 |
| First host | 10.0.0.1 |
| Last host | 10.0.0.254 |
| Broadcast | 10.0.0.255 |

### Notes
- /31 networks have no broadcast (RFC 3021)
- Private range: yes (RFC 1918)
```

---

## Anti-Patterns

- Listing entire /16 as individual IPs
- Trusting X-Forwarded-For without context in security reviews
- Assuming User-Agent for authentication or authorization
- Ignoring credentials in URLs during log review
- Using deprecated IP classes (A/B/C) instead of CIDR
- Mixing up 401 and 403 when debugging auth flows

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| URL encoding/decoding | `encode-decode` |
| Cron in deployment schedules | `cron-builder` |
| JWT in Authorization header | `hash-crypto` |
| Generate API tokens | `token-generator` |
| QR code for WiFi network | `qr-generator` |
| Deploy-time networking | `k8s-review` / `docker-audit` (devops plugin) |
