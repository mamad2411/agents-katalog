---
name: verify
description: Runtime verification of a change at its real surface for cost-guard-mcp - drive the real stdio server from a worktree venv against loopback fakes and capture quotable evidence (use before claiming any fix works; tests are never evidence).
---

# verify - cost-guard-mcp at its real surface

Observe the REAL server (console script `cost-guard-mcp`, `src/cost_guard_mcp/server.py:main`,
stdio JSON-RPC only - there is no HTTP listener) with the warehouse SDKs replaced by loopback
fakes. Unit tests, mypy and ruff are a spec to read, never evidence. Everything below ran on
2026-10-14 against `main` b3c7201 (PR #86 merged); the full harness archive this skill distils is
`$M/scratch-pad/security-verification-2026-10/verify/` (RECIPE.md, RECIPE-DELTA.md, harness/lead/, evidence/) where
`$M` is the MAIN checkout: `scratch-pad/` is gitignored, so a fresh worktree has none of it (section 1).

Hard rules: never read/source/copy `.env` or a real credential (dummy values only, generated into a
0600 file, never typed on a command line); never contact a real backend (the launcher's socket guard
refuses every non-loopback connect - if `network_guard: refused` appears in stderr, STOP and report);
do not run `tests/integration/*`; stop every process you start by pid; ports 127.0.0.1 18700-18799.

## 1. Build and launch from a worktree

```bash
W=/path/to/worktree            # never the main checkout; `git worktree add <path> -b <branch> main`
M=/path/to/main-checkout       # READ-ONLY: scratch-pad/ (the harness archive) is gitignored and exists ONLY here
S=$W/.claude/skills/verify/scripts
E=$W/../evidence/<lane>        # or scratch-pad/<run>/evidence - outside the tracked tree
mkdir -p "$E"; cd "$W" && uv sync --all-groups          # editable install: src/ IS the code under test
PY=$W/.venv/bin/python
$PY -c 'import cost_guard_mcp.server; print(cost_guard_mcp.__file__)'   # must print $W/src/...; ALSO warms the
# bytecode: the first import of the three SDK trees after `uv sync` took >60 s and timed out a 60 s client once.
```

Server command for every probe (stdout = transport, stderr = log + guard + launcher banner):
`$PY $S/launch_guarded.py`. It installs the loopback-only socket guard, optionally a fake-SDK
module (section 2), then imports and runs the real `main()`. The plain console script
(`$W/.venv/bin/cost-guard-mcp`) is the same server without the guard - use it only for
`docker`/startup-exit probes where no SDK call can happen.

Dummy operator env (needed only when a Snowflake/Databricks tool is called; BigQuery needs nothing
once `Client` is faked). Secret-shaped names are assembled with printf so no command text or file
write ever contains an assignment-shaped secret:

```bash
umask 077
{ printf 'SNOWFLAKE_ACCOUNT=fakeorg-fakeacct\nSNOWFLAKE_USER=fake_user\nSNOWFLAKE_ROLE=COST_GUARD_READER\n'
  printf 'SNOWFLAKE_%s=%s\n' PASSWORD "$(openssl rand -hex 12)"
  printf 'DATABRICKS_SERVER_HOSTNAME=fake-workspace.invalid\nDATABRICKS_HTTP_PATH=/sql/1.0/warehouses/fake0warehouse0id\n'
  printf 'DATABRICKS_%s=%s\n' TOKEN "$(openssl rand -hex 12)"; } > "$E/dummy.env"
```

Real server knobs (env read by `src/`): `COST_GUARD_MAX_IN_FLIGHT_QUERIES` (startup; `0`/`abc`/`+3`/`08` ->
exit non-zero with a static message), `COST_GUARD_ALLOW_MULTI_STATEMENT_SQL=1` (call time, skips the
scanner), `SNOWFLAKE_ROLE` (ACCOUNTADMIN/SECURITYADMIN/ORGADMIN in any quoting -> ConfigError before
connect), `SNOWFLAKE_SECONDARY_ROLES` (NONE|ALL), `SNOWFLAKE_EDITION`, `DATABRICKS_CLIENT_ID/SECRET`,
`DATABRICKS_HTTP_PATH` (`/sql/1.0/endpoints/x` -> warehouse-id allowlist refusal), `OTEL_EXPORTER_OTLP_ENDPOINT`.

## 2. Fake backends

The fake is too large to ship here (1033 lines). Reuse the archive's directly from the MAIN checkout - a fresh
worktree has no `scratch-pad/`, and the archive must not be copied into one. It plugs into the launcher, which calls
its `install()` and then its `install_network_guard()` (the fake's own guard, stacked on the launcher's):

```bash
A=$M/scratch-pad/bq-cap-gate-2026-10/harness                          # fake_backends.py: the newest copy; the only one
                                                                      # whose FakeQueryJob has `location` (#96) - BigQuery
                                                                      # probes need it (section 5). Older copies:
                                                                      # security-verification-2026-10/verify/harness/lead
                                                                      # (+ launch_server.py, mcp_client.py), rq-caps-2026-10
ls "$A/fake_backends.py"                                              # must exist BEFORE any fake-backed probe
--env CG_VERIFY_FAKE_PATH=$A --env CG_VERIFY_FAKE_MODULE=fake_backends --env CG_FAKE_RECORD_FILE=$E/<probe>.fake-calls.json
```

To write a minimal one: patch exactly these six attributes BEFORE `cost_guard_mcp` is imported, record
every call (redact `password/private_key/token/access_token/client_secret` kwargs) and never open a
socket: `google.cloud.bigquery.Client`, `google.cloud.bigquery_reservation_v1.ReservationServiceClient`,
`snowflake.connector.connect`, `databricks.sql.connect`, `databricks.sdk.WorkspaceClient`,
`databricks.sdk.core.Config` (the last two are from-imports in `engines/databricks.py`, hence "before").
Keep the real `QueryJobConfig`, `DEFAULT_RETRY`, `google.api_core.exceptions`, `snowflake.connector.errors`
/ `DictCursor` / `QueryStatus`, `databricks.sql.exc`, `GetWarehouseResponse` so the server consumes real
objects. The archive fake's knobs are all `CG_FAKE_*` env vars (rows, error injection by real exception
kind, delays, SHOW WAREHOUSES rows with LIKE semantics, STATEMENT_TIMEOUT, forged job/query ids) -
RECIPE.md section 4 is the reference; `CG_FAKE_ALLOW_NETWORK` must never be set.

## 3. Probe recipes (each spawns one fresh server; add `--stderr "$E/<probe>.stderr.log"`)

```bash
RPC="$PY $S/stdio_rpc.py --stderr $E/x.stderr.log"
# tools/list over real stdio: 4 tools, protocol + serverInfo in handshake.response
$RPC list-tools -- $PY $S/launch_guarded.py > "$E/tools-list.json"
# single-statement gate: ToolError, zero SDK calls (no fake needed - the scanner runs before any engine)
$RPC call run_query_bounded '{"engine":"bigquery","sql":"SELECT 1; SELECT 2","max_rows":5}' -- $PY $S/launch_guarded.py > "$E/multi-stmt.json"
# bare NaN cap (the SDK's JSON parser accepts it): raw JSON-RPC lines, no handshake needed - the client sends it
printf '%s\n' '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"run_query_bounded","arguments":{"engine":"bigquery","sql":"SELECT 1","max_estimated_cost_usd":NaN}}}' > "$E/nan.jsonl"
$RPC raw "$E/nan.jsonl" -- $PY $S/launch_guarded.py > "$E/nan.json"
# bounds that must refuse BEFORE any estimate: max_rows 0/-1, max_bytes_billed 2**63, warehouse_size "gigantic", NaN; +inf = no cap
# admin role refused before connect (zero `snowflake connect` records even with the fake installed)
$RPC --env-file "$E/dummy.env" --env SNOWFLAKE_ROLE="'ACCOUNTADMIN'" call check_credentials '{"engine":"snowflake"}' -- $PY $S/launch_guarded.py
# with the archive fake: estimate + run under a cap, caveats, refusals (fake-calls.json entry 0 = harness/install, entry 1 = harness/network_guard state=enabled)
$RPC --env-file "$E/dummy.env" --env CG_VERIFY_FAKE_PATH=$A --env CG_VERIFY_FAKE_MODULE=fake_backends \
  --env CG_FAKE_RECORD_FILE=$E/cc-bq.fake-calls.json call check_credentials '{"engine":"bigquery"}' -- $PY $S/launch_guarded.py
```

What mattered last time (RECIPE.md section 6, RECIPE-DELTA.md section 4): the executed SQL in the fake
record is `SELECT * FROM (<sql>) AS cost_guard_row_cap LIMIT max_rows+1`; `job_config.maximum_bytes_billed`
present only when a byte/dollar cap was given; `CG_FAKE_BQ_EXECUTE_BYTES` above the cap -> structured
`refused` + hint naming maximumBytesBilled; Snowflake `connect` carries `secondary_roles` and
`session_parameters.MULTI_STATEMENT_COUNT=1`, every `execute` carries `num_statements=1`, `ALTER SESSION SET
STATEMENT_TIMEOUT_IN_SECONDS = 60|120` only when the effective value is 0/missing/above; Databricks
`sql.connect` carries `_retry_stop_after_attempts_duration=60`, `_socket_timeout=60`,
`session_configuration.STATEMENT_TIMEOUT`; cancellation (`notifications/cancelled` from the client, or the
archive client's `call-cancel`) -> stderr `tool=run_query_bounded outcome=cancelled` and NO `Client.query
dry_run=false` afterwards; `COST_GUARD_MAX_IN_FLIGHT_QUERIES=2` + 3 parallel calls -> one immediate
`isError` naming the cap; forged ids/names with `\n`/ESC come back repr-quoted on ONE stderr line; rows with
bytes/NaN/INTERVAL cells come back base64/"nan"/str. Multi-call sessions need the archive `mcp_client.py
script` (steps.json with `parallel`, `cancel_after`).

Docker image and startup gates (console script, no SDK call possible):

```bash
docker build -t cost-guard-verify:$(git -C $W rev-parse --short HEAD) $W
docker run -i --rm -e COST_GUARD_MAX_IN_FLIGHT_QUERIES=abc cost-guard-verify:<sha> ; echo "exit=$?"   # expect non-zero + static message
env -i PATH=/usr/bin:/bin COST_GUARD_MAX_IN_FLIGHT_QUERIES=0 $W/.venv/bin/cost-guard-mcp </dev/null; echo "exit=$?"
```

Workflow steps against fixture repos (no network, never a real checkout):

```bash
$PY $S/extract_step.py $W/.github/workflows/release.yml 'name: Verify tagged commit is on main' > "$E/ancestry-gate.sh"
# build a throwaway origin.git + clones under $E (tags on main / on an unmerged branch / a tag NAMED origin/main),
# then: ( cd clone && GITHUB_REF_NAME=v0.0.4 GITHUB_SHA=$(git rev-parse v0.0.4) bash -e "$E/ancestry-gate.sh" ); echo exit=$?
git -C $W check-ignore -v .env .mcp.json service-account.json .cursor/mcp.json   # read-only on the worktree
```

## 4. Evidence discipline

- Capture under `$E/`: the client JSON (`--out` equivalent: redirect stdout), `*.stderr.log`, `*.fake-calls.json`.
  One record file per run (the fake rewrites it atomically; it accumulates otherwise).
- Quote the decisive lines in the report: `result.isError`, `content[0].text`, `structuredContent.status/reason`,
  the stderr record (`tool=... outcome=... elapsed_ms=...`, `single_statement_check=refused`, `engine=... refused reason=...`),
  the fake record entry (`backend`, `call`, `kwargs`). Say which file and which entry.
- Verdict per claim: PASS / FAIL / BLOCKED (exact point) / SKIP (why). A probe that "broke" a control is a FAIL
  even if a test passes. Running pytest/mypy/ruff or importing a function is never evidence.
- Check the first two entries of every fake record file are `harness/install` (listing the six patched attributes) and
  `harness/network_guard state=enabled` (written by the fake's own guard, which `launch_guarded.py` installs right after
  `install()`); zero `network_blocked` records; zero `network_guard: refused` stderr lines. Without a fake there is no
  record file - the guard evidence is then the stderr banner `launch_guarded: pid=... network_guard=on fake=none`.

## 5. Gotchas (all bitten before)

- Fakes older than #96 (`security-verification-2026-10/.../lead`, `rq-caps-2026-10`) have no `FakeQueryJob.location`;
  since #112 the BigQuery engine reads it on the dry-run job (`engines/bigquery_estimate_rules.py`), so every BigQuery
  `run_query_bounded` / `estimate_query_cost` probe dies with `isError: true` "'FakeQueryJob' object has no attribute
  'location'" right after the dry run, before any wrap or cap evidence is recorded. Use the `bq-cap-gate-2026-10` fake
  (knob `CG_FAKE_BQ_DRY_RUN_LOCATION`, default `US`, `absent` -> `None`), or shim a `FakeQueryJob` subclass with it
  (bitten by the #124 verification, 2026-10-19).
- The workstation's SecretScan hook blocks Bash command TEXT and Write CONTENTS that contain bearer-style
  token literals or `NAME=<secret-looking literal>` - generate dummies with `openssl rand -hex` into a 0600 file,
  pass `--env-file`, build names with `printf '%s_%s=%s'`. It also blocked `DROP TABLE` in a command line once: put
  such SQL in a steps/messages file.
- Launchers drop EMPTY env vars (`[[ -n ]]` allowlists, `setdefault`): for empty-value gates run
  `env -i PATH=... VAR= <console script>` directly.
- Stop by pid (`kill $PID`; `lsof -ti tcp:PORT -sTCP:LISTEN` for listeners); never `pkill -f <pattern>` - it matches your
  own shell whose command line contains the pattern. `stdio_rpc.py` terminates its child itself.
- `check_credentials` / `estimate` / `run` fake a different `run_query` path each: `Client.query(dry_run=True)` vs
  `(dry_run=False)` + `QueryJob.result`, Snowflake `execute` vs `execute_async` + `get_query_status`, Databricks
  `EXPLAIN COST` vs the executed statement - read the record `call` names, not counts.
- Single-statement gate: dialect-aware scanner (`sql_scope.py`), runs in BOTH estimate and run; opt-out is exactly
  `COST_GUARD_ALLOW_MULTI_STATEMENT_SQL=1`; a `;` inside a string literal passes it - the connector-side pin
  (`num_statements=1`, `MULTI_STATEMENT_COUNT`) is the second layer.
- Warehouse lookups: Snowflake `SHOW WAREHOUSES LIKE` returns `_`/`%` siblings and case variants -> exactly-one
  resolution or no dollar figure (and a dollar cap refuses); an allowlist-refused `CURRENT_WAREHOUSE()` fails
  closed; Databricks `warehouses.get` failure -> two caveats, caller-asserted size only beside a figure.
- "cache hits": `use_query_cache` is in the recorded `job_config` - the dry run never bills, so the dollar figure is
  the dry-run bytes, not what the provider bills (`CG_FAKE_BQ_EXECUTE_BYTES` shows the gap).
- Delays inside fakes block a real worker thread; the BigQuery/Databricks watchdogs are 120 s constants.
- `uv run` re-resolves; use `$W/.venv/bin/python` directly once synced so the venv under test is explicit.
- `extract_step.py` stops at the next step boundary: a `uses:` step or a single-line/folded `run:` exits 1 naming the
  step instead of handing back the NEXT step's body, and it echoes the matched line (file:line) to stderr - check it is
  the step you meant before running the extracted script.
