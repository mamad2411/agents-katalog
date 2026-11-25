---
name: verify
description: Runtime verification of a change at its real surface for tracehub-mcp - start the real console script from a worktree venv (stdio and streamable HTTP), probe it with raw sockets and JSON-RPC against loopback fakes, capture quotable evidence (use before claiming any fix works; tests are never evidence).
---

# verify - tracehub-mcp at its real surface

Observe the REAL server (`tracehub-mcp` console script, `opentelemetry_mcp.server:main`) over its real
transports - stdio JSON-RPC and streamable HTTP (`/mcp`, `/health`, `/ready`) - plus `doctor`,
`--print-config`, the Docker image and extracted workflow steps. Unit tests, mypy and ruff are a spec to
read, never evidence. The full harness archive this skill distils is
`$M/scratch-pad/security-verification-2026-10/verify/` (RECIPE.md, RECIPE-DELTA.md, harness/<pass>-<lane>/, evidence/)
where `$M` is the MAIN checkout: `scratch-pad/` is gitignored, so a fresh worktree has none of it (section 1).

Which head matters: `main` 89659c7 predates PR #41 - no bearer gate, no Host/Origin validation, `--host`
defaults to 0.0.0.0, credentialed URLs accepted. Every "expect" below marked **#41** holds from that PR
on; before it the same probe records the baseline (200 / no refusal). Say which head you verified.

Hard rules: never read/source/copy `.env` or a real credential (dummy 48-hex tokens generated into a 0600
file, never typed on a command line); bind 127.0.0.1 only, ports 18700-18799, check free first
(`lsof -ti tcp:PORT -sTCP:LISTEN`); no live integration tests; stop every process by pid.

## 1. Build and launch from a worktree

```bash
W=/path/to/worktree          # never the main checkout; `git worktree add <path> -b <branch> main`
M=/path/to/main-checkout     # READ-ONLY: scratch-pad/ (the harness archive) is gitignored and exists ONLY here
S=$W/.claude/skills/verify/scripts; E=$W/../evidence/<lane>; mkdir -p "$E"
cd "$W" && uv sync --all-groups; PY=$W/.venv/bin/python; BIN=$W/.venv/bin/tracehub-mcp
$PY -c 'import opentelemetry_mcp; print(opentelemetry_mcp.__file__)'   # must print $W/src/...
umask 077; printf 'MCP_HTTP_%s=%s\n' BEARER_TOKEN "$(openssl rand -hex 24)" > "$E/token.env"
set -a; . "$E/token.env"; set +a                                        # token now in the shell env only
```

`$S/run_server.sh` runs the worktree's console script under `env -i` with an allowlist so nothing else from your
shell reaches it: every set, non-empty shell variable named `BACKEND_*`, `SECONDARY_BACKEND_*`, `MCP_*`, `RATE_LIMIT_*`,
`QUERY_CACHE_*` or `FASTMCP_*` (by prefix - `src/` reads BACKEND_/SECONDARY_BACKEND_ by prefix too, so a knob your PR
adds passes without editing the script) plus the fixed names READINESS_CACHE_SECONDS, MAX_TRACES_PER_QUERY,
FORWARDED_ALLOW_IPS, SLOW_REQUEST_THRESHOLD_MS, SESSION_IDLE_TIMEOUT_SECONDS, SHUTDOWN_DRAIN_SECONDS,
GRACEFUL_SHUTDOWN_TIMEOUT_SECONDS, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_SERVICE_NAME, AWS_ENDPOINT_URL, AWS_ENDPOINT_URL_XRAY,
AWS_DEFAULT_REGION, SSL_CERT_FILE. `OTEL_*` and `AWS_*` are deliberately NOT globbed (OTEL_EXPORTER_OTLP_HEADERS and
AWS_ACCESS_KEY_ID-class names would carry real credentials in). Defaults `BACKEND_TYPE=jaeger
BACKEND_URL=http://127.0.0.1:18710`; extra argv passes through verbatim.

```bash
PORT=18700; lsof -ti tcp:$PORT -sTCP:LISTEN && echo busy
READINESS_CACHE_SECONDS=0 $S/run_server.sh http $PORT --rate-limit-max-requests 0 > "$E/server.log" 2>&1 &
echo $! > "$E/server.pid"; for i in $(seq 40); do curl -s -o /dev/null --max-time 2 http://127.0.0.1:$PORT/health && break; sleep 0.25; done
$S/run_server.sh stdio            # stdin/stdout are the transport - drive it with stdio_rpc.py instead
$S/run_server.sh doctor; $S/run_server.sh print-config
kill "$(cat "$E/server.pid")"     # always; `lsof -ti tcp:$PORT -sTCP:LISTEN` must then print nothing
```

Always start probe servers with `--rate-limit-max-requests 0` unless the probe is about rate limiting:
the default bucket (100 req / 60 s per TCP peer, `/health` and `/ready` included) trips a busy prober.
Flags that matter (**#41**: `--http-bearer-token`/`MCP_HTTP_BEARER_TOKEN` >= 32 printable ASCII,
`--allow-unauthenticated-http`, `--allowed-hosts`, `--forwarded-allow-ips`, `--access-log`,
`--readiness-cache-seconds`, `--session-idle-timeout-seconds`, `--stateless-http`; a bad value exits 2
naming flag and env var): confirm with `$BIN --help` at your head - do not trust this list.

## 2. Fake backends

The archive fake (`$M/scratch-pad/security-verification-2026-10/verify/harness/lead/fake_backend.py`, 736 lines;
the `verify/harness/delta-handle/` copy accepts ports up to 18299 - edit the range check for 187xx) is a Starlette
app with personas jaeger/tempo/sentry/honeycomb, `--tls` (self-signed cert in `verify/harness/lead/tls/`, pass
`SSL_CERT_FILE`), a `--raw-port` plain-TCP responder for lying Content-Length, and a `/_control/*` API (per-path
counts, last requests with headers, override rules: status/retry_after/redirect_location/gzip_bytes/body_bytes/
delay/headers, knobs). Read it from `$M` - a fresh worktree has no `scratch-pad/`; a port-range edit goes to a copy
under `$E`, never into the worktree. Run it with the worktree venv's interpreter (`$PY -I`) so starlette/uvicorn
match the server's.

To write a minimal one: a Starlette app on 127.0.0.1 serving `GET /api/services` ->
`{"data":["checkout","payment"]}`, `GET /api/services/{svc}/operations`, `GET /api/traces?...` and
`GET /api/traces/{id}` -> one static trace, a counter per `"METHOD path"` exposed at `GET /_control/state`,
and a rule hook that can answer any status/Location/Retry-After/delay once. Honeycomb/Sentry/Datadog/NewRelic
refuse `http://` - they need `--tls`. X-Ray (boto3) has no fake. For `/ready` failure classes you need no
fake at all: stopped = `backend unreachable`; a rule `status 503` = `backend error 503`; `delay 12` = `backend timeout`.

## 3. Probe recipes

```bash
B=http://127.0.0.1:$PORT
$S/http_probes.sh $B "$E/http-probes.txt"            # health, ready, unauth/wrong/auth initialize, session reuse, Host, Origin
$PY $S/rawhttp.py $PORT 'GET /health HTTP/1.1' 'Host: evil.example'          # raw socket: 421 #41 (200 before)
$PY $S/rawhttp.py $PORT 'GET /health HTTP/1.1' 'Host: [::1]evil' ; ... 'Host: localhost..' ; ... --no-host   # 421 #41 / 400 from h11
$PY $S/rawhttp.py $PORT 'GET /health HTTP/1.1' 'Origin: http://evil.example'  # 403 already at main (SDK DNS-rebinding guard)
# token placements that must NOT reach the access log (#41: 401, 0 occurrences of the token in server.log,
# with --access-log the line reads "POST /mcp HTTP/1.1" 401 with the query string stripped):
$PY $S/rawhttp.py $PORT --post-json '/mcp?access_token=__TOKEN__' "$INIT"      # also ?token= ?bearer= ?authorization=
$PY $S/rawhttp.py $PORT --post-json '/mcp;access_token=__TOKEN__' "$INIT"      # matrix parameter (rendered %3B)
$PY $S/rawhttp.py $PORT --post-json '/mcp/__TOKEN__' "$INIT"                   # path segment
grep -c -F "$MCP_HTTP_BEARER_TOKEN" "$E/server.log"                            # must print 0
curl -s -i $B/ready    # 200 ready / 503 {"status":"not_ready",...,"error":"backend unreachable|backend timeout|backend error <n>"} (#41; main leaks httpx's "All connection attempts failed")
```

Credentialed URLs must be refused on all four surfaces (**#41**: exit 1, `must not embed credentials`,
URL quoted only as `scheme://[REDACTED]@host`, no username, no 4 consecutive chars of the password, no
`input_value=`). Pre-#41 heads have no refusal: the `http` form below STARTS A REAL SERVER, so it runs under
`timeout` (GNU coreutils; `brew install coreutils` on macOS). Build the URL in a script from a generated password,
never as a literal:

```bash
PW=$(openssl rand -hex 8); CRED_URL="http://verifier:$PW@127.0.0.1:18799/base/path"
for mode in print-config doctor; do BACKEND_URL=$CRED_URL $S/run_server.sh $mode > "$E/cred-$mode.txt" 2>&1; echo "exit=$?" >> "$E/cred-$mode.txt"; done
BACKEND_URL=$CRED_URL timeout 10 $S/run_server.sh http 18701 > "$E/cred-http.txt" 2>&1; echo "exit=$?" >> "$E/cred-http.txt"
# #41: exit=1 within 1 s and nothing ever listened. main: the log shows `Uvicorn running on http://127.0.0.1:18701` and
# timeout kills it after 10 s -> exit=124; then `lsof -ti tcp:18701 -sTCP:LISTEN` must print nothing (kill any pid it prints).
$PY $S/stdio_rpc.py --env BACKEND_TYPE=jaeger --env BACKEND_URL=$CRED_URL --stderr "$E/cred-stdio.stderr.log" list-tools -- $BIN > "$E/cred-stdio.json"
grep -c -F "$PW" "$E"/cred-*                                                   # every count must be 0 (#41); also try SECONDARY_BACKEND_URL and --url
```

stdio, Docker and workflow steps:

```bash
$PY $S/stdio_rpc.py --env BACKEND_TYPE=jaeger --env BACKEND_URL=http://127.0.0.1:18710 --stderr "$E/stdio.stderr.log" list-tools -- $BIN > "$E/stdio-tools-list.json"   # 19 tools, serverInfo, protocol
$PY $S/stdio_rpc.py --env ... call list_services '{}' -- $BIN                  # needs a fake on 18710
docker build -t tracehub-verify:$(git -C $W rev-parse --short HEAD) $W
docker run --rm -p 127.0.0.1:18705:8000 -e BACKEND_TYPE=jaeger -e BACKEND_URL=http://host.docker.internal:18710 tracehub-verify:<sha>   # #41: exit 2 without a token (CMD binds 0.0.0.0); pass -e MCP_HTTP_BEARER_TOKEN by NAME
docker inspect -f '{{.Config.Env}}' tracehub-verify:<sha>                      # FASTMCP_CHECK_FOR_UPDATES=off, FASTMCP_SHOW_SERVER_BANNER=false (#41)
$PY $S/extract_step.py $W/.github/workflows/release.yml 'name: <step name>' > "$E/step.sh"   # run with `bash -e` inside a fixture repo under $E only
```

## 4. Evidence discipline

- Capture under `$E/`: `server.log` (stderr+stdout of the server), the probe outputs (`http-probes.txt`,
  `raw-*.txt`, `*.json` from `stdio_rpc.py`), `fake-*.log` and `/_control/state` dumps, `cred-*.txt` with the
  exit code appended. Tokens and passwords are masked by the scripts (`<TOKEN>`); still grep before quoting.
- Quote the decisive lines: status line + `www-authenticate`/`mcp-session-id` headers, the `/ready` body, the
  `WARNING - Unexpected Host header: '...'` / `Readiness probe failed:` / `Configuration error:` log lines, the
  fake's request count before/after, `tool_count`/`tool_names`. Name the file and the line.
- Verdict per claim: PASS / FAIL / BLOCKED (exact point) / SKIP (why). A probe that broke a control is a FAIL
  even if CI is green. Say which head (`git -C $W rev-parse --short HEAD`) and which venv.
- Readiness classes and timing matter: `/ready` answers 503 within ~10 s on a hung backend (route deadline),
  one `Readiness probe failed` WARNING per fresh probe, memoised for `READINESS_CACHE_SECONDS`.

## 5. Gotchas (all bitten before)

- SecretScan hook: Bash command TEXT and Write CONTENTS with a bearer-scheme token literal or `NAME=<secret
  literal>` are blocked - generate into a 0600 file, `set -a; . token.env; set +a`, let scripts read
  `$MCP_HTTP_BEARER_TOKEN`; `http_probes.sh` assembles the scheme word at runtime for this reason.
- Launchers drop EMPTY env vars: for the empty-token gate run
  `timeout 10 env -i PATH=$W/.venv/bin:/usr/bin:/bin MCP_HTTP_BEARER_TOKEN= $BIN --transport http --host 127.0.0.1 --port 18702; echo exit=$?`
  directly (**#41**: exit 2 `(got 0)`; main has no gate - a server starts and timeout kills it, exit=124 - then
  `lsof -ti tcp:18702 -sTCP:LISTEN` must print nothing).
- Stop by pid (`kill $(cat server.pid)`, `lsof -ti tcp:PORT -sTCP:LISTEN`); never `pkill -f <pattern>` - it
  matches your own shell. `pgrep -fl '\.venv/bin/tracehub-mcp'` must be empty when you finish.
- uvicorn quotes the request path BEFORE the access line is written: a token in a matrix parameter shows as
  `%3B...`, a path segment stays visible - test placements, not just `?access_token=`. Access log is off by
  default (**#41**); turn it on with `--access-log` for the placement probes.
- Two canonicalisers: Host matching (`_canonical_hostname`: one trailing dot stripped, IPv6 RFC 5952, `[::1]`
  with/without port OK, `[::1]evil` / unclosed `[` / `localhost..` -> 421) and the backend origin pin
  (scheme+host+port of the configured URL; same host other port, `//host`, http->https all refused before any
  connect). Test both sides; a probe that passes one is not evidence for the other.
- POST `/mcp` needs `Content-Type: application/json` AND `Accept: application/json, text/event-stream`; replies
  are SSE `data:` frames; `notifications/initialized` -> 202; unknown/reaped session id -> 404.
- The archive fake refuses ports outside its range (exits `port must be within 18100-18199`) - a silent
  `/ready` 503 was that, not the server. Copy and widen the check for 187xx.
- Fake `delay_seconds` delays the whole response; byte-trickle shapes need a raw TCP helper
  (`$M/scratch-pad/security-verification-2026-10/verify/harness/delta-handle/slow_body_server.py`).
- `verify/harness/lead/mcp_stdio_client.py` in the archive needs `--arg=--url` (argparse); `stdio_rpc.py` here takes
  the server command after `--`.
- `extract_step.py` stops at the next step boundary: a `uses:` step or a single-line/folded `run:` exits 1 naming the
  step instead of handing back the NEXT step's body, and it echoes the matched line (file:line) to stderr - this
  workflow has three `Setup Python` steps, so check the echoed line number is the step you meant.
