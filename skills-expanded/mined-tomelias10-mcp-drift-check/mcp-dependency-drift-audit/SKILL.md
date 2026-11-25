---
name: mcp-dependency-drift-audit
description: Audit MCP configuration files for mutable npm/npx package references and explain reproducibility risk without executing MCP servers. Use when reviewing .mcp.json, Cursor, VS Code, Claude, or Windsurf MCP configuration before approval or CI.
---

# MCP Dependency Drift Audit

Audit MCP configuration **statically** for package references that can resolve to different code later even when the configuration file itself has not changed.

This workflow is for reproducibility and review-boundary checks. A mutable package reference is **not** proof that a package is malicious, vulnerable, or compromised.

## When to Use This Skill

- Before approving a repository's MCP configuration.
- When adding MCP configuration checks to a pull request or CI pipeline.
- During an AI-agent security review where npm/npx-backed MCP servers are present.
- When a team wants to know whether a previously reviewed MCP config can silently resolve to newer package code.

## Safety Boundary

- Never execute commands copied from an MCP configuration.
- Never start a discovered MCP server as part of this audit.
- Never expose credentials, tokens, Authorization headers, or private configuration contents in the report.
- Do not claim exploitation or compromise from dependency mutability alone.
- If a network download is needed to obtain a scanner, tell the user first and get approval before fetching it.

## Workflow

### 1. Locate MCP configuration files

Inspect the current project for known MCP configuration paths such as:

- `.mcp.json`
- `.cursor/mcp.json`
- `.vscode/mcp.json`
- other clearly identified MCP client config files supplied by the user

Read the files as text/JSON only. Do not run any `command` or `args` value found inside them. Stay inside the requested workspace by default; use `scan-all` only if the user explicitly asks for user-level/global MCP configuration too.

### 2. Prefer the zero-execution scanner when available

If `mcp-drift-check` is already installed, run the repo-scoped mode from the intended workspace root:

```bash
mcp-drift-check scan-workspace --markdown
```

For CI-oriented output:

```bash
mcp-drift-check scan-workspace --sarif mcp-drift.sarif --markdown
```

If it is not installed, offer the user this one-shot command and explain that it fetches the open-source scanner from GitHub before running it:

```bash
uvx --from git+https://github.com/tomelias10/mcp-drift-check mcp-drift-check scan-workspace --markdown
```

Do not fetch or install anything if the user declines network access. Use the manual rules below instead.

### 3. Manual classification fallback

For npm/npx-style MCP launch commands, classify package selectors as follows:

- `package@1.2.3` or `@scope/package@1.2.3` → **SAFE** for version reproducibility.
- bare `package` or bare `@scope/package` → **HIGH** because future resolution can select different package code.
- `package@latest` → **HIGH** because the selector is explicitly mutable.
- ranges such as `package@^1.2.0`, `~1.2.0`, `>=1.2.0`, or wildcard selectors → **MEDIUM** because resolution may change inside the allowed range.
- local paths, binaries, scripts, or unknown executables → **REVIEW**; npm version-drift rules do not establish their update behavior.

Treat `-y` / `--yes` as context only. It reduces interactive confirmation but is not a vulnerability by itself.

### 4. Recommend remediation without guessing versions

For mutable npm/npx references, recommend pinning to an **exact version that the team has actually reviewed** and updating it deliberately.

Do not invent or guess the correct version. If the user wants help selecting a version, explain that checking a package registry requires network access and ask before doing so.

Pinning improves reproducibility; it does not establish package provenance, code safety, authorization safety, or runtime isolation.

### 5. Report concisely

Return a table with:

| Config | MCP server | Package/reference | Classification | Why | Recommended next step |
| --- | --- | --- | --- | --- | --- |

Then include exactly these interpretation notes when relevant:

- No MCP servers were executed during the audit.
- Mutable dependency references are review/reproducibility signals, not breach claims.
- A clean dependency-drift result is not a complete MCP security assessment.

## Example

**User:** "Audit this repo's MCP config before we approve it. Don't run any MCP servers."

**Example output:**

```text
.mcp.json | browser | @example/browser-mcp@latest | HIGH
Reason: @latest can resolve to different package code later.
Next step: pin the exact version your team reviews and update it deliberately.

No MCP servers were executed.
```

## CI Example

For teams that want the check on every pull request, MCP Drift Check also ships a GitHub Action and SARIF output for GitHub Code Scanning:

```yaml
- uses: actions/checkout@v4
- uses: tomelias10/mcp-drift-check@v0
```

The scanner is MIT licensed and designed to be zero-execution: it does not start discovered MCP servers, download discovered packages, require an API token, collect telemetry, or upload configuration data.

**Inspired by:** the public [MCP Drift Check](https://github.com/tomelias10/mcp-drift-check) workflow and public MCP configuration review examples.
