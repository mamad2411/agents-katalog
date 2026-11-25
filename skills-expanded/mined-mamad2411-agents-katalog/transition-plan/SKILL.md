# Skill: IPv6 Transition Planning

## Purpose

Plan and execute phased IPv6 migration strategies for enterprise environments across Azure, AWS, and GCP. Covers readiness assessment, migration priorities, cloud provider support matrices, risk mitigation, and rollback procedures.

## Core Knowledge

### Phased Migration Approach

IPv6 migration follows a structured progression to minimize risk:

```
Phase 1: ASSESS        Phase 2: PILOT       Phase 3: EXPAND      Phase 4: COMPLETE
─────────────────      ──────────────       ───────────────      ─────────────────
• Inventory infra      • Edge services      • Core networks      • IPv6-preferred
• App compatibility    • DNS dual-stack     • Internal apps      • Decommission IPv4
• Service support      • Public LBs         • Databases          • IPv6-only where
• Gap analysis         • External APIs      • Private links        possible
• Address planning     • Monitor/learn      • Full dual-stack    • NAT64 for legacy
• Team training        • 5-10% traffic      • 50-80% traffic     • 100% capability
```

### Phase 1: Assess Readiness

**Infrastructure Inventory:**
- List all VNets/VPCs, subnets, peering connections
- Identify network appliances (firewalls, NVAs, load balancers)
- Document DNS infrastructure and record types
- Map application dependencies and communication flows

**Application Compatibility Checklist:**
| Check | Risk if Failed |
|-------|---------------|
| Hardcoded IPv4 addresses in config/code | App failure on IPv6 |
| IPv4-only regex for address validation | Input rejection |
| `AF_INET`-only socket creation | Cannot bind IPv6 |
| 4-byte address storage in databases | Cannot store IPv6 |
| IPv4-only ACLs in application layer | Security bypass |
| Address-based session/rate limiting | Logic failure |

**Assessment Commands:**
```bash
# Find hardcoded IPv4 in codebase
grep -rn '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' ./src/

# Check if services listen on IPv6
ss -6 -tlnp           # Linux: IPv6 listening sockets
netstat -an | findstr ":::"  # Windows: IPv6 listeners

# Verify OS IPv6 stack enabled
sysctl net.ipv6.conf.all.disable_ipv6  # Linux (0 = enabled)
Get-NetAdapterBinding -ComponentID ms_tcpip6  # Windows
```

### Phase 2: Pilot

**Start at the Edge:**
1. Enable dual-stack on public-facing load balancers
2. Add AAAA records for external DNS entries
3. Configure CDN for IPv6 delivery
4. Monitor IPv6 traffic percentage and errors

**Why Edge First:**
- Lowest risk (external clients already handle both protocols)
- Immediate validation of DNS and routing
- Measurable traffic shift metrics
- No internal application changes required initially

**Pilot Success Criteria:**
- IPv6 traffic flows without errors to edge services
- Latency comparable to IPv4 (within 5ms)
- No increase in error rates
- Monitoring and alerting covers IPv6 metrics
- Team comfortable with IPv6 operational procedures

### Phase 3: Expand

**Core Network Migration:**
- Enable dual-stack on hub VNets/VPCs
- Add IPv6 to transit gateways and peering
- Extend to internal load balancers
- Migrate internal DNS to serve AAAA records
- Update firewall rules for IPv6 traffic

**Workload Migration Order:**
1. Stateless web services (easiest to validate)
2. API gateways and microservices
3. Databases and stateful services (most complex)
4. Legacy applications (may need NAT64)

### Phase 4: Complete

**IPv6-Preferred or IPv6-Only:**
- Configure DNS to prefer AAAA responses
- Deploy NAT64/DNS64 for remaining IPv4-only destinations
- Remove IPv4 addresses from internal resources where possible
- Maintain IPv4 only for legacy integrations behind NAT64

### IPv6-Only Networks — When and Why

**Use IPv6-only when:**
- Simplified operations (single stack, no dual management)
- Address exhaustion prevents further IPv4 allocation
- Internal microservices with no external IPv4 dependencies
- New greenfield deployments with no legacy constraints
- Mobile/IoT networks (Apple, Android already support IPv6-only)

**Requirements for IPv6-only:**
- NAT64 + DNS64 for reaching IPv4-only destinations
- All internal services must support IPv6
- Monitoring and tooling must handle IPv6
- 464XLAT for legacy applications that require literal IPv4

### Migration Priorities: Edge → Core → Workloads

```
Priority 1 (Edge):          Priority 2 (Core):         Priority 3 (Workloads):
• Public Load Balancers     • Hub VNets/VPCs           • Application servers
• CDN / Front Door          • VPN Gateways             • Databases
• WAF                       • ExpressRoute/DX          • Message queues
• External DNS              • Internal DNS             • Storage services
• API Gateways (public)     • Firewall / NVAs          • Container platforms
                            • Transit Gateways          • Monitoring systems
```

## Cloud-Specific Details

### Azure IPv6 Support Matrix

| Service | IPv6 Support | Notes |
|---------|-------------|-------|
| Virtual Network | ✅ Full | Dual-stack VNets, /64 subnets |
| Standard Load Balancer | ✅ Full | Dual-stack frontends and backends |
| Application Gateway v2 | ✅ Full | Dual-stack frontend |
| Azure Firewall | ✅ Full | Premium and Standard SKUs |
| VPN Gateway | ✅ Preview / opt-in | IPv6 private connectivity is preview/opt-in; route-based supported SKUs only |
| ExpressRoute | ✅ Full | Private and Microsoft peering |
| Azure DNS (public) | ✅ Full | AAAA records supported |
| Azure Private DNS | ✅ Full | AAAA records in private zones |
| AKS | ✅ Full | Dual-stack clusters supported |
| Azure Front Door | ✅ Full | IPv6 frontends |
| NAT Gateway | ✅ Partial | Standard is IPv4 outbound only; StandardV2 supports IPv6 outbound where available |
| Basic Load Balancer | ❌ No | Standard LB required |
| VNet peering | ✅ Full | Cross-region supported |
| Network Watcher | ✅ Partial | Some tools support IPv6 flows |
| Azure Bastion | ❌ No | IPv4 only for management |
| Private Endpoints | ✅ Partial | Service-dependent |

**Azure IPv6 caveats:**
- **NAT Gateway:** Standard SKU remains IPv4 outbound only. StandardV2 supports IPv6 outbound with Standard public IP resources; verify regional availability, SKU eligibility, and current limitations before designing around it. This is outbound IPv6 support, not a general NAT64 gateway.
- **VPN Gateway:** IPv6 is preview/opt-in. Validate supported gateway SKUs and configurations; current limitations include inner IPv6 traffic only, no SSTP or IKEv1, no Virtual WAN support, and UDR/routing constraints documented by Azure.

### AWS IPv6 Support Matrix

| Service | IPv6 Support | Notes |
|---------|-------------|-------|
| VPC | ✅ Full | /56 per VPC, /64 per subnet |
| EC2 | ✅ Full | Most instance families |
| ALB | ✅ Full | Dualstack mode |
| NLB | ✅ Full | Dualstack mode |
| CloudFront | ✅ Full | IPv6 enabled by default |
| Route 53 | ✅ Full | AAAA records, DNS64 |
| Security Groups | ✅ Full | IPv6 CIDR rules |
| NACLs | ✅ Full | IPv6 rules |
| Transit Gateway | ✅ Full | Dual-stack attachments |
| Direct Connect | ✅ Full | IPv6 BGP peering |
| NAT Gateway | ✅ Full | NAT64 support added |
| Egress-only IGW | ✅ Full | Outbound IPv6 for private subnets |
| EKS | ✅ Full | IPv6 cluster networking |
| S3 | ✅ Full | Dual-stack endpoints |
| RDS | ✅ Partial | Some engines, dual-stack mode |
| Lambda | ✅ Full | IPv6 in VPC mode |
| API Gateway | ✅ Partial | REST API (not HTTP API) |

### GCP IPv6 Support Matrix

| Service | IPv6 Support | Notes |
|---------|-------------|-------|
| VPC subnets | ✅ Full | External and internal IPv6 |
| Compute Engine | ✅ Full | Dual-stack VMs |
| External HTTP(S) LB | ✅ Full | IPv6 forwarding rules |
| Internal TCP/UDP LB | ✅ Full | With dual-stack subnets |
| Cloud DNS | ✅ Full | AAAA records |
| Cloud NAT | ❌ No | IPv4 only |
| Cloud Armor | ✅ Full | IPv6 source rules |
| GKE | ✅ Full | Dual-stack clusters |
| Cloud Interconnect | ✅ Full | IPv6 BGP sessions |
| Cloud VPN | ✅ Partial | HA VPN with IPv6 |
| Private Google Access | ✅ Full | IPv6-only VM access to APIs |
| Cloud Functions | ✅ Partial | Varies by gen |
| Cloud Run | ✅ Full | Dual-stack by default |
| Firewall Rules | ✅ Full | IPv6 CIDR support |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Service doesn't support IPv6 | Connectivity loss | Pre-assess all services; use NAT64 |
| Application hardcodes IPv4 | App failure | Code audit in Phase 1; fix before migration |
| ICMPv6 blocked by firewall | Broken PMTUD, NDP failure | Audit all NSG/SG rules; allow ICMPv6 |
| Monitoring blind to IPv6 | Undetected issues | Extend dashboards and alerts before migration |
| Asymmetric routing | Packet drops, state mismatch | Mirror IPv6 routes to match IPv4 topology |
| Address planning errors | Overlaps, renumbering needed | Use structured /48→/56→/64 hierarchy |
| Third-party doesn't support IPv6 | Integration failure | Maintain NAT64 for external dependencies |
| Performance regression | User impact | Benchmark before/after; implement Happy Eyeballs |
| Team unfamiliarity | Operational errors | Training before Phase 2; runbook documentation |

## Rollback Strategies

### Per-Phase Rollback

**Phase 2 (Pilot) Rollback:**
```bash
# Remove AAAA records (clients fall back to IPv4)
az network dns record-set aaaa delete --zone-name example.com \
  --resource-group myRG --name www --yes

# Disable dual-stack on load balancer
aws elbv2 set-ip-address-type \
  --load-balancer-arn arn:aws:... \
  --ip-address-type ipv4
```

**Phase 3 (Expand) Rollback:**
```bash
# Remove IPv6 from subnet (VMs lose IPv6)
az network vnet subnet update --resource-group myRG \
  --vnet-name myVNet --name mySubnet \
  --address-prefixes 10.0.0.0/24  # IPv4 only

# Disable IPv6 on interface (per-VM)
sudo sysctl -w net.ipv6.conf.eth0.disable_ipv6=1
```

**Phase 4 (Complete) Rollback:**
- More complex; requires re-adding IPv4 addresses
- Plan for this: keep IPv4 address space reserved
- Don't release IPv4 allocations until 90+ days stable

### Rollback Triggers

- Error rate increase > 1% attributable to IPv6
- Latency increase > 10ms on IPv6 vs IPv4 path
- Service availability drop below SLA
- Security incident related to IPv6 exposure
- Critical application failure on IPv6

## Success Criteria and Validation

### Phase Gate Criteria

**Phase 1 → Phase 2:**
- [ ] Complete infrastructure inventory documented
- [ ] Application compatibility assessment complete (no critical blockers)
- [ ] IPv6 address plan designed and approved
- [ ] Team completed IPv6 training
- [ ] Monitoring tools verified for IPv6 capability

**Phase 2 → Phase 3:**
- [ ] Edge services serving IPv6 traffic successfully for 30+ days
- [ ] Error rates on IPv6 equivalent to IPv4 (±0.1%)
- [ ] Latency on IPv6 within 5ms of IPv4
- [ ] Operational runbooks validated
- [ ] No P1/P2 incidents attributed to IPv6

**Phase 3 → Phase 4:**
- [ ] All core network paths dual-stack enabled
- [ ] >80% of workloads reachable over IPv6
- [ ] Internal DNS serving AAAA for all services
- [ ] NAT64/DNS64 operational for remaining IPv4 dependencies
- [ ] Full incident response tested on IPv6

### Validation Commands

```bash
# Verify dual-stack reachability end-to-end
for host in app1 app2 app3; do
  echo "=== $host ==="
  curl -4 -s -o /dev/null -w "IPv4: %{http_code} %{time_total}s\n" https://$host.example.com
  curl -6 -s -o /dev/null -w "IPv6: %{http_code} %{time_total}s\n" https://$host.example.com
done

# Check IPv6 traffic percentage (Azure)
az monitor metrics list --resource /subscriptions/.../loadBalancers/myLB \
  --metric "ByteCount" --dimension "FrontendIPAddress"

# Verify no IPv6 packet drops
# AWS VPC Flow Logs — filter for IPv6 REJECT
aws logs filter-log-events --log-group-name vpc-flow-logs \
  --filter-pattern "REJECT" | grep -i ":" 
```

## Troubleshooting Tips

- **Migration stalled?** Check for services that don't support IPv6 (use NAT64 as workaround)
- **Performance worse on IPv6?** Verify routing is symmetric; check for longer AS paths
- **Partial connectivity?** Often caused by missing IPv6 firewall rules or route table entries
- **DNS not resolving IPv6?** Ensure recursive resolvers support AAAA queries and transport
- **Rollback not working?** Cached AAAA records persist until TTL expires; lower TTL before changes

---

**Analysis only — verify against vendor documentation before applying.**
