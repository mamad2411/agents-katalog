---
name: workflow-scan
description: "Durable workflows and sagas: determinism, versioning, activity config, compensation — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: workflow-scan

## Premise

A durable workflow engine re-runs workflow code from the top, every time a worker picks the execution back up, and expects the same commands in the same order: Temporal replays the history, Azure Durable Functions replays the orchestrator, Restate replays the journal, DBOS re-runs the workflow function and reuses step outputs. Code that reads the clock, a random source, the environment or the network outside the engine's own APIs answers differently on replay, and a deploy that reorders a workflow's commands breaks every execution still open. Around the replay sit the defaults nobody wrote down: a Temporal activity retries **without limit** unless told otherwise (WK6), a Step Functions Task waits about 3.2 years before it times out (WK9), a BullMQ flow parent waits forever on a child that failed (BQ8), a Zeebe job that times out is handed to another worker while the first still runs (Camunda 8.10 docs). And the saga built on top, by an engine or by hand, can skip a compensation, run them in the wrong order, swallow the error, compensate on a cancelled context, or refund twice. Each of these fails late — on a replay, a deploy, or the failure path nobody ran. This skill finds them and proves each with its oracle. Read-only: it never edits code and never contacts an engine that is not a local dev server or a scratch container.

**The trap this skill exists to avoid is the one the pack's own agent fell into.** In the TypeScript SDK `Date.now()`, `new Date()`, `Math.random()` and `setTimeout()` are **replaced by the workflow sandbox** with deterministic versions (WK1): they are not findings (precedent 25). The same tokens are violations in Go, Java and .NET, and in Python only with the sandbox off. A token list that is not keyed by SDK is wrong on the SDK most repos use. Likewise, an activity with neither Start-To-Close nor Schedule-To-Close is **rejected when it is scheduled** (WK6) — a loud failure, not "stuck forever"; the silent hazard is the unlimited default retry on an activity that is not idempotent.

It owns `/ds-audit`'s Workflows (§1–§3) and Sagas (§4–§6) ledger rows. `@workflow-orchestrator` (this pack) judges its rows.

**Every finding cites the workflow, activity or saga `<file:line>` + the engine and its version (F1) + the event it breaks under (a replay, a deploy with open executions, a retry, a timeout after the effect, a cancellation, a crash mid-saga) + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row its verdict rests on (WK1–WK14, BQ8) or the dated doc this skill cites where no row exists yet + the oracle that showed it, or the test that would settle it + the fix in the engine's own primitive** (`workflow.Now`, `patched()`, a retry policy, `NewDisconnectedContext`, the project's saga helper). A grep hit is a candidate. "Workflows look deterministic" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) (§ 25–27 workflows and sagas). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V320–V322.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them.

1. **Part A holds: this is workflow code, an activity's options, or a saga step**, registered with a worker or engine a deployed process starts (F3, gate 1). F2 scopes every § 1 token to workflow files: the same `time.Now()` inside an activity is correct. A Go helper that takes `context.Context` in a workflow package is an activity (the grep fallback's known false positive; `workflowcheck` resolves it). A `catch` that releases a lock or a cooldown window is not a saga.
2. **Part B holds at the installed SDK version** (F1, gate 3): the token is a hazard **for that SDK** (the § 1 table), the default is the row's (WK6 unlimited attempts, WK9 `TimeoutSeconds`), and nothing in the engine replaces it (the TS sandbox, Python's sandbox, a journaled `ctx.date.now()`). A version not found makes a version-gated row Unconfirmed with the probe written out.
3. **Nothing already controls it**, across files: a worker's `ignoreModules` or sandbox setting, a retry policy in a shared options constant, an idempotency key built from the workflow id, a version gate (`patched`, `GetVersion`), worker or deployment versioning, an immutable-deployment platform (Restate), a replay test in CI (F3), the Java `Saga` defaults (precedent 27). Read the whole workflow file, its options module and the worker's registration.
4. **The oracle fired, or the fact is two-ended.** A tool exit (tier T: `workflowcheck`, a DURABLE analyzer), a replay of recorded histories, a time-skipping run or the saga failure matrix (tier C), or a static fact citing both ends (an option literal and the row it leaves at its default). Without one, the row is `[report-flagged]` / Unconfirmed with the settling test written out. A unit test that mocks every activity proves nothing about replay or timeouts.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **Retry layering and deadlines**: an activity's retry policy is one layer of `retry-deadline-scan`'s § 4 worksheet; a Start-To-Close longer than the workflow's business deadline is its § 8 (this pack). The activity's **own** options — no cap on a non-idempotent effect, no non-retryable types, no heartbeat — are §3 here (`retry-deadline-scan` § Boundaries agrees).
- **Lost update and write skew mid-saga** (SG-4: an absolute `SET qty = :n` computed in app code while compensations run) → database `transaction-scan` § 8 (V5), § 7 for an integrity invariant, when the database pack is installed, with the saga context cited. Without it: reported here tagged `saga isolation (owner pack not installed)`.
- **Money, stock and credit compensations** (a refund that can run twice) → security `logic-race-scan` § 4, when the security pack is installed: §6 hands the row over with the replay mechanism as evidence. Without it: reported here tagged `money compensation (owner pack not installed)`. A business state machine that lets a user skip a step is security § 3 — not a durable workflow.
- **Queue consumers that are not workflow steps** (a BullMQ worker's `attempts`, stalls and locks) → `messaging-scan` (this pack). §3 here owns only the **flow** shape (BQ8). **Job payload drift inside one service** across deploys is the backend pack's class (BJ-04 in the batch-5 eval); Temporal histories and engine journals are §2 here.
- **Step Functions**: the Lambda a Task invokes and its own timeout chain → infrastructure `serverless-reliability-scan` § 1 (V282), when installed. The Task's `TimeoutSeconds` / `HeartbeatSeconds` stay §3 here: no infrastructure § owns them.
- **Event-sourced process managers and their event schemas** → `event-contract-scan` (this pack). **Locks and leader keys** a workflow takes → `coordination-scan` (this pack). **Runtime state** — stuck sagas, open executions, history sizes — → `/audit-distributed-tx` (the runtime lane), and `temporal workflow show` only under `--live`.

## Adapt to the codebase — the engine lanes

Read every engine **with its version** (F1). Facts are rows of `broker-semantics.md` (tagged `[V]`/`[K]`/`[K?]` and dated there); a row tagged `[K?]` makes its verdict Unconfirmed until the settling test runs. Three engines have no row yet: their facts below were read at the named docs on 2026-10-14 for this skill (integrator request: add them as WK rows).

| Engine | Workflow files (F2) | Replay or re-run rule | Version gate for open executions (§2) | Rows · tool lane |
|---|---|---|---|---|
| **Temporal** TS · Go · Java · Python · .NET | value import of `@temporalio/workflow` · `func(ctx workflow.Context` · `@WorkflowImpl` / `implements …Workflow` · `@workflow.defn` · `[Workflow]` | full history replay; the § 1 table per SDK | `patched` / `deprecatePatch` (TS, Python `workflow.patched`), `GetVersion` (Go), `Workflow.getVersion` (Java), `Workflow.Patched` (.NET); or worker versioning | WK1–WK7, WK11 · `workflowcheck -show-pos ./...` (Go, v0.6.0); replayers `Worker.runReplayHistories`, `WorkflowReplayer`, `Replayer` (Go and .NET API names [K?]) |
| **Azure Durable** Functions / Task (.NET isolated, JS, Python, Java, Go) | `[OrchestrationTrigger]`, `TaskOrchestrator<>`, `df.app.orchestration(`, `orchestration_trigger` | orchestrator replay; JS and Python orchestrators must be **generators**, never `async` | side-by-side deploy or the SDK's orchestration versioning ([K?] per SDK) | WK8 · `Microsoft.DurableTask.Analyzers` 1.26.0, DURABLE0001–0006 + 0011 as errors; Go `orchestratorvet` [K?] |
| **Restate** | `restate.service(` / `object(` / `workflow(` | journal replay; side effects in `ctx.run`, `ctx.rand`, `ctx.date.now()` | **immutable deployments**: an invocation stays on the deployment it started on; updating a deployment in place breaks open invocations (journal mismatch RT0016) — docs.restate.dev *Versioning*, read 2026-10-14 | WK10, WK12 |
| **DBOS** | `DBOS.registerWorkflow(`, `@DBOS.workflow(` | re-run from the top, completed steps reused; non-determinism goes in steps; a mismatch throws `DBOSStepNondeterminismError` | recovery only for workflows whose **application version** matches (a hash of the workflow source by default); `DBOS.patch()` with `enablePatching` — docs.dbos.dev *Workflows*, *Upgrading workflow code*, read 2026-10-14 | WK13 |
| **Inngest** | `.createFunction({ id: …` | code outside `step.run` re-runs on every resume | step ids and their order stay stable for in-flight runs | WK10 |
| **AWS Step Functions** | ASL (`"StartAt"`), CDK `StateMachine`, Terraform `aws_sfn_state_machine`, Serverless `stepFunctions:` | no workflow code to replay; Task states call workers | the worker's input contract (read) | WK9 |
| **Camunda 8 / Zeebe** | `createWorker({ taskType`, `@JobWorker` | job delivery is **at least once**: a job that times out returns to the backlog and can run on two workers at once; handlers must be idempotent; retries at 0 raise an incident — docs.camunda.io 8.10 *Job workers*, read 2026-10-14 | the worker's variables contract (read) | WK14 |
| **BullMQ flows** | `FlowProducer` | parent completes only when children do | — | BQ8 |
| **Sagas** — Temporal Java `Saga`, Eventuate Tram, MassTransit state machines and Courier, NestJS `@Saga()`, hand-rolled try/catch compensations | `addCompensation(`, `.withCompensation(`, `compensations.push(`, `@Saga()`, `MassTransitStateMachine<`, `IExecuteActivity<` | — | — | WK11 · V322 |

### The § 1 token table — keyed by SDK (WK1–WK5, WK8, WK10)

| SDK | Hazards in **workflow** code | Not hazards (decoys the grep must stay silent on) |
|---|---|---|
| Temporal **TypeScript** | Node or I/O imports in the workflow bundle (`fs`, `http`, `axios`, `pg`, `@aws-sdk/*`, …) · `process.env` · `crypto.randomUUID()` · a value import of an activity implementation · business branching on `workflowInfo().unsafe.isReplaying` · `fetch(` · `setInterval(` | `Date.now()`, `new Date()`, `Math.random()`, `setTimeout()` — sandbox-deterministic (precedent 25) · `import type * as acts` · `sleep()` · `uuid4()` from the workflow package |
| Temporal **Go** | `time.Now`, `time.Sleep`, global `math/rand`, `crypto/rand.Reader`, `os.Stdin/Stdout/Stderr`, goroutines, native channels and `select`, **map range** (all via `workflowcheck`; it misses global-variable mutation) | `workflow.Now`, `workflow.Sleep`, `workflow.Go`, `workflow.NewSelector`, `workflow.SideEffect` |
| Temporal **Java** | `System.currentTimeMillis`, `Instant.now`, `new Random`, `UUID.randomUUID`, `Thread.sleep`, threads and executors, `CompletableFuture`, `synchronized`, mutable statics | `Workflow.currentTimeMillis`, `Workflow.newRandom`, `Workflow.randomUUID`, `Workflow.sleep`, `Async.function` |
| Temporal **Python** | with the sandbox **off** (`UnsandboxedWorkflowRunner`, `sandboxed=False`) or in a passed-through module: `datetime.now`, `random.*`, `uuid.uuid4`, `time.sleep`, threads, HTTP clients, `os.environ`, `open(` — with it on, most raise at first run (a loud failure, medium) | `workflow.now()`, `workflow.random()`, `workflow.uuid4()`, `asyncio.sleep` / `gather` on workflow coroutines (durable, WK4) |
| Temporal **.NET** | `DateTime.Now/UtcNow`, `Guid.NewGuid`, `new Random`, `Task.Run`, `Task.Delay`, `Task.WhenAny/WhenAll`, `Thread.Sleep`, `ConfigureAwait(false)`, timeout `CancellationTokenSource` | `Workflow.UtcNow`, `Workflow.DelayAsync`, `Workflow.WhenAnyAsync`, `Workflow.NewGuid` |
| **Durable** (.NET, JS, Python) | DURABLE0001–0006 (time, `Guid.NewGuid`, delays, threads, direct I/O, environment) · 0011 `while (true)` with no ContinueAsNew · an `async` JS or Python orchestrator · `.Result` on a durable task, or a deferred `Select(… CallActivityAsync …)` enumerated twice (each enumeration schedules new activities) | `context.CurrentUtcDateTime`, `context.NewGuid()`, `context.df.currentUtcDateTime`, `CreateTimer` · `await Task.WhenAll(tasks)` over `CallActivityAsync` tasks — the documented fan-out (Microsoft Learn *Durable orchestrator code constraints*, ms.date 2026-10-12, read 2026-10-14) |
| **Restate / DBOS / Inngest** | time, random, ids and reads **outside** `ctx.run` / a step / `step.run` | `ctx.date.now()`, `ctx.rand.*`; anything inside the step callback |

## Read the code — per workflow and saga, before any §

F2 lists the workflow files per engine and the saga files. For each, with the § each answer feeds:
- **Which worker registers it, which SDK and version, and is the sandbox on?** The worker's `workflowsPath` / `workflows=[…]`, its `ignoreModules` or `UnsandboxedWorkflowRunner`, the process type that starts it (F3) [§1].
- **What does the workflow read that the engine did not give it?** Follow imports from the workflow file: a shared util that reads the clock or env is a hazard in the workflow bundle and fine in an activity [§1].
- **Are executions open across a deploy, and how long do they live?** A 30-day billing loop, a human-approval wait, an entity workflow: every change to command order needs a gate, or worker versioning, or a drain. Is there a replay test over the previous release's histories (F3) [§2]?
- **For each activity call: what timeouts, what attempts, which errors are final, and is the effect idempotent?** Options come from the call, a shared options constant, or the SDK default (WK6). Does the activity charge, send or insert, and with what key — the workflow id plus the activity id, or nothing [§3]?
- **Does the workflow loop?** What bounds its history (WK7: 51,200 events / 50 MB on Temporal Cloud; self-hosted defaults [K?]), and where does it continue-as-new [§3]?
- **For a saga: list the forward steps in order and mark each compensatable, pivot or retriable.** Which steps have a compensation, when is it registered (before or after the call that can fail after its effect), in what order do compensations run, what does a failing compensation do, does the error reach the caller, and does each compensation tolerate "the forward step never ran" and running twice [§4–§6]?
- **Where is the saga's state?** An engine's history, a `saga_state` table updated with each local write, or process memory [§6].

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). F2 runs **before** the § greps: every § 1 grep runs only over F2's per-engine lists. Every `rg` names its path — `.` or `"${ROOTS[@]}"` — or reads it from a list through `xargs`; given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (`scripts/lint-rg-traps.sh`). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). Multi-line matches are piped through an `rg` that keeps the anchor line, so a count is a count of matches. Set `WF_BASE=<ref>` for a diff-scoped run (§2a).

```bash
ROOTS=(.)   # the code that defines workflows, activities and sagas: in a monorepo name the apps (ROOTS=(apps/api services/billing)); manifests, CI and state-machine files always search .
BASE="${WF_BASE:-}"   # diff-scoped run (§2): the base ref, e.g. origin/main; unset = whole repo
CB="${CONTRACT_BASE:-}"   # /ds-audit --contract-base=<dir>: a base tree mirroring repo-relative paths — §2a's base when BASE is unset (no git history)
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,go,cs}')
XB=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,generated,__generated__,vendor,target,bin,obj,.temporal}/**' -g '!**/*.d.ts' -g '!**/*.min.*' -g '!**/{docs,ai,.claude}/**')
X=("${XB[@]}" -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,migrations,seeders,seeds}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/{test_*,*_test}.{py,go}' -g '!**/*{Test,Tests,IT}.{java,kt,cs}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
T=$(mktemp -d "${TMPDIR:-/tmp}/wfs.XXXXXX"); trap 'rm -rf "$T"' EXIT   # lists live here; nothing is written into the repo
each() { tr '\n' '\0' < "$1" | xargs -0 -r "${@:2}"; }   # run an rg over the files a list names (bash 3.2: no mapfile)
# F1 workflow SDKs, engines and saga frameworks with their declared versions (gate 3: WK1-WK14, BQ8 are read at these); F1L the locked versions (pnpm, npm, yarn) — the lockfile wins over the range
rg -n --no-heading --pcre2 '"(?:@temporalio/[\w-]+|@restatedev/restate-sdk[\w-]*|@dbos-inc/dbos-sdk|inngest|@trigger\.dev/sdk|durable-functions|@aws-sdk/client-sfn|aws-cdk-lib|@camunda8/sdk|zeebe-node|bullmq|@nestjs/cqrs|@nestjs/workflows)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:@temporalio/[\w-]+|@restatedev/restate-sdk[\w-]*|@dbos-inc/dbos-sdk|inngest|@trigger\.dev/sdk|durable-functions|@aws-sdk/client-sfn|aws-cdk-lib|@camunda8/sdk|zeebe-node|bullmq|@nestjs/cqrs|@nestjs/workflows)@\d[\w.-]*|"node_modules/(?:@temporalio/[\w-]+|@restatedev/restate-sdk[\w-]*|@dbos-inc/dbos-sdk|inngest|@trigger\.dev/sdk|durable-functions|@aws-sdk/client-sfn|aws-cdk-lib|@camunda8/sdk|zeebe-node|bullmq|@nestjs/cqrs|@nestjs/workflows)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:@temporalio/[\w-]+|@restatedev/restate-sdk[\w-]*|@dbos-inc/dbos-sdk|inngest|@trigger\.dev/sdk|durable-functions|@aws-sdk/client-sfn|aws-cdk-lib|@camunda8/sdk|zeebe-node|bullmq|@nestjs/cqrs|@nestjs/workflows)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '\b(?:go\.temporal\.io/sdk|github\.com/microsoft/durabletask-go|github\.com/restatedev/sdk-go|temporalio|Temporalio[\w.]*|Microsoft\.DurableTask[\w.]*|Microsoft\.Azure\.(?:Functions\.Worker|WebJobs)\.Extensions\.DurableTask[\w.]*|azure-functions-durable|dbos(?:-transact)?|restate[_-]sdk|temporal-sdk|temporal-testing|eventuate-tram-sagas[\w-]*|MassTransit|axon-(?:messaging|legacy|modelling)|spring-zeebe[\w-]*|camunda[\w-]*|zeebe[\w-]*)\b' -g '**/{requirements*.txt,pyproject.toml,Pipfile,pom.xml,build.gradle,build.gradle.kts,*.csproj,Directory.Packages.props,go.mod}' -g '!**/node_modules/**' .
# F2 the workflow files, per engine (scoping is mandatory: the same tokens are correct inside activities and steps) — one list per lane, then wf.all
rg -l --pcre2 '^\s*import\s+(?!type\b)[^;]*?from\s+["\x27]@temporalio/workflow["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/wf.ts"
rg -l --pcre2 '\bfunc\s+\w+\s*\(\s*\w+\s+workflow\.Context\b' -g '*.go' "${X[@]}" "${ROOTS[@]}" > "$T/wf.go"
rg -l --pcre2 '@WorkflowImpl\b|\bimplements\s+\w*Workflow\b|\bWorkflow\.newActivityStub\(' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" > "$T/wf.java"
rg -l --pcre2 '@workflow\.defn\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" > "$T/wf.py"
rg -l --pcre2 '^\s*\[Workflow(?:\(|\])|\[OrchestrationTrigger\]|\bTaskOrchestrator<' -g '*.cs' "${X[@]}" "${ROOTS[@]}" > "$T/wf.cs"
rg -l --pcre2 '\bdf\.(?:orchestrator\(|app\.orchestration\()|\.orchestration_trigger\(|\bdf\.Orchestrator\.create\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/wf.durable"
rg -l --pcre2 '\brestate\.(?:service|object|workflow)\(|@DBOS\.workflow\(|\bDBOS\.registerWorkflow\(|\.createFunction\(\s*\{\s*id\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/wf.step"
rg -l --pcre2 '\baddCompensation\(|\bcompensations?\s*\.\s*(?:push|unshift)\(|\.withCompensation\(|@Saga\(\)|\bMassTransitStateMachine<|@(?:StartSaga|SagaEventHandler)\b|\bnew\s+Saga\(|\bIExecuteActivity<|\bFlowProducer\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/saga"
cat "$T"/wf.* | sort -u > "$T/wf.all"
for l in ts go java py cs durable step; do printf 'F2 %-8s %s\n' "$l" "$(wc -l < "$T/wf.$l" | tr -d ' ')"; done; echo "F2 sagas    $(wc -l < "$T/saga" | tr -d ' ')"; cat "$T/wf.all" "$T/saga"
rg -l --pcre2 '"StartAt"\s*:|^\s*StartAt\s*:|\bnew\s+(?:sfn|stepfunctions)\.StateMachine\(|\baws_sfn_state_machine\b|^\s*stepFunctions\s*:' -g '*.{json,yml,yaml,tf,ts,py}' "${XB[@]}" . > "$T/sfn"; echo "F2 step-functions $(wc -l < "$T/sfn" | tr -d ' ')"; cat "$T/sfn"
rg -n --no-heading --pcre2 '\.createWorker\(\s*\{[^\n]*\btaskType\b|\bcreateWorker\(\s*["\x27][\w-]+["\x27]|@JobWorker\b|\.newWorker\(\)\s*\.jobType\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# F3 the gates already in place (gate 4): replay tests and CI lines (tests INCLUDED), worker or deployment versioning, the sandbox switched off
rg -n --no-heading --pcre2 '\brunReplayHistor(?:y|ies)\(|\bWorkflowReplayer\b|\bReplayer\(\s*workflows|\bReplayWorkflowHistory\w*\(|\breplay_workflows?\(' "${CODE[@]}" "${XB[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bworkflowcheck\b|\borchestratorvet\b|\bdotnet_diagnostic\.DURABLE00\d\d|(?i:warnaserror|WarningsAsErrors)[^\n]*DURABLE' -g '*.{yml,yaml,json,toml,csproj,props,editorconfig,mk}' -g 'Makefile' -g '!**/node_modules/**' --hidden -g '!.git/**' .
rg -n --no-heading --pcre2 '\b(?:buildId|useVersioning|UseBuildIdForVersioning|versioningBehavior|VersioningBehavior|WorkerDeploymentVersion|deploymentOptions|DeploymentOptions|applicationVersion|enablePatching)\b|\bUnsandboxedWorkflowRunner\b|\bsandboxed\s*=\s*False\b|\bignoreModules\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 1 non-determinism, scoped to F2's lists. 1a TS (never Date.now/Math.random/setTimeout: WK1, precedent 25); 1b Python (severity rides on F3's sandbox line); 1c Go fallback; 1d Java; 1e .NET Temporal, then Durable (Task.WhenAll over durable tasks is the documented fan-out there; .Result on one is the hazard); 1f Durable JS/Python orchestrators that are async; 1g Restate/DBOS/Inngest tokens outside a step (read)
each "$T/wf.ts" rg -H -n --no-heading --pcre2 '^\s*import\s+(?!type\b)[^;]*?\s+from\s+["\x27](?:node:\w+|fs|path|os|http|https|net|tls|dns|child_process|crypto|worker_threads|axios|node-fetch|got|undici|pg|mysql2|mongodb|mongoose|ioredis|redis|@prisma/client|typeorm|knex|@mikro-orm/[\w-]+|@aws-sdk/[\w-]+|\.\.?/(?:[\w/-]*/)?activities(?:/[\w.-]+)?)["\x27]|\bprocess\.env\b|\bcrypto\.randomUUID\(|\bfetch\(|\.unsafe\.isReplaying\b|\bnew\s+WeakRef\(|\bsetInterval\(' | "${NC[@]}"
each "$T/wf.py" rg -H -n --no-heading --pcre2 '\bdatetime\.(?:now|utcnow|today)\(|\bdate\.today\(|\btime\.(?:time|time_ns|monotonic|sleep)\(|(?<![\w.])random\.\w+\(|\buuid\.uuid[14]\(|\bthreading\.|\b(?:requests|httpx|aiohttp|boto3)\.|\bos\.(?:environ|getenv)\b|(?<![\w.])open\(|\bsandboxed\s*=\s*False\b' | "${NC[@]}"
each "$T/wf.go" rg -H -n --no-heading --pcre2 '\btime\.(?:Now|Sleep|Since|Until|After|Tick|NewTimer|NewTicker)\(|^\s*go\s+[\w.(]|\bselect\s*\{|\b(?:math/)?rand\.\w+\(|\bos\.(?:Getenv|ReadFile|Stdout)\b|\bhttp\.(?:Get|Post|DefaultClient)\b|\bfor\s+[\w, ]+:=\s*range\s+\w*(?:[Mm]ap|By[A-Z]\w*|[Ii]ndex)\b' | "${NC[@]}"
each "$T/wf.java" rg -H -n --no-heading --pcre2 'System\.currentTimeMillis\(|System\.nanoTime\(|Instant\.now\(|LocalDate(?:Time)?\.now\(|new\s+Random\(|UUID\.randomUUID\(|Thread\.sleep\(|new\s+Thread\(|\bsynchronized\b|CompletableFuture|Executors?\.|System\.getenv\(' | "${NC[@]}"
each "$T/wf.cs" rg --files-without-match --pcre2 '\[OrchestrationTrigger\]|\bTaskOrchestrator<' | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 'DateTime(?:Offset)?\.(?:Now|UtcNow|Today)\b|Guid\.NewGuid\(|Task\.(?:Run|Delay|WhenAny|WhenAll|Factory\.StartNew)\(|Thread\.Sleep\(|ConfigureAwait\(\s*false\s*\)|new\s+Random\(|Environment\.GetEnvironmentVariable\(|new\s+HttpClient\(|Stopwatch\.' | "${NC[@]}"
each "$T/wf.cs" rg -l --pcre2 '\[OrchestrationTrigger\]|\bTaskOrchestrator<' | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 'DateTime(?:Offset)?\.(?:Now|UtcNow|Today)\b|Guid\.NewGuid\(|Task\.(?:Run|Delay|WhenAny|Factory\.StartNew)\(|Thread\.Sleep\(|ConfigureAwait\(\s*false\s*\)|new\s+Random\(|Environment\.GetEnvironmentVariable\(|new\s+HttpClient\(|Stopwatch\.|\.Result\b' | "${NC[@]}"
each "$T/wf.durable" rg -H -n --no-heading -U --pcre2 '\bdf\.orchestrator\(\s*async\b|\borchestration\(\s*["\x27][^"\x27]+["\x27]\s*,\s*async\b|\.orchestration_trigger\([^)]*\)\s*\n\s*async\s+def\b|\bnew\s+Date\(|\bDate\.now\(|\bMath\.random\(|\bdatetime\.(?:now|utcnow)\(' | rg --pcre2 'orchestrat\w*\(|async\s+def|Date|random|datetime'
each "$T/wf.step" rg -H -n --no-heading --pcre2 '\bDate\.now\(|\bnew\s+Date\(\s*\)|\bMath\.random\(|\bcrypto\.randomUUID\(|\bfetch\(|\bprocess\.env\b' | "${NC[@]}"
if [ -s "$T/wf.go" ]; then if command -v workflowcheck >/dev/null 2>&1; then rg --files -g 'go.mod' "${XB[@]}" . | while read -r m; do (cd "$(dirname "$m")" && workflowcheck -show-pos ./...); echo "workflowcheck $(dirname "$m") exit $?"; done; else echo "§1 Go: blocked (workflowcheck not installed — go install go.temporal.io/sdk/contrib/tools/workflowcheck@latest; v0.6.0 dated 2026-10-08)"; fi; fi
if [ -s "$T/wf.cs" ]; then rg -l 'Microsoft\.DurableTask\.Analyzers' -g '*.{csproj,props}' . || echo "§1 .NET Durable: no Microsoft.DurableTask.Analyzers reference — the T lane is: dotnet add package Microsoft.DurableTask.Analyzers (1.26.0), then dotnet build -warnaserror:DURABLE0001,DURABLE0002,DURABLE0003,DURABLE0004,DURABLE0005,DURABLE0006,DURABLE0011 in a scratch copy"; fi
# 2 versioning. 2a diff-scoped: workflow files changed since BASE (or differing from their CONTRACT_BASE copy), with the gate lines the change adds; 2b worker/deployment versioning changed in the diff; 2c whole repo: gate calls per workflow file
if [ -n "$BASE" ]; then git diff --name-only --diff-filter=MR "$BASE"...HEAD > "$T/chg"; sed 's#^\./##' "$T/wf.all" "$T/sfn" | rg -x -F -f - "$T/chg" > "$T/wfchg"; while read -r f; do echo "2a $f gate-lines-added=$(git diff -U0 "$BASE"...HEAD -- "$f" | rg -c --pcre2 '^\+.*\b(?:patched|deprecatePatch|GetVersion|getVersion|Patched|DeprecatePatch|deprecate_patch|DBOS\.patch)\(' || echo 0)"; done < "$T/wfchg"; git diff "$BASE"...HEAD | rg -n --pcre2 '^\+.*\b(?:buildId|useVersioning|versioningBehavior|VersioningBehavior|WorkerDeploymentVersion|deploymentOptions|applicationVersion)\b'; fi
if [ -z "$BASE" ] && [ -n "$CB" ]; then if [ -d "$CB" ]; then sed 's#^\./##' "$T/wf.all" "$T/sfn" | while read -r f; do [ -f "${CB%/}/$f" ] || continue; cmp -s "${CB%/}/$f" "$f" && continue; echo "2a $f (base: contract-base) gate-lines-added=$(diff "${CB%/}/$f" "$f" | rg -c --pcre2 '^>.*\b(?:patched|deprecatePatch|GetVersion|getVersion|Patched|DeprecatePatch|deprecate_patch|DBOS\.patch)\(' || echo 0)"; done; else echo "2a NOT-RUN (contract-base $CB is not a directory)"; fi; elif [ -z "$BASE" ] && [ -s "$T/wf.all" ]; then echo "2a NOT-RUN (no WF_BASE and no CONTRACT_BASE: which workflow files changed is unknown; 2c is a census, never a change list)"; fi
echo "2c version-gate calls per workflow file (absent = 0):"; each "$T/wf.all" rg -H -c --pcre2 '\b(?:patched|deprecatePatch|GetVersion|getVersion|Patched|DeprecatePatch|deprecate_patch)\(|\bDBOS\.patch\('
# 3 activity and engine configuration. 3a an activity with neither Start-To-Close nor Schedule-To-Close (rejected when scheduled, WK6 — not "stuck forever"); 3b options with no attempt cap (the default is unlimited, WK6) or an explicit 0;
#   3c activity files that never mark an error non-retryable; 3d heartbeat timeouts vs heartbeat calls; 3e an endless loop in a workflow file with no continue-as-new CALL (WK7, DURABLE0011)
rg -n --no-heading -U --pcre2 'proxyActivities(?:<[^>]*>)?\(\s*\{(?:(?!startToCloseTimeout|scheduleToCloseTimeout)[^{}]|\{[^{}]*\})*\}\s*\)|\bActivityOptions\s*\{(?:(?!StartToCloseTimeout|ScheduleToCloseTimeout)[^{}]|\{[^{}]*\})*\}|ActivityOptions\.newBuilder\(\)(?:(?!setStartToCloseTimeout|setScheduleToCloseTimeout)[^;])*;|\bexecute_activity(?:_method)?\((?:(?!start_to_close_timeout|schedule_to_close_timeout)[^()]|\([^()]*\))*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'proxyActivities|ActivityOptions|execute_activity'
rg -n --no-heading -U --pcre2 'proxyActivities(?:<[^>]*>)?\(\s*\{(?:(?!maximumAttempts)[^{}]|\{(?:(?!maximumAttempts)[^{}])*\})*\}\s*\)|\bActivityOptions\s*\{(?:(?!MaximumAttempts)[^{}]|\{(?:(?!MaximumAttempts)[^{}])*\})*\}|ActivityOptions\.newBuilder\(\)(?:(?!setMaximumAttempts|setRetryOptions)[^;])*;|\bexecute_activity(?:_method)?\((?:(?!retry_policy)[^()]|\([^()]*\))*\)|\b(?:maximumAttempts|MaximumAttempts|maximum_attempts)\s*[:=]\s*0\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'proxyActivities|ActivityOptions|execute_activity|[Mm]aximum_?[Aa]ttempts'
rg -l --pcre2 'from\s+["\x27]@temporalio/activity["\x27]|@activity\.defn\b|@ActivityInterface\b|@ActivityImpl\b|^\s*\[Activity\]|\bactivity\.(?:RecordHeartbeat|GetInfo|GetLogger)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/act"; echo "3c activity files $(wc -l < "$T/act" | tr -d ' ') · with no non-retryable marker:"; each "$T/act" rg --files-without-match --pcre2 '\bnonRetryable\b|\bnon_retryable\b|\bNonRetryable\w*|\bnonRetryableErrorTypes\b|\bdoNotRetry\b|\bNewNonRetryableApplicationError\('
echo "3d heartbeat timeouts:"; rg -n --no-heading --pcre2 '\b(?:heartbeatTimeout|HeartbeatTimeout|heartbeat_timeout|setHeartbeatTimeout)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; echo "3d heartbeat calls in activity files: $(each "$T/act" rg -c --pcre2 '\bContext\.current\(\)\.heartbeat\(|\bactivity\.(?:heartbeat|RecordHeartbeat)\(|\bActivityExecutionContext\.Current\.Heartbeat\(|(?<![\w.])heartbeat\(' | awk -F: '{s+=$NF} END {print s+0}')"
each "$T/wf.all" rg -l --pcre2 '\bwhile\s*\(\s*true\s*\)|\bwhile\s+True\s*:|^\s*for\s*\{\s*$|\bfor\s*\(\s*;\s*;\s*\)' > "$T/loop"; echo "3e endless loops with no continue-as-new call:"; each "$T/loop" rg --files-without-match --pcre2 '\bcontinueAsNew\s*(?:<[^>]*>)?\(|\bcontinue_as_new\(|\bNewContinueAsNewError\(|\bWorkflow\.continueAsNew\(|\bContinueAsNew\w*\(|\bCreateContinueAsNewException\b'
# 3f signal-then-poll-query (an Update belongs); 3g Step Functions Task states with no TimeoutSeconds (default 99,999,999 s, WK9); 3h BullMQ flows: children with no failure policy (parent waits forever, BQ8)
rg -n --no-heading -U --pcre2 '\.signal\([^)]*\)[\s\S]{0,400}?(?:while|for)\s*\([^)]*\)[\s\S]{0,200}?\.query\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.signal\('
each "$T/sfn" rg -H -n --no-heading -U --pcre2 '\{(?=(?:[^{}]|\{[^{}]*\})*"Type"\s*:\s*"Task")(?:(?!"TimeoutSeconds)[^{}]|\{[^{}]*\})*\}' | rg --pcre2 '"Type"\s*:\s*"Task"'
each "$T/saga" rg -H -n --no-heading -U --pcre2 '\{\s*name\s*:[^{}]*\bqueueName\s*:(?:(?!failParentOnFailure|ignoreDependencyOnFailure|removeDependencyOnFailure|continueParentOnFailure)[^{}]|\{(?:(?!failParentOnFailure|ignoreDependencyOnFailure|removeDependencyOnFailure|continueParentOnFailure)[^{}])*\})*\}' | rg --pcre2 'queueName' | uniq
# 4 missing compensation. 4a Eventuate participant step with no .withCompensation (not the last); 4b the pairing listing per saga file (forward calls vs registrations, for reading);
#   4c hand-rolled sagas: a catch that awaits an undo verb with an argument (no workflow engine needed) — file:line of the undo
rg -n --no-heading -U --pcre2 '\.step\(\)(?:\s|//[^\n]*)*\.invokeParticipant\((?:[^()]|\([^()]*\))*\)(?!(?:\s|//[^\n]*)*\.withCompensation)(?=(?:\s|//[^\n]*)*\.(?:step\(\)|build\(\)))' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | rg 'invokeParticipant'
each "$T/saga" rg -H -n --no-heading --pcre2 '^\s*(?:(?:const|let|var)\s+\w+\s*=\s*)?(?:await\s+|yield\s+)?(?:this\.)?\w+(?:\.\w+)?\([^;]*\)\s*;?\s*(?://.*)?$|compensations?\.(?:push|unshift)\(|\baddCompensation\(|\.withCompensation\(' | rg -v --pcre2 ':\d+:\s*(?:if|for|while|switch|return|function|export|import|throw|catch|\}|super)\b'
rg -n --no-heading -U --pcre2 '\bcatch\s*(?:\(\s*\w+(?:\s*:\s*\w+)?\s*\))?\s*\{(?:[^{}]|\{[^{}]*\})*?\bawait\s+(?:this\.)?[\w.]*\.(?:release|refund|revert|undo|cancel|void|reverse|unreserve|restore|compensate)\w*\(\s*[^)\s]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bawait\s+(?:this\.)?[\w.]*\.(?:release|refund|revert|undo|cancel|void|reverse|unreserve|restore|compensate)\w*\('
# 5 compensation order and context. 5a push + forward iteration with no reverse; 5b a catch that compensates and never rethrows; 5c Go compensation on the workflow ctx in a file with no disconnected ctx; 5d a registration on the line after the call it undoes — unless the next line calls the undo's own noun (`releaseX` then `allocateX`: registered before its own call, precedent 27)
each "$T/saga" rg -l 'compensations?\.push\(' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\.reverse\(\)|\.unshift\(|\btoReversed\(|\.length\s*-\s*1\s*;\s*\w+\s*>=\s*0' | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 'for\s*\(\s*(?:const|let)\s+\w+\s+of\s+compensations?\b|compensations?\.forEach\('
rg -n --no-heading -U --pcre2 '\bcatch\s*(?:\(\s*\w+(?:\s*:\s*\w+)?\s*\))?\s*\{(?:(?!\bthrow\b|\braise\b)[^{}]|\{(?:(?!\bthrow\b)[^{}])*\})*(?:\bcompensat\w*|\.(?:release|refund|revert|undo|unreserve)\w*\(\s*[^)\s])(?:(?!\bthrow\b|\braise\b)[^{}]|\{(?:(?!\bthrow\b)[^{}])*\})*\}' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bcatch\b'
each "$T/wf.go" rg --files-without-match 'NewDisconnectedContext' | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 'workflow\.ExecuteActivity\(\s*ctx\s*,\s*\w*(?:Refund|Cancel|Release|Revert|Undo|Compensat|Rollback)\w*'
each "$T/saga" rg -H -n --no-heading -U --pcre2 '^[^\n]*\b(?:await\s+)?(?:this\.)?\w+(?:\.\w+)?\([^\n;]*\)\s*;?[ \t]*(?://[^\n]*)?\n\s*(?:compensations?\.(?:push|unshift)|\w+\.addCompensation)\((?>(?:[^\n]*?(?:\.|::)[a-z]+([A-Z]\w*)\b)?)[^\n]*+(?!\n[ \t]*(?:(?:const|let|var|final|val)\s+\w+\s*=\s*)?(?:await\s+|yield\s+)?(?:this\.)?\w+(?:\.\w+)*\.[a-z]+\1\()' | rg --pcre2 'push\(|unshift\(|addCompensation\('
# 6 compensation state and idempotency. 6a in-memory sagas; 6b a persisted saga state anywhere (schemas included); 6c saga files whose undo calls carry no idempotency marker; 6d irreversible effects in saga files (read their position)
rg -n --no-heading --pcre2 '@Saga\(\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -i --pcre2 '\bsaga_?(?:state|instance|log|step)s?\b|\bprocess_?manager\b|\bSagaStateMachineInstance\b|\bISagaRepository\b|\bWorkflowStore\b' "${CODE[@]}" -g '*.{sql,prisma}' "${XB[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -20
each "$T/saga" rg -l --pcre2 '\b(?:refund|release|revert|cancel|void|reverse|unreserve)\w*\s*\(' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i:idempotency_?key|idempotency-key)|\bON\s+CONFLICT\b|\bsagaId\b|\bsaga_id\b|\bworkflowId\b|\bactivityId\b'
each "$T/saga" rg -H -n --no-heading --pcre2 '\b(?:send\w*(?:Email|Mail|Sms|Notification)|notify\w*|createShipment|ship\w*|publish\w*)\s*\(' | "${NC[@]}"
echo "pre-flight done (an rg exit 2 above is a failed grep, never zero hits)"
```

Reading the output:
- **F1 is the version gate**: each SDK with its source (a manifest range is marked `range`; its floor decides which rows apply). **F1L** prints the locked version: when it printed one, that is the version, not the range's floor (a package locked at two versions: the importer's entry in `pnpm-lock.yaml`, or `<app>/node_modules/<pkg>` in `package-lock.json`, says which one the app gets). No workflow SDK, engine file or saga shape anywhere → §1–§3 print `N/A (no workflow SDK)`, and §4–§6 still run on hand-rolled sagas (4c).
- **F2 is the subject list.** Every § 1 hit comes from a file F2 named for that engine; a token hit in an activity file is not printed at all. F2's Zeebe line lists the job workers for the §3 read.
- **F3 is the control list**: a replay test or a `workflowcheck` / DURABLE line in CI is the REPLAY GATE `/ds-audit` asks for; a worker-versioning or `applicationVersion` line answers §2 for every workflow on that worker; an `UnsandboxedWorkflowRunner` or `sandboxed=False` line raises 1b's severity.
- **1a–1g are candidates, never verdicts**: the § 1 table decides, by SDK. **2a** prints each changed workflow file with the gate lines the diff adds (`0` is the candidate; a file the diff **adds** is excluded — a new workflow type has no open executions); with no `WF_BASE` it compares each workflow file with its copy under `CONTRACT_BASE` (`/ds-audit --contract-base=<dir>`) — a file with no base copy is new or unchanged and is skipped — and with neither it prints `2a NOT-RUN`; **2c** prints gate calls per file. **3a–3h** are option shapes with the default each leaves (WK6, WK7, WK9, BQ8). **4b** prints each saga file's forward calls beside its registrations, in line order, for reading. **4c** is the only lane that needs no engine: a `catch` that awaits an undo verb with an argument.

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **Options built elsewhere.** `proxyActivities(defaultActivityOptions)` or a Go `ActivityOptions` from a constructor passes 3a and 3b silently. When F2 has workflow files and 3a/3b print nothing, open the options constant once.
- **A hand-rolled saga with no `catch`** — a `finally`, a `.catch(` callback, a state column flipped by a cleanup cron. 4c misses it; read each use case that makes two or more remote calls with effects when F1 shows no saga framework.
- **Go and .NET without their tools.** The Go grep fallback is name-based (map range needs types); print `§1 Go: blocked` and keep the fallback rows Unconfirmed until `workflowcheck` runs. The .NET Temporal SDK has no first-party analyzer (WK5): its rows rest on the grep and on a replay.

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples B (`wf/` 6 files across TS, Go, Java, Python, .NET Temporal and Durable; `saga/` 5) | 0.3 s, 0 rg errors. **Every BAD line surfaces in its §**: TS `axios` import, activity value import, `crypto.randomUUID`, `process.env`, `unsafe.isReplaying` (1a); Python `datetime.now`, `random`, `uuid4` and the unsandboxed runner (1b, F3); Go `time.Now`, a goroutine, a map range (1c); Java `currentTimeMillis`, `UUID.randomUUID`, `Thread.sleep`, `synchronized` (1d); .NET `DateTime.UtcNow`, `Task.Delay`, `Task.Run`, `Guid.NewGuid` and Durable `DateTime.UtcNow` (1e); a proxy with no timeout (3a); `while (true)` with `continueAsNew` imported but never called (3e); the Eventuate step with no compensation (4a); `push` + `for…of` (5a); compensations registered after the call (5d); Go `defer ExecuteActivity(ctx, Refund…)` (5c); NestJS `@Saga()` (6a). **Every decoy stays silent**: TS `Date.now()`, `import type`, `workflow.now()`, `asyncio.sleep`, `Workflow.currentTimeMillis`, `Workflow.UtcNow`, `Workflow.DelayAsync`, `context.CurrentUtcDateTime`, and the `unshift` saga in 5a |
| Seeded tree for engines the samples lack (18 files: Restate, DBOS, Inngest, Durable JS and Python, Step Functions, Zeebe, BullMQ flows, a hand-rolled TS saga, a Java `Saga`, a replay test, a scratch git repo for §2a) | Found: Restate `crypto.randomUUID`/`Date.now` outside `ctx.run`, DBOS `Date.now` and `fetch` outside a step, Inngest `Date.now` outside `step.run` (1g); an `async` Durable JS and Python orchestrator and `new Date()` in one (1f); a proxy and a Go `ActivityOptions{}` and a Python `execute_activity` with no timeout (3a); proxies with no attempt cap (3b); `heartbeatTimeout` with 0 heartbeat calls (3d); three endless loops (3e); signal-then-poll (3f); a Task with no `TimeoutSeconds` (3g); a flow child with no failure policy (3h); a catch that releases stock and swallows (4c, 5b); `addCompensation` after `withdraw` (5d); a changed workflow with 0 gate lines vs one with `patched` (2a). Silent: the generator orchestrator, `ctx.date.now()`, the timed Task, the `failParentOnFailure` child, a bounded loop that continues-as-new, an added workflow file (2a) |
| `benchmarks/fixtures/*` (18 fixtures) | 0 detector lines in all 18: F1 prints `bullmq` in 4 (brittle-suite, ci-defects, obs-defects, slow-marketplace); no workflow SDK, no `FlowProducer`, no saga shape, no state machine. Every § prints `N/A` or `checked (0)` |
| Real repository (NestJS 11 + Fastify, BullMQ 6.3.4 in the lockfile — F1L prints it since 2026-10-14 (2 lines), F1 the manifest range; read-only, about 11,100 files; re-run on the full tree 2026-10-14 with CI and the shared packages readable: 1.8 s, the same counts, and no replay or workflow gate in CI) | 1.6 s. F1: `bullmq` only; F2: 0 workflow files, 0 saga files, 0 state machines → **§1–§3 N/A (no workflow SDK)**. 4c: **2** catch-undo sites → both refuted at part A (a send-cooldown window and an import run lock released when the send or the enqueue fails; both rethrow — a lock released, not a saga compensated); 5b 0; 6a 0. The first draft searched the word `compensat*`: **204 lines in 63 files** ("compensating control" in webhook verification, a damage-compensation column), 0 sagas — every saga lane is structural for that reason |

## The 3,000-hit path

1. **Scope first** (F2). A large repo's § 1 list is only its workflow files; a hit outside them is not printed. A monorepo with one Temporal service runs § 1 on that service's files.
2. **Run the tools before reading** (`workflowcheck`, the DURABLE analyzers): a tool's exit replaces the grep for its SDK and is tier T.
3. **Group by root cause**: a shared options constant, a workflow helper module imported by many workflows, one saga helper or one base orchestrator is **one** finding with N sites.
4. **Rank**: money and stock sagas and long-lived workflows (open across deploys) first; then short workflows; then sagas whose effects are internal.
5. **Read the top 30 groups**; sample 10 sites per group, the rest inherit the verdict with the group's id.
6. **Run the bulk oracle once**: V320 — replay the previous release's histories against the current code; one run covers every § 1–§ 2 candidate of that worker.
7. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production path reached by F3. A loud failure on first execution (a sandbox error, a rejected activity) ranks below a silent one (a replay break days later, a double charge).

| § | Classes | Default severity |
|---|---|---|
| 1 | WF-1 non-determinism in workflow code, per SDK | high when the hazard changes the command sequence on replay (a branch, a loop bound, an id passed to an activity); medium when the sandbox raises at first run (Python, TS bundle errors); not a row for TS `Date.now()`/`Math.random()`/`setTimeout` (precedent 25) |
| 2 | WF-2 workflow change with open executions and no version gate; no replay test | high when executions live across deploys (loops, timers, human waits); medium for minutes-long workflows drained before deploy; not a row for a brand-new workflow type |
| 3 | WF-3 activity and engine configuration | high for unlimited retry on a non-idempotent effect, an endless loop with no continue-as-new, a Step Functions Task with no timeout on a hung call, a flow parent stuck on a failed child, a non-idempotent Zeebe handler; medium for a missing timeout (rejected at schedule time — high when only the failure path schedules it), no non-retryable types, no heartbeat on a long activity; low for signal-then-poll |
| 4 | SG-1 side-effecting step with no compensation (not the pivot) | high for money, stock or a customer-visible effect left behind; not a row for the pivot, a retriable step after it, a single-database "saga", or a written acceptance (precedent 26) |
| 5 | SG-2 compensation order, swallowed error, cancelled context, registered after the call | high for a cancelled Go context (the compensation never runs) and a swallowed error (the saga reports success); medium for forward order (high when a compensation depends on a later one) and registration after a call that can fail after its effect |
| 6 | SG-3 non-idempotent compensation; irreversible before fallible; no persisted state; in-memory saga | high for money compensations with no key (→ security) and `@Saga()` driving a cross-service money or stock command; medium for an irreversible notification before a fallible step |

### 1. Non-determinism in workflow code (WF-1)

```
BAD:   TS     import axios from 'axios' · import { charge } from './activities' · process.env.FLAG · crypto.randomUUID() · if (workflowInfo().unsafe.isReplaying) …
       Go     start := time.Now() · go notify(id) · for k := range byID { … }        Java  System.currentTimeMillis() · UUID.randomUUID()
       .NET   DateTime.UtcNow · await Task.Delay(…) · Guid.NewGuid()                 Python (sandbox off) datetime.now() · random.randint(…)
       Durable df.app.orchestration('o', async function (ctx) {…}) · async def orchestrator(context)
       Restate const id = crypto.randomUUID() before ctx.run(…) · DBOS / Inngest Date.now() outside a step
GOOD:  TS Date.now() (sandboxed) · workflow.Now(ctx) · Workflow.currentTimeMillis() · Workflow.UtcNow · workflow.now() · a generator orchestrator
       ctx.rand.uuidv4() · ctx.date.now() · the value computed inside ctx.run / step.run / DBOS.runStep
```
**Read the code:** Is the file workflow code for **this** SDK (F2), and is the token a hazard in the § 1 table for it? Is the sandbox on (F3), and is the module in `ignoreModules`? Does the value change the command sequence — a branch, a loop bound, an argument to an activity — or only a log line (`SideEffect` or `isReplaying` used for metrics is not WF-1)? Is it inside a step callback (Restate, DBOS, Inngest)? Did `workflowcheck` or the DURABLE build already rule? **Finding when** a replay of a recorded history takes a different path, or the engine raises on the code at its first run. **Proof (V320):** run `workflowcheck -show-pos ./...` (Go) or the DURABLE analyzers as errors (tier T); otherwise record a history with the current code, change nothing, replay it with the SDK's replayer after advancing the clock, and assert no `DeterminismViolationError` / non-determinism error (fails before the fix for a clock or random branch); Restate RT0016 and DBOS `DBOSStepNondeterminismError` are those engines' failures.

### 2. Workflow change with open executions and no version gate (WF-2)

```
BAD:   a diff inserts `await notifyWarehouse(id)` before an existing activity in a workflow with 30-day timers, no patched()/GetVersion
       a Restate deployment updated in place · DBOS with a fixed applicationVersion and a reordered step list
       an Inngest function whose step ids were renamed while runs are open · workflows with no replay test in CI
GOOD:  if (patched('notify-warehouse')) { await notifyWarehouse(id) } · v := workflow.GetVersion(ctx, "notify", workflow.DefaultVersion, 1)
       worker versioning pinning open executions to the old build · a new Restate deployment registered beside the old one
       CI replays the previous release's histories (Worker.runReplayHistories) and fails the build on a seeded reorder
```
**Read the code:** Do executions of this type stay open across a deploy (timers, signals, loops, human waits — F2 and the workflow's own waits)? Does the diff change the commands (add, remove, reorder an activity, a timer, a child, a signal wait) or only the code inside an activity? Is a gate added (2a), or does the worker use build-id / deployment versioning (F3)? For Restate, are deployments immutable on this platform; for DBOS, which `applicationVersion` do open workflows carry? Is there a replay test over **recorded** histories in CI (F3) — a test that runs the workflow fresh is not one? **Finding when** an open execution replays the new code into a different command sequence. **Proof (V320):** replay the previous release's committed histories (`temporal workflow show -w <id> --output json`, flag form [K?]; `fetchHistory()` in TS) against the changed code: the replay fails before the gate is added and passes after.

### 3. Activity and engine configuration (WF-3)

```
BAD:   proxyActivities({ startToCloseTimeout: '30s' }) for chargeCustomer — unlimited attempts (WK6) on a charge with no idempotency key
       proxyActivities({ retry: { maximumAttempts: 2 } }) — neither timeout: rejected when scheduled (WK6), often only on the failure path
       activities that throw plain Error on a 4xx (retried until Schedule-To-Close) · heartbeatTimeout: '1m' with no heartbeat() call ([K?])
       while (true) { await charge(); await sleep('30 days') } with no continueAsNew (WK7) · DURABLE0011
       "Type": "Task" with no TimeoutSeconds (99,999,999 s, WK9) · a FlowProducer child with no failParentOnFailure (BQ8)
       a Zeebe taskHandler that charges with no key (at-least-once; a timed-out job runs on two workers)
       client: handle.signal(approve) then a loop of handle.query(status) — an Update returns the result
GOOD:  retry: { maximumAttempts: 5, nonRetryableErrorTypes: ['CardDeclined'] } + an idempotency key from workflowId + activityId
       ApplicationFailure.nonRetryable(…) on a permanent error · heartbeat() inside the long loop · continueAsNew every N iterations
       "TimeoutSeconds": 60 (and "HeartbeatSeconds" below it) · failParentOnFailure / ignoreDependencyOnFailure set per child
```
**Read the code:** Where do the options really come from (the call, a shared constant, the SDK default row)? What does the activity do, and with what key would a second attempt repeat it — the workflow id plus the activity id, a provider idempotency key, or nothing (precedent 17's server half)? Which errors are permanent, and does the activity mark them? How long can the activity run, and does it heartbeat? Does the workflow loop, and what bounds its history? For Step Functions: is the Task's Lambda or HTTP call bounded elsewhere (→ infrastructure § 1)? For Zeebe: is the job timeout above the handler's p99, and is the handler idempotent? **Finding when** a retry repeats an effect, a permanent error retries without end, a hung step never times out, a parent never completes, or the history hits the limit. **Proof (V321):** under the time-skipping test environment, the activity mock fails after its effect on attempt 1 and succeeds on 2: the provider-side effect count must be 1 (fails at 2 before the key); a permanent error runs once; the loop continues-as-new before the limit. The missing-timeout row is proved against `temporal server start-dev`: the workflow task fails when the activity is scheduled.

### 4. Side-effecting step with no compensation (SG-1)

```
BAD:   step().invokeParticipant(this::reserveCredit).step()…  — a participant step with no .withCompensation, not the last
       await reserveInventory(o); compensations.push(release); await chargeCard(o); compensations.push(refund); await createShipment(o)
       — then a fallible step follows createShipment, and nothing undoes it
       try { await payments.charge(…); await shipping.book(…) } catch (e) { await stock.release(hold.id) }   // charge never refunded
GOOD:  .withCompensation(this::releaseCredit) · move the step after the pivot · a written acceptance naming the irreversible step
```
**Read the code:** List the forward steps (4b's listing) and mark each compensatable, pivot or retriable. Is the uncompensated step the pivot or a retriable step after it (precedent 26)? Is it a single-database "saga" that needs a transaction, not compensations? Is the irreversibility accepted in writing (an ADR or a comment naming the step)? **Finding when** step k+1 fails and step k's effect stays. **Proof (V322):** the step-k failure matrix — for each step k, inject a failure into k (clean: before its effect; ambiguous: after it) and assert C(k-1)…C1 ran; fails before the fix on the unpaired step.

### 5. Compensation order, swallowed error, cancelled context, registered after the call (SG-2)

```
BAD:   compensations.push(…) … for (const c of compensations) await c()        // forward order
       catch (e) { for (const c of compensations) await c() }                     // no rethrow: the saga reports success
       defer func() { workflow.ExecuteActivity(ctx, Refund, t) }()                 // ctx cancelled: never runs on cancellation (WK11)
       const c = await chargeCard(o); compensations.push(() => refund(c.id))       // a timeout after the charge: no refund registered
GOOD:  compensations.unshift(() => refund(txId)); await chargeCard(o, txId)        // registered before; tolerates "never ran"
       dctx, _ := workflow.NewDisconnectedContext(ctx) · throw e / ApplicationFailure after compensating · Java Saga defaults
```
**Read the code:** In what order do compensations run (`unshift`, a reversed loop, the Java `Saga` defaults — precedent 27)? Does a later compensation depend on an earlier one (release a reservation keyed by the charge)? Does the original error reach the caller and the saga's status? On Go, is the compensation's context disconnected? Can the forward call fail **after** its effect — a timeout, limited retries, a lost response — and is the compensation registered before it, keyed so it can undo an effect it never saw confirmed? **Finding when** a failure leaves effects in place, compensates in an order that fails, or reports success. **Proof (V322):** the matrix's order assertion (record calls in a list), the status assertion, and the **ambiguous** row: the mock completes the effect then times out — the compensation must still run exactly once.

### 6. Compensation idempotency, irreversible steps, saga state (SG-3)

```
BAD:   @Saga() orderPlaced = (e$) => e$.pipe(ofType(OrderPlaced), map(e => new ChargeCommand(e.id)))   // in memory, no compensation
       refund(chargeId) with no key — a retried compensation refunds twice · sendConfirmationEmail before a fallible step
       a choreographed saga whose progress lives only in events, with no saga_state row and no process manager
GOOD:  a durable engine or a saga_state(saga_id, step, status) row written with each local step · refund keyed saga:<id>:refund
       irreversible effects after the pivot · NestJS workflows with a persistent store in place of @Saga() (pre-1.0, read the version)
```
**Read the code:** Does each compensation carry a key that makes a second run a no-op (6c: a provider idempotency key, `ON CONFLICT`, a `(sagaId, step)` row)? Where does the saga's progress live if the process dies between two steps (6b)? Does `@Saga()` emit a command that crosses a service or a database boundary, and does anything compensate it? Which steps notify a customer or ship, and does a fallible step follow them (6d)? A money compensation goes to security (§ Boundaries). **Finding when** a replayed failure path repeats an effect, a crash mid-saga orphans it, or a customer is told of an order that is then compensated. **Proof (V322):** replay the whole failure path a second time (redelivery or workflow retry): provider state unchanged, the refund count stays 1; kill the process between steps 2 and 3 and restart: the saga resumes or compensates.

## Output

Example — a TypeScript Temporal service (illustrative):

```
workflow-scan coverage — scope=whole repo  sdks=@temporalio/workflow ^1.24.0 range (apps/billing/package.json:18)  engines: Temporal (TS)
Workflow files: 6 (TS) · sagas: 1 · state machines: 0 · replay test: none in CI · worker versioning: none · sandbox: on

Findings: 1 · Unconfirmed: 1 · Hardening: 1

1. apps/billing/src/workflows/billing.ts:3 · apps/billing/src/activities/billing.ts:2          [report-with-fix]   high
   §3 WF-3 — part A: chargeCustomer's proxy (startToCloseTimeout 30 s). Part B: no maximumAttempts → unlimited attempts (WK6);
   the activity charges with no idempotency key. V321 time-skipping run: 2 charges after a failure after the effect.
   Fix: retry { maximumAttempts: 5, nonRetryableErrorTypes: ['CardDeclined'] } + key `${workflowId}:${activityId}`.
2. apps/billing/src/workflows/billing.ts:14                                                    [report-flagged]    high
   §2 WF-2 — a 30-day loop, the diff adds an activity before `sleep`, no patched(), no replay test. Settling test: V320 with a
   history recorded on the base commit.
3. apps/billing/src/workflows/report.ts:8   Hardening   §1 `Date.now()` in a TS workflow — sandbox-deterministic (precedent 25)

Verification: 9 candidates → 1 finding · 1 unconfirmed · 1 hardening · 6 refuted (self-verified)

Class coverage:
  §1  non-determinism          checked (4 → 0; 1 hardening, precedent 25)
  §2  versioning               checked (1 changed workflow → 1 unconfirmed; replay test: none)
  §3  activity config          checked (6 proxies → 1 finding) · → retry-deadline-scan §4 (1 layer row)
  §4  missing compensation     checked (1 saga, 3 steps → 0; pivot = shipment, precedent 26)
  §5  order / swallow / ctx    checked (0)
  §6  idempotency / state      checked (1 → 0) · → security logic-race-scan §4 (0) · → database transaction-scan §8 (0)
```

The same block on the read-only real repository: `§1–§3 N/A (no workflow SDK: F1 bullmq only)` · `§4 checked (4c: 2 → 0, part A)` · `§5 checked (0)` · `§6 checked (0)`.

`[report-with-fix]`: the oracle failed on the unfixed code (a tool exit, a replay, a time-skipping run or the matrix), and the fix is local — the engine's own API, the shared options constant, the saga helper. `[report-flagged]`: one link is unproven (no recorded history, a tool not installed, a `[K?]` row); the row names it and the settling test. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<tool> not installed)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 25** TS Temporal `Date.now()`, `Math.random()` and `setTimeout` are sandbox-deterministic; Python `asyncio.sleep` / `gather` on workflow coroutines are durable. *Flips back:* `ignoreModules`, a custom loader, the sandbox off.
- **§ 26** the pivot and retriable steps after it need no compensation; a single-database "saga" needs a transaction; a written acceptance clears a missing compensation. **§ 27** the Java `Saga` defaults compensate in reverse order; `continueWithError = false` is a design choice.
- **§ 17** a retried activity is safe when the server stores its idempotency key — verify the server half. **§ 16** a polling loop in a workflow is not a retry. **§ 33** a test that mocks every activity proves nothing about replay. **§ 34** a comment saying "deterministic" or "idempotent" is a pointer: read the code.

Shapes this skill must not report: `SideEffect` or `isReplaying` used only for logging or metrics; a token inside an activity or a step callback; a brand-new workflow type with no gate; an activity without a cap whose effect is a read or keyed by the workflow id; a lock or cooldown released in a `catch` that rethrows.

## When to run

- On any diff that touches a workflow, orchestrator, activity options, a state machine definition, a flow, or a saga — `/ds-audit`'s "a workflow or activity file; a saga" signal. A diff-scoped run sets `WF_BASE`; a run with no git base gets `CONTRACT_BASE` from `/ds-audit --contract-base=<dir>`.
- On every whole-repo `/ds-audit`, reporting all six §s; before raising a workflow's lifetime (a timer, a loop, a human wait) or introducing a saga.
- After `/add-saga`: its Phase 6 runs V322 from the same oracle file.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the SDK and version lines and the `broker-semantics.md` row — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt before §1 when F2 did not run.** A token list over all code flags every activity; printing it is the failure the per-SDK scoping exists to avoid. **Never flag TS `Date.now()`, `Math.random()` or `setTimeout()`** as non-determinism (precedent 25), and never call a missing activity timeout "stuck forever" on Temporal (WK6).
- **Halt on any finding missing its anchors:** the workflow, activity or saga `file:line`, the SDK and version, the event it breaks under, the row or dated doc, the fix in the engine's own primitive.
- **No `[report-with-fix]` without a failed oracle** — a tool exit, a replay of a recorded history, a time-skipping run or the matrix. A test that mocks every activity is not one.
- **No proposed fix may trade a replay break for a silent double effect** (removing a gate, raising attempts on a non-idempotent activity) without a written decision.
- **Never contact an engine outside a local dev server or a scratch container** (`temporal server start-dev`, LocalStack, a Zeebe container); `temporal workflow show` and every live read only under `--live`; never run `kubectl`, `helm` or a cloud CLI against a default context or profile.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "workflows look deterministic"** without the coverage block; a § whose grep or tool did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Workflows and Sagas ledger rows; `/ds-fix` closes findings with the failing-first oracle, the fix in the engine's primitive, a re-run of this detector and the sibling sweep. `/add-saga` builds sagas this skill audits.
- `retry-deadline-scan` (activity retry as a layer, deadlines), `messaging-scan` (queue consumers), `coordination-scan` (locks a workflow takes) and `event-contract-scan` (process managers, event schemas) are the neighbours named in § Boundaries; `@workflow-orchestrator` judges these rows; the `saga` pattern is the design reference.
- database `transaction-scan` § 7–§ 8, security `logic-race-scan` § 4 and infrastructure `serverless-reliability-scan` § 1, when those packs are installed.

## Sources

Defaults are rows of `broker-semantics.md` (WK1–WK14, BQ8; read 2026-10-14 from docs.temporal.io *workflow basics* per SDK, *Retry policies*, *Detecting activity failures*, *Cloud limits*, the sdk-go `workflowcheck` README v0.6.0, durabletask-dotnet `AnalyzerReleases.Shipped.md`, learn.microsoft.com *Durable Task code constraints*, docs.aws.amazon.com *Task state*, inngest.com *Working with loops*, docs.restate.dev, temporal-sdk 1.40.0 `Saga.java`). Read for this skill on 2026-10-14: docs.dbos.dev *Workflows* and *Upgrading workflow code*, docs.restate.dev *Versioning*, docs.camunda.io 8.10 *Job workers*. Grep literals are the distributed-systems research notes B § 3–§ 4 (determinism greps per SDK, W1–W9, SG1–SG10), tested on `samples-B/wf/` and `samples-B/saga/` 2026-10-14, extended and re-measured here; the class map and the D2/D3/D12 corrections are the batch-5 eval § 1.5 and § 3.2 (DS-5). Paraphrased; no text reproduced beyond identifiers.
