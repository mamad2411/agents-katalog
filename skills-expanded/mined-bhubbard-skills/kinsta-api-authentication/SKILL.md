---
name: kinsta-api-authentication
description: "Handles authentication and base setup for the Kinsta REST API v2."
---

# Kinsta API Authentication Skill

This skill provides instructions for authenticating with the Kinsta REST API v2.

## Overview

The Kinsta REST API allows you to programmatically interact with Kinsta hosting services. All API requests must be authenticated.

- **Base URL:** `https://api.kinsta.com/v2`
- **Authentication Method:** Bearer Token

## Getting an API Key

1. Log into your Kinsta account (MyKinsta).
2. Navigate to **Company settings**.
3. Select **API Keys**.
4. Generate a new API key. Keep this key secure as it grants access to your Kinsta account.

## Making Authenticated Requests

Include the API key in the `Authorization` header of your HTTP requests as a Bearer token. 

### Example (cURL)

```bash
curl -X GET "https://api.kinsta.com/v2/sites" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Best Practices

- Store your API key securely using environment variables or a secret manager.
- Do not commit your API key to version control.
- If an API key is compromised, immediately revoke it in the MyKinsta dashboard and generate a new one.
