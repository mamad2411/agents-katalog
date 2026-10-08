---
name: diagnose-network
description: Investigate network connectivity issues by walking the stack from link layer up to application — Wi-Fi/Ethernet, DNS, routing, latency, and TLS. Trigger when the user says the internet is slow, a site won't load, "can't reach X", DNS errors, VPN issues, or asks why a specific host is unreachable.
---

# Diagnosing network problems

The job is to localize the failure: is it the user's machine, the local network, DNS, the route, or the destination? Don't run `ping 8.8.8.8` and stop. Walk the stack from the bottom up so each step rules out a layer below.

## 0. Pin down the symptom first

Before measuring, ask one clarifying question if it's not obvious from the user's message:

- **Everything is broken** vs. **one specific site/service is broken** — the diagnostic path is completely different.
- **Slow** vs. **fails entirely** — slow points at latency/DNS/MTU; fails points at routing/firewall/auth.
- **Was working, now isn't** vs. **never worked here** — the former suggests a recent change (network switch, VPN, DNS); the latter suggests config.

Also note: are they on Wi-Fi, Ethernet, tethered, or behind a VPN? VPNs change DNS, routing, and MTU all at once — flag this early.

## 1. Link layer — is the machine even on a network?

```bash
# macOS
ifconfig | grep -E "^[a-z]|inet " | grep -v "127.0.0.1"
networksetup -getairportnetwork en0           # current Wi-Fi SSID
ipconfig getsummary en0 2>/dev/null | grep -E "SSID|RSSI|Channel"   # signal strength

# Linux
ip -br addr
ip -br link
iwconfig 2>/dev/null | grep -E "ESSID|Signal"      # Wi-Fi
nmcli device status 2>/dev/null
```

Look for:
- **No IPv4 address** on the active interface → DHCP failed. Restart the interface or rejoin Wi-Fi.
- **169.254.x.x (link-local)** → DHCP failed silently; same fix.
- **RSSI worse than -75 dBm** (macOS) or "Signal level" weak (Linux) → Wi-Fi is too far/blocked. Move closer or switch to 5GHz.
- **Multiple default gateways** (e.g. Wi-Fi + Ethernet + VPN) → routing ambiguity. See step 3.

## 2. DNS — can names resolve?

DNS is the single most common cause of "the internet is broken". Test it independently from connectivity.

```bash
# Resolve via the OS resolver (uses configured DNS, /etc/hosts, mDNS, search domains).
dscacheutil -q host -a name <host>          # macOS
getent hosts <host>                          # Linux

# Resolve via a specific DNS server, bypassing the OS cache. Reveals "is it my resolver, or is it DNS itself?".
dig +short <host> @8.8.8.8
dig +short <host> @1.1.1.1
dig <host>   # full output: which servers were tried, latency (Query time), authority section

# What resolvers are configured?
scutil --dns | head -30                     # macOS — note macOS doesn't use /etc/resolv.conf
cat /etc/resolv.conf                        # Linux
resolvectl status 2>/dev/null               # systemd-resolved
```

Patterns:
- **OS resolver fails, public resolver works** → DNS server is the problem. VPN's DNS, captive portal, or stale cache. Try `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` (mac) or `resolvectl flush-caches` (linux).
- **All DNS fails, IP works** → DNS is fully blocked (corporate proxy, captive portal). Test with `curl --resolve <host>:443:<known-IP> https://<host>/`.
- **Wrong IP returned** → DNS hijack, stale cache, or `/etc/hosts` override. Check `/etc/hosts` and `dig +trace <host>`.
- **Slow DNS (Query time > 200ms repeatedly)** → switch resolver; probably worth setting Cloudflare/Google DNS explicitly.

## 3. Routing & reachability — can packets get there?

```bash
# Default route + interface
netstat -nr -f inet | head -10              # macOS
ip route                                     # Linux

# Reachability of the destination
ping -c 4 <host-or-IP>
ping -c 4 1.1.1.1                            # known-good public IP
ping -c 4 <default-gateway>                  # local network (from step above)

# Path — where do packets stop?
traceroute -n -w 2 -q 1 <host>              # macOS / Linux (-n = numeric, -w 2 = 2s timeout per hop)
mtr -rwc 30 <host>                           # Linux (better — combines traceroute + ping)
```

Read the trace bottom-up:
- **Loss starts at hop 1 (gateway)** → local network problem (Wi-Fi, switch, ISP modem).
- **Loss starts mid-path then recovers** → some routers don't reply to ICMP; ignore if the destination still pings. Real loss appears as `* * *` continuing to the end.
- **Loss only on the final hop** → destination host or its firewall.
- **High latency on one hop, low after** → that hop reports its own ICMP slowly; not a real bottleneck.

If `ping` works but the app doesn't:
- Test the actual port: `nc -vz <host> <port>` or `curl -v telnet://<host>:<port>`.
- ICMP is often allowed while specific TCP ports are blocked by firewalls.

## 4. Application layer — is the service itself responding?

```bash
# HTTP/HTTPS — show timings and TLS handshake
curl -v -o /dev/null -s -w 'dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s ttfb=%{time_starttransfer}s total=%{time_total}s code=%{http_code}\n' https://<host>/

# TLS handshake details (cert chain, SNI, protocol)
openssl s_client -connect <host>:443 -servername <host> </dev/null 2>&1 | head -30
```

Read `curl -w` timings:
- **`dns` high** → see DNS section.
- **`connect` high** → TCP-level latency or SYN drops. Compare to `ping` RTT.
- **`tls` high** → TLS handshake slow. Often cert chain fetch (AIA) over a slow link.
- **`ttfb` high but others fast** → server-side. Not a client-network problem.

## 5. VPN, proxies, and captive portals — the usual culprits

If the user mentions a VPN, corporate network, or hotel/airport Wi-Fi, check these *before* deeper digging:

```bash
# Is a VPN interface up?
ifconfig | grep -E "utun|tun|tap"            # macOS
ip -br link | grep -E "tun|wg|ppp"           # Linux

# Is HTTP traffic going through a proxy?
echo "HTTP_PROXY=$HTTP_PROXY HTTPS_PROXY=$HTTPS_PROXY NO_PROXY=$NO_PROXY"
scutil --proxy                               # macOS system proxy

# Captive portal detection (macOS opens this URL at join)
curl -s -o /dev/null -w "%{http_code}\n" http://captive.apple.com/hotspot-detect.html
# Should return 200 with "Success" body. Anything else = captive portal interception.
```

Common patterns:
- **Site loads outside VPN, fails on VPN** → VPN's DNS or split-tunneling. Check `scutil --dns` for the VPN's nameservers.
- **HTTP proxy env var set but proxy unreachable** → unset it (`unset HTTP_PROXY HTTPS_PROXY`) or fix the proxy.
- **Captive portal** → open a browser to any HTTP (not HTTPS) site to trigger the portal page.

## 6. MTU / fragmentation issues (rarer but distinctive)

Symptom: small things work (ping, DNS, HTTP HEAD) but large transfers stall (page hangs after first chunk, `git clone` hangs on big repos, SSH hangs after login). Almost always VPN-related.

```bash
# Probe the largest packet that gets through without fragmentation.
# macOS: -D forbids fragmentation. -s sets payload size.
ping -D -s 1472 -c 3 1.1.1.1
# Linux: -M do = don't fragment.
ping -M do -s 1472 -c 3 1.1.1.1
```

If 1472 fails but 1400 succeeds, MTU on the path is below 1500. Set the interface MTU to 1400 (VPN tunnels are typically 1380–1420):

```bash
sudo ifconfig <iface> mtu 1400              # macOS
sudo ip link set dev <iface> mtu 1400       # Linux
```

## How to report back to the user

- State *which layer* you've localized the problem to (link / DNS / routing / app / VPN / MTU). Vague "your network is broken" reports aren't actionable.
- Show the smallest reproducer that demonstrates the failure (one `dig`, one `curl -w`) so the user can re-run it themselves.
- Separate **diagnosis** from **fix**. Many fixes (`flushcache`, MTU change, gateway reset) are cheap and reversible — propose them, but don't run network-wide changes without confirmation.
- If you've ruled out the user's machine and the problem is upstream (ISP, destination, VPN provider), say so explicitly — it tells the user where to escalate.
