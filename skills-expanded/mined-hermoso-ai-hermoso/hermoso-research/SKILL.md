---
name: hermoso-research
description: >-
  Competitor + ad-library intelligence with Hermoso: find a brand's competitors, pull their real running ads
  across Meta/Google/LinkedIn, and surface the winning hooks/angles worth copying. Use when the user asks to
  "find my competitors", "pull <brand>'s ads", "what ads are working in my niche", "research the longest-running
  ads", or wants proven creative to remix. NOT for: generating creative (use hermoso-generate / hermoso-ad-from-brand).
argument-hint: "[a brand/domain or a research question, e.g. 'longest-running protein-pancake ads']"
allowed-tools: Bash
---

# Hermoso: competitor & ad research

This is Hermoso's discovery half (which most generators don't have). Drive the **Hermoso CLI**.

## Setup (once)
- Install the CLI once: `npm install -g hermoso`, then run every command as `hermoso …`, as written below. If you cannot install packages, prefix the commands with `npx -y`, but know that npx asks the npm registry on every single call, so an agent making many calls can be rate-limited by npm (an HTTP 429 from npm, before Hermoso is ever reached). No MCP server is needed.
- Sign in once: `npx -y hermoso auth login` (opens a browser; nothing to paste). On a machine with no browser (a server, chatted over Telegram, Discord or WhatsApp): run `npx -y hermoso auth login --device --no-wait`, send the user the link and short code it prints, and once they approve run `npx -y hermoso auth login --device --resume`. No key needed. Only if nobody can open a link: `npx -y hermoso auth login --token <your key>`, using a key from app.hermoso.ai under **MCP & CLI**. No account at all? An agent can sign itself up on a paid plan with `POST /v1/signup` at app.hermoso.ai; see the Hermoso README.
- For anything these steps do not cover (organic search on TikTok, Instagram, YouTube, Reddit or Threads, creator search, a competitor teardown): `hermoso tools --search <what you want>` finds the tool, `hermoso tools <name>` prints its arguments, `hermoso call <name> --json '{...}'` runs it.

## Procedure
Pick the tool that fits the ask:
1. **Find competitors** for a domain: `hermoso competitors <domain> [--mode competitors|inspiration|company] --json`
   - `competitors` = head-to-head rivals; `inspiration` = best relevant ads incl. the brand itself; `company` = the company's own.
2. **Pull a brand's real ads** across ad libraries: `hermoso ads pull --company "<name>" [--domain <d>] [--platforms facebook,google,linkedin] [--country US] --json`
   - Defaults to Meta (richest library). Add google/linkedin only if asked (Google detailed pulls cost more).
3. **Natural-language research** (Claude tool-use over ad libraries + organic TikTok): `hermoso research "<request>"`
   - e.g. `hermoso research "the longest-running protein-pancake ads on Meta and what hooks they use"`. Prints a summary + the found ads with their URLs.
4. **Synthesize**: report the strongest hooks, angles, formats, and what's worth copying, be specific (quote the actual headlines/angles). If the user then wants to build one, hand off to `hermoso-ad-from-brand` / `hermoso-generate`.
5. **What to post on TikTok**, from posts working this month: `hermoso call tiktok_ideas --json '{"category":"<niche>","dryRun":true}'` prices it (nothing runs); run it without `dryRun` after the user agrees. Up to 6 ideas, each backed by linked TikTok posts with their views. To make one: `hermoso call tiktok_ideas --json '{"pick":<that idea object>,"to":"render_ad"}'` (free) returns the plan_ad brief with the claims the ad may make; nothing renders until that next call.

## Notes
- Research spends credits (ad-library calls); keep platform scope to what's asked.
- Add `--json` for the raw ad objects (URLs, copy, run dates) when the user wants the data, not a summary.
