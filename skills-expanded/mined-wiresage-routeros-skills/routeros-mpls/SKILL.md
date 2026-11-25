---
name: routeros-mpls
description: MPLS on MikroTik RouterOS 7. Covers label switching and penultimate hop popping, prerequisites (loopback LSR ID, IGP reachability), LDP setup for IPv4, IPv6 and dual stack, label binding filters, MPLS MTU and TTL propagation, traceroute through an MPLS cloud, VPLS pseudowires (LDP signalled, static Cisco style, BGP signalled), MP-BGP L3VPN and VRF pointers, RSVP-TE traffic engineering tunnels, and EXP bits for queuing. Use when building or debugging an MPLS backbone, configuring LDP or VPLS between sites, sizing MPLS MTU, or when labelled traffic is dropped or traceroute is misleading.
---

# RouterOS MPLS

MPLS forwards by labels instead of IP lookups. Because packets in the cloud are switched on labels, network-layer features (NAT, IP
filtering) do not apply to them there: apply those at the ingress or egress router, ingress preferably. It is not supported on SMIPS devices
(hAP lite, hAP lite TC, hAP mini). Plan the design before configuring; the manual recommends solid MPLS knowledge before production use.

## Prerequisites, then LDP

1. A loopback address on every router (a bridge without ports, commonly named `lo`), used as the LSR ID and LDP transport address.
2. IP reachability between loopbacks from an IGP (`routeros-ospf` or IS-IS in `routeros-routing`); LDP follows the routing table, so a
   labelled packet takes the path an unlabelled one would.
3. Enable LDP only on core-facing interfaces, not on customer-facing ones.

```ros
/interface/bridge/add name=lo
/ip/address/add address=10.255.255.1/32 interface=lo
/mpls/ldp/add afi=ip lsr-id=10.255.255.1 transport-addresses=10.255.255.1
/mpls/ldp/interface/add interface=ether2
/mpls/ldp/neighbor/print
/mpls/forwarding-table/print
```

- `transport-addresses` makes the router originate sessions from, and advertise, that address. Without a reachable loopback route on the
  peer the session does not come up.
- For IPv6 or dual stack set `afi=ip,ipv6` (and `preferred-afi`) on the LDP instance and interface.
- Reduce label state with `/mpls/ldp/accept-filter` and `advertise-filter` (for example, labels only for loopback /32 routes).
- Explicit null (`use-explicit-null`), default-route labels (`distribute-for-default`) and loop detection are instance options.

## MTU and TTL

An MPLS packet is larger than the IP packet by the label stack. When the path has hops with different MTUs, set `mpls-mtu` in
`/mpls/interface` to the smallest value that every hop can carry (path MTU plus label size), otherwise packets are silently dropped on
hops that cannot carry them. Make sure the underlying interface MTU and L2 MTU allow it. `/mpls/settings` has `dynamic-label-range` (exclude statically assigned labels), `propagate-ttl`
(default yes; `no` hides the MPLS hops from traceroute) and `allow-fast-path`. Details: `references/help/mpls-mtu-forwarding-and-label-bindings.md`.

## Troubleshooting with traceroute

RFC 4950 lets traceroute show the label stack (`<MPLS:L=19,E=0>`). ICMP errors generated inside the cloud are label-switched towards
the far end of the LSP, so if an LSP is broken in the middle, traceroute stops answering and cannot show where; check `/mpls/ldp/neighbor`,
`/mpls/ldp/local-mapping`, `/mpls/ldp/remote-mapping` and `/mpls/forwarding-table` hop by hop instead.

## VPLS (Layer 2 over MPLS)

A VPLS interface is a transparent Ethernet tunnel like EoIP, normally added to a bridge. Two labels are pushed: tunnel and transport.
Both ends exchange labels with LDP signalling or, in larger designs, BGP autodiscovery and signalling. A working label distribution
(LDP, RSVP-TE or static bindings) must exist first.

```ros
/interface/vpls/add name=vpls-to-r3 peer=10.255.255.3 vpls-id=100:1 disabled=no
/interface/bridge/port/add bridge=customerA interface=vpls-to-r3
```

Other options: `cisco-static-id` for static Cisco-style pseudowires, `pw-type`, `pw-control-word` (see `vpls/control-word.md`), and
BGP-signalled VPLS through `/routing/bgp/vpls` (needs iBGP, preferably with route reflectors; `routeros-bgp`).

## L3VPN and traffic engineering

MP-BGP VPNv4/VPNv6 over MPLS uses VRFs (`routeros-routing`) and route distinguishers and targets (the "Route Distinguisher and Route Target" page in `routeros-routing`);
the BGP side is `/routing/bgp/vpn` (`routeros-bgp`). RSVP-TE tunnels (explicit paths, CSPF, OSPF TE extensions, bandwidth reservation)
are under `/mpls/traffic-eng` (`traffic-eng.md`). EXP bits can map to queue priorities (`exp-bit-and-mpls-queuing.md`, `routeros-queues`).

## Where to look

| Need | Open |
| --- | --- |
| Overview and supported features | `references/guides/user-guides/routing-and-networking-protocols/mpls.md` |
| LDP prerequisites, setup, filters, traceroute, IPv6 | `.../mpls/ldp.md` |
| VPLS | `.../mpls/vpls.md`, `.../mpls/vpls/control-word.md` |
| Traffic engineering, EXP bit queuing | `.../mpls/traffic-eng.md`, `.../mpls/exp-bit-and-mpls-queuing.md` |
| MPLS MTU, label range, TTL | `references/help/mpls-mtu-forwarding-and-label-bindings.md` |
| Properties of `/mpls/*` and `/interface/vpls` | `references/cli/mpls/`, `references/cli/interface/vpls.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ospf`, `routeros-routing` (VRF, IS-IS), `routeros-bgp` (VPNv4, BGP VPLS), `routeros-queues`,
`routeros-bridging-switching` (bridges for VPLS ports), `routeros-vpn` (EoIP alternative).
