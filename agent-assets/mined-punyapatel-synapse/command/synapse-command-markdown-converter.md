# Markdown Converter

Converts between Markdown and HTML bidirectionally.

## Instructions

You have access to the Synapse `markdown_converter` skill located at `skills/markdown_converter/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/markdown_converter/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/markdown_converter/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `md_to_html`
- `html_to_md`

### Example Invocation
```json
{
  "operation": "md_to_html",
  "data": "# Hello World"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/markdown_converter/markdown_converter.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/markdown_converter/package.json`
- Python: check `skills/markdown_converter/requirements.txt`
