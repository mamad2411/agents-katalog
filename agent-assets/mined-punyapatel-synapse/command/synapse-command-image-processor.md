# Image Processor

Performs image manipulation: resize, crop, rotate, and format conversion on base64 images.

## Instructions

You have access to the Synapse `image_processor` skill located at `skills/image_processor/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/image_processor/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/image_processor/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `resize`
- `crop`
- `rotate`
- `convert`

### Example Invocation
```json
{
  "operation": "resize",
  "data": "<base64>",
  "options": {
    "width": 200,
    "height": 200
  }
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/image_processor/image_processor.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/image_processor/package.json`
- Python: check `skills/image_processor/requirements.txt`
