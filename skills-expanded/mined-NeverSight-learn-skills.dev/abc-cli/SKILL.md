---
name: abc-cli
description: Manage Apple Business Connect listings using the abc CLI. Use when working with business locations, place cards, hours, or when the user mentions Apple Business Connect, Apple Maps business, location listings, or abc.
---

# Apple Business Connect CLI

Manage Apple Business Connect listings using the `abc` command-line tool.

## Prerequisites

```bash
abc --version
export ABC_TOKEN='your-oauth-token'
abc auth status
```

## Authentication

- OAuth token from Apple Business Connect
- Environment variable: `ABC_TOKEN`
- Or: `abc auth login` for interactive OAuth flow

## Business Locations

### List & Search

```bash
abc locations list --limit 50
abc locations search --query "Apple Store"
abc locations get LOCATION_ID
```

### Create & Update

```bash
abc locations create --name "My Business" --address "123 Main St"
abc locations update LOCATION_ID --phone "+1-555-123-4567"
abc locations update LOCATION_ID --hours "mon-fri:9am-5pm,sat:10am-4pm"
```

### Status

```bash
abc locations status LOCATION_ID
abc locations verify LOCATION_ID --method postcard
abc locations close LOCATION_ID --temporary --until 2024-12-01
```

## Place Cards

```bash
abc placecard get LOCATION_ID
abc placecard update LOCATION_ID --photos ./photos/
abc placecard categories list
abc placecard categories set LOCATION_ID --primary "Restaurant"
```

## Actions & Posts

```bash
abc actions list LOCATION_ID
abc actions create LOCATION_ID --type ORDER --url "https://order.example.com"
abc posts list LOCATION_ID
abc posts create LOCATION_ID --title "Summer Special" --photo promo.jpg
```

## Insights

```bash
abc insights summary --location LOCATION_ID --days 30
abc insights queries --location LOCATION_ID --start 2024-06-01
abc insights directions --location LOCATION_ID --days 30
```

## Agent Best Practices

1. **Verification**: Required before location appears on Maps
2. **Hours format**: Use comma-separated with dashes
3. **Photos**: Follow Apple's photo guidelines
4. **Categories**: Choose most specific category available
