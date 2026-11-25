---
name: terminal-specific-art-fallbacks
description: "Layer terminal detection and fallback fragments so the same mascot identity renders correctly across Apple Terminal, xterm, and other hosts."
metadata:
  author: ychampion
---

# SKILL: Terminal-specific Art Fallbacks
**Domain:** terminal-ui  
**Trigger:** When the same brand art must render on Apple Terminal, xterm, and other hosts with different Unicode/color capabilities while preserving the mascot identity.
**Source Pattern:** Distilled from reviewed terminal rendering and compatibility patterns.

## Core Method
Detect the terminal host (e.g., via `env.terminal`) before rendering and prepare specialized fragments for hosts that need them. Use a default art path for general terminals but route sensitive fragments (eye shapes, raised arms, background fills) through the host-specific data, keeping the fallback path centered on the default segments so the identity stays consistent even when the terminal cannot express the fancy fragments.

## Key Rules
- Gate the choice of fragment set on the detected terminal (Apple Terminal uses the `APPLE_EYES` set; others reuse `POSES`) so hosts with different capabilities stay readable.
- Keep the identity stable by falling back to the default pose when a specialized host-specific variant is unavailable, rather than constructing a completely new layout.
- When a test host requires a background-fill trick (Apple Terminal’s background-color fill), wrap the fragments in a dedicated render path instead of mixing it with the default path.

## Example Application
If your release banner has `env.terminal === "Apple_Terminal"` users and others, detect the host early, feed Apple with background-filled eye fragments, and serve the general Unicode art to everyone else while maintaining the same mascot name, spacing, and pose structure.

## Anti-Patterns (What NOT to do)
- Rendering only a single art variant and letting hosts with lesser glyph support break the UI or show garbage characters.
- Mixing host-specific fragments inside the default render path so every render re-evaluates terminal detection and corrupts memoization caches.
- Creating entirely separate mascots per terminal host instead of sharing the same segments and only swapping fragments.
