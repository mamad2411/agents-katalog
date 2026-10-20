# Skill: Routing Debug (ntsh_routing-debug)

Debug routing issues including effective route analysis, UDR conflicts, BGP route propagation, next-hop validation, and route table inspection across Azure, AWS, and GCP.

---

## Azure — Effective Routes

The effective route table for a VM NIC shows all routes that determine traffic forwarding, combining system routes, UDRs, BGP-learned routes, and service endpoint routes.

### Show Effective Routes
```bash
# Show effective routes for a VM NIC
az network nic show-effective-route-table \
  --name MyVMNic --resource-group MyRG -o table

# Output columns: Source, State, AddressPrefix, NextHopType, NextHopIP
# Sources: Default (system), User (UDR), VirtualNetworkGateway (BGP), Unknown
```

### Route Selection Priority (Azure)
When multiple routes match a destination, Azure selects in this order:
1. **Longest prefix match** — /28 beats /16 for addresses in both prefixes.
2. **Source priority** — User (UDR) > VirtualNetworkGateway (BGP) > Default (system).
3. **For BGP routes** — standard BGP path selection (local preference, AS path length, MED, etc.).

### Common Effective Route Issues
- **Route state "Invalid"**: UDR points to a next-hop IP that doesn't exist or is unreachable.
- **Missing VNet peering routes**: Peering not configured or not connected. Check `az network vnet peering list`.
- **Default route (0.0.0.0/0) override**: A UDR or BGP-advertised default route overrides the system internet route, causing forced tunneling.
- **Next hop "None"**: Black hole route — traffic matching this prefix is silently dropped. Used intentionally to block traffic or indicates misconfiguration.

### Next Hop Validation
```bash
# Check next hop for specific destination
az network watcher show-next-hop \
  --vm MyVM --resource-group MyRG \
  --source-ip 10.0.1.4 \
  --dest-ip 10.0.2.5

# Output: NextHopType (VirtualNetwork, VirtualAppliance, Internet, None)
#         NextHopIpAddress (IP of NVA if VirtualAppliance)
#         RouteTableId (which route table matched)
```

---

## UDR Conflicts and Common Misconfigurations

### Conflict Patterns

**Overlapping prefixes with different next hops**:
```
UDR1: 10.0.0.0/8 → VirtualAppliance (10.0.3.4)   # NVA firewall
UDR2: 10.0.2.0/24 → VNetPeering                     # Direct peering
```
Azure applies longest prefix match — 10.0.2.x traffic goes via peering (more specific), all other 10.x traffic goes via NVA. This may be intentional or a misconfiguration.

**Missing return path UDR**:
Traffic from subnet A to subnet B routes through NVA (via UDR on subnet A), but subnet B has no UDR sending return traffic through the same NVA. Result: asymmetric routing → NVA drops return traffic because it has no session state.

**Solution**: Apply symmetric UDRs on both subnets:
```bash
# Subnet A UDR: traffic to Subnet B via NVA
az network route-table route create \
  --route-table-name SubnetA-RT --resource-group MyRG \
  --name ToSubnetB --address-prefix 10.0.2.0/24 \
  --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.3.4

# Subnet B UDR: traffic to Subnet A via NVA
az network route-table route create \
  --route-table-name SubnetB-RT --resource-group MyRG \
  --name ToSubnetA --address-prefix 10.0.1.0/24 \
  --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.3.4
```

**NVA IP forwarding not enabled**:
When using a VM as an NVA, IP forwarding must be enabled at both the Azure NIC level and within the VM OS.
```bash
# Enable IP forwarding on NIC
az network nic update --name NVA-NIC --resource-group MyRG --ip-forwarding true

# Enable inside Linux VM
sudo sysctl -w net.ipv4.ip_forward=1
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
```

---

## BGP Route Propagation

### Azure VNet Gateway — Learned and Advertised Routes
```bash
# Routes learned from BGP peers (on-premises, other clouds)
az network vnet-gateway list-learned-routes \
  --name MyGateway --resource-group MyRG -o table

# Routes advertised to a specific BGP peer
az network vnet-gateway list-advertised-routes \
  --name MyGateway --resource-group MyRG \
  --peer 10.0.0.1 -o table

# BGP peer status
az network vnet-gateway list-bgp-peer-status \
  --name MyGateway --resource-group MyRG -o table
```

### Azure Route Server
Route Server enables dynamic route exchange between NVAs and the Azure VNet. NVAs peer with Route Server via BGP and inject routes into the VNet's effective route table.

```bash
# Check Route Server learned routes
az network routeserver peering list-learned-routes \
  --routeserver MyRouteServer --resource-group MyRG \
  --name NVAPeering

# Check Route Server advertised routes
az network routeserver peering list-advertised-routes \
  --routeserver MyRouteServer --resource-group MyRG \
  --name NVAPeering
```

---

## AWS Route Table Inspection

```bash
# Show all routes in a route table
aws ec2 describe-route-tables \
  --route-table-ids rtb-xxx \
  --query 'RouteTables[0].Routes[].{Dest:DestinationCidrBlock, Target:GatewayId || NatGatewayId || TransitGatewayId || VpcPeeringConnectionId || NetworkInterfaceId, State:State, Origin:Origin}' \
  -o table

# Check route propagation status
aws ec2 describe-route-tables \
  --route-table-ids rtb-xxx \
  --query 'RouteTables[0].PropagatingVgws'

# Identify which route table is associated with a subnet
aws ec2 describe-route-tables \
  --filters "Name=association.subnet-id,Values=subnet-xxx" \
  --query 'RouteTables[0].{RouteTableId:RouteTableId, Routes:Routes[].{Dest:DestinationCidrBlock, Target:GatewayId}}'
```

### Common AWS Route Issues
- **Route propagation disabled**: VGW routes not appearing in route table. Enable: `aws ec2 enable-vgw-route-propagation`.
- **More specific static route overrides propagated route**: Static routes take precedence over propagated BGP routes for the same prefix.
- **Blackhole route**: Route target was deleted (e.g., NAT Gateway removed) but route entry remains. State shows "blackhole".

---

## GCP Routes Inspection

```bash
# List all routes in a VPC
gcloud compute routes list \
  --filter="network=my-vpc" \
  --format="table(name,destRange,nextHopGateway,nextHopInstance,nextHopIp,nextHopVpnTunnel,priority)"

# Check Cloud Router status (BGP-learned routes)
gcloud compute routers get-status my-router --region us-central1 \
  --format="json(result.bestRoutes)"

# Show route details
gcloud compute routes describe my-route
```

### GCP Route Priority
- Routes are evaluated by specificity first (longest prefix match), then by priority (lower number = higher priority).
- Dynamic routes (from Cloud Router BGP) have base priority 100 by default; regional preference adds to this.
- Static routes with priority 1000 (default) are overridden by more specific dynamic routes.

**Analysis only — verify against vendor documentation before applying.**
