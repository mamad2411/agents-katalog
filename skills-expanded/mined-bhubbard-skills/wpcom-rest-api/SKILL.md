---
name: wpcom-rest-api
description: Guides interaction with the WordPress.com REST API. Use this skill whenever building integrations, querying site data, or managing content programmatically via WordPress.com API endpoints.
---
# WordPress.com REST API

This skill provides guidance on using the WordPress.com REST API.

## Core Concepts
- **Base URL**: The base URL for the API is generally `https://public-api.wordpress.com/rest/v1.1/` or `v1.2/` depending on the endpoint.
- **Site ID/Domain**: Most site-specific endpoints require the site identifier, which can be the numerical Site ID or the domain name (e.g., `example.wordpress.com`).

## Authentication
To access non-public data or perform actions (POST, PUT, DELETE), you must authenticate requests using an OAuth2 token. Pass the token in the Authorization header: `Authorization: Bearer <your_token>`.

## Common Endpoints
- **Get Site Info**: `GET /sites/$site`
- **Posts**: `GET /sites/$site/posts`, `POST /sites/$site/posts`
- **Users**: `GET /sites/$site/users`

## Best Practices
1. **Pagination**: API responses with lists usually support `number` and `page` (or `offset`) query parameters.
2. **Field Filtering**: Use `?fields=ID,title,URL` to limit the response payload and improve performance.
3. **Error Handling**: The API returns standard HTTP status codes (e.g., 400 for Bad Request, 401 for Unauthorized, 403 for Forbidden, 404 for Not Found).

## Reference
Always refer to the official documentation at:
https://developer.wordpress.com/docs/api/
