---
name: security-scanner
version: 0.1.0
description: |
  MCP server providing Checkov (IaC), Semgrep (source), Bandit (Python), and
  ASH (multi-tool) security scanning. Produces SECURITY.md reports. Requires
  Docker or local tool install. No external API keys required.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [security, swe, qa-agent]
mcp: security-scanner
trigger: scan|checkov|semgrep|bandit|vulnerability|IaC|security report
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Security Scanner MCP

Security scanning via MCP tools. Start with Docker, then invoke tools directly.

## Quick Start

```bash
docker compose up security-scanner
```

## MCP Tools

| Tool | Input |
|------|-------|
| `scan_with_checkov` | `code: str`, `format_type: str` |
| `scan_with_semgrep` | `code: str`, `language: str` |
| `scan_with_bandit` | `code: str` |
| `scan_directory_with_checkov` | `directory_path: str` |
| `scan_directory_with_semgrep` | `directory_path: str`, `language: str` |
| `scan_directory_with_bandit` | `directory_path: str` |
| `scan_directory_with_ash` | `directory_path: str` |
| `generate_security_report` | `project_name: str`, `scan_results: str` |
```
