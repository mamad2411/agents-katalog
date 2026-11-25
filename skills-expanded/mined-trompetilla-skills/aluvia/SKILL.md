---
name: aluvia
description: Proxy any HTTP request or browser session through Aluvia's premium mobile IPs. Use when websites return 403s, CAPTCHAs, or rate limits. Zero dependencies — works immediately with curl, Python, or any browser.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ALUVIA_API_KEY"] },
        "primaryEnv": "ALUVIA_API_KEY",
        "emoji": "🌐",
      },
  }
---

# Aluvia — Mobile IP Proxy

Aluvia gives you trusted mobile IP addresses from real US carrier networks. Websites see a legitimate mobile user, not a datacenter bot. Use it to bypass 403 blocks, CAPTCHAs, and rate limits.

API base: `https://api.aluvia.io/v1`
All requests require: `Authorization: Bearer $ALUVIA_API_KEY`

## When to Use

- A website returns **403 Forbidden**, **429 Too Many Requests**, or a CAPTCHA challenge
- You need to scrape or browse a site that blocks datacenter/cloud IPs
- You need a **stable IP** across multiple requests (sticky sessions)
- You need an IP from a **specific US state** (geo-targeting)

Do NOT proxy traffic that works fine without it — direct connections are faster and free.

## Quick Start

Get a proxy URL in one step:

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({"description": "openclaw", "rules": ["*"]}).encode()
req = urllib.request.Request("https://api.aluvia.io/v1/account/connections", data=data, method="POST")
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
req.add_header("Content-Type", "application/json")
result = json.load(urllib.request.urlopen(req))
conn = result["data"]
print(json.dumps({
    "connection_id": conn["connection_id"],
    "proxy_url": conn["proxy_urls"]["url"],
    "username": conn["proxy_username"],
    "password": conn["proxy_password"],
    "server": f"{conn['proxy_urls']['raw']['protocol']}://{conn['proxy_urls']['raw']['host']}:{conn['proxy_urls']['raw']['port']}"
}, indent=2))
EOF
```

Response:

```json
{
  "connection_id": 1328,
  "proxy_url": "http://BeKprkcj:cyLTNMaJ@gateway.aluvia.io:8080",
  "username": "BeKprkcj",
  "password": "cyLTNMaJ",
  "server": "http://gateway.aluvia.io:8080"
}
```

**Save the `connection_id` and `proxy_url` — reuse them for all subsequent requests.** Only create a new connection if you need separate credentials or independent session/geo settings.

## Proxy HTTP Requests

### curl

```bash
curl -x "$PROXY_URL" https://httpbin.org/ip
```

Or with explicit auth:

```bash
curl --proxy "http://gateway.aluvia.io:8080" \
     --proxy-user "USERNAME:PASSWORD" \
     https://httpbin.org/ip
```

### Python (stdlib)

```bash
python <<'EOF'
import urllib.request, json

proxy_url = "http://USERNAME:PASSWORD@gateway.aluvia.io:8080"
proxy_handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
opener = urllib.request.build_opener(proxy_handler)

response = opener.open("https://httpbin.org/ip")
print(json.loads(response.read().decode()))
EOF
```

### Python (requests)

```python
import requests

proxies = {"http": proxy_url, "https": proxy_url}
response = requests.get("https://httpbin.org/ip", proxies=proxies)
print(response.json())
```

## Proxy Browser Traffic

When you need full browser navigation through Aluvia (not just HTTP requests), launch a browser with proxy settings.

### Playwright

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch(proxy={
        "server": "http://gateway.aluvia.io:8080",
        "username": "USERNAME",
        "password": "PASSWORD"
    })
    page = await browser.new_page()
    await page.goto("https://example.com")
    content = await page.content()
    await browser.close()
```

### Any Chromium Browser (CLI)

For headless Chromium without Playwright, set the proxy and handle auth via environment:

```bash
chromium --proxy-server="http://gateway.aluvia.io:8080" --headless https://example.com
```

Note: CLI-launched Chromium doesn't handle proxy auth automatically. Use Playwright for authenticated proxy access, or use curl/Python for HTTP-only tasks.

## List Existing Connections

Before creating a new connection, check if one already exists:

```bash
python <<'EOF'
import urllib.request, os, json

req = urllib.request.Request("https://api.aluvia.io/v1/account/connections")
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
result = json.load(urllib.request.urlopen(req))
for conn in result["data"]:
    print(json.dumps({
        "connection_id": conn["connection_id"],
        "proxy_url": conn["proxy_urls"]["url"],
        "rules": conn.get("rules", []),
        "session_id": conn.get("session_id"),
        "target_geo": conn.get("target_geo")
    }, indent=2))
EOF
```

## Update Routing Rules

Rules control what the Aluvia gateway proxies. Update rules on an existing connection:

```bash
python <<'EOF'
import urllib.request, os, json

connection_id = CONNECTION_ID  # integer
data = json.dumps({"rules": ["example.com", "*.blocked-site.com"]}).encode()
req = urllib.request.Request(
    f"https://api.aluvia.io/v1/account/connections/{connection_id}",
    data=data, method="PATCH"
)
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
req.add_header("Content-Type", "application/json")
result = json.load(urllib.request.urlopen(req))
print(json.dumps({"rules": result["data"]["rules"]}, indent=2))
EOF
```

### Rule Patterns

| Pattern         | Matches                                         |
| --------------- | ----------------------------------------------- |
| `*`             | All hostnames (proxy everything)                |
| `example.com`   | Exact match                                     |
| `*.example.com` | All subdomains of example.com                   |
| `google.*`      | google.com, google.co.uk, etc.                  |
| `-example.com`  | Exclude (use with `*` to proxy all except this) |

Examples:

- `["*"]` — proxy all traffic
- `["target-site.com"]` — proxy only target-site.com
- `["*", "-safe-site.com"]` — proxy everything except safe-site.com

## Set Session ID (Sticky IPs)

Requests with the same session ID use the same mobile IP. Use this when a site requires consistent identity across requests.

```bash
python <<'EOF'
import urllib.request, os, json

connection_id = CONNECTION_ID
data = json.dumps({"session_id": "my-session-1"}).encode()
req = urllib.request.Request(
    f"https://api.aluvia.io/v1/account/connections/{connection_id}",
    data=data, method="PATCH"
)
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
req.add_header("Content-Type", "application/json")
result = json.load(urllib.request.urlopen(req))
print(json.dumps({"session_id": result["data"]["session_id"]}, indent=2))
EOF
```

To rotate to a fresh IP, change the session ID to any new value.

## Set Geo Target

Use a mobile IP from a specific US state:

```bash
python <<'EOF'
import urllib.request, os, json

connection_id = CONNECTION_ID
data = json.dumps({"target_geo": "us_ca"}).encode()
req = urllib.request.Request(
    f"https://api.aluvia.io/v1/account/connections/{connection_id}",
    data=data, method="PATCH"
)
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
req.add_header("Content-Type", "application/json")
result = json.load(urllib.request.urlopen(req))
print(json.dumps({"target_geo": result["data"]["target_geo"]}, indent=2))
EOF
```

### List Available Geos

```bash
python <<'EOF'
import urllib.request, os, json

req = urllib.request.Request("https://api.aluvia.io/v1/geos")
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
result = json.load(urllib.request.urlopen(req))
for geo in result["data"]:
    print(f"{geo['code']:8s} {geo['label']}")
EOF
```

## Check Account Balance

```bash
python <<'EOF'
import urllib.request, os, json

req = urllib.request.Request("https://api.aluvia.io/v1/account")
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
result = json.load(urllib.request.urlopen(req))
acct = result["data"]
print(json.dumps({
    "balance_gb": acct["balance_gb"],
    "connection_count": acct["connection_count"]
}, indent=2))
EOF
```

## Check Data Usage

```bash
python <<'EOF'
import urllib.request, os, json

req = urllib.request.Request("https://api.aluvia.io/v1/account/usage")
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
result = json.load(urllib.request.urlopen(req))
print(json.dumps(result["data"], indent=2))
EOF
```

## Smart Unblocking Workflow

When you encounter a block (403, 429, CAPTCHA), follow this pattern:

1. **Try the request directly first** (no proxy)
2. **If blocked**, get or create an Aluvia connection
3. **Retry through the proxy**
4. **If still blocked**, rotate the IP by changing session ID

```bash
python <<'EOF'
import urllib.request, os, json, time

TARGET_URL = "https://example.com/data"
API_KEY = os.environ["ALUVIA_API_KEY"]

# Step 1: Try direct
try:
    req = urllib.request.Request(TARGET_URL)
    req.add_header("User-Agent", "Mozilla/5.0")
    response = urllib.request.urlopen(req, timeout=10)
    print(json.dumps({"status": "direct_ok", "code": response.getcode()}))
except urllib.error.HTTPError as e:
    if e.code in (403, 429):
        print(json.dumps({"status": "blocked", "code": e.code, "action": "retrying_via_aluvia"}))

        # Step 2: Get or create an Aluvia connection
        data = json.dumps({"description": "unblock", "rules": ["*"]}).encode()
        api_req = urllib.request.Request(
            "https://api.aluvia.io/v1/account/connections", data=data, method="POST"
        )
        api_req.add_header("Authorization", f"Bearer {API_KEY}")
        api_req.add_header("Content-Type", "application/json")
        conn = json.load(urllib.request.urlopen(api_req))["data"]
        proxy_url = conn["proxy_urls"]["url"]

        # Step 3: Retry through Aluvia
        proxy_handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        req2 = urllib.request.Request(TARGET_URL)
        req2.add_header("User-Agent", "Mozilla/5.0")
        response = opener.open(req2, timeout=15)
        print(json.dumps({"status": "unblocked_via_aluvia", "code": response.getcode()}))
    else:
        raise
EOF
```

## Delete Connection

Clean up connections you no longer need:

```bash
python <<'EOF'
import urllib.request, os, json

connection_id = CONNECTION_ID
req = urllib.request.Request(
    f"https://api.aluvia.io/v1/account/connections/{connection_id}",
    method="DELETE"
)
req.add_header("Authorization", f"Bearer {os.environ['ALUVIA_API_KEY']}")
result = json.load(urllib.request.urlopen(req))
print(json.dumps(result["data"], indent=2))
EOF
```

## Error Handling

| Code | Meaning                                        |
| ---- | ---------------------------------------------- |
| 401  | Invalid or missing `ALUVIA_API_KEY`            |
| 403  | Endpoint requires account-level API token      |
| 404  | Connection not found                           |
| 422  | Validation error (bad rules, invalid geo code) |

### Troubleshooting: Invalid API Key

```bash
echo $ALUVIA_API_KEY
```

If empty, the user needs to set it. Get the API key from [dashboard.aluvia.io](https://dashboard.aluvia.io) → API tab.

## Notes

- **Reuse connections.** Create once, use many times. Don't create a new connection for every request.
- **Proxy selectively.** Only proxy requests to sites that block you. Direct connections are faster and don't consume data balance.
- **Rotate IPs** by changing the `session_id`. Each unique session ID gets a different mobile IP.
- **Data balance** is measured in GB. Check balance before large jobs. The user can purchase more data at [aluvia.io/pricing](https://www.aluvia.io/pricing).
- **No use case restrictions.** Unlimited data, unlimited connections.
- **Proxy URL format:** `http://USERNAME:PASSWORD@gateway.aluvia.io:8080`
- Mobile IPs are from real devices on Tier 1 US carriers. They have high trust scores and rarely get blocked.

## Resources

- [Aluvia Docs](https://docs.aluvia.io/)
- [Dashboard](https://dashboard.aluvia.io/)
- [Pricing](https://www.aluvia.io/pricing)
- [Python SDK](https://pypi.org/project/aluvia-sdk/) (for advanced use: local proxy with hostname routing)
- [Node SDK](https://www.npmjs.com/package/@aluvia/sdk)
