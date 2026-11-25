---
name: hackernews
description: Use when handling MediaUse Hacker News automation tasks, including story list retrieval, story search, item thread reading, and user profile lookup, with Windows install, key onboarding, strict context/auth flow, full dynamic command map, and safety/rate controls.
---

# MediaUse Hacker News Skill

Track Hacker News stories and discussions through a clean workflow for lists, search, thread reading, and user inspection.

## Scope

Use this skill when the task targets Hacker News operations such as:

- Get lists: top, best, ask, new, show, jobs
- Search: stories
- Read: item with comment tree controls
- User: profile lookup

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

- .mediause/skills/hackernews/SKILL.md

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
mediause plugin add hackernews --json
mediause hackernews -h
mediause hackernews get -h
```

### 3.2 Bind context before any read/write

`use account` must be executed successfully before any fetch/read action.

`use account` argument format:

- `<platform:account_id>`
- `account_id` should be selected from `mediause auth list --json`.

```powershell
mediause auth list --json
mediause use account hackernews:guest --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account hackernews:guest --policy balanced --show --json
```

`--show` usually lowers repeated interception risk in challenged sessions.

### 3.3 Auth health precondition

`auth health` is valid only after successful `use account`.

```powershell
mediause auth health --json
```

If `auth health` indicates not logged in/expired for a non-guest account:

```powershell
mediause auth login hackernews --json
mediause use account hackernews:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

Hacker News plugin exposes `guest` as default account context.

```powershell
mediause use account hackernews:guest --json
```

Guest mode rules:

- Read-only operations only.
- Write operations are not part of this plugin command set.

## 4. Hacker News Dynamic Command Map (v1)

Source schema:

- plugin: `plugin.hackernews`
- manifest: `crates/platforms/plugins/hackernews/manifest.yaml`

### 4.1 get.*

- `mediause hackernews get top [--limit <n>] --json`
- `mediause hackernews get best [--limit <n>] --json`
- `mediause hackernews get ask [--limit <n>] --json`
- `mediause hackernews get new [--limit <n>] --json`
- `mediause hackernews get show [--limit <n>] --json`
- `mediause hackernews get jobs [--limit <n>] --json`

### 4.2 search.*

- `mediause hackernews search stories --query <text> [--limit <n>] [--sort <value>] --json`

### 4.3 read.*

- `mediause hackernews read item --id <item_id> [--limit <n>] [--depth <n>] [--replies <n>] [--max-length <n>] --json`

### 4.4 user.*

- `mediause hackernews user profile --username <name> --json`

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce risk and keep behavior stable.

### 5.1 Human-like pacing

- Avoid tight polling loops.
- Add randomized delay between repeated reads/searches.
- Mix different read actions instead of repeatedly hitting the same endpoint.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated risk prompt or challenge.

Suggested limits:

- Get/search/read/user read: <= 60 per minute

Minimum spacing:

- Get/search/read/user read: >= 1 second between actions

Same-target guardrails:

- Repeated read on same item/user: >= 3 seconds

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

## 6. Workflow Examples

### 6.1 Top stories scan

```powershell
mediause use account hackernews:guest --json
mediause hackernews get top --limit 20 --json
mediause trace last --json
```

### 6.2 Search then read thread

```powershell
mediause use account hackernews:guest --json
mediause hackernews search stories --query "rust" --limit 10 --sort relevance --json
mediause hackernews read item --id <item_id> --depth 2 --replies 20 --max-length 2000 --json
mediause trace last --json
```

### 6.3 User profile lookup

```powershell
mediause use account hackernews:guest --json
mediause hackernews user profile --username <username> --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed via `npm install -g @mediause/cli` on Windows.
2. PATH updated and `mediause --version` works.
3. API key configured and verified.
4. Account context bound via `mediause use account <platform:account_id>`.
5. `mediause auth health --json` checked after context bind when non-guest account is used.
6. If not logged in on non-guest account, run `mediause auth login hackernews --json` and re-bind context.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/risk prompts.
3. Avoid repetitive burst loops.

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
mediause plugin add hackernews --json
mediause hackernews -h
mediause hackernews get -h

# context + status
mediause auth list --json
mediause use account hackernews:guest --json
mediause auth health --json

# read actions
mediause hackernews get top --limit 20 --json
mediause hackernews search stories --query "ai" --limit 10 --json
mediause hackernews read item --id <item_id> --depth 2 --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2




