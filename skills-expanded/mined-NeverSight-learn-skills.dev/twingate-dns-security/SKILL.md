---
name: twingate-dns-security
description: >
  Twingate Internet Security — DNS filtering, exit networks, browser security,
  and DNS-over-HTTPS. Load when the user mentions DNS filtering, content filtering,
  internet security, exit networks, egress routing, browser security, NextDNS,
  DoH, DNS categories, or profile priority. Also trigger on 'Internet Security',
  'DNS Security Profile', 'fixed egress IP', or 'SaaS allowlisting' in a Twingate
  context. Also activate for DNS conflicts and symptom-shaped DNS queries: a
  third-party DNS filter or AV product conflicting with Twingate (Cisco Umbrella,
  DNSFilter, AdGuard, Avast Real Site Protection), CGNAT range conflicts
  (`100.96/12`), multiple-network-interface DNS resolution problems, "all
  nameservers have failed", DNS request delays on Linux, a Docker container's
  second DNS query returning the wrong IP, or a personal/DIY exit-network VPN
  built on Twingate.
---

## Role

This skill owns Twingate's Internet Security product area: DNS filtering, exit networks, DNS-over-HTTPS, and browser security. It covers DNS Security Profile design, priority ordering, group-based policy assignment, exit network egress patterns, and the licensing boundary between Internet Security and Private Access. It is the authority on when to use DNS filtering versus exit networks versus resource-level access policy.

## Decisions & Guidelines

- **Confirm Internet Security entitlement before designing any solution around DNS filtering or exit networks.** Internet Security is a separate product area and may require a different license tier. If the customer doesn't have entitlement, DNS Security Profiles and exit network configuration won't appear in the admin console.
- **Exit networks route traffic to a fixed egress point — they do not block destinations.** If the goal is to prevent access to a website, use DNS filtering. If the goal is to ensure traffic exits from a fixed IP, use an exit network. These are not substitutes.
- **Priority is numeric, and lower number = higher priority.** This is the most commonly confused aspect of DNS Security Profile assignment. A permissive Engineering profile at priority 1 beats a restrictive Corporate profile at priority 2, even when the user is in both groups.
- **Always configure the "Everyone" group as a baseline with the high-confidence threat categories blocked at minimum.** Users not in any group with a profile receive no filtering at all. "Everyone" is the safety net. Current category names and recommended baseline categories are in `references/dns-security-overview.md` and `references/dns-filtering.md`.
- **Enable STRICT fallback mode only after pre-populating the allow list with the customer's known-good domains.** STRICT mode (deny-by-default) will block legitimate SaaS tools until they are explicitly allowed. Always roll out STRICT to a pilot group first.
- **DNS-over-HTTPS in Twingate covers only DNS queries that flow through the Twingate Client.** It does not encrypt OS-level DNS for non-Twingate traffic or queries made before the Client starts. If full-device DoH is required, configure it at the OS or network level in addition to Twingate.
- **A "DNS conflict" symptom is usually a CGNAT range collision or a competing DNS-modifying tool, not a Twingate misconfiguration.** Twingate claims the entire `100.96/12` range and acts as a transparent DNS proxy on only one interface (the default gateway's). Before redesigning a DNS Security Profile, rule out a third-party DNS filter/AV product or a multi-NIC environment — the help-center corpus documents the specific known conflicts and their workarounds.

## Search References First

**Grep `references/` with the user's own keywords or exact error text before answering.**
Vendor names, CGNAT ranges, and exact log lines live in the file bodies, not the
filenames:

```
grep -ril "all nameservers have failed" references/   # -> 9539322912-twingate-linux-client-fails-to-start-logs-show-dns-errors.md
grep -ril "100.96/12" references/                     # -> 4359531030-cgnat-ip-conflicts-...md
grep -ril "avast" references/                         # -> 6928700605-dns-avast-real-site-protection.md
```

If the user reports an exact error message or names a third-party product, **grep for
it before theorizing about causes.** Never answer from training-data memory for: DNS
filtering category names, third-party DNS/AV product conflicts, exit-network
configuration steps, or DNS Security Profile schema and priority mechanics — the
category list and third-party integration behavior change and are documented per-vendor
in `references/`. Filenames reveal only the topic — vendor names, tool names, and exact
error strings live in the bodies. This skill also owns `gh-*` community repos (DIY VPN,
Ubiquiti headless gateway); **if the user asks whether tooling or a reference build
exists for X, grep before saying no.**

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: profile-to-group
mapping → **identity**; split-DNS interception model → **architect**; filtering breaking
access → **troubleshoot**.

- **→ twingate-identity**: DNS Security Profiles attach to Groups; for group management, SCIM provisioning, or understanding how group membership determines which profile applies
- **→ twingate-architect**: for split DNS model questions — understanding which DNS queries Twingate intercepts before configuring Internet Security
- **→ twingate-troubleshoot**: when DNS filtering appears to be interfering with private resource access or general connectivity, or the symptom is a client-side bug rather than a DNS Security Profile design question

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Three kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`{numeric-id}-{slug}.md`** — Twingate help-center articles: symptom-shaped DNS
  conflict reports, exact error strings, and per-platform gotchas.
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: community
  exit-network deployment tooling.

| If the user asks about… | Read first |
|---|---|
| DNS Security overview, profile design, exit-node config, DoH enforcement | `dns-security-overview.md`, `dns-security.md` |
| DNS filtering categories, allow/block lists, profile priority | `dns-filtering.md` |
| Internet Security product scope, licensing, client config | `internet-security.md`, `internet-security-client-configuration.md` |
| Exit networks (egress IPs, configuration, AWS-specific patterns) | `exit-networks.md`, `configuring-aws-exit-nodes.md` |
| Browser security features | `browser-security.md` |
| DNS over HTTPS (Cloudflare integration) | `doh-cloudflare.md` |
| NextDNS integration | `nextdns-configuration.md` |
| Cisco AnyConnect with Umbrella alongside Twingate | `configuring-anyconnect-with-umbrella.md` |
| Zscaler alongside Twingate | `configuring-zscaler-with-twingate.md` |
| Netskope DLP alongside Twingate | `netskope-dlp-config.md` |
| Comprehensive DNS guide | `dns-ultimate-guide.md` |
| **Personal/DIY exit-network VPN** — Terraform deploys for Minikube, DigitalOcean Droplets, or DigitalOcean Kubernetes; requires Home/Enterprise plan (Exit Networks unavailable on Starter) | `gh-twingate-community-diy-vpn.md` |
| **Headless client on Ubiquiti UniFi gateways** — systemd-nspawn container intercepting a VLAN's DNS via iptables + bind9 and forwarding through Twingate split-DNS resolvers, for whole-VLAN access with no per-device client | `gh-twingate-community-ubiquiti-headless-gateway.md` |
| **Third-party DNS filter / AV conflicts** — DNSFilter, AdGuard for Mac, Avast Real Site Protection running alongside Twingate | `5745151855-dns-using-dnsfilter-alongside-twingate.md`, `8487611740-dns-using-adguard-for-mac-alongside-twingate.md`, `6928700605-dns-avast-real-site-protection.md` |
| **CGNAT range & multi-interface DNS conflicts** — `100.96/12` collisions, Windows client only honoring the default-gateway interface's DNS, general multi-NIC DNS/resource-access issues | `4359531030-cgnat-ip-conflicts-dns-resolution-resource-access-issues-with-twingate.md`, `1402124326-windows-client-limitations-with-multiple-network-interfaces-with-differing-dns.md`, `3556574910-potential-dns-or-resource-access-issues-on-devices-with-multiple-network-interfaces-connected.md` |
| **Linux DNS client bugs** — client fails to start with "All nameservers have failed" (Network Manager v1.42+ incompatibility), general DNS request delays | `9539322912-twingate-linux-client-fails-to-start-logs-show-dns-errors.md`, `4817674373-dns-request-delays-while-using-twingate-on-linux.md` |
| **macOS Docker DNS resolution bug** — container's first DNS query succeeds, subsequent queries fall back to a non-CGNAT resolver; fix via pinning `--dns` flags to Twingate resolvers | `7318897884-macos-client-docker-container-s-second-connections-to-twingate-dns-resource-fails.md` |

For comprehensive coverage, see [`references/`](./references/) for the full
set of doc summaries. **Default to checking** — category names, third-party
integration behavior, and known-conflict lists change.
