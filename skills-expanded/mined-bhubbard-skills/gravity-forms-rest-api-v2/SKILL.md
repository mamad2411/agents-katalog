---
name: gravity-forms-rest-api-v2
description: "Advanced guide on endpoints, authentication, and submitting data headlessly."
---

# Gravity Forms REST API v2

The REST API v2 is built on top of the WordPress REST API infrastructure. It is the modern standard for communicating with Gravity Forms headlessly.

## Reference
[REST API v2 Documentation](https://docs.gravityforms.com/rest-api-v2/)

## Endpoints

All endpoints are prefixed with `/wp-json/gf/v2/`.

### Submitting Forms (Headless Forms)
To submit a form from a decoupled frontend (like React or a mobile app), do NOT use the `/entries` POST endpoint. Instead, use the form submissions endpoint so that validation, notifications, and add-on feeds run correctly.

`POST /wp-json/gf/v2/forms/{form_id}/submissions`

**Payload:**
Send the data as JSON with the field IDs as keys.
```json
{
  "1": "John Doe",
  "2": "john@example.com"
}
```

**Response:**
Returns a JSON object with `is_valid`. If `is_valid` is true, an entry ID is returned. If false, validation messages are returned per field.

### Fetching Entries
`GET /wp-json/gf/v2/entries`

Query parameters allow you to filter results. The syntax can be complex.
Example: Fetching entries for form ID 5 where field 2 equals "active".
`GET /wp-json/gf/v2/entries?form_ids[0]=5&search={"field_filters":[{"key":"2","value":"active"}]}`

## Authentication
If you are submitting forms headlessly for anonymous users, you might not need authentication if the form is public. However, to read entries or manage forms, you must authenticate.

- **Basic Auth with GF API Keys**: Go to Forms > Settings > REST API. Create a key. Send these as standard Basic Auth headers (Key is Username, Secret is Password).
- **Cookie Auth**: If the API call originates from JavaScript on the same WordPress site, include the `X-WP-Nonce` header.

## Best Practices
- Always use `/wp-json/gf/v2/forms/{id}/submissions` for external form submissions.
- When retrieving entries via the API, leverage the `paging` and `sorting` JSON parameters to limit the payload size.
