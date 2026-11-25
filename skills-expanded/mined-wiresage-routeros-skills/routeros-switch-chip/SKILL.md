---
name: routeros-switch-chip
description: Switch chip features and hardware offloading on MikroTik RouterOS 7 (CRS, CCR2xxx, RB5009, hEX, L009 and other models with a switch chip). Covers finding out which chip a model has and what it can do, the /interface/ethernet/switch menus, port mirroring and RSPAN, ingress and egress rate limits, storm control, port isolation (private VLAN), switch rules (ACL) for wire-speed filtering, redirecting, VLAN and VRF actions, port security, hardware QoS on Marvell Prestera (QoS profiles, trust, maps, WRED, ECN, PFC), Layer 3 hardware offloading (L3HW, FastTrack offload, suppress-hw-offload, per-VLAN offload), and the older CRS1xx and CRS2xx VLAN, host and rule tables. Use when a feature must run on the switch chip at wire speed, when offloading stops or traffic bypasses the firewall, when mirroring, limiting or isolating ports, or when configuring CRS switch QoS or hardware routing.
---

# RouterOS switch chip and hardware offloading

A switch chip forwards frames between ports without the CPU. RouterOS drives it through the bridge (`routeros-bridging-switching`: ports,
VLAN filtering, STP) and through `/interface/ethernet/switch` for what a bridge cannot express: mirroring, rate limits, ACL, QoS and
Layer 3 routing. **Traffic that the chip handles never reaches RouterOS**: no firewall, no queues, no sniffer, no torch, no bridge filter
(counters only). A feature that needs the CPU switches the offload off for the traffic it touches.

## Which chip, which features

1. `/interface/ethernet/switch/print` lists the chips with their `TYPE`, `/interface/ethernet/print` shows which port is on which chip, and
   `references/guides/bridging-and-switching/switch-chip-features.md` maps every model to its chip. Ports on a second chip or a management
   port wired to the CPU (for example `ether9` of the CRS312-4C+8XG) cannot be bridged into the hardware path: leave them out.
2. What the chip offers depends on the family:

| Family | Examples | What the guides say it has |
| --- | --- | --- |
| Marvell Prestera 98DX / 98CX | CRS3xx, CRS5xx, CRS8xx, CCR2116, CCR2216 | ACL, port isolation, mirroring and RSPAN, MAC and protocol VLAN, ingress VLAN translation, hardware bonding and MLAG, hardware QoS, L3HW |
| 88E6393X, 88E6191X, 88E6190 | RB5009, L009, CCR2004-16G-2S+ | VLAN filtering offload, rate limits, mirroring; a rule table only on the 88E6393X (up to 256 rules) |
| MT7621, MT7531, RTL8367, EN7523 | hEX, RB4011, RB1100AHx4, hAP ax lite | VLAN filtering offload, rate limits, mirroring, no rule table |
| QCA8337, Atheros8327 / 8316 / 8227 / 7240, ICPlus | RB3011, hAP ac series, RB2011 | VLAN table on most, host and rule tables on some (rule table 32 to 92 rules), rate limit with `bandwidth` on `/interface/ethernet`; the oldest offload plain port switching only |
| QCA-8511, QCA-8519, QCA-8513L | CRS1xx, CRS2xx | VLAN, host and rule tables, trunking, isolation, mirroring; ACL on CRS105, CRS106, CRS112, CRS210, CRS212 and CRS226, not on CRS125 and CRS109 |

3. The CLI pages under `references/cli/interface/ethernet/switch/` carry a `Syscap:` line (`rbswitch`, `crs_prestera`, `musicswitch`) that
   names the switch capability a menu needs, and one menu can have a section per capability: `port-isolation` has `forwarding-override`
   under `rbswitch` and `ports`, `type`, `forwarding-type` and profile arguments under `musicswitch`. Read the section for your device.
4. Chips with a VLAN table in the bridge (88E6393X, 88E6191X, 88E6190, MT7621, MT7531, EN7523, RTL8367, Prestera) are configured with bridge
   VLAN filtering, not with `/interface/ethernet/switch/vlan`. That menu is for the older Atheros / QCA chips.

## Rules that save time

- Prestera devices offload only one bridge (`hw=yes` on the bridge port chooses it); a second bridge runs in software, and with L3HW it can
  cause undefined behavior: use one bridge and VLAN filtering. CRS1xx and CRS2xx can offload several.
- Changing switch rules (add, remove, disable, move) makes the existing rules inactive for a short time: expect brief leakage. Do not
  rely on a rule edit for a security cut-over on a live link.
- IPv4 and IPv6 conditions cannot be in one rule. For IP matches also set `mac-protocol=ip` or `mac-protocol=ipv6`.
- VLAN matchers and actions of a rule (`vlan-id`, `vlan-header`, `new-vlan-id`, `new-vlan-priority`) do nothing unless the bridge has
  `vlan-filtering=yes` and the ports are hardware offloaded. With `ether-type=0x88a8` on the bridge they act on the service tag.
- Every rule counts hits: `/interface/ethernet/switch/rule/print stats`, reset with `reset-counters`.
- Rule slots are limited per model (128 to 1024 on Prestera, see "Models" in `marvell-prestera-switch-chip-features.md`) and shared with
  FastTrack hardware connections. Check `/interface/ethernet/switch/rule/print` after a large change.

## Mirroring

```ros
# Prestera, RouterOS 7.15 or newer: several source ports, directions chosen per port
/interface/ethernet/switch/port set ether2 mirror-ingress=yes mirror-egress=yes
/interface/ethernet/switch set switch1 mirror-target=ether3
# older releases: one source port
/interface/ethernet/switch set switch1 mirror-source=ether2 mirror-target=ether3
# by VLAN, MAC, IP or protocol: a rule with mirror=yes (ingress packets only)
/interface/ethernet/switch/rule add switch=switch1 ports=ether1 vlan-id=11 mirror=yes
# remote analyzer: copies are tagged with the given VLAN and sent to the target port
/interface/ethernet/switch set switch1 mirror-target=ether3 rspan=yes rspan-egress-vlan-id=999 rspan-ingress-vlan-id=999
```

- Source and target must be on the same chip. `mirror-target=cpu` sends the copies to the chip's CPU port. The 88E6393X, 88E6191X and
  88E6190 chips use `mirror-ingress` / `mirror-egress` with `mirror-ingress-target` (port menu) and `mirror-egress-target` (switch menu).
- A device with two chips, both mirroring to the CPU with source ports in one bridge, creates a loop that can lock you out.

## Limits, storm control, isolation

```ros
/interface/ethernet/switch/port set ether1 ingress-rate=10M egress-rate=5M        # ingress policer drops, egress shaper queues first
/interface/ethernet/switch/port set ether1 storm-rate=1 limit-broadcasts=yes limit-unknown-unicasts=yes
/interface/ethernet/switch/port-isolation set ether1 forwarding-override=sfp1     # private VLAN: ether1 may only talk to sfp1
```

- `storm-rate` is a percentage of the link speed (1 on a 1 Gbps port is 10 Mbps). `limit-broadcasts` defaults to `yes`, the other two to `no`.
  On 98DX224S, 98DX226S, 98DX2528 and 98DX3236 chips `egress-rate` and `storm-rate` misbehave on a 10G port linked at 10/100 Mbps or
  1/2.5/5 Gbps, and unknown multicast cannot be told from all multicast.
- On Atheros / QCA chips the per-port limit is `bandwidth` in `/interface/ethernet`; per-flow limits are a rule with `rate=` (the first 32
  rule slots, QCA8337 and Atheros8327 only).
- Isolation works per port, not per VLAN, and only between ports of the same chip. `forwarding-override` affects ingress traffic only. A
  hardware bond is not in the isolation menu: isolate its member ports. RSTP cannot work where several isolated groups exist.
- Port security: allow the MAC with a rule and drop the rest on that port, set `learn=no unknown-unicast-flood=no` on the bridge port, add
  a static `/interface/bridge/host` entry for egress. Broadcast and multicast still leave the port unless `broadcast-flood` and
  `unknown-multicast-flood` are turned off.

## Switch rules (ACL)

Ordered like firewall rules, the first match wins, a rule without an action accepts. Actions: `copy-to-cpu`, `redirect-to-cpu`, `mirror`,
`new-dst-ports` (empty drops), `new-vlan-id`, `new-vlan-priority`, `new-vrf`, `rate`.

```ros
/interface/ethernet/switch/rule
add switch=switch1 ports=sfp-sfpplus1 vlan-id=10 dst-address=10.0.0.0/8 new-dst-ports=""   # guest VLAN: dropped by the chip
add switch=switch1 dst-address=10.0.1.2/32 dst-port=3306 ports=ether1 new-dst-ports=""                  # MySQL server unreachable from ether1
```

An ACL cannot match connection state. For "allow established, drop the rest" keep the rule in the firewall and offload with FastTrack
(below). Use an ACL whenever the match is stateless: one rule covers many connections, while each hardware FastTrack connection uses its own slot.

## Hardware QoS (Prestera)

Needs RouterOS 7.15 or newer for every feature; 7.23 made most settings `auto` and added lossless traffic classes. Marking assigns a QoS
profile from the ingress header, enforcement schedules the eight queues of a port.

```ros
/interface/ethernet/switch/qos/profile add name=voip dscp=46 pcp=5 traffic-class=5
/interface/ethernet/switch/qos/port set ether1 profile=voip                   # profile for ingress traffic on the phone ports
/interface/ethernet/switch/qos/port set sfp-sfpplus1 trust-l3=trust trust-l2=trust   # trunk: believe DSCP and PCP
/interface/ethernet/switch set switch1 qos-hw-offloading=yes
```

Before 7.23 also add `qos/map/ip` and `qos/map/vlan` entries for the profile. WRED, ECN, PFC and lossless buffers exist only on the
larger chips (98DX8xxx, 98DX4xxx, 98DX3255/3257, 98CX8410, 98DX7335); the support table is in `quality-of-service.md`. Watch the
resources with `/interface/ethernet/switch/qos/monitor`. The chip forwards these frames itself, so CPU queues (`routeros-queues`) never
see them.

## Layer 3 hardware offloading (L3HW)

```ros
/interface/ethernet/switch set 0 l3-hw-offloading=yes
/interface/ethernet/switch/port set [find] l3-hw-offloading=yes                  # routed in hardware: both ingress and egress port = yes
/interface/ethernet/switch/port set sfp-sfpplus16 l3-hw-offloading=no            # upstream port: through the CPU, firewall and NAT apply
```

- Port `no` on the egress port sends packets through the CPU; `no` on only the ingress port is unpredictable. Switch `no` turns the
  offload off for everything. Connections that already exist may keep their path.
- **Disable L3HW while changing Layer 2**: bridges, bridge ports, bonds, VLANs, MTU / L2MTU and MAC addresses. Set it back to `yes` last.
  MTU: the chip holds eight MTU profiles (1500 and seven more).
- Inter-VLAN routing in hardware needs the VLAN interface on a **hardware-offloaded, vlan-filtering bridge** and the bridge itself as a
  tagged member of the VLAN. A VLAN interface created directly on a port or bond is not offloaded and can bypass the CPU (the 98DX7xxx is the
  exception); then set `l3-hw-offloading=no` on those ports. `/interface/vlan` also has a per-VLAN `l3-hw-offloading`.
- A route's `H` flag means eligible, not offloaded. `suppress-hw-offload=yes` on a route, or `set suppress-hw-offload yes` in a routing
  filter, keeps it on the CPU.
- FastTrack: `action=fasttrack-connection ... hw-offload=yes` offloads a connection, and the number of hardware connections is small. Slow-path
  features (bridge `use-ip-firewall`, bridge filter or NAT rules, sniffer, torch) disable FastPath and with it the offload.
- An ACL with `redirect-to-cpu=yes` on a port stops L3HW for that traffic. MAC-Telnet does not reach the CPU on 98DX8xxx, 98DX4xxx and 98DX325x
  with L3HW unless a rule redirects UDP port 20561 to the CPU.
- 98DX2xxx / 98DX3xxx: only the last octet of an interface MAC may differ, so ports, bridge and VLAN interfaces used for routing share the
  other five. Feature support per chip (VRF, FastTrack NAT, route limits) is in `l3-hardware-offloading.md`.

## Older chips (CRS1xx, CRS2xx, Atheros, QCA)

The tables `/interface/ethernet/switch/port` (`vlan-mode`, `vlan-header`, `default-vlan-id`), `vlan`, `host` and `rule`. On QCA8337 and Atheros8327
keep `vlan-header=leave-as-is` and set `default-vlan-id` on access ports. `references/guides/bridging-and-switching/user-guides/crs1xx-2xx-series-switches-examples.md`
has VLAN, Q-in-Q, mirroring, trunking, isolation, QoS and bandwidth examples. Port switching itself is bridge-based since v6.41.

## Where to look

| Need | Open |
| --- | --- |
| Model to chip, features per chip, mirroring, isolation, rule table of older chips | `references/guides/bridging-and-switching/switch-chip-features.md` |
| Prestera: models, ACL, shaping, storm control, port security, bonding, dual boot | `references/guides/bridging-and-switching/marvell-prestera-switch-chip-features.md` |
| Hardware routing: setup, examples, mistakes, per-chip support | `references/guides/bridging-and-switching/l3-hardware-offloading.md` |
| QoS marking and enforcement, Dante, RoCE, WRED, ECN, PFC | `references/guides/bridging-and-switching/quality-of-service.md` |
| CRS1xx / CRS2xx configuration examples | `references/guides/bridging-and-switching/user-guides/crs1xx-2xx-series-switches-examples.md` |
| Properties of every switch menu | `references/cli/interface/ethernet/switch.md` and `references/cli/interface/ethernet/switch/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-bridging-switching` (bridge, VLAN filtering, STP, IGMP snooping; start there for any VLAN setup),
`routeros-high-availability` (bonding, MLAG), `routeros-ethernet` (ports, MTU), `routeros-firewall` (FastTrack, `hw-offload`),
`routeros-queues` (CPU queues), `routeros-hardware` (models, PoE).
