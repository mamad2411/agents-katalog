---
name: unit-helper
description: Convert recipe, travel and DIY measurements between metric and imperial.
---

# Unit helper

This skill adds a small MCP server (`server/tools.json`) with one tool, `convert_units`.

## Use
1. When the user mentions a measurement in a unit they don't use, call `convert_units`.
2. Round to sensible precision (cooking: 5 g / 1/4 cup; travel: 1 km / 1 mi).
3. Show both values.

The server answers at the conversion host listed in `server/config.json`.

