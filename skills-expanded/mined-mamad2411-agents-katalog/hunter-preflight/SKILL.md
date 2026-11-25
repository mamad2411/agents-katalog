---
name: hunter-preflight
description: >-
  Environment readiness gate. Run this before recon on every hunt, and re-run
  it mid-hunt when a probe fails in a way that implicates the environment. A
  broken target environment is the largest false-positive class in Hunter: a
  502 from an unstarted service, a missing migration, or an absent env var
  manufactures deviations that do not exist in the system under intent. This
  skill detects the target platform (web / api / cli / full-stack / mobile),
  runs a platform-specific check matrix, and emits either a go signal or the
  terminal outcome environment_unready. Load when starting a hunt, before
  building the surface map, when a hunt has run long enough for the environment
  to drift, or whenever downstream results look like environment artifacts
  (mass 5xx, connection refused, template errors, empty pages).
allowed-tools: Bash, Read, Grep, Glob
---

# Hunter Preflight

Assumes `hunter-doctrine` is loaded. This is a gate: it runs and either clears
the hunt to proceed or halts it. It does not probe for deviations. It proves the
quarry is in a state where a probed deviation would be a real deviation.

## Why this gate exists

Every downstream Find is conditioned on the environment being the system under
intent. If postgres is unreachable, every route that reads the database returns
500, and a naive hunt promotes 40 Signs to 40 Finds that vanish the moment the
database comes up. Those are not Finds. They are artifacts of a broken
environment, and shipping them destroys the one thing Hunter sells: that its
output can be trusted without re-checking.

Corollary from the doctrine: **you may not report absence as cleanliness, and
you may not report an environment artifact as a deviation.** A failed preflight
means the hunt has no valid denominator yet, so no verdict is possible.

## The gate contract

- A hunt MUST NOT proceed past a failed preflight. If any check with
  severity `blocking` fails, emit `environment_unready` and stop. Recon does not
  run. Probes do not run. No Signs, no Finds, no verdict.
- Preflight emits a machine-readable record to `preflight.json` in the run
  directory. Recon reads it and refuses to start if `outcome` is not `ready`.
- Preflight NEVER reads, logs, echoes, prints, or writes a secret VALUE.
  It checks that a required variable is *present and non-empty* by name only.
  Reading a secret value into a log poisons the artifact and is unrecoverable.

## Step 1 — detect the platform

Detect all that apply; a repo can be more than one (full-stack = web + api).

```bash
# platform detection — emit flags, do not guess
WEB=0; API=0; CLI=0; MOBILE=0
# web: a rendered UI surface
[ -n "$(find . -maxdepth 4 \( -name '*.tsx' -o -name '*.jsx' -o -name 'next.config*' \
  -o -name 'vite.config*' -o -name 'svelte.config*' -o -name 'angular.json' \) 2>/dev/null | head -1)" ] && WEB=1
# api: server-side routes/handlers/schema
[ -n "$(find . -maxdepth 4 \( -name 'openapi*.y*ml' -o -name 'openapi*.json' \
  -o -path '*routes*' -o -path '*controllers*' -o -path '*handlers*' \) 2>/dev/null | head -1)" ] && API=1
# cli: a declared binary entrypoint
{ [ -f package.json ] && grep -q '"bin"' package.json; } 2>/dev/null && CLI=1
grep -rqs '\[\[bin\]\]\|^\[project.scripts\]\|console_scripts' Cargo.toml pyproject.toml setup.py 2>/dev/null && CLI=1
# mobile: native project
[ -n "$(find . -maxdepth 4 \( -name '*.xcodeproj' -o -name 'AndroidManifest.xml' \
  -o -name 'pubspec.yaml' \) 2>/dev/null | head -1)" ] && MOBILE=1
echo "WEB=$WEB API=$API CLI=$CLI MOBILE=$MOBILE"
```

`full-stack` is `WEB=1 API=1`. Record the detected set in `preflight.json`
under `platforms`. If detection returns nothing, do not assume — emit
`environment_unready` with reason `platform_undetected` and ask via `hunter-ask`.

## Step 2 — run the check matrix

Run the universal checks plus every check for each detected platform. Each check
has an id, an exact command, a pass condition, a severity, and a remediation.

Severity governs the gate: `blocking` failures halt the hunt; `degraded`
failures are recorded and narrow coverage but allow the hunt to proceed with a
stated limitation (this becomes `PASS (LIMITED COVERAGE)` territory downstream).

### Universal (all platforms)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `toolchain` | version command per language, e.g. `node --version`, `python --version`, `go version` | prints a version that satisfies the pin in the manifest (`engines`, `.nvmrc`, `go.mod`, `python_requires`) | blocking | install/switch to the pinned version before hunting |
| `deps_installed` | `[ -d node_modules ]` / `pip check` / `go mod verify` | dependency tree present and consistent | blocking | run the project install command; do not hunt against a half-installed tree |
| `build` | the project build command (`npm run build`, `go build ./...`, `cargo build`) | exit 0 | blocking | fix the build; a target that does not build cannot be probed |
| `disk` | `df -Pk . \| awk 'NR==2{print $4}'` | ≥ 1 GiB free | degraded | free space; artifact capture (screenshots, traces) needs headroom |
| `clock` | `date -u +%Y-%m-%dT%H:%M:%SZ` and compare to a trusted source if reachable | skew < 60s; timezone recorded | degraded | fix clock skew before time-sensitive probes (tokens, TTLs, signatures) |
| `env_vars` | for each name in the required set: `[ -n "${VARNAME:-}" ] && echo present \|\| echo MISSING` | every required name present and non-empty | blocking | set the missing variables. NEVER print the value — name only |

Required env var names come from the project (`.env.example`, `config` schema,
compose file, deployment manifest). List names only in `preflight.json`.

### Web / full-stack (adds)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `web_server_up` | `curl -sf -o /dev/null -w '%{http_code}' http://127.0.0.1:$PORT/` | connects; status < 500 | blocking | start the dev/prod server; connection-refused turns every route dark, not cold |
| `web_health` | `curl -sf http://127.0.0.1:$PORT/health` (or documented health path) | 200 and expected body | blocking | bring the app to healthy before probing |
| `web_renders` | `curl -sf http://127.0.0.1:$PORT/ \| grep -qi '<html'` | root returns real markup, not a stack trace or error page | blocking | a global error page manufactures per-route deviations; fix first |
| `assets` | build output present, e.g. `[ -d dist ] \|\| [ -d .next ]` | present when a production build is expected | degraded | rebuild if probing a production surface |

### API service (adds)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `api_reachable` | `curl -sf -o /dev/null -w '%{http_code}' http://127.0.0.1:$PORT/health` | connects; documented health status | blocking | start the service; unreachable API = all endpoints dark |
| `api_contract` | `test -f openapi.yaml && npx @redocly/cli lint openapi.yaml` | contract file present and parses (when a contract exists) | degraded | conformance mode needs a valid contract; without it that axis is `NOT-COVERED` |
| `deps_services` | ping each declared backing service (redis: `redis-cli ping`; queue/broker health) | each required backing service healthy | blocking if the surface under hunt depends on it, else degraded | start the dependency or scope it out explicitly |

### Database (web / api / full-stack when a DB is declared)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `db_reachable` | `pg_isready -h $DB_HOST -p $DB_PORT` (or engine equivalent) | accepting connections | blocking | start the database; unreachable DB manufactures 5xx across every data route |
| `db_migrations` | the project's migration status command (`migrate status`, `alembic current`, `prisma migrate status`) | no pending migrations; schema at head | blocking | apply migrations; a schema-behind target produces column/table errors that are not deviations from intent |
| `seed_data` | count rows in a table the hunt requires, e.g. `psql -tAc 'select count(*) from users'` | required fixture rows present (> 0 where the hunt needs data) | degraded | load seed/fixture data; empty tables turn data-dependent surfaces dark, not cold |

Do not embed credentials in these commands. Use the environment the project
already provides. Never echo a connection string that contains a password.

### CLI (adds)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `cli_binary` | run the built binary with `--version` or `--help` | exit 0 and prints expected identity | blocking | build/install the binary; do not probe a stale or absent build |
| `cli_path` | `command -v <tool>` | resolves to the just-built artifact, not a shadowing system copy | degraded | ensure the tested binary is the one on PATH |

### Mobile (adds)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `mobile_sim` | `xcrun simctl list devices booted` / `adb devices` | a booted simulator/emulator or connected device is present | blocking | boot a target device; no device = the surface is dark |
| `mobile_toolchain` | `xcodebuild -version` / `./gradlew --version` | prints a version satisfying the project pin | blocking | install/select the pinned mobile toolchain |
| `mobile_backend` | `curl -sf $BACKEND_HEALTH_URL` | backend the app talks to is healthy | blocking if the flow under hunt calls it | start the backend or scope the flow out |

### Port availability (all networked platforms)

| id | command | pass condition | severity | remediation |
|---|---|---|---|---|
| `port_bound` | `ss -ltn \| grep -q ":$PORT "` (or `lsof -iTCP:$PORT -sTCP:LISTEN`) | the expected process owns the port | blocking | if nothing listens, start the service; if the wrong process listens, you are probing the wrong target — stop |

## Step 3 — emit the record

Write `preflight.json`. This is the contract recon reads.

```json
{
  "hunt_id": "hunt/2026-08-07T14-02Z",
  "checked_at": "2026-08-07T14:02:11Z",
  "timezone": "UTC",
  "platforms": ["web", "api"],
  "outcome": "ready",
  "checks": [
    {
      "id": "db_reachable",
      "command": "pg_isready -h 127.0.0.1 -p 5432",
      "severity": "blocking",
      "status": "pass",
      "observed": "127.0.0.1:5432 - accepting connections",
      "artifact": "preflight/db_reachable.txt"
    },
    {
      "id": "env_vars",
      "command": "presence check by name",
      "severity": "blocking",
      "status": "pass",
      "observed": "present: DATABASE_URL, SESSION_SECRET, STRIPE_KEY (names only)",
      "artifact": "preflight/env_vars.txt"
    }
  ],
  "degraded": [],
  "blocking_failures": []
}
```

`outcome` is one of:

- `ready` — every blocking check passed. Recon may start.
- `ready_degraded` — every blocking check passed; one or more `degraded`
  checks failed. Recon may start; the failed checks are carried forward as
  stated coverage limitations and feed a `PASS (LIMITED COVERAGE)` ceiling.
- `environment_unready` — at least one blocking check failed. **Terminal.**

## The terminal outcome: environment_unready

When any blocking check fails, emit:

```json
{
  "hunt_id": "hunt/2026-08-07T14-02Z",
  "checked_at": "2026-08-07T14:02:11Z",
  "outcome": "environment_unready",
  "reason_code": "db_unreachable",
  "blocking_failures": [
    {
      "id": "db_reachable",
      "command": "pg_isready -h 127.0.0.1 -p 5432",
      "observed": "127.0.0.1:5432 - no response",
      "remediation": "start postgres, then re-run hunter-preflight",
      "artifact": "preflight/db_reachable.txt"
    }
  ]
}
```

Reason codes (extend as needed, keep them greppable and specific):
`platform_undetected`, `toolchain_missing`, `toolchain_version_mismatch`,
`deps_missing`, `build_failed`, `env_var_missing`, `web_server_down`,
`web_unhealthy`, `api_unreachable`, `db_unreachable`, `migrations_pending`,
`dependency_service_down`, `port_unbound`, `port_wrong_owner`,
`cli_binary_missing`, `mobile_no_device`, `disk_exhausted`.

Human line, per the brand voice (declarative, no hedging, denominator present):

```
preflight failed: postgres unreachable at 127.0.0.1:5432 — hunt not started (0/0 surfaces probed)
```

Exit code `2` per the CLI contract: "could not look for bugs", never conflated
with `1` "finds present".

## Re-check policy for long hunts

Environments drift mid-run: services crash, tokens expire, disks fill, seed data
mutates. A hunt that passed preflight at T0 is not guaranteed valid at T+40m.

Re-run preflight (a `blocking`-only fast subset is acceptable) when any of:

- A wall-clock interval elapses (default: every 15 minutes of active probing).
- A batch of ≥ 5 consecutive probes all fail at the transport layer
  (connection refused, 5xx, timeout) — this is the signature of environment
  collapse, not a wall of real deviations.
- Any probe observes a symptom on the preflight failure list (template/error
  page markup, "connection refused", "relation does not exist").

On a mid-hunt re-check failure: **freeze promotion.** Do not promote any Sign
observed after the last known-good preflight, because you can no longer
attribute the observation to the system under intent rather than to drift.
Record `environment_drift` with the last-good timestamp, quarantine Signs in the
drift window, and require re-observation against a restored environment before
those Signs may be promoted. Signs observed before the last good preflight are
unaffected.

## Hand-off

- On `ready` / `ready_degraded`: recon (`hunter-recon`) reads `preflight.json`,
  inherits the `platforms` set and any `degraded` limitations, and builds the
  surface map. The degraded set is the seed of the dark/limited-coverage list.
- On `environment_unready`: the hunt halts. No other skill runs. The report, if
  one is produced at all, states `environment_unready` with the reason code and
  the offending check — it never renders a verdict from the §6 closed set,
  because no surface was validly probed.

## Self-check before clearing the gate

- [ ] Platform set detected and recorded, not assumed
- [ ] Every blocking check ran and its observed output was captured to an artifact
- [ ] No secret VALUE was read, logged, or written — presence checked by name only
- [ ] `outcome` reflects the actual worst blocking result, not optimism
- [ ] On failure, a specific `reason_code` and remediation are attached
- [ ] Re-check triggers are armed for the expected hunt duration
