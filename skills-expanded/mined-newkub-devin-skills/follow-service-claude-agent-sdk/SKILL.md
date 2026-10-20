---
name: follow-service-claude-agent-sdk
description: Use @anthropic-ai/claude-agent-sdk to build AI agents — query, tools, MCP, sessions
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test

---

## Goal

Use @anthropic-ai/claude-agent-sdk to build AI agents — query, tools, MCP, sessions

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (service claude agent sdk)

## Execute

### Workflows

| Topic  | Workflow |
|--------|----------|
| Setup  | `## Merged Details → setup-claude-agent-sdk` — SDK install, `ANTHROPIC_API_KEY` |
| Config | `## Merged Details → config-claude-agent-sdk` — model, tools, permissions, sessions config |
| Verify | `## Merged Details → verify-connection` — API key valid, minimal query responds |

Read `workflows/<name>/SKILL.md` per topic and follow the flow there — do not execute from this table directly

### 1. Setup And Usage

> Goal: Use it correctly per the official docs

Latest: `@anthropic-ai/claude-agent-sdk@0.3.283` (verified 2026-09-26) — renamed from the `claude-code` SDK; the entry point is `query()`

1. Use the `query()` function as the entry point — a streaming async iterator
1. Set `options`: model, allowedTools, mcpServers, systemPrompt
1. Use `tool()` + `createSdkMcpServer` for in-process custom tools
1. Manage sessions with `sessionId`/`resume` for multi-turn

### 2. Verify

> Goal: Confirm correct usage

1. Do `/run-verify` for lint, typecheck
2. Do `/run-test` if relevant tests exist
3. Check the latest official docs before using an uncertain API (service claude agent sdk)

## Rules

- ANTHROPIC_API_KEY required in env — never hardcode
- Control tools explicitly with `allowedTools`/`disallowedTools`
- Server-side only — never bundle into a client
- Set `maxTurns`/`permissionMode` appropriate to the use case

## Merged Details

### config-claude-agent-sdk

##### Goal

Set/edit `query()` options of `@anthropic-ai/claude-agent-sdk` — model, tools, permissions, MCP servers, and sessions — merging with the existing config

##### Scope

- Covers the `options` object, custom tools (`tool()` + `createSdkMcpServer`), and session resume
- If not installed/API key missing → do `## Merged Details → setup-claude-agent-sdk` first

##### Execute

###### 1. Read Current Config

> Goal: Know the current options before editing

1. Read the `query()` call sites and the options passed
2. Do `/deep-review-codebase` domain `review-config` if config lives separately in other files
3. If no `query()` is found → do `## Merged Details → setup-claude-agent-sdk` first

###### 2. Configure Model And Prompt

> Goal: model/system prompt match the use case

1. Set `options.model` per the use case — verify the latest model names from the official docs before use
2. Set `options.systemPrompt` for the agent's behavior
3. Set `options.maxTurns` and `options.cwd` suitably for the task

###### 3. Configure Tools And Permissions

> Goal: the agent accesses only the tools it needs

1. Define `allowedTools`/`disallowedTools` explicitly — never enable every tool without need
2. Set `permissionMode` to match the use case (`default`, `acceptEdits`, `bypassPermissions`, etc. — see official docs)
3. Custom tools → use `tool()` + `createSdkMcpServer`, then pass via `options.mcpServers`
4. External MCP servers → declare in `options.mcpServers` per the SDK schema

###### 4. Configure Sessions

> Goal: multi-turn conversations work correctly

1. Use `sessionId`/`resume` in options to resume an existing session
2. Manage session lifecycle — store the session id per user/conversation

###### 5. Verify

> Goal: config works with the real agent

1. Run a test `query()` with the new options — confirm tools are allowed/denied as set
2. Do `/run-verify` and `/run-test` if relevant tests exist
3. If broken → revert the key just changed, then report the diff

##### Rules

- Control tools explicitly with `allowedTools`/`disallowedTools` — least privilege
- Set `maxTurns`/`permissionMode` appropriate to the use case — never `bypassPermissions` unless required
- Secrets in `mcpServers` config go through `/follow-secret-manager`
- Use official docs https://docs.claude.com/en/api/agent-sdk for uncertain options

##### Expected Outcome

- Model, tools, permissions correct per least privilege
- Custom tools/MCP servers work
- Session resume works — lint, typecheck, tests pass

### setup-claude-agent-sdk

##### Goal

Install `@anthropic-ai/claude-agent-sdk` and prepare `ANTHROPIC_API_KEY` so `query()` can call the agent — first-time setup

##### Scope

- Install the package and make a minimal `query()` call server-side
- Configure the API key via a secret manager
- If already set up → verify only; model/tools/permissions config → `## Merged Details → config-claude-agent-sdk`

##### Execute

###### 1. Check Prerequisites

> Goal: Confirm the project is ready and not yet set up

1. Check `package.json` for `@anthropic-ai/claude-agent-sdk` — if present → skip to verify
2. Check env/secrets for `ANTHROPIC_API_KEY`
3. If the key is missing → do `/open-web-for-config-secret` pointing the user to the Anthropic Console

###### 2. Install SDK

> Goal: Install the SDK server-side

1. Run `bun add @anthropic-ai/claude-agent-sdk` (or the project's package manager)
2. Confirm the import works with `import { query } from '@anthropic-ai/claude-agent-sdk'`
3. Confirm it runs server-side only — never bundle into a client

###### 3. Configure API Key

> Goal: key safe, not committed

1. Store `ANTHROPIC_API_KEY` via `/follow-secret-manager` — never hardcode or commit
2. The SDK reads the env automatically — no need to pass the key in code

###### 4. Smoke Test

> Goal: `query()` actually works

1. Run a minimal call:
   ```typescript
   for await (const msg of query({ prompt: 'Say hi', options: { maxTurns: 1 } })) {
     console.log(msg)
   }
   ```
2. Confirm an assistant message comes back without an auth error

###### 5. Verify

> Goal: the SDK is ready to use

1. Do `/run-verify` for lint, typecheck
2. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report
3. Success → do `/suggest-next-action`

##### Rules

- `ANTHROPIC_API_KEY` required in env — never hardcode
- Server-side only — never bundle into a client
- Use official docs https://docs.claude.com/en/api/agent-sdk when unsure about the API

##### Expected Outcome

- SDK installed and `query()` works server-side
- API key stored in the secret manager
- Ready for `## Merged Details → config-claude-agent-sdk`

### verify-connection

##### Goal

Confirm after setup/config that the Claude Agent SDK really connects to the Anthropic API — key valid, model available, query responds

##### Scope

- Used when `/follow-service-claude-agent-sdk` dispatches to `verify`/`verify-connection`
- Read-only: check only — do not change config

##### Execute

###### 1. Check API Key

> Goal: `ANTHROPIC_API_KEY` exists and has the right format

1. Check the env var has a value (do not print it)
2. Check the key is not a placeholder (`sk-ant-...` format)

###### 2. Smoke Test Query

> Goal: the API really responds

1. Run a minimal SDK call — e.g. a short query or a model list if the SDK supports it
2. Confirm the response is not 401/403 (auth) or 429 (rate limit)
3. Record rough latency as a baseline

###### 3. Report

> Goal: Summarize connection status

1. Use `/report` columns: `No.`, `Check`, `Result`, `Evidence`
2. Verdict: `connected` / `auth-failed` / `rate-limited` / `unreachable`

##### Rules

- Use minimal queries only — control token cost
- Do not print the API key
- Auth failure → recommend `/follow-secret-manager` — do not fix it yourself

##### Expected Outcome

- Connection verdict with model/latency evidence

### references/package-manifest

#### Package Manifest

> Metadata of the primary package(s) this skill installs or covers. Update during `/update-devin-global-skills` or `/deep-review-codebase` runs.

##### Primary Package

| Field | Value |
|-------|-------|
| Package | `@anthropic-ai/claude-agent-sdk` |
| Registry | `npm` |
| Latest Version | `0.3.273` |
| Release Date | `2026-09-11` |
| Verified | `2026-09-12` (date this file was last checked) |
| Author / Publisher | Anthropic |
| License | `SEE LICENSE IN README.md` |
| Repository | `https://github.com/anthropics/claude-agent-sdk-typescript` |
| Website | `https://www.anthropic.com/` |
| Documentation | `https://docs.claude.com/en/api/agent-sdk/overview` |
| Releases / Changelog | `https://github.com/anthropics/claude-agent-sdk-typescript/releases` |

##### Install

```bash
bun add @anthropic-ai/claude-agent-sdk
```

##### Secondary Packages

| Package | Registry | Latest | Notes |
|---------|----------|--------|-------|
| `claude-code` | `npm` | `unknown` | Legacy package name — SDK was renamed to `@anthropic-ai/claude-agent-sdk` |

##### Notes

- Breaking changes in latest major: still `0.x` — API surface may change between minor releases; entry point is `query()`
- Version pinned in SKILL.md: `0.3.273`

## Expected Outcome

- Library used correctly per best practices (service claude agent sdk)
- No known security/performance pitfalls (service claude agent sdk)
- Lint, typecheck, tests pass