---
name: custom_webhook
display_name: Custom Webhook
description: Call any custom HTTPS endpoint
auth_type: api_key
category: custom
---

# Custom Webhook Skill

## When to use
When the user wants their voice agent to call a custom API or webhook
that is not one of the built-in integrations. This is the escape hatch
for any HTTPS endpoint. Common triggers:
- "call my API when..."
- "send data to my webhook"
- "integrate with our internal system"

## What to do

1. **Ask for details**: What is the HTTPS endpoint URL? What HTTP method?
   What data should be sent? What does the response look like?

2. **Use `secret("custom_webhook")`** in tool scripts if authentication is
   needed. The system will automatically emit the correct action card based
   on the platform configuration. Do NOT emit action cards manually.
   If the webhook uses a custom auth header name, read it from
   `secret('custom_webhook.header_name')` instead of hardcoding the header.

3. **Generate tool config**: Use a QuickJS `script` field. The endpoint MUST use HTTPS.

## Example tool configs

### No authentication
```json
{
  "name": "webhook.notify",
  "description": "POST caller data to the webhook",
  "params": [
    {"name": "caller_name", "type": "string", "required": true},
    {"name": "summary", "type": "string", "required": false}
  ],
  "script": "let resp = http_post('https://hooks.example.com/incoming', {caller_name: caller_name, summary: summary});\nif (resp.status >= 200 && resp.status < 300) { return 'Done'; }\nthrow new Error(`Webhook ${resp.status}: ${resp.body}`);",
  "side_effect": true
}
```

### Bearer token authentication
```json
{
  "name": "webhook.notify",
  "description": "POST caller data to the webhook using bearer auth",
  "params": [
    {"name": "caller_name", "type": "string", "required": true},
    {"name": "summary", "type": "string", "required": false}
  ],
  "script": "let key = secret('custom_webhook');\nlet resp = http_post_h('https://api.example.com/hook', {caller_name: caller_name, summary: summary}, {'Authorization': 'Bearer ' + key});\nif (resp.status >= 200 && resp.status < 300) { return 'Sent'; }\nthrow new Error(`Webhook ${resp.status}: ${resp.body}`);",
  "side_effect": true
}
```

### Custom header authentication
```json
{
  "name": "webhook.notify",
  "description": "POST data using a custom auth header",
  "params": [
    {"name": "data", "type": "string", "required": true}
  ],
  "script": "let key = secret('custom_webhook');\nlet header = secret('custom_webhook.header_name') || 'X-API-Key';\nlet headers = {};\nheaders[header] = key;\nlet resp = http_post_h('https://api.example.com/webhook', {data: data}, headers);\nif (resp.status >= 200 && resp.status < 300) { return 'OK'; }\nthrow new Error(`Webhook ${resp.status}: ${resp.body}`);",
  "side_effect": true
}
```

## Rules
- Endpoint MUST use HTTPS (the existing SSRF validator enforces this)
- NEVER put API keys or tokens in plain script strings
- Use `secret('custom_webhook')` for the primary key/token
- Use `secret('custom_webhook.header_name')` to read the custom header name field
- NEVER hardcode a user-provided custom auth header name. The header name belongs in the
  connection config so the credential card can update it later.
- NEVER ask for credentials in chat
- If no auth is needed, omit the `secret()` call entirely
- For script tools, treat non-2xx HTTP responses as failures and `throw` using `resp.status`/`resp.body` instead of returning a plain-text error string
