---
name: claude-3p-parity
description: Diagnose and repair Claude Desktop Mac third-party inference / 3p / DeepSeek-style Claude Code setups for best-effort parity with first-party Claude Code. Use when users mention Claude Code Mac app developer mode, Claude Desktop 3p, third-party API providers, DeepSeek V4 Pro/Flash, bypassPermissions not working, repeated Allow prompts, missing Code/Cowork capabilities, missing web/search/browser/Chrome/CDP/MCP/skills/plugins, stale embedded Claude Code runtime, or requests to make a third-party Claude Code app behave like the original app.
---

# Claude 3p Parity

## Core Rule

Treat parity as best-effort. Do not claim third-party inference can become identical to first-party Claude. Auto mode, macOS privacy prompts, provider-side model support, and missing `/v1/models` discovery cannot always be fixed by local settings.

Always inspect first. A "one-click repair" still means: run dry-run, read the current state and missing items, summarize the planned changes for the user, then apply only after the user has explicitly approved the write step. The only exception is when the user has already said in the same turn to apply without another confirmation.

## Workflow

1. Run the bundled script in dry-run mode first:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py
   ```

2. Review the report's `inspection`, `connectivity`, and `changes` sections. Tell the user:

   - what the current Claude/3p/MCP/runtime state is;
   - which expected permissions, env vars, MCP servers, model mappings, runtime pieces, or network paths are missing;
   - exactly which files or external settings the apply step will change;
   - whether live network probing was skipped or approved. By default, the script only inspects proxy/npm/git config to avoid permission popups.
   - whether secret-looking values are present in config files. Do not print the values; tell the user which file contains them and whether the location is expected.

3. Only run live network probes when the user approves possible outbound-network permission prompts:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py --network-check
   ```

4. If npm/GitHub/Hugging Face/Claude release downloads are blocked or slow in mainland China, prefer this order:

   - use an existing user proxy if one is already configured;
   - ask before injecting a proxy into Claude/MCP env with `--proxy-url`;
   - ask before changing global npm config with `--set-npm-registry https://registry.npmmirror.com`;
   - keep `HF_ENDPOINT=https://hf-mirror.com` for memory/embedding tools;
   - use `NO_PROXY` for localhost/private-network routes when a proxy is supplied;
   - use `NODE_EXTRA_CA_CERTS` or `CLAUDE_CODE_CERT_STORE=system` for corporate TLS inspection, not TLS verification disablement;
   - do not run runtime overlay until `https://downloads.claude.ai/` is reachable through direct network or proxy.

5. If the plan matches the user's target, apply normal config repairs:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py --apply
   ```

   By default, the current working directory is treated as the trusted workspace. To target a different project folder:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
     --apply \
     --workspace-dir ~/Projects/my-app
   ```

   Do not add the whole home directory unless the user explicitly asks for maximum local access:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
     --apply \
     --allow-home-directory
   ```

6. Use an aggressive permission profile only when the user explicitly wants fewer prompts and understands this broadens local tool access:

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py --apply --permission-profile aggressive
   ```

7. Use runtime overlay only when Desktop 3p is pinned to an old embedded Claude Code runtime and the user explicitly approves. Claude must be fully quit first.

   ```bash
   python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py --apply --runtime-overlay 2.1.131
   ```

8. After any apply step, restart Claude Desktop and start a new Code/Cowork session. Verify with the report or by checking:

   ```bash
   ~/Library/Application\ Support/Claude-3p/claude-code/2.1.121/claude.app/Contents/MacOS/claude --version
   cat ~/Library/Application\ Support/Claude-3p/claude-code-vm/.sdk-version
   ```

## What The Script Repairs

- `~/.claude/settings.json`: bypass permission defaults, protected-path prompt skip, common tool allowlist, additional directories, sandbox knobs, DeepSeek V4 Pro/Flash model environment (with `[1m]` context suffix), subagent model, effort level (`xhigh` via `effortLevel` + `CLAUDE_CODE_EFFORT_LEVEL=max`), autocompact threshold (`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80`), API timeout (`API_TIMEOUT_MS=600000` for max-effort thinking), alwaysThinkingEnabled, showThinkingSummaries, and optional auto-allow PermissionRequest hooks. The default workspace is the current directory; use `--workspace-dir` or `--allow-home-directory` for broader access.
- `~/.claudeignore`: auto-generates with sensible exclusions (node_modules, .git, binary files, secrets, etc.) to reduce noise in tool results and save tokens. Existing files are merged rather than overwritten.
- cc-switch compatibility: `--cc-switch-compatible` strips `[1m]` suffix from model names and defaults gateway URL to cc-switch's local proxy (`http://127.0.0.1:15721`), avoiding the silent Flash fallback issue.
- Third-party model routing env: `ANTHROPIC_BASE_URL`, model slot aliases (both Pro and Flash get `[1m]` suffix for full 1M context), `CLAUDE_CODE_SUBAGENT_MODEL`, and optional API key/auth token env only when the user explicitly asks for key writing.
- Permission rules: uses official MCP permission forms like `mcp__playwright` and `mcp__playwright__*`; optionally keeps deny rules for common secret paths so `Read(*)`/`Edit(*)` do not silently expose `.env`, SSH, AWS, kube, or GitHub credentials.
- WebFetch behavior: sets `skipWebFetchPreflight` by default for gateway/3p use cases where the Anthropic domain safety preflight would be blocked or irrelevant.
- `~/.claude.json`: enables Claude Code auto-updates and keeps native update protection.
- `~/Library/Application Support/Claude-3p/claude_desktop_config.json`: keeps 3p mode and enables useful Code/Cowork preferences.
- `~/Library/Application Support/Claude-3p/configLibrary/*.json`: normalizes third-party inference model entries, optional gateway base URL/API key, workspace folder access, local MCP/extension switches, and Cowork egress host allowlist.
- MCP: installs a practical MCP baseline through official `claude mcp add-json --scope user` and also writes legacy `~/.mcp.json` by default for older/3p setups. Use `--mcp-scope user|local|project|legacy-home|both` to change this.
- Network/bootstrap checks: default dry-run inspects current proxy/npm/git settings without outbound probes; `--network-check` probes npm official registry, npmmirror, GitHub, Hugging Face, hf-mirror, and Claude Code release downloads after user approval.
- Optional network bootstrap: `--proxy-url` injects proxy env into Claude and MCP servers, `--no-proxy` sets proxy bypasses, `--node-extra-ca-certs` / `--cert-store` handle TLS inspection, `--set-npm-registry` changes user npm registry only when explicitly requested, and `--set-npm-proxy` writes npm proxy settings only when explicitly requested.
- Optional plugin install: `--install-plugin name@marketplace` runs the official plugin installer only when explicitly requested. Enabling a plugin in settings is not the same as installing it.
- Optional live diagnostics: `--run-claude-checks` runs `claude doctor`, `claude mcp list`, and `claude plugin list`; warn the user that MCP health checks may spawn configured servers.
- Secret hygiene: checks core config files for token/private-key patterns without printing values.
- Desktop 3p runtime overlay: optional, backed up, checksum-verified, and locally re-signed when needed.

## Guardrails

Read `references/limits.md` before promising a fix for missing first-party behavior. In particular:

- Do not present macOS Accessibility, Screen Recording, Automation, or file privacy prompts as Claude Code permission prompts.
- Do not present DeepSeek's Anthropic-compatible `/messages` success as proof that `/v1/models` discovery works.
- Do not promise `/model` picker parity for non-`claude`/`anthropic` model IDs. If discovery fails or filters out provider model names, use environment-variable model aliases.
- Do not silently run `--runtime-overlay`; it modifies local Desktop runtime files and may be overwritten by a future Desktop update.
- Do not silently change global npm proxy/registry settings. Ask first because it affects the user's whole Node/npm environment.
- Do not silently install plugins. Plugins and marketplaces can execute arbitrary local code.
- Do not rely on SOCKS proxy URLs; Claude Code supports HTTP/HTTPS proxy env vars, not SOCKS directly.
- Do not expose API keys in output. The script redacts common key/token fields.

## Common Adjustments

For non-DeepSeek providers, pass explicit models:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --apply \
  --pro-model provider-pro-model \
  --flash-model provider-fast-model
```

For DeepSeek-compatible Desktop configuration:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --apply \
  --gateway-base-url https://api.deepseek.com/anthropic
```

For cc-switch local proxy compatibility (strips `[1m]` suffix, defaults to `http://127.0.0.1:15721`):

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --apply \
  --cc-switch-compatible
```

When using cc-switch, do NOT add `[1m]` to model names — the suffix is Claude Code client syntax that cc-switch's proxy does not strip, causing DeepSeek to silently fall back to Flash.

Only pass `--gateway-api-key` if the user explicitly asks the skill to write the key into Desktop 3p config.

If the user also wants the CLI/runtime env to carry the key, require explicit confirmation and use:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --apply \
  --gateway-api-key sk-... \
  --write-api-key-to-env
```

For mainland China network bootstrap, inspect first:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py
```

Then, only after the user approves, apply with a proxy and npm mirror:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --apply \
  --proxy-url http://127.0.0.1:7890 \
  --no-proxy localhost,127.0.0.1,::1 \
  --set-npm-registry https://registry.npmmirror.com
```

For live verification after config writes:

```bash
python3 ~/.claude/skills/claude-3p-parity/scripts/claude_3p_parity.py \
  --run-claude-checks
```
