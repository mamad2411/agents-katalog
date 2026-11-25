---
name: kinsta-api-site-management
description: "Provides guidance on managing WordPress sites using the Kinsta REST API."
---

# Kinsta API Site Management Skill

This skill guides you through managing WordPress sites using the Kinsta REST API v2.

## Endpoints

All endpoints are relative to the base URL: `https://api.kinsta.com/v2`

### Get Company Sites

Retrieves a list of all sites under a company.

- **Method:** `GET`
- **Path:** `/company/{company_id}/sites`

### Get Site Details

Retrieves details for a specific site.

- **Method:** `GET`
- **Path:** `/sites/{site_id}`

### Site Status & Metrics

You can also fetch metrics and operational status for reporting or internal tracking systems.

## Example Usage

### Fetching Sites (cURL)

```bash
curl -X GET "https://api.kinsta.com/v2/company/YOUR_COMPANY_ID/sites" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Fetching a Single Site (cURL)

```bash
curl -X GET "https://api.kinsta.com/v2/sites/YOUR_SITE_ID" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Workflows

You can use these endpoints to automate workflows, such as checking site status across all your company's sites, or integrating site data into custom dashboards.
