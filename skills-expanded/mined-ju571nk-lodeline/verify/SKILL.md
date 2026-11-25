---
name: verify
description: Drive the real lodeline-manager release binary and its embedded web console in a real browser with MOCK_FLEET=1, and capture screenshots, Playwright traces, and curl bodies. Use to prove a change to login, the alerts queue, triage, the fleet pages, host detail, the proxy and invocation pages, the Downloads page, the Enroll a host page, settings, or the /api/v1 responses on the real binary, or to reproduce a console bug.
---

# Verify lodeline-manager

The primary surface is the web console, driven by the Playwright specs in `web/tests/e2e` in Chromium against the release binary with its embedded SPA. The secondary surface is the HTTP API, driven by curl with a real login. Each run gets its own free port, SQLite file, session state, and scratch directory through `drive.sh`.

Paths below are relative to `apps/manager`. Read [`features/README.md`](features/README.md), then the matching feature file. A proof covers every entry point the feature file lists, or names the ones it skipped.

## Hard rules

- Start the server only through `drive.sh new`. A direct `lodeline-manager` reads your shell's environment, and `./var/triage.sqlite` is its default database.
- Do not use a bare `npm run e2e` as a proof. Outside CI it attaches to anything that answers on port 18181. `drive.sh e2e` runs the same specs on this run's instance.
- Never set `LODELINE_SERVER_BASE_URL`, `LODELINE_SERVER_READ_TOKEN`, `TRUSTED_PROXIES`, or `OIDC_*` for a run, and never remove `MOCK_FLEET=1`. Never connect a run to a real `lodeline-server`, a real config, or a shared instance.
- Use only the test credentials, `admin` and `test-password`. They come from the public fixture in `web/playwright.config.ts`. `drive.sh` generates `JWT_SECRET` for each run and writes it nowhere. Do not read `.env` or any private key or notes file outside this folder.
- Kill only what the run started. `drive.sh cleanup` does that by recorded pid and start time. Never use `pkill`, `killall`, or a kill by process name.
- Commit no evidence, no binary, and no account IDs, keys, credentials, or personal paths. Stage files by path.

## Launch

From `apps/manager`:

```sh
RUN=$(.claude/skills/verify/drive.sh new)
```

This runs `npm ci` if `web/node_modules` is missing, then `npm run build` in `web/` and `LODELINE_MANAGER_REQUIRE_DIST=1 cargo build --release --locked`. The binary lands in `${CARGO_TARGET_DIR:-target}/release/`, so set `CARGO_TARGET_DIR` in the calling shell to use another target dir. `drive.sh` starts the binary on `127.0.0.1` with an empty environment plus the variables below, and prints the run id on stdout. The instance is ready when the id prints and Doctor passes. The binary creates the SQLite schema before it listens, so a healthy `/api/health` means that the database is usable. No seed step exists: the mock fleet loads in process, and the triage tables start empty.

| Variable | Value | Why |
|---|---|---|
| `LISTEN_ADDR` | `127.0.0.1:<free port>` | Loopback only, a port per run. |
| `MOCK_FLEET` | `1` | The built-in mock fleet; no upstream. |
| `TRIAGE_DB_PATH` | `<scratch>/triage.sqlite` | A fresh database per run. |
| `ADMIN_USERNAME`, `ADMIN_PASSWORD_BCRYPT` | `admin`, the hash from `web/playwright.config.ts` | The test login. |
| `JWT_SECRET` | 32 random bytes, hex | Sessions die with the run. |
| `LODELINE_INSECURE_COOKIE` | `1` | Plain HTTP, so the cookie must drop `Secure` or the browser never sends it back. |

`TRUSTED_PROXIES` stays unset: the browser and curl connect directly, so the limiter keys on `127.0.0.1`.

It needs `cargo`, a C compiler, `node`, `npm`, `curl`, `jq`, `lsof`, `sqlite3`, and `openssl`. If Doctor reports that Chromium is missing, run `npx playwright install chromium` in `web/`.

The shell does not keep `RUN` between tool calls, so pass the id literally in each later call. Runs can overlap once they have started. Start them one at a time from a single checkout, because the build writes `web/dist` and the target dir.

## Doctor

```sh
.claude/skills/verify/drive.sh doctor "$RUN"
```

Read-only, apart from one login. It exits 0 when the recorded pid is alive and holds the port, `/api/health` reports the version in `Cargo.toml`, the server log shows `mode=mock-fleet` and a database in scratch, no source changed since the build, a test login resolves to `admin`, and Chromium is installed. After a `[FAIL]` about changed source, clean up and start a new run. Run Doctor first whenever anything looks off.

## Drive

```sh
.claude/skills/verify/drive.sh e2e "$RUN" <label> [playwright args...]
.claude/skills/verify/drive.sh api "$RUN" <label> <METHOD> <path> [json-body]
.claude/skills/verify/drive.sh db "$RUN" <label> <sql>
```

- `e2e` runs `web/tests/e2e` through `playwright.verify.config.mts`, which keeps the repo's settings, turns on traces and screenshots for every test, and removes `webServer`. A dead instance fails the run instead of starting a second server. The `setup` project signs in once and saves the session to `<scratch>/auth.json`, which every test starts with. Pass a spec path and `-g <pattern>` to narrow it. `drive.sh e2e "$RUN" all` runs every spec.
- `api` sends one request with a per-run cookie jar. Log in through `POST /api/v1/auth/login` first. Only `/api/health`, `/api/v1/auth/login`, `/api/v1/auth/methods`, and the OIDC routes work without the cookie. A non-2xx status is a valid capture and exits 0.
- `db` runs read-only SQL on the run's SQLite file through `sqlite3 -readonly`. Tables are `triage`, `triage_notes`, and `triage_log`.
- A label is single-use, so evidence is never overwritten.

To drive behavior that no spec covers, add a test to the matching spec in `web/tests/e2e`. Prefer `getByRole` and `getByLabel`, the handles those specs already use.

### The login limit

Login allows 10 attempts a minute per client address, success or not, and loopback is not exempt. Everything in a run connects from `127.0.0.1`, so Doctor, the e2e `setup` project, the login specs, and `drive.sh api ... /api/v1/auth/login` all share one window. `drive.sh e2e "$RUN" all` makes 5 logins. A run that adds Doctor and a few API logins in the same minute reaches the limit, and the next login gets `429` with `Retry-After`. That is the limiter working, not a failed journey: wait the `Retry-After` seconds and continue. A spec that fails on a `429` is not evidence either way. Rerun it after the window resets, or start a new run.

### Which specs reach the binary

A passing spec proves a server response only if the spec did not replace that response with `page.route`.

| Spec | Reaches the binary for |
|---|---|
| `alerts.spec.ts` | Everything. No stubs. |
| `login.spec.ts` | Everything. No stubs. |
| `fleet.spec.ts` | Everything, except the second half of `observed controls survive...`, which stubs one host read. |
| `oidc.spec.ts` | Only `unconfigured provider leaves local login available`. |
| `investigation.spec.ts` | Only the first step of `Settings labels stale...`. Every other test stubs the endpoint it asserts on. |
| `devices.spec.ts` | Login only. The hosts endpoint is stubbed for the whole test. |
| `proxies.spec.ts` | Everything, except `a server without proxy reads is named as such`, which stubs the proxy endpoints. |
| `setup-guides.spec.ts` | Rendering only: every test stubs the answer of the endpoint that makes its off state. |
| `proxy-invocations.spec.ts` | Everything. No stubs. |
| `proxy-inventory.spec.ts` | Everything. No stubs. |
| `downloads.spec.ts` | Everything, except `a server without artifacts_dir is named as such`, which stubs the index. |
| `enroll.spec.ts` | Everything, except `a server that does not accept the mint certificate is named as such`, which stubs the POST, and `a host id the page cannot accept sends no request`, which aborts any POST. |

The stubbed specs prove how the SPA renders a response. Prove the matching server response with `drive.sh api`.

## Evidence

Everything goes to `${TMPDIR:-/tmp}/lodeline-manager-verify/<run>/evidence/`, outside the repo. It survives cleanup and stays until the OS clears `TMPDIR`, so copy it elsewhere if it must last. Doctor prints the path.

| File | Contents |
|---|---|
| `build.txt`, `build.log` | The git SHA, the dirty files under `apps/manager`, the binary path, the port, the `/api/health` body, and the build output. |
| `server.stderr` | The startup mode line and the access log. |
| `<label>/<test>/trace.zip`, `test-finished-1.png` | The trace and the final screenshot of each test, plus any screenshot the spec saves. Open a trace with `npx playwright show-trace <file>` in `web/`. |
| `<label>.cmd`, `.stdout`, `.stderr`, `.exit` | A browser run. |
| `<label>.cmd`, `.status`, `.headers`, `.body` | An API call. `.headers` hides the session cookie value. |
| `<label>.cmd`, `.rows` | A SQL read. |

Evidence holds your local `TMPDIR` path, so quote it in a PR only after you replace that path. `trace.zip` and the screenshots can hold a live session token, so never paste or commit them. The token dies with the run's server, and `<scratch>/auth.json` goes with cleanup.

Proof standards:

- Drive the real user path: the browser against the release binary, or a real login cookie for the API.
- Capture the action and the resulting state. Pair a browser mutation with a second view through `drive.sh db` or `drive.sh api`.
- Report each result as verified, skipped, or failed. A skipped entry point is not verified through another path.
- Name what `MOCK_FLEET=1` replaced. See [What the mock hides](#what-the-mock-hides).

### Capture an API response as a baseline

To record what the API returns, so that a later build can be compared with it, capture from a fresh run. Send anonymous requests before the login, and send reads before any mutation, because the cookie jar and the triage rows change later responses. Each capture holds the method and path in `.cmd`, the status in `.status`, and the body in `.body`. Then blank the volatile fields:

```sh
jq -S 'walk(if type == "object" then with_entries(if (.key | test("(^|_)(ts|at)$|^timestamp$|^event_id$|^next_cursor$")) then .value = "<volatile>" else . end) else . end)' <label>.body
```

Those fields change between runs because the mock anchors its fixtures to the startup time and derives each `event_id` from it. The filter leaves two more differences to handle yourself:

- `version` in `/api/health` is the crate version.
- `Date` and the `Expires` attribute in `.headers` are volatile.

These facts are part of the response, so do not normalize them away:

- `expires_at` has two formats. `/auth/login` returns UTC with fractional seconds. `/auth/me` returns the host's time zone with whole seconds.
- `fleet/hosts` returns `"hostname": null` for the disconnected host.
- Triage timestamps have nine fractional digits.

For a full regression check of every route, run the parity suite instead (`web/tests/parity/README.md`).

## Cleanup

```sh
.claude/skills/verify/drive.sh cleanup "$RUN"
```

Stops this run's server, removes `scratch/`, keeps `evidence/`, and lists what survived. It is safe to run twice. Run it after every failed attempt too.

## What cannot be isolated

- **Build output.** The build writes `web/dist` in the checkout and the release binary in the target dir. Both are ignored by git. A later `drive.sh new` from another checkout state replaces them.
- **The browser cache.** Chromium comes from the shared Playwright cache. Only the server runs with an empty environment. Playwright keeps your shell's environment, without `CI`.
- **The time zone.** The binary uses the host's zone, which shows in `/auth/me`.
- **The port.** A short gap exists between choosing the free port and binding it. Doctor fails if another process holds the port.

## What the mock hides

`MOCK_FLEET=1` replaces the HTTP fleet client with the fixtures in `testdata/mock-fleet.json`, `testdata/mock-proxies.json`, `testdata/mock-proxy-invocations.json`, `testdata/mock-proxy-inventory.json` and four one-line release files (`src/fleet/mock.rs`), and a mock enrollment mint (`src/enroll.rs`), so no run talks to a `lodeline-server`. A green run says nothing about these areas, which stay with `cargo test` (`src/fleet/tests.rs` runs a real `lodeline-server` in process, and `src/fleet/http/tests.rs` covers TLS) and the parity suite's live cases:

- The bearer token, the custom CA, and mTLS to `lodeline-server`.
- Retries and the mapping of upstream failures to `upstream_unauthorized`, `read_api_disabled`, `certificate_refused`, `service_unavailable`, `upstream_error`, for the proxy reads `proxy_reads_unavailable`, `upstream_forbidden`, `invalid_cursor` and `invalid_filter`, and for the release files `artifacts_not_configured`. The browser specs for those states use `page.route`.
- Decoding of real responses, real paging cursors, real filter behavior, and real retention.
- Streaming a large release file, and the 30 s stall limit of a download.
- Fixture accuracy. The fixtures are a copy of the Go console's mock, written against the contract in `docs/specs/fleet-api/contract.md` at the repo root.

The fleet read cache stays in the path. `FLEET_POLL_INTERVAL_SECONDS` (unset here, so 5) is how long a cached read stays fresh, not how often the SPA polls. Past that the cache still answers with the old read, up to 12 times that age, while it refreshes, and fleet metadata and single events stay fresh 12 times longer than other reads. So a read can be older than the SPA's poll interval suggests.

Other settings also differ from production:

- `LODELINE_INSECURE_COOKIE=1` removes the `Secure` cookie flag, and the run uses plain HTTP with no TLS terminator.
- `TRUSTED_PROXIES` is unset and nothing sits in front of the binary, so the reverse-proxy path of the limiter is not driven.
- OIDC is not configured. The `/api/v1/auth/oidc/*` routes are not driven, and `oidc.spec.ts` stubs them.
- No container image or service unit exists for the console yet, so only the bare binary is driven.

Keep the map current with `/maintain-verification-skill`.
