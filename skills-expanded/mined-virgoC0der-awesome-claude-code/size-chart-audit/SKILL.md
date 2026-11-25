---
name: size-chart-audit
description: Use when auditing TikTok Shop listings for size chart coverage - checking which categories support size charts, which listings are missing them, and whether DTC has size chart images to extract.
---

# Size Chart Audit Workflow

Audit a TikTok Shop merchant's listings to determine size chart coverage and identify gaps.

## Workflow Steps

### 1. Query Active Listings

Get all active listings for the org from `products-p-listings`:

```sql
SELECT product_listing_id, product, sales_channel_product_id, sales_channel_store_key
FROM product_listings
WHERE organization_id = '{org_id}' AND state = 'active'
  AND sales_channel_store_key = '{store_key}'
LIMIT 500
```

From the `product` JSON field, extract:
- `product.categories[0].sales_channel_id` — TikTok category ID
- `product.size_chart.images` — existing size chart (empty array = none)
- `product.title` — product title

### 2. Check Category Size Chart Support

For each unique category ID, call the categories/rules API:

```bash
curl 'http://pltf-pd-product-listings.as-in.com/api/v1/categories/rules?external_category_id={cat_id}&sales_channel_store_key={store_key}&sales_channel_platform=tiktok-shop&organization_id={org_id}' \
  --header "am-api-key: ${AM_API_KEY}"
```

Check `data.rule.size_chart.is_supported` (boolean). Only supported categories can have size charts.

### 3. Identify Missing Size Charts

Cross-reference:
- Listings in categories where `is_supported = true`
- Listings where `product.size_chart.images` is empty

This gives the list of listings that *can* have a size chart but *don't*.

### 4. Check DTC for Size Charts

For missing listings, trace back to the DTC product URL via DB chain:

```
listing_id
  -> products-p-listings.products_center_product_id
  -> products-p-core.connectors_product_id
  -> connectors-p-product.product_url
```

Then fetch `{product_url}.json` from Shopify and check:
1. `product.body_html` — search for size chart keywords ("size chart", "size guide", etc.)
2. `product.images` — check alt text/filenames for size-related keywords
3. **Note**: Many merchants embed size charts as plain images in descriptions (e.g., alicdn URLs) with no keywords. These can only be identified by visual inspection. Flag them for manual review.

### 5. Output CSV

Write to `data/{org_id_prefix}_listings.csv` with columns:
- `listing_id`, `title`, `category_id`, `size_chart_supported`, `has_size_chart`

### 6. Update Notion

Update the merchant's Notion page with:
- Total active listings and category count
- Which categories support size chart (with listing counts)
- Listings already with size chart vs missing
- Missing listings table with: listing ID, category, title, DTC link, DTC size chart status

## Required Inputs

- **Organization ID**: AfterShip org_id
- **Store Key**: TikTok Shop store key (from `sales_channel_store_key` in DB)
- **Notion page URL**: For documenting results (optional)

## Environment

Set before running any API call:

```bash
export AM_API_KEY=<your-am-api-key>
```


## API Reference

### Categories Rules API
- Endpoint: `http://pltf-pd-product-listings.as-in.com/api/v1/categories/rules`
- Auth header: `am-api-key: ${AM_API_KEY}` — set via env var, never hardcode
- Size chart support: `data.rule.size_chart.is_supported`
- **Not** in `data.rules[]` — it's `data.rule` (singular)

### DB Access

Go query tool at `~/.claude/skills/database/scripts/go/`:
```bash
go run query_any_db.go -db {db_name} -q "{sql}"
```

Databases: `connectors-p-product`, `products-p-core`, `products-p-listings`
