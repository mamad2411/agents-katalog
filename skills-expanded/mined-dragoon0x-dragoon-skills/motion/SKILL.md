---
name: motion
description: Generate motion tokens (durations + easings) using values detected by /scan, falling back to material-quality defaults when nothing was detected. Produces fast/normal/slow durations and standard/enter/exit easings. Use when the user wants to formalize motion tokens or scaffold a motion system. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/motion/scripts/motion.js`.
version: 1.0.0
---

# /motion

Generates motion tokens (durations + easings) from your codebase.

## When to use

- The user wants to formalize motion tokens
- The user asks for "transition tokens", "easing tokens", "animation system"
- Cleaning up a codebase with too many one-off durations

## Tokens produced

Durations: `fast` / `normal` / `slow`. Snapped to detected values when possible (e.g., your codebase uses 200ms → that becomes `normal`), defaults otherwise.

Easings: `standard` (cubic-bezier curve from your codebase if found) / `enter` / `exit`.

## Run it

```
dragoon motion
dragoon motion --apply
dragoon motion --format css --apply
```
