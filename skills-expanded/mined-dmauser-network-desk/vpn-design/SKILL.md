# Skill: VPN Gateway Design (hyb_vpn-design)

Design and configure VPN gateways for site-to-site and point-to-site connectivity across Azure, AWS, and GCP. This skill covers gateway SKU selection, tunnel configuration, IPsec/IKE policy customization, and performance optimization.

---

## Site-to-Site (S2S) vs Point-to-Site (P2S)

### Site-to-Site VPN
Connects an entire on-premises network to a cloud VNet/VPC through an IPsec/IKEv2 tunnel between the on-premises VPN device and the cloud VPN gateway. Suitable for persistent, always-on connectivity between networks.

- **Azure**: VPN Gateway resource with `GatewayType: Vpn`. Requires a Local Network Gateway (LNG) representing the on-premises device (public IP + address space). Connection object links VPN Gateway to LNG with shared key.
- **AWS**: Customer Gateway (CGW, representing on-premises device) + VPN Connection to Virtual Private Gateway (VGW) or Transit Gateway. Each VPN connection includes two tunnels for redundancy, each to a different AWS endpoint.
- **GCP**: External VPN Gateway (representing on-premises device) + HA VPN Gateway or Classic VPN Gateway + VPN Tunnels + Cloud Router for BGP.

### Point-to-Site VPN
Connects individual client devices to a cloud VNet. Suitable for remote workers, administrators, and development scenarios.

- **Azure P2S protocols**: IKEv2 (Windows 10+, macOS, Linux strongSwan), OpenVPN (all platforms via Azure VPN Client or OpenVPN client), SSTP (Windows only, TCP 443). Authentication: Azure certificate, Azure AD/Entra ID, RADIUS.
- **AWS Client VPN**: OpenVPN-based managed service. Supports Active Directory, mutual certificate, federated (SAML) authentication. Split-tunnel or full-tunnel.
- **GCP**: No native P2S service — use third-party NVAs (e.g., OpenVPN Access Server, WireGuard) on Compute Engine instances.

---

## IKEv2 vs OpenVPN Protocol Selection

| Factor | IKEv2 | OpenVPN |
|--------|-------|---------|
| Transport | UDP 500/4500 | UDP 1194 or TCP 443 |
| Performance | Higher (kernel-space) | Lower (user-space) |
| NAT traversal | Built-in (UDP 4500) | Built-in |
| Firewall friendliness | May be blocked | TCP 443 rarely blocked |
| Platform support | Windows, macOS, iOS, Linux | All platforms |
| Reconnection | MOBIKE for seamless roaming | Manual or keepalive-based |

**Recommendation**: Use IKEv2 for S2S tunnels and performance-sensitive P2S. Use OpenVPN for P2S when firewall traversal is required or cross-platform consistency is needed.

---

## BGP vs Static Routing

### BGP (Dynamic Routing)
- Automatically propagates route changes — essential for failover scenarios.
- Required for active-active VPN gateways, ExpressRoute coexistence, and Transit Gateway.
- Azure: Enable BGP on VPN Gateway (ASN assignment), configure BGP peer IPs.
- AWS: Enabled per tunnel in VPN Connection. Each tunnel has two BGP sessions (inside tunnel IPs).
- GCP: Cloud Router manages BGP sessions for HA VPN. Supports custom route advertisements.

### Static Routing
- Simpler configuration, no BGP support required on on-premises device.
- Routes must be manually updated when address spaces change.
- Not recommended for production environments with multiple paths or failover requirements.

**Recommendation**: Always prefer BGP for S2S VPN unless the on-premises device lacks BGP support.

---

## Active-Active vs Active-Standby

### Active-Active
- **Azure**: Two VPN Gateway instances, each with its own public IP. Both tunnels active simultaneously. Requires BGP. Distributes traffic across both instances.
- **AWS**: Default behavior — each VPN connection has two active tunnels (but traffic typically uses one; asymmetric routing is possible).
- **GCP HA VPN**: Two interfaces (interface 0 and interface 1), each with its own public IP. Four tunnels for full HA (two per interface).

### Active-Standby
- **Azure**: Default mode. One active instance, one standby. Failover takes 10–15 seconds (with BGP) or 60–90 seconds (static). Only one public IP.
- Not applicable to AWS or GCP HA VPN by design.

**Recommendation**: Use active-active for production workloads requiring < 30-second failover and higher aggregate throughput.

---

## Custom IPsec/IKE Policies

Define specific cryptographic parameters instead of relying on cloud provider defaults:

### Phase 1 (IKE SA) Parameters
- **Encryption**: AES-256-GCM (preferred), AES-256-CBC, AES-192-CBC, AES-128-CBC
- **Integrity**: SHA-384 (preferred), SHA-256, SHA-1 (avoid — deprecated)
- **DH Group**: ECP384 (preferred), ECP256, DHGroup24, DHGroup14. Avoid DHGroup2 (1024-bit — insecure).
- **SA Lifetime**: Default 28,800 seconds (8 hours). Shorter lifetimes increase security but add rekeying overhead.

### Phase 2 (IPsec SA / Child SA) Parameters
- **Encryption**: AES-256-GCM (preferred — provides both encryption and integrity), AES-256-CBC
- **Integrity**: SHA-256 (when not using GCM), SHA-384
- **PFS Group**: ECP384, ECP256, PFS24, PFS2048 (DHGroup14)
- **SA Lifetime**: Default 3,600 seconds (1 hour) or 102,400 KB. Azure allows configuring by time and data.

### Configuration Examples

**Azure — Custom IPsec Policy:**
```bash
az network vpn-connection ipsec-policy add \
  --connection-name MyS2SConnection \
  --resource-group MyRG \
  --ike-encryption AES256 \
  --ike-integrity SHA384 \
  --dh-group ECP384 \
  --ipsec-encryption GCMAES256 \
  --ipsec-integrity GCMAES256 \
  --pfs-group ECP384 \
  --sa-lifetime 3600 \
  --sa-data-size 102400000
```

**AWS — Tunnel Options in VPN Connection:**
```bash
aws ec2 create-vpn-connection \
  --type ipsec.1 \
  --customer-gateway-id cgw-xxx \
  --vpn-gateway-id vgw-xxx \
  --options '{"TunnelOptions": [{"Phase1EncryptionAlgorithms": [{"Value": "AES256"}], "Phase1IntegrityAlgorithms": [{"Value": "SHA2-384"}], "Phase1DHGroupNumbers": [{"Value": 20}], "Phase2EncryptionAlgorithms": [{"Value": "AES256-GCM-16"}], "Phase2IntegrityAlgorithms": [{"Value": "SHA2-384"}], "Phase2DHGroupNumbers": [{"Value": 20}]}]}'
```

---

## Azure VPN Gateway SKU Selection

Default new designs to **VpnGw1AZ through VpnGw5AZ** for zone-resilient production gateways, and verify current tunnel, P2S, and throughput values in the Azure VPN Gateway SKU documentation before sizing. Treat non-AZ **VpnGw1 through VpnGw5** as legacy or migration-only choices because Azure is consolidating gateway SKUs; check the SKU consolidation timeline before creating or resizing gateways: https://learn.microsoft.com/en-us/azure/vpn-gateway/gateway-sku-consolidation.

**SKU Selection Guidance:**
- **VpnGw1AZ**: Development, testing, and smaller branch workloads after validating current limits.
- **VpnGw2AZ/VpnGw3AZ**: Typical production workloads that need BGP and zone resilience.
- **VpnGw4AZ/VpnGw5AZ**: High-throughput, large-scale branch or P2S deployments after validating current limits and cost.
- **Non-AZ VpnGw1-5**: Use only for existing deployments, migration sequencing, or documented exceptions; plan upgrades to AZ SKUs where supported.

**Analysis only — verify against vendor documentation before applying.**
