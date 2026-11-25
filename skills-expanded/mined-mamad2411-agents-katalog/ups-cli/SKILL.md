---
name: ups-cli
description: Track UPS shipments and manage shipping using the ups CLI. Use when working with package tracking, shipping labels, rates, or when the user mentions UPS, package tracking, shipping, or ups.
---

# UPS CLI

Track and manage UPS shipments using the `ups` command-line tool.

## Prerequisites

```bash
ups --version
export UPS_API_KEY='your-api-key'
export UPS_USERNAME='your-username'
export UPS_PASSWORD='your-password'
ups auth status
```

## Authentication

- API key, username, and password from UPS Developer Kit
- Environment variables: `UPS_API_KEY`, `UPS_USERNAME`, `UPS_PASSWORD`

## Package Tracking

### Track Shipments

```bash
ups track TRACKING_NUMBER
ups track TRACKING_NUMBER --details
ups track TRACKING_NUMBER --proof-of-delivery
```

### Batch Tracking

```bash
ups track --file tracking-numbers.txt
ups track 1Z999AA10123456784 1Z999AA10234567895 --summary
```

### History

```bash
ups history --days 30 --status delivered
ups recent --limit 20
```

## Shipping Rates

```bash
ups rates --from "90210" --to "10001" --weight 5lbs
ups rates --from ZIP --to ZIP --weight WEIGHT --dimensions LxWxH --service ground
ups rates compare --from ZIP --to ZIP --weight 10lbs
```

## Shipping Labels

```bash
ups label create --from SHIPPER_JSON --to RECIPIENT_JSON --package PACKAGE_JSON
ups label void LABEL_ID --confirm
ups label reprint LABEL_ID
```

## Pickup & Drop-off

```bash
ups pickup schedule --date 2024-06-15 --time "14:00-16:00"
ups pickup cancel PICKUP_ID
ups locations --near "90210" --type "UPS Store"
```

## Agent Best Practices

1. **Tracking numbers**: Validate format before querying
2. **Rate shopping**: Use `compare` for best service/price
3. **Address validation**: Use `--validate` before creating labels
4. **Reference numbers**: Use for internal tracking
