---
name: compute-actions-cli
description: Drive ComputeSDK Actions — the platform's CI engine that runs GitHub-style workflow YAML in sandboxes on your org's compute providers — from a shell with `compute actions` from @computesdk/cli 2.x. Use when dispatching or inspecting ComputeSDK Actions CI runs, streaming logs, checking flakiness, managing vault secrets/variables, or configuring repos and provider credentials.
---

# `compute actions` — CI runs on hosted sandboxes

ComputeSDK Actions runs ordinary GitHub Actions workflow YAML (`.github/workflows/*.yml`) inside ComputeSDK sandboxes placed on the providers your organization registers — jobs execute under `act` and report `provider:region` placement. Actions is free for every organization. The `compute` CLI (`@computesdk/cli` 2.x, binary `compute`; group also reachable as `compute ci`) drives the whole surface against `https://platform.computesdk.com` (`/api/v1/actions`).

`compute market` (the sell side of the compute market) exists as a sibling command group but is out of scope for this skill.

## Install, auth, output

```bash
npm i -g @computesdk/cli        # or: npx @computesdk/cli <cmd>
compute --version               # must show 2.x
```

If `--version` shows 1.0.x, an old standalone binary (`~/.local/bin/compute`) is shadowing the npm install — remove it.

- **Interactive:** `compute login` — OAuth device flow (open the URL, enter the code). `compute logout` clears it. One login covers `compute actions`, `compute sandboxes`, `compute market`, and `compute bench`.
- **Non-interactive (CI, agents):** prefer an org API key (Settings → API keys). Resolution order: `--api-key <key>` → `COMPUTE_API_KEY` → `BENCHMARKS_PLATFORM_API_KEY` (legacy) → stored `compute login` session.
- **Another platform host:** `--base-url <url>` or `COMPUTE_PLATFORM_URL`. Non-`computesdk.com` hosts also need `--allow-untrusted-host` (explicit keys only — stored logins are never sent there).
- **Multi-org accounts (2.1+):** `compute org list` shows your orgs, `compute org use <slug>` sets the persisted active org, `compute org current` (or `compute whoami`) shows the user + active org. Org selection per command resolves `--org <slug>` → `COMPUTE_ORG` → the login's saved org; the `compute login` approval screen also offers an org picker. Org API keys are tied to one org — `--org`/`COMPUTE_ORG` don't apply to them. Every subcommand accepts `--org`.
- Every subcommand accepts `--api-key`, `--base-url`, `--allow-untrusted-host`, `--org`, and `--json`. **Agents should always pass `--json`** — failures land on stderr as a single error envelope.
- `insufficient_scope` or 401 errors → run `compute login` again.
- **Admin-only:** dispatch, rerun, cancel, provider credentials, settings, and vault writes need an org owner or admin — whether you authenticate by login or API key.
- Never echo, print, or commit API keys or secrets; read them from environment variables.

## Dispatch and follow runs

```bash
compute actions dispatch <owner/repo> --workflow <path|name|id> [--ref <ref>]
    [--inputs key=value ...] [--manual]
    [--provider <id>[:<region>] | --provider-region <region>]
    [--max-bid <usd> --max-bid-per second|minute|hour]
compute actions runs <owner/repo> [--status passed|failed|running|cancelled|none ...] [--branch ...]
compute actions history <owner/repo> --workflow <w> [--branch ...] [--job <j>] [--limit n]  # ≤50, --workflow required
compute actions run <run-id>        # jobs, provider:region placement, attempts, benchmarks digest
compute actions benchmarks <run-id> # benchmark runs this run produced: provider · score · success (--json for all rows)
compute actions summary <run-id>    # failure digest: failed jobs/steps + redacted log tails
compute actions inspect <run-id>    # resolved image, caches, secret names, concurrency
compute actions logs <run-id> [--job <j>] [--step <n|runner>] [--follow]
compute actions artifacts <run-id> [--job <j>] [--out <dir>]
compute actions cancel <run-id>     # owner/admin
compute actions rerun <run-id>      # owner/admin; same commit, deduped by requestId
```

- `--workflow` matches the workflow's **full path** (`.github/workflows/ci.yml`), its display name, or its id — a bare basename like `ci.yml` will not resolve.
- `--manual` runs a workflow that doesn't declare `workflow_dispatch`; such runs take no `--inputs`.
- **`--max-bid`** prices a compute-market fill per vCPU, in the unit given by `--max-bid-per` (default `second`; `minute`/`hour` for coarser caps). If the market doesn't fill the bid, the job falls through to the next provider in the org's order.
- Logs are byte-addressed and resumable — `--follow` reconnects pick up where the last read ended.
- **Check `history` before fixing a failure:** per-job/per-step failure rollups tell a regression from a flaky step; `failedBeforeSteps` counts jobs that died before any step ran (platform flakiness, not broken code).
- Run dashboard URL: `https://platform.computesdk.com/<orgSlug>/actions/runs/<runId>`.

## Repos

```bash
compute actions repos                                        # connected repos
compute actions repos connect <cloneUrl> [--name o/r] [--branch <b>]
    [--token <t> | --username <u> --token <t> | --ssh-key-file <f> [--known-hosts-file <f>]]
compute actions repos enable|disable <owner/repo> [--repo-id <id>]
compute actions repos sync                                   # re-read the GitHub App installation
```

Connect via the platform GitHub App (repo access + push/PR triggers) or a generic git remote — http(s) token/basic, ssh, or unauthenticated. `connect` validates with a real `ls-remote` and lands enabled. A repo granted to the App after install shows up on the next `sync`; `enable` runs that sync itself when the repo isn't listed yet.

`--token <t>` puts the credential in the process arguments (visible in `ps` and shell history). Prefer `--ssh-key-file` for private repos, or an ssh remote; use `--token` only on single-user machines.

## Provider credentials

```bash
compute actions providers                                     # regions, act/usable status
compute actions providers configure <provider> --key <key> [--verify]
compute actions providers configure <provider> --field name=value ...   # multi-field
compute actions providers verify <provider>                   # probe with a real sandbox
compute actions providers remove <provider>                   # refused while live boxes need it
```

Credentials are bring-your-own, stored encrypted and never readable again. Jobs walk the org's provider order (`provider[:region]` entries, `market` allowed) and every refusal lands on the job's `placementAttempts`. Providers without built-in dockerd need `verify` to prove act-capability before jobs will place on them.

## Vault — secrets and variables

```bash
compute actions vault ls [--repo o/r] [--kind secret|variable]   # names/metadata only, never values
compute actions vault set <name> [--repo] [--kind] [--revealable] [--description] [--labels]
    [--proxy --hosts <hosts...> | --inject]                      # value from stdin or --from-file —
                                                               # NEVER a command argument; stored exactly as read
compute actions vault delivery <name> [--repo] [--kind] (--proxy --hosts <hosts...> | --inject)
                                                               # reclassify delivery — labels only, no value
compute actions vault get <name> [--repo] [--kind]               # variables, or secrets created --revealable
compute actions vault rm <name> [--repo] [--kind]
```

Secrets reach workflows as `${{ secrets.NAME }}` and are masked in logs; variables (`vars.NAME`) are always readable config. `--revealable` is fixed at creation — a non-revealable secret can only be replaced, not read. A repo item overrides the same-named org item. Use `printf '%s' "$VALUE" | compute actions vault set NAME` (no trailing newline).

Delivery (`--proxy`/`--inject`) is the credential-proxy classification: `--proxy --hosts api.github.com,*.github.com` hands the job a `pk-proxy-NAME` placeholder and the control plane attaches the real value to matching requests — it never enters the sandbox; `--inject` (the default) writes the real value into the job environment. `vault delivery` reclassifies an existing secret without its value — the labels-only PATCH exists because labels are immutable on `vault set`.

## Org settings

```bash
compute actions settings                                  # routing policy
compute actions settings set [--order market,blaxel|default]
    [--order-type limit|market] [--general-cap <usd>/<unit>|none]
    [--cap <size>=<usd>/<unit>|<size>=none]...            # --cap repeatable
```

`settings` prints the Actions lane's routing policy — order type (`limit` by default), general market cap, per-size caps (`—` when unset, with the size's reference price), provider order, sizes, warm pool, snapshot pool. `settings set` PATCHes `GET/PATCH /api/v1/actions/settings`; owner/admin only (non-admin → "Only org owners/admins can change actions settings"). `--order default` restores the platform default order; `--general-cap none` and `--cap <size>=none` clear caps; units are required, same parser as `--max-price`. The sandbox lane (`compute sandboxes settings`) inherits these values where its own are unset.

## Run local changes without committing

`--with-changes` diffs the working tree against the remote ref (tracked + untracked files, run from
any subdirectory), uploads the patch, and the run applies it after checkout. A workflow file that
only exists locally is dispatched by path and defines the run.

```bash
compute actions dispatch myorg/myrepo --workflow .github/workflows/bench.yml --with-changes --json
```

Dispatching from a dirty tree without the flag prints a hint. Refused on untrusted hosts.

## Benchmark results on a run

A run that executed a benchmark carries its numbers; read them instead of parsing logs:

```bash
compute actions benchmarks <run-id>          # per-provider table, each provider's overall row
compute actions benchmarks <run-id> --json   # { runId, conclusion, benchmarks: [{ benchmarkSlug, status, dashboardUrl, providers }] }
```

`benchmarks: []` = the workflow ran no benchmark; a benchmark still running is listed with
`providers: []`. The Actions conclusion is the job exit code — a provider failing tasks shows as
`successRate < 1`, not a failed run. Edit → `dispatch --with-changes` → `benchmarks` is the iteration loop.

## Typical workflow

```bash
compute actions dispatch myorg/myrepo --workflow .github/workflows/ci.yml --ref main --inputs env=staging --json
compute actions runs myorg/myrepo --status running
compute actions logs <run-id> --follow
compute actions summary <run-id>            # if it fails
compute actions artifacts <run-id> --out ./artifacts
```

dispatch → `runs`/`run` → `logs --follow` → `summary` on failure → `benchmarks` for bench runs → `artifacts --out`.

## References

- Actions docs: https://github.com/computesdk/computesdk/blob/main/docs/platform/actions.md
- CLI docs: https://github.com/computesdk/computesdk/blob/main/docs/platform/cli.md
- API reference: https://github.com/computesdk/computesdk/blob/main/docs/platform/api-reference.md
- REST users: the same surface lives under `https://platform.computesdk.com/api/v1/actions/*` with `Authorization: Bearer $COMPUTE_API_KEY`.
