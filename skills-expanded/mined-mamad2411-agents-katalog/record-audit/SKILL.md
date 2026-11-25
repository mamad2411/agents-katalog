# Skill: DNS Record Audit (`dns_record_audit`)

Audit DNS zones for stale records, orphaned entries, incorrect TTLs, missing reverse DNS, CNAME-at-apex issues, and other hygiene problems that degrade reliability and security.

---

## Audit Checklist

| Check | Risk | Severity |
|---|---|---|
| **Stale A records** | Point to decommissioned IPs — dangling DNS risk (subdomain takeover) | Critical |
| **Orphaned CNAME records** | Point to deleted resources (e.g., deleted App Service, S3 bucket) | Critical |
| **Incorrect TTLs** | Too high = slow failover; too low = excessive DNS query volume | Medium |
| **Missing reverse DNS (PTR)** | Email deliverability issues, compliance audit failures | Medium |
| **CNAME at zone apex** | RFC violation — causes resolution failures in some resolvers | High |
| **Duplicate records** | Conflicting A records for the same name, unexpected round-robin | Medium |
| **Missing SPF/DKIM/DMARC** | Email spoofing risk | High |
| **Wildcard record conflicts** | Wildcard matches names that should not resolve | Medium |

---

## Stale and Orphaned Record Detection

### Azure

```bash
# List all A records in a zone
az network dns record-set a list --resource-group myRG --zone-name contoso.com \
  --query '[].{Name:name,TTL:ttl,IPs:aRecords[].ipv4Address}' --output table

# Check if IPs are still allocated in Azure
az network public-ip list --query '[].{Name:name,IP:ipAddress}' --output table

# List all CNAME records and check targets
az network dns record-set cname list --resource-group myRG --zone-name contoso.com \
  --query '[].{Name:name,Target:cnameRecord.cname}' --output table

# For private zones
az network private-dns record-set a list --resource-group myRG --zone-name internal.contoso.com \
  --output table
```

### AWS

```bash
# List all records in a hosted zone
aws route53 list-resource-record-sets --hosted-zone-id Z0123456789 \
  --query 'ResourceRecordSets[?Type==`A`].[Name,ResourceRecords[0].Value]' --output table

# Check if IPs map to active EC2 instances
aws ec2 describe-addresses --query 'Addresses[].{IP:PublicIp,InstanceId:InstanceId,AllocationId:AllocationId}' --output table
```

### GCP

```bash
# List all record sets in a zone
gcloud dns record-sets list --zone=my-zone --format='table(name,type,ttl,rrdatas)'

# Check if IPs are active
gcloud compute addresses list --format='table(name,address,status,users)'
```

### Subdomain Takeover Risk

A **dangling CNAME** is a critical security risk. If a CNAME points to a cloud resource that has been deleted (e.g., `app.contoso.com → myapp.azurewebsites.net`), an attacker can register that resource name and serve malicious content under your domain.

**Detection:**
```bash
# Test if CNAME target is active
dig +short app.contoso.com    # returns CNAME target
dig +short myapp.azurewebsites.net  # if NXDOMAIN or unclaimed → vulnerable

# Check Azure-specific services prone to takeover
# azurewebsites.net, cloudapp.azure.com, trafficmanager.net, blob.core.windows.net
```

**Mitigation:** Delete DNS records before deleting cloud resources. Use domain verification (Azure App Service domain verification, custom domain validation).

---

## TTL Audit

| Record Type | Recommended TTL | Why |
|---|---|---|
| A / AAAA (stable) | 300s (5 min) | Balances cache efficiency and change agility |
| A / AAAA (failover) | 60s | Fast failover for health-checked records |
| CNAME | 300–3600s | Moderate caching, rarely changes |
| MX | 3600s (1 hour) | Email routing changes are infrequent |
| NS | 172800s (48 hours) | Delegation rarely changes, high caching reduces upstream load |
| TXT (SPF/DKIM) | 3600s | Changes are planned, not emergency |
| SOA minimum (negative TTL) | 300s | How long to cache NXDOMAIN responses |

```bash
# Find records with suspiciously high TTLs (> 1 day)
az network dns record-set list --resource-group myRG --zone-name contoso.com \
  --query '[?ttl > `86400`].{Name:name,Type:type,TTL:ttl}' --output table

# Find records with very low TTLs (< 60s) that aren't failover records
az network dns record-set list --resource-group myRG --zone-name contoso.com \
  --query '[?ttl < `60`].{Name:name,Type:type,TTL:ttl}' --output table
```

---

## CNAME at Apex Issues

The DNS RFC (RFC 1034) prohibits CNAME records at the zone apex (e.g., `contoso.com CNAME something.else.com`) because CNAME cannot coexist with other record types, and the apex always has SOA and NS records.

**Cloud solutions:**
- **Azure**: Use **alias records** — an A or AAAA record that points to an Azure resource (Traffic Manager, Front Door, public IP) and auto-updates when the resource IP changes.
- **AWS**: Use **alias records** in Route 53 — A or AAAA alias to ALB, CloudFront, S3, etc. No charge for alias queries to AWS resources.
- **GCP**: No native alias records. Use **A records** with automation to update IPs, or use a CDN/LB with a stable IP.

```bash
# Azure alias record at apex
az network dns record-set a create --resource-group myRG --zone-name contoso.com \
  --name "@" --target-resource /subscriptions/.../frontDoors/myFD

# AWS alias record at apex
aws route53 change-resource-record-sets --hosted-zone-id Z0123456789 \
  --change-batch '{
    "Changes": [{"Action":"CREATE","ResourceRecordSet":{
      "Name":"contoso.com","Type":"A",
      "AliasTarget":{"HostedZoneId":"Z2FDTNDATAQYW2","DNSName":"d1234.cloudfront.net","EvaluateTargetHealth":true}
    }}]}'
```

---

## Email DNS Audit (SPF/DKIM/DMARC)

```bash
# Check SPF record
dig +short TXT contoso.com | grep spf
# Expected: "v=spf1 include:spf.protection.outlook.com -all"

# Check DMARC record
dig +short TXT _dmarc.contoso.com
# Expected: "v=DMARC1; p=reject; rua=mailto:dmarc@contoso.com"

# Check DKIM (example for Microsoft 365)
dig +short CNAME selector1._domainkey.contoso.com
```

**Analysis only — verify against vendor documentation before applying.**
