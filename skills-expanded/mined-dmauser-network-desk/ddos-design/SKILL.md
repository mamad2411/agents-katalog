# Skill: DDoS Protection Design (nsec_ddos-design)

Design and configure DDoS protection across Azure, AWS, and GCP. This skill covers protection tiers, tuning, alerting, and response procedures.

---

## Azure DDoS Protection

### Protection Tiers

**DDoS Network Protection** (formerly DDoS Protection Standard):
- Applied per Virtual Network. Protects all public IP resources within the VNet.
- Automatic traffic profiling and adaptive tuning — learns normal traffic patterns over 30+ days and detects anomalies.
- Mitigation capacity: absorbs multi-terabit volumetric attacks using Azure's global scrubbing infrastructure.
- Attack telemetry: real-time metrics (under attack, packets dropped, packets forwarded), diagnostic logs, attack analytics.
- Cost protection: service credits for resource scale-out costs incurred during a verified DDoS attack.
- Rapid Response: access to the DDoS Rapid Response (DRR) team during active attacks.
- Pricing: ~$2,944/month base + per-resource overage above 100 protected resources.

**DDoS IP Protection**:
- Applied per public IP address. No VNet-wide coverage.
- Same mitigation engine as Network Protection but without DRR support, cost protection, or WAF discounts.
- Pricing: ~$199/month per protected IP.
- Suitable for smaller deployments or specific high-value endpoints.

### Configuration
```bash
# Create DDoS Protection Plan
az network ddos-protection create \
  --name MyDDoSPlan --resource-group MyRG

# Associate with VNet
az network vnet update \
  --name MyVNet --resource-group MyRG \
  --ddos-protection-plan MyDDoSPlan --ddos-protection true

# Enable diagnostic logging for attack telemetry
az monitor diagnostic-settings create \
  --name DDoSLogs \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/publicIPAddresses/{pip} \
  --logs '[{"category":"DDoSProtectionNotifications","enabled":true},{"category":"DDoSMitigationFlowLogs","enabled":true},{"category":"DDoSMitigationReports","enabled":true}]' \
  --workspace /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{ws}
```

---

## AWS Shield

### Shield Standard
- Automatic, free L3/L4 DDoS protection for all AWS resources.
- Protects against SYN/ACK floods, UDP reflection attacks, and other volumetric attacks.
- No configuration required — always on for CloudFront, Route 53, ALB, NLB, EC2, and Global Accelerator.
- No visibility into attacks (no metrics or notifications at Standard tier).

### Shield Advanced
- $3,000/month per organization + data transfer fees.
- L3/L4/L7 DDoS protection with advanced detection and mitigation.
- **DDoS Response Team (DRT)**: 24/7 access to AWS DDoS experts who can proactively mitigate attacks and tune WAF rules during incidents.
- **Cost protection**: Credits for scaling charges incurred during DDoS attacks (EC2, ELB, CloudFront, Route 53, AWS Global Accelerator).
- **Enhanced metrics**: CloudWatch metrics for DDoS attack vectors, volume, and duration.
- **Proactive engagement**: AWS can proactively contact you during detected attacks (requires health check configuration).
- **WAF integration**: AWS WAF included at no additional cost for resources protected by Shield Advanced.

```bash
# Enable Shield Advanced (organization-level)
aws shield create-subscription

# Add resource protection
aws shield create-protection \
  --name "ProdALB" \
  --resource-arn arn:aws:elasticloadbalancing:us-east-1:123456789:loadbalancer/app/my-alb/xxx

# Associate health check for proactive engagement
aws shield associate-health-check \
  --protection-id xxx \
  --health-check-arn arn:aws:route53:::healthcheck/xxx
```

---

## GCP Cloud Armor

### DDoS Protection
Cloud Armor provides DDoS protection for resources behind Google Cloud HTTP(S) Load Balancing (external Application Load Balancers).

**Standard Tier**: Always-on volumetric DDoS protection. Absorbs L3/L4 volumetric attacks at Google's edge before they reach the customer's load balancer. No additional configuration needed.

**Cloud Armor Managed Protection Plus**: Advanced adaptive protection using ML-based anomaly detection. Automatically generates suggested WAF rules to block application-layer DDoS attacks. Requires security policy attachment to backend services.

### Security Policies
```bash
# Create Cloud Armor security policy
gcloud compute security-policies create my-ddos-policy \
  --description "DDoS and WAF protection"

# Enable adaptive protection
gcloud compute security-policies update my-ddos-policy \
  --enable-layer7-ddos-defense

# Add rate-limiting rule
gcloud compute security-policies rules create 1000 \
  --security-policy my-ddos-policy \
  --action throttle \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60 \
  --conform-action allow \
  --exceed-action deny-429 \
  --enforce-on-key IP

# Attach policy to backend service
gcloud compute backend-services update my-backend \
  --security-policy my-ddos-policy --global
```

---

## Protection Tuning

### Traffic Profiling
- Allow 30+ days of baseline traffic collection before relying on adaptive thresholds.
- Azure DDoS Protection automatically builds traffic profiles per public IP.
- Review auto-tuned thresholds and adjust if application has known traffic patterns (e.g., scheduled batch jobs, marketing campaigns).

### Threshold Configuration
- **SYN packets/sec**: Baseline SYN rate × 3–5x for trigger threshold.
- **UDP packets/sec**: Baseline UDP rate × 5–10x (UDP is commonly amplified in attacks).
- **Total packets/sec**: Baseline × 3x for initial detection, × 10x for full mitigation.

### False Positive Mitigation
- Whitelist known scanner IPs (monitoring services, CDN health checks).
- Exclude known high-volume sources (partner APIs, internal services accessing public endpoints).
- Use geo-based rules to allow traffic from expected regions while blocking unexpected origins.

---

## Alerting Configuration

### Azure DDoS Alerts
```bash
# Create alert for DDoS attack detection
az monitor metrics alert create \
  --name "DDoSAttackAlert" \
  --resource-group MyRG \
  --scopes /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/publicIPAddresses/{pip} \
  --condition "avg IfUnderDDoSAttack > 0" \
  --window-size 5m \
  --action /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Insights/actionGroups/{ag}
```

### AWS Shield Advanced Alerts
- Configure CloudWatch alarms on `DDoSDetected` and `DDoSAttackBitsPerSecond` metrics.
- Enable SNS notifications for Shield events.
- Configure proactive engagement with Route 53 health checks for automatic DRT contact.

### GCP Cloud Armor Alerts
- Configure Cloud Monitoring alerts on `loadbalancing.googleapis.com/https/request_count` with filters for denied requests.
- Set up log-based metrics for Cloud Armor rule match events.
- Use Security Command Center for centralized DDoS event visibility.
**Analysis only — verify against vendor documentation before applying.**
