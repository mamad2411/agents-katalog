---
name: network-security-design
description: >-
  Azure network security design patterns. Covers private endpoints, NSG/ASG
  design, zero trust networking, firewall configuration, WAF requirements,
  and common security findings.
when-to-use: >-
  Invoke when designing network security for Azure workloads, reviewing
  network configurations for security compliance, implementing private
  endpoints, or hardening production network architecture.
categories:
  - security
  - networking
  - azure
  - architecture
---

# Network Security Design

Network security enforces defense in depth and limits blast radius. Network is not an identity — every service-to-service call must also be authenticated.

## Production Requirements (Non-Negotiable)

- [ ] **Private endpoints for all PaaS services** — Storage, SQL, Cosmos DB, Key Vault, ACR, App Service. Public network access disabled.
- [ ] **NSGs on every subnet** — deny by default, allow specific ports and source ranges only. No NSG = no deployment.
- [ ] **No public IPs on VMs** — use Azure Bastion for management. JIT VM access as alternative.
- [ ] **WAF on internet-facing web apps** — Application Gateway v2 or Azure Front Door with WAF. OWASP 3.2 rule set minimum.
- [ ] **DDoS Protection Standard** — on all VNets with public IP resources. Basic tier is insufficient.

---

## Zero Trust Network

No implicit trust between any network segments:

- **Microsegmentation with NSGs + ASGs** — each application tier in its own subnet with its own NSG. Use Application Security Groups to simplify rules.
- **East-west traffic inspection** — Azure Firewall or NVA in hub VNet inspecting traffic between spokes. Not just north-south.
- **No implicit trust between subnets** — web tier cannot talk to database tier directly. All traffic goes through defined paths.
- **Every service-to-service call authenticated** — managed identity + RBAC, not just network proximity.

---

## Private Endpoint Checklist

For every PaaS service, verify:

| Service | Private Endpoint? | Public Access Disabled? | Private DNS Zone? | DNS Resolving? |
|---|---|---|---|---|
| Storage (blob, file, table, queue) | | | | |
| Azure SQL / Cosmos DB | | | | |
| Key Vault | | | | |
| Azure Container Registry | | | | |
| App Service / Functions | | | | |
| Event Hub / Service Bus | | | | |

**Private endpoints vs service endpoints:** Service endpoints don't disable public access. Always prefer private endpoints in production.

---

## NSG Design Principles

- **Default deny** — start with deny-all, add specific allow rules
- **Least privilege** — allow only required ports and source ranges
- **Use ASGs** — group VMs/NICs by role instead of managing IP addresses
- **Log all flows** — enable NSG flow logs for security analysis
- **Review regularly** — rules accumulate over time, remove stale allows

### NSG Rule Priority

| Priority Range | Purpose |
|---|---|
| 100-999 | Application-specific allow rules |
| 1000-1999 | Platform/infrastructure rules |
| 2000-3999 | Reserved for future use |
| 4000-4095 | Deny rules (explicit blocks) |
| 65000-65500 | Azure defaults (do not modify) |

---

## Firewall Review

- [ ] Azure Firewall or NVA deployed in hub?
- [ ] All egress through firewall? (UDR on all subnets)
- [ ] Threat intelligence enabled? (block known malicious IPs/domains)
- [ ] TLS inspection where appropriate?
- [ ] IDPS in alert or deny mode? (Azure Firewall Premium)
- [ ] Application rules over network rules? (FQDN-based where possible)
- [ ] No direct internet breakout from spoke subnets?

---

## WAF Configuration

- OWASP 3.2 rule set minimum on all internet-facing endpoints
- Enable bot protection rules
- Review and tune false positives — don't disable rules globally
- Use exclusions for known-good patterns rather than disabling entire rule groups
- Enable logging to Log Analytics for security analysis

---

## Common Findings (Always Flag These)

| Finding | Severity | Remediation |
|---|---|---|
| App Service with public endpoint, no IP restriction | High | Add access restrictions or private endpoint |
| Storage account without private endpoint (prod) | High | Deploy private endpoint, disable public access |
| VM with public IP assigned directly | High | Remove public IP, use Bastion |
| NSG allowing 0.0.0.0/0 on port 22 or 3389 | Critical | Restrict to Bastion subnet or specific IPs |
| Service endpoints where private endpoints available | Medium | Migrate to private endpoints |
| No WAF on internet-facing Application Gateway | High | Add WAF v2 with OWASP ruleset |
| Subnets without NSG associations | High | Associate NSG with deny-all default |
| No forced tunneling — egress bypassing firewall | High | Add UDR pointing to firewall |

---

## DNS Considerations

- Private DNS zones must be linked to all VNets that need resolution
- Use Azure Private DNS Resolver for hybrid (on-prem ↔ Azure) resolution
- Split-brain DNS: public zone for external access, private zone for internal
- Verify DNS resolution after deploying private endpoints — broken DNS is the #1 private endpoint issue

## Related Skills

- `security-review-framework` — Full security review checklist
- `secrets-management-audit` — Authentication and secrets hardening
