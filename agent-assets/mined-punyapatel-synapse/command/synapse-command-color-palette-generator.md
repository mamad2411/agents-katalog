# Color Palette Generator

Generates harmonious color palettes (analogous, monochromatic, triadic, complementary) from a base hex color.

## Instructions

You have access to the Synapse `color_palette_generator` skill located at `skills/color_palette_generator/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/color_palette_generator/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/color_palette_generator/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `generate`

### Example Invocation
```json
{
  "operation": "generate",
  "base_color": "#3498db",
  "scheme": "analogous"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/color_palette_generator/color_palette_generator.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/color_palette_generator/package.json`
- Python: check `skills/color_palette_generator/requirements.txt`
