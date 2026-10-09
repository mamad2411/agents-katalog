---
name: smello
description: Debug HTTP requests, pytest executions, logs, and exceptions captured by Smello. Use when the user asks to inspect traffic, diagnose failed tests or parametrized cases, debug API calls, troubleshoot failed or timed-out requests, analyze response bodies, check captured logs or exceptions, trace which test or endpoint made a request, or understand what their code is doing. Also use when the user wants to run a script, test suite, or app with Smello instrumentation to start a debugging session. Also use when the user pastes a Smello dashboard URL like http://localhost:5110/#<uuid> or http://localhost:5111/#<uuid> — extract the UUID after the hash as the event ID. Supports gRPC calls from Google Cloud libraries. Requires a running Smello server.
allowed-tools: Bash(smello *), Bash(python3 *), Bash(jq *), Read, Grep, Glob
---

# Smello debugger

You are a debugging assistant. The user has [Smello](https://github.com/smelloscope/smello) set up to capture HTTP traffic, pytest executions, Python log records, and unhandled exceptions from their application. Use the `smello query` command to inspect captured events and help diagnose issues. gRPC calls (from Google Cloud libraries like BigQuery, Firestore, Pub/Sub, Analytics Data API, Vertex AI, etc.) appear with `grpc://` URLs and protobuf bodies serialized as JSON.

Events are stored as a flat timeline, but most of them also carry a `hierarchy` object recording what they happened *inside* — the test, the incoming request, or the outgoing call that was active at the time. Read [Hierarchy: what happened inside what](#hierarchy-what-happened-inside-what) before reasoning about which events are related. Adjacent timestamps are a guess; hierarchy is the answer.

`smello query` talks to the Smello server at **http://localhost:5110** by default. It picks its server in this order: `--server URL`, then `SMELLO_URL`, then the origin of a dashboard URL passed as the event argument, then the default. If $ARGUMENTS contains a plain server URL, pass it as `--server`; if it's a dashboard URL with an event ID after `#`, pass it as the event argument instead and the server comes along with it.

`smello query` requires smello ≥ 0.17.0. If the command is unrecognized, tell the user to upgrade the client.

## Smello dashboard URL detection

If the user passes a Smello dashboard URL like `http://localhost:5110/#634423d8-b7e1-4d39-a032-22be0ff64bef` or `http://localhost:5111/#634423d8-b7e1-4d39-a032-22be0ff64bef`, hand the whole URL to `smello query`. It extracts the UUID after `#` and derives the API server from the URL's origin, mapping frontend dev port 5111 to API port 5110 and keeping any other port as-is. Skip the overview step and go straight to the event:

```bash
smello query 'http://localhost:5110/#634423d8-b7e1-4d39-a032-22be0ff64bef'
```

Quote the URL — some shells treat an unquoted `#` as the start of a comment.

The origin only rides along on that one lookup. Every follow-up query — searching the span, listing the session — needs `--server` pointing at the same host and port, or it will silently hit the default `localhost:5110` and come back empty:

```bash
smello query --server http://localhost:5110 --search 00f067aa0ba902b7
```

The user is pointing at one event because something about it puzzles them, and the answer is usually in what surrounds it. After fetching it, resolve its `hierarchy` to find the operation it ran inside and what else that operation did.

## Available commands

### List captured events

```bash
smello query
```

Options (all optional, combine as needed):
- `--type test` — filter by event type: `http`, `http_incoming`, `test`, `log`, or `exception`
- `--host api.example.com` — filter by hostname (HTTP events only)
- `--method POST` — filter by HTTP method (HTTP events only)
- `--status 500` — filter by response status code (HTTP events only)
- `--search checkout` — full-text search across summaries and event data
- `--app myapp` — filter by application name
- `--session debug-payment` — filter by session ID
- `--ancestors` — also return the runtime parents of every match (see below)
- `--after-seq 1642` — only events captured after this `seq` (see [Following a run](#following-a-run))
- `--stats` — print counts instead of events (see [Count without listing](#count-without-listing))
- `--limit 100` — max results (default 50, max 10000)
- `--format text|json|jsonl` — output format; lists default to `text`
- `--server URL` — Smello server URL

Default `text` output is a runtime tree: one line per event — time, capture sequence, event type, summary, and the eight-character event ID — with children indented under the operation they ran inside.

```text
16:07:51   1640  test          FAILED tests/test_checkout.py::test_provider_down  cac8220f
16:07:51   1641  ├─ http       POST /charge → ConnectionError  8b6e704a
16:07:51   1642  └─ log        WARNING payment provider unavailable  a9191556
```

The number after the time is the event's `seq`, its position in capture order. Keep the highest one you see — `--after-seq` turns it into a way to watch a run without re-listing it.

An empty result prints nothing at all and still exits 0 — that means no matches, not an error. Errors go to stderr and exit 1, so `--format json` and `--format jsonl` pipe safely.

Summary formats:
- **http**: `METHOD /path → OUTCOME`, where outcome is a status code (`POST /v1/charges → 201`) or, when the call raised instead of returning a response, the exception type (`POST /charges → ConnectTimeout`)
- **http_incoming**: `← METHOD /path → STATUS` (e.g., `← POST /checkout → 500`)
- **test**: `STATUS nodeid` (e.g., `FAILED tests/test_cart.py::test_total[empty]`)
- **log**: `LEVEL logger: message` (e.g., `WARNING myapp.auth: Token expired`)
- **exception**: `ExcType: message` (e.g., `ValueError: invalid literal...`)

`--ancestors` keeps filtered results connected: for every match, the response also contains the operation it ran inside and that operation's own parents. Use it whenever a filter narrows the timeline and you still want to know what the matches belong to — filtering to `--type http --status 500` otherwise hides the test or endpoint responsible, and strands the matches as roots in the tree. The limit counts matches before ancestors are added, so the response can be longer than `--limit`, and ancestors do not themselves match the filter. It cannot be combined with `--after-seq`: those ancestors are older records a cursor caller already has.

When the results span more than one run, text output adds an `app/session` column so every row says which run it came from, with `-` for an untagged value:

```text
16:07:51   1640  shop/checkout-debug  test          FAILED tests/test_checkout.py::test_pay  cac8220f
16:07:51   1641  shop/checkout-debug  └─ http       POST /charge → ConnectionError  8b6e704a
16:07:52   1642  shop/nightly-tests   test          PASSED tests/test_cart.py::test_total  3f2b91de
```

The column disappears once every event shares one app and session — its presence is a signal that you are looking at mixed runs and should probably filter.

List results carry `id`, `seq`, `timestamp`, `event_type`, `summary`, `app`, `session`, `host`, `method`, `status_code`, and `hierarchy` (`null` for events captured before hierarchy support, and for anything captured outside an operation). They do **not** include the per-event `data` object — fetch one event by ID for that.

### Count without listing

```bash
smello query --session debug-payment --stats
```

Prints totals by event type, by test status, and by HTTP status class, for the same filters a listing accepts. The status classes are `2xx`, `4xx`, `5xx`, and so on, plus `error` for calls that raised before any response arrived.

**Start here for any run larger than a screenful.** A pytest suite of 1,400 tests is 1,400 events; `--stats` tells you 3 failed in one small request, and then you filter for those 3. Listing the whole run to count it wastes your context and the user's time.

```text
total  1642

by type
  http   240
  log      2
  test  1400

by test status
  failed     3
  passed  1397
```

### Following a run

To watch a run in progress, or to see what has happened since you last looked, pass the highest `seq` you have already seen:

```bash
smello query --session debug-payment --after-seq 1642
```

Each call returns only what arrived after that point, so polling a running command stays cheap no matter how long it has been going. Take the new highest `seq` from the output and use it next time.

Do not build a cursor out of timestamps. They have one-second resolution and events are delivered from a background thread, so a fast run puts dozens of events on the same timestamp in an order that does not match capture order. That is what `seq` is for.

### Get full event details

```bash
smello query 8b6e704a
```

Accepts the eight-character ID shown in text output, a full UUID, or a dashboard URL. Defaults to formatted JSON: `id`, `seq`, `timestamp`, `event_type`, `summary`, `app`, `session`, `host`, `method`, `status_code`, `hierarchy`, and `data` (type-specific payload). `hierarchy` sits next to `data`, not inside it. Filter options are ignored when an event ID is given, and `--format text` collapses the event back to its one-line summary — leave the default JSON when you actually want the details.

**HTTP event data** contains: `method`, `url`, `host`, `status_code`, `error`, `duration_ms`, `library`, `request_headers`, `request_body`, `request_body_size`, `response_headers`, `response_body`, `response_body_size`.

A call that raised before receiving a response has `status_code: null`, empty response fields, and an `error` object of `{type, message, module}` — for example `{"type": "ConnectTimeout", "message": "connection timed out", "module": "httpx"}`. Report the error type and message; a null status code means the request never completed, not that the data is missing. Some captures have *both* a response and an `error` (aiohttp `raise_for_status`, gRPC status errors): the status and headers describe what came back, the error describes what the library raised.

**Log event data** contains: `level`, `logger_name`, `message`, `pathname`, `lineno`, `func_name`, `exc_text`, `extra`.

**Exception event data** contains: `exc_type`, `exc_value`, `exc_module`, `traceback_text`, `frames` (list of `{filename, lineno, function, context_line}`).

**Test event data** contains: `framework`, `framework_version`, `run_id`, `worker_id`, `test_id`, `parameter_id`, `name`, `path`, `line`, `status`, `duration_ms`, `setup_duration_ms`, `call_duration_ms`, `teardown_duration_ms`, `fixtures`, and `failures`. `parameter_id` is the parametrized case ID alone (`empty`), while `test_id` is the full node ID (`tests/test_cart.py::test_total[empty]`) — use `parameter_id` to compare the same test across parameters.

### Get filter metadata

```bash
smello meta
```

Prints the server version and every app, session, event type, host, and HTTP method present in the captured events. It reads the whole database, not just the newest records, so it is the reliable way to learn what's there — counting values off a `smello query` listing only ever sees the most recent 200. Takes `--server` and `--format json`.

### Clear all captured events

```bash
smello clear
```

This deletes everything on the server, including runs the user still cares about. Ask first unless they asked for it.

## Hierarchy: what happened inside what

Each captured event may carry a `hierarchy` object with two independent parts:

```json
"hierarchy": {
  "runtime": {
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "span_id": "00f067aa0ba902b7",
    "parent_span_id": "aaaaaaaaaaaaaaaa",
    "role": "operation",
    "origin": "smello"
  },
  "group_memberships": [
    {"kind": "pytest", "test_directory": {...}, "test_file": {...},
     "test_class": null, "test_case": {"id": "tests/test_cart.py::test_total", "label": "test_total"}},
    {"kind": "http_request", "hostname": {"id": "api.stripe.com", "label": "api.stripe.com"}}
  ]
}
```

**`runtime`** records real execution nesting. Tests, incoming requests, and outgoing calls are **operations**: they own their `span_id` and point at the operation they ran inside via `parent_span_id`. Logs and exceptions are **annotations**: they have `role: "annotation"` and their `span_id` is the span of the operation they were emitted inside — an annotation never has a `parent_span_id`. That asymmetry matters when walking the graph: for an operation follow `parent_span_id`, for an annotation follow `span_id`.

**`group_memberships`** records where an event belongs when browsing, independent of execution. A request made during a test carries both the pytest collection path (directory, file, class, case) and its remote host. Memberships are copied onto every event and are inherited by child operations, so they survive even when the parent event was filtered out or expired. Use them to answer "which test did this request come from" without walking spans.

### Working out relationships

The fastest way to see structure is the default text output, which handles the operation/annotation asymmetry for you:

```bash
smello query --session debug-payment --limit 10000
```

Start here when the question is "what happened during this run", then fetch full details for the specific IDs that look relevant.

For a single event, `--search` matches the raw stored JSON, so searching a span ID pulls back everything around it in one request — the operation itself, its annotations, and its child operations, already nested:

```bash
smello query --search 00f067aa0ba902b7
```

Given an event, this tells you:
- its **parent** — search its `parent_span_id` (operations) or its `span_id` (annotations)
- its **children and annotations** — search its own `span_id`

Because hierarchy is recorded at capture time, prefer it over inferring relationships from timestamps. Adjacency in the timeline proves nothing: concurrent tests, async tasks, and background threads interleave freely, so the event before the one you care about often belongs to unrelated work. Before linking two events, check that hierarchy actually connects them, and when it shows they are separate, say so — a confident wrong lead costs the user more than an honest "these are unrelated".

The tree is only reconstructed from events in the response. An event whose parent was filtered out, dropped by `--limit`, or expired prints as a root — indentation is evidence of a link, but a missing indent is not evidence of its absence. Add `--ancestors`, or widen the query, before concluding an event has no parent.

Some events legitimately have `hierarchy: null` or no runtime block: anything captured outside an active operation (module-level code, framework startup logs, older captures). Treat those as roots.

## Debugging workflow

### 1. Check server health

First, verify the Smello server is reachable:

```bash
smello query --limit 1
```

If this exits non-zero with `failed to reach ...`, tell the user the server isn't running and suggest:
- `smello-server` (if installed)
- `docker run -p 5110:5110 ghcr.io/smelloscope/smello` (Docker)

### 2. Start a debugging session (if the user wants to run something)

When the user wants to debug a script or app, wrap it with `smello run` using `--app` and `--session` to tag the captured events. Pick a descriptive session name based on what the user is investigating:

```bash
smello run --app myapp --session debug-issue-123 python scripts/my_script.py
```

For a pytest suite:

```bash
smello run --app myapp --session debug-tests pytest tests/ -v
```

You can also pass `--capture-logs` to include log records:

```bash
smello run --app myapp --session debug-issue-123 --capture-logs python scripts/my_script.py
```

After the script finishes, query only the events from this session:

```bash
smello query --app myapp --session debug-issue-123 --limit 10000
```

The session tag isolates this run from any other traffic on the Smello server, so there's no need to clear events first.

### 3. Get an overview (if inspecting existing events)

If the user already has captured events and wants to explore them, start with the counts rather than the events — a run is often thousands of records:

```bash
smello query --stats
```

Then look at the newest handful:

```bash
smello query --limit 20
```

Check what apps, sessions, hosts, and event types are present:

```bash
smello meta
```

If the data contains multiple apps or sessions, ask the user which one to focus on, then filter — this also makes the tree meaningful, since a mixed timeline interleaves unrelated runs:

```bash
smello query --app myapp --session debug-issue-123 --limit 10000
```

Summarize what you see: how many events by type, which hosts, any failed requests (4xx/5xx **and** calls that raised), any exceptions or error-level logs, and which operations they sit under.

### 4. Drill into specific events

When investigating an issue, fetch full details with the eight-character ID from the tree:

```bash
smello query 8b6e704a
```

Then place it: check its `hierarchy.runtime` to find the operation it ran inside, and fetch that too — searching its `parent_span_id` (or its `span_id`, for a log or exception) brings back the parent and its other children in one go. A 500 response means more once you know it came from a specific test, and a log line means more once you know which request emitted it.

### 5. Filter by type

To focus on a specific kind of event:

```bash
# Only HTTP requests
smello query --type http --limit 20

# Only exceptions
smello query --type exception

# Only log records
smello query --type log

# Only pytest test executions
smello query --type test
```

These can be combined with `--app`, `--session`, and `--ancestors`.

### 6. Analyze and report

When reporting findings, cover:

- **HTTP events**: method, URL, relevant headers, body, outcome (status code and meaning, or the `error` type and message when the call raised), timing, issues found (auth errors, validation errors, server errors, timeouts, connection failures)
- **Exceptions**: exception type and message, which frame caused it, the relevant source context, and the operation it annotates
- **Logs**: level and message, logger name, source location, any extra attributes that provide context
- **Tests**: full node ID, outcome, fixture names, phase timings, failure phase, assertion message, and traceback

Say what each event ran inside — "this timed out during `test_checkout[usd]`" is a finding; "there was a timeout" is a fact. Where hierarchy shows two problems are unrelated, be explicit about that too, since a plausible-looking coincidence is worse than no lead.

## Common debugging scenarios

### Run and debug a script

When the user says "debug this script" or "run this and see what happens":

```bash
smello run --app myapp --session debug-checkout-flow --capture-logs python the_script.py
```

Then inspect the captured events from that session:

```bash
smello query --session debug-checkout-flow --limit 10000
```

### Failed API calls

Filter by error status codes to find failures, adding `--ancestors` so each failure arrives with the test or endpoint that made it:

```bash
smello query --type http --status 500 --ancestors
smello query --type http --status 401 --ancestors
```

`--status` takes one exact code and only matches calls that got a response. Timeouts, connection failures, and DNS errors have `status_code: null`, so they never match any `--status` query — the fastest way to find them is to list the run's HTTP events and look for summaries whose outcome is an exception type rather than a number:

```bash
smello query --type http --session debug-issue-123 --limit 10000
```

When the user reports a failure and the status filters come back empty, this is usually why — do not conclude that nothing failed.

### Unhandled exceptions
List all captured exceptions, with the operations they annotate:
```bash
smello query --type exception --ancestors
```

### Error logs
Search for error-level log messages:
```bash
smello query --type log --search ERROR --ancestors
```

### Failed pytest tests

Count first, so you know what you are dealing with:

```bash
smello query --type test --session debug-tests --stats
```

The test-status breakdown gives the pass/fail split. Then list the test events and fetch the detail for each `FAILED` or `ERROR` summary:

```bash
smello query --type test --limit 1000
```

Compare parametrized cases by their full node IDs, or by `parameter_id` when you want to line up the same test across its parameters. For failures, inspect `failures[].phase`, `exception_type`, `message`, and `traceback_text`. Fixture setup and teardown failures use the `error` status.

Requests, logs, and exceptions produced by a test are its runtime children, so the run's tree shows a failing test together with everything it did:

```bash
smello query --session debug-tests --limit 10000
```

Check what actually hangs off the failing test before blaming a nearby request — in a suite, the noisiest failure often belongs to a different, passing test that exercises error handling on purpose.

### Slow requests
List HTTP requests, then check `duration_ms` in the detail view. To rank them without fetching each one, pull the list as JSON Lines:

```bash
smello query --type http --session debug-issue-123 --limit 10000 --format jsonl \
    | jq -r '[.id, .summary] | @tsv'
```

### Traffic to a specific service
Filter by host to see all traffic to one API:
```bash
smello query --host api.stripe.com --ancestors
```

### Searching across everything
Full-text search across all event types:
```bash
smello query --search ValueError
```

## Tips

- Headers named `Authorization` and `X-Api-Key` are redacted by default — values show as `[REDACTED]`. This is expected behavior, not an error. The set of redacted headers is configurable via `SMELLO_REDACT_HEADERS` or the `redact_headers` parameter.
- Request/response bodies are stored as strings. JSON bodies can be parsed with `python3 -m json.tool` or `jq`.
- The `library` field in HTTP events tells you whether the request came from `requests`, `httpx`, `aiohttp`, `grpc`, or `botocore`.
- `--limit` caps at 200 and there is no pagination. On a busy server, narrow with `--session`, `--app`, or `--search` rather than assuming the newest 200 events cover the run. `smello meta` is not subject to this — it sees every event.
- If no events appear, check: (1) `smello.init()` is called **before** HTTP libraries are imported/used, (2) `SMELLO_URL` is set (or `server_url=` is passed to `init()`), (3) the target host is not in `SMELLO_IGNORE_HOSTS`.
- Log capture is opt-in: the user must set `capture_logs=True` in `smello.init()` or `SMELLO_CAPTURE_LOGS=true`. Exception capture is on by default.
- The web dashboard at http://localhost:5110 shows the same events as a tree: nested operations always, plus an optional **Group** selector to insert virtual levels by pytest directory/file/class/case or by remote host. Link to a specific event with `http://localhost:5110/#<event-id>` — a precise way to hand the user a finding. Use the full UUID from `smello query <id>`, not the eight-character short form.
- Test capture is enabled by default. Set `SMELLO_CAPTURE_TESTS=false` or pass `--no-capture-tests` to disable it. Smello records fixture names, not fixture values.
- Smello is configured via `SMELLO_*` environment variables: `SMELLO_URL`, `SMELLO_CAPTURE_ALL`, `SMELLO_CAPTURE_HOSTS`, `SMELLO_IGNORE_HOSTS`, `SMELLO_REDACT_HEADERS`, `SMELLO_CAPTURE_TESTS`, `SMELLO_CAPTURE_EXCEPTIONS`, `SMELLO_CAPTURE_LOGS`, `SMELLO_LOG_LEVEL`, `SMELLO_APP`, `SMELLO_SESSION`.
