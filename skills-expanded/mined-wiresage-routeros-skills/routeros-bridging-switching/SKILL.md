---
name: routeros-bridging-switching
description: Layer 2 on MikroTik RouterOS 7. Covers bridges and bridge ports, bridge VLAN filtering (trunk, access and hybrid ports, PVID, frame types, the bridge VLAN table, management VLAN access), VLAN interfaces and inter-VLAN routing, QinQ, STP, RSTP and MSTP, loop protect, IGMP and MLD snooping, DHCP snooping, ARP inspection and RA guard, bridge hardware offloading and which bridge features break it, VXLAN, MACVLAN, MACsec, bridge firewall, and SwOS pointers. Use when building or changing a bridge or VLAN setup, turning a router into a switch, debugging VLAN traffic, loops or lost management access, or choosing between software and hardware-offloaded bridging. Switch chip features (mirroring, ACL, QoS, hardware routing) are in routeros-switch-chip.
---

# RouterOS bridging, VLAN and switching

A bridge joins ports into one Layer 2 segment. With `vlan-filtering=yes` it behaves like a managed switch (VLAN-aware, independent VLAN
learning). The most expensive mistake in this area is **enabling VLAN filtering before the VLAN table and the management path exist**,
which locks you out. Build the configuration with filtering off, then switch it on last.

## VLAN filtering: the order that works

```ros
/interface/bridge/add name=bridge1 vlan-filtering=no
/interface/bridge/port/add bridge=bridge1 interface=ether2 frame-types=admit-only-vlan-tagged                           # trunk
/interface/bridge/port/add bridge=bridge1 interface=ether6 pvid=200 frame-types=admit-only-untagged-and-priority-tagged  # access
/interface/bridge/port/add bridge=bridge1 interface=ether7 pvid=300 frame-types=admit-only-untagged-and-priority-tagged
/interface/bridge/vlan/add bridge=bridge1 tagged=ether2 vlan-ids=200
/interface/bridge/vlan/add bridge=bridge1 tagged=ether2 vlan-ids=300
# management access, tagged on VLAN 99: the bridge itself must be a tagged member so the VLAN interface reaches the CPU
/interface/vlan/add name=MGMT interface=bridge1 vlan-id=99
/ip/address/add address=192.168.99.1/24 interface=MGMT
/interface/bridge/vlan/add bridge=bridge1 tagged=bridge1,ether2 vlan-ids=99
/interface/bridge/set bridge1 vlan-filtering=yes                  # last step
```

- `pvid` assigns untagged ingress traffic to a VLAN. `frame-types` and `ingress-filtering` (default yes in v7) decide what a port
  accepts. Ports with `admit-all` or `admit-only-untagged-and-priority-tagged` become untagged members of their PVID automatically;
  list only tagged ports in the table for those VLANs.
- Use a list of VLAN IDs (`vlan-ids=100-115,120`) only for **tagged** entries. On access ports a multi-VLAN entry can leak tagged
  frames out of the wrong port.
- Every VLAN that must be switched needs a table entry; ingress filtering drops VLANs that are not in it. A VLAN interface on the
  bridge is added to the table automatically as tagged from v7.16.
- Inter-VLAN routing by the bridge: VLAN interfaces on `bridge1` with addresses, the bridge as tagged member of each VLAN, and
  firewall rules (`routeros-firewall`). Allowing a VLAN to reach the CPU also allows it to reach the router's services: filter it.
- Set the optional `frame-types=admit-only-vlan-tagged` on the bridge itself to refuse untagged traffic and the default VLAN 1.
- QinQ and tag stacking (`ether-type=0x88a8`, `tag-stacking`) and MVRP are in the VLAN-filtering section of the bridge guide.
- Check: `/interface/bridge/vlan/print`, `/interface/bridge/host/print where !local`, `/interface/bridge/port/print`.
- Changing `vlan-filtering`, `protocol-mode`, IGMP snooping, DHCP snooping, L2MTU or flow control on a bridge that uses the switch chip
  can reset the chip and drop all Ethernet ports for a moment. Do it in a maintenance window and with a way back (`routeros-fundamentals`).

## Hardware offloading

Bridge ports on a device with a switch chip forward at wire speed when the bridge is offloaded (`H` flag on the port). Hardware-forwarded
frames never reach RouterOS (counters only). Only one bridge per switch chip is offloaded (CRS1xx/2xx support several; choose with `hw=yes|no`
on the bridge port). Chips with Marvell Prestera, RTL8367, 88E6393X/88E6191X/88E6190, MT7621, MT7531 and EN7523 can offload VLAN filtering
(since v7); other devices lose offloading when VLAN filtering is on and should use the VLAN-interface method of the "Basic VLAN switching" guide.
Which bridge features break offloading per chip is tabulated in the bridge guide. What the chip can do beyond forwarding (port mirroring,
rate limits and storm control, port isolation, switch rules, hardware QoS, Layer 3 hardware offloading, the CRS1xx / CRS2xx tables) is the
subject of `routeros-switch-chip`.

## Loops, STP and protection

- Default `protocol-mode=rstp`. Use MSTP for per-VLAN topologies (needs VLAN filtering). Set bridge `priority` so the intended root wins.
  RSTP/STP BPDUs and VLAN-interface bridging interact badly; prefer VLAN filtering. A dot1x server on a bridge port needs RSTP/MSTP.
- Loop Protect (`user-guides/loop-protect.md`) disables a port that sees its own frames. `user-guides/layer2-misconfiguration.md` lists typical mistakes.
- IGMP/MLD snooping stops multicast flooding (`igmp-snooping=yes`, a querier on the segment). DHCP snooping, ARP inspection, IP source guard,
  DHCPv6 shield and RA guard mark ports trusted or untrusted; enabling DHCP snooping turns off bridge fast path.
- The bridge firewall (`/interface/bridge/filter`, `/interface/bridge/nat`) filters frames; IP firewall on bridged traffic needs
  `use-ip-firewall` (and `use-ip-firewall-for-vlan` for VLAN-tagged frames) in `/interface/bridge/settings`.

## Other Layer 2 features

- **VXLAN** (`/interface/vxlan`): 24-bit VNI overlay over IP/UDP, point-to-multipoint via VTEPs, 50 bytes of overhead for IPv4 and 70 for
  IPv6, so lower the MTU or raise the underlay MTU. Add the VXLAN interface to a bridge to stretch a VLAN. EVPN control plane: `routeros-bgp`.
- **MACVLAN**: extra virtual interfaces with their own MAC address on one parent. **MACsec** (`/interface/macsec`): Ethernet link encryption
  between two devices.
- **SwOS / SwOS Lite** are separate operating systems for some switches, configured only through a browser; the manual has per-family
  pages (`swos/crs3.md`, `css106.md`, `css610.md`, `gpen21.md`) and a page on SwOS upgrade failure. Their commands do not exist in RouterOS.
- **Controller Bridge and Port Extender** (help-only page `references/help/controller-bridge-and-port-extender.md`): a controller bridge
  managing port extender devices.
- Wireless in a bridge: `routeros-wireless` (VLANs on wireless, CAPsMAN with VLANs).

## Where to look

| Need | Open |
| --- | --- |
| Bridge settings, ports, STP, hosts, multicast, VLAN filtering, snooping, bridge firewall | `references/guides/bridging-and-switching.md` |
| Step-by-step VLAN cases | `references/guides/bridging-and-switching/user-guides/` (`basic-vlan-switching.md`, `bridge-vlan-table.md`, `wireless-vlan-trunk.md`, ...) |
| Switch chip features, ACL, switch QoS, L3 hardware offloading, CRS tables | the skill `routeros-switch-chip` |
| VLAN interfaces | `references/guides/bridging-and-switching/vlan.md` |
| Properties | `references/cli/interface/bridge/`, `references/cli/interface/vlan.md`, `references/cli/interface/vxlan.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-switch-chip` (switch chip, ACL, QoS, hardware routing), `routeros-ethernet` (ports, interface lists), `routeros-wireless`, `routeros-firewall`, `routeros-vpn` (EoIP, L2TP-Ether),
`routeros-high-availability` (bonding, MLAG), `routeros-queues`, `routeros-dhcp` (relay and snooping).
