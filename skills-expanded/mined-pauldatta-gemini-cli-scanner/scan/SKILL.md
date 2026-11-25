---
name: scan
description: Scan your AI coding tool ecosystem — Gemini CLI, Claude Code, Antigravity (Desktop, CLI, IDE), Continue, Windsurf, JetBrains AI, OpenCode. Produces a maturity score, advisory recommendations, and optionally generates reusable SKILL.md files from your conversation patterns. Use when the user asks to audit their environment, check their setup, scan their tools, or wants skill suggestions.
---

# Scan AI Coding Environment

Audit your AI coding tool ecosystem and discover reusable patterns.

## When to Use

- User says "scan my environment", "audit my setup", "check my tools"
- User asks about their maturity score or wants recommendations
- User wants to discover what skills they should create
- User asks what AI tools they have installed
- User wants to compare tool configurations across their ecosystem

## Quick Scan (No API Key)

Run a full environment scan without AI-powered skill suggestions:

```bash
npx gemini-cli-scanner@latest --skip-suggestions
```

This produces:
- `scan-results/gemini-env-manifest.json` — structured data for aggregation
- `scan-results/gemini-env-report.md` — human-readable report with scores and recommendations

After the scan completes, read the report and present the key findings to the user.

## Full Scan (With Skill Suggestions)

If the user wants AI-generated skill suggestions, ensure credentials are set:

```bash
# Check for credentials
echo $GOOGLE_CLOUD_PROJECT  # Vertex AI
echo $GOOGLE_API_KEY        # API Key
```

Then run:

```bash
npx gemini-cli-scanner@latest
```

## Scan With Repos

To include project-level scanning (`.gemini/` configs, GEMINI.md, repo patterns):

```bash
npx gemini-cli-scanner@latest --repos ~/Code --skip-suggestions
```

For deeper repo discovery:

```bash
npx gemini-cli-scanner@latest --repos ~/Code --repo-depth 4
```

## Read and Present Results

After scanning, always:

1. Read the JSON manifest:
   ```bash
   cat scan-results/gemini-env-manifest.json
   ```

2. Read the markdown report:
   ```bash
   cat scan-results/gemini-env-report.md
   ```

3. Present to the user:
   - **Maturity score** (0–67) and tier (Getting Started / Intermediate / Advanced / Expert)
   - **Top recommendations** — actionable items to improve their setup
   - **Ecosystem summary** — which tools are installed, skill counts, MCP servers
   - **Antigravity brain intelligence** — if present, summarize tool usage patterns, conversation counts, and top tools
   - **Skill suggestions** — if generated, present the candidates with install commands

## CLI Options

| Flag | Purpose |
|---|---|
| `--skip-suggestions` | Skip AI skill generation (no API key needed) |
| `--repos PATH` | Scan project repositories |
| `--repo-depth N` | Max depth for recursive repo discovery (default: 3) |
| `--chat-days N` | Only include conversation data from the last N days |
| `--json-only` | Output JSON only, no markdown report |
| `--include-prompts` | Include raw prompts in output (privacy-sensitive) |
| `--output-dir PATH` | Output directory (default: ./scan-results) |

## What Gets Scanned

- **Gemini CLI**: Settings, MCP servers, skills, agents, extensions, policies, conversations, 4-tier memory hierarchy, skill extraction state
- **Claude Code**: Skills, CLAUDE.md, project configs
- **Antigravity Desktop**: Brain conversations, skills, knowledge items, MCP servers
- **Antigravity CLI**: Brain sessions, skills, plugins, settings, history, import manifest, cached projects
- **Antigravity IDE**: Brain conversations, skills, plugins, MCP servers
- **Continue, Windsurf, JetBrains AI, OpenCode**: Skills, configs, presence detection

## Gotchas

- The scanner runs entirely locally — no data leaves your machine unless `--include-prompts` is passed AND you share the output file
- Output manifest contains only aggregate statistics by default (counts, tool names, chain fingerprints)
- API keys, OAuth tokens, and secrets are auto-redacted in the manifest
- On first run, `npx` downloads the package (~60 KB) — subsequent runs use the cache
- If the scan takes a long time, it's usually the AI skill suggestion step — use `--skip-suggestions` for fast scans

## Validation

After presenting results, ask the user:
1. Were there any surprising findings?
2. Would they like to act on any of the recommendations?
3. Should we install any of the suggested skills?
