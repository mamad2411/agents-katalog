---
name: vibe-audit
description: Classify a vibe-coded project (Lovable, Bolt, v0, Replit, Cursor) and recommend which category audit skill(s) to run. Use when the user's request is generic ("audit my project," "what audit should I run," "audit this repo") or when the repo plausibly contains multiple categories. Detects user-facing webapps, mobile apps (Expo/React Native/iOS/Android), backend services / webhook handlers, chat bots (Slack/Discord/GitHub), CLI scripts, and MCP servers / AI agents. Recommends `vibe-webapp-audit`, `vibe-mobile-audit`, `vibe-service-audit`, `vibe-bot-audit`, `vibe-script-audit`, or `vibe-mcp-agent-audit` with rationale. Classifies and points only — does not perform audits.
allowed-tools: Read Grep Glob
---

# Vibe-coded project classifier

This skill answers one question: **which audit skill should I run on this repo?** It detects
what kind of thing the repo is and recommends one or more category skills from the
`vibe-*-audit` family. It does not perform any audit itself.

Use this when the user's request is generic ("audit my project," "what should I run on this,"
"what's in this repo") or when the repo plausibly contains more than one category of vibe-coded
work (e.g., a Next.js webapp that also serves a Slack bot endpoint).

If the user already named the category ("audit my Slack bot," "review my MCP server"), Claude
Code's normal skill dispatch should pick the specific skill directly — this classifier exists
for the ambiguous case.

## Workflow

1. **Detect**. Run the checks below. Don't do anything else — no file reads beyond what's needed
   to classify.
2. **Summarize what's in the repo** in one or two sentences ("This is a Next.js app with a
   Supabase backend and a `/api/slack/events` route that handles Slack webhooks.").
3. **Recommend** one or more category skills with rationale.
4. **Stop**. Tell the user the exact skill names to invoke. Do not chain into them.

### Detection commands

```bash
# Top-level manifests
ls package.json pyproject.toml requirements.txt Gemfile go.mod 2>/dev/null

# Package.json contents (deps are the strongest signal)
[ -f package.json ] && head -100 package.json

# Python deps
[ -f pyproject.toml ] && head -100 pyproject.toml
[ -f requirements.txt ] && cat requirements.txt

# Frontend frameworks → webapp
grep -hE '"(react|next|vite|svelte|solid-js|nuxt|astro|remix)"' package.json 2>/dev/null

# Webapp UI directories
ls app pages src/pages src/app components src/components 2>/dev/null

# Mobile frameworks → mobile
grep -hE '"(react-native|expo|@react-native|@expo)"' package.json 2>/dev/null
find . -maxdepth 4 \( -name "*.xcodeproj" -o -name "Info.plist" -o -name "AndroidManifest.xml" -o -name "pubspec.yaml" \) 2>/dev/null | head -5

# Chat-bot SDKs → bot
grep -hE '"(@slack/bolt|@slack/web-api|discord\.js|discord\.py|@octokit/webhooks|botbuilder)"' \
  package.json 2>/dev/null
grep -hE "(slack_sdk|discord\.py|pygithub|aiogram|python-telegram-bot)" \
  requirements.txt pyproject.toml 2>/dev/null

# MCP / agent SDKs → mcp-agent
grep -hE '"(@modelcontextprotocol/sdk|@anthropic-ai/claude-agent-sdk|langchain|langgraph|@anthropic-ai/sdk|openai)"' \
  package.json 2>/dev/null
grep -hE "(mcp|claude-agent-sdk|langchain|langgraph|anthropic|openai)" \
  requirements.txt pyproject.toml 2>/dev/null

# Webhook routes and route handlers → service (or bot, depending on what's at the endpoint)
find . -path ./node_modules -prune -o \
  \( -name "route.ts" -o -name "route.js" -o -path "*/webhooks/*" -o -path "*/api/*" \) \
  -print 2>/dev/null | head -20

# Scheduled jobs → service
ls .github/workflows vercel.json fly.toml render.yaml 2>/dev/null
grep -lE "schedule:|crons|cron:" .github/workflows/*.yml vercel.json 2>/dev/null

# Single-file CLI scripts → script
# Python with __main__
grep -lE 'if __name__ == .__main__.' --include="*.py" -r . 2>/dev/null | head -5
# Node with CLI parsing libs and no framework
grep -hE '"(commander|yargs|meow|cac|clipanion)"' package.json 2>/dev/null
# Bash scripts
find . -maxdepth 3 -name "*.sh" -not -path "*/node_modules/*" 2>/dev/null | head -10
```

## Classification heuristics

Apply in order. The first match doesn't preclude the others — record everything that matches.

| Signal                                                                                                                                | Recommended skill                                          |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Frontend framework dep present (React/Next/Vite/etc.) AND a UI directory (`app/`, `pages/`, `src/components/`) exists, NO mobile deps | `vibe-webapp-audit`                                        |
| `react-native` / `expo` / `@react-native` / `@expo` dep present, OR `*.xcodeproj` / `AndroidManifest.xml` / `pubspec.yaml` found      | `vibe-mobile-audit`                                        |
| Slack/Discord/GitHub bot SDK present, OR a webhook route handler at `/slack/*`, `/discord/*`, `/github/*`                             | `vibe-bot-audit`                                           |
| MCP SDK present (`@modelcontextprotocol/sdk`, `mcp` Python package), OR a `tools/list` handler                                        | `vibe-mcp-agent-audit`                                     |
| LLM SDK present (`anthropic`, `openai`) AND tool-use loop code (no UI)                                                                | `vibe-mcp-agent-audit`                                     |
| Webhook handler with HMAC verification, scheduled jobs, or `/api/*` endpoints AND no UI                                               | `vibe-service-audit`                                       |
| Single file (`.py`, `.ts`, `.sh`) with CLI argument parsing AND no server framework                                                   | `vibe-script-audit`                                        |
| Multiple match — record all that apply                                                                                                | List them in priority order (most user-data-exposed first) |

If nothing matches: ask the user what the repo does. Don't guess.

## Output format

After detection, output something like:

```
Detected: <one-or-two-sentence summary of what's in the repo>

Recommended audits (run in this order):

1. `vibe-webapp-audit` — primary surface. The repo is a Next.js app with Supabase auth
   and 12 API route handlers. This skill covers RLS, IDOR, input validation, and live
   probes against the deployed URL.

2. `vibe-bot-audit` — secondary. `app/api/slack/events/route.ts` is a Slack event handler.
   Bot-specific checks (signature verification, OAuth scopes, replay protection) aren't
   covered by the webapp audit.

To run the first, ask Claude Code: "run the vibe-webapp-audit skill on this repo."
```

## What this skill is NOT

- Not an auditor. It does not run secret scans, SAST, dependency audits, or anything else from
  the baseline. The category skills do that.
- Not a chain. It does not invoke the recommended skill — the user does, with their own
  intentions about scope and live targets.
- Not a substitute for direct dispatch. If the user knows their app is a Slack bot, they should
  invoke `vibe-bot-audit` directly; this classifier is for when they don't know.
