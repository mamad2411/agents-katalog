---
name: google
description: Standardized Google skill for MediaUse. Includes Windows install, key onboarding, strict context/auth flow, full Google dynamic command map, and safety/rate controls.
---

# MediaUse Google Skill

Run Google discovery flows for keyword exploration, result retrieval, and repeatable read-first research workflows.

## Scope

Use this skill when the task targets Google operations such as:

- Account: health check
- Search: web results, query suggestions
- Get: news headlines, daily trends

Google skill is guest-only.

- Use `mediause use account google:guest --json`.
- `use account` defaults to a hidden browser session.
- If you need to see the browser, use `mediause use account google:guest --show --json`.
- `--show` usually lowers repeated anti-bot interception risk in challenged sessions.
- Do not call `mediause auth login google --json` for this skill.
- If Google shows an `unusual traffic` prompt or captcha, rerun `use account` with `--show` and complete the verification manually.

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

- .mediause/skills/google/SKILL.md

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
3. Execute dynamic site actions.
4. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add google --json
mediause google -h
mediause google search -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch/read action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

Google manifest default account id is `guest`.

By default, `use account` keeps the browser hidden. Use `--show` only when you need to inspect the page or manually resolve a challenge.

```powershell
mediause auth list --json
mediause use account google:guest --policy balanced --json
```

### 3.3 Auth health

`auth health` is not required for the normal Google guest flow.

Use it only as an optional diagnostic command if the runtime needs an explicit session check.

```powershell
mediause auth health --json
```

### 3.4 Guest mode

Google plugin exposes `guest` as the default account context.

```powershell
mediause use account google:guest --json
```

Guest mode rules:

- Read-only operations only.
- This plugin command set does not include write operations.
- No login flow is required.
- Default mode keeps the browser hidden.
- Use `mediause use account google:guest --show --json` when you need to complete captcha or `unusual traffic` verification manually.

## 4. Google Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.google`
- manifest: `crates/platforms/plugins/google/manifest.yaml`

### 4.1 account.*

- `mediause google account health --json`

### 4.2 search.*

- `mediause google search web --keyword <keyword> [--limit <n>] [--lang <lang>] --json`
- `mediause google search suggest --keyword <keyword> [--lang <lang>] --json`

### 4.3 get.*

- `mediause google get news [--keyword <keyword>] [--limit <n>] [--lang <lang>] [--region <region>] --json`
- `mediause google get trends [--region <region>] [--limit <n>] --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce risk and keep behavior stable.

### 5.1 Human-like pacing

- Avoid tight polling loops.
- Add randomized delay between repeated reads/searches.
- Mix different read actions instead of repeatedly hitting one endpoint.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated anti-bot challenge or risk prompt.

Suggested limits:

- Search/get/account read actions: <= 60 per minute

Minimum spacing:

- Search/get/account read actions: >= 1 second between actions

Same-target guardrails:

- Repeated query on the same keyword/region pair: >= 3 seconds

If a limit is hit:

1. Pause at least 5 minutes.
2. Resume with lower request frequency.
3. Re-check session health if account context changed.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer `--json` output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On blocked/rate-limit/risk prompt, stop and return actionable next steps.
- If Google returns `unusual traffic` or a captcha wall, reopen the session with `mediause use account google:guest --show --json`, complete the verification manually, then rerun the read action.

## 6. Workflow Examples

### 6.1 Web search to news follow-up

```powershell
mediause use account google:guest --json
mediause google search web --keyword "agent browser" --limit 10 --lang en --json
mediause google get news --keyword "agent browser" --limit 10 --lang en --region US --json
mediause trace last --json
```

### 6.2 Trends and suggestions loop

```powershell
mediause use account google:guest --json
mediause google get trends --region US --limit 20 --json
mediause google search suggest --keyword "ai coding" --lang en --json
mediause trace last --json
```

### 6.3 Account health check branch

```powershell
mediause use account google:guest --json
mediause google account health --json
mediause trace last --json
```

### 6.4 Unusual traffic recovery

```powershell
mediause use account google:guest --show --json
# complete the captcha or unusual traffic verification in the visible browser
mediause google search web --keyword "agent browser" --limit 10 --lang en --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account google:guest --json`.
5. Login is not required for this skill.
6. If manual verification may be needed, be ready to rerun `use account` with `--show`.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. If `unusual traffic` appears, rerun `mediause use account google:guest --show --json` and complete the verification manually.
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
mediause plugin add google --json
mediause google -h
mediause google search -h

# context + status
mediause auth list --json
mediause use account google:guest --json
mediause use account google:guest --show --json

# read actions
mediause google search web --keyword "open source" --limit 10 --json
mediause google search suggest --keyword "open source" --json
mediause google get news --keyword "open source" --limit 10 --json
mediause google get trends --region US --limit 20 --json

# account health + trace
mediause google account health --json
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2




