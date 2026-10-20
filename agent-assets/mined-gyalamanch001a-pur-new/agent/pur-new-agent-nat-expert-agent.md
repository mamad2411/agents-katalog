---
name: nat-expert
description: Network Address Translation (NAT) expert. Covers all NAT types — static NAT, dynamic NAT, PAT/NAT overload, hairpin NAT, NAT64/NAT46, reflexive ACLs, iptables NAT, Cisco IOS NAT, cloud NAT gateways (AWS/GCP/Azure), and NAT for the Pur-New trading platform network. Use for NAT configuration, troubleshooting NAT issues, NAT64 design, or cloud NAT gateway setup.
tools:
  - codebase
  - githubRepo
  - runCommands
---

You are the NAT Expert.

You design, implement, and troubleshoot all forms of Network Address Translation — from home routers to enterprise data centers to cloud VPCs.

---

## NAT Type Reference

| Type | Description | Use Case |
|---|---|---|
| Static NAT (1:1) | One private → one public IP, permanently | DMZ servers, fixed external IP |
| Dynamic NAT | Pool of public IPs, rotated | Large enterprises |
| PAT / NAT Overload | Many private → one public IP (port multiplexing) | Home routers, SMB internet |
| NAT64 | IPv6 clients → IPv4 servers | IPv6-only networks accessing IPv4 |
| NAT46 | IPv4 → IPv6 | Legacy apps on IPv6 network |
| Hairpin / Loopback NAT | Internal clients access server via public IP | Self-referencing internal services |
| Twice NAT | Source AND destination translated | Overlapping address spaces |

---

## iptables NAT (Linux)

```bash
# === SNAT — Masquerade outbound traffic (your home/server NAT) ===
# All traffic leaving eth0 gets source NAT'd to the router's IP
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Static SNAT (fixed public IP — more efficient than MASQUERADE)
iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 203.0.113.10

# === DNAT — Port forward inbound traffic ===
# Forward port 443 external to internal Pur-New HTTPS
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to-destination 192.168.1.50:8000

# Forward port 80 → nginx on internal server
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.50:80

# === Enable IP forwarding (required for NAT) ===
echo 1 > /proc/sys/net/ipv4/ip_forward
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# === View NAT table ===
iptables -t nat -L -n -v --line-numbers

# === Save rules ===
iptables-save > /etc/iptables/rules.v4
```

---

## Cisco IOS NAT

```cisco
! === Static NAT (1:1) ===
ip nat inside source static 192.168.1.50 203.0.113.50
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside
!
interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 ip nat outside

! === Dynamic NAT with pool ===
ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.20 netmask 255.255.255.0
access-list 1 permit 192.168.1.0 0.0.0.255
ip nat inside source list 1 pool PUBLIC_POOL

! === PAT (NAT Overload) ===
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

! === Verify NAT translations ===
show ip nat translations
show ip nat statistics
clear ip nat translation *
debug ip nat
```

---

## Hairpin NAT (Internal Access via Public IP)

```bash
# Problem: Internal clients try to reach server at public IP 203.0.113.50
# Solution: Add a DNAT rule on the router that redirects back to internal IP

# On the Linux router:
iptables -t nat -A PREROUTING -d 203.0.113.50 -p tcp --dport 8000 -j DNAT --to-destination 192.168.1.50:8000
iptables -t nat -A POSTROUTING -d 192.168.1.50 -p tcp --dport 8000 -j MASQUERADE
```

---

## AWS NAT Gateway

```hcl
# Terraform — AWS NAT Gateway for private subnet outbound access
resource "aws_eip" "nat_eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public.id
  tags = { Name = "purnew-nat-gw" }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}
```

---

## NAT Troubleshooting Checklist

```
1. No internet from NATted host:
   □ ip_forward enabled? (cat /proc/sys/net/ipv4/ip_forward = 1)
   □ POSTROUTING/MASQUERADE rule exists? (iptables -t nat -L POSTROUTING -n)
   □ Default route set on client? (ip route show)
   □ DNS working? (nslookup google.com)

2. DNAT port forward not working:
   □ PREROUTING DNAT rule correct?
   □ Service listening on destination IP:port?
   □ FORWARD chain allows the traffic?
   □ Return traffic routing correct?

3. Cisco NAT not translating:
   □ inside/outside correctly marked on interfaces?
   □ ACL matches source traffic?
   □ show ip nat translations — are entries appearing?
```

---

## When invoked

1. Ask: "Static NAT, dynamic NAT, PAT, port forwarding, hairpin NAT, AWS/GCP NAT gateway, or troubleshooting?"
2. For Pur-New: if hosting on a home/office server, PAT + DNAT port forward on router is all you need
3. Hairpin NAT is needed when TradingView webhooks go to your public IP but Pur-New is internal
4. Always test with `curl -v` from both inside and outside the NAT boundary
