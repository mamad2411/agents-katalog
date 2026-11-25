---
name: size-chart-sync
description: Use when syncing size charts to TikTok Shop listings for a Shopify merchant - fetching products, resolving listing IDs, categorizing by product type, generating batch payloads, checking DB for missing size charts, and updating Notion progress docs.
---

# Size Chart Sync Workflow

End-to-end workflow for syncing size chart images to TikTok Shop listings for Shopify merchants.

## Workflow Steps

### 1. Fetch Products

Fetch all products from the Shopify store via paginated `/collections/all/products.json` API.

```
GET {store_url}/collections/all/products.json?limit=250&page={n}
```

- Cache results to `data/{store_name}_products.json`
- Use `--no-cache` to force re-fetch
- Key fields: `id` (shopify_product_id), `handle`, `title`, `product_type`

### 2. Resolve Listing IDs

Map Shopify product IDs to AfterShip listing IDs via 3-step DB chain:

```
shopify_product_id (external_product_id)
  -> connectors-p-product.product_id    (connectors_product_id)
  -> products-p-core.product_id         (products_center_product_id)
  -> products-p-listings.product_listing_id  (listing_id)
```

- Query in batches of 50
- Filter by `organization_id` in step 1
- Not all products will resolve (some may not have listings)

### 3. Write CSV

Output to `data/{store_name}_products.csv` with columns:

- `listing_id`, `shopify_product_id`, `handle`, `title`
- Remove rows without `listing_id`
- If merchant has multiple size charts by category: add `category` and `size_chart_url` columns

### 4. Categorize Products (if needed)

Use Shopify `product_type` field to classify. Fall back to title/handle keywords for empty types.

Typical mapping:

| product_type | category |
|---|---|
| tops, outerwear, jackets & vest, kimonos & cardigans | tops |
| bottoms | bottoms |
| dresses & rompers | dresses |
| shoes | shoes |
| jeans (title contains "jean") | denim |
| accessories | skip (no size chart) |

### 5. Generate Batch Payloads

Create JSON payload files in `generated_size_charts/{store_name}/payloads/`.

Payload format:
```json
{
    "group_name": "batch_edit_product_listings_product_attributes",
    "organization_id": "{org_id}",
    "store_key": "{store_key}",
    "platform": "shopify",
    "inputs": {
        "edit_attributes_task": {
            "product_listing_ids": ["id1", "id2", ...],
            "size_chart": {
                "images": [{
                    "sales_channel_id": "",
                    "url": "{size_chart_image_url}"
                }]
            }
        }
    }
}
```

Grouping rules:
- Same size chart URL -> same payload file
- Split into batches (typically 50 or 200 per file)
- File naming: `{category}.json` or `{category}_batch_{nn}.json`

### 6. Check Existing Size Charts

Query `products-p-listings` to find which listings already have size charts:

```sql
SELECT product_listing_id, product FROM product_listings
WHERE product_listing_id IN (...) LIMIT N
```

Size chart is in the `product` JSON field at `product.size_chart.images`. Empty array = no size chart.

Generate separate payloads for missing ones in `payloads_missing/` directory.

### 7. Update Notion

Update the merchant's Notion page with:
- Total active listings count
- Category breakdown with counts
- Size chart URLs used
- Completion status

## Required Inputs from User

- **Store URL**: Shopify store domain (e.g., `https://example.com`)
- **Organization ID**: AfterShip org_id
- **Store Key**: AfterShip store_key for payloads
- **Size Chart URLs**: GCS URLs for size chart images (one universal or per-category)
- **Notion page URL**: For progress tracking (optional)

## Key Directories

- `data/` - CSV files and cached product JSON
- `generated_size_charts/{store_name}/payloads/` - Batch payload files
- `scripts/` - Per-store fetch scripts

## DB Access

Uses Go query tool at `~/.claude/skills/database/scripts/go/`:
```bash
go run query_any_db.go -db {db_name} -q "{sql}"
```

Databases: `connectors-p-product`, `products-p-core`, `products-p-listings`
