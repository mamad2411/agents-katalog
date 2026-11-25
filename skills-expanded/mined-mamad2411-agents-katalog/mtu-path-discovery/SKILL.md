# Skill: MTU and Path MTU Discovery (ntsh_mtu-path-discovery)

Diagnose and resolve MTU-related network issues including path MTU discovery failures, fragmentation problems, MSS clamping, and MTU black holes.

---

## Path MTU Discovery (PMTUD)

### How PMTUD Works
1. Sender sets the Don't Fragment (DF) bit in the IP header and sends a full-size packet (typically 1500 bytes).
2. If a router along the path has a smaller MTU, it drops the packet and returns an ICMP "Destination Unreachable — Fragmentation Needed" (Type 3, Code 4) message containing the next-hop MTU.
3. Sender reduces packet size to the reported MTU and retransmits.
4. Process repeats until the packet reaches the destination or no more ICMP errors are received.

### Why PMTUD Fails
- **Firewall blocking ICMP**: If any device in the path blocks ICMP Type 3 Code 4 messages, the sender never learns about the smaller MTU. Packets are silently dropped — creating an **MTU black hole**.
- **ICMP rate limiting**: Some routers rate-limit ICMP responses, causing intermittent PMTUD failures under load.
- **Asymmetric paths**: ICMP "need to fragment" messages may follow a different return path and get filtered by a different firewall.

---

## Common MTU Values

| Path / Environment | MTU (bytes) | Notes |
|--------------------|-------------|-------|
| Standard Ethernet | 1500 | Default for most networks |
| IPsec VPN (ESP + tunnel mode) | 1400–1422 | Depends on encryption algorithm and mode |
| GRE tunnel | 1476 | 24 bytes GRE overhead |
| GRE + IPsec | 1360–1400 | Combined overhead |
| VXLAN overlay | 1450 | 50 bytes VXLAN overhead |
| PPPoE (DSL) | 1492 | 8 bytes PPPoE overhead |
| Azure VNet (standard) | 1500 | Within VNet and across peering |
| Azure accelerated networking | 8900 | Jumbo frames for intra-VNet VM-to-VM |
| AWS VPC (default) | 9001 | Jumbo frames supported within VPC |
| AWS VPN tunnel | 1399 | AWS-specific VPN overhead |
| GCP VPC (default) | 1460 | GCP default MTU |
| GCP VPC (configurable) | Up to 8896 | Per-VPC MTU setting |

---

## Diagnosing MTU Issues

### Symptoms
- Large file transfers stall or fail, while small transfers (< 1400 bytes) work.
- SSH connections establish (small packets), but SCP/SFTP transfers hang (large packets).
- Web pages partially load — HTML loads but images/scripts don't (they require larger packets).
- `ping` succeeds (64 bytes) but application traffic fails.

### Testing with DF Bit
```bash
# Linux — find the maximum MTU without fragmentation
# Start at 1500 and decrease until ping succeeds
ping -M do -s 1472 destination.example.com   # 1472 + 28 (IP+ICMP headers) = 1500
ping -M do -s 1400 destination.example.com   # 1400 + 28 = 1428
ping -M do -s 1372 destination.example.com   # 1372 + 28 = 1400

# Windows — same test with -f flag
ping -f -l 1472 destination.example.com
ping -f -l 1400 destination.example.com
ping -f -l 1372 destination.example.com

# Expected output when packet is too large:
# Linux: "ping: local error: message too long, mtu=1400"
# or "From 10.0.0.1 icmp_seq=1 Frag needed and DF set (mtu = 1400)"
# Windows: "Packet needs to be fragmented but DF set."
```

### Binary Search for Path MTU
```bash
# Efficient binary search approach:
# Test 1472 (MTU 1500): FAIL
# Test 1200 (MTU 1228): PASS
# Test 1336 (MTU 1364): PASS
# Test 1404 (MTU 1432): FAIL
# Test 1370 (MTU 1398): PASS
# Test 1387 (MTU 1415): FAIL
# Test 1378 (MTU 1406): FAIL
# Test 1374 (MTU 1402): FAIL
# Test 1372 (MTU 1400): PASS → Path MTU is 1400
```

---

## MSS Clamping

TCP MSS (Maximum Segment Size) defines the largest TCP payload a host will accept. MSS is negotiated during the TCP three-way handshake (SYN and SYN-ACK packets carry the MSS option).

### MSS = MTU − 40 bytes
- IP header: 20 bytes
- TCP header: 20 bytes
- For 1500 MTU: MSS = 1460
- For 1400 MTU (VPN): MSS = 1360

### Configuring MSS Clamping
MSS clamping modifies the MSS value in TCP SYN packets as they pass through a router or firewall, ensuring that TCP segments never exceed the path MTU.

```bash
# Cisco IOS — clamp MSS on an interface
interface Tunnel0
  ip tcp adjust-mss 1360

# Linux iptables — clamp MSS for traffic leaving a VPN tunnel
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
  -o tun0 -j TCPMSS --set-mss 1360

# Linux iptables — auto-clamp to path MTU
sudo iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
  -j TCPMSS --clamp-mss-to-pmtu
```

### Azure VPN Gateway MSS
Azure VPN Gateway automatically clamps MSS to 1350 bytes for S2S tunnels. On-premises VPN device should also clamp MSS to prevent issues on the on-premises → Azure direction.

---

## Jumbo Frames

Jumbo frames use MTU > 1500 bytes (typically 9000 bytes) to improve throughput efficiency by reducing per-packet overhead.

### Cloud Support
- **Azure**: Jumbo frames (8900 bytes) supported between VMs with accelerated networking enabled, within the same VNet. Not supported across VNet peering, VPN, or ExpressRoute.
- **AWS**: Jumbo frames (9001 bytes) supported within VPC, across VPC peering (same region), and on placement groups. Not supported over VPN, Direct Connect, or internet gateway. Transit Gateway supports 8500 bytes.
- **GCP**: Configurable per-VPC MTU up to 8896 bytes. VMs in the VPC must have a NIC on the VPC with matching MTU configured in the OS.

### Jumbo Frame Gotchas
- All devices in the path must support the same MTU — one device with 1500 MTU in a jumbo-frame path will cause fragmentation or drops.
- NVAs/firewalls in the path must be configured for jumbo MTU on all interfaces.
- Health probes may use small packets and succeed while application traffic (jumbo) fails.
- VPN and internet paths always require standard 1500 MTU or less.

---

## Troubleshooting MTU Black Holes

An MTU black hole occurs when packets are too large for a path segment, PMTUD fails (ICMP blocked), and no ICMP error is returned to the sender.

### Identification
1. Large transfers stall — packet capture shows repeated retransmissions of the same large segment.
2. `ping -M do -s 1472` fails silently (no ICMP response, just timeout).
3. Packet capture at the sender shows data packets leaving but no ACKs returning for large segments.

### Resolution Steps
1. **Enable ICMP**: Ensure all firewalls, NSGs, and NACLs allow ICMP Type 3 (Destination Unreachable) in both directions. This is the most common cause.
2. **Apply MSS clamping**: Set TCP MSS to 1360 on VPN tunnel interfaces as a conservative default.
3. **Reduce interface MTU**: Set the VM or tunnel interface MTU to match the path MTU.
4. **Use PMTUD-compatible configurations**: Ensure VPN devices set the DF bit and handle ICMP responses correctly.

```bash
# Linux — set interface MTU
sudo ip link set eth0 mtu 1400

# Verify current MTU
ip link show eth0 | grep mtu

# Azure — check VM NIC MTU (via serial console or SSH)
cat /sys/class/net/eth0/mtu
```

**Analysis only — verify against vendor documentation before applying.**
