---
name: modelgo-shared
version: 0.1.4
description: "modelgo-cli setup, command routing, and troubleshooting. Use when the user first runs modelgo, sees permission/scope errors, needs to update, asks about installation, or when you need to pick which modelgo command fits an intent. Triggers: 安装 modelgo, modelgo install, modelgo upgrade, modelgo update, modelgo permission, modelgo error, modelgo setup, install modelgo-cli."
metadata:
  requires:
    bins: ["modelgo"]
  cliHelp: "modelgo --help"
---

# modelgo-cli setup and troubleshooting

This skill is the shared helper for the `modelgo` CLI. Other `modelgo-*` skills
(`modelgo-inspect`, `modelgo-x402`) assume the basics here.

## Skill / CLI version check (agent — do first)

**Before** following this skill or any `reference/` file, confirm the installed
skill matches the installed `modelgo` binary. Stale skills document flags that
may no longer exist.

1. **Skill version** — read `version` in the YAML frontmatter at the top of this file.
2. **CLI version** — run `modelgo --version` (prints e.g. `v0.1.2`; compare only `X.Y.Z`, dropping the leading `v`).
3. **Dev builds** — if `modelgo --version` is `v0.0.0-dev` (or `dev`), it is a local build; skip the check.
4. **Compare** — if the two `X.Y.Z` strings differ, refresh **before** running any command from this skill:
   ```bash
   npx @model-go/cli@latest install
   ```
   This is idempotent: it upgrades the binary and re-syncs the `modelgo-*` skills.
5. **Re-check** — run `modelgo --version` again and confirm it matches this file's `version`.
6. **Missing `modelgo`** — if `modelgo --version` fails, install it (see [Install or upgrade](#install-or-upgrade)).

## Command reference (authoritative)

Per-command flags, usage, and examples are documented in:

- [`reference/index.md`](reference/index.md) — quick index, global conventions, exit codes
- [`reference/<group>.md`](reference/) — per command group (e.g. [`reference/auth.md`](reference/auth.md), [`reference/env.md`](reference/env.md), [`reference/tenant.md`](reference/tenant.md))

These are auto-generated from the CLI's own `--help`. Don't guess flags — read
the reference file or run `modelgo <command> --help`. (`balance`, `permissions`,
`logs` live in the `modelgo-inspect` skill; `pay` lives in `modelgo-x402`.)

## When to use which command

| User intent | Command | Skill |
| --- | --- | --- |
| Log in / authorize | `modelgo auth login` | this skill |
| Check login status | `modelgo auth status` | this skill |
| Log out | `modelgo auth logout [--all]` | this skill |
| Switch environment (cn / intl / custom) | `modelgo env use <name>` | this skill |
| List / add / remove environments | `modelgo env list` / `env add` / `env remove` | this skill |
| Switch the active tenant | `modelgo tenant use <slug\|id>` | this skill |
| List logged-in tenants | `modelgo tenant list [--remote]` | this skill |
| Balance / billing / grant status | `modelgo balance [transactions\|grant]` | `modelgo-inspect` |
| Account permissions / accessible menus | `modelgo permissions` | `modelgo-inspect` |
| Call logs / latency / cost / usage | `modelgo logs [<id>\|stats\|usage]` | `modelgo-inspect` |
| Pay-per-call model API (x402, no login) | `modelgo pay request` | `modelgo-x402` |
| Inspect / build x402 payment headers | `modelgo pay methods\|header\|status\|set` | `modelgo-x402` |

## Global conventions

- `--json` — structured JSON on **stdout** for success. On error, the CLI writes a plain-text message to **stderr** and exits non-zero (there is no JSON error envelope).
- `--env <name>` — operate against a specific env instead of the active one. **Accepted only by `auth`, `tenant`, and `pay request`**; `balance`/`permissions`/`logs` always use the active env (switch with `modelgo env use <name>`), and passing `--env` to them is a usage error (exit 2).
- `--tenant <slug\|id>` — a **global** flag placed *before* the subcommand (e.g. `modelgo --tenant acme balance`); selects which logged-in tenant's credential authenticates the call, for `balance`, `permissions`, and `logs`. An unknown tenant errors (exit 1, names the tenant); passing `--tenant` to any other command is a usage error (exit 2). To change the *default* tenant instead, use `modelgo tenant use <slug\|id>`.
- `--config PATH` / `--store PATH` — override `~/.modelgo/config.json` and `~/.modelgo/auth.json`.
- **Exit codes:** `0` success · `1` runtime error (auth / permission / network / API / CLI) · `2` usage error.

## Install or upgrade

Run the official install command. It is idempotent — running it again upgrades
to the latest version and re-syncs skills.

```bash
npx @model-go/cli@latest install
```

Verify install:

```bash
modelgo --version
```

## Commands

Currently available commands (full flags in [`reference/`](reference/index.md)):

- `modelgo auth login [--env NAME] [--scope SCOPE]` — log in with ModelGo device authorization
- `modelgo auth login --no-wait --json` — get a verification URL and device code without blocking
- `modelgo auth login --device-code CODE` — resume polling after the user approves the URL from a prior `--no-wait` run
- `modelgo auth status` — show local login status
- `modelgo auth logout` — clear local credentials (`--all` clears every env)
- `modelgo env list` / `modelgo env use <name>` / `modelgo env add <name> --base-url URL` — manage environments (`cn`, `intl`, or custom)
- `modelgo tenant list [--remote]` / `modelgo tenant use <slug|id>` — manage the active tenant per env
- `modelgo balance` — view tenant balance, transactions, and grant status
- `modelgo permissions` — view account permissions and accessible menus
- `modelgo logs` — query call logs, statistics, and usage summaries
- `modelgo pay methods/header/request` — inspect x402 channels, build payment headers, or call model APIs through x402 pay-per-call

Features not listed in `modelgo --help` are not implemented yet. If the user asks
for a feature that isn't available, suggest filing an issue (see
[Report a CLI bug](#report-a-cli-bug)).

For non-streaming agent harnesses, prefer split-flow:

```bash
modelgo auth login --no-wait --json
```

Return the `verification_url` to the user exactly as printed and end the turn.
Do not show the URL and then immediately block on `modelgo auth login --device-code ...`
in the same turn; in final-message-only harnesses that prevents the user from
seeing the URL before the agent starts waiting.

After the user confirms approval in a later step, resume polling:

```bash
modelgo auth login --device-code <device_code>
```

## Troubleshooting

- **Command not found after install** — open a new terminal so the updated `PATH` from the npm global bin takes effect. Or run `npm bin -g` to find the install location and add it to `PATH`.
- **Network error during install** — set `https_proxy` if behind a firewall, or use a corporate npm mirror: `npm install -g @model-go/cli --registry=https://your-mirror/`.
- **`[SECURITY] Checksum mismatch`** — the downloaded binary did not match the expected SHA-256. Do not run it. Report the issue.
- **`session expired`** — run `modelgo auth login` to re-authenticate.
- **`permission denied`** — check access with `modelgo permissions`; the active tenant may lack the scope.

## Report a CLI bug

When a `modelgo` command fails and the cause is **not** a user/service-side error
(usage, auth, quota, permission, network the user can fix), it may be a CLI bug.
Classify the failure and, if it qualifies, offer to file a GitHub issue —
full protocol (EXCLUDE/INCLUDE rules, redaction, template, `gh` submission) in
[`assets/issue-reporting.md`](assets/issue-reporting.md).

Issue tracker: https://github.com/modelgo/modelgo-cli/issues
