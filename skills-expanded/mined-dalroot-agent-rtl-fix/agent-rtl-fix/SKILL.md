---
name: agent-rtl-fix
description: Automatically configures Antigravity IDE, Cursor, and VS Code for native RTL/LTR BiDi support, Vazirmatn fonts, and global agent formatting rules.
---

# Agent RTL Fix Skill

Configures autonomous coding agents and editors for native Right-to-Left (Persian, Arabic, Urdu, Hebrew) and Left-to-Right bidirectional text support.

## Automated Actions
1. **Font Setup**: Installs clean Vazirmatn typography for seamless multilingual rendering.
2. **Editor Settings**: Configures `editor.unicodeHighlight.bidiCharacters: true`, clean font fallback (`'Vazirmatn', 'Fira Code', 'Consolas', monospace`), and balanced line-height.
3. **Global Agent Rule**: Installs machine-wide rule (`~/.gemini/config/rules/rtl-formatting.md`) so all agent responses render in proper RTL without token overhead.
