---
description: Cursor Rules Instructions
globs:
alwaysApply: false
---
# Cursor Rules Instructions

To create or edit a rule:
1. Rules should be stored in the `.cursor/rules` directory
2. Rule files must have a `.mdc` extension (e.g., `my-rule.mdc`)
3. To reference a file in your rule, use the format: `[filename.ext](mdc:filename.ext)` where the path is relative to the workspace root
4. Rules use Markdown format with special Cursor-specific extensions
5. Rules will be shown to the AI to help with codebase navigation and understanding
6. Do not touch the metadata under any circumstances. Only edit the content after the metadata, and when editing, output only the content changes without including metadata

Example rule referencing a file:

```
# Project Structure Guide
The main entry point is [index.js](mdc:index.js), which loads configuration from [config.js](mdc:config.js)
```

Use these instructions to generate new rules or modify existing ones. Refer to the conversation history to understand the proper context for each rule.


