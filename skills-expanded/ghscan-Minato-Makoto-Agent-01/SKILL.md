---
name: web_operations
description: Perform HTTP requests and web scraping with URL safety checks.
module: builtin_tools.web_ops
tools:
  - http_request
  - web_scrape
---

# Web Operations Skill

HTTP and scraping tools with default SSRF protections.

## `http_request`

- Required: `url`
- Optional: `method`, `headers`, `body`, `allow_private_network`
- Default behavior blocks localhost/private/link-local targets

## `web_scrape`

- Required: `url`
- Optional: `selector`, `allow_private_network`
- Removes noisy tags and returns sanitized text output

## Safety

Use `allow_private_network=true` only when user intent explicitly requires local/private targets.
