---
name: c2-hygiene
description: Command-and-Control infrastructure hygiene for red teams — redirector architecture (HTTP/HTTPS/DNS), traffic shaping (sleep/jitter/staging), TLS-cert and domain aging, OPSEC checklist, and defensive detection opportunities mapped to ATT&CK Command and Control (TA0011).
---

# C2 Hygiene

> **Sandbox/lab-only and RoE-strict**: this skill describes architecture and hygiene discipline for C2 infrastructure in red-team engagement context. Specific beacon configurations, malleable-profile strings for named C2 frameworks, or EDR-bypass recipes do not live here — those belong in a closed engagement vault. The skill provides architectural patterns, OPSEC checklists, and a detection perspective, all verifiable in a lab.

## When to use

C2 (Command and Control) is the operational backbone of every red-team engagement or APT simulation: how you talk to placed implants without getting caught, and how you make the traffic realistic enough that detection tuning has something to bite on. This skill provides the architecture and hygiene lens, not framework-specific setup.

Triggers on:

- A question like "how do I set up C2 redirectors", "is domain fronting still feasible in 2026", "what is a reasonable beacon jitter", "OPSEC review of our C2 stack", "how do we test detection against our C2".
- Red-team engagement preparation where C2 infra needs to be designed or assessed.
- A purple-team exercise where the defensive side wants to test detection against realistic beacons.
- Defensive context: a SOC team wants to know which patterns to detect — this skill gives the offensive lens, `detection-engineer` provides the rule side.
- Threat emulation against specific threat actors (CIS / MITRE Adversary Emulation Plans) — this skill provides the C2 layer; threat intel comes from elsewhere.

### When NOT (handoff)

- Initial access or phishing → `phishing-sim`, `web-exploit-triage`, `payload-crafter`. This skill starts at "how does the implant keep talking".
- Post-exploitation / lateral movement / persistence → `post-exploit`, `ad-attacks`. C2 is the transport; those skills perform actions over it.
- Detection-rule building → `detection-engineer`, `siem-query`, `purple-ops`. This skill names detection opportunities; those skills build the rules.
- Final reporting → `pentest-reporter`.
- Threat intelligence on specific in-the-wild C2 frameworks → `ioc-hunter`.
- Forensics after an identified C2 in production → `forensics-assist` plus `ir-runbook`.

## Approach

Six phases. Phase 1 (architecture) and phase 4 (OPSEC discipline) are where C2 engagements fail or succeed.

### 1. Redirector architecture

An implant rarely talks directly to your teamserver — at least one redirector layer sits in between. Goal: shield the attack source, make traffic look legitimate, and reduce the cost of takedown.

**Layers** (from implant to operator):

- **Implant** in the target environment.
- **Front domain** the implant talks to. Preferably CDN-fronted, an "aged" domain with credible content.
- **Redirector** (HTTP/HTTPS): nginx or Apache with a reverse-proxy config that only forwards specific paths/User-Agents/headers to the teamserver, all others to a harmless sinkhole page (HTTP 200, no redirect — that would trigger a scanner).
- **DNS redirector** for DNS-C2 channels: your nameserver with an NS delegation of a subdomain to your C2 server.
- **Teamserver / C2 controller**: not directly reachable from the internet. Access via VPN or bastion.

**Selection criteria for the front domain**:

- Domain age (the older the more credible; a freshly registered domain = red flag for DNS monitoring).
- Categorization at filtering services (BlueCoat/SquidGuard/Cisco Umbrella). Categorize as news/business rather than unknown.
- TLS cert from a public CA with a credible subject (SAN matches the domain).
- Desired reputation via `urlscan.io` and `threatintelligenceplatform.com` checks before going live.

**Domain fronting**: routing traffic through a CDN with an SNI/Host-header mismatch so it looks bound for one host but is steered to another. Since ~2018 this has been closed by the major providers (Google, AWS CloudFront, Microsoft Azure). Through 2022–2024 it has not been reproducible in most mainstream CDNs without violating vendor policy. The skill names it as historical context, not a recommended technique for 2026.

**Alternatives to domain fronting**:

- **Domain borrowing / high-reputation CDN edge deployments**: legitimate tenant deployments that work as a front; vendor-policy boundaries vary.
- **Cloud-storage fronting**: object-storage public-read URLs (S3, GCS, Azure Blob) as a download relay. Vendor policies are similarly monitored.
- **DNS-over-HTTPS (DoH)** as a channel: traffic looks like ordinary DoH to Cloudflare/Google DNS.
- **Webhook services** (Slack, Discord, Telegram): API traffic is by definition outbound-allowed in many orgs. Detection via behavioural analysis on these legitimate services.

Discipline: never pick a front whose policy explicitly says it must not be used for this. Not just an ethical issue — if the provider does a takedown you lose your infra mid-engagement.

### 2. Traffic shaping and beacon tuning

Beacons are periodic check-ins from implant to teamserver. Two-axis discipline: how often and how regularly.

- **Sleep interval**: time between check-ins. Short sleep (10–30 sec) = fast interaction, more traffic, higher detection chance. Long sleep (5–60 min) = stealthier but slower. Default for stealthy engagement: minutes-range, not seconds.
- **Jitter**: percentage of random deviation around the sleep interval. Without jitter the interval is `60s, 60s, 60s` — a SIEM sees the regularity. With 30% jitter: `42s, 75s, 51s` — less cyclic. Default: 25–50% jitter.
- **Staging**: small clean initial payload (loader), full implant staged via a second request after trust is gained. Reduces first-impact detection.
- **Working-hours schedule**: beacon only during target-organization working hours. Implant sleeps outside 9–17 local time. Traffic blends in with legitimate work. Implementation via the implant clock (leaves a time-zone fingerprint, trade-off) or operator-side scheduled window.
- **C2 channel rotation**: multiple channels (HTTP, DNS, named-pipe) so a takedown of one does not stop everything. Implant config with fallback order.

Detection perspective per shaping choice:

- High jitter + long sleep is harder for frequency analysis, but TLS fingerprint and domain reputation are unchanged. Defense in depth detects multiple layers.
- A working-hours schedule is detectable when the implant clock does not match the actual target time zone (off by an hour).
- C2 channel rotation leaves a pattern where the same implant is seen on multiple channels.

### 3. TLS, certificates, and domain aging

C2 traffic in 2026 is almost always TLS-encrypted. Cert and domain discipline:

- **Cert issuer**: Let's Encrypt is free but low-reputation in some scoring systems. A commercial CA cert (DigiCert / Sectigo) lowers cert-based detection.
- **Cert fingerprint** (JA3/JA3S, JA4/JA4S since 2023): TLS-handshake fingerprint identifies the TLS stack. An implant with a JA3 that does not match the browsers in the target environment stands out. Discipline: match the implant's TLS stack to the expected fingerprint, or emulate legitimate-library traffic.
- **Domain age**: a fresh registration carries a "domain age <30 days" flag at multiple DNS-monitoring services. Plan domain purchase + DNS record publish weeks before the engagement.
- **Categorization at content filters**: pre-check via urlscan.io / Cisco Talos / Symantec WebPulse. Recategorize via vendor portals where possible.

### 4. OPSEC discipline

A bumper rail at every step in the C2 operation. The checklist mixes lagging and leading indicators.

- **Operator-side IP aging**: teamserver behind a VPN, not directly from the operator workstation. The VPN exit IP is not the same as the operator home IP.
- **DNS-resolution checks**: all implant domains via target-side resolvers, not operator-side. A mistake leaks operator DNS into target logs.
- **Tooling fingerprints**: default tooling (default Cobalt Strike strings, default Sliver paths) is fingerprinted by commercial EDR vendors. Customize ahead of time, no out-of-the-box runs.
- **Operator-side logging discipline**: every command, every beacon, every file transfer in an immutable log. For the report and for cleanup verification.
- **Cleanup readiness**: a pre-engagement checklist of what must be cleaned up post-engagement (DNS records, S3 buckets, registered domains, certs). Not improvised on delivery day.
- **Time discipline**: action windows synchronized with the target time zone (see working hours above), command execution only inside the agreed slot.
- **Communication with the customer**: real-time check-ins on tier-0 actions, in case something escalates.

### 5. Detection perspective and handoff to blue team

Every C2 choice leaves a signal behind. Document per layer what the blue team could have seen.

| C2 choice | Detection opportunity |
|---|---|
| Front domain with low age | DNS newly-registered-domain detection (Cisco Umbrella, DomainTools) |
| Default tooling strings | YARA rules from EDR vendors |
| TLS JA3 fingerprint mismatch | Network monitoring with a JA3 allowlist |
| Beacon without jitter | Frequency analysis on outbound DNS/HTTP |
| Working hours not matching TZ | Time-of-day anomaly detection |
| Volume anomaly during staging | Baseline-vs-current outbound-bytes anomaly |
| Geographic anomaly of VPN exit | GeoIP-based UEBA |

Per engagement report, a table like this plus mapping to ATT&CK TA0011 sub-techniques (T1071-application-layer-protocol, T1090-proxy, T1573-encrypted-channel, T1568-dynamic-resolution, T1132-data-encoding).

Handoff to `detection-engineer` for concrete sigma/KQL rules.

### 6. Verification-loop

Layer 1: scope (all C2 components within RoE? cleanup checklist complete?), assumptions (domain age and cert fingerprint actually checked before going live?), gaps (operator-side logging complete for reconstruction?). Layer 2: ATT&CK TA0011 sub-techniques correct, no invented JA3 strings or vendor-tool fingerprints, domain-fronting claims current (this technique shifts quickly; do not claim "still works on vendor X" without verification), OPSEC checklist not overstated.

## Output

```
C2 architecture — <engagement>
RoE: <which channels permitted, which working hours>
Goal: <stealthy / detection-validation / threat-emulation>

Architecture:
  Front domain:        <FQDN, age, categorization, cert issuer>
  HTTP redirector:     <hostname, infrastructure (cloud VM/container)>
  DNS redirector:      <NS delegation, subdomain>
  Channels in use:     <HTTP-S / DNS / DoH / webhook>
  Teamserver location: <behind VPN/bastion, not directly internet-reachable>

Beacon config (lab-tested):
  Sleep:               <minutes-range>
  Jitter:              <%>
  Staging:             <yes/no, how many stages>
  Working hours:       <slot in target time zone>
  Channel fallback:    <order>

OPSEC checklist:
  Operator-IP aging:    <ok/finding>
  DNS resolution:       <target-side / operator-side leak: ok/finding>
  Tooling fingerprint:  <customized: ok/finding>
  Cert fingerprint:     <JA3/JA4 vs target baseline>
  Domain categorization:<ok/finding>
  Logging complete:     <ok/finding>
  Cleanup checklist:    <prepared: ok/finding>

Detection opportunities (handoff to detection-engineer):
  Per C2 choice: signal shape, log source, rule shape

ATT&CK mapping:
  TA0011 sub-techniques in use: <T-IDs>

Cleanup status (post-engagement):
  Domain registration expired/sold: <date>
  TLS certs revoked:                <ok>
  Cloud resources deleted:          <ok>
  Logs to engagement vault:         <ok>

Verification-loop: ...
```

## References

- **MITRE ATT&CK — Command and Control (TA0011)** — [https://attack.mitre.org/tactics/TA0011/](https://attack.mitre.org/tactics/TA0011/). Sub-techniques as a framework.
- **MITRE D3FEND** — [https://d3fend.mitre.org/](https://d3fend.mitre.org/). Defensive counters.
- **MITRE Adversary Emulation Plans** — [https://github.com/center-for-threat-informed-defense/adversary_emulation_library](https://github.com/center-for-threat-informed-defense/adversary_emulation_library). Threat-emulation templates with concrete C2 requirements.
- **JA3/JA4 fingerprinting** — [https://github.com/FoxIO-LLC/ja4](https://github.com/FoxIO-LLC/ja4). Modern TLS-fingerprint spec; mainstream since 2023.
- **NCSC-NL "Defensive Threat Intelligence" guidance** — [https://www.ncsc.nl/](https://www.ncsc.nl/). NL perspective on C2 detection.
- **SpecterOps blog — C2 OPSEC posts** — [https://specterops.io/blog/](https://specterops.io/blog/). Methodology source for red-team OPSEC.
- **Microsoft TLS-fingerprint research** — [https://techcommunity.microsoft.com/](https://techcommunity.microsoft.com/). Vendor perspective on detection.
- **Center for Threat-Informed Defense — TRAM** — [https://github.com/center-for-threat-informed-defense/tram](https://github.com/center-for-threat-informed-defense/tram). Mapping tooling.
- **NIST SP 800-115 §5** — [https://csrc.nist.gov/pubs/sp/800/115/final](https://csrc.nist.gov/pubs/sp/800/115/final). Methodology context.

## Categories

- pentest
