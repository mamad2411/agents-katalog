---
name: retry-deadline-scan
description: "Retries and deadlines: eligibility, caps, backoff, nested layers, non-idempotent retries, propagation — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: retry-deadline-scan

## Premise

A retry is a second copy of a request the caller could not see finish. Whether that copy is harmless is decided by defaults nobody wrote down: axios-retry retries **any** method — POST included — on a network error, go-retryablehttp and the .NET standard resilience handler retry POST, a bare tenacity `@retry` never stops and never waits, p-retry and Polly never jitter, the AWS SDK already makes 3 attempts before your wrapper makes its own, and a Temporal activity retries forever. Each layer looks reasonable on its own; three layers at 3 attempts are 27 calls on a dependency that is already down (243× at five layers, AWS; 64× at three layers of four, Google SRE). A deadline that is not carried across a hop lets the work run on after the caller gave up, and a retry then runs beside it. This skill finds retries and deadlines in code and config, classifies each as IF (what is retried), WHEN (cap, delay, jitter), HOW (what a retry repeats) and the budget (layers, deadlines), and proves each with its oracle. Read-only: it never edits code and never calls a real dependency.

It owns `/ds-audit`'s Retries (§1–§6) and Deadlines (§7–§8) ledger rows. `@resilience-reviewer` (this pack) judges its rows.

**Every finding cites the retry or deadline `<file:line>` + the call chain it sits on (the layer worksheet below) + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row its verdict rests on (RY1–RY12, BQ2, CY3, KA7, WK6, LO2), read at the installed version + the oracle that showed it, or the test that would settle it + the fix in the project's own primitive** (its outbound kernel, retry constant, base producer or deadline helper). A grep hit is a candidate. "Retries look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) § 14–18 and § 36. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V304–V309.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them to retries.

1. **Part A holds: this is a retry (or a deadline) on a production path.** Retry re-executes the same failed operation. Polling, a spin-lock, a periodic job and a reconnect loop are not retry (precedent 16; in the WASABI study 29 of 60 false positives were exactly this). A process type the deploy starts runs it (gate 1).
2. **Part B holds at the installed version.** The library version is read from the lockfile or manifest (F1, gate 3), and the default the verdict rests on is a named row: "no jitter" on a library that jitters by default is a fabrication (precedent 15). The AWS SDK row needs the SDK version **and** the environment: the 2026 retry behaviour is opt-in through `AWS_NEW_RETRIES_2026=true` (RY10; F1b).
3. **Nothing already controls it**, across files. A shared outbound kernel that classifies errors, a `retryCondition` that excludes POST, a server that stores the client's idempotency key (precedent 17), a deadline that aborts the work (precedent 36), an inner layer that swallows its own exhausted failure so the outer layer never retries it. **Read the callee bodies in other files** before accepting "no backoff" or "no cap" — WASABI's second false-positive class was a sleep in a helper in another file.
4. **The oracle fired, or the fact is two-ended.** A unit or container oracle (tier C) counts the attempts, the gaps, the downstream calls or the provider effects; or the static fact cites both ends — attempts × per-attempt timeout + backoff against the outer budget, each term with its `file:line` (tier S). Without one the row is `[report-flagged]` / Unconfirmed with the settling test written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **The timeout value and its latency** — whether an outbound call has a timeout at all, whether it is total (body included), whether it fits the dependency's p99, Go `context.Background()` in a handler — are performance `request-path-scan` § 12. **This skill owns retry layering and deadline propagation**: how many layers retry one call (§4), whether the budget is carried across a hop (§7) and whether attempts × per-attempt timeout + backoff fits the caller's remaining budget (§8). A synchronous chain with no retry layer and no async hop stays § 12's.
- **Proxy and load-balancer retries** (`proxy_next_upstream … non_idempotent`, `retryNonIdempotentMethod`, an Envoy `retry_policy` with no method gate) → infrastructure `edge-reliability-scan` § 3 (V284); the platform timeout chain (LB → proxy → app) → § 1 (V282). §5 and §8 here exclude proxy config.
- **Serverless retries** — Lambda async-invoke retries, event-source `maximum_retry_attempts`, SDK × async × redelivery on a function — → infrastructure `serverless-reliability-scan` § 6 (V259), when that pack is installed. This skill keeps chains that run in long-lived processes and prints `→ infrastructure serverless-reliability-scan §6 (k)` for the rest.
- **Money, stock and credit** — a retried charge, a PSP key minted per attempt — → security `logic-race-scan` § 4, when the security pack is installed; §5 hands the row over with the retry mechanism as evidence. Without it, reported here tagged `money retry (owner pack not installed)`.
- **What happens to a message that keeps failing** (poison, DLQ, requeue loops) → `messaging-scan` (this pack) § 3; a job that repeats its effect on **redelivery** → `messaging-scan` § 2. §4 here owns "a job retried by both `attempts` and an inner client"; `messaging-scan` § 3 corroborates when `attempts` has no backoff.
- **Temporal activity options** (`proxyActivities`, `ActivityOptions`, unlimited attempts by default, WK6) → `workflow-scan` (this pack) § 3 owns the row; here the activity is one layer of the §4 worksheet.
- **Lock acquisition retries** (redlock `retryCount`, LO2) are §2 here; the lock itself is `coordination-scan` (this pack).
- **Backend `api-consistency-audit` #13** hands retry eligibility here (§5) and keeps only the policy drift; **job contracts** (overlap, payload drift, result discarded) stay backend's. A client device's offline queue replaying with a fresh key per send → mobile `offline-sync-scan` § 2.
- **Bulkheads and admission control** → performance `request-path-scan` § 14; retry storms at the platform edge → infrastructure as above.

## Adapt to the codebase — the retry lanes

Read every retry, HTTP and SDK library **with its version** (F1). Facts are rows of `broker-semantics.md` § Retry and deadline libraries (tagged and dated there); a row tagged `[K?]` makes its verdict Unconfirmed until the settling test runs.

| Lane | Defaults that decide verdicts | Shapes to grep (pre-flight) |
|---|---|---|
| **Node** — axios-retry, p-retry, got, ky, cockatiel, a project outbound kernel (`retry: {…}` options), `@aws-sdk/*` | RY3 (delay 0; POST retried on a network error), RY2 (no jitter, 10 retries), RY4 (got: 2, no POST, ±100 ms), RY10 (AWS 3 attempts, full jitter, `AWS_NEW_RETRIES_2026`), RY11 (gRPC: no deadline, Node propagation manual) | 0a, 0b, 3b, 4a, 4d, 5a, 5b, 5e, 7a, 7c |
| **BullMQ / Bull** job retries (the outer layer) | BQ2 (`attempts` 1, no `backoff` → immediate retry; a stalled job re-runs once) | F2, 0c, 4d |
| **Python** — tenacity, backoff, stamina, urllib3 `Retry`, Celery `autoretry_for` / `self.retry` | RY1 (bare `@retry`: forever, no wait), CY3 (Celery `max_retries` 3, `None` = forever, `retry_backoff` off), urllib3 does not retry POST by default (`precedents/backend.md` B-R1) | 1a, 1b, 2a, 3b, 5f |
| **.NET** — Polly v8, `Microsoft.Extensions.Http.Resilience`, MassTransit `UseMessageRetry` | RY6 (constant, no jitter, every exception), RY7 (standard handler retries POST; one handler only; `ConfigureHttpClientDefaults` applies it everywhere) | 1c, 3a, 4b, 4c, 5d |
| **JVM** — Resilience4j, Spring 7 `@Retryable`, Spring Retry, Spring Kafka error handlers, `@RetryableTopic` | RY8 (3 attempts, constant 500 ms, every exception), RY9 (`@Retryable` any exception; a second layer), KA7 (`DefaultErrorHandler()` 10 attempts, 0 delay) | 1a, 1c, 3a, 3b, 4c |
| **Go** — go-retryablehttp, cenkalti/backoff, gRPC | RY5 (unjittered, retries POST), RY12 (jittered), RY11 (gRPC propagation automatic in Go) | 3b, 5c |
| **Temporal, Sidekiq, Laravel** (outer layers) | WK6 (activities unlimited), RB1 (Sidekiq 25 retries), LV2 (`$tries = 0` unlimited, [K?]) | 0c, F2; Temporal config → `workflow-scan` §3 |

## Read the code — per call chain, before any §

Start from the retry-policy inventory (0a, 0b) and the outer layers (F2, 0c), not from vocabulary: on the real repo, retry words hit 809 lines in 276 files while the inventory and the layer join named 5 chains. For each chain, answer these; the § each answer feeds is in brackets.
- **Is it retry at all?** The same failed operation re-executed, or a poll, a periodic sweep, a reconnect, a spin on a lock? [part A of every row]
- **What does it retry?** Every exception, or the transient ones (timeouts, connection resets, 5xx, 429, 503)? A validation error, a 4xx, a deserialisation failure, an auth failure retried is wasted attempts and a delayed dead letter [§1; `THR-RES-RETRY.never_on`]
- **When does it stop, and how long between attempts?** A cap, a total time budget, a capped exponential with jitter, `Retry-After` honoured on 429 [§2, §3]
- **How many layers retry this one call?** The SDK, the kernel, the wrapper, the job's `attempts`, the broker's redelivery, an activity policy — and **does the inner layer's exhausted failure reach the outer layer?** A client that catches and returns `null` stops the multiplication [§4]
- **Is the call safe to repeat?** A read, a PUT by key, a write the far end dedupes on a key we send (stable across attempts and across job re-runs) — or a POST that creates [§5]
- **What did attempt 1 leave behind?** A flushed row, a consumed stream, a half-written file, a first external effect the retry repeats [§6]
- **Whose deadline is it?** Does the caller's remaining budget travel with the call (a context, an `AbortSignal`, `grpc-timeout`, an `expiresAt` on the message), and does the work stop when it expires? [§7, §8]

## The layer worksheet (§4, §8)

One worksheet per chain; 4d prints the candidate chains. Fill it from F2 (outer attempts and backoff, with their source), 0b (inner policies) and the reads above:

```
chain: <entry: job/consumer/route>  →  <hop>  →  <call site>
layer   file:line                         attempts  backoff/jitter      per-attempt timeout  propagates?            source row
outer   queue.producer.ts:203 (base)      3         jittered, 1–… s     job deadline 30 s    —                      BQ2 + F2
inner   orders.client.ts:92               3         full jitter ≤ 5 s   15 s (STANDARD tier)  thrown → job fails     0b
SDK     —                                 1         —                   —                    —                      RY10 n/a (no SDK)
product: 3 × 3 = 9 calls per failing action (THR-RES-RETRY.max_attempts 5; precedent 14: one retrying layer)
budget:  15 s × 3 + 2 waits ≤ 5 s = 55 s per inner call vs the 30 s job deadline → §8 candidate (aborted by the job signal? P36)
```

A layer counts only when its exhausted failure **propagates** to the layer above: a client that catches and returns a result, a `null` or a logged warning ends the chain there, and the product is that layer's attempts alone. The product > `THR-RES-RETRY.max_attempts` (5; 3 for money-moving and LLM calls), or more than one retrying layer on a dependency other callers share, is a candidate. `THR-RES-RETRY.layers` is 1 and its `budget` caps the product across layers at `max_attempts` (precedent 14).

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). Grep **N** feeds detector **§N**; the F lines are the gates and the outer-layer inventory; 0a–0c are the retry inventory every § starts from. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (for a path several globs match, the last one wins). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). 4d joins by constructor-injection types (TS, Java, C#); Python and Go chains are a read step from 0c.

```bash
export LC_ALL=C; ROOTS=(.)   # the server-side code: in a monorepo name the apps (ROOTS=(apps/api apps/worker services)); config greps always search .
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,go,java,kt,cs,rb,php}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,bin,obj,target,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,fuzz,stories}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/*Tests.cs' -g '!**/*Test.java' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**')
MAN=(-g '**/{package.json,requirements*.txt,pyproject.toml,Pipfile,go.mod,pom.xml,build.gradle,build.gradle.kts,*.csproj,Directory.Packages.props,Gemfile,composer.json}' -g '!**/node_modules/**' -g '!**/vendor/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
CONS='@Processor\(|\bextends\s+\w*WorkerHost\b|\bnew\s+Worker\(|\beachMessage\b|\beachBatch\b|@(?:EventPattern|MessagePattern|RabbitSubscribe|SqsMessageHandler)\(|@(?:shared_task|app\.task|celery\.task)\b|@(?:KafkaListener|RabbitListener|SqsListener|JmsListener)\b|\bIConsumer<|\bsidekiq_options\b|\bimplements\s+ShouldQueue\b|\bworkflow\.ExecuteActivity\(|\bproxyActivities\b'
RLIB='\baxiosRetry\(|\bpRetry\(|\bfrom\s+["\x27](?:async-retry|cockatiel|p-retry|exponential-backoff)["\x27]|@retry\b|\b(?:Async)?Retrying\(|\bstamina\.retry\b|\bbackoff\.on_exception\b|\bHTTPAdapter\(\s*max_retries\b|\bRetryStrategyOptions\b|\.AddRetry\(|\bAdd(?:Standard)?ResilienceHandler\(|\.AddPolicyHandler\(|\.AddTransientHttpErrorPolicy\(|\bWaitAndRetry\w*\(|\bRetryForever\w*\(|@Retryable\b|@RetryableTopic\b|\bRetryTemplate\b|\bRetry\.of\(|\bRetryConfig\.|@Retry\(|\bretryablehttp\.NewClient\(|\bbackoff\.Retry(?:Notify)?\(|\bretry\.Do\(|\bUseMessageRetry\(|\bautoretry_for\b|\bself\.retry\(|\bretry_on\b|\bRetriable\.retriable\b'
ROPT='\bretry\??\s*:\s*(?:\{|[A-Z][A-Z0-9_]{2,}\b)|\b(?:maxRetries|max_retries|maxAttempts|max_attempts|MaxRetryAttempts|RetryMax|retryCount|retry_count|maximumAttempts)\s*[:=]\s*[\w.$-]+'
# F1 retry, HTTP and SDK libraries with their versions (gate 3: RY1-RY12 are read at these); F1b the AWS retry environment (RY10: AWS_NEW_RETRIES_2026 is opt-in); F1L the locked versions (pnpm, npm, yarn) — the lockfile wins over the range
rg -n --no-heading --pcre2 '["\x27]?(?:axios|axios-retry|p-retry|async-retry|exponential-backoff|got|ky|undici|cockatiel|opossum|@nestjs/axios|@grpc/grpc-js|@temporalio/\w+|bullmq|@aws-sdk/[\w-]+|tenacity|backoff|stamina|urllib3|requests|httpx|celery|Polly|Polly\.Core|Microsoft\.Extensions\.Http\.Resilience|Microsoft\.Extensions\.Http\.Polly|resilience4j[\w-]*|spring-retry|spring-kafka|spring-core|hashicorp/go-retryablehttp|cenkalti/backoff\S*|avast/retry-go\S*|google\.golang\.org/grpc|faraday-retry|retriable)["\x27]?(?:\s*[:=<>~^!]=?\s*|\s+v|\s*\(|"\s+Version=")["\x27]?v?\d' "${MAN[@]}" .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:axios|axios-retry|p-retry|async-retry|exponential-backoff|got|ky|undici|cockatiel|opossum|@nestjs/axios|@grpc/grpc-js|@temporalio/[\w-]+|bullmq|@aws-sdk/client-[\w-]+)@\d[\w.-]*|"node_modules/(?:axios|axios-retry|p-retry|async-retry|exponential-backoff|got|ky|undici|cockatiel|opossum|@nestjs/axios|@grpc/grpc-js|@temporalio/[\w-]+|bullmq|@aws-sdk/client-[\w-]+)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:axios|axios-retry|p-retry|async-retry|exponential-backoff|got|ky|undici|cockatiel|opossum|@nestjs/axios|@grpc/grpc-js|@temporalio/[\w-]+|bullmq|@aws-sdk/client-[\w-]+)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '\bAWS_(?:NEW_RETRIES_2026|MAX_ATTEMPTS|RETRY_MODE)\b|\bretry_mode\s*=|\bmax_attempts\s*=' --hidden -g '*.{env,yml,yaml,json,tf,toml,ini,cfg}' -g '**/.env*' -g '**/Dockerfile*' -g '**/config' -g '!.git/**' -g '!**/node_modules/**' -g '!**/package-lock.json' .
# F2 the outer layers: every job, consumer and task with its resolved attempts and backoff (messaging-scan's ds-inventory.py); F2c is its fallback
DSI=.claude/skills/messaging-scan/scripts/ds-inventory.py; if command -v python3 >/dev/null 2>&1 && [ -f "$DSI" ]; then python3 -B "$DSI" .; else echo 'F2 NOT-RUN (python3 or ds-inventory.py absent): read 0c and every producer for attempts/backoff'; fi
# 0a retry constructs by library; 0b the retry-policy inventory — option literals and named policies (the inner layers); 0c consumer and job files (the outer layers)
rg -n --no-heading --pcre2 "$RLIB" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 "$ROPT|\b(?:[A-Z][A-Z0-9_]*_)?RETR(?:Y|IES)(?:_[A-Z0-9_]+)?\s*(?::\s*\w+\s*)?=\s*\{" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
# 1a a bare or unclassified tenacity/Spring retry; 1b a catch-all retry condition; 1c policy files with no exception filter; 1d consumer files that never classify an error (input, not a verdict)
rg -n --no-heading --pcre2 '^\s*@retry\b(?![^\n]*\bretry\s*=)|@Retryable\b(?![^\n]*\b(?:includes|include|retryFor|value|noRetryFor|excludes|exclude)\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bautoretry_for\s*=\s*\(\s*(?:Exception|BaseException)\s*,?\s*\)|\bretry_if_exception_type\(\s*(?:Exception|BaseException)?\s*\)|\.Handle<Exception>\(\)|\bhandleAll\b|\bretryCondition\s*:\s*\(\s*\w*\s*\)\s*=>\s*true\b|\bretryExceptions\(\s*(?:Exception|Throwable)\.class' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bRetryStrategyOptions\b|\.AddRetry\(|\bRetryConfig\.|\bRetry\.of\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bShouldHandle\b|\bretryExceptions\b|\bretryOnException\b|\bretryOnResult\b|\bignoreExceptions\b'
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bUnrecoverableError\b|\b(?:is)?[rR]etryable\b|\bisTransient\b|\bNonRetryable\w*|\bDoNotRetry\w*|\bdont_autoretry_for\b|\bnot_retryable\b|\bnoRetryFor\b'
# 2a no cap: forever, Infinity, None, -1, Temporal maximumAttempts 0, Forever helpers, a bare tenacity decorator; 2b files with an endless loop AND retry words (read: is it retry, polling or a reconnect? precedent 16)
rg -n --no-heading --pcre2 '\bforever\s*:\s*true\b|\bretries\s*:\s*(?:Infinity|Number\.POSITIVE_INFINITY)\b|\bmax_retries\s*=\s*None\b|\bretryCount\s*:\s*-1\b|\bmaximumAttempts\s*:\s*0\b|\b(?:maxRetries|maxAttempts|max_attempts|MaxRetryAttempts|RetryMax)\s*[:=]\s*(?:-1\b|int\.MaxValue|Integer\.MAX_VALUE|math\.MaxInt)|\b(?:WaitAndRetry|Retry)Forever\w*\(|\$tries\s*=\s*0\b|^\s*@retry\s*(?:\(\s*\))?\s*(?:#.*)?$' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bwhile\s*\(\s*(?:true|1)\s*\)|\bfor\s*\(\s*;\s*;\s*\)|^\s*while\s+True\s*:|^\s*for\s*\{\s*$|\bloop\s+do\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l -i --pcre2 '\bretr(?:y|ies|ying)\b|\bre-?attempt\w*|\battempts?\b'
# 3a explicit zero, constant or unjittered delays; 3b a library whose default has no delay or no jitter, used without the option that adds it (RY2, RY3, RY5, RY8, CY3); 3c a retry that handles 429 and never reads Retry-After
rg -n --no-heading --pcre2 '\bBackoffType\s*=\s*DelayBackoffType\.Constant\b|\bUseJitter\s*=\s*false\b|\brandomize\s*:\s*false\b|\bnew\s+DefaultErrorHandler\(\s*\)|\bnew\s+FixedBackOff\(|\.Immediate\(\s*\d+\s*\)|\bretryDelay\s*:\s*\(\s*\)\s*=>\s*\d+|\bretry_backoff\s*=\s*False\b|\bwait_fixed\(|\bwaitDuration\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
while IFS= read -r p; do rg -l0 --pcre2 "${p%%~~*}" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 "${p#*~~}" | sed "s/$/  (3b)/"; done <<'EOF'
\baxiosRetry\(~~\bretryDelay\b|\bexponentialDelay\b
\bpRetry\(~~\brandomize\s*:\s*true\b
\bretryablehttp\.NewClient\(~~\bLinearJitterBackoff\b|\.Backoff\s*=
\bRetryConfig\.|\bRetry\.of\(~~\bofExponentialRandomBackoff\b|\brandomizedWaitFactor\b|\bRandomized\w*
\bautoretry_for\b~~\bretry_backoff\s*=\s*True\b
EOF
rg -l0 --pcre2 "$RLIB" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\b429\b|\bthrottl\w*|TooManyRequests' | xargs -0 -r rg --files-without-match -i --pcre2 'retry-?after|\bretryAfter\w*|\bRetryAfter\w*'
# 4a an SDK that retries by itself (AWS 3 attempts, RY10; Google/Azure clients) inside a retry construct; 4b .NET handlers stacked on one client or on every client; 4c a retry annotation or policy on a listener whose container also retries
rg -l0 --pcre2 "$RLIB" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '@aws-sdk/client-|\baws-sdk\b|\bimport\s+boto3\b|\bboto3\.client\(|software\.amazon\.awssdk|aws-sdk-go|@google-cloud/|\bfrom\s+google\.cloud\b|\bAzure\.\w+' | "${NC[@]}"
rg -n --no-heading --pcre2 '\bConfigureHttpClientDefaults\(|\bAdd(?:Standard)?ResilienceHandler\(|\.AddPolicyHandler\(|\.AddTransientHttpErrorPolicy\(|\bAddStandardHedgingHandler\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '@(?:KafkaListener|RabbitListener|SqsListener|JmsListener)\b|\bUseMessageRetry\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '@Retryable\b|\bRetryTemplate\b|@Retry\(|\bUse(?:Delayed|Scheduled)Redelivery\(|\bUseMessageRetry\(' | "${NC[@]}"
# 4d the layer join (TS/Java/C# constructor injection, two hops): an outer-layer file (0c) that injects, directly or through one class, a class or interface declared in a file holding a retry site (0a/0b) — each line: outer ← hop ← retrying file
T=$(mktemp -d "${TMPDIR:-/tmp}/rds.XXXXXX")
rg -l --pcre2 "$RLIB|$ROPT" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$T/l0"
rg -l --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$T/out"
rg -o -N --no-filename --pcre2 '\bimplements\s+\K[A-Z]\w+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort | uniq -c | awk '$1 >= 3 {print $2}' > "$T/common"   # shared bases (UseCase, OnModuleInit) join everything: dropped
hop() { tr '\n' '\0' < "$1" | xargs -0 -r rg -H -o --no-heading --pcre2 '\b(?:class|interface)\s+\K[A-Z]\w+|\bimplements\s+\K[A-Z]\w+' | awk -F: 'FILENAME == ARGV[1] {c[$1]; next} !($2 in c)' "$T/common" - | sort -u | sort -t: -k2 > "$1.d"
  [ -s "$1.d" ] || return 0; alt=$(cut -d: -f2 "$1.d" | sort -u | paste -sd'|' -)
  rg -H -o --no-heading --pcre2 "(?:readonly|private|protected|public)\s+\w+\s*:\s*\K(?:$alt)\b" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | sort -t: -k2 | join -t: -1 2 -2 2 -o 1.1,0,2.1 - "$1.d" | awk -F: '$1 != $3'; }
hop "$T/l0" > "$T/j1"; cut -d: -f1 "$T/j1" | sort -u > "$T/l1"; hop "$T/l1" > "$T/j2"
awk -F: 'FILENAME==ARGV[1]{o[$1]=1;next} ($1 in o){print $1" ← "$2" ← "$3}' "$T/out" "$T/j1"
awk -F: 'FILENAME==ARGV[1]{o[$1]=1;next} FILENAME==ARGV[2]{h[$1]=h[$1]" "$2"@"$3;next} ($1 in o)&&($3 in h){print $1" ← "$2" ← "$3" ←"h[$3]}' "$T/out" "$T/j1" "$T/j2"
rm -rf "$T"
# 5a a write sent with a retry option in the same call; 5b axios-retry clients (RY3: POST retried on a network error); 5c go-retryablehttp files that POST (RY5); 5d .NET standard handler with no unsafe-method opt-out (RY7); 5e a key minted fresh where it should be stable (read: inside the retried callback or the job body?); 5f urllib3 retries every method
rg -n --no-heading -U --pcre2 '\bmethod\s*:\s*["\x27](?:POST|PATCH|post|patch)["\x27](?:(?!\bmethod\s*:)[^;]){0,600}?\bretry\??\s*:\s*(?!undefined\b|false\b|null\b|0\b)|\bretry\??\s*:\s*\{[^{};]{0,300}?\bmethods\s*:\s*\[[^\]]*["\x27](?:post|POST|patch|PATCH)["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bmethod\s*:|\bretry\??\s*:\s*\{'
rg -n --no-heading --pcre2 '\baxiosRetry\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bretryablehttp\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\.Post(?:Form)?\(|\bMethodPost\b|"POST"'
rg -l0 --pcre2 '\bAddStandardResilienceHandler\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bDisableForUnsafeHttpMethods\(|\bDisableFor\('
rg -l0 -i --pcre2 'idempot\w*|client[-_]?token|dedupe?[-_]?key' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading -i --pcre2 '(?:idempot\w*|\w*key|client_?token|reference|dedupe\w*)["\x27]?\s*[:=,]\s*(?:await\s+)?(?:crypto\.)?(?:randomUUID|uuid(?:v4|\.v4|\.uuid4|\.New(?:String)?)?|v4|nanoid|ulid|uuid4|Guid\.NewGuid|UUID\.randomUUID)\(' | "${NC[@]}"
rg -n --no-heading --pcre2 '\ballowed_methods\s*=\s*(?:None|False|[^\n)]*["\x27]POST)|\bmethod_whitelist\s*=\s*False' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6a retry sites in files that also open or flush a unit of work (read: is the transaction or session created INSIDE the retried block?); 6b consumer files making two or more awaited external calls (read for a per-step checkpoint); 6c an attempt counter incremented in two places; 6d a stream body under retry
rg -l0 --pcre2 "$RLIB|$ROPT" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -c --pcre2 '\bem\.(?:flush|persistAndFlush|transactional|begin)\b|\.transaction\(|\bsession\.(?:commit|flush)\(|\bSaveChanges(?:Async)?\(|@Transactional\b|\btransaction\.atomic\b'
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -c --pcre2 '\bawait\s+this\.\w*(?:[cC]lient|[gG]ateway|[aA]dapter|[mM]ailer|[sS]ender|[nN]otifier|[pP]sp|[pP]rovider|[cC]arrier)\w*\.\w+\(' | awk -F: '$2 >= 2'
rg -H -c --pcre2 '\b\w*[aA]ttempts?\w*\s*(?:\+\+|\+=\s*1\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '$2 >= 2'
rg -l0 --pcre2 "$RLIB|$ROPT" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bbody\s*:\s*(?:fs\.)?createReadStream\(|\bbody\s*:\s*\w*[sS]tream\b|\bReadable\.from\(' | "${NC[@]}"
# 7a gRPC servers (Node, Python) with no deadline read (RY11); 7b a user-facing command enqueued with no expiry (read the consumer: does it check one?) — `code` and `confirm` are whole tokens (not geocode, confirm-order); 7c a deadline built from Promise.race with nothing aborted (precedent 36); 7d deadline helpers (do they thread a signal into the outbound calls?)
rg -l0 --pcre2 '\bServer(?:Unary|Writable|Readable|Duplex)(?:Call|Stream)\b|\bsendUnaryData\b|@GrpcMethod\(|\bgrpc\.ServicerContext\b|\w+Servicer\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bgetDeadline\(|\bdeadline\b|\btime_remaining\(|\bpropagate_flags\b'
rg -n --no-heading -i --pcre2 '\.(?:add|send|enqueue\w*|publish|delay|apply_async|perform_async)\(\s*["\x27`][\w:.-]*(?:otp|verif\w*|reserv\w*|hold|quote|login|(?<=[-_.:"\x27`])code\b|(?-i:(?<=[a-z])Code\b)|(?:\b|(?-i:(?<=[a-z])(?=C)))confirm(?:ation)?[-_.:]?(?:code|email)|checkout|price)[\w:.-]*["\x27`](?![^\n]*(?:expiresAt|expires_at|deadline|validUntil|\bttl\b|\bexpir\w*))' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bPromise\.race\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bAbortController\b|\.abort\(|\bsignal\b|\bAbortSignal\b'
rg -n --no-heading --pcre2 '\b(?:with(?:Deadline|Timeout)\w*|runWithDeadline|deadlineFor|currentDeadline\w*)\s*(?:=|\()|\bAbortSignal\.any\(|\bcontext\.With(?:Timeout|Deadline)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 8 the outer budgets the inner attempts must fit (job deadline, lock, request deadline, workflow/activity timeouts, Celery limits, .NET total vs attempt) — the worksheet pairs each with 0b's per-attempt timeout × attempts
rg -n --no-heading --pcre2 '\b(?:JOB_TIMEOUT\w*|jobTimeout\w*|REQUEST_(?:DEADLINE|TIMEOUT)\w*|requestTimeout|lockDuration|startToCloseTimeout|scheduleToCloseTimeout|workflowExecutionTimeout|workflowRunTimeout|soft_time_limit|time_limit|visibility_timeout|TotalRequestTimeout|AttemptTimeout|TimeoutSeconds)\b\s*[:=(]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

Reading the output:
- **F1 is the version gate.** Print each library with its source; a range marks its floor. **F1L** prints the locked version: when it printed one, that is the version, not the range's floor (a package locked at two versions: the importer's entry in `pnpm-lock.yaml`, or `<app>/node_modules/<pkg>` in `package-lock.json`, says which one the app gets). F1b with no `AWS_NEW_RETRIES_2026` means the SDK runs its pre-2026 behaviour; with it, re-read RY10 before judging timing or quota.
- **F2 is the outer layer**: `ds-inventory.py` (shipped with `messaging-scan`) prints every job and consumer with its resolved `attempts`, `backoff` and the source of each (call, `defaultJobOptions`, a producer wrapper, a library default). A BullMQ row with `attempts` > 1 and no `backoff` is a §3 candidate (BQ2: an immediate retry).
- **0b is the inner layer**: every retry option and named policy. Group by policy constant (one `DEFAULT_RETRY` used at 20 sites is one row with 20 sites).
- **4d is the subject list for §4**: `outer ← hop ← retrying file`. Each line is a worksheet to fill, never a verdict — the propagation read decides it.
- The **file-level lines** (1c, 1d, 2b, 3b, 3c, 5d, 7a, 7c) list files: read each whole. 1d is an input (consumer files that never classify an error), never a verdict.

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **A project kernel owns the loop.** One `for (;;)` in an outbound kernel serves every call; 0a is quiet and 0b holds the opt-ins. Read the kernel once (classification, jitter, `Retry-After`, the signal it races) and cite it on every row.
- **DI hides the hop.** A processor injects a use case, the use case injects a port, the port's implementation retries. 4d follows two hops by type name and drops interfaces with three or more implementers (a shared `UseCase` base joined every file to every client: 411 lines → 5 on the real repo).
- **The SDK retries invisibly.** An AWS, Google or Azure client inside a wrapper is a layer whether or not the code says "retry" (RY10). 4a lists them only where a retry construct sits in the same file; the worksheet asks for every SDK on the chain.

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples (`samples/` 15 stacks, `samples-B/` 7) | 0.4 s, 0 rg errors. Every retry BAD surfaces in its §: Celery `autoretry_for=(Exception,)` (1b) with `max_retries=None` and `self.retry(…, max_retries=None)` (2a), Laravel `$tries = 0` (2a, LV2), MassTransit `r.Immediate(50)` and Spring `new DefaultErrorHandler()` + `FixedBackOff` (3a), Celery with no `retry_backoff` (3b), `UseMessageRetry` on a receive endpoint (4c), `@RetryableTopic` (0a, after it was added to the construct list). The good Celery task (`retry_backoff=True, retry_jitter=True`) stays out of 3b; the Temporal `proxyActivities` retry with no timeout is printed by 0b for `workflow-scan` §3 |
| Seeded tree (14 files: Node, Python, Go, .NET, Java) | Every seed surfaces: bare `@retry` (1a, 2a), catch-all `autoretry_for` (1b), Polly options with no `ShouldHandle` (1c), `forever: true` (2a), an endless `try/continue` loop that logs "retrying" (2b), `randomize: false`, `UseJitter = false`, constant Polly (3a), axios-retry with no delay, p-retry with no `randomize`, go-retryablehttp default backoff, Celery with no backoff (3b), an S3 call inside p-retry (4a), two .NET handlers (4b), `@Retryable` on a `@KafkaListener` (4c), the job → use case → retrying port chain (4d), a POST with a retry opt-in (5a), `axiosRetry(client)` (5b), retryablehttp POST (5c), the standard handler with no opt-out (5d), a key minted inside the retry callback (5e), urllib3 `allowed_methods=None` (5f), a gRPC handler with no deadline read (7a), an OTP job with no expiry (7b), `Promise.race` with nothing aborted (7c), a 30 s job deadline (8). Decoys stay out: a jittered tenacity retry with `retry=`, a jittered reconnect loop with no retry vocabulary (precedent 16) |
| `benchmarks/fixtures/*` (18) | Quiet: F1 context in 7 fixtures; 0c/1d list 3 consumer files (input); 8 one server `requestTimeout`; 5e 2 lines in mobile-defects — a device offline queue minting `Idempotency-Key: uuid()` per send → mobile `offline-sync-scan` § 2, outside server ROOTS. Narrowed before shipping: 7d from 33 lines over 10 fixtures (`AbortSignal.timeout` on every fetch is § 12's timeout presence) to deadline helpers and `AbortSignal.any` only; 5a's `methods: […]` arm from 29 route and CORS lines to retry objects only; 5e from 5 lock tokens to key-named assignments |
| Real repository (NestJS 11, BullMQ 6.3.4 in the lockfile — F1L prints it since 2026-10-14 with ky, `@grpc/grpc-js`, an S3 client and undici locked at 6 and 8 (12 lines; the importer's entry says which undici the app gets) — a shared outbound kernel; read-only, about 11,100 files, ROOTS = the API app; re-run on the full tree 2026-10-14: 4.2 s with F2, the same 5 chains, 0b 71 lines and 5a 19 lines — 69 and 16 on the earlier partial copy, the new ones unread) | 2.2 s (+ 2.2 s for F2). 0a **0** library constructs: retry lives in one kernel, opt-in per call ("only where the operation is idempotent"), full jitter, error classification, every attempt racing the ambient deadline signal. 0b 69 policy lines; F2 resolves the outer layer: `attempts` 3 from the base producer, 5 on webhook jobs, jittered backoff. **4d: 5 chains** from 8 consumer files, **including the eval's 3 × 3** (a subscription-refresh job at `attempts: 3` → a client listing subscriptions with `retry: { attempts: 3 }`). Its read **refutes** it at gate 4: the client catches the exhausted failure and returns `null`, and the registration POST has no retry, so the job never fails on them — at most 3 calls per list, not 9. The same join surfaced the live candidate: the webhook job at 5 attempts → an order-fetch GET at `attempts: 3` whose failure the processor rethrows → up to 15 GETs per failing delivery. Read on the full tree: the kernel's attempt count is total calls (3), every attempt passes one breaker per dependency (5 failures open it for 30 s; an open breaker fails fast and is not retried), and the job ladder waits 30 s × 4ⁿ — so 15 is the ceiling for intermittent failures, and a provider outage meets the breaker, not 15× load: Hardening, V306 to count it. 5a **12 POST sites** with an in-call retry, each with a written reason (the far end dedupes; a model call; a GraphQL read) — pointers, not evidence (precedent 34); one relies on the caller's list diff, which the in-call retry does not re-run (Unconfirmed, V307). 5e 1 (a key minted once per operation and reused by its follow-up). 7c **0**; 7d the request and job deadline helpers (`AbortSignal.any` into every attempt: the precedent-36 control). §8: `JOB_TIMEOUT_MS` 30 s default vs a 15 s tier × 3 + 2 waits ≤ 5 s = 55 s — inner > outer, cut by the job's abort → Hardening |

## The 3,000-hit path

1. **Intersect** with F3 from `messaging-scan` (process roles): a retry in code no production process starts (a script, a seed, a CLI) is dismissed with one read. Name the directory in the coverage block.
2. **Group by root cause**: one kernel, one retry constant, one `ConfigureHttpClientDefaults`, one base producer is **one** finding with N sites. Twenty opt-ins of `DEFAULT_RETRY` on reads are one row.
3. **Rank**: chains that end in a write (§5), then chains with two or more layers (§4), then shared dependencies with many callers (§3), then the rest.
4. **Read the top 30 groups** with the read-the-code questions; for WASABI's IF outliers, compare one exception's retry ratio across sites (retried at ≥ 2/3 of its sites but not here, or the reverse). Sample 10 sites per group; the rest inherit the verdict with the group's id.
5. **Run the bulk oracle once**: V306 (count downstream calls for one failing action) on the top chain of each group, against a mock server.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production chain reached by F3. A retried write that creates an order, ships a parcel or sends a customer message is **high** for §5; money is security's (§ Boundaries).

| § | Classes | Default severity |
|---|---|---|
| 1 | RT-1 non-retryable error retried (IF; backend BJ-09) | medium; low when attempts ≤ 3 and the only cost is a delayed dead letter |
| 2 | RT-2 no cap (WHEN) | high on a consumer, a job or a shared dependency; medium elsewhere |
| 3 | RT-3 no backoff, no jitter, `Retry-After` ignored (WHEN) | medium; high on a dependency many callers share |
| 4 | RT-4 retries multiplied across layers | high when the product > `THR-RES-RETRY.max_attempts` on a shared dependency; medium otherwise |
| 5 | RT-5 retry of a non-idempotent call (backend BO-02, BO-05) | high; money → security |
| 6 | RT-6 state not reset; a retry repeats an earlier step (HOW; backend BJ-10) | medium; high when the repeated step is an external effect |
| 7 | TD-1 deadline not propagated across a hop | medium; high for a command that is wrong once late (precedent 18) |
| 8 | TD-2 timeout order inverted (inner × attempts ≥ outer) | medium; high when the overrun leaves work running that a retry duplicates (precedent 36) |

### 1. Non-retryable error retried (RT-1)

```
BAD:   @retry(stop=stop_after_attempt(5)) around a call that raises ValidationError (no retry=, RY1)
       new RetryStrategyOptions { MaxRetryAttempts = 3 } with the default ShouldHandle (every exception, RY6)
       @Retryable(maxRetries = 3) with no includes (RY9) · autoretry_for=(Exception,) · retryCondition: () => true
       a BullMQ processor that throws a 400 from the provider like any other error (no UnrecoverableError, no classification)
GOOD:  retry=retry_if_exception_type(TransientError) · ShouldHandle on HttpRequestException + 5xx/408/429 · includes = …
       throw new UnrecoverableError(…) for permanent errors · a kernel whose error type answers retryable (timeout, network, 5xx, 429)
```
**Read the code:** Which errors reach the retry — does the client map 4xx to an error type the policy excludes? Is a permanent failure (validation, 4xx other than 408/429, deserialisation, auth) ever retried, and what does each wasted attempt cost (a provider call, a partial effect, a delayed dead letter)? Libraries that classify by default (got, the .NET standard handler, the AWS SDK, Spring Kafka's not-retryable list, KA7) are not RT-1. **Finding when** a permanent error is retried more than once. **Proof (V304):** inject a permanent error at the call: exactly 1 attempt after the fix (more before).

### 2. No cap (RT-2)

```
BAD:   bare @retry (RY1) · pRetry(fn, { forever: true }) · retries: Infinity · max_retries=None (CY3) · redlock retryCount: -1 (LO2)
       while (true) { try { return await step() } catch { log.warn('retrying'); continue } } · a negative configured cap read as "infinite"
GOOD:  stop_after_attempt(n) / a total-time budget · max_retries=5 · a loop with an attempt bound and a surfaced final error
```
**Read the code:** Is the loop retry or a reconnect, a poll, a sweep (precedent 16 — a jittered reconnect on a long-lived connection is not RT-2)? Where is the bound — the call, a policy constant, a helper in another file? Is a configured cap ever negative or zero with an "unlimited" meaning (Temporal `maximumAttempts: 0`, WK6)? Is the counter incremented twice (6c: half the cap)? **Finding when** a persistently failing call is retried without bound. **Proof (V304):** a persistent transient error: attempts ≤ the stated cap, then the error is surfaced or dead-lettered.

### 3. No backoff, no jitter, `Retry-After` ignored (RT-3)

```
BAD:   axiosRetry(client) with no retryDelay (delay 0, RY3) · p-retry default (randomize false, RY2) · retryablehttp.NewClient() (RY5)
       new DefaultErrorHandler() (10 attempts, 0 delay, KA7) · Polly BackoffType.Constant / UseJitter = false (RY6) · MassTransit r.Immediate(n)
       BullMQ attempts: 5 with no backoff (BQ2) · a retry that handles 429 and never reads Retry-After
GOOD:  exponential with full jitter and a cap (`random(0, min(cap, base·2ⁿ))`) · retryDelay: axiosRetry.exponentialDelay · LinearJitterBackoff
       `THR-RES-RETRY`: backoff exponential, jitter required, honor_retry_after true
```
**Read the code:** Does the installed library already jitter (got noise, the .NET standard handler, the AWS SDK, cenkalti, Celery `retry_jitter` with `retry_backoff` — precedent 15)? Is the delay computed in a helper in another file? Many callers × one schedule is a synchronised herd even when every site agrees (backend `api-consistency-audit` #13 says the same). **Finding when** a retry fires with no delay, a constant delay, or an unjittered schedule on a dependency several callers share. **Proof (V305):** under a fake clock, record attempt times: the gaps grow, are capped, and two clients' schedules differ.

### 4. Retries multiplied across layers (RT-4)

```
BAD:   a job at attempts: 3 → a use case → a client with retry: { attempts: 3 } whose failure propagates   (9 calls per failing job)
       pRetry(() => s3.send(cmd)) (the SDK already makes 3 attempts, RY10) · ConfigureHttpClientDefaults(…AddStandardResilienceHandler())
       + a per-client handler (RY7) · @Retryable on a @KafkaListener whose container retries (KA7) · UseMessageRetry × UseDelayedRedelivery
GOOD:  exactly one retrying layer per chain: the inner call at attempts 1 (or catching its own exhausted failure), the outer layer owns retry
       · SDK maxAttempts: 1 under one outer policy · one resilience handler per client
```
**Read the code:** Fill the worksheet (§ The layer worksheet) for every 4d line and every SDK on a chain. Does the inner layer's exhausted failure reach the outer layer, or is it caught and turned into a result (the real-repo refutation)? Is the dependency shared (other callers, a provider's rate limit)? An activity's unlimited default (WK6) multiplies everything under it. **Finding when** two or more layers retry one call and the product exceeds the budget. **Proof (V306):** one failing user action against a mock that always fails: count downstream calls; after the fix ≤ the stated budget, with exactly one layer retrying.

### 5. Retry of a non-idempotent call (RT-5)

```
BAD:   axiosRetry(client) on a client that POSTs (RY3: any method on a network error — backend lab: 4 hits for one POST)
       retryablehttp client.Post(…) (RY5) · AddStandardResilienceHandler() with no DisableForUnsafeHttpMethods() (RY7)
       { method: 'POST' }, { retry: DEFAULT_RETRY } on a create · urllib3 Retry(allowed_methods=None)
       pRetry(async () => post(body, { 'Idempotency-Key': randomUUID() }))   // a new key per attempt (BO-05)
       a job retried around a provider call whose key is minted inside the job body (a new key per job attempt)
GOOD:  no retry on the create, or a key from the business id sent on every attempt and every job re-run, verified to be stored by the
       server (precedent 17) · retryCondition excluding non-idempotent methods · DisableForUnsafeHttpMethods()
```
**Read the code:** Does the call create, send or charge? Does the far end dedupe — and is that read in its documentation or contract, not in a comment (precedent 34)? Is the key stable across in-call attempts **and** across the job's own retries (minted from the business id, never inside the retried callback or the job body)? A 429 from a throttler that answered before any work (a refresh POST retried only on 429) is safe. Proxy-level retries are infrastructure's. **Finding when** a write can be applied twice by a retry after a lost response. **Proof (V307):** a mock that applies the call, then drops the response: the retry carries the same key and the provider records 1 effect after the fix (2 before).

### 6. State not reset, or a retry repeats an earlier step (RT-6)

```
BAD:   pRetry(() => this.em.flush()) around an EntityManager that a failed flush left dirty · a transaction opened outside the retried block
       a stream body re-sent on attempt 2 (already consumed) · a handler that sends an email, then calls a carrier that fails: the job retry re-sends the email
       attempts++ in the loop and again in the catch (half the cap)
GOOD:  the unit of work created inside the retried function (em.fork, a new session) · a per-step checkpoint or reserve
       (step k done → skip on retry) · retry only the failing step · a rebuilt body per attempt
```
**Read the code:** What did attempt 1 leave behind — a flushed row, a persisted entity in an identity map, a consumed stream, a temp file, a first effect? Does the retry run the whole handler again (a job's `attempts`) or only the failing call? Is there a step ledger (`(jobId, step)` reserve) or an idempotent first step? A job that repeats its effect on **redelivery** is `messaging-scan` § 2. **Finding when** attempt 2 repeats an effect of attempt 1 or fails on its leftovers. **Proof (V308):** fail after partial work on attempt 1: attempt 2 succeeds and leaves exactly one result; the first effect is not repeated.

### 7. Deadline not propagated across a hop (TD-1)

```
BAD:   a gRPC Node or Python handler calling out with no deadline taken from the call (RY11: propagation is manual there)
       queue.add('send-otp', d) with no expiresAt, consumed an hour later · a worker that never reads a deadline header
       Promise.race([work(), timeout(30_000)]) — the promise rejects, the work keeps running (precedent 36)
GOOD:  deadline: call.getDeadline() passed on · an expiresAt on the command, checked first, expired → dropped or dead-lettered
       an AbortSignal (or a cancelled context) threaded into every outbound call: AbortSignal.any([own, ambient])
```
**Read the code:** Where does the caller's budget live (a context, an async-local `AbortSignal`, `grpc-timeout`, a message field), and does every hop carry it? Does a job deadline **abort** the work or only reject the promise? Is lateness harmful for this command (an OTP, a reservation hold, a quote) or harmless (a report, a cleanup — precedent 18)? Go `context.Background()` in a synchronous handler is perf § 12. **Finding when** work continues, or a command is applied, after the caller's deadline has passed. **Proof (V309):** with a caller budget B and a slow mock, the outbound call carries ≤ the remaining budget, the callee stops within a margin of cancel, and an expired command is dropped or dead-lettered.

### 8. Timeout order inverted (TD-2)

```
BAD:   a 30 s job deadline over an outbound tier of 15 s × 3 attempts + backoff (55 s) · a .NET TotalRequestTimeout below AttemptTimeout × attempts
       a Temporal Start-To-Close longer than the workflow's business deadline · a queue visibility shorter than attempts × timeout (→ messaging-scan §6)
GOOD:  inner × attempts + Σ backoff < the outer budget with margin, or every attempt races the outer signal so the overrun is cut, not orphaned
```
**Read the code:** Take each worksheet's per-attempt timeout, attempts and backoff cap (0b, F2) and the outer budget (8, F2's resolved deadline); write the arithmetic with both ends cited. Does each attempt race the outer deadline (then the overrun is wasted attempts, not orphaned work: Hardening by precedent 36)? The platform chain (LB, proxy, Lambda) is infrastructure's. **Finding when** the inner chain can outlive the outer budget and keep working after the caller has given up or retried. **Proof (V309):** the static fact with both terms cited; the deadline-budget test settles it.

## Output

```
retry-deadline-scan coverage — scope=whole repo  libs=undici 6.28.1 (apps/api/package.json:81), bullmq ^6.3.4 range · AWS SDK: s3 only, AWS_NEW_RETRIES_2026 unset
Inventory: 0 library constructs, 1 outbound kernel (outbound-http.ts), 69 policy lines (12 POST opt-ins) · outer: 7 consumers, attempts 3 / 5 (F2)

Findings: 0 · Unconfirmed: 2

1. apps/api/src/queue/processors/webhook.processor.ts:650 → orders.client.ts:92                [report-flagged]   medium
   §4 RT-4 — part A: a job retry (attempts 5, webhook.producer.ts:30) over a kernel retry (attempts 3). Part B: the fetch failure is
   rethrown (webhook.processor.ts:676), so one failing delivery makes up to 15 GETs on the provider. Settling test: V306 — count calls.
2. apps/api/src/integrations/connector.ts:196                                                  [report-flagged]   medium
   §5 RT-5 — a webhook-registration POST with an in-call retry; the comment's safety rests on the caller's list diff, which the in-call
   retry does not re-run (precedent 34). Settling test: V307 — succeed, drop the response, count subscriptions.

Verification: 9 candidates → 0 findings · 2 unconfirmed · 1 hardening · 6 refuted (self-verified)

Class coverage:
  §1 retry IF                checked (kernel classifies: timeout, network, 5xx, 429 → 0)
  §2 cap                     checked (0; 4 endless-loop files read: kernel loop bounded by attempts)
  §3 backoff / jitter        checked (full jitter in the kernel; F2 backoff jittered → 0)
  §4 layers                  checked (5 chains → 1 unconfirmed; the 3 × 3 refuted: inner failure caught)
  §5 non-idempotent          checked (12 POST opt-ins → 1 unconfirmed) · → security logic-race-scan §4 (0)
  §6 state / repeated step   checked (4 files read → 0)
  §7 propagation             checked (AbortSignal.any into every attempt, precedent 36 → 0)
  §8 timeout order           checked (30 s job vs 55 s chain → 1 hardening, cut by the abort)
  → infrastructure edge-reliability-scan §3 (0) · serverless-reliability-scan §6 (0) · performance request-path-scan §12 (timeout values)
```

`[report-with-fix]`: the oracle failed on the unfixed code and the fix is local to the project's kernel, retry constant, base producer or deadline helper. `[report-flagged]`: one link is unproven (no oracle run, the far end's dedupe unread, a propagation read pending); the row names it and the settling test. The coverage block lists **all eight** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 14** exactly one retrying layer per chain is the design; a missing circuit breaker alone is Hardening (RES-2 allows `n-a`). *Flips back:* two or more layers retry the same call.
- **§ 15** library defaults decide "no cap / no backoff / no jitter" — read them at the installed version (RY1–RY12, KA7, WK6).
- **§ 16** polling, spin-locks, periodic jobs and reconnect loops are not retry — part A first.
- **§ 17** retrying a POST is safe when the server stores the client's key — verify the server half.
- **§ 18** background work without a deadline is fine when lateness is harmless; not for an OTP, a hold or a quote.
- **§ 34** a comment saying "idempotent" or "the far end dedupes" is a pointer, not evidence; **§ 36** a deadline that aborts the work is the control for a retry running beside the original.
- **§ 32** one replica does not make retry classes latent; **§ 33** a mocked dependency proves call counts (V306) but not a provider's dedupe (V307 needs the provider's documented behaviour or its sandbox).

Shapes this skill must not report: a reconnect loop with jitter; a poll with a fixed interval; a POST retried only on 429 from a throttler that answers before any work; an inner client that catches its exhausted failure and returns a result (the chain ends there); jittered retries reported as unjittered because the jitter lives in a helper in another file.

## When to run

- On any diff that touches a retry library or option (`attempts`, `retry:`, `@Retryable`, `autoretry_for`), a client factory or outbound kernel, a resilience handler, a deadline helper, or a job's options — `/ds-audit`'s "a retry library, a retry option, a client factory, a deadline" signal.
- On every whole-repo `/ds-audit`, reporting all eight §s; before adding a retry to a client, raising a job's `attempts`, or wrapping an SDK call.
- When backend `api-consistency-audit` #13 hands a retry-on-POST row over (§5).

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the `broker-semantics.md` row, the version lines and the worksheet — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt before any § when F1 is unread.** A verdict resting on a library default whose version is unknown is invalid; when no RY row covers the installed range, the row is Unconfirmed with the release notes to read.
- **Halt on any §4 row without a filled worksheet** (every layer with `file:line`, attempts, source and the propagation read) and any §8 row without both terms cited.
- **No `[report-with-fix]` without an oracle that failed** (V304–V309) or, for §8, the two-ended static fact.
- **No proposed fix may trade a duplicate for a loss** without a written decision: removing a retry from a read that the user needs, or `attempts: 1` on a job whose only recovery was the retry. The fix keeps one retrying layer, it does not delete them all.
- **Never call a real dependency, provider sandbox or cloud API** from an oracle without the user's explicit go; mocks and containers only. Never run `kubectl`, `helm` or a cloud CLI against a default context or profile.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "retries look fine"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Retries and Deadlines ledger rows; `/ds-fix` closes findings with the failing-first oracle, the fix at the root primitive (the kernel, the constant, the base producer), a re-run of this detector and the sibling sweep.
- `messaging-scan` (its `ds-inventory.py` is F2), `dual-write-scan`, `coordination-scan` and `workflow-scan` (this pack) are the neighbours named in § Boundaries; `@resilience-reviewer` judges these rows.
- performance `request-path-scan` § 12, § 14; infrastructure `edge-reliability-scan` § 1, § 3 and `serverless-reliability-scan` § 6; security `logic-race-scan` § 4; backend `api-consistency-audit` #13; mobile `offline-sync-scan` § 2 — when those packs are installed.

## Sources

Defaults are rows of `broker-semantics.md` § Retry and deadline libraries (RY1–RY12, read 2026-10-14 from tenacity, p-retry, axios-retry, got, go-retryablehttp, Polly, learn.microsoft.com *Build resilient HTTP apps*, Resilience4j, the Spring Framework 7.0 reference, the AWS SDKs and Tools reference *Retry behavior*, grpc.io *Deadlines*, cenkalti/backoff) and BQ2, CY3, KA7, LO2, WK6. Amplification figures: the AWS Builders' Library *Timeouts, retries and backoff with jitter* and Google SRE ch. 21–22. IF/WHEN/HOW and the false-positive classes: WASABI (SOSP '24). The axios-retry POST measurement is the backend research lab (2026-10-14). Grep literals: the distributed-systems research catalog R-1…R-7, T-1, T-2 and notes C, and the batch-5 eval § 3.2 DS-3 and § 3.8, re-measured here. Paraphrased; no text reproduced beyond identifiers.
