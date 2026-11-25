---
name: creating-gomarkdown-paste
description: Creates a markdown paste on gomarkdown.online and returns the shareable URL. Use when the user wants to share markdown content via a link, create a paste of markdown, publish markdown online, or generate a shareable markdown document URL.
license: MIT
metadata:
  author: gomarkdown
  version: "1.0.0"
  homepage: https://gomarkdown.online
compatibility: Requires curl or equivalent HTTP client and internet access
---

# Creating a GoMarkdown Paste

Create a markdown paste on [gomarkdown.online](https://gomarkdown.online) and return the shareable URL.

## How to create a paste

Send a POST request to the GoMarkdown API:

```bash
curl -s https://gomarkdown.online/api/paste \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{"markdown": "<MARKDOWN_CONTENT>"}'
```

The response is JSON:

```json
{
  "id": "abc1234567",
  "url": "/paste/abc1234567"
}
```

The shareable URL is `https://gomarkdown.online` + the `url` field from the response.

**Example:** If the response `url` is `/paste/abc1234567`, the full URL is `https://gomarkdown.online/paste/abc1234567`.

## Important details

- Maximum paste size: 500KB
- No authentication required
- The `markdown` field in the request body is required and must be a string
- Supports all standard markdown features plus Mermaid diagrams
- Escape JSON special characters in the markdown content (newlines as `\n`, quotes as `\"`, backslashes as `\\`)
- On success the API returns HTTP 201
- On invalid content the API returns HTTP 400 with an error message

## After creating the paste

Always return the full shareable URL to the user: `https://gomarkdown.online/paste/<id>`
