---
name: unifi-api
description: Interact with a UniFi Dream Router (UDR) or any UniFi OS console via its REST API. Use this skill whenever the user wants to query or control their UniFi network — listing connected clients, blocking/unblocking devices, managing firewall policies, checking WAN health and speed test results, rebooting devices, managing VLANs or SSIDs, reading traffic stats, port forwarding, or any other UniFi network management task. Trigger even if the user doesn't say "API" or "UniFi" — phrases like "check my network", "block that device", "show me who's connected", "add a firewall rule", "what's my WAN IP", "how's my internet speed", or "what's on the guest network" are all good triggers.
allowed-tools:
  - Bash(python3 *:*)
  - Bash(curl -sk *:*)
---

# UniFi API Skill

Interact with a UniFi Dream Router or other UniFi OS console via its REST API.
Tested against UDR-7 running UniFi OS 4.x / Network Application 10.x.

## Setup

Ask the user for:
- **Router IP** (commonly `192.168.1.1`, `10.0.0.1`, or `10.0.1.1`)
- **API key** — read from `UNIFI_API_KEY` env var (generate in Network App → Integrations → Create New API Key)

All requests go to port **443** over HTTPS. The router uses a self-signed cert by default.

```python
import os, urllib.request, json, ssl

BASE = f"https://{ROUTER_IP}"
KEY = os.environ["UNIFI_API_KEY"]
HEADERS = {"X-API-KEY": KEY, "Accept": "application/json"}
CTX = ssl._create_unverified_context()  # self-signed cert

def get(path):
    req = urllib.request.Request(f"{BASE}{path}", headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())

def post(path, body=None):
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, method="POST",
        headers={**HEADERS, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())

def put(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, method="PUT",
        headers={**HEADERS, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())
```

Curl equivalent:
```bash
curl -sk -H "X-API-KEY: $UNIFI_API_KEY" -H "Accept: application/json" \
  https://<ROUTER_IP>/proxy/network/integration/v1/sites
```

**Note:** The API key works on both the Integration API and the legacy private API — no session cookie needed on UDR-7.

> **Security note:** `ssl._create_unverified_context()` disables TLS certificate verification to accommodate the router's self-signed cert. This is acceptable on a trusted home LAN but means a MITM on the same network could intercept the API key. Do not use this pattern over untrusted networks.

## Site Identifiers

Two formats are used depending on the API layer. Always start by fetching sites:

```python
sites = get("/proxy/network/integration/v1/sites")["data"]
SITE = sites[0]["id"]              # UUID — for Integration API
SITE_S = sites[0]["internalReference"]  # short name (usually "default") — for Legacy API

IV1    = f"/proxy/network/integration/v1/sites/{SITE}"
LEGACY = f"/proxy/network/api/s/{SITE_S}"
```

## Response Formats

**Integration API** — paginated:
```json
{"offset": 0, "limit": 25, "count": 25, "totalCount": 100, "data": [...]}
```
Page through with `?offset=N&limit=25`. To get all results loop until `offset + count >= totalCount`.

**Legacy API** — flat list:
```json
{"meta": {"rc": "ok"}, "data": [...]}
```

---

## Endpoints Reference

### Clients / Stations

```python
# All currently connected clients (rich: ip, mac, hostname, tx/rx bytes,
# uptime, switch port, network, fingerprint, fixed_ip flag, etc.)
get(f"{LEGACY}/stat/sta")

# All known clients including historical
get(f"{LEGACY}/stat/alluser")

# Single client by MAC
get(f"{LEGACY}/stat/user/aa:bb:cc:dd:ee:ff")

# Via Integration API (lighter fields, paginated)
get(f"{IV1}/clients")
get(f"{IV1}/clients/{{clientId}}")
```

Key client fields: `mac`, `ip`, `hostname`, `name`, `network`, `network_id`,
`is_wired`, `uptime`, `first_seen`, `last_seen`, `wired-tx_bytes`,
`wired-rx_bytes`, `wired-tx_bytes-r` (current rate), `wired-rx_bytes-r`,
`sw_port`, `use_fixedip`, `fixed_ip`, `local_dns_record`, `is_guest`,
`dev_family`, `oui`, `confidence`.

**Client commands** _(destructive — confirm MAC before executing)_**:**
```python
post(f"{LEGACY}/cmd/stamgr", {"cmd": "block-sta",   "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/stamgr", {"cmd": "unblock-sta", "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/stamgr", {"cmd": "kick-sta",    "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/stamgr", {"cmd": "forget-sta",  "mac": "aa:bb:cc:dd:ee:ff"})
```

### Devices

```python
# Full device stats (rich: system-stats, uplink, wan1, speedtest-status, port stats)
get(f"{LEGACY}/stat/device")

# Lightweight list
get(f"{LEGACY}/stat/device-basic")

# Via Integration API
get(f"{IV1}/devices")
get(f"{IV1}/devices/{{deviceId}}")
```

Key device fields: `mac`, `name`, `model`, `version`, `uptime`,
`system-stats` (cpu%, mem%, uptime string), `uplink` (ip, rx_bytes, tx_bytes,
drops, latency, xput_down, xput_up, speedtest_lastrun), `wan1` (full port stats),
`speedtest-status` (latency, xput_download, xput_upload, server details).

**Device commands** _(destructive — `restart`, `upgrade`, and `power-cycle` will disrupt connectivity; confirm with user before executing)_**:**
```python
post(f"{LEGACY}/cmd/devmgr", {"cmd": "restart",      "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/devmgr", {"cmd": "upgrade",      "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/devmgr", {"cmd": "set-locate",   "mac": "aa:bb:cc:dd:ee:ff"})  # blink LED
post(f"{LEGACY}/cmd/devmgr", {"cmd": "unset-locate", "mac": "aa:bb:cc:dd:ee:ff"})
post(f"{LEGACY}/cmd/devmgr", {"cmd": "speedtest"})
post(f"{LEGACY}/cmd/devmgr", {"cmd": "speedtest-status"})
post(f"{LEGACY}/cmd/devmgr", {"cmd": "power-cycle",  "mac": "...", "port_idx": 1})
```

### Health & Status

```python
# Subsystem health: wlan, wan, www, lan, vpn
# wan: WAN IP, ISP name, latency monitors, uptime stats, client counts, CPU/mem
# www: xput_up/down, latency, speedtest_status, speedtest_lastrun
get(f"{LEGACY}/stat/health")

# Controller version, timezone, hostname, all IP addresses, uptime
get(f"{LEGACY}/stat/sysinfo")
```

Health `www` subsystem fields: `xput_up`, `xput_down`, `latency`, `uptime`,
`drops`, `speedtest_status`, `speedtest_lastrun`, `speedtest_ping`.

### Networks / VLANs

```python
# Full network config (WAN + all LANs/VLANs)
# Fields: name, purpose (wan/corporate), ip_subnet, vlan, wan_dns1/2,
#         wan_provider_capabilities, firewall_zone_id
get(f"{LEGACY}/rest/networkconf")
put(f"{LEGACY}/rest/networkconf/{{id}}", updated_fields)

# Integration API (cleaner, full CRUD)
get(f"{IV1}/networks")
post(f"{IV1}/networks", new_network)
put(f"{IV1}/networks/{{networkId}}", updated_network)
# DELETE also available
```

### WiFi / SSIDs

```python
# All WLANs — fields: name, enabled, wlan_band (both/2g/5g), wpa_mode,
#   x_passphrase (returned in plaintext — avoid logging), networkconf_id,
#   usergroup_id, hide_ssid, is_guest, pmf_mode
get(f"{LEGACY}/rest/wlanconf")

# Toggle on/off
put(f"{LEGACY}/rest/wlanconf/{{id}}", {"enabled": True})

# Change password
put(f"{LEGACY}/rest/wlanconf/{{id}}", {"x_passphrase": "newpassword"})

# Create new SSID
post(f"{LEGACY}/add/wlanconf", {...})
```

### Firewall

**Firewall policies** (Integration API — the primary firewall system on UDR-7):
```python
# Paginate through all policies
get(f"{IV1}/firewall/policies?offset=0&limit=25")

# Fields: id, enabled, name, description, index, action.type (BLOCK/ALLOW),
#   source.zoneId, source.trafficFilter, destination.zoneId,
#   destination.trafficFilter (ipAddressFilter, portFilter, macAddressFilter),
#   ipProtocolScope.ipVersion, loggingEnabled, metadata.origin

# Enable/disable a policy (PATCH — use requests library for PATCH support)
# PATCH /proxy/network/integration/v1/sites/{SITE}/firewall/policies/{id}
# body: {"enabled": false}
```

**Firewall zones:**
```python
get(f"{IV1}/firewall/zones")
# Zone fields: id, name, networkIds, metadata.origin (SYSTEM_DEFINED/USER_DEFINED)
# System zones: Gateway, Vpn, Dmz, Hotspot, External, Internal
```

**Legacy firewall** (old-style rules — may be empty if using new policy system):
```python
get(f"{LEGACY}/rest/firewallrule")   # individual rules
get(f"{LEGACY}/rest/firewallgroup")  # IP/MAC address groups
```

**Traffic rules** (v2):
```python
get(f"/proxy/network/v2/api/site/{SITE_S}/trafficrules")
post(f"/proxy/network/v2/api/site/{SITE_S}/trafficrules", new_rule)
```

### Port Forwarding

```python
# Read current rules
# Fields: name, fwd (dest IP), fwd_port, dst_port, proto, enabled,
#   pfwd_interface, rx_bytes, rx_packets
get(f"{LEGACY}/stat/portforward")

# Create
post(f"{LEGACY}/rest/portforward", {
    "name": "My Service", "fwd": "10.0.0.x", "fwd_port": "8080",
    "dst_port": "8080", "proto": "tcp_udp", "pfwd_interface": "wan"
})

# Enable/disable
put(f"{LEGACY}/rest/portforward/{{id}}", {"enabled": False})
```

### Time-Series Stats

```python
# Always specify attrs to get useful data back
ATTRS = ["bytes", "rx_bytes", "tx_bytes", "num_sta"]

post(f"{LEGACY}/stat/report/5minutes.site",  {"attrs": ATTRS})
post(f"{LEGACY}/stat/report/hourly.site",    {"attrs": ATTRS})
post(f"{LEGACY}/stat/report/daily.site",     {"attrs": ATTRS})

# Per-client (filter by MAC)
post(f"{LEGACY}/stat/report/hourly.user",
     {"attrs": ["bytes", "rx_bytes", "tx_bytes"], "mac": "aa:bb:cc:dd:ee:ff"})

# Per-AP
post(f"{LEGACY}/stat/report/hourly.ap", {"attrs": ATTRS})
```

Data retention defaults: 24h at 5-min resolution, 7d hourly, 90d daily.

### Events & Alarms

```python
get(f"{LEGACY}/stat/event")   # recent events
get(f"{LEGACY}/stat/alarm")   # active alarms
```

### Site Settings

```python
# Full settings blob (keys: super_identity, super_mgmt, connectivity, locale,
#   snmp, mgmt, usg, ips, rsyslogd, broadcastping, and more)
get(f"{LEGACY}/rest/setting")
```

---

## What Does NOT Work on UDR-7 (Integration API 404s)

These endpoints exist in the docs but return 404 on UDR-7 firmware 4.x:
- `/wifi-broadcasts` → use legacy `/rest/wlanconf` instead
- `/dns-policies`
- `/supporting-resources/wan-interfaces`
- `/supporting-resources/dpi-categories`
- `/supporting-resources/device-tags`
- `/supporting-resources/site-to-site-vpn-tunnels`
- `/supporting-resources/vpn-servers`
- `/supporting-resources/radius-profiles`
- `/v2/api/site/{site}/trafficstats`

---

## Common Patterns

**Get WAN status:**
```python
health = get(f"{LEGACY}/stat/health")["data"]
wan = next(s for s in health if s["subsystem"] == "wan")
www = next(s for s in health if s["subsystem"] == "www")
print(f"WAN IP: {wan['wan_ip']}, ISP: {wan.get('isp_name','?')}")
print(f"Speed: ↓{www['xput_down']} ↑{www['xput_up']} Mbps, latency: {www['latency']}ms")
```

**List clients sorted by current throughput:**
```python
clients = get(f"{LEGACY}/stat/sta")["data"]
for c in sorted(clients, key=lambda x: x.get("wired-tx_bytes-r", 0) + x.get("wired-rx_bytes-r", 0), reverse=True):
    name = c.get("name") or c.get("hostname") or c["mac"]
    tx_r = c.get("wired-tx_bytes-r", 0)
    rx_r = c.get("wired-rx_bytes-r", 0)
    print(f"{name:35} {c.get('ip','?'):16} ↓{rx_r/1024:.1f} ↑{tx_r/1024:.1f} KB/s")
```

**Find a client by name, hostname, or IP:**
```python
clients = get(f"{LEGACY}/stat/sta")["data"]
query = "my-device"
target = next((c for c in clients if
    query.lower() in (c.get("name","") + c.get("hostname","")).lower() or
    c.get("ip") == query), None)
```

**Paginate through all firewall policies:**
```python
policies, offset = [], 0
while True:
    page = get(f"{IV1}/firewall/policies?offset={offset}&limit=25")
    policies.extend(page["data"])
    if offset + page["count"] >= page["totalCount"]:
        break
    offset += 25
```

**Toggle an SSID:**
```python
wlans = get(f"{LEGACY}/rest/wlanconf")["data"]
wlan = next(w for w in wlans if w["name"] == "My SSID")
put(f"{LEGACY}/rest/wlanconf/{wlan['_id']}", {"enabled": not wlan["enabled"]})
```

**PATCH support** (needed for firewall policy enable/disable):
```python
# urllib doesn't support PATCH — install requests or use this workaround:
import urllib.request
class PatchRequest(urllib.request.Request):
    def get_method(self): return "PATCH"

req = PatchRequest(f"{BASE}{path}", data=json.dumps(body).encode(),
    headers={**HEADERS, "Content-Type": "application/json"})
with urllib.request.urlopen(req, context=CTX) as r:
    return json.loads(r.read())
```
