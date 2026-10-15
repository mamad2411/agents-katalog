---
name: cavemaenggu-help
description: >
  Quick-reference card for all cavemaenggu modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /cavemaenggu-help,
  "cavemaenggu help", "what cavemaenggu commands", "how do I use cavemaenggu".
---

# Cavemaenggu Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in caveman style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | `/cavemaenggu lite` (or `/mg lite`) | Drop filler. Keep sentence structure. |
| **Full** | `/cavemaenggu` (or `/mg`) | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | `/cavemaenggu ultra` (or `/mg ultra`) | Extreme compression. Bare fragments. Tables over prose. |
| **Maeng-Gu-Lite** | `/cavemaenggu maeng-gu-lite` | Korean 개조식. Drop filler/honorifics, keep grammar. |
| **Maeng-Gu-Full** | `/cavemaenggu maeng-gu` | Full 명사형/전보체. Drop particles, Sino-Korean preferred in Hangul. |
| **Maeng-Gu-Ultra** | `/cavemaenggu maeng-gu-ultra` | Pure noun sequences. Telegraphic. Hangul only, no Hanja. |

Mode stick until changed or session end. Any prompt containing `맹구` auto-flips to `maeng-gu` (= maeng-gu-full).

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **cavemaenggu-commit** | `/cavemaenggu-commit` | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **cavemaenggu-review** | `/cavemaenggu-review` | One-line PR comments: `L42: bug: user null. Add guard.` |
| **cavemaenggu-compress** | `/cavemaenggu:compress <file>` | Compress .md files to caveman prose. Saves ~46% input tokens. |
| **cavemaenggu-help** | `/cavemaenggu-help` | This card. |

## Deactivate

Say "stop caveman", "normal mode", or Korean equivalent (`보통 모드`, `맹구 꺼`). Resume anytime with `/cavemaenggu` or `/mg`.

## Configure Default Mode

Default mode = `full`. Change it:

**Environment variable** (highest priority):
```bash
export CAVEMAENGGU_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/cavemaenggu/config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start. User can still activate manually with `/cavemaenggu` or `/mg`.

Resolution: env var > config file > `full`.

## More

Full docs: https://github.com/tk4n9/cavemaenggu
