---
name: env-scanner
description: Scan and audit Gemini CLI, Claude Code, Antigravity, Continue, Windsurf, JetBrains AI, and OpenCode environments. Discovers configurations, audits memory tiers, detects skill extraction state, analyzes behavioral tool chains, checks policy governance (v0.40+), and suggests reusable skills with evidence gating. Privacy-by-default — output manifest contains only aggregate counts. Use when the user wants to analyze their AI setup, audit policies, discover patterns, or generate an environment report.
---

# Environment Scanner Skill

Runs `gemini-cli-scanner` (v3.5.6) to audit the user's AI coding tool ecosystem.

## When to Activate

- User asks to "scan my environment", "analyze my setup", or "audit my tools"
- User wants to know what skills, MCP servers, extensions, or agents they have
- User wants to discover usage patterns from conversation history
- User wants a maturity score or environment report
- User asks about memory configuration, policy governance, or skill extraction
- User mentions "tribal knowledge", "pattern discovery", "skill suggestions", or "ecosystem audit"

## Running the Scanner

Use `${extensionPath}` to reference the scanner directory.

### Quick scan (no API needed)

```bash
node ${extensionPath}/scanner.js --output-dir ./scan-results --skip-suggestions
```

### Full scan with AI skill suggestions

Requires `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT`. Uses evidence-gated two-stage pipeline: flash-lite identifies patterns, pro writes SKILL.md files in parallel.

```bash
node ${extensionPath}/scanner.js --output-dir ./scan-results
```

### With repo discovery

```bash
node ${extensionPath}/scanner.js --output-dir ./scan-results --repos ~/Code
node ${extensionPath}/scanner.js --output-dir ./scan-results --repos ~/Code --repo-depth 4
node ${extensionPath}/scanner.js --output-dir ./scan-results --repos ~/Code/project-a ~/Code/project-b
```

### Filter by time

```bash
node ${extensionPath}/scanner.js --output-dir ./scan-results --chat-days 30
node ${extensionPath}/scanner.js --output-dir ./scan-results --json-only
```

### All flags

| Flag | Default | Purpose |
|:---|:---|:---|
| `--version`, `-v` | — | Show version |
| `--gemini-dir PATH` | `~/.gemini` | Gemini config dir |
| `--home-dir PATH` | `~` | Home dir for ecosystem scanning |
| `--output-dir PATH` | `./scan-results` | Output directory |
| `--repos PATH [PATH..]` | `[]` | Repo paths or parent dirs |
| `--repo-depth N` | `3` | Max recursive discovery depth |
| `--chat-days N` | all | Limit to last N days of history |
| `--skip-suggestions` | `false` | Skip AI suggestions |
| `--json-only` | `false` | JSON only, no markdown |
| `--include-prompts` | `false` | Include raw prompts, topics, project names in manifest |
| `--skip-update-check` | `false` | Skip GitHub version check |

## What Gets Scanned

| Source | What's Extracted |
|:---|:---|
| `settings.json` | MCP servers, model config, auth, autoMemory |
| `GEMINI.md` | Global memory (Tier 1) |
| `skills/` | Installed skills |
| `agents/` | Custom agents |
| `extensions/` | Extension catalog |
| `policies/` | TOML rules (v0.40+: modes, mcpName, denyMessage, interactive, commandRegex) |
| `tmp/*/chats/*.jsonl` | Tool usage, models, tokens, behavioral tool chains |
| `tmp/*/memory/` | Private project memory (Tier 2), MEMORY.md, sibling files |
| `tmp/*/memory/.extraction-state.json` | Skill extraction runs, inbox, stale locks |
| System policy dirs | Admin policies (silent skip if inaccessible) |
| `~/.claude/`, Continue, Windsurf, JetBrains | Cross-ecosystem detection |
| `--repos` paths | Project-level `.gemini/` and `.claude/` configs |

## Output Files

- `scan-results/gemini-env-manifest.json` — Structured data for aggregation (counts-only by default, no raw prompts)
- `scan-results/gemini-env-report.md` — Human-readable markdown report (always contains full detail)

**Privacy model:** The manifest strips user prompts, thought topics, and project names, replacing them with `user_prompt_count`, `topic_count`, and `project_count`. The AI synthesis pipeline uses full data in-memory before redaction. Pass `--include-prompts` for raw data in the manifest.

## Reading the Report

After running, read `scan-results/gemini-env-report.md` and present findings:

1. **Maturity Score** (0–67) with tier and breakdown
2. **MCP Servers** — configured integrations
3. **Skills & Extensions** — installed across all tools, with origin tags (Auto/User)
4. **Memory Architecture** — 4-tier table with word counts and file counts
5. **Skill Extraction** — auto-created skills, inbox backlog, extraction health
6. **Conversation Intelligence** — top tools, models, tokens, behavioral chain patterns
7. **Emerging Patterns** — weak-evidence patterns not yet skill-worthy
8. **Advisory Recommendations** — categorized by severity (critical/warning/info)
9. **Code Repos** — project-level configs if `--repos` was used
10. **AI Ecosystem** — cross-tool skill overlap analysis

## Gotchas

- **Privacy by default** — manifest contains only aggregate counts; raw prompts and project names require `--include-prompts`
- `--repos ~/Code` discovers repos recursively — use `--repo-depth 2` on large directories
- Without API credentials, scanner runs but skips skill suggestions
- Evidence gate may skip API calls if conversation history is too sparse (< 10 prompts or patterns only in 1 project)
- System admin policy dirs require elevated permissions — scanner silently skips if inaccessible
- Stale `.extraction.lock` files (>30 min) indicate a crashed extraction run

## Validation

```bash
ls -la scan-results/gemini-env-manifest.json scan-results/gemini-env-report.md
node -e "JSON.parse(require('fs').readFileSync('scan-results/gemini-env-manifest.json', 'utf8')); console.log('✓ Valid JSON')"
node -e "const m = JSON.parse(require('fs').readFileSync('scan-results/gemini-env-manifest.json', 'utf8')); console.log('Score:', m.sophistication_score?.total + '/' + m.sophistication_score?.max)"
node -e "const m = JSON.parse(require('fs').readFileSync('scan-results/gemini-env-manifest.json', 'utf8')); console.log('Skills suggested:', (m.suggested_skills||[]).length)"
```
