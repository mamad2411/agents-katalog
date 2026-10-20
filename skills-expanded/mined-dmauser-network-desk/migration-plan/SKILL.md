# Skill: DNS Migration Plan (`dns_migration_plan`)

Plan and execute DNS zone migrations between providers or from on-premises to cloud. Covers TTL preparation, zone export/import, parallel running, validation, delegation cutover, and rollback strategy.

---

## Migration Workflow

### Phase 1 — Pre-Migration (T-7 days)

**1. Export the source zone:**

```bash
# BIND zone file export (on-prem)
dig @source-dns contoso.com AXFR > contoso.com.zone

# Azure DNS export
az network dns zone export --resource-group myRG --name contoso.com --output-file contoso.com.zone

# AWS Route 53 — no native export; use CLI to list and transform
aws route53 list-resource-record-sets --hosted-zone-id Z0123456789 > records.json

# GCP Cloud DNS export
gcloud dns record-sets export records.yaml --zone=my-zone --zone-file-format
```

**2. Inventory all records:**

Create a record inventory spreadsheet:

| Name | Type | Value | TTL | Status | Notes |
|---|---|---|---|---|---|
| @ | A | 52.1.2.3 | 3600 | Active | Front Door VIP |
| www | CNAME | contoso.azurefd.net | 300 | Active | |
| mail | MX | 10 contoso-com.mail.protection.outlook.com | 3600 | Active | M365 |
| legacy-app | A | 10.1.1.50 | 86400 | Stale? | Verify with app team |

**3. Identify special records:**
- Alias/ALIAS records (not standard DNS — provider-specific).
- Failover/routing policy records (Route 53 weighted, latency, etc.).
- Records with health checks attached.
- DNSSEC-signed zones (require key migration or re-signing).

### Phase 2 — TTL Lowering (T-48h)

Lower TTLs on all records at the **source** zone to reduce cache persistence during cutover:

```bash
# Lower all A record TTLs to 60s (Azure example)
az network dns record-set a update --resource-group myRG --zone-name contoso.com \
  --name www --set ttl=60

# AWS — update TTL
aws route53 change-resource-record-sets --hosted-zone-id Z0123456789 \
  --change-batch '{
    "Changes": [{"Action":"UPSERT","ResourceRecordSet":{
      "Name":"www.contoso.com","Type":"CNAME","TTL":60,
      "ResourceRecords":[{"Value":"contoso.azurefd.net"}]
    }}]}'
```

**Wait the original TTL duration** before proceeding. If the old TTL was 3600s (1h), wait at least 1h after lowering so all caches expire with the old value.

**Do NOT lower NS record TTLs** aggressively — these are cached at the TLD level and lowering can cause excess load on TLD servers.

### Phase 3 — Parallel Zone Setup (T-24h)

Create the destination zone and import all records:

```bash
# Azure — import zone file
az network dns zone import --resource-group myRG --name contoso.com --file-name contoso.com.zone

# AWS — create records from JSON
# Transform exported records into change-batch format and apply
aws route53 change-resource-record-sets --hosted-zone-id ZNEW123456 --change-batch file://import-batch.json

# GCP — import zone file
gcloud dns record-sets import records.yaml --zone=my-zone --zone-file-format
```

**Validate all records match** between source and destination:

```bash
# Compare resolution from source and destination nameservers
dig @ns1.source-dns.com www.contoso.com A +short
dig @ns1-09.azure-dns.com www.contoso.com A +short
# Both should return identical results
```

### Phase 4 — Validation (T-4h)

Run comprehensive validation before switching delegation:

```bash
# Verify all records at destination
for record in www mail app api; do
  echo "--- $record.contoso.com ---"
  dig @ns1-09.azure-dns.com $record.contoso.com ANY +short
done

# Verify SOA serial is higher at destination
dig @ns1-09.azure-dns.com contoso.com SOA

# Verify MX records (email is high-impact)
dig @ns1-09.azure-dns.com contoso.com MX +short

# Verify TXT records (SPF, DMARC, domain verification)
dig @ns1-09.azure-dns.com contoso.com TXT +short
```

### Phase 5 — Delegation Cutover (T-0)

Update the NS records at the domain registrar to point to the new provider's nameservers:

```
contoso.com NS → ns1-09.azure-dns.com
contoso.com NS → ns2-09.azure-dns.net
contoso.com NS → ns3-09.azure-dns.org
contoso.com NS → ns4-09.azure-dns.info
```

**This is the point of no return** (within the NS TTL window). NS changes propagate based on the TLD's NS record TTL (typically 48h).

Monitor propagation:
```bash
# Check which nameservers are being used globally
dig contoso.com NS +trace
dig @8.8.8.8 contoso.com A +short
dig @1.1.1.1 contoso.com A +short
```

### Phase 6 — Post-Migration (T+48h)

1. **Keep source zone active** for at least 72h — some resolvers cache NS records longer than TTL.
2. **Restore normal TTLs** at the destination zone (300s for A records, 3600s for MX, etc.).
3. **Enable DNSSEC** at the destination if applicable (add DS record at registrar).
4. **Decommission source zone** only after confirming zero traffic via source provider's query logs.

---

## Rollback Plan

If issues are detected after delegation cutover:

1. **Revert NS records** at the registrar back to the source provider.
2. Source zone must still be running with all records intact.
3. Wait for NS TTL to expire (up to 48h).
4. **Faster rollback**: If the destination zone is misconfigured, fix the records there rather than reverting NS records — this is faster than waiting for NS propagation.

---

## Common Migration Mistakes

1. **Not lowering TTLs before cutover** — clients cache old records for hours/days after the switch.
2. **Forgetting MX or TXT records** — email delivery breaks, SPF validation fails.
3. **Deleting the source zone too early** — cached NS records still point clients to the source.
4. **DNSSEC complications** — switching providers with DNSSEC active requires careful key/DS record management. Disable DNSSEC at source, migrate, re-enable at destination.
5. **Provider-specific record types** — Route 53 alias records, Azure alias records, and GCP routing policies don't transfer between providers. Recreate using the destination provider's equivalent.

**Analysis only — verify against vendor documentation before applying.**
