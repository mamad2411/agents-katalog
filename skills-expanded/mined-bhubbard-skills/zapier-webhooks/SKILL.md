---
name: zapier-webhooks
description: "Implement incoming and outgoing Webhooks by Zapier, handle custom requests, and parse JSON payloads."
---

# Zapier Webhooks Skill

## Overview
This skill focuses on using "Webhooks by Zapier" to connect apps that don't have native Zapier integrations, enabling custom HTTP requests and real-time data reception.

## Core Concepts

### 1. Catch Hooks (Incoming Webhooks)
- Generates a unique URL to receive POST, PUT, or GET requests.
- **Silent Mode:** Append `/silent` to the webhook URL to prevent Zapier from returning a success response body, which some third-party apps require.
- Zapier automatically parses incoming JSON or form-encoded payloads.

### 2. POST / PUT / GET (Outgoing Webhooks)
- Send data from Zapier to external APIs.
- Supports query parameters, headers, and basic authentication.
- Payloads can be sent as Form or JSON.

### 3. Custom Requests
- For complex APIs, use the "Custom Request" action.
- Allows raw payload construction (e.g., raw JSON strings).
- Essential when APIs require specific nested JSON structures or custom headers.

## Best Practices
- **Authentication:** Never expose API keys or bearer tokens in plain text if possible. Pass them securely via Headers.
- **Data Parsing:** If Zapier fails to parse an incoming webhook, ensure the sender is setting the `Content-Type: application/json` header.
- **Rate Limits:** Webhooks by Zapier have rate limits (e.g., around 100 requests per 10 seconds). High-volume webhooks might get throttled.

## Common Scenarios
- Receiving data from a custom internal tool.
- Sending a Slack message when a custom webhook is triggered.
- Making authenticated API calls to a service lacking a Zapier integration.
