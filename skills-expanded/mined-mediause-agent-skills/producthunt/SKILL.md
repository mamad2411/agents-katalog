---
name: producthunt
description: Use when handling MediaUse Product Hunt automation tasks, including launch feed retrieval, hot ranking, single product detail extraction, and category browse search, with Windows install, key onboarding, strict context/auth flow, and safety/rate controls.
---

# MediaUse Product Hunt Skill

Collect Product Hunt launch intelligence with a stable workflow for latest feeds, hot lists, category browse, and single product detail parsing.

## Scope

Use this skill when the task targets Product Hunt operations such as:

- Get lists: posts, today, hot
- Get detail: single product detail by URL
- Search: browse products by category
- Trace: execution verification and recovery

Current command set is read-only. No publish/reply/engage write actions are exposed by this plugin.

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

- .mediause/skills/producthunt/SKILL.md

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
2. Bind account context with use account.
3. Check status with auth health.
4. Execute Product Hunt dynamic actions.
5. Verify with trace/task.

### 3.1 Discover and plugin setup

```powershell
mediause plugin list --json
mediause plugin add producthunt --json
mediause producthunt -h
mediause producthunt get -h
mediause producthunt search -h
```

### 3.2 Bind context before actions

use account must be executed successfully before any get/search action.

use account argument format:

- <platform:account_id>
- account_id should be selected from mediause auth list --json.

```powershell
mediause auth list --json
mediause use account producthunt:guest --policy balanced --json
```

If challenge/risk prompts appear, reopen in visible mode:

```powershell
mediause use account producthunt:guest --policy balanced --show --json
```

### 3.3 Auth health precondition

auth health is valid only after successful use account.

```powershell
mediause auth health --json
```

If auth health indicates expired for a non-guest account:

```powershell
mediause auth login producthunt --json
mediause use account producthunt:<account_id> --policy balanced --json
mediause auth health --json
```

### 3.4 Guest mode

Product Hunt plugin exposes guest as default account context.

```powershell
mediause use account producthunt:guest --json
```

Guest mode rules:

- Read-only operations only.
- Write operations are not part of this plugin command set.

## 4. Product Hunt Dynamic Command Map (v1)

Source schema:

- plugin: plugin.producthunt
- manifest: crates/platforms/plugins/producthunt/manifest.yaml

### 4.1 get.*

- mediause producthunt get posts [--limit <n>] [--category <name>] --json
- mediause producthunt get today [--limit <n>] --json
- mediause producthunt get hot [--limit <n>] --json
- mediause producthunt get detail --url <product_url_or_slug> [--comments-limit <n>] --json

Parameter notes:

- --limit default is 20.
- --url is required for get detail.
- --comments-limit default is 20 and controls extracted comment count.

Typical detail return fields:

- product: name, tagline, description
- company: name, website
- team: maker names and profile links
- tags: topic tags
- comments: ranked comments up to comments limit
- meta: title, description, canonical, og-style metadata
- jsonLd: extracted structured data blocks

### 4.2 search.*

- mediause producthunt search browse --category <slug> [--limit <n>] --json

Category example values:

- developer-tools
- productivity
- artificial-intelligence

## 5. Operational Constraints (Mandatory)

Apply these constraints for all actions to reduce risk and keep behavior stable.

### 5.1 Human-like pacing

- Avoid tight polling loops.
- Add randomized delay between repeated actions.
- Mix list and detail actions instead of repeating one endpoint.

### 5.2 Frequency limits and minimum spacing

- Hard stop if operation rate is abnormally high.
- Stop immediately on repeated challenge/risk prompts.

Suggested limits:

- get/search/detail reads: <= 60 per minute

Minimum spacing:

- get/search/detail reads: >= 1 second between actions

Same-target guardrails:

- Repeated detail on same URL: >= 5 seconds

If a limit is hit:

1. Pause at least 5 minutes.
2. Resume with lower request frequency.
3. Re-check context health before continuing.

### 5.3 Safety policy

- Do not bypass platform protections.
- Do not attempt credential scraping or session hijacking.
- Respect platform terms and local regulations.

### 5.4 Output and error handling

- Prefer --json output for machine workflows.
- Require structured error handling with stable fields/code when available.
- On challenge pages, stop and return actionable next steps.

Known Product Hunt challenge behavior:

- get detail may return blocked error when Cloudflare challenge is active.
- Handle code producthunt.get.detail.blocked by reopening context with --show and retrying.

## 6. Workflow Examples

### 6.1 Daily launch scan

```powershell
mediause use account producthunt:guest --json
mediause producthunt get today --limit 20 --json
mediause trace last --json
```

### 6.2 Category browse then open one detail

```powershell
mediause use account producthunt:guest --json
mediause producthunt search browse --category developer-tools --limit 20 --json
mediause producthunt get detail --url https://www.producthunt.com/products/notion --comments-limit 20 --json
mediause trace last --json
```

### 6.3 Hot ranking monitor

```powershell
mediause use account producthunt:guest --json
mediause producthunt get hot --limit 30 --json
mediause trace last --json
```

## 7. Execution Checklist

Before run:

Before every run, execute the install script once.

1. CLI installed and available in PATH; verify with mediause --version on Windows.
2. PATH updated and mediause --version works.
3. API key configured and verified.
4. Account context bound via mediause use account <platform:account_id>.
5. auth health checked after context bind when non-guest account is used.
6. If not logged in on non-guest account, run mediause auth login producthunt --json and re-bind context.
7. Pacing policy is enabled.

During run:

1. Respect delays and minimum spacing.
2. Stop on anti-bot/challenge prompts.
3. Avoid repetitive burst loops.

After run:

1. Save logs and outcomes.
2. Record risk warnings and cooldown events.
3. Keep activity under conservative limits.

## 8. Quick Command Reference

```powershell
# always run once before each workflow (auto-upgrade latest)
mediause --version
mediause --version

# discover
mediause plugin list --json
mediause plugin add producthunt --json
mediause producthunt -h
mediause producthunt get -h
mediause producthunt search -h

# context + status
mediause auth list --json
mediause use account producthunt:guest --json
mediause auth health --json

# read actions
mediause producthunt get posts --limit 20 --json
mediause producthunt get today --limit 20 --json
mediause producthunt get hot --limit 20 --json
mediause producthunt get detail --url https://www.producthunt.com/products/notion --comments-limit 20 --json
mediause producthunt search browse --category developer-tools --limit 20 --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-team
Last-Updated: 2026-08-22
Version: v2


