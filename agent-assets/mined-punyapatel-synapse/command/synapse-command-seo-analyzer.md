# Seo Analyzer

Analyzes HTML for SEO best practices: title tags, meta descriptions, heading structure, alt text.

## Instructions

You have access to the Synapse `seo_analyzer` skill located at `skills/seo_analyzer/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/seo_analyzer/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/seo_analyzer/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `analyze`

### Example Invocation
```json
{
  "operation": "analyze",
  "html": "<html><head><title>My Page</title></head></html>"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/seo_analyzer/seo_analyzer.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/seo_analyzer/package.json`
- Python: check `skills/seo_analyzer/requirements.txt`
