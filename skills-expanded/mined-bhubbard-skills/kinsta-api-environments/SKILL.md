---
name: kinsta-api-environments
description: "Instructions for managing environments for Kinsta sites via the REST API."
---

# Kinsta API Environments Skill

This skill explains how to manage environments (e.g., staging, production) for Kinsta sites using the REST API v2.

## Endpoints

All endpoints are relative to the base URL: `https://api.kinsta.com/v2`

### Get Site Environments

Retrieves a list of environments for a specific site.

- **Method:** `GET`
- **Path:** `/sites/{site_id}/environments`

### Get Environment Details

Retrieves details for a specific environment.

- **Method:** `GET`
- **Path:** `/sites/environments/{environment_id}`

### Clear Site Cache

Clears the edge and server cache for a given environment.

- **Method:** `POST`
- **Path:** `/sites/environments/{environment_id}/clear-cache`

## Example Usage

### Fetching Environments (cURL)

```bash
curl -X GET "https://api.kinsta.com/v2/sites/YOUR_SITE_ID/environments" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Clearing Cache (cURL)

```bash
curl -X POST "https://api.kinsta.com/v2/sites/environments/YOUR_ENVIRONMENT_ID/clear-cache" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Best Practices

- Use environment endpoints to build custom CI/CD pipelines.
- Automate cache clearing after deploying new code to ensure visitors see the latest content.
