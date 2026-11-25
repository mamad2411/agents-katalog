---
name: routeros-bgp
description: Configuring BGP on MikroTik RouterOS 7. Covers instances, connections, templates and sessions, eBGP and iBGP, route reflectors and dynamic peers, multihop and BGP unnumbered, advertising networks with address lists, input and output filter chains and accept-nlri, communities, next-hop handling, RFC 9234 roles for route-leak prevention, RPKI origin validation, BFD, monitoring advertisements, and EVPN and L3VPN pointers. Use when peering with a provider or IXP, building an iBGP full mesh or route-reflector setup, filtering or advertising prefixes, validating origins, or when a session will not establish or routes are missing.
---

# RouterOS BGP

BGP in v7 is redesigned around four menus:

| Menu | Role |
| --- | --- |
| `/routing/bgp/instance` | The BGP process: `as` and `router-id`. Every connection belongs to one instance, and best-path selection only compares routes received by the same instance |
| `/routing/bgp/template` | Protocol parameters (AS, input and output sections, filters). Inherited by connections (`templates=`) and used for dynamic peers. The built-in `default` template needs your own AS if you use it: `/routing/bgp/template/set default as=65531` |
| `/routing/bgp/connection` | One peer (or a listening subnet): `instance`, `remote.address`, `local.role`, `connect`, `listen`, plus any template parameter |
| `/routing/bgp/session` | Read-only state of established, pending and recently dropped sessions (cache survives a flap to avoid route churn) |

Template parameters are also exposed on the connection, so a template is optional for simple setups. Parameters are grouped by direction:
`input.*`, `output.*`, `local.*`, `remote.*`. The global router ID comes from `/routing/id` (default: highest interface address).

## A first session

```ros
# Router1, AS 65531
/routing/bgp/instance/add name=inst1 as=65531
/routing/bgp/connection/add name=toR2 instance=inst1 remote.address=192.0.2.2 local.role=ebgp output.network=bgp-nets
# Router2, AS 65532
/routing/bgp/instance/add name=inst1 as=65532
/routing/bgp/connection/add name=toR1 instance=inst1 remote.address=192.0.2.1 local.role=ebgp output.network=bgp-nets
/routing/bgp/session/print
```

- `local.role` is mandatory: `ebgp`, `ibgp`, `ibgp-rr`, or an RFC 9234 role (below). The remote AS is learned from the OPEN message; set
  `remote.as` only to accept a specific AS.
- eBGP to a peer that is not on a connected network fails unless `multihop=yes`; then set `local.address` (the old `update-source`).
  Without it BGP picks an address (highest loopback, else highest address; for a connected eBGP peer the address on that network).
- iBGP is multihop by default and normally runs between loopbacks over an IGP (`routeros-ospf`). A route learned from an iBGP peer is not
  passed to another iBGP peer (split horizon): use a full mesh or a route reflector (`local.role=ibgp-rr` on the reflector; clients peer
  only with it; ORIGINATOR_ID and CLUSTER_LIST prevent loops).
- `input.allow-as` relaxes AS-path loop prevention (needed for some MPLS L3VPN CE setups); `nexthop-choice=propagate` keeps the
  original next hop (EVPN overlays).
- Listening on a subnet (`listen=yes` with a prefix as `remote.address`, for dynamic peers) exposes a DoS surface; protect it with the firewall.
- BGP unnumbered: empty `remote.address` and `local.address` set to an interface; one connection per interface, IPv6 link-local discovery.
- Sessions that never start leave no session entry: a TCP block (firewall, MD5 mismatch) shows nothing in `/routing/bgp/session`. Check
  the log (`/log/print where topics~"bgp"`) and that TCP 179 is accepted in `input`.

## Advertising networks

There is no `network` menu: put prefixes in an address list, make sure the prefix exists in the routing table (a blackhole route is the
usual anchor), and reference the list from the connection. BGP only advertises prefixes that are present in the routing table; synchronisation
with IGP routes cannot be turned off.

```ros
/ip/firewall/address-list/add list=bgp-nets address=198.51.100.0/24
/ip/route/add dst-address=198.51.100.0/24 blackhole
/routing/bgp/connection/set toR2 output.network=bgp-nets          # or output.network-blackhole=yes to auto-create the route
```

## Filters

Filters are routing filter chains (`routeros-routing`). The **default action of a chain is reject**. If no output chain is set, BGP
advertises every active route it can find: always set `output.filter-chain` on external sessions.

```ros
/routing/filter/rule/add chain=bgp_in rule="if (dst in 192.168.0.0/16) { accept }"
/routing/filter/rule/add chain=bgp_in rule="set bgp-local-pref -1; accept"
/routing/bgp/connection/set toR2 input.filter=bgp_in output.filter-chain=bgp_out
```

`input.accept-nlri=<address-list>` (and other `input.accept-*`) drops unwanted prefixes before they are parsed and stored, saving memory;
a normal input filter only rejects, so the route stays visible as "not active, filtered". Use `bgp-med`, `bgp-local-pref`,
`bgp-path-prepend`, communities and large communities in rules; `bgp-out-med` belongs in the eBGP output chain.

## Route leaks and RPKI

- **RFC 9234 roles** protect transit relationships: use `ebgp-provider` / `ebgp-customer`, `ebgp-rs` / `ebgp-rs-client`, `ebgp-peer`. The router
  sends the Role capability in OPEN and ends the session with Role Mismatch (OPEN error subcode 8) if the pair is wrong. `ebgp`, `ibgp`
  and `ibgp-rr` do not negotiate roles.
- **RPKI**: `/routing/rpki/add group=rpki address=192.0.2.10 port=8282` connects to an RTR validator; then in a filter
  `rpki-verify rpki` followed by `if (rpki invalid) { reject } else { accept }`. States: `valid`, `invalid`, `unknown`, `unverified`.
  Test one prefix with `/routing/rpki/rpki-check group=rpki prfx=... origin-as=...`.

## Operation and troubleshooting

1. `/routing/bgp/session/print` (flag `E` = established, `.capabilities`, `.messages`, `last-notification`).
2. Output advertisements are not recorded by default. Set `output.keep-sent-attributes=yes`, then
   `/routing/bgp/session/dump-saved-advertisements 0 save-to=out.pcap`.
3. Per-process load: `/routing/stats/process/print interval=1`. BGP input and output can be pinned with `input.affinity` and
   `output.affinity` (`alone`, `afi`, `instance`, `vrf`, `remote-as`, `main`).
4. Big tables need memory: check `/system/resource/print` and use `accept-nlri` and filters. Long-lived sessions across BFD:
   `use-bfd=yes` on the connection.
5. Limits: `input.limit-process-routes-ipv4` and `-ipv6` protect the router from a peer that sends too much.

## Where to look

| Need | Open |
| --- | --- |
| Session types, local address selection, unnumbered, dynamic peers | `references/guides/user-guides/routing-and-networking-protocols/unicast/bgp/peering-sessions.md` |
| Protocol basics, attributes, best-path selection | `.../unicast/bgp/understanding-bgp.md` |
| Next-hop handling | `.../unicast/bgp/nexthop-selection.md` |
| Roles and route-leak prevention | `.../unicast/bgp/route-leak-prevention.md` |
| RPKI | `.../unicast/rpki.md` |
| EVPN (L2 and L3 overlays) | `.../unicast/evpn.md` |
| FAQ | `.../unicast/bgp/faq.md` |
| Properties of `/routing/bgp/*` and `/routing/rpki/*` | `references/cli/routing/bgp/`, `references/cli/routing/rpki/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-routing` (filters, tables, BFD, v6 migration), `routeros-ospf` (IGP for iBGP), `routeros-mpls`
(L3VPN, VPNv4), `routeros-firewall` (TCP 179), `routeros-ipsec` (protecting sessions).
