---
name: observability-sentry
description: Use when working with Sentry — SDK init, breadcrumbs/tags/context, releases + source maps, performance monitoring, the sentry CLI.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-07-01
  type: observability
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-07-01"
  related: [observability-essentials, debugging, root-cause, security]
---

# Sentry

**Iron Law: send errors with breadcrumbs + tags + user context. Release tracking + source maps for stack traces that actually point at code.**

> NOTE for Claude: this skill describes the `sentry` CLI which executes shell commands. Run CLI invocations only when the user explicitly asks for them. If a command would mutate (delete, resolve, merge, deploy), confirm with the user first and verify org/project context in the output.

Sentry groups exceptions into **issues** (the same bug fingerprinted across thousands of events), attaches breadcrumbs and stack frames with local variables, and ties them to **releases** so you can see "this regressed in 1.4.2." It also ingests OTel-compatible traces and logs. Sentry is the system of record for things that broke — logs are narrative, metrics are aggregates, **Sentry is the bug queue**.

## SDK init — one line per language

```python
import sentry_sdk
sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], release="checkout@1.4.2",
                environment=os.environ["ENV"], traces_sample_rate=0.1,
                send_default_pii=False, before_send=scrub)
```

```typescript
import * as Sentry from "@sentry/node";
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: "checkout@1.4.2",
  environment: process.env.ENV,
  tracesSampleRate: 0.1,
  sendDefaultPii: false,
  beforeSend: scrub,
});
```

```go
sentry.Init(sentry.ClientOptions{ Dsn: os.Getenv("SENTRY_DSN"),
            Release: "checkout@1.4.2", Environment: os.Getenv("ENV"),
            TracesSampleRate: 0.1, BeforeSend: scrub })
```

```rust
sentry::init(sentry::ClientOptions {
    dsn: std::env::var("SENTRY_DSN").ok().and_then(|s| s.parse().ok()),
    release: Some("checkout@1.4.2".into()),
    environment: std::env::var("ENV").ok().map(Into::into),
    traces_sample_rate: 0.1, send_default_pii: false, ..Default::default()
});
```

DSN identifies the project; environment & release scope the events. **Release must match exactly** what you create via `sentry-cli releases new` — same string, character for character. It's the join key for source maps, deploys, regression detection.

## Breadcrumbs — the trail before the crash

Breadcrumbs are auto-captured for HTTP, DB, console — and you add custom ones:

```python
sentry_sdk.add_breadcrumb(category="checkout", message="cart locked",
                          level="info", data={"order_id": id})
```

Default ring buffer: 100 most-recent. When the exception fires, all are attached. The pre-crash narrative is usually where the root cause hides.

## Tags vs context vs extras — pick the right slot

| Slot        | Indexed?            | Searchable?       | Cardinality                        | Use for                                                      |
| ----------- | ------------------- | ----------------- | ---------------------------------- | ------------------------------------------------------------ |
| **Tag**     | yes                 | yes (`tag:value`) | **bounded** (keep <100 values/key) | `env`, `feature_flag`, `region`, `tier`                      |
| **Context** | structured, partial | partial           | bounded                            | `user`, `os`, `runtime`, `device`, custom blocks             |
| **Extra**   | no                  | no                | unbounded                          | dumping data you might want to see (request bodies, configs) |

```python
sentry_sdk.set_tag("region", "us-east-1")               # search: region:us-east-1
sentry_sdk.set_user({"id": user_id, "email": email})    # contextual (PII-aware)
sentry_sdk.set_context("order", {"id": id, "total": 99.50, "items": 3})
sentry_sdk.set_extra("raw_request_body", body)          # last-resort dump
```

**Decision tree:**

- Need to filter issues by this field in the UI? → **tag** (bounded values)
- Per-user/per-request structured info? → **user** + **context**
- "Just want to see it on the event"? → **extra**
- High-cardinality (request IDs, timestamps, order IDs)? → **never a tag**; context or extra

## Releases — the join key for everything

All commands use the `sentry-cli` binary. Set `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT` in env (or `.sentryclirc`) so the per-command flags below stay short.

```bash
# Version MUST match Sentry.init({ release }) exactly
sentry-cli releases new "checkout@1.4.2"

# Associate commits (needs SCM integration + local git checkout)
sentry-cli releases set-commits "checkout@1.4.2" --auto

# Or read commits from local git only (no integration)
sentry-cli releases set-commits "checkout@1.4.2" --local

sentry-cli releases finalize "checkout@1.4.2"
sentry-cli deploys new -r "checkout@1.4.2" -e production
```

`--auto` requires a Sentry SCM integration (GitHub/GitLab/Bitbucket) **and** a local checkout. In CI, ensure `actions/checkout` with `fetch-depth: 0` runs before `set-commits --auto`. Wired correctly, you get **suspect commits** ("introduced in abc123 by alice") and commit links on every issue.

## Source maps — JS/TS stack traces that point at source

Without source maps, frames show minified gibberish. Modern flow uses **debug IDs** injected into bundles:

```bash
sentry-cli sourcemaps inject ./dist                     # inject debug IDs into JS + maps
sentry-cli sourcemaps upload --release "checkout@1.4.2" ./dist
```

Run both as a build step **after bundling, before deploy**. Debug IDs let Sentry match a frame from any release to the right source map, even if URLs change.

For other languages: Python frames are readable by default (debug builds), Go binaries need `--no-rewrite` + matching binary uploaded as a debug file, Java uses ProGuard mapping uploads.

## CLI — what `sentry-cli` actually does

`sentry-cli` is for release management, source-map upload, debug-info upload, event sending, and project listing — NOT issue triage. For issue search, AI root-cause (Seer), trace exploration, and live logs, use the web UI or the official MCP server (`Skill(mcp-protocol)` for the protocol; the Sentry MCP server exposes `search_issues`, `analyze_issue_with_seer`, etc.).

```bash
sentry-cli send-event -m "test event from CI"        # smoke-test SDK config
sentry-cli projects list                              # confirm auth + org context
sentry-cli debug-files upload ./binary                # symbolicate native/JVM/Apple builds
sentry-cli info                                       # print auth / org / project
```

Run `sentry-cli help` to see the full subcommand tree for your installed version. Subcommands names ARE the contract — they have changed across major versions (e.g., `releases` was once `release`).

## Performance monitoring

Sentry tracing is OTel-compatible: Sentry's SDK (auto-instruments HTTP/DB/queues), or OTel SDK + Sentry exporter, or OTel Collector + Sentry exporter pipeline. Trace IDs match across backends — pivot freely. `tracesSampleRate: 0.1` is sane; sample more on critical paths via `tracesSampler`. `profilesSampleRate` adds continuous profiling. See `Skill(observability-essentials)` for OTel basics.

## Redaction — `send_default_pii=False` is the right default

Wire `before_send=scrub` (see SDK init blocks above) — the SDK invokes it on every event:

```python
import re
SCRUB_KEYS = {"password", "passwd", "pwd", "token", "secret", "client_secret", "private_key",
              "key", "apikey", "api_key", "authorization", "bearer", "cookie", "set-cookie",
              "ssn", "card", "cvv"}
QUERY_RE = re.compile(
    r"([?&](?:token|api_key|apikey|access_token|sig|password|secret|client_secret|"
    r"private_key|key|bearer)=)[^&]+", re.I)

def _scrub(o):                                              # recurse dicts, lists, and nested mixes
    if isinstance(o, dict):
        return {k: ("[REDACTED]" if k.lower() in SCRUB_KEYS else _scrub(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [_scrub(x) for x in o]
    return o

def scrub(event, hint):
    req = event.get("request") or {}
    for field in ("headers", "cookies", "data", "env"):     # data = POST body (dict OR list)
        if field in req: req[field] = _scrub(req[field])
    if "query_string" in req: req["query_string"] = QUERY_RE.sub(r"\1[REDACTED]", req["query_string"])
    if "url" in req:          req["url"]          = QUERY_RE.sub(r"\1[REDACTED]", req["url"])
    event["extra"] = _scrub(event.get("extra"))             # `set_extra` dumps (arbitrary shape)
    for span in event.get("spans") or []:
        span["data"] = _scrub(span.get("data"))             # span attributes (dict-of-dicts/lists)
    return event
```

Headers-only scrubbers (the common copy-paste) leak credentials in `?password=`, `Cookie`, JSON POST bodies, list-shaped extras, and span attributes. Cover every channel. Also enable Sentry's server-side data-scrubbing rules (Settings → Security & Privacy) — defense in depth, since the client may crash before `before_send` runs.

## Integrations to enable

- **SCM (GitHub/GitLab/Bitbucket):** suspect commits, "Open in GitHub" on frames, auto-resolve via commit message.
- **Issue trackers (Jira/Linear):** create tickets from issues with one click.
- **Alerts → Slack/PagerDuty:** route by tag (`env:prod`) and priority.
- **CI release creation:** add `sentry-cli releases new` to the deploy job. Without it, no regression detection.

## Anti-patterns

- Release string in `Sentry.init` ≠ `sentry-cli releases new` version → no association, no source maps, no suspect commits
- Uploading source maps **after** deploy or to the wrong release → frames stay minified
- `send_default_pii=True` "for debugging" → leaks across the user base
- High-cardinality values as **tags** (request IDs, timestamps) → broken search, billing pain
- One DSN shared across prod/staging/dev → environments mix; use one project + distinct `environment`
- Resolving issues in Sentry without a commit referencing them → lose the link
- Echoing auth tokens in CI logs — never log them; the CLI keeps them out of stdout
- Manually constructing issue queries when `--query "is:unresolved assigned:me"` does it

## Red flags

| Thought                                  | Reality                                                              |
| ---------------------------------------- | -------------------------------------------------------------------- |
| "Source maps are nice-to-have"           | Without them, every JS crash is "Object.t at e.min.js:1:24891".      |
| "We'll match release strings eventually" | "Eventually" = never. Mismatch silently breaks regression detection. |
| "Tags are free"                          | High-cardinality tags break search and bloat indexes.                |
| "PII off means we can't debug"           | Set `user.id` only; redact the rest. You can still triage.           |

## Hand-off

For the OTel pipeline that feeds Sentry: `Skill(observability-essentials)`. For working from a Sentry issue to a root cause: `Skill(debugging)` + `Skill(root-cause)`. For scrubbing patterns: `Skill(security)`.
