# Skill: Network Segmentation Design (nsec_segmentation-design)

Design network segmentation strategies using micro-segmentation patterns, tier-based architectures, environment isolation, and zero-trust principles across Azure, AWS, and GCP.

---

## Micro-Segmentation Patterns

Micro-segmentation moves security enforcement from the network perimeter to individual workloads, limiting the blast radius of a compromise by preventing lateral movement between workloads even within the same subnet.

### Workload-Based Segmentation
Instead of relying on subnet boundaries for security, apply security policies based on workload identity — what the application does, not where it sits in the network.

**Azure Application Security Groups (ASGs)**:
ASGs allow grouping VMs by application role and referencing those groups in NSG rules, eliminating the need to manage individual IP addresses.

```bash
# Create ASGs for workload tiers
az network asg create --name WebServers --resource-group MyRG
az network asg create --name AppServers --resource-group MyRG
az network asg create --name DbServers --resource-group MyRG

# NSG rule: only WebServers can reach AppServers on port 8080
az network nsg rule create \
  --nsg-name AppSubnetNSG --resource-group MyRG \
  --name AllowWebToApp --priority 100 \
  --direction Inbound --access Allow --protocol TCP \
  --source-asgs WebServers \
  --destination-asgs AppServers \
  --destination-port-ranges 8080

# NSG rule: only AppServers can reach DbServers on port 5432
az network nsg rule create \
  --nsg-name DbSubnetNSG --resource-group MyRG \
  --name AllowAppToDb --priority 100 \
  --direction Inbound --access Allow --protocol TCP \
  --source-asgs AppServers \
  --destination-asgs DbServers \
  --destination-port-ranges 5432
```

**AWS Security Group Chaining**:
Reference one SG as the source in another SG's inbound rules, creating a chain of trust that follows application traffic flow.

```bash
# Create SGs for each tier
WEB_SG=$(aws ec2 create-security-group --group-name web-sg --vpc-id vpc-xxx --description "Web tier" --query 'GroupId' --output text)
APP_SG=$(aws ec2 create-security-group --group-name app-sg --vpc-id vpc-xxx --description "App tier" --query 'GroupId' --output text)
DB_SG=$(aws ec2 create-security-group --group-name db-sg --vpc-id vpc-xxx --description "DB tier" --query 'GroupId' --output text)

# Chain: Internet → Web (443) → App (8080) → DB (5432)
aws ec2 authorize-security-group-ingress --group-id $WEB_SG --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $APP_SG --protocol tcp --port 8080 --source-group $WEB_SG
aws ec2 authorize-security-group-ingress --group-id $DB_SG --protocol tcp --port 5432 --source-group $APP_SG
```

**GCP Service Account-Based Firewall Rules**:
Target firewall rules by service account identity rather than network tags (more secure — service accounts are IAM-managed and cannot be changed by instance users).

```bash
# Allow only web-tier service account to reach app-tier on port 8080
gcloud compute firewall-rules create allow-web-to-app \
  --direction=INGRESS --action=ALLOW --rules=tcp:8080 \
  --source-service-accounts=web-tier@project.iam.gserviceaccount.com \
  --target-service-accounts=app-tier@project.iam.gserviceaccount.com
```

---

## Tier-Based Segmentation (Web / App / DB)

The classic three-tier architecture maps naturally to network segmentation:

### Subnet Design
| Tier | Subnet | Allowed Inbound | Allowed Outbound |
|------|--------|-----------------|------------------|
| Web | 10.0.1.0/24 | Internet (80/443), LB health probes | App tier (8080) |
| App | 10.0.2.0/24 | Web tier (8080), management (22/3389 from bastion) | DB tier (5432/3306), external APIs (443) |
| DB | 10.0.3.0/24 | App tier (5432/3306) | Backup storage, monitoring agents |
| Management | 10.0.4.0/24 | VPN/Bastion (22/3389) | All tiers (management) |

### Key Principles
- **No direct internet access for app or DB tiers** — route through web tier or API gateway.
- **No direct DB access from web tier** — force all data access through the application layer.
- **Dedicated management subnet** with bastion host or Azure Bastion / AWS SSM Session Manager for administrative access.
- **Outbound restrictions on DB tier** — prevent data exfiltration by allowing only backup and monitoring destinations.

---

## Environment Isolation (Production / Staging / Development)

### Isolation Strategies

**Separate VNets/VPCs per environment** (strongest isolation):
- Each environment in its own VNet/VPC with no peering between prod and non-prod.
- Shared services (DNS, monitoring, identity) accessed via Private Link or service endpoints.
- Prevents accidental cross-environment access and credential reuse.

**Separate subnets with NSG isolation** (moderate isolation):
- All environments in the same VNet/VPC but different subnets.
- NSG/SG rules deny all traffic between environment subnets.
- Simpler management but higher risk of misconfiguration or rule drift.

**Separate subscriptions/accounts** (organizational isolation):
- Azure: separate subscriptions for prod vs non-prod under different management groups.
- AWS: separate accounts in an AWS Organization with SCPs restricting cross-account networking.
- GCP: separate projects with VPC Service Controls preventing cross-project access.

### Recommended Architecture
```
Production VNet (10.1.0.0/16) — isolated subscription/account
├── Web subnet (10.1.1.0/24) — NSG: deny all except prod LB
├── App subnet (10.1.2.0/24) — NSG: deny all except prod web tier
└── DB subnet  (10.1.3.0/24) — NSG: deny all except prod app tier

Staging VNet (10.2.0.0/16) — separate subscription/account
├── Web subnet (10.2.1.0/24)
├── App subnet (10.2.2.0/24)
└── DB subnet  (10.2.3.0/24)

No VNet peering between prod and staging. Access to shared services via Private Link.
```

---

## Zero-Trust Segmentation Principles

1. **Default deny all** — every flow must be explicitly allowed. Start with deny-all baselines, then add specific allow rules.
2. **Identity-aware access** — prefer ASG/service-account-based rules over IP-based rules. IPs change; identities persist.
3. **Encrypt east-west traffic** — use mutual TLS (mTLS) or IPsec between workloads, even within the same subnet.
4. **Continuous verification** — regularly audit rules against actual traffic patterns (flow logs). Remove rules that haven't matched traffic in 30+ days.
5. **Least-privilege network access** — allow only the specific protocol, port, and source required. Avoid port ranges when a single port suffices.
**Analysis only — verify against vendor documentation before applying.**
