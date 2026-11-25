---
name: claude-seo-bing
description: Bing Webmaster Tools + IndexNow extension. Microsoft Copilot citations are fed by the Bing index; this skill makes Bing visibility, link data, and IndexNow URL submission first-class.

compatibility: "Requires BING_WEBMASTER_API_KEY and (optionally) INDEXNOW_KEY in ~/.claude/settings.json env. Run extensions/bing-webmaster/install.sh to configure."
metadata:
  version: "2.2.0"
---

> **Nota per Kimi Code:** questa skill è convertita dal plugin Claude Code `claude-seo`. I comandi slash (`/seo ...`) non sono disponibili; descrivi semplicemente in linguaggio naturale cosa vuoi analizzare. Gli script sono in `~/.kimi/skills/claude-seo/scripts/`.



# seo-bing

The non-Google indexing surface. Google still rejects IndexNow (per
Gary Illyes, multiple SOTR episodes 2024-2025), so this skill is
specifically for **Bing/Yandex/Seznam/Naver indexing** and
**Microsoft Copilot AI citation** (which pulls from the Bing index).

## Prerequisites

- Run `extensions/bing-webmaster/install.sh` or `install.ps1`.
- A Bing Webmaster Tools API key.
- Optional: an IndexNow host key (32+ chars) published at the URL
  declared as `INDEXNOW_KEY_LOCATION`.

## Routing

| Command | Underlying script |
|---|---|
| `bing links <url>` | `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/bing_webmaster.py links <url>` |
| `bing compare <urlA> <urlB>` | `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/bing_webmaster.py compare <urlA> <urlB>` |
| `bing submit <url>` (single URL) | `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/indexnow_submit.py --host ... --urls <url>` |
| `bing submit-batch <file>` | `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/indexnow_submit.py --urls-file <file>` |
| `bing verify-indexnow` | `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/indexnow_submit.py --verify-only` |

## When this skill applies

- The user is publishing new pages and wants Microsoft Copilot
  citation eligibility (Bing index ingestion).
- The user wants to nudge Bing/Yandex/Seznam/Naver indexing for fresh
  URLs.
- The user is doing competitor backlink analysis and wants Bing's
  unique link data (Bing tracks links Google's API doesn't surface).

## Cross-skill delegation

- For Google indexing (very different model — sitemap-driven, no
  IndexNow), use `claude-seo-google indexing`.
- For multi-source backlink confidence weighting, fall back to
  `claude-seo-backlinks` which already integrates Bing + Moz + CC.
