---
name: yoast-seo-rest-api
description: "Using the Yoast REST API endpoints to fetch head metadata and SEO scores headlessly."
---

# Yoast SEO REST API

The Yoast SEO REST API provides endpoints to retrieve SEO metadata for WordPress entities (posts, pages, terms, authors, and the homepage) in a headless environment.

## Reference
[REST API Documentation](https://developer.yoast.com/customization/apis/rest-api/)

## Endpoints

Yoast SEO adds an endpoint to retrieve all meta tags and schema markup generated for a specific URL.

### `/wp-json/yoast/v1/get_head`

**Parameters:**
- `url` (string, required): The full URL of the page you want to get the SEO metadata for.

**Example Request:**
```
GET /wp-json/yoast/v1/get_head?url=https://example.com/my-post/
```

**Response:**
Returns a JSON object containing the complete `<head>` HTML string and a parsed JSON object of the metadata and Schema graph.

```json
{
  "html": "<title>My Post - Example</title><meta name=\"description\" content=\"...\" />...",
  "json": {
    "title": "My Post - Example",
    "description": "...",
    "schema": {
      "@context": "https://schema.org",
      "@graph": [ ... ]
    }
  }
}
```

## Best Practices
- When building a headless WordPress frontend (Next.js, Gatsby, Vue), simply fetch this endpoint with the current route's corresponding WordPress URL.
- Use the `html` string to inject the SEO tags directly into your frontend `<head>` section.
- You can disable the REST API endpoint using the `wpseo_enable_rest_api` filter if it's not needed.
