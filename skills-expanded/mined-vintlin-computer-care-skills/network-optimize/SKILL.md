---
name: network-optimize
description: Use to establish a baseline when a user reports slow internet, unstable latency, packet loss, DNS delays, Wi-Fi or Ethernet issues, poor speedtest results, MTU/path-MTU problems, loaded latency, browser-only or terminal-only slowness, IPv4/IPv6 differences, background bandwidth contention, stale saved networks, mDNS/Bonjour/LLMNR noise, VPN-on networking, proxy/PAC/TUN overlap, or Clash/V2Ray/Xray/Mihomo routing conflicts on macOS, Windows, or Linux.
---

# Network Optimize

## Overview

Establish a read-only baseline before any change. Prefer reversible, minimal changes. Explain each meaningful decision with conclusion, reason, risk, next step, scope, and validation.

Never ask the user to disable their VPN/proxy as a first step — preserve the required access path. Do not optimize from a single speed number.

## Workflow

1. Classify the symptom: web first-load, bulk download, video call, gaming, SSH, Git/npm/pip/Docker, AI API, LAN/NAS, browser-only, terminal-only, VPN-only, or all traffic.
2. Identify OS, active interface, default route, DNS, proxy/PAC, VPN/TUN state, IPv4/IPv6 state, browser path, and available tools.
3. Run a read-only baseline: responsiveness and loaded latency, bandwidth, DNS transport and answer quality, packet loss, MTU/path-MTU, Wi-Fi/Ethernet link quality, curl timing, route/path, and active bandwidth consumers.
4. Compare paths when relevant:
   - required VPN/TUN path vs in-app node/mode/rule variations
   - direct or no-proxy only when it does not break required access, or when the user explicitly asks for that comparison
   - IPv4 vs IPv6
   - browser vs curl/terminal
   - idle vs loaded network
   - LAN target vs public target
5. Classify the bottleneck:
   - Access: weak Wi-Fi, crowded channel, low negotiated rate, Ethernet negotiation, AP backhaul, router queueing.
   - DNS: slow resolver, poor CDN answer, DoH/split DNS mismatch, VPN DNS hijack conflicts, stale cache.
   - Path: packet loss, PMTU/MSS mismatch, ISP/CDN route, VPN exit path, bad node.
   - Transport/NIC: TCP retransmits, adapter errors/drops, offload/queue/driver problems.
   - Application: browser DoH, HTTP/3/QUIC, proxy extension, certificate/security filter, service TTFB.
   - Policy: enterprise VPN, NRPT/per-link DNS, MDM/GPO, firewall/EDR/content filter.
6. Apply the smallest safe fixes first.
7. Validate with the same measurements and summarize before/after numbers plus rollback.

## Platform References

Read only the relevant reference:

| Reference | Topic |
| --- | --- |
| `references/common-baseline.md` | Common baseline and safety |
| `references/macos.md` | macOS |
| `references/windows.md` | Windows |
| `references/linux.md` | Linux |
| `references/browser-app-layer.md` | Browser/app layer |
| `references/dns-doh-splitdns.md` | DNS, DoH, and split DNS |
| `references/pmtu-mtu.md` | PMTU and MTU |
| `references/tcp-nic.md` | TCP and NIC diagnosis |
| `references/router-sqm-bufferbloat.md` | Router SQM and bufferbloat |
| `references/vpn-proxy.md` | VPN/proxy overlap |

Use this routing table when the symptom already points to a specific layer:

| Symptom | Read first |
| --- | --- |
| Calls, games, SSH, or page loads stall during upload/download | `references/router-sqm-bufferbloat.md`, `references/common-baseline.md` |
| HTTP/3/QUIC, voice/video, game UDP, or VPN UDP works poorly while TCP works | `references/pmtu-mtu.md`, `references/browser-app-layer.md`, `references/vpn-proxy.md` |
| Browser is slow but curl/terminal is normal | `references/browser-app-layer.md`, `references/dns-doh-splitdns.md` |
| Terminal tools are slow but browser is normal | `references/browser-app-layer.md`, `references/vpn-proxy.md`, platform reference |
| Internal or corporate domains fail | `references/dns-doh-splitdns.md`, `references/vpn-proxy.md`, platform reference |
| IPv4 and IPv6 differ | `references/dns-doh-splitdns.md`, `references/pmtu-mtu.md`, platform reference |
| Ethernet negotiates low speed or adapter errors increase | `references/tcp-nic.md`, platform reference |
| WSL, Docker, registries, npm, pip, or Git are slow while host browsing is normal | `references/vpn-proxy.md`, `references/dns-doh-splitdns.md`, platform reference |

Use scripts as read-only diagnostic helpers:

- macOS: `scripts/macos_network_snapshot.sh`
- Windows PowerShell: `scripts/windows_network_snapshot.ps1`
- Linux: `scripts/linux_network_snapshot.sh`

Scripts collect state only; they do not change DNS, MTU, proxy, routes, VPN, firewall, TCP, or NIC settings.

`scripts/macos_network_snapshot.sh` runs `networkQuality` by default, which uses Internet data. Set `SKIP_BANDWIDTH=1` to skip that section when data usage, metered links, or active calls matter.

## Decision Heuristics

- Treat loaded latency/responsiveness as a first-class metric. If idle latency is normal but latency spikes during upload/download, classify loaded-latency or bufferbloat before changing DNS.
- If DNS query time is fast but TCP, TLS, TTFB, or total HTTP time is high, do not over-optimize DNS.
- If DNS is fast but CDN IP or TTFB is poor, compare A, AAAA, HTTPS/SVCB answers, browser Secure DNS state, and curl `remote_ip` across resolvers.
- If IPv4 and IPv6 behave differently, treat it as Happy Eyeballs, dual-stack routing, DNS answer quality, PMTU, VPN/TUN, firewall, or CDN behavior before disabling IPv6 globally.
- If HTTP/3/QUIC, VPN, or UDP-heavy apps fail while TCP works, investigate PMTU/UDP/QUIC behavior before lowering global interface MTU.
- If browser and curl disagree, inspect browser Secure DNS/DoH, HTTP/3/QUIC, extensions, NetLog/HAR, cache, certificate interception, and proxy rules.
- If terminal tools are slow but browser is fast, inspect shell proxy variables, WinHTTP, WSL/Docker DNS, CLI CA certificates, and `NO_PROXY`.
- If Wi-Fi RSSI is strong but throughput is low, inspect channel width, band, MCS/NSS, BSSID roaming, AP backhaul, WPA mode, and driver.
- If Ethernet negotiates below expected speed, inspect cable, switch port, duplex, EEE, driver, and error counters.
- If adapter errors/drops increase during tests, prioritize NIC/driver/offload/queue diagnosis over DNS or VPN changes.
- If VPN/TUN is active, preserve the required VPN app and compare safe in-app variations first: node, policy/rule mode, TUN vs system proxy ownership when both remain available, DNS mode, UDP/QUIC setting, and browser path. Do not tell the user to pause or quit the VPN app unless they explicitly ask for a direct-access experiment.
- If system DNS is fully overridden by VPN or browser DoH, changing OS DNS may not affect the observed application.
- If MTR/traceroute shows loss on a single intermediate hop but later hops and the destination are clean, treat it as likely ICMP rate limiting.
- If WSL or Docker is slow while the host is normal, inspect virtualization networking, DNS tunneling, auto proxy, container DNS, registry mirror, and VPN compatibility.
- If a change improves one metric but worsens throughput, loss, or loaded latency, roll it back and keep the evidence.

## Safe Change Ladder

Use this order unless evidence points elsewhere:

0. Read-only diagnosis: routes, DNS, proxy, VPN, Wi-Fi/Ethernet, IPv4/IPv6, curl timing, adapter stats, path tests.
1. Low-risk reversible actions: flush DNS cache, switch to better link/AP, change VPN node/protocol, pause a named bandwidth-heavy task.
2. Local configuration with evidence and rollback: per-interface DNS, interface MTU, proxy bypass, Wi-Fi profile priority, low-data/metered setting.
3. High-risk system configuration: TCP globals, Windows registry/adapter advanced properties, Linux offload/ring/coalescing, firewall, IPv6 disablement, system services. Do not do this by default.
4. Network device configuration: router SQM/CAKE, channel width, WPA mode, firmware, AP backhaul, flow offload. Require user authority over the device.

## Safety Rules

Do not recommend these as first-line fixes:

- Disable IPv6 globally.
- Disable firewall or security/EDR tools globally.
- Change TCP global parameters without workload evidence.
- Change NIC offload, ring, coalescing, or power settings without packet/error evidence.
- Replace, pause, or disable VPN/proxy apps or corporate DNS before checking split DNS and safe in-app alternatives.
- Force public DNS on corporate networks.
- Delete Wi-Fi profiles without listing them.
- Enable both router SQM and hardware flow offloading as a universal optimization.
- Interpret one speedtest result as the network baseline.

## Common Safe Fixes

- Flush DNS cache.
- Prefer Ethernet, 5 GHz, or 6 GHz over crowded 2.4 GHz.
- Add stable secondary DNS only if system DNS is in use and not overridden by VPN, DoH, or enterprise policy.
- Set interface MTU only when path-MTU evidence supports it; prefer VPN/router MSS or MTU tuning when available.
- Remove only clearly obsolete preferred Wi-Fi networks after naming them.
- Avoid duplicate VPN/TUN/proxy ownership while preserving the path the user needs.
- Recommend VPN node/protocol changes if system, link, DNS, and route baselines are already clean.

## Reporting

For each meaningful decision, report:

- Conclusion
- Reason
- Risk
- Next step
- Scope and validation method when changing settings

For before/after work, use this structure:

```text
Baseline:
- Symptom:
- Scope: interface / app / VPN path / IPv4 or IPv6 / direct or proxy
- Key metrics: idle latency, loaded latency or responsiveness, packet loss, DNS answers, remote IP, curl timing, throughput

Action:
- Change:
- Why this is the smallest safe change:
- Risk:
- Rollback:

After:
- Same metrics:
- Improved / unchanged / regressed:
- Residual uncertainty:
- Next step:
```

Finish with exact rollback commands where possible and call out any metric that was not re-measured.
