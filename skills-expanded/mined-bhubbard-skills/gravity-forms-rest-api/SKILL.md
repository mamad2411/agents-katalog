---
name: gravity-forms-rest-api
description: "Guides interaction with Gravity Forms from external clients via the REST API."
---

# Gravity Forms REST API

## Introduction

The Gravity Forms REST API provides endpoints that allow interaction with Gravity Forms from an external client, such as a desktop application, mobile app, or headless frontend (e.g., React, Vue).

## Versions

### REST API v2 (Recommended)
Gravity Forms' latest REST API is an extension of the WordPress REST API structure. It allows developers to create, read, update, and delete forms, entries, and results over HTTP.
- **Reference**: [REST API v2 Documentation](https://docs.gravityforms.com/rest-api-v2/)
- **Base Route**: `/wp-json/gf/v2/`
- **Endpoints**:
  - `/forms`: GET (list forms)
  - `/forms/<id>`: GET, PUT, DELETE
  - `/forms/<id>/submissions`: POST (submit a form)
  - `/entries`: GET, POST
  - `/entries/<id>`: GET, PUT, DELETE

### Web API v1 (Legacy)
Formerly called the Web API, v1 loosely follows REST-style principles. While still supported, it is highly recommended to use v2 for all new development.

## Authentication
To access the REST API endpoints, you must authenticate. Gravity Forms v2 supports standard WordPress authentication methods:
- **Cookie Authentication**: For logged-in users within the same site (e.g., frontend AJAX). Requires the `X-WP-Nonce`.
- **Application Passwords**: Supported via WordPress core for basic authentication.
- **OAuth 1.0a / JWT**: Supported if the respective WordPress plugins are installed.
- **Gravity Forms API Keys**: You can generate specific REST API keys within the Gravity Forms settings (Gravity Forms > Settings > REST API) for use with Basic Auth.

## Best Practices
- Always use **REST API v2**.
- When submitting a form from an external app, use the `/forms/<id>/submissions` endpoint instead of directly creating an entry via `/entries`. The submissions endpoint runs validation, notifications, and add-on feeds, whereas creating an entry directly bypasses these.
