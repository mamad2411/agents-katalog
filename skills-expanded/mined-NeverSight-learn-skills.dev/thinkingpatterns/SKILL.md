---
name: thinkingpatterns
description: "Security findings management for AI-assisted development. Use when running analysis agents, uploading scan results, or fixing findings in a project."
---

# ThinkingPatterns Security Platform

You have access to ThinkingPatterns tools for managing security findings. Tools are available via **MCP** (if configured) and **CLI** (`tp` commands). Both interfaces cover the same core operations — use whichever is available, preferring CLI when both are present for token efficiency.

## Setup check

Before starting, determine which interface is available:
- Run `tp --version` — if it succeeds, CLI is installed
- Run `tp whoami` — if it succeeds, CLI is authenticated
- If not authenticated, run `tp login` to save credentials
- Check if MCP tools are available by attempting `list_projects`
- If neither works, install via: `npx skills add thinkingpatternsai/skills` (installs this skill + CLI for your agent)
- If `tp` is not installed but Node.js is available, use `npx @thinkingpatterns/cli@latest` as a prefix. For best performance, install globally: `npm install -g @thinkingpatterns/cli`

## Interface selection

| Situation | Use | Why |
|-----------|-----|-----|
| CLI (`tp`) is available | **CLI** | 10–32x cheaper in tokens, 100% reliable, no schema overhead |
| Only MCP is configured | **MCP** | Full tool access via structured protocol |
| Bulk operations (10+ findings) | **CLI** | Loop in shell, no per-call LLM overhead |
| First time exploring the platform | **MCP** | Dynamic discovery of available tools |
| CI/CD pipeline or script | **CLI** | Deterministic, no LLM required |

**Rule of thumb:** If you can run `tp --help` successfully, prefer CLI. Fall back to MCP when CLI is unavailable.

## Available operations

| Operation | MCP tool | CLI command |
|-----------|----------|-------------|
| List findings | `list_findings` | `tp findings list --project <id> [--severity critical] [--status open] [--module-path src/]` |
| Get finding detail | `get_finding` | `tp findings get <finding-id>` |
| Triage a finding | `triage_finding` | `tp findings triage <finding-id> --action accept [--reason "..."]` |
| Bulk triage | `bulk_triage` | `tp findings bulk-triage --ids <id1,id2,...> --action dismiss --reason "..."` |
| Add comment | `add_comment` | `tp findings comment <finding-id> --body "..."` |
| List projects | `list_projects` | `tp projects list` |
| Get metrics | `get_metrics` | `tp metrics --project <id>` |
| Top risk modules | `get_top_risk_modules` | `tp risk-modules --project <id> [--limit 10]` |
| List runs | `list_runs` | `tp runs list --project <id>` |
| Ingest SARIF | `ingest_sarif` | `tp ingest sarif --project <id> --file results.sarif` |
| List agents | `list_agents` | `tp agents list` |
| Get agent | `get_agent` | `tp agents get <agent-id>` |
| Create agent | `create_agent` | `tp agents create --name "Name" --slug name --skill-md ./SKILL.md` |
| Run agent | `run_agent` | `tp agents run <agent-id> --project <id>` |
| Check auth | — | `tp whoami` |

## Common workflows

### Security review of current state

**Via CLI:**
```bash
tp projects list
tp metrics --project <id>
tp findings list --project <id> --severity critical --status open
tp findings list --project <id> --severity high --status open
tp findings get <finding-id>   # for each critical finding
```

**Via MCP:**
1. `list_projects` to find the relevant project
2. `get_metrics` for the project health overview (MTTR, fix rate, open count)
3. `list_findings` with `severity: "critical"` then `severity: "high"`
4. `get_finding` for each critical finding to understand details
5. Present a summary to the user with recommendations

### Fix findings

1. List open findings: `tp findings list --project <id> --status open` or `list_findings`
2. For each finding, get details: `tp findings get <id>` or `get_finding`
3. Read the code at `code_location_file`:`code_location_line_start`, understand the issue
4. Apply the minimal fix that resolves the root cause
5. Comment what was changed: `tp findings comment <id> --body "..."` or `add_comment`
6. Close the finding: `tp findings triage <id> --action complete` or `triage_finding`
7. For one fix resolving multiple findings, use bulk triage:
   - CLI: `tp findings bulk-triage --ids <id1,id2,id3> --action complete --reason "Fixed in commit abc123"`
   - MCP: `bulk_triage` with `action: "complete"`

### Post-code-change security check

1. List findings in the changed area:
   - CLI: `tp findings list --project <id> --module-path src/lib/auth/`
   - MCP: `list_findings` with `module_path: "src/lib/auth/"`
2. Review any findings in the modified area
3. Fix and complete findings as appropriate

### Bulk operations (CLI preferred)

For operations touching many findings, CLI avoids per-call token overhead:

```bash
# Dismiss all info-level findings in test files
tp findings list --project <id> --severity info --module-path test/ \
  | jq -r '.data[].id' \
  | xargs -I{} tp findings triage {} --action dismiss --reason "Test file, informational only"

# Export critical findings as JSON for reporting
tp findings list --project <id> --severity critical > critical-findings.json
```

### Run an agent analysis

1. Discover agents: `tp agents list` or `list_agents`
2. Run the agent: `tp agents run <agent-id> --project <id>` or `run_agent`
3. Follow the returned SKILL.md workflow step by step, using available tools
4. When done, ingest results: `tp ingest sarif --project <id> --file results.sarif` or `ingest_sarif`

### Manage agents

1. List agents: `tp agents list` or `list_agents`
2. Inspect an agent: `tp agents get <agent-id>` or `get_agent`
3. Create a new agent: `tp agents create --name "My Agent" --slug my-agent --skill-md ./SKILL.md` or `create_agent`
4. Agents are workflow definitions (SKILL.md + MCP configs) that always output SARIF

## Important notes

- The `project_id` is a UUID. Use `tp projects list` or `list_projects` first if you don't know it
- If a `.thinkingpatterns.json` file exists in the repo root, it contains the `project_id` — CLI reads it automatically so `--project` can be omitted
- Findings have `code_location_file` and `code_location_line_start` fields — use these to navigate to affected code
- Metrics include MTTR (mean time to resolution in days), fix_rate_7d (percentage), and rework_ratio (findings reopened)
- Triage decisions (accept, dismiss, defer, reopen) are handled by humans — focus on scanning and fixing
- CLI outputs JSON by default, making it easy to pipe to `jq` or other tools
- Run `tp login` to authenticate once — credentials are saved to `~/.thinkingpatterns/credentials.json`
- CLI commands also accept `--api-key` flag or `TP_API_KEY` env var as overrides (useful for CI/CD)
