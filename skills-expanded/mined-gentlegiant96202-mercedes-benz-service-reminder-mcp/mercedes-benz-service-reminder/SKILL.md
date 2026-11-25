---
name: mercedes-benz-service-reminder
description: Mercedes-Benz Service A/B reminders and warning-light guidance by SilberArrows Dubai.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://mercedes-benz.silberarrows.com/
    requires:
      anyBins:
        - npx
        - curl
---

# Mercedes-Benz Service Reminder (SilberArrows)

Help Mercedes-Benz owners estimate the next Service A or Service B, explain what each service typically includes, look up general warning-light guidance, and find SilberArrows contact details in Dubai.

Homepage: [https://mercedes-benz.silberarrows.com/](https://mercedes-benz.silberarrows.com/)

Intervals are general guidance only (about 15,000 km or 12 months, whichever comes first, on most models). Always follow the vehicle ASSYST indicator and the manufacturer schedule for the specific model.

## Hosted MCP endpoint

Prefer the hosted Streamable HTTP MCP server when the agent can call remote MCP URLs:

- MCP URL: `https://silberarrows-mcp.netlify.app/mcp`
- Product site: `https://mercedes-benz.silberarrows.com/`

Example client config:

```json
{
  "mcpServers": {
    "mercedes-benz-service-reminder": {
      "url": "https://silberarrows-mcp.netlify.app/mcp"
    }
  }
}
```

Optional API key (any non-empty value works, for example `silberarrows-public`) via `Authorization: Bearer ...` or `x-api-key`.

## Local MCP via npx

If `npx` is available, run the stdio MCP server locally:

```bash
npx -y mercedes-benz-service-reminder-mcp
```

Example client config:

```json
{
  "mcpServers": {
    "mercedes-benz-service-reminder": {
      "command": "npx",
      "args": ["-y", "mercedes-benz-service-reminder-mcp"]
    }
  }
}
```

## Plain REST (optional)

When MCP is not available, use `curl` against the same Netlify deployment:

- `GET https://silberarrows-mcp.netlify.app/api/next-service`
- `GET https://silberarrows-mcp.netlify.app/api/service-info`
- `GET https://silberarrows-mcp.netlify.app/api/warning-light`
- `GET https://silberarrows-mcp.netlify.app/api/contact`

OpenAPI: `openapi.json` in the project root (also suitable for RapidAPI Studio import).

## Tools / capabilities

| Capability | Purpose |
| --- | --- |
| Next service estimate | From last service type (A/B), date, and mileage, estimate the next Service A/B due date and km. |
| Service explanation | What Service A or Service B typically includes. |
| Warning lights | General guidance for common Mercedes-Benz warning lights and messages. |
| Specialist contact | SilberArrows Mercedes-Benz service centre details in Al Quoz, Dubai. |

## About SilberArrows

SilberArrows is a Mercedes-Benz service centre in Al Quoz Industrial Area 1, Dubai. Learn more at [https://mercedes-benz.silberarrows.com/](https://mercedes-benz.silberarrows.com/).
