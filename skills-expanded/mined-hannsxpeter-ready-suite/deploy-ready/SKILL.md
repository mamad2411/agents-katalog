---
name: deploy-ready
description: "Ship an app from a known-green build into real user-facing environments safely, repeatably, and reversibly. Triggers on 'deploy this,' 'CI/CD pipeline,' 'promote to staging,' 'zero-downtime migration,' 'expand-contract,' 'rollback,' 'canary,' 'blue/green,' 'progressive rollout,' 'first deploy,' 'environment parity,' 'promote through Actions,' 'GitOps,' 'promote the same artifact,' or any request to move code from pre-prod to prod. Enforces same-artifact promotion, expand/contract as a multi-deploy calendar, code-vs-data rollback asymmetry, and paper-canary detection. Does not pick IaC tools (stack-ready), wire observability (observe-ready), or manage secrets vaults (security). Pairs with observe-ready. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: shipping
upstream:
  - production-ready
  - stack-ready
  - repo-ready
downstream:
  - observe-ready
pairs_with:
  - observe-ready
  - launch-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Deploy Ready

This skill exists to solve one specific failure mode. A build that is green on the developer's laptop, green on CI, and green in every unit test, and then collapses the moment it meets a real environment. The migration locks the orders table for an hour. The canary routes 5% of traffic and nobody is watching the metric that would have caught the regression. The rollback plan is a wiki page that was last tested two years ago. The first deploy to the new region fails because the IAM role does not exist and nobody noticed because `terraform plan` had no opinion about runtime. The second version of the code ships while the first version is still on one box, and a reused feature flag wakes up dormant code that takes the company down. These are not code bugs. They are shipping-mechanics bugs, and the tooling that exists today has no opinion about any of them.

The job here is the opposite. Produce a deploy plan that marks, per change, whether it is reversible; that decomposes a schema migration into a multi-deploy calendar rather than a single cutover; that refuses to call something a canary unless there is a metric, a threshold, and a rollback trigger; and that treats the first deploy to any new environment as a distinct failure surface from subsequent deploys to the same one. If a deploy cannot answer "what rolls back if this fails and how long does that take," it is not ready to ship.

This is harder than it sounds because deploy is a *system* layered on top of a system. A single production deploy touches the build, the artifact registry, the environment variables, the secrets path, the DNS, the certificates, the database schema, the cache layer, the rolling-update algorithm, the load balancer, the feature flag evaluator, the canary router, and the rollback strategy. If any one layer is papered over, the whole deploy collapses into a cosmetic green checkmark with a real outage behind it.

## Core principle: what rolls back is code, not data

Do not design deploys as if rollback is a uniform "undo button." The moment a migration writes to or restructures data, that data is forward. Reverting the code does not revert the data. Deploy-ready's load-bearing discipline is:

> Every change is classified as reversible (code-only) or data-forward (schema or data mutation). Reversible changes get a rollback plan. Data-forward changes get a compensating-forward plan plus a restore point, and never a "rollback" bullet that pretends to undo the data.

This principle is non-negotiable. An AI-generated deploy plan that writes "rollback: redeploy previous image" next to a schema migration is a deploy-plan bug, not a deploy plan. Every "rollback" step in the plan must be proven reachable from the post-deploy state, not assumed.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Picking the deploy tool itself** ("should I use Fly.io or Render," "Terraform vs. Pulumi," "Argo CD vs. Flux"). That is `stack-ready`. Deploy-ready assumes the tool choice exists.
- **Observability** ("add Datadog," "set up Sentry," "define an SLO," "write a runbook"). That is `observe-ready`. Deploy-ready refuses to emit a canary without metrics and names the boundary explicitly; it does not wire the metrics itself.
- **Repo hygiene** ("add CI for lint and test," "write CONTRIBUTING.md," "set up branch protection," "configure CODEOWNERS"). That is `repo-ready`. Deploy-ready reads CI *outputs* (test-green status) and adds deploy stages on top; it does not own the lint/test/build layer.
- **Secrets management** ("set up a vault," "rotate these keys," "audit who read this secret"). That is security territory. Deploy-ready owns only the *injection path* from whatever vault is present to the running process (no secrets in image layers, no committed `.env`, no `pull_request_target` on untrusted forks).
- **App wiring** ("build the users page," "wire the dashboard to the API," "add RBAC"). That is `production-ready`. Deploy-ready reads `.production-ready/STATE.md` to know what to ship; it does not change the app.
- **Cost optimization or performance tuning** ("this Lambda is too expensive," "reduce bundle size"). Route to cloud-provider docs or a future scale-ready.
- **Launch marketing** ("landing page," "SEO," "Product Hunt post"). That is `launch-ready`.
- **Greenfield infrastructure choice** ("what region should I pick," "Kubernetes or ECS"). That is `stack-ready`'s hosting/deploy dimension.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a deploy that passes validate and fails at the environment boundary.

### Step 0. Detect project and deploy state

Read `references/deploy-research.md` and run the mode detection protocol.

- **Mode A (First deploy to an environment)**: the target environment does not yet exist, or the app has never successfully shipped to it. First deploys fail differently; run the `first-deploy-checklist.md` cold-start gate before anything else.
- **Mode B (Subsequent deploy)**: the pipeline has shipped to this environment before. Focus is on the change-class classification, migration phase, and rollback plan.
- **Mode C (Incident / rollback)**: production is currently broken or a ship just went wrong. Skip to Step 11 (rollback or compensating-forward).
- **Mode D (Pipeline construction)**: the user is building the CI/CD pipeline itself, not shipping a specific change. Focus on Steps 3 and 4; Steps 5 through 10 run as a dry walkthrough against a representative change.
- **Mode E (Migration-dominated)**: the change set is primarily a schema or data migration. Step 6 moves to the front; the deploy calendar is the plan.

**Passes when:** a mode is declared, and the corresponding research output block from `deploy-research.md` is produced.

### Step 1. Pre-flight

Read `references/preflight-and-gating.md`. Answer the 10 pre-flight questions in writing:

1. **What is shipping.** The change set in one sentence, with a link to the build, PR, or STATE.md entry.
2. **Build provenance.** Where does the artifact come from? Same commit, same build, or rebuilt per environment? If rebuilt, that is an immediate drift hazard.
3. **Target environments.** The full promotion path (e.g., `preview -> staging -> canary -> prod`), not just the terminal environment.
4. **Topology.** Static, container, serverless, long-running service, edge, or mixed? (See `deployment-topologies.md`.)
5. **Data-layer involvement.** Does this change touch schema or data? If yes, Step 6 is mandatory.
6. **Stateful side effects.** Does this change send emails, process payments, trigger webhooks, or mutate third-party state that has no rollback?
7. **Blast radius.** If this ships wrong, what is the worst single-step outcome? Who is affected? How many users?
8. **Rollback path.** For the reversible portion, what is the exact command or action that reverts? Has it been run recently against a non-prod copy?
9. **Feature flag lineage.** Are any flag names in this change reused from a prior deploy? (Knight Capital lesson. See `rollback-playbook.md` for the flag-reuse check.)
10. **Approval posture.** Who must approve promotion to prod? Where is the gate configured? Is the gate enforced by the pipeline or only by convention?

If the request is vague ("deploy this to prod"), do not interrogate the user. Pick plausible defaults (same-artifact promotion, standard promotion path for the detected topology, code-only change if no migration is in the diff), state them in one paragraph as assumptions, and proceed.

**Passes when:** all 10 questions answered in writing, assumptions stated for any gaps, and the change-class (reversible vs. data-forward vs. mixed) is declared in question 5.

### Step 2. Topology and environment map

Produce a short note (6 to 15 lines) covering:

- **Topology.** One of: static, container, serverless function, long-running service, edge/worker, scheduled job, mixed. Reference `deployment-topologies.md` for the picker and the per-topology first-deploy hazards.
- **Environments.** Named list with their purpose. Typical: `dev`, `preview` (per-PR), `staging`, `canary`, `prod`. Mark which are persistent and which are ephemeral.
- **Artifact type.** Docker image, static bundle, serverless package, deb/rpm, compiled binary, or framework-native build output.
- **Artifact path.** Where it is built, where it is stored, how it moves between environments. This is the same-artifact invariant in writing. The invariant applies to *logical* environments (dev, staging, canary, prod). Platform-native region replication or per-region image rebuilds (Fly.io, Cloud Run, Vercel edge) are not drift if the source commit and build configuration are pinned; record the pin in the artifact path note.
- **Promotion hierarchy.** The ordered path from build to prod. Every step named. If the promotion ladder is compact (dev -> prod only, or dev -> preview -> prod), declare it as a **compact ladder** and document the parity compensations in Step 3. The skill does not force a staging rung where one does not exist; it forces the parity gap to be visible.
- **Runtime dependencies.** Secrets, env vars, DNS entries, certs, IAM roles, database connectivity, cache layer, queue, third-party APIs. Each marked "exists in target" or "must be provisioned."

**Mode B (subsequent) shortcut:** quote the note from the last successful deploy and mark only the delta.

**Passes when:** every bullet has a concrete answer. Any "must be provisioned" item goes into the first-deploy checklist.

### Step 3. Environment promotion hierarchy

Read `references/environment-parity.md`. Define the promotion ladder and the *differences* between rungs.

For each environment, state:

- **Traffic source.** Real users, synthetic, engineers only, or nobody.
- **Data source.** Same DB as prod, branched copy, synthetic, seeded, or empty.
- **Scale.** Same as prod, scaled-down, single-instance, or ephemeral.
- **Feature-flag defaults.** On, off, or mixed. Which flags diverge from prod?
- **Observability reach.** Does `observe-ready` (or equivalent) get telemetry from this env? If no, this env cannot be a canary.

The three 12-factor parity gaps (time, personnel, tooling) apply; the fourth, **fidelity**, is deploy-ready's addition: what about the environment is deliberately lower-fidelity than prod, and what is that lie costing you?

**Passes when:** the ladder is named in order; every rung has all five bullets answered; every gap between rungs is an explicit note, not a silent drift.

### Step 4. Pipeline design

Read `references/pipeline-patterns.md`. The pipeline is not the tool. The pipeline is the set of *gates* the change must pass.

Required gate list, in order:

1. **Build.** Deterministic, hermetic, pinned. Output is a single named artifact with a content hash.
2. **Test.** Green from `repo-ready` territory. Deploy-ready does not add tests here; it fails if tests did not pass.
3. **Security.** Image scan, dependency audit, secret scan on the artifact itself (not just the source). See `secrets-injection.md` for the per-topology scan list.
4. **Promote to first non-prod env.** Same-artifact. Smoke-check the deployment, not just the HTTP 200.
5. **Promote to staging.** Same-artifact. Run the pre-deploy checklist for staging.
6. **Approval gate.** Explicit, named, enforced by the pipeline (environment protection rule, approval step), not by convention. **Solo-dev exception:** on single-maintainer projects, the approval is a distinct second action the maintainer performs (push a signed tag, invoke the deploy command, merge a deploy-marker commit) separate from the build step. A pipeline that auto-deploys on push to main with no distinct second action does not clear this gate even for solo projects; the whole point of the gate is that shipping is a choice, not a side effect of committing.
7. **Promote to prod.** Same-artifact. Rollout per Step 7.
8. **Post-deploy verification.** Step 11.

Anti-patterns to reject in this step (each covered in `pipeline-patterns.md`):

- A single job that builds, tests, and deploys to prod on push to main.
- Per-environment rebuilds of the artifact.
- `pull_request_target` with checkout of untrusted fork code and secret access ([timescale/pgai was the cautionary case](https://github.com/timescale/pgai/security/advisories/GHSA-89qq-hgvp-x37m)).
- Approval gates that any push can bypass.
- Secrets stored as workflow file literals.
- Deploy credentials scoped to a PAT on someone's personal account.

**Passes when:** each of the 8 gates is named in the pipeline, the same-artifact promotion is verifiable (the content hash at the final promote matches the hash at build), and the approval gate is enforced by a protection rule, not a comment convention.

### Step 5. Change-class classification

For each distinct change in the ship, classify it:

| Class | Definition | Requires |
|---|---|---|
| **Reversible** | Code-only. Bytes, config, feature-flag default. Reverting the artifact is the full undo. | Rollback plan with the revert command and a time-to-revert estimate. |
| **Data-forward** | Schema migration, backfill, or data mutation that cannot be undone by reverting the code. | Compensating-forward plan, pre-migration restore point, expand/contract decomposition (Step 6). |
| **Mixed** | Reversible code paired with data-forward migration. | Both of the above, plus a named sequencing order (expand phase ships first, code ships after, contract ships later; see Step 6). |
| **Side-effectful** | External state mutation with no undo (email send, payment capture, webhook emission). | Idempotency guard (so a retry does not duplicate), and explicit acknowledgement that "rollback" does not recall the emails that went out. |

**Passes when:** every change in the ship appears in the table with its class, and the required artifacts for that class are produced (or referenced).

### Step 6. Migration plan (the expand/contract calendar)

Read `references/zero-downtime-migrations.md`. If any change is data-forward or mixed, this step is mandatory and non-negotiable.

**The output is not one migration. It is a deploy calendar.**

For every schema change, decompose into phases:

1. **Expand.** Additive only. New column nullable. New table unreferenced. New index created `CONCURRENTLY`. Old readers and writers continue to work unchanged.
2. **Migrate.** Dual-write or backfill in batches. Both old and new structures in use. The code tolerates reading either shape.
3. **Cutover.** Reads and writes shift to the new structure. Old is still present but unused.
4. **Contract.** Only after *every* running code version has moved, remove the old structure in a separate deploy.

Each phase is its own deploy. The contract phase ships at a later calendar point; it never rides the same deploy as the expand phase.

**Expand-only-by-design.** Some changes are legitimately expand-only: adding a permanently-nullable audit column, adding a new enum value that will never be removed, adding a new table that coexists forever with its predecessor. In that case the calendar entry is explicit: "expand: v1.12.0 (2026-04-22). contract: none, by design. reason: <one line>." An absent contract phase is only a trap when it was deferred and forgotten; it is not a trap when it was designed out. The STATE.md in-progress cycles block must still record this so future agents do not re-invent a contract step that was never intended.

Guardrails applied to any proposed migration (catch list, not exhaustive, see `zero-downtime-migrations.md` for the full list):

- No `ALTER COLUMN` type change on a populated table without the expand-migrate-cutover-contract decomposition.
- No `NOT NULL` added to a populated column in a single step; use the add-nullable, backfill, `CHECK NOT VALID`, validate, `SET NOT NULL` sequence.
- No `CREATE INDEX` without `CONCURRENTLY` on a non-empty table.
- No rename of a column still being read by any running version of the app (deploy the read of the new name behind a dual-read before dropping the old).
- No backfill inside the same transaction as the schema change.
- No migration without an explicit `lock_timeout` and `statement_timeout` in the session.
- No destructive DDL (`DROP TABLE`, `DROP COLUMN`, `TRUNCATE`) without a documented pre-drop restore point and a minimum one-deploy-cycle gap since the last read.

**Passes when:** every data-forward change has a named phase, the deploy calendar has the correct number of entries (expand and contract are not the same ship), and every guardrail above has a pass or a named exception with justification.

### Step 7. Rollout plan (progressive delivery and the paper-canary rule)

Read `references/progressive-delivery.md`. Pick one rollout strategy per change, per environment.

Options:

- **All-at-once.** The simplest. Ship to 100% of the target at one time. Acceptable for: small staging fleets, isolated internal tools, hotfixes to config where the alternative is worse, and low-traffic prod services where the blast radius is explicitly bounded (named user count under threshold, internal-only audience, or solo-maintained app). Not acceptable for broad user-facing changes without a named blast-radius justification recorded in the plan.
- **Rolling update.** The default for long-running services. New pods roll in, old pods roll out, readiness probes gate the rollover. Requires a truthful readiness probe (not a 200 as soon as the HTTP server binds).
- **Blue/green.** Two parallel fleets, traffic shift at the load balancer. Faster rollback; double the capacity during the cutover.
- **Canary.** Percentage of traffic routed to the new version, with a *defined success metric, threshold, window, and automated rollback action*.
- **Ring deployment.** Staged cohorts (internal employees, then beta customers, then geographic regions, then all). Preferred for anything that pushes to endpoint devices.

**The paper-canary rule.** A canary without all four of the following is not a canary. It is a paper canary. Refuse to call it one.

| Required | Example |
|---|---|
| **Named success metric** | p99 error rate; 5xx rate; p95 latency; conversion rate on the critical path. |
| **Threshold** | Numeric. "error rate < 0.5%" or "p95 latency < 300ms." |
| **Window** | Time-bounded. "15 minutes" or "1000 requests per region." |
| **Automated rollback trigger** | If the threshold is breached in the window, the canary router reverts traffic without a human click. |

If any of the four is missing *and* `observe-ready` is not installed to provide the metric path, the canary is cosmetic. Do not ship a canary. Pick all-at-once (if the blast radius permits) or stop and install the observability first.

**Blast-radius rule.** No change ships to 100% of the fleet in one step if the change is untested in that environment. CrowdStrike, Cloudflare 2019, and Facebook 2021 are the same shape. A uniform rollout of an untested change is a deploy plan bug.

**Passes when:** the rollout strategy is named per change; canaries meet all four paper-canary criteria; no change goes 0-to-100 in a single uniform step unless explicitly justified in one sentence.

### Step 8. Secrets-injection audit

Read `references/secrets-injection.md`. Deploy-ready does not opinion on where secrets live; it opinions on the path from vault to runtime.

Audit list:

- **No secrets in image layers.** Docker `COPY . /app` is a catch-all landmine. Grep the artifact for known-bad patterns (`.env`, `aws_secret`, `sk_live_`, `ghp_`, RSA key headers) before push.
- **No secrets in git.** Run a secret scan against the diff of this ship.
- **No secrets in workflow literals.** Secrets come from the CI provider's secret store, scoped to the environment, not pasted into YAML.
- **No untrusted-fork secret exposure.** `pull_request_target` or equivalent must not check out fork code with secret access. Environment protection rules must be on.
- **Secrets are injected as env vars or mounted files at runtime.** Not baked. Not layered. Not dumped to logs.
- **Runtime identity is least-privileged.** The deploy identity that ships the artifact is not the same identity the app uses at runtime. The app's runtime role has only the permissions the app needs.

**Passes when:** each audit item has a pass or a named exception. No secret lands in the image, the git history, or the workflow literals.

### Step 9. Pre-deploy checklist

Read `references/first-deploy-checklist.md` (Mode A) or the subsequent-deploy section of `preflight-and-gating.md` (Mode B).

The Mode A cold-start gates (every one a hard block):

- Target environment exists and is reachable.
- DNS record(s) created and propagated.
- TLS certificate(s) provisioned and not expiring in under 30 days.
- Database provisioned, migrations applied up through the expand phase.
- Env vars set in the platform (not just in the code). Vercel/Netlify-class gotcha: env vars added after the deployment are `undefined` until redeploy.
- IAM / runtime role exists with least-privileged permissions.
- Image pushed to the target registry; pull credentials valid from the target runtime.
- Healthcheck endpoint returns a meaningful signal (not just 200 on bind).
- Log aggregation reaches this env (or an explicit "we are shipping without logs" exception).
- Rollback path exists and has been dry-run at least once in a non-prod environment.

The Mode B subsequent-deploy checklist is shorter: the environment exists, the change-class is classified, migrations are in the right phase, canary criteria are met, and the last deploy is known-green.

**Passes when:** the correct checklist is walked end-to-end; every item is green or has a named, justified exception.

### Step 10. Ship

Execute the pipeline. Watch the rollout live. Do not declare done until the post-deploy checks have passed.

During the ship:

- **Watch the canary metric directly**, not just the pipeline status. A green pipeline with a breached canary is a failed deploy.
- **Do not bypass the approval gate.** If the gate is failing because the approver is asleep, fix the process. Do not merge the approval step into the prior one.
- **Do not run ad-hoc fixes into prod mid-rollout.** If something is wrong, trigger rollback (Step 11) or pause the rollout; fix the plan, then re-ship.

**Passes when:** the artifact is running in prod at the target traffic percentage, the canary metric is within threshold for the full window, and the approval gate was honored.

### Step 11. Post-deploy and rollback discipline

Read `references/rollback-playbook.md`.

**Post-deploy checklist (happy path):**

- Healthcheck returns healthy from every prod instance.
- p99 latency and error rate are within the canary threshold for at least 15 minutes.
- A smoke run through the critical path (login, one mutation, one read) succeeds.
- Alerts from `observe-ready` (if present) fire correctly against synthetic fault injection.
- If the ship included an expand phase, the follow-up contract phase is scheduled on the calendar, not forgotten.

**Rollback path (unhappy path):**

- Code-only change: revert the artifact. Time to revert: seconds to minutes.
- Data-forward change: **rollback is not the plan.** Execute the compensating-forward. The compensating-forward was written in Step 6; now is when you ship it.
- Mixed change: revert the code to the last version that tolerates *both* schemas. This is why expand-contract is a multi-deploy calendar: the interstitial code versions must be valid rollback targets.
- Side-effectful change: acknowledge what is not recoverable. If emails went out, they went out. Communicate to affected users; do not pretend the rollback undoes them.

**Post-incident:**

- Every rollback, or every close call, writes a `.deploy-ready/incidents/NNN-slug.md` entry. Date, what broke, what recovered it, what to change in the deploy plan so this shape does not recur. Do not skip this on the grounds that the outage was brief; the pattern matters more than the blast radius.
- Update the rollback playbook if a step in the recovery did not match what was written.

**Passes when:** the ship is green in prod with the checks above, or the ship failed and a rollback / compensating-forward was executed and recorded, or the ship is still in progress but the rollout state is visible and monitored.

## Completion tiers

20 requirements across 4 tiers. Aim for the highest tier the session allows. Declare each tier explicitly at its boundary.

### Tier 1: Pipelined (5)

The app builds deterministically and ships to at least one non-prod environment through a named pipeline.

| # | Requirement |
|---|---|
| 1 | **Deterministic build.** A single hermetic build produces a single artifact with a content hash. |
| 2 | **At least one non-prod environment exists** (preview, staging, or both) and receives the artifact through the pipeline, not manual upload. |
| 3 | **Same-artifact promotion declared.** The pipeline does not rebuild per environment. The content hash at promote matches the hash at build. |
| 4 | **Test and security gates pass before any deploy.** `repo-ready` territory is green. Image scan and secret scan run on the artifact. |
| 5 | **Healthcheck endpoint is truthful.** Readiness returns healthy only when the app can actually serve requests, not just when the port is bound. |

### Tier 2: Promotable (5)

The pipeline promotes from staging to prod with an enforced gate. The first prod deploy has succeeded.

| # | Requirement |
|---|---|
| 6 | **Promotion hierarchy named.** Every rung from build to prod is named, with parity gaps documented per `environment-parity.md`. |
| 7 | **Approval gate enforced.** Prod promotion requires an explicit, named, pipeline-enforced approval. Not a wiki convention. |
| 8 | **First-deploy checklist walked.** Every cold-start gate from `first-deploy-checklist.md` is green or has a justified exception. |
| 9 | **Secrets-injection audit green.** No secrets in image layers, git history, workflow literals, or untrusted-fork checkout paths. |
| 10 | **Pipeline-as-code is version-controlled.** Changes to the pipeline go through the same review as changes to the app. |

### Tier 3: Reversible (5)

Every change has a classified rollback or compensating-forward path. Migrations are disciplined.

| # | Requirement |
|---|---|
| 11 | **Every change classified.** Reversible, data-forward, mixed, or side-effectful per Step 5. No unclassified change ships. |
| 12 | **Rollback path rehearsed.** For reversible changes, the revert command has been run against a non-prod copy within the last 90 days. |
| 13 | **Expand/contract decomposed.** Every data-forward change has a named expand phase, cutover phase, and contract phase on the deploy calendar, or is explicitly marked expand-only-by-design with a one-line reason. Expand and contract are never the same ship. |
| 14 | **Migration guardrails pass.** No destructive DDL without a restore point, no `NOT NULL` in one step, no non-concurrent index on a live table, no rename-then-read, no in-transaction backfill, no missing `lock_timeout`. |
| 15 | **Feature-flag lineage checked.** No flag name is reused from a prior deploy without an audit that the old code path is fully removed (Knight Capital lesson). |

### Tier 4: Hardened (5)

Progressive delivery is real. Blast-radius limits exist. Canaries are not paper.

| # | Requirement |
|---|---|
| 16 | **Rollout strategy is explicit per change.** Rolling, blue/green, canary, or ring. No silent 0-to-100 uniform pushes to prod. |
| 17 | **Canaries meet the four-field rule.** Named metric, threshold, window, automated rollback trigger. Or the strategy is not called a canary. |
| 18 | **Observability path exists.** `observe-ready` (or equivalent) emits the canary metric and can trigger rollback. If absent, no canary is claimed. |
| 19 | **Post-deploy incident log maintained.** Every rollback or close call is recorded in `.deploy-ready/incidents/`. Patterns inform the next deploy plan, not just individual incidents. |
| 20 | **First deploy distinguished from subsequent.** The plan explicitly calls out which Mode (A or B) it is in; first-deploy cold-start gates are not skipped on the assumption "the environment is just like the other one." |

**Proof test:** a new engineer reads `.deploy-ready/PLAN.md` (or the live session's plan output), can name the rollback path for every change in the ship, can point at the canary metric, and can walk the deploy calendar across the expand/contract cycle without opening any additional files.

## The "have-nots": things that disqualify the deploy at any tier

If any of these appear, the deploy fails this skill's contract and must be fixed:

- A "rollback plan" bullet on a data-forward migration with no compensating-forward written.
- A canary with no named metric, no threshold, no window, or no rollback trigger.
- A pipeline that rebuilds the artifact per environment.
- A pipeline that pushes to prod on every push to main with no gate.
- An approval gate enforced by convention ("ping someone in Slack") rather than by the pipeline's environment protection rule.
- Secrets baked into a Docker image layer (grep finds them in the artifact, not just the source).
- Secrets in workflow YAML literals.
- `pull_request_target` or equivalent that checks out untrusted fork code with secret access.
- A migration that takes an `ACCESS EXCLUSIVE` lock on a populated table, including: `ALTER COLUMN` type change, `NOT NULL` default in one step, `CREATE INDEX` without `CONCURRENTLY`, or a backfill inside the schema-change transaction.
- A rename of a column that the currently-running code still reads.
- A `DROP TABLE`, `DROP COLUMN`, `TRUNCATE`, or other destructive DDL without a documented restore point and a minimum one-deploy-cycle gap since the last read.
- A feature-flag name reused from a prior deploy without a check that the old code path is removed.
- A readiness probe that returns 200 on socket bind rather than on "I can serve a real request."
- A first-deploy cold-start that assumes env vars, DNS, certs, IAM, or the registry exist in the target without verifying.
- A rollout that goes from 0% to 100% of the fleet in a single uniform step.
- A rollback path that has never been tested against a non-prod copy.
- A destructive deploy-time command run against prod (including `terraform destroy`, `kubectl delete`, `prisma migrate reset`, `rm -rf`) without an explicit confirmation step and a known backup. AI-agent deploy failures (Replit, DataTalks.Club) are all variants of this.
- A canary step named in the plan but implemented as "we'll watch Grafana for a bit." That is not a canary. It is a paper canary.
- Any reference to a rollback as "just redeploy the previous version" for a change that touched data.

When you catch yourself about to write any of these, fix it before proceeding. A broken deploy plan is worse than no plan; the team will ship it and discover the bug in prod.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `deploy-research.md` | **Always.** Start of every session (Step 0). | ~6K |
| `preflight-and-gating.md` | **Always.** Step 1 pre-flight and Step 9 subsequent-deploy checklist. | ~7K |
| `deployment-topologies.md` | **Tier 1.** Step 2; the picker and per-topology first-deploy hazards. | ~10K |
| `pipeline-patterns.md` | **Tier 1.** Step 4; CI/CD patterns and anti-patterns. | ~11K |
| `environment-parity.md` | **Tier 2.** Step 3; the ladder, the four parity gaps, drift audit. | ~7K |
| `first-deploy-checklist.md` | **Mode A.** Step 9 cold-start gate. | ~6K |
| `zero-downtime-migrations.md` | **Tier 3.** Step 6; expand/contract calendar, guardrails, famous footguns. | ~14K |
| `rollback-playbook.md` | **Tier 3.** Step 11; code-vs-data asymmetry, compensating-forward, flag lineage. | ~9K |
| `progressive-delivery.md` | **Tier 4.** Step 7; canary, blue/green, ring, the paper-canary rule. | ~10K |
| `secrets-injection.md` | **Tier 2.** Step 8; path from vault to runtime, per-topology audit. | ~7K |
| `RESEARCH-2026-04.md` | **On demand.** Source citations behind the guardrails and incident examples. | ~30K |
| `deploy-antipatterns.md` | **Every cutover + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Loaded at every cutover plan review. | ~5K |

Skill version and change history live in `CHANGELOG.md`. When resuming a project, confirm the skill version your session loaded matches the version recorded in `.deploy-ready/STATE.md`. A skill update between sessions may change guardrail lists (new migration footguns, new CI supply-chain patterns) or tier requirements. If versions differ, re-read the changed sections before continuing the ship.

## Suite membership

deploy-ready is the shipping-tier skill that owns the pre-prod-to-prod handoff. See `SUITE.md` at the repo root for the full map. The relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (this skill, ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. Install what you need.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill falls back to its own defaults.

| If present | deploy-ready reads it during | To pre-fill |
|---|---|---|
| `.production-ready/STATE.md` | Step 1 (pre-flight) and Step 2 (topology note) | Current tier, stack, last known-green build, open questions blocking work, audit-log schema. A non-green STATE.md blocks the ship. |
| `.production-ready/adr/*.md` | Step 2 and Step 6 | Architectural decisions that affect deploy: chosen DB, auth, session store, migration style. |
| `.production-ready/deferred-cta.md` | Step 1 | Block the first prod deploy while any entry is `deferred` or `in-progress`. Half-wired CTAs do not ship. |
| `.stack-ready/DECISION.md` | Step 2 (topology note) | Hosting, database, ORM, language/runtime. Do not re-decide; quote. |
| `repo-ready` CI outputs | Step 4 (pipeline design) | Build, lint, test, security scan jobs are present and green. Deploy-ready adds deploy stages on top; it does not re-author the test stage. |

If an upstream artifact *contradicts* the code or the target environment, trust the code and the environment, and note the drift. Upstream artifacts are historical records, not current-state overrides.

## Produces for downstream

deploy-ready emits the following artifacts for downstream skills and for the next deploy session to consume. Writing these is part of the skill's definition of done.

| Artifact | Path | Consumed by |
|---|---|---|
| **Deploy state** | `.deploy-ready/STATE.md` | Next deploy session reads to know the last shipped version, environment, and any in-progress expand/contract cycle. |
| **Deploy plan** | `.deploy-ready/PLAN.md` (current ship) | The ship itself; also the audit trail for the next incident review. |
| **Topology and environment map** | `.deploy-ready/TOPOLOGY.md` | `observe-ready` reads to know what to monitor and at what granularity. `launch-ready` reads to know what the public URLs are. |
| **Healthcheck endpoints list** | `.deploy-ready/healthchecks.md` | `observe-ready` reads to wire synthetic checks and SLOs. |
| **Rollback playbook** | `.deploy-ready/rollback.md` (per service) | Incident response reads in the middle of the night. |
| **Incident log** | `.deploy-ready/incidents/NNN-slug.md` | `observe-ready` reads to tune alert thresholds against actual incident shapes. Next deploy session reads to avoid repeating patterns. |
| **Expand/contract calendar** | `.deploy-ready/migrations/calendar.md` | Next deploy session reads to know which contract phases are due. Prevents the expand-only migration trap. |

If any downstream skill is not installed, deploy-ready still produces these artifacts. They cost nothing to emit and make the suite extensible: install `observe-ready` later and it already has everything it needs.

## Handoff: observability is not this skill's job

If the work needs metrics, logs, traces, SLOs, alert rules, dashboards, or runbooks, delegate to `observe-ready`. The two skills compose: deploy-ready owns the shipping mechanics; observe-ready owns what the system tells you after it is live. Do not duplicate either.

The tight coupling: a canary in deploy-ready requires a metric from observe-ready. If observe-ready is not installed, deploy-ready refuses to emit canaries and says so explicitly. This is not graceful degradation of the canary; it is correct refusal. A paper canary is worse than an all-at-once rollout because it looks like a safety mechanism and is not one.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke `observe-ready` directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user: "This step needs `observe-ready`. Install it or handle the observability layer separately." Do not attempt to generate Datadog dashboards or Sentry alert rules inline from this skill.

## Session state and handoff

Ship cycles span sessions: expand phase today, cutover next week, contract the week after. Without a state file, every resume rediscovers the calendar from scratch, and expand-only migration traps accumulate silently.

Maintain `.deploy-ready/STATE.md` at every deploy boundary. Read it first on resume. If it conflicts with the running system, trust the running system and update the file.

**Template:**

```markdown
# Deploy-Ready State

## Skill version
Built under deploy-ready [current skill version], [frontmatter updated date]. If the agent loads a newer version on resume, re-read the changed sections before the next ship.

## Environments in play
| Env | Purpose | Last ship | Current version | Health |
|---|---|---|---|---|
| preview | per-PR | continuous | HEAD of PR | green |
| staging | integration | 2026-04-21 | v1.12.3 | green |
| prod | customers | 2026-04-20 | v1.12.2 | green |

## Active pipelines
- Build: GitHub Actions workflow `build.yml`, hermetic, content-hashed.
- Promote: environment protection on `staging` and `prod`, approvals required from @team-infra.
- Rollout: rolling update on Fly.io, 30% per wave, healthcheck-gated.

## In-progress expand/contract cycles
- **users.avatar_url column rename.** Expand shipped 2026-04-15 (v1.11.7). Code shifted 2026-04-18 (v1.12.0). Contract scheduled for v1.13.0 (week of 2026-04-29). Do not ship contract until confirmed every running version is v1.12.0 or later.

## Rollback paths by service
- `api`: `flyctl releases rollback <id>`. Time to revert: ~90s. Last rehearsed: 2026-03-18 against staging.
- `worker`: same.
- `db`: forward-only. Restore point: nightly snapshot + WAL.

## Incidents logged
- 2026-04-02 (001-dns-propagation.md). Cert was fine; DNS TTL was 24h on the old record.
- 2026-03-11 (002-silent-migration-lock.md). `ALTER TABLE` on orders took an ACCESS EXCLUSIVE for 47 min; incoming writes queued; fix: repeat in expand/contract form.

## Open questions blocking the next deploy
- [open, target: v1.13.0] Contract can't ship until the mobile app client is on 4.3.x (count at 78% today). Blocks: the column contract step. Owner: @mobile-team.

## Last session note
[2026-04-22] Planned v1.12.3 patch ship. Expand/contract cycle noted above still in-progress.
```

**Rules:**
- STATE.md is the contract with the next session. If it is out of date, the next session will ship a contract phase too early or skip a cold-start gate.
- At every `/compact`, `/clear`, or context reset, update STATE.md first.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- The in-progress expand/contract cycles block is load-bearing. An expand phase shipped and then forgotten is the `expand-only migration trap`, and the trap compounds across future migrations until paid off.

## Keep going until it is actually shipped

The change landing on main is roughly 30% of the work. The remaining 70% is the classification, the migration phase decomposition, the pipeline gates, the first-deploy cold-start walk, the canary criteria, the rollback rehearsal, and the contract-phase scheduling. Budget for all of it.

A "deployed" change is one a real user can hit, a real operator can roll back, and a real future session can reconcile against the STATE.md without guessing. When in doubt, simulate the failure. The first thing that does not have a clean answer to "what happens if this breaks right now" is the next thing to write down.
