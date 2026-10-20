# Skill: Retail / Live Pricing APIs (`price_skill_retail_prices_api`)

**This skill is the mandatory source of truth for every live Azure network price, and the entry point for the equivalent AWS and GCP pricing APIs.** Never quote a hard-coded, cached, or model-recalled rate. Always *fetch* the current price from the provider's pricing API, then *cite* the exact query, the returned fields, and the retrieval timestamp. If — and only if — a provider's API is unreachable, you may present a number explicitly flagged `INDICATIVE — not fetched from a live pricing API`.

---

## Azure — Azure Retail Prices API (authoritative for Azure)

**Endpoint:** `https://prices.azure.com/api/retail/prices` — anonymous, **no authentication**, no Azure subscription required.

Add `?api-version=2023-01-01-preview` to receive `savingsPlan[]` and reservation fields:

```
https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
```

### Query model — OData `$filter` + currency

Build an OData `$filter` and always pin the currency with `&currencyCode='USD'` (or the user's currency):

```
$filter=serviceName eq 'Bandwidth' and armRegionName eq 'eastus' and priceType eq 'Consumption'
&currencyCode='USD'
```

**Network query patterns:**

| Need | `$filter` (combine with `&currencyCode='USD'`) |
|---|---|
| Internet egress / data transfer | `serviceName eq 'Bandwidth' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| VPN Gateway | `serviceFamily eq 'Networking' and armRegionName eq 'eastus' and armSkuName eq '<sku>' and priceType eq 'Consumption'` |
| ExpressRoute | `serviceFamily eq 'Networking' and serviceName eq 'ExpressRoute' and armRegionName eq 'eastus'` |
| Azure Firewall | `serviceFamily eq 'Networking' and serviceName eq 'Azure Firewall' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| NAT Gateway | `serviceFamily eq 'Networking' and serviceName eq 'NAT Gateway' and armRegionName eq 'eastus'` |
| Standard Public IP | `serviceFamily eq 'Networking' and serviceName eq 'Virtual Network' and armSkuName eq 'Standard' and armRegionName eq 'eastus'` |
| Load Balancer | `serviceFamily eq 'Networking' and serviceName eq 'Load Balancer' and armRegionName eq 'eastus'` |
| Application Gateway | `serviceFamily eq 'Networking' and serviceName eq 'Application Gateway' and armRegionName eq 'eastus'` |
| Front Door | `serviceFamily eq 'Networking' and serviceName eq 'Azure Front Door Service' and armRegionName eq 'eastus'` |
| Private Link / Private Endpoint | `serviceFamily eq 'Networking' and serviceName eq 'Virtual Network Private Link' and armRegionName eq 'eastus'` |
| DNS | `serviceFamily eq 'Networking' and serviceName eq 'Azure DNS'` |

> Do **not** assume the exact `serviceName`/`meterName`. Confirm them from the response — start with a broad filter (e.g. `serviceFamily eq 'Networking'` + region), inspect `serviceName`/`meterName`/`productName`, then narrow.

### Response fields to use and cite

Cite these from each returned item:

| Field | Use |
|---|---|
| `retailPrice` | Public list price (use this to quote) |
| `unitPrice` | Price per unit (may equal `retailPrice`; differs for tiered/reservation rows) |
| `unitOfMeasure` | e.g. `1 GB`, `1 Hour`, `1/Month` — quote alongside the number |
| `armRegionName` | Region the price applies to (prices are region-specific) |
| `armSkuName` / `skuName` | SKU identifier |
| `productName` | Human-readable product |
| `meterName` | Specific meter (egress tier, gateway hour, etc.) |
| `type` | `Consumption`, `Reservation`, or `DevTestConsumption` |
| `reservationTerm` | `1 Year` / `3 Years` (reservation rows) |
| `savingsPlan[]` | Savings-plan rates (preview api-version only) |
| `effectiveStartDate` | When the price became effective — **always cite this** |

### Pitfalls to encode

1. **Paging:** results are paged. The response includes `NextPageLink` — **follow it until it is `null`**, accumulating `Items`. A single call returns only the first 100 items.
2. **Egress is tiered with a free allowance:** internet egress is metered under `serviceName 'Bandwidth'` with **multiple tiered meters** and a **monthly free allowance**. Model the tiers and the free allowance **from the returned meters** — never from a memorized number.
3. **Region-specific:** every price is per `armRegionName`. Quote the region you queried; do not generalize one region's price to another.
4. **Confirm meter identity:** verify the exact `serviceName`/`meterName` from the response rather than assuming a meter exists or is named as expected.
5. **Consumption vs Reservation:** filter `priceType eq 'Consumption'` for pay-as-you-go; query reservation/savings-plan rows separately for committed-use comparisons.

### Worked example — egress (curl)

```bash
curl -s "https://prices.azure.com/api/retail/prices?\$filter=serviceName eq 'Bandwidth' and armRegionName eq 'eastus' and priceType eq 'Consumption'&currencyCode='USD'" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(i['meterName'], i['retailPrice'], i['unitOfMeasure'], i['effectiveStartDate']) for i in d['Items']]"
```

### Worked example — PowerShell with `NextPageLink` loop

```powershell
$base = "https://prices.azure.com/api/retail/prices"
$filter = "serviceFamily eq 'Networking' and armRegionName eq 'eastus' and priceType eq 'Consumption'"
$url = "$base`?`$filter=$([uri]::EscapeDataString($filter))&currencyCode='USD'"

$items = @()
while ($url) {
    $resp  = Invoke-RestMethod -Uri $url -Method Get
    $items += $resp.Items
    $url    = $resp.NextPageLink   # follow paging until null
}

$items |
  Select-Object meterName, armSkuName, retailPrice, unitOfMeasure, armRegionName, effectiveStartDate |
  Sort-Object retailPrice | Format-Table -AutoSize
```

### Worked example — Python (`requests`)

```python
import requests

BASE = "https://prices.azure.com/api/retail/prices"
params = {
    "$filter": "serviceName eq 'Azure Firewall' and armRegionName eq 'eastus' "
               "and priceType eq 'Consumption'",
    "currencyCode": "'USD'",
}

items, url = [], BASE
while url:
    r = requests.get(url, params=params if url == BASE else None, timeout=30)
    r.raise_for_status()
    data = r.json()
    items.extend(data["Items"])
    url = data.get("NextPageLink")

for i in items:
    print(i["meterName"], i["retailPrice"], i["unitOfMeasure"],
          i["armRegionName"], i["effectiveStartDate"])
```

### Worked example — Consumption vs 1-yr RI vs 3-yr RI

For services with reservations (ExpressRoute, gateways), query each `type` and compare. Use the preview api-version so reservation/savings-plan rows are returned:

```bash
# Consumption
curl -s "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName eq 'ExpressRoute' and armRegionName eq 'eastus' and priceType eq 'Consumption'&currencyCode='USD'"

# Reservations (1 Year / 3 Years appear in reservationTerm)
curl -s "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName eq 'ExpressRoute' and armRegionName eq 'eastus' and priceType eq 'Reservation'&currencyCode='USD'"
```

Build the comparison from the returned rows:

| Option | Source field | Quote |
|---|---|---|
| Pay-as-you-go | `retailPrice` where `type eq 'Consumption'` | per `unitOfMeasure` |
| 1-year reserved | `retailPrice` where `reservationTerm eq '1 Year'` | amortized monthly |
| 3-year reserved | `retailPrice` where `reservationTerm eq '3 Years'` | amortized monthly |

Always show the `effectiveStartDate` and retrieval timestamp next to each figure.

---

## AWS — AWS Price List Query API

The Azure Retail Prices API is authoritative **only for Azure**. For AWS network prices, fetch from the **AWS Price List Query API** (`api.pricing.us-east-1.amazonaws.com`, action `GetProducts`):

```bash
# Requires AWS credentials. Pricing data is global; query the us-east-1 (or ap-south-1) endpoint.
aws pricing get-products \
  --region us-east-1 \
  --service-code AmazonVPC \
  --filters 'Type=TERM_MATCH,Field=regionCode,Value=us-east-1' \
  --output json
```

- Service codes: `AmazonVPC` (NAT Gateway, Private Link, data transfer), `AWSDataTransfer` (egress), `AmazonVPN`, `AWSDirectConnect`, `ElasticLoadBalancing`, `AWSNetworkFirewall`.
- Parse `PriceList[]` → `terms.OnDemand.*.priceDimensions.*` for `pricePerUnit.USD`, `unit`, and `description`. Cite the `serviceCode`, region filter, unit price, currency, and retrieval timestamp.

## GCP — Cloud Billing Catalog API

For GCP, fetch from the **Cloud Billing Catalog API** (`cloudbilling.googleapis.com/v1/services/.../skus`):

```bash
# Find the networking service id via the services list, then list its SKUs.
curl -s "https://cloudbilling.googleapis.com/v1/services?key=$GCP_API_KEY"
curl -s "https://cloudbilling.googleapis.com/v1/services/<SERVICE_ID>/skus?key=$GCP_API_KEY"
```

- Filter SKUs by `category.resourceFamily` / `serviceRegions` for egress, Cloud VPN, Interconnect, Cloud Load Balancing, Cloud NAT.
- Parse `pricingInfo[].pricingExpression.tieredRates[].unitPrice` (`units` + `nanos`) and `usageUnit`. Cite the `skuId`/`description`, region, unit price, currency, and retrieval timestamp.

## Fallback rule

If a provider's pricing API cannot be reached, present any number you must give as:

> **`INDICATIVE — not fetched from a live pricing API`** (provider page: `<url>`, retrieved: `<n/a — API unreachable>`)

Never silently substitute a memorized or cached rate for a live one.

---

## Citation template

Every quoted Azure price must be accompanied by its provenance:

```markdown
**Source (Azure Retail Prices API):**
- `$filter`: serviceName eq 'Bandwidth' and armRegionName eq 'eastus' and priceType eq 'Consumption'
- Region: eastus · SKU/meter: <armSkuName> / <meterName>
- retailPrice: <value> per <unitOfMeasure> · currency: USD
- effectiveStartDate: <date> · retrieved: <YYYY-MM-DDTHH:MMZ>
```

Use the equivalent block (service code / SKU id, region, unit price, currency, retrieval timestamp) for AWS and GCP.

---

Pricing is fetched live — never quote hard-coded, cached, or memorized rates; cite the query, returned fields, and retrieval timestamp.
**Analysis only — verify against vendor documentation before applying.**
