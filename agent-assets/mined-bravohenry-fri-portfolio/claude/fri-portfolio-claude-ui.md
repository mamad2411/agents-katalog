# components/ui/
> L2 | Parent: src/components/CLAUDE.md

Shared UI primitives — server components with pure CSS, no client state. Building blocks consumed by every panel on the homepage.

## Members

GlassPanel.tsx: Frosted-glass container with backdrop blur, the universal panel wrapper
TechBorder.tsx: GlassPanel variant with neon-pink corner accents via CSS pseudo-elements
ProgressBar.tsx: Horizontal fill indicator, percentage-driven width via inline style
ThemeToggle.tsx: Client component — toggles data-theme on `<html>`, persists to localStorage

[PROTOCOL]: Update this file on any member change, then check parent CLAUDE.md
