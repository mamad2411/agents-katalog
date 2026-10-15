---
name: hui-help
description: >
  Quick-reference card for all hui modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /hui-help,
  "hui help", "what hui commands", "how do I use hui".
---

# Hui Help

Display this reference card when invoked. One-shot — do not change mode, write flag files, or persist anything. Output in hui style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | `/hui-lite` | Drop filler. Keep sentence structure. |
| **Full** | `/hui` | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | `/hui-ultra` | Terse fragments when meaning stays clear. |
| **Wenyan-Full** | `/hui-wenyan` | Full 文言文 style. |

Legacy form remains supported: `/hui lite|full|ultra|wenyan`.

Mode sticks until changed or session end.

## Commands

| Command | Behavior |
|---|---|
| `/hui` / `/hui-global` | Persistent full HUI writing style for future replies. Does not rewrite transcript, context, or cache. |
| `/hui-lite` / `/hui-ultra` | Persistent lite or ultra writing style. |
| `/hui-wenyan[-lite\|-full\|-ultra]` | Persistent Wenyan writing style. |
| `/hui demo` | **本地文本示例**. Fixed local before/after text; no model call or state writes. Claude Code only. |
| `/hui-commit` / `/hui-review` | One-shot commit or review behavior. |
| `/hui-compress <file>` | Rewrites an explicit natural-language file; creates backup and validates structure. |
| `/hui-stats` | Reads observed local session usage. No savings or cost estimate. |
| `/hui-session` | Read-only current-transcript summary; `--compact` creates validated sibling copy, never modifies original. Claude Code only. |
| `/hui-init` | Writes project rule files; use dry-run first. |
| `/hui-help` | This display; no state writes. |

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **hui-commit** | `/hui-commit` | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **hui-review** | `/hui-review` | One-line PR comments: `L42: bug: user null. Add guard.` |
| **hui-compress** | `/hui-compress <file>` | Rewrites supported natural-language files while preserving validated structure. |
| **hui-help** | `/hui-help` | This card. |

## Deactivate

Say "stop hui" or "normal mode". Resume anytime with `/hui`.

## Language

Keep user's language by default. Compress style, not language. Technical terms, code, commands, commit types, and exact error strings stay verbatim unless user asks for translation.

## Configure Default Mode

Default mode = `full`. Change it:

**Environment variable** (highest priority):
```bash
export HUI_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/hui/config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start. User can still activate manually with `/hui`.

Resolution: env var > config file > `full`.

## Product and Distribution

**HUI** is product name: plugins, skills, `/hui`, hooks, statusline, and global `hui` command. **`next-token-hui`** is npm distribution name. Install with `npx -y next-token-hui -- ...`; do not assume npm package `hui` exists.

## More

Full docs: https://github.com/everything-ok/next-token
