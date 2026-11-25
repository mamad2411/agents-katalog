---
name: bluebox-otel-instrumentation
description: >
  Use when asked to instrument a service or repository with OpenTelemetry so its telemetry
  flows to Bluebox, or when you find a `.env.otel.bluebox-template` file in the repo. Guides
  service targeting, safe OTel config, secret handling, logging preservation, and verification
  with `bluebox ask`. Do NOT use for OpenTelemetry setups that target a non-Bluebox backend
  (e.g. exporting to Jaeger, Datadog, or a self-hosted collector) — that is generic OTel work,
  not this skill.
  Triggers: "add OpenTelemetry", "instrument this service", "instrument this repo", "set up
  tracing", "OTel setup", "wire up telemetry for Bluebox", ".env.otel.bluebox-template".
compatibility: Coding agents (Claude Code, Cursor, Windsurf, Copilot, Kiro, OpenCode, Codex)
metadata:
  version: "0.5.15"
  audience: coding-agent
---

# Bluebox OTel Instrumentation

> **STOP — do this first, even if the request says "add OpenTelemetry" or "instrument this."**
> Your **first response** must contain **only** (a) the service inventory and (b) the three
> instrumentation levels, and must **ask the user to choose a level before continuing**, marking
> level 3 (traces + logs + metrics) as the recommended default. If your harness offers an
> interactive single-select / radio-style prompt tool, present the three levels through it;
> otherwise end with an explicit question asking the user to reply with a number (1, 2, or 3). In that first
> response you must **not** call any file-editing, file-creation, install, or shell/command tools,
> and must not commit or open a PR. Then **end your turn and wait** for the user's answer.
> Do **not** announce a plan and carry it out: phrases like "I'll proceed with…" or "traces-first"
> are wrong here. Do not pick the level yourself, and do not default to a smaller level. A phrase like
> "add OpenTelemetry to this project" is the user asking you to start — it is **not** permission to
> finish in one turn or to choose the level for them.
> **Only exception:** if the caller's task instructions or the system prompt say no interactive user
> is available (an automated/batch/regression run that must finish without prompting), skip the wait,
> use the default (**traces + logs + metrics**), state the level you chose, and run to completion. If the user
> already named a level or scope, honor it and skip the question.

## Scope

Add repo-local OpenTelemetry SDK/agent instrumentation to the intended deployable service(s).
The user chooses how much to collect (see the STOP banner at the top); the recommended default is
the full set — **traces, logs, and metrics** — flowing to Bluebox.

This skill is **not** a full Dynatrace rollout. It wires the application's OpenTelemetry export
path and service identity; other observability/security products may still require separate setup.
Bluebox can analyze those other signals when they already exist in the connected environment, but
this skill does not configure them.

Adapt to the repository, but follow the workflow below. Do not silently choose a service, broaden
an ambiguous request to a repo-wide change, rewrite logging, or change timestamp semantics.

## The instrumentation-level gate

The STOP banner at the top of this skill is the governing rule: the instrumentation level is the
user's decision, so your first response is the inventory + the level menu + a question, with no edits
and no tool calls that change the repo, and you wait for their answer. Instrumenting changes what
data leaves the application and edits deployment/config, which is why the user — not you — picks the
scope. The rest of this skill (implementation, validation, commit/PR) happens only *after* the user
has chosen, or when the single exception in the banner applies.

## Capability coverage

Be explicit with the user about what this skill will and will not cover before editing code.

| Capability | Covered by this skill? | What to say / do |
|---|---|---|
| Server-side distributed tracing | **Yes — primary path** | Configure OTel spans, context propagation, service identity, and OTLP export for trusted server-side services. |
| OTel application logs | **Default (added safely)** | Part of the default instrumentation level (see Instrumentation level). Added additively: preserve existing log format, timestamps, sinks, and levels; add trace correlation (`trace_id`/`span_id`) so a failing request links to its logs. If you cannot capture a baseline log sample or cannot add logs without changing the existing format, fall back to traces-only and say so. |
| OTel application metrics | **Default (full level)** | Part of the recommended default level. Bluebox metrics ingest requires **delta temporality** (see the metrics rule below) — cumulative metrics are rejected. Dashboards, alerts, and SLOs are separate configuration. |
| Custom span attributes | **Yes, when useful** | Add attributes only when they are low-cardinality, non-sensitive, and useful for diagnosis. They are not the same as product-level request attributes or business events. |
| Business events | **No, except explicit follow-up work** | Do not claim OTel tracing creates business events. If the user needs business events, stop and propose a separate design/configuration task. |
| Browser RUM, Session Replay, Web Vitals | **No** | Do not put Bluebox OTLP ingest tokens in browser bundles or `VITE_*` env vars. Use the product's RUM/frontend instrumentation path instead. |
| Mobile RUM | **No** | Requires mobile RUM SDK/setup, not this server-side OTel workflow. |
| AppSec, vulnerabilities, attack/security events | **No** | Requires the product's application-security/security setup. Basic OTel SDK wiring does not enable AppSec or vulnerability detection. |
| OneAgent deep process/runtime/host monitoring | **No** | Requires OneAgent or equivalent platform setup, not repo-local OTel SDK wiring. |
| Kubernetes cluster / node / pod telemetry | **Separate procedure** | Not app-code instrumentation. Achievable via an OpenTelemetry Collector that ships cluster/node/pod metrics and Kubernetes events to Bluebox over the **same** Bluebox OTLP endpoint and ingest token, and it complements app spans (shared `k8s.*` attributes line workloads up with your services). Only when the user asks for cluster monitoring, read `references/kubernetes-collector.md`. |
| Host metrics, Prometheus scrape, log files, datastore metrics | **Separate procedure** | Not app-code instrumentation. Achievable via an OpenTelemetry Collector that ships host metrics (`hostmetrics`), an existing Prometheus `/metrics` scrape, log files (`filelog`), or datastore metrics (`postgresql`/`mysql`/`redis`/…) to Bluebox over the **same** OTLP endpoint and ingest token. Cumulative metric sources need the `cumulativetodelta` processor; datastore receivers need a least-privilege monitoring credential. Only when the user asks for one of these, read `references/collector-receivers.md`. |
| Serverless functions (AWS Lambda) | **Separate procedure** | App-code instrumentation, but the runtime lifecycle differs: the SDK's default batch export drops spans across the freeze/thaw cycle, so the recommended path is the AWS-managed OpenTelemetry Lambda layer (or an explicit force-flush before the handler returns), exporting to the **same** Bluebox OTLP endpoint and ingest token. Only when the user asks to instrument a Lambda function, read `references/serverless-lambda.md`. |
| Cloud provider resource inventory / managed-service monitoring | **No** | Requires cloud provider integrations. OTel app spans and `cloud.*` resource attributes reference these resources, but this skill does not install or configure cloud-service monitoring. |
| Synthetic monitoring | **No** | Requires synthetic monitor configuration. |
| SLOs, dashboards, alerts, anomaly detectors | **No** | OTel data can feed these later, but this skill does not create or tune them. Recommend a separate monitoring/SLO task after telemetry is verified. |

If the user asks for an out-of-scope capability, do not improvise a partial implementation under the
OTel skill. Explain the boundary, finish any requested OTel baseline work, and list the separate
setup path as a follow-up.

## Instrumentation level

After the service inventory and before editing, present the user a short choice of how much
telemetry to collect. Write for someone who does not know observability jargon: describe each level
by **what Bluebox can then do for them**, not by signal names. Offer these three cumulative levels
and recommend the default:

1. **Essential — request traces.** Records the path of each request through the service(s). Lets
   Bluebox investigate incidents end to end (find the root cause of failures or slowness across
   your services), answer questions like "why is checkout slow or erroring?", and map how your
   services depend on each other. No changes to your logging; lowest overhead.
2. **Better root cause — traces + logs.** Everything in Essential, plus your app's logs
   **sent to Bluebox** and linked to the matching request, so Bluebox can tell you not just *what*
   failed but *why* — it can pull the exact error text from the failing request during an
   investigation, and you can search logs when you ask Bluebox questions. This requires actually
   exporting logs to Bluebox, not only stamping trace IDs on local logs. Added safely: your existing
   log sink, format, and timestamps are preserved (see the log-export mechanics below).
3. **Full picture — traces + logs + metrics (recommended default).** Everything above, plus trends over time (request
   volume, error rate, response-time percentiles, resource use), so Bluebox can learn what "normal"
   looks like, catch regressions, answer capacity questions ("can this handle more traffic?"), and
   confirm a deploy did not make things worse.

Behavior:

- By default, present the three levels (default marked) and **stop — end your turn and wait for the
  user to choose.** Do not edit, install, configure, commit, or open a PR first, and do not assume
  you are unattended and pick for them (see the STOP banner at the top).
- Skip the wait only when the user already specified a level or scope (honor it), or the caller's
  instructions/system prompt state that no interactive user is available and the task must finish
  without prompting (automated/batch/regression run) — then use the **default (level 3: traces + logs
  + metrics)** and state which level you chose.
- If logs cannot be **exported** safely for the selected service, fall back to trace-only for that
  service and say so explicitly — do not silently downgrade. "Traces plus trace-correlated local
  logs but no log export" is a fallback, not the default: it does not give Bluebox the log text, so
  name it as a limitation and record it as a `blocked`/partial log signal in the verification table.

### Log-export mechanics (level 2+)

The default level means log records reach Bluebox, added **additively** — never by replacing or
reformatting the existing logger:

- **Preferred:** keep the app's existing log sink (stdout/file) and format exactly as-is, and add an
  OTel logs export path alongside it — the OTel logs SDK + an OTLP **log** exporter, bridged from the
  logging framework already in use via its matching OTel appender/bridge (for example the
  winston/pino/bunyan appenders for Node, the `logging`/`structlog` handler for Python, the
  Logback/Log4j appender for Java). Add trace correlation (`trace_id`/`span_id`) so exported logs
  line up with spans.
- **Bespoke logger with no off-the-shelf bridge:** emit an OTel `LogRecord` additively from the
  existing log function (keep the current write, and also emit through the OTel logs API) rather
  than swapping the logger. Only do this if it is low-risk and preserves the existing output.
- **Only** fall back to trace-only (or trace-correlated-local-logs-without-export, named as a
  limitation) when neither path can be done without changing the existing logging behavior.
- The logging bridge/appender that matches the app's existing logger is a legitimate dependency at
  this level (log export is in scope by default); still do not add a bridge for a logger the app
  does not use, and do not pull broad auto-instrumentation just for logs.
- Offer the **contextual add-ons** only when the repo shows they apply, and never fold them into the
  three-level choice: Kubernetes/host infrastructure monitoring (via a Collector — privileged, get
  explicit approval; see the Separate-procedure rows) and AWS Lambda serverless instrumentation.
  Metrics-only-from-infrastructure and datastore monitoring likewise live in the Separate-procedure
  references, not in the app-signal levels above.

## Hard rules

1. **Never handle the ingest token.** Do not fetch it, print it, paste it into a file, or pass it as
   a CLI argument. Wire the app to read a token from an env var or secret reference; the user
   supplies the value.
2. **Keep config external.** Do not hardcode endpoints, tokens, headers, service names, or secrets
   in source code.
3. **Never commit secrets.** Confirm local env files that may contain a real token are git-ignored.
4. **Inventory before editing.** Write the required service-inventory table (see Service targeting)
   before changing dependencies, instrumentation code, or deployment config; it must identify
   deployable services, browser/client code, route/controller code, shared libraries, and the
   intended target set. Present it together with the instrumentation-level menu as your first-turn
   output (see the STOP banner at the top). In an interactive run your first turn ends there and waits for
   the user; only when the caller has said to run without prompting do you continue straight through
   to implementation, validation, and commit/PR.
5. **Minimize dependencies.** Before adding any package, name the exact signal and runtime path it
   enables. Do not install compatibility shims, logging transports, metrics exporters, or framework
   integrations for libraries that are not present in the selected service or for signals the user
   did not approve. Prefer the smallest framework-recommended OTel setup that satisfies the agreed
   scope.
6. **The instrumentation level is a user decision (see the STOP banner at the top).** Do not edit until it
   is chosen. Traces + logs + metrics (the full level) is the recommended default and the level to
   use when the user declines to choose or the caller has stated no interactive user is available;
   logs are added additively, preserving format/timestamps, and metrics use Bluebox-compatible delta
   temporality. Never add a signal that changes existing logging behavior without the safety checks
   in rule 8.
7. **Do not expose ingest tokens to browsers.** For browser-only frontends or static SPAs, do not
   put Bluebox ingest tokens or OTLP headers in client-side env vars such as `VITE_*`, bundles, or
   HTML. Use a server-side collector/gateway or the product's RUM path instead.
8. **Preserve logging and timestamps.** Logging changes must be additive. Do not replace loggers,
   formatters, timestamp fields, timezone, precision, schemas, sinks, levels, or correlation fields
   unless the user explicitly approves it. If you cannot capture a baseline log sample, do not
   modify logging config.
9. **Use the Bluebox/Dynatrace direct-ingest OTLP contract.** Generic OpenTelemetry supports
   multiple transports, but Bluebox's direct Dynatrace ingest path is intentionally narrower: use
   `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` and the HTTPS OTLP endpoint Bluebox provides
   (normally port 443 for SaaS). Do not switch direct-to-Bluebox ingest to gRPC/4317. Use the
   authorization header value exactly as Bluebox shows it for the token type; do not invent or
   change the auth scheme.
10. **Metrics must use delta temporality.** If — and only if — you configure metrics, Bluebox
    ingest requires **delta** temporality; cumulative metrics are rejected (HTTP 400 /
    partial-success), so misconfigured metrics fail silently. For SDK/app exporters set
    `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta` (or the equivalent in-code delta
    temporality selector). For an OpenTelemetry Collector pipeline whose receivers emit cumulative
    metrics (for example `prometheus` or database receivers), add the `cumulativetodelta` processor
    to the metrics pipeline. This applies only when metrics are in scope; it does not affect traces
    or logs.

## Service targeting

Build a compact inventory before implementation. A deployable service is a runtime process with
production or production-like deployment evidence: API server, server-rendered frontend, worker/
consumer, scheduler/cron job, admin service, or similar long-running process. Exclude libraries,
generated clients, browser-only/static frontends, examples, tests, build tools, API routes/controllers
that run inside another service, and one-off scripts unless the user explicitly includes them or
deployment manifests prove they run as trusted server processes.

Before installing packages or editing code, write this table in your plan or progress notes (Hard rule 4 governs when to proceed vs. stop):

| Candidate | Path | Evidence | Classification | Action |
|---|---|---|---|---|
| `<name>` | `<path>` | `<package script, Docker/compose/k8s entry, runtime entrypoint, import evidence>` | `deployable service` / `browser-client` / `route-controller` / `shared-library` / `tooling-test-example` / `unknown` | `instrument` / `exclude` / `ask` |

Use `instrument` only for deployable trusted server-side processes in the selected target set. Use
`exclude` for browser/client code, shared packages, route/controller files that are part of an
already-listed service, and tooling/test/example code. Use `ask` only when the user's request is
ambiguous and you cannot safely infer the target set. For each instrumented service, include the
proposed `OTEL_SERVICE_NAME`, start command/config injection point, and existing telemetry/logging
notes before editing.

Target-selection rules:

- If the user names one service, instrument only that service.
- If the user explicitly says "all", "repo", "repository", or "project", show the inventory and
  plan, then instrument all deployable services.
- If multiple deployable services exist and the user did not clearly choose one or all, show the
  inventory and ask before editing.
- Never choose a target based on first file found, easiest implementation, directory order, or
  perceived importance.

## Bluebox config template

Bluebox setup writes **`.env.otel.bluebox-template`** at the repository root. Treat it as the
canonical config contract; do not invent a parallel set of variable names.

Use these values from the template/runtime environment:

- `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`
- `OTEL_EXPORTER_OTLP_ENDPOINT=<Bluebox/Dynatrace OTLP endpoint>`
- `OTEL_SERVICE_NAME=<one stable name per runtime service>`
- `OTEL_RESOURCE_ATTRIBUTES=service.namespace=...,deployment.environment=...`

When the service runs on a cloud provider, extend `OTEL_RESOURCE_ATTRIBUTES` with cloud resource attributes from the [OTel cloud semconv](https://opentelemetry.io/docs/specs/semconv/resource/cloud/). These let Bluebox correlate traces with infrastructure context:

| Attribute | Representative values | Notes |
|---|---|---|
| `cloud.provider` | `aws` / `azure` / `gcp` / `alibaba_cloud` / `ibm_cloud` / `tencent_cloud` | Set whenever the service runs on a cloud provider |
| `cloud.region` | `us-east-1`, `westus2`, `us-central1`, … | Provider-specific region identifier |
| `cloud.availability_zone` | `us-east-1a`, `uksouth-1`, … | Specific AZ within the region |
| `cloud.platform` | `aws_ec2`, `aws_ecs`, `aws_lambda`, `azure_vm`, `azure_functions`, `gcp_compute_engine`, `gcp_cloud_run`, `gcp_kubernetes_engine`, … | Runtime platform |
| `cloud.account.id` | AWS account ID / Azure subscription ID / GCP project ID | — |
| `cloud.resource_id` | ARN or ID of the resource matching `cloud.platform` — ECS task ARN for `aws_ecs`, EC2 instance ARN for `aws_ec2`, Lambda function ARN for `aws_lambda`, Azure VM resource ID for `azure_vm`, … | **Strongly recommended**; must match the running resource, not the underlying host |

Example for a service running on AWS ECS (include `cloud.resource_id` with the task ARN):
`OTEL_RESOURCE_ATTRIBUTES=service.namespace=backend,deployment.environment=prod,cloud.provider=aws,cloud.region=us-east-1,cloud.platform=aws_ecs,cloud.resource_id=arn:aws:ecs:us-east-1:123456789012:task/my-cluster/abc123def456`

Some OTel SDKs ship a cloud resource detector that auto-populates these attributes from the instance/task metadata endpoint (EC2 IMDSv2, ECS task metadata, Azure IMDS, GCP metadata server) — prefer the detector over hardcoded values to avoid configuration drift. Check the SDK's resource detector docs for the specific runtime.

Also extend `OTEL_RESOURCE_ATTRIBUTES` with VCS resource attributes from the
[OTel VCS semconv registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/vcs/)
(reference link only — the guidance below is self-contained, nothing needs to be fetched).
They tie the running service to the repository and commit it was built from, which is how Bluebox
maps a service's telemetry back to its source:

| Attribute | Value | Notes |
|---|---|---|
| `vcs.repository.url.full` | Canonical URL of the repository the service is built from — the browser-locatable https form, no credentials, e.g. `https://github.com/org/repo` | This URL is the service→repository mapping key for multi-repo support. Bluebox connects repositories by this same canonical https form, so deriving it from `git remote get-url origin` + the normalization rules below yields the matching key by construction; if the repository was connected through a fork or mirror URL, use that URL instead |
| `vcs.ref.head.revision` | The commit SHA the running build was produced from | Full SHA, i.e. `git rev-parse HEAD` at build time |

Derive both values at **build/deploy time, not runtime** — inside a container there is typically
no `.git` to inspect. Inject them where the build knows them: the start/dev script or the
CI/deploy environment, a Docker build-arg passed through to a runtime env var (VCS identity is
build metadata, not a secret — build-args are appropriate here and keep the revision drift-free;
never pass tokens or OTLP auth through build-args), or the platform's equivalent (Helm value,
task definition, pipeline-set app config). For local dev runs the git commands work directly.
For example:

```bash
OTEL_RESOURCE_ATTRIBUTES="...,vcs.repository.url.full=$(git remote get-url origin | <normalize>),vcs.ref.head.revision=$(git rev-parse HEAD)"
```

Normalize the remote URL to the canonical form: (1) map ssh remotes (`git@host:owner/repo(.git)`,
`ssh://…`) to `https://host/owner/repo`; (2) strip any userinfo/credentials; (3) strip a trailing
`.git` — the registry note says the URL should not include the `.git` extension — and any trailing
slash. Guard each substitution: if the git command fails or prints nothing, drop that entire
`key=value` pair — an unguarded `$(git …)` emits exactly the empty value this block forbids.

Where env injection is not the runtime's idiom, set the same two attributes in code — **merge**
them into the SDK's default/env-derived resource; do not construct a replacement resource, which
would drop env-derived attributes such as `service.namespace` and `deployment.environment` —
reading values the build stamped into the artifact (a generated build-info file, a
linker/compile-time-injected constant, or a manifest entry): same attribute names, same values as
the env form. Every SDK this skill targets honors `OTEL_RESOURCE_ATTRIBUTES`, so prefer the env
route whenever it is available.

When a source value is unavailable (no git remote, a detached or tarball build), **omit** that
attribute entirely rather than emitting it with an empty value.

`OTEL_SERVICE_NAME` is the standard convenience variable for the `service.name` resource attribute.
Do not also set a conflicting `service.name` inside `OTEL_RESOURCE_ATTRIBUTES`. If the service
already has a deliberate `service.name` in code, collector config, or deployment config, preserve it
unless the user agrees to rename it.

The ingest token is not in the template. If you document an env-file example for the user to fill,
quote header values because they contain spaces, for example
`OTEL_EXPORTER_OTLP_HEADERS="Authorization=... <token>"`. For the Bluebox/Dynatrace ingest token,
use the header format Bluebox displays; do not URL-encode the space in `Api-Token <token>` unless a
specific SDK/runtime documents that it requires encoding. Keep the real token out of tracked files.

The template remains the canonical variable contract. Prefer the generic `OTEL_EXPORTER_OTLP_*`
variables when all configured signals share the same Bluebox endpoint and token. Use signal-specific
variables such as `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` or `OTEL_EXPORTER_OTLP_TRACES_HEADERS` only
when a runtime requires them or when signals intentionally use different endpoints/credentials. For
OTLP/HTTP, a generic endpoint is the base OTLP endpoint (SDKs append `/v1/traces`, `/v1/metrics`, or
`/v1/logs`); a signal-specific endpoint usually includes the signal path. For multi-service repos,
mirror the same variable contract into each service's runtime env, deployment manifest, compose
service, Helm values, or process manager config. Each runtime service needs its own service identity;
do not reuse one `OTEL_SERVICE_NAME` for unrelated services.

If the endpoint is blank, run:

```bash
bluebox otlp-endpoint
```

- Exit `0`: stdout is the endpoint; write it into the template or service env config.
- Exit `1`: endpoint is not available yet; wait and retry.
- Exit `2`: manual connection setup is required; stop and tell the user to configure the monitoring
  environment connection in the Bluebox web frontend.

If the template is missing, first run the setup phase that reconciles local repositories, for
example `bluebox setup local-repos` with the appropriate repo selection. If that cannot regenerate
the template, ask the user to run `bluebox setup` for the repository. Do not hand-write the template
from memory.

## Implementation workflow

1. **Inventory + ask, then STOP.** Produce the service inventory and the instrumentation-level menu,
   ask the user which level to use, and **end your turn without editing anything** (see the STOP
   banner at the top). Do steps 2+ only after the user has chosen — or immediately, without asking,
   when the caller has said no interactive user is available.
2. **Audit current observability** for each selected service: existing OTel/vendor agents, startup
   command, deployment env injection, logger configuration, timestamp behavior, and current
   dependencies/logging libraries.
3. **Plan minimal changes** per service. Prefer zero-code/auto-instrumentation when reliable; add
   code only where the runtime/framework needs it. List every new package before installing it and
   justify why it is required for the agreed signal scope.
4. **Add SDK/init or runtime instrumentation** for selected services only.
5. **Set service identity** with `OTEL_SERVICE_NAME` and resource attributes. Preserve an existing
   deliberate `service.name` unless it is clearly wrong and the user agrees to change it. Avoid
   conflicting service-name sources; `OTEL_SERVICE_NAME` should align with, not fight, any existing
   `service.name` resource attribute. When the service runs on a cloud provider, add cloud resource
   attributes (`cloud.provider`, `cloud.region`, `cloud.platform`, etc.) to `OTEL_RESOURCE_ATTRIBUTES`;
   prefer the SDK's cloud resource detector when available in the target runtime rather than
   hardcoding values. Also set the VCS resource attributes (`vcs.repository.url.full`,
   `vcs.ref.head.revision`) from build/deploy-time values per the VCS block in *Bluebox config
   template*.
6. **Protect logging while exporting it (default level).** Logs are part of the default level, so
   export them to Bluebox — but additively: keep the existing log sink, formatter, schema,
   timestamps, timezone, precision, and levels unchanged, and add an OTel log-export path alongside
   them (see *Instrumentation level* → log-export mechanics). Add trace/span correlation and map
   existing event timestamps as event time, not ingest time. If you cannot export logs without
   changing the existing logging behavior, fall back to trace-only and say so — do not silently ship
   correlation-without-export as if it were the default.
7. **Wire deployment config.** Non-secret defaults may be set via runtime env, compose, Kubernetes,
   Helm, process manager config, or Dockerfile `ENV` when appropriate. The ingest token or
   authorization header must never be set with Dockerfile `ENV`/`ARG`, image build args, committed
   compose files, or committed Helm values; reference it only through runtime env injection or a
   secret.
8. **Update run instructions.** If instrumentation changes the start command (for example adding
   `opentelemetry-instrument`, `-javaagent`, or `node --require`), update the README, developer
   docs, compose command, or scripts that tell people how to run that service.
9. **Hand off the token.** Tell the user to get it from Bluebox: open the Setup page and use the
   **Reveal token** action in the instrumentation step. Tell them exactly which env var or secret
   key to populate. Never ask to see the value.

## Language reference

| Lang | Preferred approach | Notes |
|---|---|---|
| Go | OTel SDK + OTLP HTTP exporter; middleware such as `otelhttp`, `otelgin`, `otelecho`, `otelgrpc` | Add a tracer provider and graceful shutdown; do not replace existing logger config. |
| Node/TS server | Framework-recommended server-side OTel setup, usually `@opentelemetry/sdk-node`, `auto-instrumentations-node`, and an OTLP HTTP trace exporter or env-driven exporter config | Load instrumentation before app startup; avoid reordering startup in a way that changes logging. For Next.js, use the server/runtime instrumentation hook and guard browser/edge runtimes. Do not treat browser Vite/React apps as Node server services. Do **not** add `@opentelemetry/shim-opencensus` unless the repo actually uses OpenCensus. For the default level, add a **log** export path: use the OTel logs SDK + OTLP log exporter and the appender for the logger already in use (for example `@opentelemetry/winston-transport` when the app uses winston, or the pino bridge for pino) — additively, preserving the existing sink; for a bespoke logger, emit `LogRecord`s alongside the existing write. Do not add a logging bridge for a logger the app does not use. |
| Python | `opentelemetry-distro`, OTLP HTTP exporter, `opentelemetry-bootstrap -a install` | Prefer `opentelemetry-instrument <app cmd>` when compatible; preserve `logging`/structlog/loguru formatting. |
| Java | OTel Java agent | Prefer `-javaagent` plus env/system properties; preserve Logback/Log4j patterns and timezone. |
| Ruby | `opentelemetry-sdk`, `opentelemetry-instrumentation-all`, OTLP exporter | Use `use_all`; preserve Rails/Sinatra logger formatting. |
| Rust | `opentelemetry`, `opentelemetry-otlp`, `tracing-opentelemetry` | Add a tracing layer without replacing subscriber formatting/timers unless necessary and documented. |

All languages should read transport config from `OTEL_*` env vars. Do not put endpoint or token
literals in language-specific code.

## Verify with Bluebox

Do not declare success until each selected service and configured signal is verified or clearly
marked as blocked/unverified. Verification has levels — do not collapse them:

| Status | Meaning |
|---|---|
| `configured` | Code, dependency, env, or deployment wiring exists, but you have not observed telemetry emission. |
| `emitting locally` | A local smoke test or temporary OTLP receiver observed the process attempting to export telemetry. This proves SDK/exporter emission only; it is **not** Bluebox verification. Keep temporary receivers/endpoints out of tracked production config. |
| `verified in Bluebox` | `bluebox ask` against a real workspace confirmed telemetry arrived for the service, signal, and time window, and that the VCS resource attributes configured for it (if any) are present. |
| `blocked` | Verification could not run or returned a non-answer. Explain the blocker and do not claim success for that signal. |

1. Build/test/start each selected service using its normal command.
2. Generate one known request, message, or job per selected service. Record the wall-clock time,
   route/job name, environment, expected `OTEL_SERVICE_NAME`, and the expected VCS values as
   configured at instrumentation time — the normalized repository URL and the build's commit SHA.
3. Verify traces with the Bluebox CLI; include `--env` when known. The question must also ask
   what values the spans carry for the VCS resource attributes — verifying them is part of the
   required verification, not an optional extra. Compare the returned values against the step-2
   expectations: `vcs.repository.url.full` must match the repository URL exactly as it is
   connected to Bluebox, and `vcs.ref.head.revision` must match the deployed commit. A mismatch,
   or a configured VCS attribute that does not show up, is a verification failure for that service
   (attributes legitimately omitted at build time per the VCS block are exempt); if the workspace
   cannot return the attribute values, record the existing `blocked` status rather than a pass:

```bash
bluebox ask --service <OTEL_SERVICE_NAME> --env <env> "are spans or traces arriving for <service> around <recorded-test-time>, and what values do they carry for vcs.repository.url.full and vcs.ref.head.revision?"
```

4. If metrics or logs were configured, verify those too with `bluebox ask`. For logs, compare
   against the baseline log sample and confirm timestamp field, timezone, precision, level, message,
   and sink are preserved:

```bash
bluebox ask --service <OTEL_SERVICE_NAME> --env <env> "show recent logs for <service> around <recorded-test-time> with event timestamps"
```

5. If a real Bluebox token/workspace is unavailable, you may use an untracked disposable local OTLP
   receiver only to check whether the service emits telemetry. Report that evidence as `emitting
   locally`, not as Bluebox verification. Do not commit local receiver services, fake endpoints, or
   test-only OTLP config as production instrumentation.
6. Scan tracked changes for accidental secrets before finishing. At minimum, check for real token
   prefixes such as `dt0c01.` / `dt0s16.`, committed `OTEL_EXPORTER_OTLP_HEADERS=` values that
   contain a real token, and userinfo-bearing URLs (e.g. `https://user:token@…`) in any committed
   `vcs.repository.url.full` value. Remove any hit before reporting success.
7. Treat non-zero `bluebox ask` exits as blockers. If `bluebox ask` returns a non-answer such as
   `## Cannot complete`, or says it is a dry-run/shim instead of a live workspace query, report the
   affected service/signal as `blocked`; do not fabricate evidence or mark it verified.

For deeper query patterns and `bluebox ask` behavior, load the **`production-query`** skill.

## Final response checklist

Always produce this report as your closing message, **even when verification was blocked** (including
when this environment's `bluebox ask` is a dry-run shim) or a signal could not be wired — mark those
signals `blocked` in the table and still include the next-steps recommendations. A blocked
verification is not a reason to end the task without the report.

Report:

- selected service inventory and why each service was included or excluded;
- files changed per service;
- every dependency added, with the signal/runtime reason for each one; explicitly state that no
  unused compatibility shims, logging transports, or unapproved signal exporters were added;
- env vars and secret references the user must populate, including whether dotenv header values
  must be quoted;
- secret-scan result showing no real ingest token or authorization header was committed;
- run-instruction docs updated when the service start command changed;
- whether logging was untouched or how existing logging/timestamps were preserved;
- `bluebox ask` verification result per selected service;
- a per-service/per-signal verification table using the statuses above, for example:
  `| Service | Signal | Status | Evidence | Blocker / next step |`;
- the instrumentation level chosen (and whether it was the user's choice or the default), and covered signals per service (traces, logs, and metrics by default) and whether each one was configured, emitting locally, verified in Bluebox, or blocked;
- out-of-scope capabilities that were **not** configured (for example RUM, AppSec, OneAgent, infrastructure/Kubernetes/cloud monitoring, synthetics, SLOs, dashboards, alerts) when relevant to the repo;
- any browser-only frontend or other service intentionally left out of direct OTLP instrumentation and why;
- any service, signal, or capability that remains blocked and why;
- **next steps for deeper insight** — close the report with a short, prioritized list of concrete,
  repo-grounded follow-ups that would give Bluebox more to work with, each framed by the insight it
  unlocks rather than by signal name ("next, instrument X so Bluebox can Y"). Draw only from what
  this repo shows and this run did not cover, for example: raising the level the user chose
  (traces → add log export so Bluebox can show the failing log lines; traces + logs → add metrics so
  Bluebox can baseline normal, catch regressions, and verify deploys); instrumenting services or
  entry points left out of this pass; contextual add-ons the repo has evidence for (Kubernetes/host
  infrastructure monitoring, AWS Lambda serverless, datastore/Prometheus/host metrics via a
  Collector); browser RUM for a detected frontend; or custom span attributes / business events on
  key flows (checkout, payment, signup). Suggest only items that apply to this repo, and present
  them as recommendations — do not implement them without a new request.
