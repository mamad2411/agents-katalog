---
name: blender-mcp-workflow
description: Use a connected Blender MCP to inspect and modify scenes, then verify the visible result. Applies to scene editing, object manipulation and rendering through Blender.
---

# Blender MCP workflow

Use the Blender server selected through the Hub. Discover its actual tool names and schemas; Blender MCP implementations expose different operations.

Before editing an existing scene, inspect the objects, selection and relevant scene settings using the available inspection tools. Translate the requested change into specific objects or settings. For a new scene, establish the intended output and preserve existing work unless replacing it is within the request.

Choose the smallest set of tool calls that accomplishes the change. If the server exposes code execution, inspect its schema and returned errors before relying on it; use scene inspection to obtain object names instead of guessing them.

After editing, use the available viewport capture or render operation to check the visible result. Correct material differences from the request before reporting completion. State the resulting scene or saved output location when one was produced.

When the task involves appearance, composition or lighting, inspect the attached design skill summaries and load the one relevant to the requested result.
