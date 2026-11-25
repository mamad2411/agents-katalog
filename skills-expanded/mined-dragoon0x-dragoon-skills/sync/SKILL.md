---
name: sync
description: Export design tokens to figma.tokens.json (tokens-studio-compatible format) so they can be imported into the Figma "tokens studio" plugin. dragoon does NOT live-sync with Figma - that requires OAuth and the Figma REST API. Use for one-way export from code to Figma, manually re-run after major token changes. Run as `node ~/.claude/skills/dragoon/skills/sync/scripts/sync.js`.
version: 1.0.0
---

# /sync

One-way export from your codebase to Figma's tokens-studio format.

## When to use

- Bridging from code-defined tokens to a Figma plugin
- The user says "export tokens", "send to figma"

## Limitations (honest scoping)

- one-way: code → figma.tokens.json
- not live: re-run after major token changes
- live sync requires figma oauth, planned for week 7+

## Run it

```
dragoon sync           # preview
dragoon sync --apply   # write figma.tokens.json
```

Then in Figma: Tokens Studio plugin → File → Import → select `figma.tokens.json`.
