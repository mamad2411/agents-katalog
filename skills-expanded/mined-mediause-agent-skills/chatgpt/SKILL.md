---
name: chatgpt
description: Standardized ChatGPT skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full ChatGPT dynamic command map, and safety/rate controls.
---

# MediaUse ChatGPT Skill

Use this skill to run structured ChatGPT workflows in MediaUse, including conversation control, prompt/response retrieval, and image generation with safe execution pacing.

## Scope

Use this skill when the task targets ChatGPT operations such as:

- Account: health check
- Chat: status, new conversation, send/ask prompts, read/history/detail
- Image: generate images from prompts

## 1. Install MediaUse CLI

Install the MediaUse CLI in the user's own secure environment using the official npm package:

```powershell
npm install -g @mediause/cli
mediause --version
```

If the CLI is already installed, run the version check again to confirm it is available in PATH.

Current support status:

- Windows: supported
- Linux: not supported yet
- macOS: not supported yet

Recommended skill install path:

- .mediause/skills/chatgpt/SKILL.md

## 2. Get and Configure MediaUse Key

### 2.1 Apply for key

1. Open https://mediause.dev/ in the user's browser.
2. Sign in to the user's account.
3. Open the Project settings.
4. Create or view the API key in the user's own secure environment; never paste it into chat, logs, terminal history, or a CLI command.

### 2.2 Configure key in CLI

```powershell
mediause manage key --json
```

## 3. Core Flow (Mandatory Order)

Always follow this order:

First step on every run: execute install script once to auto-install/auto-upgrade the latest MediaUse CLI.

1. Discover site and commands.
2. Bind account context with `use account`.
3. Check status with `auth health`.
4. Execute dynamic site actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add chatgpt --json
mediause chatgpt -h
mediause chatgpt chat -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch or interaction action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

By default, `use account` keeps the browser hidden. Use `--show` when manual observation or takeover is needed.

```powershell
mediause auth list --json
mediause use account chatgpt:<account_id> --policy balanced --json
```

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired:

```powershell
mediause auth login chatgpt --json
mediause use account chatgpt:<account_id> --policy balanced --json
mediause auth health --json
```

If page shows `unusual traffic`, captcha, or risk confirmation:

```powershell
mediause use account chatgpt:<account_id> --policy balanced --show --json
```

Risk reduction note:

- In challenged sessions, `--show` usually reduces repeated interception risk.

Complete verification manually, then rerun the action.

### 3.4 Guest mode (optional)

Manifest default account id is `guest`. Guest mode can be used only for read/chat actions when the runtime supports unauthenticated `chatgpt:guest` context (that is, `mediause use account chatgpt:guest --json` succeeds):

```powershell
mediause use account chatgpt:guest --json
```

Guest mode rules:

- Read/chat operations only (`chat.status`, `chat.new`, `chat.send`, `chat.ask`, `chat.read`, `chat.history`, `chat.detail`).
- `image.generate` may require logged-in account depending on current runtime and page state.
- If action is blocked in guest mode, switch to logged-in account context.

## 4. ChatGPT Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.chatgpt`
- manifest: `crates/platforms/plugins/chatgpt/manifest.yaml`

### 4.1 account.*

- `mediause chatgpt account health --json`

### 4.2 chat.*

- `mediause chatgpt chat status --json`
- `mediause chatgpt chat new --json`
- `mediause chatgpt chat send --prompt <text> [--new <bool>] --json`
- `mediause chatgpt chat ask --prompt <text> [--timeout <seconds>] [--new <bool>] --json`
- `mediause chatgpt chat read [--markdown <bool>] --json`
- `mediause chatgpt chat history [--limit <n>] --json`
- `mediause chatgpt chat detail --id <conversation_id> [--markdown <bool>] --json`

### 4.3 image.*

- `mediause chatgpt image generate --prompt <text> [--timeout <seconds>] --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce account risk and keep behavior stable.

### 5.1 Human-like pacing

- Never execute high-frequency prompt bursts continuously.
- Add randomized delay between repeated prompt/image requests.
- Add longer cooldown after long-running ask/generate operations.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated anti-bot challenge, login re-validation, or risk prompt.

Quick policy matrix:

- `chat.ask` / `chat.send`: <= 30 per hour, >= 5s spacing
- `image.generate`: <= 10 per hour, >= 30s spacing
- `chat.read` / `chat.history` / `chat.detail` / `chat.status`: <= 60 per minute, >= 1s spacing

If a limit is hit:

1. Pause at least 10 minutes.
2. Resume with read/status actions first.
3. Re-check session health before interaction actions.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer `--json` output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On blocked/rate-limit/risk prompt, stop and return actionable next steps.

## 6. Workflow Examples

### 6.1 Ask and read workflow

```powershell
mediause use account chatgpt:<account_id> --json
mediause auth health --json
mediause chatgpt chat ask --prompt "Summarize latest Rust async patterns" --timeout 90 --json
mediause chatgpt chat read --markdown true --json
mediause trace last --json
```

### 6.2 Conversation history and detail workflow

```powershell
mediause use account chatgpt:<account_id> --json
mediause auth health --json
mediause chatgpt chat history --limit 20 --json
mediause chatgpt chat detail --id <conversation_id> --markdown true --json
mediause trace last --json
```

### 6.3 New conversation and image generation workflow

```powershell
mediause use account chatgpt:<account_id> --json
mediause auth health --json
mediause chatgpt chat new --json
mediause chatgpt image generate --prompt "minimal poster design, geometric, red black white" --timeout 120 --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account chatgpt:<account_id> --json`.
5. If guest mode is used, verify the target action is actually supported in guest context.
6. If manual verification may be needed, be ready to rerun `use account` with `--show`.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. If `unusual traffic` appears, rerun `mediause use account chatgpt:<account_id> --show --json` and complete verification manually.
4. Avoid repetitive burst loops.

After run:

1. Save logs and outcomes.
2. Record any risk warning and cooldown events.
3. Keep activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add chatgpt --json
mediause chatgpt -h
mediause chatgpt chat -h

# context + status
mediause auth list --json
mediause use account chatgpt:<account_id> --json
mediause use account chatgpt:<account_id> --show --json
mediause auth health --json

# chat actions
mediause chatgpt account health --json
mediause chatgpt chat status --json
mediause chatgpt chat new --json
mediause chatgpt chat send --prompt "Draft a release note" --json
mediause chatgpt chat ask --prompt "Explain CAP theorem in simple terms" --timeout 90 --json
mediause chatgpt chat read --markdown true --json
mediause chatgpt chat history --limit 10 --json
mediause chatgpt chat detail --id <conversation_id> --markdown true --json

# image action
mediause chatgpt image generate --prompt "isometric dashboard illustration" --timeout 120 --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2




