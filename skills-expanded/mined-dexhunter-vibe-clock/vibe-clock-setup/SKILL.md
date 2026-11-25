---
name: vibe-clock-setup
description: Set up vibe-clock to track AI coding agent usage (Claude Code, Codex, Gemini CLI, OpenCode) and display SVG stats on a GitHub profile README.
license: MIT
compatibility:
  - claude-code
  - codex-cli
  - opencode
metadata:
  version: "0.2.0"
  author: dexhunter
  repository: https://github.com/dexhunter/vibe-clock
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# vibe-clock Setup

You are helping a user set up **vibe-clock**: a CLI that reads the session logs Claude Code, Codex, Gemini CLI, and OpenCode already write locally, and turns them into SVG charts on the user's GitHub profile.

`vibe-clock setup` performs the entire installation interactively. **Prefer it over doing the steps yourself.** This document exists to tell you what it is doing, what it asks for, and what to do when a step cannot be automated. Do not restate configuration the tool prints — read its output and respond to it.

## The one command

```bash
uv tool install vibe-clock      # or pipx install vibe-clock / pip install vibe-clock
vibe-clock setup
```

`setup` will, asking before each step that changes anything outside the machine:

1. Detect which agents have data directories.
2. Get a GitHub token — borrowed from `gh auth` when the GitHub CLI is authenticated, otherwise prompted for, with the token-creation URL printed.
3. Confirm the profile repo (defaults to `<login>/<login>` when `gh` can supply the login).
4. Print the **exact JSON** it would publish and wait for confirmation.
5. Create the public Gist.
6. Set the `VIBE_CLOCK_GIST_ID` repository secret with `gh secret set`, or print where to paste it.
7. Write `.github/workflows/vibe-clock.yml` if run from inside the profile repo checkout, or print it.
8. Install a daily local `vibe-clock push` (launchd, systemd user timer, or crontab).
9. Print the `<img>` markdown for the profile README.

Non-interactive form, for when you already know the answers:

```bash
vibe-clock setup --profile-repo OWNER/REPO --charts card,donut --yes
```

`--yes` accepts every prompt, including publishing the Gist. Use it only when the user has explicitly agreed to publish.

## Prerequisites

- Python 3.10+
- At least one supported agent with data: Claude Code (`~/.claude/`), Codex (`~/.codex/`), Gemini CLI (`~/.gemini/`), or OpenCode (`~/.local/share/opencode/`)
- A GitHub profile repo (`<username>/<username>`) with a README.md
- Either the `gh` CLI authenticated (`gh auth status`), **or** a **Classic** PAT with the `gist` scope. Fine-grained tokens cannot write Gists.

The `gist` scope is all that is needed. The `repo` scope is required only for the optional `github.trigger_workflow` setting, which makes `push` dispatch the render workflow immediately instead of waiting for its daily cron. Leave it off unless the user asks — `repo` grants read/write to every one of their repositories.

## Privacy — cover this before running `share` or `setup`

Everything stays local until the user confirms a preview. Show them the preview:

```bash
vibe-clock push --dry-run
```

The default payload has exactly ten fields: `schema_version`, `producer_version`, `generated_at` (floored to UTC midnight), `days_covered`, `active_days`, `total_sessions`, `total_minutes`, `active_agents`, `favorite_model`, and `models[]` (family names and session counts).

Never published, regardless of flags: file paths, the home directory, the username, real project or repository names (aliased to `Project A`, `Project B`, …), raw model IDs (reduced to families such as `Claude` / `OpenAI`), prompts, responses, code, session IDs, git data, and hostnames. `sanitizer.py` builds the payload from an allowlist — that is the guarantee. `_validate_no_pii` sits behind it as a backstop assertion over the fields carrying machine-derived text, so a future bug crashes locally instead of publishing.

`vibe-clock render` draws from that same allowlisted payload whether it collects locally or reads a Gist, so its SVGs are safe to commit. `vibe-clock export` is the one command that writes unsanitized data to a file.

Optional data is off unless requested, one flag each: `--daily-activity`, `--time-patterns`, `--message-counts`, `--token-counts`, `--project-aliases`. Enable only what the user asks for.

To stop publishing, `vibe-clock unshare` deletes the Gist **and its revision history**. A public Gist retains every past revision, so this is the only thing that removes previously published data.

## When automation is not available

If `gh` is missing, `setup` prints what to do at each step. The manual equivalents:

**Token** — [github.com/settings/tokens/new?scopes=gist](https://github.com/settings/tokens/new?scopes=gist&description=vibe-clock), Classic, `gist` scope.

**Secret** — profile repo → Settings → Secrets and variables → Actions → New repository secret, named `VIBE_CLOCK_GIST_ID`.

**Workflow** — `vibe-clock workflow` prints the file; `vibe-clock workflow --write` writes it to `.github/workflows/vibe-clock.yml`. It is:

```yaml
name: Update Vibe Clock Stats

on:
  schedule:
    # Runs after your local `vibe-clock push` updates the Gist.
    - cron: "30 0 * * *"
  workflow_dispatch:

# Required: the action commits the generated SVGs back to this repo, and
# GITHUB_TOKEN is read-only by default.
permissions:
  contents: write

concurrency:
  group: vibe-clock
  cancel-in-progress: false

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dexhunter/vibe-clock@v1.5.0
        with:
          gist_id: ${{ secrets.VIBE_CLOCK_GIST_ID }}
          chart_types: card,donut
```

The `permissions:` block is required. The action commits SVGs back to the repo, and `GITHUB_TOKEN` is read-only by default, so a workflow without it fails with a 403 on `git push`.

**README** — add the images the workflow generates:

```html
<p align="center">
  <img src="images/vibe-clock-card.svg" alt="Vibe Clock Stats" />
  <img src="images/vibe-clock-donut.svg" alt="Model Usage" />
</p>
```

Then run it once: profile repo → **Actions** → *Update Vibe Clock Stats* → **Run workflow**.

## Two clocks, both required

The local `vibe-clock push` writes the Gist; the Actions cron reads it and commits SVGs half an hour later. If the local push is not scheduled, the Gist goes stale and the profile freezes — the most common way a working setup silently stops working.

```bash
vibe-clock schedule           # daily, at the local equivalent of 00:00 UTC
```

Backends are chosen automatically: launchd on macOS, a systemd **user** timer on Linux, crontab otherwise. On Linux a user timer stops when the user logs out, unless `sudo loginctl enable-linger $USER` is set. Keep it a user unit: a system service with `ProtectHome=true` can neither execute a `uv tool` / `pipx` binary under `$HOME` nor read the agent logs. Windows has no backend — use WSL or Task Scheduler.

## Troubleshooting

- **403 on `git push` in the workflow**: missing `permissions: contents: write`. Compare against `vibe-clock workflow`.
- **`payload carries no schema_version`, or a version-skew error**: the machine running `push` is older than the action rendering it. `uv tool upgrade vibe-clock`, then push again. The failure is deliberate; the old behaviour was rendering a plausible but wrong number.
- **`chart 'X' needs ...`**: a requested chart needs data that was never shared. Re-run `share` with the named flag, or drop the chart from `chart_types`.
- **401 on push**: the token is fine-grained, or lacks `gist`. It must be a Classic PAT.
- **`vibe-clock: command not found`**: `~/.local/bin` is not on PATH (`uv tool update-shell`). If `vibe-clock --version` disagrees with what was just installed, run `which -a vibe-clock` — a `uv tool` install shadows a Homebrew one.
- **No sessions found**: check the agent data directories exist and contain session files (`~/.claude/projects/`, `~/.codex/sessions/`, `~/.gemini/`, `~/.local/share/opencode/storage/`).
- **SVGs stale in the README**: GitHub caches proxied images; wait or hard-refresh.

## Configuration reference

Config lives at `~/.config/vibe-clock/config.toml` (`0600`, in a `0700` directory). Rather than reproducing it here, read the live file, or see the Configuration section of [README.md](README.md), which is kept in sync with `config.py`.

Environment overrides: `GITHUB_TOKEN` (used only when the TOML token is empty), `VIBE_CLOCK_GIST_ID`, `VIBE_CLOCK_DAYS`.

Note that `vibe-clock init` only creates or refreshes the config file. It does not create the Gist, set the secret, write the workflow, or schedule anything — that is what `setup` is for.
