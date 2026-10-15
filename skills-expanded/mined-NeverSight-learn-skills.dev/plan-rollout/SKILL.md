---
name: plan-rollout
description: "Adds a multi-environment change-monitoring section to the agent's plan: enumerates target environments (staging, prod, regions, BYOC tenants), picks SLIs (golden signals + intended-effect + business-outcome) per env or shared, queries 24h baselines, sets baseline-referenced thresholds, and chooses a checkpoint schedule based on risk tier. Use when the user is planning a code change that will be deployed, preparing a rollout, asking how to monitor a release, doing post-deploy validation prep, planning a canary, or wants production watched after merging — even when they don't say 'monitoring plan'. Anchored on Google SRE book vocabulary (golden signals, SLI, error budget, blast radius). Companion to monitor-rollout."
argument-hint: "[optional: paste of the change diff, PR url, or --merge-sha <sha> for post-merge-no-plan]"
---

# plan-rollout

Authors a change-monitoring section for the user's plan. The section becomes the input to `monitor-rollout` after the change ships.

## When to use

The user is preparing a code change that will be deployed to production. Specifically:
- They're in plan mode and the change has a production-facing surface.
- They're drafting or reviewing a PR that will deploy.
- They're asking *"how should I monitor this?", "what should we watch for?", "what are the SLIs?", "do we need a canary?"*
- They're planning a release, a rollout, or a feature flag flip.

Skip this skill when the change is read-only or local-only, dev-stack only, or pure-documentation. Tell the user no monitoring plan is warranted in those cases.

## Methodology

Anchored on the Google SRE book. Full term map in [references/sre-vocabulary.md](references/sre-vocabulary.md). Risk-tiering rubric in [references/risk-rubric.md](references/risk-rubric.md). Tier-to-checkpoint mapping in [references/checkpoint-schedule.md](references/checkpoint-schedule.md). Indicator design (RATIO vs GAUGE, baselines, thresholds) in [references/indicator-design.md](references/indicator-design.md). Multi-environment handling in [references/multi-env.md](references/multi-env.md).

The plan you author has five pillars:
1. **Risk tier** + one-sentence reason — drives checkpoint cadence.
2. **Environments** — staging, prod, regions, tenants. Each gets its own deploy-detection command and may carry its own indicator overrides.
3. **Indicators** — golden signals + intended-effect + business outcome. Each indicator has a 24h baseline value queried *now* and a threshold expressed relative to that baseline.
4. **Deploy-detection** — exact command per environment that returns "deploy started for this commit" once the rollout begins.
5. **Rollback hint** — one line. The exact thing to do if a regression is detected. Required.

Per-source telemetry recipes:
- [references/datadog.md](references/datadog.md), [references/honeycomb.md](references/honeycomb.md), [references/axiom.md](references/axiom.md), [references/prometheus.md](references/prometheus.md), [references/cloudwatch.md](references/cloudwatch.md).

Per-deploy-system recipes:
- [references/github-actions.md](references/github-actions.md), [references/buildkite.md](references/buildkite.md), [references/argocd.md](references/argocd.md), [references/vercel.md](references/vercel.md).

## Workflow

Copy this checklist into the response and tick items off as work progresses:

```
plan-rollout progress:
- [ ] 1. Analyzed the diff (services, paths, data writes, infra)
- [ ] 2. Risk-tiered the change (low/medium/high + reason)
- [ ] 3. Enumerated target environments
- [ ] 4. Probed telemetry tools; picked one default
- [ ] 5. Picked checkpoint schedule from tier
- [ ] 6. Picked indicators (golden signals + intended + business); marked per-env vs shared
- [ ] 7. Queried 24h baseline per env per indicator
- [ ] 8. Picked deploy-detection recipe + exact command per env
- [ ] 9. Picked rollback hint (one line)
- [ ] 10. Asked the user about ambiguities (or noted N/A)
- [ ] 11. Rendered plan section + companion check
```

### 1. Analyse the diff

Run `git diff <base>...<head>` (three dots — merge-base). If the user pasted a PR url, use `gh pr diff <url>` first.

**Post-merge-no-plan invocation (`--merge-sha <sha>` argument):** when the umbrella chains plan-rollout for a post-merge-no-plan case, it passes `--merge-sha <sha>` of the merged commit. In that mode, anchor the diff on the *actual merged change* via `git diff <merge-sha>~1...<merge-sha>` (or `gh pr view <pr> --json mergeCommit,baseRefName` if the user gave a PR URL). This is what the change introduced — same diff the executor's evidence-discipline will reason about. Do not fall back to working-tree HEAD when `--merge-sha` is given; the working tree may have diverged.

Identify:
- Services and packages touched.
- HTTP request paths or RPCs whose behaviour changes.
- Data writes (new columns, migrations, queue producers).
- Infrastructure changes (Terraform, Helm, k8s manifests, IAM).
- Dependencies bumped (note major-version vs minor-version).
- Public-API contract changes.

Quote the file paths you considered — the agent and the user both benefit from the explicit paper trail.

### 2. Risk-tier the change

Read [references/risk-rubric.md](references/risk-rubric.md) and pick `low | medium | high`. State the tier and one sentence of reasoning. The tier drives step 5; do not skip the reasoning.

### 3. Enumerate target environments

Run `bash plan-rollout/scripts/enumerate_envs.sh` from inside the repo being changed. The script inspects deploy config:
- `.github/workflows/*.y*ml` for matrix jobs and per-environment workflows.
- `argocd/`, `gitops/` for `ApplicationSet` definitions.
- `vercel.json`, `.vercel/` for preview/prod scopes.
- `terraform/stacks/`, `deployments/` for fan-out targets.
- `netlify.toml`, `render.yaml`, `wrangler.toml` (with `[pages]`), `fly.toml` for git-integration deploys.
- Heuristic for git-integration-only repos (Next/Astro/Remix/Nuxt/SvelteKit + no GH Actions deploy + no IaC): emits `git-integration:likely-vercel-or-netlify`.
- Stderr emits `no-deploy-config-detected` when nothing fires, so the agent knows to ask explicitly rather than silently assuming single-env.

**Behaviour by mode:**
- **Interactive mode** — surface the script's output to the user and ask once: *"This change will deploy to {env list}. Confirm or amend."* Don't proceed past step 3 with an unconfirmed env list — getting it wrong silently leaves environments unmonitored.
- **Auto mode** (signal: a `system-reminder` mentions auto mode is active, or the agent is operating without a human-in-the-loop) — proceed with the script's output + tier-default below, and **log the assumption explicitly in the rendered plan section**: *"Assumption (auto mode): targeted {env list} based on tier={tier}; user did not confirm at plan-write time."* Auto mode is the user's explicit instruction to proceed; respect it.

Defaults when env detection is ambiguous:
- Low-risk / hotfix → prod-only.
- Medium-risk → staging + prod.
- High-risk → all available envs (staging + prod + any regions / tenants the deploy system fans out to).

### 4. Probe telemetry tools and pick one default

Run `bash plan-rollout/scripts/probe_telemetry_tools.sh`. The script prints `PRIMARY=<name>`, `PRIMARY_VERIFIED=<yes|no>` (whether the queryable endpoint actually responded), `AVAILABLE=<list>`, and warnings about push-only OTLP endpoints (which are configured but not queryable). Pick the script's `PRIMARY` unless you have a clear reason to override (see "Overriding the script's pick" below).

The priority order encoded in the script:

**For backend-service targets** (default — when the repo has Go / Rust / Python / etc. backend code):

1. **Datadog** (`Datadog:*` MCP tools or `DD_API_KEY` + `DD_APP_KEY` env vars). Note: `DD_APP_KEY` is required for the *query* path — `DD_API_KEY` alone is ingest-only.
2. **Honeycomb** (`Honeycomb:*` MCP tools, `HONEYCOMB_API_KEY` env, or `hccli` / `honeycomb` CLI).
3. **Axiom** (`Axiom:*` MCP tools, `AXIOM_TOKEN` env, or `axiom` CLI).
4. **Grafana stack** (Tempo + Loki + Prometheus/Mimir as one tier — picked when ≥2 of the three are queryable). Read [references/tempo.md](references/tempo.md) for traces, [references/loki.md](references/loki.md) for logs, [references/prometheus.md](references/prometheus.md) for metrics (also covers Mimir).
5. **Prometheus alone** if Grafana stack tier didn't trigger but Prometheus is queryable.
6. **CloudWatch** (AWS credentials configured + `aws sts get-caller-identity` succeeds).
7. **http-poll** (last-resort fallback; uses `kind: shell` indicators).

**For static-site / front-end-only targets** (heuristic: package.json has Next/Astro/Remix/Nuxt/SvelteKit AND no `go.mod`/`Cargo.toml`/`pyproject.toml`/`cmd/`/`*.go` at root): the script *demotes* the metrics-backend tier and prefers platform-native CLIs:

1. **vercel-cli** (`vercel whoami` returns a logged-in user) — read [references/vercel-telemetry.md](references/vercel-telemetry.md) for `vercel logs`, `vercel inspect`, `vercel analytics` query patterns.
2. **netlify-cli** (`netlify status` returns OK).
3. **wrangler-cli** (`wrangler whoami` returns OK) for Cloudflare Pages.
4. **http-poll**.

Why the demotion: general-purpose metrics backends (Datadog, Prometheus, Tempo) cover server-side services. Even when reachable from the user's machine, they almost certainly don't have telemetry for a static site — the script's "is the endpoint queryable" check is necessary but not sufficient evidence that a tool covers the deploy target. Picking Prometheus for a marketing-site deploy sends the executor down a rabbit hole looking for metrics that don't exist.

#### Overriding the script's pick

The script can detect tool reachability but not whether a tool's data covers the deploy target. Override `PRIMARY` to `http-poll` (or to a platform CLI) when context contradicts the script's pick:

- **The deploy target's telemetry isn't in the picked backend.** E.g. the script picks Prometheus because the user's machine reaches the org's product Prometheus, but the deploy is a marketing site whose data lives in PostHog/Vercel Analytics, not Prometheus. → Override to `vercel-cli` (if Vercel-hosted) or `http-poll`.
- **A log drain is configured.** E.g. Vercel → Datadog log drain means Datadog *does* have the deploy target's logs even though it's a static site. → If the user confirms a drain exists, keep the script's metrics-backend pick. If the user is unsure, ask: *"I see Datadog is available — do you have a Vercel→Datadog log drain configured for this project? If yes I'll use Datadog; otherwise I'll fall back to vercel-cli."*
- **The script's PRIMARY_VERIFIED=no.** Env-presence-only detection (Datadog / Honeycomb / Axiom / CloudWatch). Try a single sentinel query before committing; if it fails with auth or not-found, fall back.

Push-only OTLP endpoints (e.g. `OTEL_EXPORTER_OTLP_ENDPOINT` set but no Prometheus/Tempo/Loki queryable) are surfaced as warnings — telemetry is being sent somewhere reachable, just not by us. Tell the user explicitly so they can either configure a queryable surface or accept that we'll fall back to `http-poll`.

Do not list every available tool to the user as equal options — pick the priority winner (or your contextual override), mention the alternatives in passing if the primary is somehow inadequate. Default-with-escape-hatch beats decision paralysis.

Then read the corresponding `references/<source>.md` for that primary tool's query syntax and example indicator queries. Use the `Server:tool_name` format when referencing MCP tools (e.g. `Datadog:query_metrics`, `Grafana:query_logs`, not the legacy `mcp__datadog__query_metrics`).

#### Auth-required MCP servers

When the agent's MCP tool list includes a server whose tools return `requires_authentication` (e.g. an OAuth-gated server like Firetiger MCP, or a freshly-installed Datadog MCP that hasn't completed its OAuth flow), surface a one-line user prompt:

> "The {server-name} MCP server is registered but not authenticated. Run the OAuth flow now, or skip this source?"

If the user declines or skips, drop that source from the priority list and re-pick `PRIMARY` from what's left. Do not silently fail telemetry queries against an unauth'd source — the executor would mark every indicator `INCONCLUSIVE` for the wrong reason.

### 5. Pick the checkpoint schedule from the tier

Read [references/checkpoint-schedule.md](references/checkpoint-schedule.md). Use the tier→schedule mapping there verbatim. Do not invent new schedules unless the user explicitly overrides — the schedule shape is calibrated against production data and ad-hoc tweaks are rarely better.

### 6. Pick indicators

Read [references/indicator-design.md](references/indicator-design.md). Required minimum:
- At least one indicator per applicable golden signal (latency, traffic, errors, saturation) on each affected service.
- At least one **intended-effect** indicator (the thing this change is *supposed* to move). Mark its `direction` as `intended-up` or `intended-down`.
- At least one **business-outcome** indicator if one exists for the affected surface. If you can't infer one, ask the user (see step 10).

For each indicator capture:
- `name` — short, kebab-case.
- `kind` — `ratio` (preferred — good_events / total_events) or `gauge` (only when no honest denominator exists, e.g. queue depth, p95 latency value).
- `source` — exact query string for the primary telemetry tool (`Datadog:query_metrics` payload, Prom expression, Honeycomb breakdown, etc.).
- `direction` — `intended-up | intended-down | unintended-watch`.
- `per-env vs shared` — if the indicator is identical across envs (golden signals on the same service, with `service:my-svc` filter), mark *shared, applies to all*. If it differs (e.g. business KPI is region-specific), nest under the env. See [references/multi-env.md](references/multi-env.md).

### 7. Query the 24h baseline per env per indicator

Run each indicator's query right now against the last 24 hours, per environment. Capture the actual value (e.g. *baseline 0.18% over last 24h, p99 7.2 minutes ago*). The baseline value is what makes the threshold meaningful.

If the telemetry tool is unreachable for an indicator, flag it as `baseline-pending` rather than dropping the indicator silently — the executor will treat a missing baseline as `INCONCLUSIVE` and the user can fill it in before the executor runs.

Then express the threshold *relative to the baseline*, not as an absolute number:
- *"+30% vs baseline over a 5-minute window"* — good.
- *"alert at >1% error rate"* — bad (no context for what's normal).

### 8. Pick the deploy-detection recipe per env

Read the matching `references/<deploy-system>.md`. Copy the exact poll command into the plan's `Deploy detection` block for that environment. The command must:
- Take no interactive input.
- Print machine-parseable output (JSON or a single-line key=value).
- Match on the merge SHA (or its ancestor — see ArgoCD / canary recipes).

If the user uses multiple deploy systems (e.g. GH Actions for staging, ArgoCD for prod), give each environment its own command.

### 9. Pick the rollback hint

One line. Specific. The exact thing the user (or their on-call) will do if the executor reports `ISSUE_DETECTED`. Examples:
- *"Revert PR #1234 and redeploy via GH Actions deploy.yml."*
- *"Roll back ArgoCD app `my-svc-prod` to revision `abc123` (the previous synced rev)."*
- *"Flip feature flag `new-checkout-flow` to off in LaunchDarkly."*

This is the MTTR lever. Do not skip it. If you genuinely cannot infer one, ask the user (step 10) — never write a vague rollback hint.

### 10. Ask the user about ambiguities

**Behaviour by mode:**

- **Interactive mode** — use [assets/ambiguity-questions.md](assets/ambiguity-questions.md) for the canonical wording. Hard rule: never proceed past step 10 on a `high`-tier change with unresolved ambiguity. Common ambiguities:
  - *"Multiple telemetry tools are available — which is canonical for service X?"* (only ask if the priority order from step 4 was inconclusive.)
  - *"What counts as a 'good' request — 2xx only, or 2xx+3xx? Should auth-required 401s count?"*
  - *"Is this change behind a feature flag? If so, what fraction is the rollout?"*
  - *"What's the rollback procedure?"* (only if you couldn't infer it.)
  - *"Default monitoring window for this tier is N — increase or decrease?"*

- **Auto mode** (signal: `system-reminder` mentions auto mode is active) — do **not** ask. Use the tier-defaults and log each skipped question as an explicit assumption in the rendered plan section, e.g. *"Assumption (auto mode): treated 2xx as 'good' requests; treated feature flag as fully rolled out; rollback is 'revert PR + redeploy via deploy.yml'; window matches tier-default."* Auto mode is the user's explicit instruction to proceed without blocking; respect it. The user can review the assumptions in the rendered plan and edit before invoking monitor-rollout.

### 11. Render the plan section + companion check

Run `bash plan-rollout/scripts/render_plan_section.sh` with the gathered fields piped on stdin as JSON. By default it writes the rendered plan to `.rollout/<branch-slug>-monitoring-plan.md` (relative to the git root) and prints the absolute path on stdout's last line. Override the destination with `--out <path>` or `--out -` for stdout.

The conventional location matters: `monitor-rollout`, when invoked without a plan-path argument, auto-discovers `.rollout/*-monitoring-plan.md` in the current repo. Stick to the convention unless the user has an explicit reason to override.

Then run `bash plan-rollout/scripts/check_companion.sh`. If `monitor-rollout` is not installed, print its install hint verbatim. The plan is useless without the executor.

End plan-rollout's response with the activation hand-off line, quoting the absolute path the script printed:

```
After the change merges and the deploy is triggered, run:
  /monitor-rollout <absolute path printed by render_plan_section.sh>
in this same session to monitor it.
```

The umbrella `rollout` skill greps for the absolute path on the last line of plan-rollout's output to thread it into the chained `/monitor-rollout` invocation when the user asked for the full lifecycle.

## Worked examples

- [examples/low-risk-bugfix.md](../examples/low-risk-bugfix.md) — single-env, two early checkpoints.
- [examples/medium-risk-api-change.md](../examples/medium-risk-api-change.md) — staging + prod, golden signals + intended-effect.
- [examples/high-risk-db-migration.md](../examples/high-risk-db-migration.md) — staging + prod, full schedule including +24h and +72h.
- [examples/high-risk-infra-change.md](../examples/high-risk-infra-change.md) — infra, full schedule.
- [examples/multi-region-rollout.md](../examples/multi-region-rollout.md) — four regions fanned out via ArgoCD `ApplicationSet`.

## Anti-rationalizations

Common shortcuts the agent is tempted to take, paired with why they're wrong here. If you catch yourself reaching for one, course-correct.

| Tempting shortcut | Why it's wrong |
|-------------------|----------------|
| *"This change looks small, I'll skip the risk-tier rubric."* | The rubric drives the checkpoint schedule and whether ambiguity questions are required. Skipping it produces a plan that's either over- or under-scoped. Spend the 10 seconds on step 2. |
| *"Generic 'monitor error rate' alerting is good enough; no need to query baselines."* | Without a baseline, the threshold has no context. A 1% error-rate alert is fine for checkout but constant noise for an email-bounce ingester. The executor's evidence-discipline gate will mark thresholds with no baseline as `INCONCLUSIVE` — the indicator becomes useless. |
| *"I'll skip the intended-effect indicator — golden signals cover regressions and that's the main risk."* | A change that ships and doesn't move the metric it was *supposed* to move is a different kind of failure. Silent unless you watch for it. Required, not optional. |
| *"The user can figure out the rollback path under pressure."* | MTTR is the dominant lever in incident impact (SRE book ch. 13). Asking on-call to invent a rollback at 3am is exactly when the plan should have already named one. One line, written when you're calm. |
| *"Multiple telemetry tools are available, I'll list them all and let the user pick."* | Decision paralysis. Default-with-escape-hatch beats menu-of-options. The priority order in step 4 exists for this; pick one and note alternatives only in passing. |
| *"This deploys to one region today, I'll skip the env enumeration."* | The plan must enumerate explicitly, even when the answer is one. The `enumerate_envs.sh` script also surfaces fan-out cases the user may have forgotten (matrix jobs, ApplicationSet generators, Vercel preview targets). |
| *"This is a high-risk change but the user is in a hurry — I'll skip the ambiguity questions."* | Hard rule (interactive mode): never proceed past step 10 on a high-tier change with unresolved ambiguity. A wrong plan run by the executor wastes the +10m checkpoint and shifts blame later. The questions are the cheapest part of the workflow. **Auto-mode exception:** in auto mode, log the assumptions in the rendered plan instead of asking — the user reviews the plan before invoking monitor-rollout. |
| *"I'll just ask the user even though we're in auto mode."* | Auto mode is the user's explicit instruction to proceed without blocking. Asking stalls the workflow and ignores the explicit signal. Use tier-defaults, log every skipped question as an assumption in the plan, and let the user audit at review time. |

## Limits

If the user asks one of these limit-questions, read [references/limitations.md](references/limitations.md):
- "Can this run while I'm offline / when my session ends?"
- "How does my team see what's being monitored?"
- "Can it learn from past deploys?"
- "Can I auto-rollback?"
- "Why can't I fix two regressions in parallel?"

## What this skill does NOT do

- Does not run the monitoring itself — that's `monitor-rollout`.
- Does not promise to detect every possible regression. The plan is anchored on *this* change's failure modes.
- Does not write generic "monitor everything" plans. Generic alerting is upstream of change control.
- Does not file issues or modify CI. The plan is a markdown section the executor reads.
