# Skill: NAT Debugging (ntsh_nat-debug)

Diagnose and resolve NAT issues including SNAT port exhaustion, DNAT misconfigurations, connection tracking, and idle timeout problems across Azure, AWS, and GCP.

---

## SNAT Port Exhaustion

### The Problem
Each outbound connection from a cloud VM to an external destination requires a unique SNAT (Source NAT) port. The combination of {SNAT IP, SNAT port, destination IP, destination port, protocol} must be unique. When all available SNAT ports are consumed, new outbound connections fail.

### Azure Load Balancer SNAT
- Default: 1,024 SNAT ports per backend instance per frontend IP (for pools ≤ 50 instances).
- Ports scale inversely with pool size: 50 instances = 1,024 ports each; 100 instances = 512 each; 1,000 instances = 64 each.
- **Maximum**: 64,000 SNAT ports per frontend IP (theoretical; practical limit is lower due to port reuse timers).

**Symptoms of SNAT exhaustion**:
- Intermittent outbound connection failures (TCP timeouts).
- Azure Monitor metric: `SNAT Connection Count` with `Connection State = Failed`.
- Application logs: "An attempt was made to access a socket in a way forbidden by its access permissions" (Windows) or "Cannot assign requested address" (Linux).

**Diagnostic Commands**:
```bash
# Check SNAT port allocation for a Load Balancer
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/loadBalancers/{lb} \
  --metric "SnatConnectionCount" \
  --aggregation Total \
  --filter "ConnectionState eq 'Failed'" \
  --interval PT1M

# Check used SNAT connections
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/loadBalancers/{lb} \
  --metric "UsedSnatPorts" \
  --aggregation Average \
  --interval PT1M
```

### Azure NAT Gateway
- 64,512 SNAT ports per public IP address (verify current Azure limits/quotas before sizing).
- Supports up to 16 public IP addresses = 1,032,192 total SNAT ports for inventory planning; public IP count scales ports, not bandwidth.
- Dynamically allocates ports on demand (no pre-allocation per instance).
- Recommended over LB SNAT for outbound-heavy workloads.

**NAT Gateway Metrics**:
```bash
# Check SNAT connection count
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/natGateways/{nat} \
  --metric "SNATConnectionCount" --aggregation Total --interval PT1M

# Check total SNAT connections
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/natGateways/{nat} \
  --metric "TotalConnectionCount" --aggregation Total --interval PT1M

# Check dropped packets (indicates exhaustion or other issues)
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/natGateways/{nat} \
  --metric "DroppedPackets" --aggregation Total --interval PT1M
```

### AWS NAT Gateway
- Official capacity framing is per NAT gateway and per unique destination, not a fixed per-second connection-rate ceiling.
- Bandwidth starts at 5 Gbps and scales up to 100 Gbps; packet processing scales from 1 million to 10 million packets per second.
- Each IPv4 address supports 55,000 simultaneous connections to each unique destination (destination IP, destination port, protocol). Add secondary private IPv4 addresses or distribute traffic across NAT gateways to increase per-destination connection capacity.
- If `ErrorPortAllocation` or `PacketsDropCount` CloudWatch metrics increase, connections or packets are being dropped; correlate with `ActiveConnectionCount`, `ConnectionAttemptCount`, and AWS Service Quotas before sizing.

**AWS NAT Gateway Metrics**:
```bash
# Check for SNAT port allocation errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/NATGateway \
  --metric-name ErrorPortAllocation \
  --dimensions Name=NatGatewayId,Value=nat-xxx \
  --start-time 2024-01-15T00:00:00Z --end-time 2024-01-15T23:59:59Z \
  --period 300 --statistics Sum

# Check active connection count
aws cloudwatch get-metric-statistics \
  --namespace AWS/NATGateway \
  --metric-name ActiveConnectionCount \
  --dimensions Name=NatGatewayId,Value=nat-xxx \
  --start-time 2024-01-15T00:00:00Z --end-time 2024-01-15T23:59:59Z \
  --period 300 --statistics Maximum

# Check dropped packets
aws cloudwatch get-metric-statistics \
  --namespace AWS/NATGateway \
  --metric-name PacketsDropCount \
  --dimensions Name=NatGatewayId,Value=nat-xxx \
  --start-time 2024-01-15T00:00:00Z --end-time 2024-01-15T23:59:59Z \
  --period 300 --statistics Sum
```

---

## SNAT Exhaustion Remediation

### 1. Use NAT Gateway Instead of LB SNAT
Azure NAT Gateway provides significantly more ports (64K per IP, up to 16 IPs) and dynamic allocation vs. Load Balancer's static per-instance allocation.

### 2. Add More Public IPs
Each additional public IP adds 64,000 SNAT ports.

### 3. Use Connection Pooling
Reuse HTTP connections instead of creating new ones for each request. Configure keep-alive settings in application HTTP clients.

### 4. Reduce Idle Timeout
Default TCP idle timeout is 4 minutes (Azure LB/NAT Gateway configurable 4–120 min). Shorter timeouts free ports faster.
```bash
# Azure NAT Gateway — set idle timeout
az network nat gateway update \
  --name MyNATGateway --resource-group MyRG \
  --idle-timeout 10
```

### 5. Use Private Endpoints
For connections to Azure PaaS services, use Private Endpoints to route traffic privately — bypasses SNAT entirely.

---

## DNAT Rules

DNAT (Destination NAT) translates the destination IP/port of incoming traffic, typically used for inbound load balancing or port forwarding.

### Azure Load Balancer Inbound NAT Rules
```bash
# Create inbound NAT rule (port forwarding)
az network lb inbound-nat-rule create \
  --lb-name MyLB --resource-group MyRG \
  --name SSH-VM1 --protocol TCP \
  --frontend-port 50001 --backend-port 22 \
  --frontend-ip-name MyFrontendIP

# List inbound NAT rules
az network lb inbound-nat-rule list \
  --lb-name MyLB --resource-group MyRG -o table
```

### Common DNAT Issues
- **Health probe failure**: Backend VM removed from pool because health probe fails. DNAT rule exists but traffic goes nowhere.
- **NSG blocking probe**: Azure health probes come from 168.63.129.16 — NSG must allow this source.
- **Backend port not listening**: Application not started or listening on wrong port/interface.

---

## Connection Tracking

Cloud NAT gateways and load balancers maintain connection tracking tables to map outbound SNAT translations to return traffic.

### Idle Timeout Behavior
- **Azure LB/NAT Gateway**: Default 4-minute TCP idle timeout. Connections idle longer than this are cleared from the tracking table. Return traffic after timeout is dropped (no matching entry).
- **AWS NAT Gateway**: 350-second (5 min 50 sec) idle timeout for TCP. 60-second timeout for UDP. Non-configurable.
- **GCP Cloud NAT**: 1200-second (20 min) default TCP established timeout. Configurable via `--tcp-established-idle-timeout`.

### Symptoms of Idle Timeout Issues
- Long-lived connections (database connections, WebSocket) drop after exactly the timeout period.
- Application receives RST or connection reset after period of inactivity.

### Remediation
- Enable TCP keepalive at the application level (typically every 60 seconds).
- Configure TCP keepalive at the OS level: `sysctl net.ipv4.tcp_keepalive_time=60` (Linux).
- Increase idle timeout on the NAT gateway (Azure: up to 120 minutes).
- Use application-level heartbeat/ping messages for protocols that support them.

```bash
# Linux — configure TCP keepalive
sudo sysctl -w net.ipv4.tcp_keepalive_time=60
sudo sysctl -w net.ipv4.tcp_keepalive_intvl=10
sudo sysctl -w net.ipv4.tcp_keepalive_probes=6
```

**Analysis only — verify against vendor documentation before applying.**
