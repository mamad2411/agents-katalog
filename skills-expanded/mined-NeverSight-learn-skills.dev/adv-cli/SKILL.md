---
name: adv-cli
description: Query Advance Commerce APIs using the adv CLI. Use when working with e-commerce data, product catalogs, inventory, orders, or when the user mentions Advance Commerce, e-commerce, product data, or adv.
---

# Advance Commerce CLI

Query Advance Commerce APIs using the `adv` command-line tool.

## Prerequisites

```bash
adv --version
export ADV_API_KEY='your-api-key'
export ADV_API_SECRET='your-api-secret'
adv auth status
```

## Authentication

- API key and secret from Advance Commerce
- Environment variables: `ADV_API_KEY`, `ADV_API_SECRET`
- Or: `adv auth login` for interactive setup

## Products

### List & Search

```bash
adv products list --limit 100
adv products search --query "laptop" --category electronics
adv products get PRODUCT_ID
```

### Catalog Management

```bash
adv products create --file product.json
adv products update PRODUCT_ID --price 999.99
adv products delete PRODUCT_ID --confirm
adv products bulk --file products.csv
```

## Inventory

```bash
adv inventory list --warehouse WAREHOUSE_ID
adv inventory get PRODUCT_ID --warehouse WAREHOUSE_ID
adv inventory update PRODUCT_ID --quantity 100 --warehouse WAREHOUSE_ID
adv inventory alerts --low-stock --threshold 10
```

## Orders

```bash
adv orders list --status pending --limit 50
adv orders get ORDER_ID --details
adv orders create --customer CUSTOMER_ID --items items.json
adv orders update ORDER_ID --status shipped --tracking TRACKING_NUM
adv orders cancel ORDER_ID --reason "Customer request"
```

## Customers

```bash
adv customers list --limit 100
adv customers get CUSTOMER_ID
adv customers search --email "customer@example.com"
adv customers orders CUSTOMER_ID --limit 20
```

## Reports & Analytics

```bash
adv reports sales --start 2024-06-01 --end 2024-06-30
adv reports inventory --warehouse WAREHOUSE_ID
adv analytics trends --metric revenue --days 30
adv export orders --start 2024-01-01 --format csv
```

## Agent Best Practices

1. **Pagination**: Use `--cursor` for large datasets
2. **Bulk operations**: Use CSV/JSON files for batch updates
3. **Date filters**: ISO 8601 format (YYYY-MM-DD)
4. **Rate limits**: Check response headers for limits
