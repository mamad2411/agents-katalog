---
name: cisco-ios-router-troubleshooting
description: "Evidence-driven troubleshooting for Cisco IOS and IOS XE router support bundles, tarballs, show command transcripts, show tech output, syslog/debug logs, running configs, crashinfo, routing tables, interface counters, and packet captures. Use when diagnosing Cisco router issues involving reachability, routing protocols such as OSPF/EIGRP/BGP, interfaces, ACL/NAT/policy, CPU/memory, reloads, tracebacks, or configuration-change correlation."
---

# Cisco IOS Router Troubleshooting

## Mission

Troubleshoot Cisco IOS router evidence like a senior network escalation engineer. Preserve customer artifacts, start broad, maintain competing hypotheses, correlate across layers, and separate directly observed facts from inferences and unknowns.

## Intake

1. Treat the customer's `data/` directory and uploaded tarballs as read-only evidence.
2. List all supplied files, sizes, timestamps, and archive types before deep analysis.
3. Extract archives into scratch space such as `work/<bundle-name>/`, preserving directory structure. Unpack nested archives into that scratch tree.
4. Build a quick inventory of logs, `show` outputs, configs, `show tech`, crashinfo, core/traceback files, packet captures, topology notes, and README/index files.
5. Identify device names from filenames, prompts, `hostname`, `show version`, syslog hostnames, or collector metadata. If device identity is inferred, label it as an inference.
6. Read summaries, manifests, README files, TAC notes, and collection indexes before raw logs.

## Useful Tool Choices

Prefer simple read-only tools first: `rg`, `find`/`Get-ChildItem`, `tar -tf`, `tar -xf` into scratch, `file` where available, `jq`, `yq`, `awk`, and `sed`.

When installed and appropriate:

- Use Cisco pyATS/Genie parsers for structured parsing of supported `show` command output.
- Use TextFSM/ntc-templates for command outputs that are not handled by Genie.
- Use ciscoconfparse or similar structured config parsers for IOS-style configuration queries.
- Use packet-analysis tools for `.pcap`/`.pcapng` only after determining the relevant hosts, protocols, and time window.

If a parser fails, keep the raw text as the source of truth and note the parser limitation.

## Artifact Classification

For every major file, decide which category it belongs to:

- Syslog/debug log: IOS messages like `%LINK`, `%LINEPROTO`, `%OSPF`, `%BGP`, `%SYS`, `IP: s=... d=...`, tracebacks, or debug output.
- Command transcript: prompts and echoed commands such as `Router#show version`, `show ip route`, or `show interfaces`.
- Show tech/support bundle: one large file containing many command sections.
- Configuration: `running-config`, `startup-config`, `show archive config differences`, or extracted config blocks.
- State/counters: interface, routing, neighbor, CPU, memory, platform, environmental, and queue outputs.
- Crash/reload evidence: `show version`, `show stacks`, `show context`, crashinfo, tracebacks, reload reasons, core files.
- Capture/topology data: pcap files, diagrams, addressing tables, traceroute/ping outputs.

Do not assume a tarball has command output just because filenames say "log"; sample bundles may contain only syslog/debug streams.

## Broad First Pass

Run broad searches before focusing on one theory. Useful IOS keyword groups:

```text
%[A-Z0-9_-]+-[0-3]-|traceback|crash|reload|bus error|segv|software-forced|watchdog|malloc|memory|CPUHOG
CONFIG_I|PARSER|archive|AAA|LOGIN|SEC|SNMP|NTP|clock|certificate|PKI|x509
LINK|LINEPROTO|BFD|UDLD|ERRDISABLE|CRC|input error|output error|drops|overrun|ignored|throttle|carrier
OSPF|EIGRP|BGP|LDP|PIM|HSRP|VRRP|GLBP|adjacency|neighbor|dead timer|hold time|reset|flap
unreachable|unroutable|encapsulation failed|redirect|fragment|MTU|CEF|punt|drop|ACL|NAT|ZBFW|uRPF
```

Capture context around hits, not isolated lines. Identify repeated noisy streams and summarize their pattern so they do not hide sparse high-signal events.

## Command Section Handling

For transcripts or `show tech`:

1. Split sections by prompt/command boundaries when possible.
2. Record the command, device, source file, and line range for each important section.
3. Prefer direct command evidence over inferred state from logs.
4. If command echoing is absent, infer sections cautiously from headings and output shape.

High-value baseline sections:

- `show version`, `show inventory`, `show module`, `show platform`, `show license`
- `show running-config`, `show startup-config`, `show archive config differences`
- `show logging`, `show clock`, `show ntp status`
- `show interfaces`, `show ip interface brief`, `show controllers`
- `show ip route`, `show ip cef`, `show arp`, `show adjacency`
- `show ip ospf neighbor`, `show ip ospf interface`, `show ip protocols`
- `show ip bgp summary`, `show bgp`, `show tcp brief`
- `show processes cpu`, `show processes memory`, `show memory statistics`
- `show access-lists`, `show ip nat translations/statistics`, firewall/policy outputs

## Hypothesis Loop

After the first pass, maintain 2-5 competing hypotheses. Use this table shape in notes and final output when useful:

| ID | Hypothesis | Status | Confidence | Supporting evidence | Refuting evidence | Next check |
| --- | --- | --- | --- | --- | --- | --- |

Allowed statuses: `Open`, `Strengthening`, `Weakening`, `Rejected`, `Confirmed`.

For each hypothesis, actively seek both support and refutation. Stop when one hypothesis explains the symptoms materially better than alternatives and the evidence is consistent across logs, state, config, and timeline.

## IOS-Specific Lenses

### Interface And Physical Layer

Distinguish:

- `administratively down`: configured shutdown or parent dependency, often change-driven.
- `line protocol down`: L2/keepalive/encapsulation problem or remote side down.
- Physical down: cable, optics, carrier, transceiver, speed/duplex, port-channel member, or provider circuit.

Correlate `LINK`/`LINEPROTO` events with interface counters, `show controllers`, config changes, routing neighbor changes, and reachability tests. CRC/input errors plus drops plus adjacency flaps are stronger than any single counter.

### Routing Protocols

For OSPF:

- `Neighbor Down: Interface down or detached` points toward local interface state or configured shutdown at that moment.
- `Neighbor Down: Dead timer expired` means Hellos were not received in time; causes include link loss, congestion, filtering, CPU starvation, mismatched timers/network type, one-way reachability, or neighbor process failure.
- Check area, network type, hello/dead timers, passive-interface, MTU, authentication, duplicate router ID, ACL multicast filtering, and adjacency state history.

For BGP:

- Separate TCP/session issues from policy/prefix issues.
- Check neighbor state, reset reason, source interface/update-source, route to peer, TTL/eBGP multihop, MD5/auth, ACL/firewall, AS number, route-maps, prefix-lists, max-prefix, and next-hop reachability.

For EIGRP:

- Check K-values, AS number, authentication, passive interfaces, hold timers, SIA messages, stub behavior, route filtering, and interface multicast reachability.

### Reachability And Forwarding

Correlate ping/traceroute/debug evidence with RIB, CEF, ARP, ACL/NAT/policy, VRF, and MTU. `IP: ... unroutable` in debug output is evidence of a missing or unusable route for that destination at that router, not automatically the root cause.

For asymmetric or intermittent issues, check policy routing, recursive next hops, FHRP state, ECMP, NAT translations, return path, and control-plane policing.

### Configuration Change Correlation

Treat `%SYS-5-CONFIG_I` as a change marker, not a failure. Correlate it with nearby state transitions, archive diffs, AAA user/source, and running config. If a config message precedes an adjacency or interface event by seconds, treat change-induced outage as a strong hypothesis but still seek the exact changed stanza.

### Device Health And Software

Tracebacks, `%SYS` severity 0-3, watchdog, crashinfo, bus errors, malloc failures, and reload reasons can indicate software defect or platform instability. Confirm with IOS version, uptime, reload reason, matching crashinfo, recurrence, and whether data-plane symptoms align in time. Do not call a traceback the root cause if it is isolated and unrelated to the symptom window.

High CPU or memory is causal only when timing and process evidence match the symptom, such as OSPF dead timers expiring during CPU starvation.

### Debug Logs

IOS debug output can dominate a bundle. Collapse repeated flows by `(source, destination, interface, message type, time range)`. Do not treat every `rcvd`, `sending`, `packet consumed`, or `stop process pak for forus packet` line as an error. Prioritize unusual debug outcomes such as `unroutable`, `encapsulation failed`, ACL deny/drop, ICMP unreachable, TTL exceeded, fragmentation, or missing expected reverse traffic.

## Evidence Standards

Every important claim should cite concrete evidence:

- File path and line number, or command section and source file.
- A concise excerpt or summary of the relevant lines.
- Why the evidence matters.

Use labels:

- **Fact**: directly observed in evidence.
- **Inference**: reasoned from one or more facts.
- **Unknown**: missing, ambiguous, or inconclusive evidence.

Avoid exposing secrets from configs. Redact passwords, keys, SNMP communities, TACACS/RADIUS secrets, certificates/private keys, and customer-sensitive addresses when they are not necessary to the conclusion.

## Timeline Rules

Build a timeline from the earliest high-signal event through recovery or collection end.

- Normalize timestamps when multiple devices are present.
- IOS logs often omit year and timezone; infer year only from file metadata or external context and label that inference.
- Account for clock skew, uptime-based timestamps, local timezone, and collector timestamps.
- Put config changes, interface transitions, routing neighbor changes, reachability failures, CPU/memory events, tracebacks, and reloads on the same timeline.

## Output

Lead with the answer, then show evidence. Prefer a few strong findings over a long list of weak clues.

Use this final shape unless the user requests otherwise:

1. **Executive Summary**: most likely issue, scope/impact, confidence.
2. **Current Hypotheses**: statuses and why each strengthened, weakened, or remains open.
3. **Strongest Evidence**: supporting and refuting evidence with paths/lines or command sections.
4. **Timeline**: ordered key events with timestamp assumptions.
5. **Conclusion**: confirmed root cause if justified; otherwise most likely cause and remaining uncertainty.
6. **Next Actions**: safest remediation or exact additional evidence needed.

If evidence is insufficient, say so early and specify the missing discriminator, such as adjacent router logs, `show run` around the interface/protocol, `show ip route` at failure time, CPU history, interface counters before/after, packet capture, or archive config diff.

## Safety

Do not recommend disruptive live commands casually. Prefer show commands and offline analysis. Mention that IOS debugs can be CPU-intensive and should be scoped/conditional on production devices. Do not suggest reloads, clears, shutdown/no-shutdown, routing resets, or config changes unless evidence supports them and safer checks are exhausted.
