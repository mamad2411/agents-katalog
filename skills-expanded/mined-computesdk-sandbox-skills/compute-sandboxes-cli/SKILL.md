---
name: compute-sandboxes-cli
description: Drive hosted ComputeSDK Platform sandboxes from a shell with `compute sandboxes` (alias `compute sbx`) from @computesdk/cli 2.x — create sandboxes on your org's providers or the compute market, run commands (one-shot `run`, `exec`, detached `spawn`), serve ports, copy files, get preview URLs, and take snapshots. Use when creating, running commands in, or managing hosted ComputeSDK sandboxes from a shell — no per-provider SDK or provider keys needed in your code.
---

# `compute sandboxes` — hosted sandboxes from the shell

The `compute` CLI (`@computesdk/cli`) drives the ComputeSDK Platform at `https://platform.computesdk.com`: it places a sandbox on your organization's own provider credentials (or a compute-market fill) via `/api/v1/sandboxes` and lets you exec commands, spawn processes, move files, resolve preview URLs, and snapshot — all without embedding a provider SDK. Requires @computesdk/cli **2.x**; creating sandboxes requires the org to have **Sandboxes enabled** (403 otherwise), and usage bills to the org.

`compute market` (the sell side of the compute market) exists as a sibling command group but is out of scope for this skill.

## Install, auth, output

```bash
npm i -g @computesdk/cli        # or: npx @computesdk/cli <cmd>
compute --version               # must show 2.x
```

If `--version` shows 1.0.x, an old standalone binary (`~/.local/bin/compute`) is shadowing the npm install — remove it.

- **Interactive:** `compute login` — OAuth device flow (open the URL, enter the code). `compute logout` clears it. One login covers `compute sandboxes`, `compute actions`, `compute market`, and `compute bench`.
- **Non-interactive (CI, agents):** prefer an org API key (create under Settings → API keys on the platform). Credential resolution order: `--api-key <key>` → `COMPUTE_API_KEY` → `BENCHMARKS_PLATFORM_API_KEY` (legacy) → stored `compute login` session.
- **Another platform host:** `--base-url <url>` or `COMPUTE_PLATFORM_URL`. Non-`computesdk.com` hosts also need `--allow-untrusted-host`, which applies to explicit keys only — stored logins are never sent there.
- **Multi-org accounts (2.1+):** `compute org list` shows your orgs, `compute org use <slug>` sets the persisted active org, `compute org current` (or `compute whoami`) shows the user + active org. Org selection per command resolves `--org <slug>` → `COMPUTE_ORG` → the login's saved org; the `compute login` approval screen also offers an org picker. Org API keys are tied to one org — `--org`/`COMPUTE_ORG` don't apply to them.
- **Agents:** always pass `--json` — machine-readable success output, and failures come back on stderr as a single error envelope.
- `insufficient_scope` or 401 errors → run `compute login` again.
- Never echo, print, or commit API keys or secrets; read them from environment variables.

## Commands

```bash
compute sandboxes create [--order market,blaxel,vercel] [--size small|medium|large|xlarge]
    [--label <l>] [--image <img>] [--snapshot-id <id>] [--cpus <n>] [--memory-mb <n>]
    [--disk-mb <n>] [--timeout-ms <ms>] [--max-price <usd>/<unit>]
    [--order-type market|limit | --market] [--secret <vaultName>...]
    # compact one-liner by default; -q prints only the ID, --verbose the details
compute sandboxes quote [--size|--cpus/--memory-mb/--disk-mb] [--region <r>]
    [--timeout-ms <ms>] [--order-type <t>|--market] [--max-price <usd>/<unit>]
    # dry-run of a create: provider/box, rate, caps, balance, ok or a reason code
compute sandboxes list [--status creating|running|destroyed] [--limit n] [--cursor c]
compute sandboxes get <id>          # provider, placement, cost
compute sandboxes destroy [id]      # ALWAYS destroy when done — sandboxes bill while running

compute sandboxes use <id> | use --clear   # mark/clear this directory's current instance
compute sandboxes run [create flags] [--keep] [-d|--detach] [--yes] -- <cmd...>
    # create+spawn+stream in one shot; destroys the instance at the end.
    # --keep keeps it (becomes current), -d returns immediately, -q prints only the ID.
    # TTY Ctrl-C asks Destroy/keep/detach; non-TTY Ctrl-C destroys.
compute sandboxes serve [id] --port <n> [--cwd <dir>] [-e K=V] -- <cmd...>
    # spawn a server, wait until the port listens on a public addr, print the URL.
    # Loopback-only binds fail with the 0.0.0.0 hint; -q prints only the URL.
compute sandboxes cp <src> <dst>              # one side local, one side [id:]/abs/path
    # copies files/dirs in both directions; -q prints nothing.

compute sandboxes exec [id] [--timeout-ms <ms>] <command...>      # one-off, buffered (~290s max)
compute sandboxes spawn [id] [--cwd <dir>] [-e K=V]... [--stdin] <command...>  # detached; returns a job ID
compute sandboxes ps [id]
compute sandboxes logs <id> <jobId> [-f|--follow]           # stream until exit
compute sandboxes wait <id> <jobId> [--timeout-ms]          # job keeps running on timeout
compute sandboxes kill <id> <jobId> [--signal SIGKILL]
compute sandboxes stdin <id> <jobId> [--data|--file|--base64|piped]  # needs spawn --stdin
compute sandboxes close-stdin <id> <jobId>

compute sandboxes ls <id> [path]
compute sandboxes cat <id> <path>
compute sandboxes write <id> <path> [--content|--file <local>|stdin]   # absolute paths
compute sandboxes mkdir <id> <path>
compute sandboxes rm <id> <path>

compute sandboxes url [id] --port <n> [--protocol <p>]      # public preview URL
compute sandboxes settings                                # org routing policy (admin: PATCH via `settings set`)
compute sandboxes settings set [--order market,blaxel|inherit]
    [--order-type limit|market|inherit] [--general-cap <usd>/<unit>|none]
    [--cap <size>=<usd>/<unit>|<size>=none]...            # --cap repeatable
compute sandboxes snapshots <id>                            # list
compute sandboxes snapshot <id> [--label <l>]               # snapshot a running box
compute sandboxes snapshot-delete <id> <snapshotId>
```

## Typical workflow

```bash
# market fills are limit orders by default — quote, then cap at that price
RATE=$(compute sandboxes quote --size medium --json | jq -r '.rateUsd.perHour // empty')
ID=$(compute sandboxes create --order market,blaxel,vercel \
    ${RATE:+--max-price "$RATE/hour"} --json | jq -r .id)
compute sandboxes write $ID /app/server.py --file ./server.py
compute sandboxes exec $ID pip install flask
compute sandboxes spawn $ID --cwd /app python /app/server.py        # returns a job ID
compute sandboxes logs $ID <jobId> --follow                         # Ctrl-C detaches; the job keeps running
compute sandboxes url $ID --port 5000                               # → https://...
compute sandboxes destroy $ID
```

`logs --follow` blocks until the job exits, so for a long-running server it never returns — detach with Ctrl-C (or run `url`/`destroy` from another shell) before continuing.

**Command flags pass through to the sandbox (2.1.1+).** Put CLI options *before* the command — everything after the command's first word goes to the sandboxed program untouched. `exec $ID uname -a` runs `uname -a` (not "unknown option"); `spawn $ID --cwd /app npm run dev` runs the dev server with its flags. Options may sit before `<id>` or between `<id>` and the command; a bare `--` ends option parsing explicitly (`exec $ID -- ls -la`). Unknown leading flags error with a hint instead of reaching the sandbox. `create --json` prints the sandbox object itself, so its id is `.id` (REST `POST /api/v1/sandboxes` wraps it: `.sandbox.id`).

create → write/exec → `spawn` for servers → `url --port` → **destroy**. Shortcuts: `run` does create→spawn→stream→destroy in one command; `serve` does spawn→wait-for-port→print-URL.

## Current instance

Most commands take `[id]` **optional**: resolution order is explicit `<id>` arg → `COMPUTE_INSTANCE` env var → this directory's stored pick (`~/.benchsdk/current-instances.json`, keyed by git root + org). `create` sets the pick (`--no-use` skips), `use <id>` sets it by hand, `use --clear` and `destroy` clear it, and a stale pick (404) clears itself. **Agents: pass the ID explicitly or `export COMPUTE_INSTANCE=<id>` — don't rely on the per-directory pick, which a human may have set for a different task.**

## Sizes and market pricing

- **Platform sizes** are the normal way to say how big a box should be: `small` = 1 vCPU / 2 GB, `medium` = 2 / 4 GB (the default — a size-less, resources-less create lands on medium), `large` = 4 / 8 GB, `xlarge` = 8 / 16 GB. Raw `--cpus`/`--memory-mb`/`--disk-mb` stay for advanced use and can't be combined with `--size`. On a market fill, `get`/`quote` report the requested `size` plus the seller's `box` (provider, the ask's `sizeName`, resources) in `placement`.
- **Quote before you buy:** `compute sandboxes quote` is a dry-run of the create — it prints the provider and box, order type, rate, cheapest live, reference, est. cost/required hold/balance, cap, and protection limit (one item per line), ending `ok` or a reason code. Nothing is created. Every rate the CLI prints shows all three units, per hour first: `$0.1008/hr · $0.00168/min · $0.000028/s`. **When telling a user the price, quote the per-hour number.** Money amounts (balance, est. cost, holds) print as `$1,234.56`. The same all-units format covers `compute market` prices.
- **The default order type is `limit`** — with no market cap configured and no `--max-price`, a create fails `market_cap_required`. The normal flow is quote → create with `--max-price` at the quoted rate. `--market` (or `--order-type market`) is the opt-in for filling at the cheapest live price, bounded by the platform protection ceiling (about 3× the size's reference price).
- **To cap the price**, pass `--max-price <usd>/<unit>` — the unit is required (`second`, `minute`, or `hour`, e.g. `--max-price 0.12/hour`; `--max-price-per <unit>` is an alias for a bare `--max-price` usd). A limit order fills only at or under that price.
- **Error codes:** `market_access_required` (403 — the org isn't approved to buy on the market; request access on the org's market page), `insufficient_credits` (top up first), `limit_not_met` (cheapest live price above your max), `above_protection_limit` (ask prices above the protection ceiling), `no_market_capacity` (no live ask covers the request).

## Pitfalls

- **~290s ceiling:** `exec` buffers output and tops out around 290 seconds. Anything longer — servers, builds, watchers — goes through `spawn` + `logs -f` or `wait`.
- **Preview URLs:** the server must listen on `0.0.0.0` on the exact `--port`, or the preview 502s. Flask: `app.run(host="0.0.0.0", port=N)`. Vite: `vite --host 0.0.0.0 --port N --strictPort` plus `server.allowedHosts` covering the preview host (e.g. `.bl.run`). Next.js: `next dev -H 0.0.0.0 -p N`.
- **Tensorlake:** `url` makes every exposed port on that sandbox public, not just the one you asked for.
- **`--secret`** names an org-vault secret injected into the sandbox environment (repeatable); manage vault items with `compute actions vault` (see the `compute-actions-cli` skill).
- **Provider order** walks entries 1,2,3… — `market` bids on the compute market first; each refusal is recorded in `placementAttempts`. Snapshots are BYOK-only (market-filled boxes refuse them).
- Destroy is verified — it settles billing only once the provider confirms the box is gone; a 502 means retry.

## REST equivalent

For scripts that skip the CLI: the `@computesdk/platform` provider gives hosted sandboxes the same `compute.sandbox` interface in code (`platform({ apiKey: process.env.COMPUTE_API_KEY })` — no raw fetch needed; see the `computesdk` skill's "Hosted platform" section). Raw REST: `POST https://platform.computesdk.com/api/v1/sandboxes` with `Authorization: Bearer $COMPUTE_API_KEY` returns `{ sandbox: { id, … } }`. File writes are `POST /api/v1/sandboxes/{id}/files` with `{ path, content }`.

```
POST   /api/v1/sandboxes        { label?, providerOrder?, image?, snapshotId?,
                                size?: small|medium|large|xlarge,
                                resources?: {cpus,memoryMb,ephemeralDiskMb},
                                orderType?: market|limit, maxPrice?: {usd,per},
                                timeoutMs?, secrets?: [vaultNames] }
GET    /api/v1/sandboxes/quote?size|resources&region&timeoutMs&orderType&maxPriceUsd&maxPricePer
GET    /api/v1/sandboxes?status=&limit=&cursor=
GET    /api/v1/sandboxes/{id}   → sandbox + attach
DELETE /api/v1/sandboxes/{id}   → settles cost
GET    /api/v1/sandboxes/costs  → { running, settled, totalUsd, byProvider }
```

### Provider order

Each create walks a provider order — `provider` or `provider:region` entries — recording every refusal in `placementAttempts`. The special entry `market` bids on the compute market's open asks before the walk continues. Resolution order: per-request `providerOrder` (the CLI's `--order`) → the org's own sandbox order → the Actions provider order → the deployment default (`["vercel"]`).

### Settings, rates, warm pool

```
GET/PATCH /api/v1/sandboxes/settings   { providerOrder?, marketCap?, marketCaps?, marketOrderType?, providerResources?, warmPool? }
GET/PUT/DELETE /api/v1/sandboxes/rates { provider, rate, per: second|minute|hour }  (org overrides)
GET/POST  /api/v1/sandboxes/pool/fill  report floors + inventory; trigger an ensure now
```

Read them with `compute sandboxes settings` (prints the resolved view incl. the Actions values the lane inherits) and write them with `compute sandboxes settings set` — owner/admin only; a non-admin credential gets "Only org owners/admins can change sandbox settings". `set` takes `--order market,blaxel` (`--order inherit` restores the Actions order), `--order-type limit|market|inherit`, `--general-cap <usd>/<unit>|none`, and repeatable `--cap <size>=<usd>/<unit>` (`=none` clears that size's cap). Units are required, same parser as `--max-price`.

- `providerOrder` — the org's sandbox order; an empty list inherits the Actions order.
- `marketCap` — max $/vCPU-time for `market` order entries (required when the order uses `market`).
- `marketCaps` — per-platform-size caps (`small`/`medium`/`large`/`xlarge`); a size cap overrides `marketCap` for that size.
- `marketOrderType` — `limit` or `market`; `null` inherits the Actions lane's order type.
- `providerResources` — per-provider default sizes.
- `warmPool` — `provider[:region] → count` floor of pre-warmed boxes a plain create claims instead of cold-placing. Creates carrying `image`/`snapshotId`/`resources`/`secrets` skip the pool; labels under `sb-pool` are reserved.
- Cost model: a per-provider rate (org override → platform default) is snapshotted onto the sandbox at placement and applied to wall-clock lifetime; every sandbox carries `cost: { rate, runtimeSeconds, costUsd, settled }`.

### The `attach` descriptor

`POST`/`GET` return `sandbox.attach: { provider, providerSandboxId, region } | null` — with your own provider key (BYOK) you can drive the box directly via the provider's SDK (`connect()` with the id + region) instead of proxying through the platform. `attach` is `null` on market fills (the seller's credential is never handed out), ambient providers, and non-running boxes. Direct attach bypasses command audit and vault `secrets` env injection.
