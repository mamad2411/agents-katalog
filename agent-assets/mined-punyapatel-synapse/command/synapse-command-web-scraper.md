# Web Scraper

Fetches web pages and extracts data using CSS selectors.

## Instructions

You have access to the Synapse `web_scraper` skill located at `skills/web_scraper/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/web_scraper/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/web_scraper/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `scrape`

### Example Invocation
```json
{
  "operation": "scrape",
  "url": "https://example.com",
  "selector": "h1"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/web_scraper/web_scraper.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/web_scraper/package.json`
- Python: check `skills/web_scraper/requirements.txt`
