---
name: br
description: >-
  Use the br CLI to inspect Bitrise CI builds, fetch logs, and diagnose failures.
  Use when investigating Bitrise build status, analyzing CI failures, fetching
  build logs with --failed-only, resolving app slugs, running br doctor, or when
  the user mentions Bitrise, br build, or .br.yml.
---

# br — Bitrise CLI for agents

`br` is a `gh`-style CLI for Bitrise. Prefer **`--json` output** for inspection.

## Prerequisites

```bash
brew install novr/taps/br          # macOS
go install github.com/novr/bitrise-cli/cmd/br@latest
```

Linux: download from [GitHub Releases](https://github.com/novr/bitrise-cli/releases).

**Auth** — env vars beat stored config. Override the config directory with `BR_CONFIG_DIR` (empty = unset; default `$HOME/.config/br`):

```bash
export BITRISE_API_TOKEN=<token>   # preferred; BITRISE_TOKEN also works
echo "$BITRISE_API_TOKEN" | br auth login --with-token   # CI / scripts
br auth status

# isolate accounts without profiles (direnv, etc.)
# .envrc: export BR_CONFIG_DIR="$HOME/.config/br-work"
export BR_CONFIG_DIR="$HOME/.config/br-work"
```

Token: [Bitrise Personal Access Token](https://app.bitrise.io/me/profile#/security). Workspace API tokens work; `br auth login` greeting may skip `/me` but `Client.Verify` uses `GET /apps?limit=1`.

When auth or app resolution fails, run `br doctor` first (exits non-zero if issues remain — suitable for CI).

## App slug resolution

Build commands need a Bitrise app slug. Priority:

1. `--app <slug>`
2. `BITRISE_APP_SLUG`
3. `.br.yml` (`app:` key) — walk cwd → git root
4. `git remote get-url origin` matched against Bitrise apps

If origin matches no accessible app, the command **errors** (no silent fallback). Pin with `br config set app <slug>` or `--app`.

```bash
br config show
br config set app <app-slug>   # writes .br.yml in cwd
br doctor                      # auth + resolution + API reachability
br doctor --app <slug>         # override slug for diagnosis only
```

## Standard workflow

```bash
# 1. Latest build on current branch (structured)
br build list --branch @current --limit 1 --json status,statusCode,buildNumber,branch,workflow

# 2. Latest build (any branch)
br build list --limit 1 --json status,statusCode,buildNumber,branch,workflow

# 3. If still running — wait for completion
br build watch <buildNumber> --exit-status --json status,buildNumber,failedSteps

# 4. If failed — structured step logs (agent) or raw errors only
br build logs <buildNumber> --json steps,failedStepLogs
br build logs <buildNumber> --failed-only

# 5. Optional build metadata with failed step names (no log bodies)
br build view <buildNumber> --json status,buildNumber,failedSteps
```

`build logs` and `build view` take **build number** (`#123`), not build slug.

### Status filters (`build list --status`)

`success`, `running`, `aborted`, and any of `failed` / `failure` / `error` (all map to Bitrise status code 2).

### JSON `status` vs `statusCode`

`--json status` mirrors Bitrise `status_text` (failed builds often show `"error"`). For programmatic checks, use `statusCode`: `0=running`, `1=success`, `2=failed/error`, `3=aborted`.

**Build list fields:** `branch`, `buildNumber`, `commitHash`, `commitMessage`, `durationSeconds`, `finishedAt`, `slug`, `status`, `statusCode`, `triggeredAt`, `workflow` — or `all` / `*`.

**Build view fields:** same as list plus `failedSteps` (`[{name, exitCode}]`). Log is fetched only when `failedSteps` is requested (or with `all`). Output is a single JSON object.

**Build logs JSON fields:** `steps` (`[{name, exitCode}]`), `failedStepLogs` (`[{name, exitCode, body}]`) — or `all` / `*`. Mutually exclusive with `--failed-only`. `failedSteps` (view/watch) has no log bodies; use `failedStepLogs` here.

**App list fields:** `repoURL`, `slug`, `title` — or `all` / `*`.

`--json` takes a **separate token** (not `=`):

```bash
br build list --limit 3 --json status,buildNumber,branch,workflow
br app list --json slug,title,repoURL
```

Unknown field names error with the valid list.

## Commands

| Command | Notes |
|---------|-------|
| `br build list` | `--limit`, `--branch`, `--workflow`, `--status`, `--json` |
| `br build watch <n>` | Poll until finished; `--exit-status`, `--json`, `--interval` |
| `br build view <n>` | `--json`; includes `failedSteps` on failed builds |
| `br build logs <n>` | Full log; `--failed-only` or `--json steps,failedStepLogs` |
| `br app list` | Apps visible to the token; `--json` |
| `br config show` | Token config + effective `.br.yml` |
| `br doctor` | Diagnostics; non-zero exit on failure |
| `br auth login` / `logout` / `status` | Token management |
| `br version` | CLI version |

## `.br.yml` and monorepos

```yaml
app: <app-slug>
```

Discovery walks up to **git root** (not `bitrise.yml`). Subpackages can override with a nearer `.br.yml`. `br doctor` warns when `.br.yml` slug disagrees with git-detected slug.

Global config stores **token only**; app slugs belong in `.br.yml` (commit for team sharing). Do not add token or profile fields to `.br.yml`.

## Agent tips

- Run from the **target project directory** (or pass `--app` / set `BITRISE_APP_SLUG`).
- Prefer `--failed-only` over full logs when analyzing failures.
- `--failed-only` / `--json` are **best-effort**: they parse Bitrise step headers. On parse failure, stderr says to re-run without those flags; empty output may mean no failures or an unparseable log format.
- **Running builds:** use `br build watch <n>` to poll until finished (`--exit-status` for CI). With `--json`, poll output is discarded so stdout is only the final JSON object. `build logs` returns a snapshot (not a live stream).
- `build view` and `--failed-only` share `parseLogSteps` — step names stay consistent.
- Ctrl+C cancels in-flight API calls (`signal.NotifyContext` on root command).
