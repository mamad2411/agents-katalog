---
name: messaging-scan
description: "Queue semantics: ack order, consumer idempotency, poison/DLQ, ordering, rebalance, lock vs run — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: messaging-scan

## Premise

Every broker a real repo uses delivers **at least once**, and most of them decide *when* a message counts as done by a default nobody wrote down: kafkajs commits when `eachMessage` resolves, amqplib's `nack` requeues unless told otherwise, sqs-consumer ≥ 14 deletes only a message the handler **returns**, BullMQ re-runs a stalled job once (`maxStalledCount` 1) even at `attempts: 1`, Celery acks on receipt. A consumer that is correct under one of those defaults loses, duplicates or reorders work under the next. The failure is silent: the job "completed", the offset moved, the queue drained — and a customer got two receipts, or none. This skill finds those places in consumer and producer code and broker config, and proves each with its oracle against the real broker in a container. Read-only: it never edits code and never touches a broker that is not a scratch container.

It owns `/ds-audit`'s Delivery (§1–§3, §6), Order and groups (§4–§5) and Producers and brokers (§7–§11) rows. `@resilience-reviewer` (this pack) judges its rows.

**Every finding cites the consumer or producer `<file:line>` + the delivery event it breaks under (redelivery, a crash between ack and effect, a poison message, a rebalance, a lock expiry, a broker outage, an eviction) + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row its verdict rests on, read at the installed version + the oracle that showed it, or the test that would settle it + the fix in the project's own primitive** (its base processor, producer wrapper, retry constant or reserve helper). A grep hit is a candidate. "Queues look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V291–V299.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them to queues.

1. **Part A holds: this is the consumer (or producer) of a production queue.** A process type the deploy starts (F3) runs it. A one-off script, a test harness or a CLI is not (refute-before-report § 4, the first of its domain-wide precedents). A Redis pub/sub cache-bust broadcast is not a work queue.
2. **Part B holds at the installed version.** The broker, client and server versions are read from the lockfile, the manifest range or the image tag (F1, gate 3). The default the verdict rests on is a named `broker-semantics.md` row (BQ2, KJ4, RQ2, AW4, CY1, …). A managed broker whose setting is not in the repo is `UNREAD (<service>)`, and every row resting on it is Unconfirmed (row RD5).
3. **Nothing already controls it**, across files. The options a consumer or a job really runs with come from the call, the queue's `defaultJobOptions`, a producer base class, a subclass override, the `@Processor` decorator, a base processor and imported constants — F2 (`ds-inventory.py`) prints each one with its source. A reserve in the effect's transaction, an aborting deadline (precedent 36), a bounded nack (precedent 7), a DLQ in the infrastructure repo (precedent 5), a per-key serialisation (precedent 9) or a written at-most-once decision (precedent 6) is a control. **Read the whole file and its callees**: in the real-repo run, a lease drop was refuted only by a check 20 lines below it.
4. **The oracle fired, or the fact is two-ended.** A container oracle (tier C) shows the lost, duplicated or reordered effect, or the static fact cites both ends — the config value and the code that depends on it (tier S: visibility vs p99, `max.poll.records × p99` vs `max.poll.interval.ms`). Without one, the row is `[report-flagged]` / Unconfirmed with the settling test written out. A mocked broker is not a tier (precedent 33).

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **Consumer idempotency, poison/DLQ and lock or visibility vs run time** are owned **here** (§2, §3, §6). performance `request-path-scan` § 24 keeps its greps as the **fallback** when this pack is not installed; with it installed, perf prints `→ distributed-systems messaging-scan §2/§3/§6 (k)` and does not grade (decision recorded in the batch-5 eval § 4.3). Both use the same oracle: V296 is perf V44's probe 1.
- **Worker concurrency, prefetch numbers, partitions vs consumers and the autoscaler signal** → performance `request-path-scan` § 23 (V43). §9 here keeps only the broker-API shapes (no `prefetch()`, `XREADGROUP` with no `COUNT`). **Durable work held in process memory** (`void work()` in a handler, an in-process queue driver) → § 22.
- **Money, stock and credit effects** → security `logic-race-scan` § 4 (idempotency on the consumer) and § 5 (check-then-act, the clamped debit), when the security pack is installed: §2 hands those rows over with the redelivery or stall mechanism as evidence. Without it they are reported here tagged `money consumer (owner pack not installed)`.
- **Publish or enqueue inside an open transaction** (a phantom job that reads "not found") → database `transaction-scan` § 1 (V8). **After** the commit with nothing durable between, and the outbox relay itself, → `dual-write-scan` (this pack) §1–§3. A reserve that exists but is not atomic with the effect → `dual-write-scan` § 4; §2 here owns the reserve's **absence** and its **unstable key**.
- **Retry policy across layers** (a job's `attempts` around a client that retries, the IF/WHEN/HOW of retry, a retry that repeats an earlier step) → `retry-deadline-scan` (this pack) §1–§6. §3 here owns what happens to a message that keeps failing; it corroborates `attempts` with no backoff.
- **Lock and lease helpers** that are not a broker's (a Redis leader key, `withLeaderLock`, ShedLock) → `coordination-scan` (this pack).
- **Lambda, EventBridge and SQS-to-Lambda event sources** (visibility vs function timeout, `ReportBatchItemFailures`, the event-source DLQ) → infrastructure `serverless-reliability-scan` § 2–§ 4 (`THR-QUEUE-VISIBILITY`), when that pack is installed. This skill covers non-Lambda pollers (`sqs-consumer`, `@SqsListener`, a hand loop) and prints `→ infrastructure serverless-reliability-scan §2–§4 (k)` for the rest.
- **Trace context across the queue hop** → observability `trace-propagation-scan` § 2.
- **Replaying a DLQ** is the `dlq-replay` skill (this pack); runtime DLQ depth is `/audit-distributed-tx` (the runtime lane).

## Adapt to the codebase — the broker lanes

Read every broker client **with its version** (F1). The Node lane is inline below; every other stack's grep literals, defaults and decoys are in [`stacks.md`](stacks.md), loaded only when its F1 line printed. Facts are rows of `broker-semantics.md` (tagged `[V]`/`[K]`/`[K?]` and dated there); a row tagged `[K?]` makes its verdict Unconfirmed until the settling test runs.

| Lane | Done means | Defaults that decide verdicts | Shapes to grep (pre-flight) |
|---|---|---|---|
| **BullMQ** / `@nestjs/bullmq` (`@Processor` + `WorkerHost`, `new Worker`), Bull (legacy) | the processor's promise resolves | BQ2 (`attempts` 1, `maxStalledCount` 1, `lockDuration` 30 s renewed on the event loop), BQ3 (failed set is the DLQ), BQ4 (`jobId` dedupe ends at removal), BQ5 (`deduplication` is admission only), BQ6 (`noeviction`), BQ1 (6.0 removed `repeat`), BQ9 (Bull) | 1a, 1b, 2c, 3a, 3b, 4b, 6a, 6c, 7a, 7d, 8, 11 |
| **kafkajs** / `@confluentinc/kafka-javascript` | `eachMessage` resolves (kafkajs); periodic commit every 5 s (confluent, KJ7) | KJ2, KJ3, KJ4 (`restartOnFailure` loops a poison message), KJ5, KJ6, KJ9; KJ1 (unmaintained: a migration note, never a defect) | 1c, 1d, 3c, 4a, 5a, 5b, 7a, 7c |
| **amqplib** (`amqp-connection-manager`, `@golevelup/nestjs-rabbitmq`) | `ack` | RQ4 (`nack`/`reject` requeue by default, no prefetch = unlimited, no confirms), RQ1, RQ2 (4.3: nack does not count), RQ7, RQ8 | 1e, 3d, 7b, 7c, 8, 9 |
| **SQS** (`@aws-sdk/client-sqs` loops, `sqs-consumer`) | `DeleteMessage`; sqs-consumer ≥ 14 deletes only a returned message | AW1–AW4, AW6, AW7 | 1f, 2d, 2e, 3e, 6b, 8 |
| **NATS JetStream** (`@nats-io/jetstream`, `nats` 2.x) | `ack()` | NA1 (`MaxDeliver` -1), NA2, NA3, NA5 | 1g, 2e, 3e, 6b |
| **Redis Streams** (ioredis `xreadgroup`) | `XACK` | RD1, RD3 | 1e, 3f, 8, 9 |
| Python, Java/Kotlin, Go, .NET, Ruby, PHP, Pub/Sub | per [`stacks.md`](stacks.md) | CY, KA, LD, GL, RB, LV, NT, GP rows | `stacks.md` |

A **stable id** is the key a reserve must use: rows ID1–ID9. Never `job.id` from an auto id, `deliveryTag`, `ReceiptHandle`, an SNS-fed SQS `MessageId` or a Sidekiq `jid`.

## Read the code — per consumer, before any §

F2 lists every consumer with the options it resolves to. For each one, answer these; the § that each answer feeds is in brackets.
- **What tells the broker "done", and is every effect durable before it?** Follow the handler to its last awaited write: an un-awaited call, a `void`, a `.then` without `return`, an in-memory buffer or an executor hand-off returns early [§1].
- **Which id would a redelivery carry, and is the reserve keyed on something that survives it?** Where is the reserve — in the effect's transaction, a Redis `SET NX` beside a SQL write, a read-then-write? [§2; atomicity → `dual-write-scan` §4]
- **Where does each error go?** Thrown, swallowed, `UnrecoverableError`, nack with or without requeue, a hand-written dead-letter queue, a failed set that something alerts on? [§3]
- **Does the handler's write need per-key order?** Does it overwrite state from the payload (`SET status = payload.status`) without a version check, while concurrency, a parallel batch or a retry can reorder it? [§4]
- **What is the worst run time against the lock, the visibility or the ack-wait, and does anything renew it?** A CPU-bound inline processor, a call with no timeout, a deadline that only rejects the promise and leaves the work running? [§5, §6]
- **For the producer:** is the send awaited and its failure surfaced? Does a fact another service relies on go through an outbox? Can an enqueue the caller was told failed still land later? [§7]

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). Grep **N** feeds detector **§N**; the F lines are the gates and the inventory. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (for a path several globs match, the last one wins — the repo's rg-traps lint enforces it). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). `$CONS` is the consumer-file signature every file-level grep starts from.

```bash
ROOTS=(.)   # the server-side code: in a monorepo name the apps (ROOTS=(apps/api apps/worker)); config greps always search .
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs}')
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,fuzz,stories}.*' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**')
CFG=(--hidden -g '*.{json,yml,yaml,conf,tf,tfvars,env,properties,toml,ini}' -g '**/Dockerfile*' -g '**/.env*'
     -g '!.git/**' -g '!**/node_modules/**' -g '!**/{package-lock,npm-shrinkwrap,composer}.json' -g '!**/pnpm-lock.yaml' -g '!**/yarn.lock'
     -g '!**/{test,tests,__tests__,e2e,fixtures,__fixtures__,testdata}/**' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
CONS='@Processor\(|\bextends\s+\w*WorkerHost\b|\bnew\s+Worker\(|\beachMessage\b|\beachBatch\b|\b\w*(?:[cC]h|[cC]hannel|[cC]onsumer)\.(?:consume|fetch)\(|\bConsumer\.create\(|\bnew\s+ReceiveMessageCommand\(|\.xreadgroup\(|\.consumers\.get\(|\bfor\s+await\s*\(\s*const\s+\w+\s+of\s+\w*(?:messages|sub|consumer)\w*|@(?:EventPattern|MessagePattern|RabbitSubscribe|SqsMessageHandler)\('
# F1a broker clients and their declared ranges (gate 3); F1b the locked versions; F1c broker images and managed services; F1d brokers reached by URL (external: server defaults UNREAD)
rg -n --no-heading --pcre2 '"(?:bullmq|bull|@nestjs/bullmq|@nestjs/bull|bee-queue|kafkajs|@confluentinc/kafka-javascript|node-rdkafka|amqplib|amqp-connection-manager|@golevelup/nestjs-rabbitmq|rascal|@aws-sdk/client-sqs|sqs-consumer|@ssut/nestjs-sqs|nats|@nats-io/[\w-]+|ioredis|redis|@google-cloud/pubsub|@nestjs/microservices|@nestjs/cqrs|bullmq-otel)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:bullmq|bull|kafkajs|@confluentinc/kafka-javascript|amqplib|sqs-consumer|nats|ioredis)@\d[\w.-]*|"node_modules/(?:bullmq|bull|kafkajs|@confluentinc/kafka-javascript|amqplib|sqs-consumer|nats|ioredis)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:bullmq|bull|kafkajs|amqplib|sqs-consumer|nats|ioredis)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '\bimage:\s*["\x27]?(?:[\w.-]+/)*(?:redis|valkey|rabbitmq|nats|localstack|elasticmq[\w-]*|cp-kafka|kafka|kafka-native|redpanda)[:@\s"\x27]|^\s*FROM\s+(?:[\w.-]+/)*(?:redis|valkey|rabbitmq|nats)\b|\bresource\s+"(?:aws_elasticache_\w+|aws_msk_cluster|aws_mq_broker|aws_sqs_queue|aws_lambda_event_source_mapping|google_redis_instance|google_pubsub_subscription|digitalocean_database_cluster|azurerm_redis_cache|confluent_kafka_cluster)"|^\s*Type:\s*["\x27]?(?:AWS::SQS::Queue|AWS::Lambda::EventSourceMapping|SQS)\b|\bengine\s*[:=]\s*["\x27]?(?:redis|valkey|kafka|rabbitmq)\b' "${CFG[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:REDIS|VALKEY|RABBITMQ|AMQP|KAFKA|NATS|SQS)_(?:URL|URI|HOST|BROKERS?|ENDPOINT)\b|\b(?:rediss|amqps)://|\b[\w.-]+\.(?:cache\.amazonaws\.com|ondigitalocean\.com|redis\.cache\.windows\.net|confluent\.cloud)\b|\bport:\s*2506[01]\b' "${CFG[@]}" -g '!**/package.json' . | "${NC[@]}"
# F2 the inventory: every consumer and producer with the options it resolves to and where each came from (ds-inventory.py); F2a consumer files, F2b producer lines and F2c queue registrations and worker options are its fallback when python3 is absent
DSI=.claude/skills/messaging-scan/scripts/ds-inventory.py; if command -v python3 >/dev/null 2>&1 && [ -f "$DSI" ]; then python3 -B "$DSI" .; else echo 'F2 NOT-RUN (python3 or ds-inventory.py absent): F2a-F2c are the inventory, read each consumer and producer for its options'; fi
rg -l --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --no-heading --pcre2 '\b\w*(?:[qQ]ueue|[fF]low[pP]roducer|dlq)\w*\.add(?:Bulk)?\(|\b\w*[pP]roducer\w*\.send(?:Batch)?\(|\.(?:publish|sendToQueue)\(\s*["\x27`\w]|\bnew\s+SendMessage(?:Batch)?Command\(|\.xadd\(|\bjs\.publish\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'BullModule\.register(?:Queue|FlowProducer)\w*\(|\bdefaultJobOptions\b|@Processor\(\s*[^)\n]*,\s*\{|\bnew\s+Queue\(\s*[^)\n]*,\s*\{|\bsettings\s*:\s*\{\s*backoffStrategy\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# F3 deployment shape (gate 7): replicas, autoscalers, Jobs/CronJobs, start commands per process type, TZ
rg -n --no-heading --pcre2 '^\s*replicas:\s*\d|\bkind:\s*(?:HorizontalPodAutoscaler|ScaledObject|ScaledJob|CronJob|Job)\b|\b(?:min|max)Replicas:\s*\d|^\s*(?:CMD|ENTRYPOINT)\b|^\s*-?\s*(?:command|args):|^\s*ENV\s+TZ\b|^\s*-?\s*name:\s*["\x27]?TZ["\x27]?\s*$|\bTZ=' "${CFG[@]}" . | "${NC[@]}"
# 1a BullMQ processor whose first statement is a call neither awaited nor returned (process or handle — a base class may own process()); 1b Bull done() before awaited work
rg -n --no-heading -U --pcre2 '(?:\basync\s+(?:process|handle)\s*\([^)]*\)[^{\n]*\{|\bnew\s+Worker\s*\(\s*[^,\n]+,\s*async\s*\(?[^)\n]*\)?\s*=>\s*\{)\s*\n(?:[ \t]*(?:try\s*\{\s*)?\n)*?[ \t]+(?:try\s*\{\s*)?(?!await\b|return\b|const\b|let\b|var\b|if\b|for\b|throw\b|logger\b|this\.logger\b|console\b|super\b)(?:this\.)?[\w$]+(?:\.[\w$]+)*\.[\w$]+\([^\n]*\)\s*;?[ \t]*$' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\b(?:process|handle|Worker)\s*\('
rg -n --no-heading -U --pcre2 '\(\s*job\s*,\s*done\s*\)\s*=>\s*\{\s*\n(?:[^\n]*\n){0,6}?[ \t]*done\(\s*\)\s*;?\s*\n(?=(?:[^\n]*\n){0,6}?[^\n]*\bawait\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bdone\b'
# 1c kafkajs eachMessage body not awaited; 1d resolveOffset before the work; 1e ack-free modes (amqplib noAck, sqs-consumer alwaysAcknowledge, Redis NOACK, JetStream AckNone/AckAll); 1f ack or delete as the first statement (amqplib, an SQS receive loop, JetStream)
rg -n --no-heading -U --pcre2 '\beachMessage\s*:\s*async\s*\([^)]*\)\s*=>\s*\{\s*\n[ \t]+(?!await\b|return\b|const\b|let\b|var\b|if\b|for\b|try\b|throw\b|logger\b|this\.logger\b|console\b)(?:this\.)?[\w$]+(?:\.[\w$]+)*\.[\w$]+\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\beachMessage\b'
rg -n --no-heading -U --pcre2 '^[ \t]*resolveOffset\([^\n]*\)\s*;?\s*\n(?:[^\n]*\n){0,3}?[ \t]*await\s+(?!heartbeat\b|commitOffsetsIfNecessary\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bresolveOffset\('
rg -n --no-heading --pcre2 '\bnoAck\s*:\s*true\b|\balwaysAcknowledge\s*:\s*true\b|["\x27]NOACK["\x27]|\bAckPolicy\.(?:None|All)\b|\back_policy\s*:\s*["\x27]?(?:none|all)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\.consume\(\s*[^,\n]+,\s*(?:async\s*)?\(?\s*(\w+)\s*\)?\s*=>\s*\{\s*\n\s*(?:this\.)?\w+\.ack\(\s*\1\s*\)|^[ \t]*for\s*\(\s*(?:const|let|var)\s+\w+\s+of\s+[^\n]*Messages[^\n]*\n[^\n]*(?:\bDeleteMessage(?:Batch)?Command\b|\.deleteMessage(?:Batch)?\()|for\s+await\s*\(\s*const\s+(\w+)\s+of\s+[^\n]*\)\s*\{\s*\n\s*\2\.(?:ack|ackAck)\(\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.consume\(|\bfor\b'
# 2a consumer files with no dedupe marker anywhere (perf request-path-scan 24b's list — the input, not the verdict); 2b a reserve or key built on an id the broker changes per delivery or per add
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bidempoten\w*|\bdedup\w*|\bprocessed_(?:messages|events|jobs)\b|\bON\s+CONFLICT\b|\bonConflict\w*\(|\bupsert\w*\(|\binsertOrIgnore\b|\bjobId\s*:|\bclaim\w*\('
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '(?:\b(?:key|dedupe\w*|idempotency\w*|eventId|event_id|messageId|reserve\w*)\s*[:=]\s*[^\n;]*|\b(?:insert|reserve|claim|setnx|set)\w*\([^\n]*)\b(?:job\.id|msg\.fields\.deliveryTag|deliveryTag|ReceiptHandle|message\.MessageId|m\.MessageId|jid)\b' | "${NC[@]}"
# 2c BullMQ jobId freed on completion, admission-only dedupe, and every removeOn* (read with BQ3/BQ4); 2d sqs-consumer handler that never returns the message (gate on the installed major: ≥ 14, AW4); 2e constant or random SQS group/dedupe ids, JetStream publish with no msgID
rg -n --no-heading --pcre2 '\bjobId\s*:[^\n]*\bremoveOnComplete\s*:\s*true\b|\bremoveOnComplete\s*:\s*true\b[^\n]*\bjobId\s*:|\bdeduplication\s*:\s*\{(?![^}\n]*\bttl\b)[^}\n]*\}|\bremoveOn(?:Complete|Fail)\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\bhandleMessage(?:Batch)?\s*:\s*async\s*\(\s*\w*\s*\)\s*=>\s*\{(?:(?!\breturn\b)[^{}]|\{[^{}]*\})*\}' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bhandleMessage'
rg -n --no-heading --pcre2 '\bMessageGroupId\s*:\s*["\x27][^"\x27]*["\x27]|\b(?:MessageGroupId|MessageDeduplicationId)\s*:\s*(?:crypto\.)?(?:randomUUID|uuid\w*|v4|nanoid|ulid|Date\.now|Math\.random)\(|\bjs\.publish\((?![^\n]*\bmsgID\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3a a catch with no rethrow inside a consumer file (X-SWALLOW; first line of each block); 3b failed set discarded / permanent errors never marked
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading -U --pcre2 '\bcatch\s*(?:\(\s*[\w$]+(?:\s*:\s*[\w$<>]+)?\s*\))?\s*\{(?:(?!\bthrow\b|\breturn\s+Promise\.reject\b|\bmoveToFailed\b|\bUnrecoverableError\b|\bnack\b|\bnak\b|\bterm\b|\bdeadLetter\w*|\bdlq\b)[^{}]|\{[^{}]*\})*\}' | rg --pcre2 '\bcatch\b'
rg -n --no-heading --pcre2 '\bremoveOnFail\s*:\s*true\b|\bUnrecoverableError\b|\brestartOnFailure\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3c kafkajs consumer files with no dead-letter path; 3d amqplib nack/reject that requeues (requeue defaults to true, RQ4); 3e SQS whole-batch Promise.all, JetStream bare nak(); 3f SQS batch calls that never read Failed; 3g Redis Streams readers with no reclaim
rg -l0 --pcre2 '\beach(?:Message|Batch)\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\b(?:dlq|DLQ|dead[-_.]?letter|deadLetter|\.DLT\b|retry[-_.]topic)'
rg -l0 --pcre2 '\bamqp(?:lib|-connection-manager)?\b|@golevelup/nestjs-rabbitmq|\bcreate(?:Confirm)?Channel\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\.nack\(\s*[\w.]+\s*(?:,\s*(?:false|true)\s*)?(?:,\s*true\s*)?\)|\.reject\(\s*[\w.]+\s*(?:,\s*true\s*)?\)|\bnew\s+Nack\(\s*true\s*\)' | "${NC[@]}"
rg -n --no-heading --pcre2 'Promise\.(?:all|allSettled)\(\s*(?:[\w$]+\.)?Messages\??\.map\(|\.nak\(\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '(?:SendMessageBatch|DeleteMessageBatch|ChangeMessageVisibilityBatch|PublishBatch)Command\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\.Failed\b|\[["\x27]Failed["\x27]\]'
rg -l0 -i --pcre2 '\bxreadgroup\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match -i --pcre2 '\bxautoclaim\b|\bxclaim\b|\bxpending\b'
# 4a a batch handled in parallel, the legacy or a non-murmur2 partitioner; 4b a produce with no key; 4c worker concurrency per queue (read against the handler's write); constant or random FIFO groups are 2e
rg -n --no-heading --pcre2 'Promise\.(?:all|allSettled)\(\s*batch\.messages\.map\(|\bLegacyPartitioner\b|["\x27]partitioner["\x27]\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\bmessages\s*:\s*\[\s*\{(?![^}]*\bkey\s*:)[^}]*\bvalue\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\bmessages\s*:'
rg -n --no-heading --pcre2 '\bconcurrency\s*:\s*[\w.$]+|\bpartitionsConsumedConcurrently\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5a kafkajs eachBatch with no heartbeat()/isStale() in the file; 5b session/rebalance timeouts set in code
rg -l0 --pcre2 '\beachBatch\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bheartbeat\s*\(|\bisStale\s*\('
rg -n --no-heading --pcre2 '\b(?:sessionTimeout|rebalanceTimeout|maxBytesPerPartition)\s*:|["\x27]max\.poll\.interval\.ms["\x27]\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6a lock/stall settings that shorten or skip the lock; 6b SQS/NATS handlers with a timeout but no heartbeat; 6c per-attempt deadlines (do they abort the work?) and sandboxed processors
rg -n --no-heading --pcre2 '\bskip(?:LockRenewal|StalledCheck)\s*:\s*true\b|\bmaxStalledCount\s*:\s*(?:0\b|[2-9]\b|\d{2,})|\blockDuration\s*:\s*[\w.$]+|\bstalledInterval\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bhandleMessageTimeout\s*:|\bterminateVisibilityTimeout\s*:\s*true|\.(?:consume|fetch)\(\s*\{' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bheartbeatInterval\s*:|\.working\(\)|\bInProgress\('
rg -l0 --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bwithDeadline\(|\bwithTimeout\(|\bPromise\.race\(|\bAbortSignal\.(?:timeout|any)\(|\bnew\s+Worker\(\s*[^,\n]+,\s*(?:path\.\w+\(|[`"\x27][^`"\x27\n]+\.[cm]?[jt]s[`"\x27])|\buseWorkerThreads\s*:' | "${NC[@]}"
# 7a a send or add whose promise is dropped; 7b a channel that publishes with no confirms; 7c persistent:false; 7d an enqueue raced against a timer (does the losing add still land?)
rg -n --no-heading --pcre2 '^[ \t]+(?!return\b|await\b|yield\b)(?:this\.)?[\w$]*(?:[qQ]ueue|[pP]roducer)[\w$]*\.(?:add|addBulk|send|sendBatch)\(|^[ \t]+void\s+(?:this\.)?[\w$]*(?:[qQ]ueue|[pP]roducer)[\w$]*\.(?:add|addBulk|send|sendBatch)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\.(?:publish|sendToQueue)\(\s*["\x27`\w]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\bamqp(?:lib)?\b|\bcreateChannel\(' | xargs -0 -r rg --files-without-match --pcre2 'createConfirmChannel|waitForConfirms|ConfirmChannel'
rg -n --no-heading --pcre2 '\bpersistent\s*:\s*false\b|\bdeliveryMode\s*:\s*1\b|\backs\s*:\s*(?:0|1)\b|\bidempotent\s*:\s*false\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\b\w*(?:[qQ]ueue|[pP]roducer)\w*\.(?:add|addBulk|send)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bPromise\.race\(' | "${NC[@]}"
# 8a Redis maxmemory-policy in config; 8b the policy as claimed in code comments (a pointer, precedent 34); 8c stream trims without ACKED, RabbitMQ TTL/max-length in code (read for a DLX); 8d broker and IaC retention, redrive, delivery-limit, consumer timeout; 8e a RabbitMQ queue's arguments or a policy's definition with a TTL or max-length and no dead-letter exchange in the same object (definitions.json, a values file)
rg -n --no-heading --pcre2 'maxmemory[-_]policy["\x27]?\s*[:= ]\s*["\x27]?[\w-]+|--maxmemory-policy["\x27]?[\s,]+["\x27]?[\w-]+' "${CFG[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 'maxmemory[-_]?policy|noeviction' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --no-heading -i --pcre2 '\bx(?:add|trim)\b(?![^\n]*["\x27]ACKED["\x27])[^\n]*["\x27](?:MAXLEN|MINID)["\x27]|["\x27]x-message-ttl["\x27]|["\x27]x-max-length(?:-bytes)?["\x27]|\bmessageTtl\s*:|\bexpiration\s*:' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:redrive_policy|RedrivePolicy|maxReceiveCount|message_retention_seconds|MessageRetentionPeriod|visibility_timeout_seconds|VisibilityTimeout|x-dead-letter-exchange|dead-letter-exchange|x-delivery-limit|delivery-limit|x-single-active-consumer|consumer_timeout|x-consumer-timeout|"message-ttl"|"max-length"|"overflow")\b' "${CFG[@]}" . | "${NC[@]}"
rg -n --no-heading -U --pcre2 '"(?:arguments|definition)"\s*:\s*\{(?=[^{}]*"(?:x-)?(?:message-ttl|max-length(?:-bytes)?)")(?![^{}]*"(?:x-)?dead-letter-exchange")' "${CFG[@]}" . | "${NC[@]}"
# 9a amqplib consumers with no prefetch (unlimited, RQ4); 9b prefetch(0), XREADGROUP with no COUNT
rg -l0 --pcre2 '\.consume\(\s*["\x27`\w]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\bamqp(?:lib)?\b|\bcreate(?:Confirm)?Channel\(|\bChannel\b' | xargs -0 -r rg --files-without-match --pcre2 '\.prefetch\(\s*[1-9]|\bprefetch(?:Count)?\s*:\s*[1-9]'
rg -n --no-heading -i --pcre2 '\.prefetch\(\s*0\s*\)|\bxreadgroup\b(?![^\n]*(?:["\x27]COUNT["\x27]|\bcount\s*[=:]))' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 10 broker durability config: Redis persistence, Kafka replication/acks, JetStream sync, dead mirroring policies; then NATS server configs that enable JetStream and never set sync_interval (the default fsyncs about every 2 minutes, NA4)
rg -n --no-heading --pcre2 '^\s*appendonly\s+no\b|--appendonly\s+no\b|\bmin\.insync\.replicas\s*[=:]\s*["\x27]?1\b|MIN_INSYNC_REPLICAS["\x27]?\s*[=:]\s*["\x27]?1\b|\bunclean\.leader\.election\.enable\s*[=:]\s*["\x27]?true|UNCLEAN_LEADER_ELECTION_ENABLE\s*[=:]\s*["\x27]?true|\bsync_interval\b|\bha-mode\b' "${CFG[@]}" . | "${NC[@]}"
rg -l0 --pcre2 '^\s*jetstream\s*(?::\s*)?(?:\{|enabled\b|true\b)' "${CFG[@]}" . | xargs -0 -r rg --files-without-match --pcre2 '^\s*sync_interval\b' | sed 's/^/10 no sync_interval (JetStream default, NA4): /'
# 11 version traps (gate on F1): BullMQ ≥ 6 legacy repeat API, ≥ 2 QueueScheduler; the deprecated nats npm package (F1a)
rg -n --no-heading --pcre2 '\bnew\s+QueueScheduler\s*\(|\brepeat\s*:\s*\{|\.(?:getRepeatableJobs|removeRepeatable(?:ByKey)?)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

Reading the output:
- **F1 is the version gate.** Print each client with its source: the lockfile version, or the manifest range marked `range` (its floor decides which `broker-semantics.md` rows apply). F1c with no broker image in the production manifests, plus F1d (a `*_URL` from a secret, a managed port such as 25061, a `rediss://` URL) means the server is external: its settings are `UNREAD (<service>)` unless a parameter group or config file is in the repo.
- **F2 is the subject list.** `ds-inventory.py` prints one TSV row per consumer, producer and producer wrapper — the queue, the site, `RESOLVED` or `UNRESOLVED (<why>)`, the client version (the lockfile's — pnpm, npm or yarn — marked `locked`, else the manifest range; its major gates the defaults), then every option as `key=value [source]`. A source is a `file:line`, `(call)`, `(override)`, `(forced)` for a wrapper key after the caller's spread, `default:<lane>` for a library default (applied only when F1 read the major), or `env:NAME|fallback`. Its `# candidate:` lines are pairings no grep sees (a job with `backoff: { type: 'custom' }` whose worker sets no `backoffStrategy`: BullMQ throws `Unknown backoff strategy` at retry time — `src/classes/backoffs.ts`, read 2026-10-14). Usage: `python3 -B .claude/skills/messaging-scan/scripts/ds-inventory.py <root> [--format=json] [--lane=bullmq,kafkajs,amqplib,sqs,celery,spring]`; `--self-test` checks it. The Spring lane is locate-only: its rows stay UNRESOLVED until the container factory and error-handler beans are read.
- **F3 is the process map** (gate 7): which image or command starts the workers, how many replicas, KEDA or HPA, and `TZ`.
- The **file-level lines** (2a, 3c, 3f, 3g, 5a, 6b, 7b, 9a, 10's `no sync_interval` line) list files, not lines: read each whole. 8e is an absence inside one object: a policy whose `pattern` matches the queue may still carry the DLX — read the `policies` before the row. 2a is perf's grep 24b — an **input** (consumers with no dedupe word anywhere), never a verdict.

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **A base class owns `process()`.** NestJS subclasses hold `handle()`, `@Processor` and `@OnWorkerEvent` (the explorer reads only the direct prototype), so 1a matches `handle(` too, and F2 pairs every subclass with the base that runs it.
- **A producer wrapper hides `queue.add`.** Fifty `this.enqueue(…)` calls through one base producer are one `queue.add` with fifty option sets. F2 follows the wrapper (defaults before the caller's spread, forced keys after it, subclass overrides, imported constants); a caller through an interface type is a read step.
- **The broker's own config lives elsewhere.** Quorum `x-delivery-limit`, a DLX, `maxmemory-policy`, redrive and retention sit in `definitions.json`, Terraform, a Helm chart or a provider console. Quiet greps mean "not in the repo", never "not configured" (precedent 5).

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples (BullMQ, kafkajs, amqplib, SQS, NATS, Redis Streams TS files, bad and good) | 0.4 s, 0 rg errors. **Every BAD line surfaces in its §**: un-awaited `process` (1a), Bull `done()` first (1b), un-awaited `eachMessage` (1c), `resolveOffset` first (1d), `noAck` and `NOACK` (1e), ack-first amqplib, delete-first SQS loop and ack-first JetStream (1f), `jobId` + `removeOnComplete: true` and `deduplication` with no `ttl` (2c), void sqs-consumer handler (2d), constant `MessageGroupId` + random dedupe id (2e), swallowed catch (3a), requeueing `nack`/`reject` ×3 (3d), `Promise.all` over `Messages` and a bare `nak()` (3e), batch `Failed` ignored (3f), `xreadgroup` with no reclaim (3g), parallel batch + `LegacyPartitioner` (4a), key-less produce (4b), `eachBatch` with no heartbeat (5a), `skipLockRenewal` + `maxStalledCount: 5` + 5 s lock (6a), `handleMessageTimeout` with no heartbeat (6b), un-awaited `add` (7a), non-confirm channel (7b), `acks: 1` + `idempotent: false` (7c), `x-message-ttl` and `MAXLEN` with no `ACKED` (8c), no `prefetch` (9a), `XREADGROUP` with no `COUNT` (9b), `repeat:` + `QueueScheduler` (11). Good files print only inventory lines the read step clears: a 60 s `lockDuration` (6a), a `jobId` with an age-bounded `removeOnComplete` (2c), a sandboxed processor (6c), and one kafkajs consumer with no DLQ topic (3c, read: does it throw into `restartOnFailure`?) |
| Seeded tree for greps the samples lack (12 files) | `handle()` un-awaited behind a base `process()` (1a), a reserve keyed on `job.id` and a provider key from `job.id` (2b), a JetStream `fetch` loop with no `working()` (6b), `maxmemory-policy allkeys-lru` in `redis.conf` and in a compose `command` array (8a), `appendonly no`, `KAFKA_UNCLEAN_LEADER_ELECTION_ENABLE` and `KAFKA_MIN_INSYNC_REPLICAS` (10). The decoys — a processor awaiting its effect behind `inbox.reserve`, a fetch loop that calls `working()` — never appear |
| Real repository (NestJS 11 + Fastify, `@nestjs/bullmq` 11.0.5, BullMQ 6.3.4 and ioredis 5.11.1 locked in `pnpm-lock.yaml`, managed Valkey; read-only, about 11,100 files) | Re-run on the full tree 2026-10-14 (lockfile, CI and the shared packages readable): 6.1 s with `ROOTS=(.)`, 4.1 s with the API app, the same lines both ways. F1b prints the locked versions, and since 2026-10-14 so does `ds-inventory.py`'s version column (`bullmq 6.3.4 locked (pnpm-lock.yaml; ^6.3.4 in apps/api/package.json)` on all 20 rows; the manifest range before); F1c 3 `redis:7-alpine` images, all in dev compose files and CI services, none in a production manifest; F1d the managed-cache ports plus local `REDIS_URL`s → the server is still external. F2a **8 consumer files** (7 processors + the base that owns `process()`). §1 **0** (1a covers `handle()`); 2a 6 files (input); 2c the 3 `removeOn*` lines (a count of 1,000 keeps the last 1,000 completed: `jobId` dedupe ends by count, BQ4 — read every effect that relies on it); §3 **1 → 0** (the `catch` in an `onFailed` that files a report after the dead letter is kept: Refuted at gate 4); 4c 7 concurrency lines, all `env:WORKER_CONCURRENCY|5`; 6c the base's aborting `withDeadline` (the precedent-36 control); 7d **1** — the enqueue raced against a timer: an `add` already in ioredis's offline queue may still land after the caller got 503 (Unconfirmed, V297's stall-then-recover variant; the producer now checks a `live()` flag before `queue.add`, so only an add issued before the timer fires can land); §8: no policy in config, 8b one code comment claiming `noeviction` (three on the earlier partial copy; deploy comments and an alert rule say the same — claims, not config), F1d a managed-cache port → **Unconfirmed (policy UNREAD)**, precedent 34; §11 **0** on BullMQ 6 (no `repeat:`). Two first-draft false positives were fixed before shipping: the consumer signature matched two `.consume()` calls on token stores (10 → 8 consumer files, 3a 5 → 1), and the requeue grep matched `Promise.reject(…)` and a port's `reject(…)` (3 → 0, now scoped to amqp files) |
| `ds-inventory.py` on the same repo | 2.5 s. **20/20 rows resolved** (gate: ≥ 90 %): 7 consumers (queue, `concurrency`, the spread `limiter`, the per-queue `backoffStrategy`, default `lockDuration`/`maxStalledCount` from BQ2, the base that owns `process()`, the deadline resolved through `super(…)` to 165 000 ms or `env:JOB_TIMEOUT_MS|30000`, `@OnWorkerEvent('failed')`) and 13 producer rows over 9 producer classes (one wrapper, eight subclasses, one external caller), each with `attempts`, `backoff`, `removeOn*` and `jobId` traced to the wrapper, the override and the imported constants. One `# candidate:` line: a queue whose jobs carry a custom backoff at 3 attempts while its worker sets no `backoffStrategy` (§3). Full tree: the same 20/20 and the same candidate; the version column still prints the manifest range (`bullmq ^6.3.4`) with a lockfile present, whose 6.3.4 equals the range floor, so no default moves. Read at 6.3.4 (BullMQ's `v6.3.4` tag): `Job.shouldRetryJob` awaits `Backoffs.calculate` with no catch, so `moveToFailed` rejects before any state is written, the worker emits `error` instead of `failed`, and the job is left to stall recovery — the row stays Unconfirmed until V293 shows what a real failing job does |
| `benchmarks/fixtures/*` (18 fixtures) | Quiet: F1–F3 context in 7 fixtures; detector greps 0 except brittle-suite 2c (a `removeOnComplete: 1_000` in `defaultJobOptions`, inventory) and obs-defects 2a (one consumer file, input). infra-ops prints 46 IaC queue lines in 8d, all Lambda-fed → `→ infrastructure serverless-reliability-scan §2–§4`. Narrowed before shipping: 6c from 20 lines over 11 fixtures (`AbortSignal.timeout` in frontend fetches) to consumer files only (0), F1c from 61 to 20 (resource declarations only, not references) |

## The 3,000-hit path

1. **Intersect** with F3: a consumer in code no production process type starts is dismissed with one read (a script, a seed, `apps/web` for server classes). Name the directory in the coverage block.
2. **Group by root cause**: one base processor, one producer wrapper, one retry or backoff constant, one queue definition file is **one** finding with N sites. Fifty consumers inheriting one `process()` that acks early are one row.
3. **Rank**: consumers whose effect moves money or stock, sends a customer message or creates an order first; then ordered streams; then the rest.
4. **Read the top 30 groups** with the read-the-code questions; sample 10 sites per group, and the rest inherit the verdict with the group's id.
5. **Run the bulk oracle once**: the duplicate-replay harness (V292) over the top consumer of each group, against a broker container.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production consumer reached by F3. A row on a consumer that creates orders, moves stock or sends customer messages is **BLOCKER** for §1, and for §3 when one poison message blocks an ordered partition or queue on a revenue path. Money effects are security's (§ Boundaries).

| § | Classes | Default severity |
|---|---|---|
| 1 | MQ-1 ack, commit or delete before the effect | high; BLOCKER as above |
| 2 | MQ-2 at-least-once with no idempotent consumer, or a reserve on an unstable id | high with an external or financial side effect; medium for an internal idempotent-by-luck write |
| 3 | MQ-3 poison: requeue loop, no DLQ, swallow-and-ack, whole-batch retry | high; BLOCKER as above |
| 4 | MQ-4 ordering assumption broken | high where a per-key state is overwritten; else not a row (precedent 8) |
| 5 | MQ-5 consumer-group rebalance | medium; high with a non-idempotent effect |
| 6 | MQ-6 lock, visibility or ack-wait shorter than processing (non-serverless) | high with a non-idempotent effect; medium otherwise |
| 7 | MQ-7 producer fire-and-forget, no confirms, weak acks | high for a fact another service relies on; medium |
| 8 | MQ-8 retention, TTL or eviction drops unprocessed work | high (silent loss); Unconfirmed on a managed broker |
| 9 | MQ-9 unbounded consumer buffering (broker API only) | medium |
| 10 | MQ-10 broker durability configuration | medium; high when the queue carries money or orders |
| 11 | MQ-11 library and version traps | the class the trap causes |

### 1. Ack, commit or delete before the effect (MQ-1)

```
BAD:   async handle(job) { this.mailer.sendReceipt(job.data.orderId) }          // returns at once: BullMQ marks the job completed (BQ2)
       eachMessage: async ({ message }) => { this.handler.handle(parse(message)) }   // offset committed as soon as it resolves (KJ2)
       for (const m of batch.messages) { resolveOffset(m.offset); await handle(m) }
       ch.consume('orders', async (msg) => { ch.ack(msg); await process(msg) }) · { noAck: true } on business work
       for (const m of Messages) { await sqs.send(new DeleteMessageCommand(…)); await handle(m) }
GOOD:  await (or return) the whole effect chain; ack, resolve, delete after the last durable write
```
**Read the code:** Is every effect awaited before the handler returns — no `void`, no `.then` without `return`, no in-memory buffer, no executor? Is the broker told "done" before the effect: `noAck`, ack first, delete first, `alwaysAcknowledge` with a catching handler, an `AckAll` policy under concurrency (NA2)? Is the loss a written choice (telemetry, a cache ping, precedent 6)? A fully awaited handler under auto-commit is at-least-once, not MQ-1 (precedent 1). **Finding when** a crash between "done" and the effect loses the work. **Proof (V291):** the handler blocks on a latch after the ack, the consumer is killed (`SIGKILL`, `docker kill`), restarted: the message is gone (fails); after the fix it is redelivered and the effect count is 1.

### 2. At-least-once with no idempotent consumer, or an unstable reserve id (MQ-2)

```
BAD:   await this.psp.charge(job.data.orderId, { idempotencyKey: job.id })    // auto id: a re-add is a new id (ID4)
       queue.add('charge', d, { jobId: order.id, removeOnComplete: true })     // the id is free again after completion (BQ4)
       queue.add('x', d, { deduplication: { id } })                           // admission only (BQ5)
       handleMessage: async (m) => { await processOrder(m) }                  // sqs-consumer ≥ 14: never deleted, redelivered (AW4)
       dedupe on m.MessageId for an SNS-fed queue (AW6) · MessageDeduplicationId: randomUUID()
GOOD:  a unique reserve on a business or publisher-set id (ID1–ID9) written in the effect's transaction, or a conditional transition
       (UPDATE … WHERE status = 'pending'); a provider idempotency key from the business id; `return m` / `strictReturn`
```
**Read the code:** Start from 2a (consumers with no dedupe word) and from every consumer whose effect writes or calls out. Which id would a redelivery, a stall re-run (BQ2: `maxStalledCount` 1 re-runs a job **once even at `attempts: 1`**) or a producer retry carry? Is the effect naturally idempotent (an upsert by business key, a `SET`, a guarded transition — precedent 2)? Is the guard a read-then-write (not a reserve), an in-memory set (precedent 3), or "exactly-once" config that covers producer duplicates only (precedent 4)? Does a `jobId` dedupe survive the `removeOn*` the inventory resolved? A money, stock or credit effect goes to security (§ Boundaries) with the mechanism as evidence. **Finding when** a second delivery of the same message produces a second effect. **Proof (V292):** deliver the same message twice, sequentially and then concurrently behind a barrier, against the real broker: the effect count is 2 before the fix, 1 after.

### 3. Poison: requeue loop, no DLQ, swallow-and-ack, whole-batch retry (MQ-3)

```
BAD:   catch (e) { ch.nack(msg) }                      // requeue defaults to true (RQ4); on RabbitMQ ≥ 4.3 nack never reaches the delivery limit (RQ2)
       try { await charge(job.data) } catch (e) { logger.error(e) }   // swallowed: completed, never retried, never in the failed set
       removeOnFail: true  ·  kafkajs handler throwing on bad JSON (restartOnFailure loops the partition, KJ4)
       await Promise.all(Messages.map(handle)) then delete all   // one failure redelivers the whole batch
       backoff: { type: 'custom' } with no worker backoffStrategy (F2 # candidate)
GOOD:  nack(msg, false, false) + a DLX and x-delivery-limit · throw UnrecoverableError for permanent errors · bounded attempts with backoff
       and a dead-letter something alerts on · a DLQ topic with the original key and headers · per-message delete as each succeeds
```
**Read the code:** For each consumer, where does a permanent error end — a DLQ, the failed set, a hand-written dead-letter queue, nowhere? Is the attempt count bounded (`attempts`, `MaxDeliver`, `x-delivery-limit`, `maxReceiveCount`) and is that bound real at the server version (RQ2: a nack does not count on 4.3)? Is the `catch` the job's own failure, or a best-effort step after the dead letter is kept (the real-repo decoy)? Does anything alert on the DLQ? A bounded nack checking an attempt counter is precedent 7; a DLQ defined in another repo is precedent 5 once read. **Finding when** one bad message loops, blocks its partition or group, vanishes, or retries the whole batch. **Proof (V293):** 1 poison + 100 good against the broker: the 100 drain within budget, the poison lands in the DLQ after N attempts, no hot loop (fails before the fix).

### 4. Ordering assumption broken (MQ-4)

```
BAD:   await Promise.all(batch.messages.map(handle))   on an order-state topic   ·   producer.send({ topic, messages: [{ value }] })   // no key
       createPartitioner: Partitioners.LegacyPartitioner in one service, the default in another (KJ6; librdkafka CRC32, LD4)
       kafka-go kafka.Message{Value: body} on a CRC32Balancer (or no Balancer: round-robin) beside a Java murmur2 producer (GL5, stacks.md G5)
       concurrency: 10 on a queue whose handler sets status from the payload · MessageGroupId: 'orders' or randomUUID()
GOOD:  a key per entity, per-key serial handling (partitionsConsumedConcurrently keeps partition order, KJ9), a version guard on the write
```
**Read the code:** Does the handler's write need per-key order (a state machine, a balance, last-write semantics), or is the effect commutative (precedent 8)? Is order already kept by the key, the group id, a single active consumer or a `WHERE version < :v` guard (precedent 9)? Do retries or backoff move a message behind later ones? Relay order is `dual-write-scan` §3. **Finding when** two messages for one key can apply out of order and the second overwrites the first. **Proof (V294):** emit v1..v100 for one key with a transient failure on v3: the final state is v100 and the handler saw v1..v100 in order.

### 5. Consumer-group rebalance (MQ-5)

```
BAD:   eachBatch: async ({ batch, resolveOffset }) => { for (…) { await slow(m); resolveOffset(m.offset) } }   // no heartbeat(), no isStale()
       a handler whose p99 exceeds sessionTimeout (KJ3) or the confluent rebalanceTimeout (KJ7)
GOOD:  await heartbeat() and check isRunning()/isStale() in the loop; handler p99 well under the timeout; an idempotent effect anyway
```
**Read the code:** What is the handler's p99 (a metric, a test timing, a stated budget) against `sessionTimeout`, `rebalanceTimeout` or `max.poll.interval.ms`? Both terms must be cited (tier S); with the p99 unknown the row is Unconfirmed with the metric to read. Partitions vs consumers is capacity → perf § 23. **Finding when** a rebalance during processing hands an in-flight message to a second member, or commits past an unprocessed one. **Proof (V295):** two consumers, a handler slower than the poll interval, a third consumer joins: effect count per message stays 1 and no committed offset passes an unprocessed message.

### 6. Lock, visibility or ack-wait shorter than processing (MQ-6, non-serverless)

```
BAD:   a 40 s CPU-bound PDF render inline in the processor at the default lockDuration 30 s (renewal runs on the blocked event loop, BQ2)
       skipLockRenewal: true · maxStalledCount: 5 · lockDuration: 5000 on a 20 s job
       handleMessageTimeout with no heartbeatInterval (AW4) · a JetStream fetch loop with no working()/InProgress() past AckWait 30 s (NA1)
GOOD:  a sandboxed processor (new Worker(q, path)) for CPU work, a heartbeat or lock extension, a deadline that aborts the work — and an idempotent effect
```
**Read the code:** What is the worst run (the deadline the base processor enforces, the outbound timeouts × attempts, a measured p99)? Does a deadline **abort** the work, or only reject the promise while the work runs on beside the retry (precedent 36)? Is the processor CPU-bound and inline? `THR-DS-CONSUMER-TIMING`: the lock or visibility is ≥ 2 × p99, or a heartbeat renews it at ≤ 1/3 (Kafka: `max.poll.interval.ms` ≥ 1.5 × `max.poll.records` × p99 per record). Lambda event sources are infrastructure's (`THR-QUEUE-VISIBILITY`). **Finding when** the work can outlive its lock or visibility while nothing renews it and the effect is not idempotent. **Proof (V296, = perf V44 probe 1):** a job running 1.5 × the lock or visibility against the real broker gives exactly 1 effect after the fix (2 before). Use small real durations, never fake timers, for lock expiry.

### 7. Producer: fire-and-forget, no confirms, weak acks (MQ-7)

```
BAD:   this.ordersQueue.add('charge', { id })        // not awaited: a Redis failure is an unhandled rejection, the caller saw success
       ch.publish(…) on createChannel() (no confirms, RQ4) · persistent: false on a durable queue · acks: 1 / idempotent: false (KJ5)
       Promise.race([queue.add(…), timeout]) answering 503 while the losing add still lands later
GOOD:  await the send and surface its failure · a confirm channel + waitForConfirms · an outbox for facts others rely on
```
**Read the code:** Is the send awaited, and does its failure reach the caller or a retry? For a race-bounded enqueue: can an `add` already handed to the client (ioredis's offline queue holds commands while disconnected) execute after the timer fired, and does the caller retry the 503 with no dedupe key? Is the event a fact another service relies on — then the after-commit half is `dual-write-scan` §1. `void work()` that is in-process work, not a send, is perf § 22. A telemetry send with a written loss budget is precedent 6. **Finding when** the producer reports success while the message can be lost, or a refused enqueue can still land. **Proof (V297):** stop or pause the broker container, call the use case: it must fail visibly or persist to an outbox (fails before the fix); the stall-then-recover variant counts the jobs that land after the refusal.

### 8. Retention, TTL or eviction drops unprocessed work (MQ-8)

```
BAD:   maxmemory-policy allkeys-lru on the Redis that holds BullMQ or Sidekiq jobs (BQ6) · XADD … MAXLEN ~ N with a lagging group (RD1)
       'x-message-ttl' / 'x-max-length' with no dead-letter exchange · a standard-queue DLQ retention ≤ the source's (AW3)
GOOD:  noeviction on a dedicated job Redis · an ACKED or MINID trim on 8.2+ · a DLX on every TTL'd queue · DLQ retention 14 d
```
**Read the code:** Which server holds the jobs, and is its policy in the repo (8a, 8d) or only claimed in a comment (8b, precedent 34)? A managed cache with no parameter group is `UNREAD (<service>)` (RD5): the row is Unconfirmed with the provider setting to read. Is a trim or a TTL tied to the slowest consumer? **Finding when** unprocessed work can be evicted, trimmed or expired with no dead-letter. **Proof (V298):** fill the broker past the limit or advance past the TTL against a container: the message is in the DLQ or processed, never silently gone.

### 9. Unbounded consumer buffering — broker API shapes (MQ-9)

```
BAD:   ch.consume(q, handler) with no ch.prefetch(n), or prefetch(0) (RQ4) · XREADGROUP … STREAMS s > with no COUNT (RD3)
GOOD:  ch.prefetch(10) · XREADGROUP COUNT 100 · a bounded pool over the receive batch
```
**Read the code:** Can the broker push more unacked messages than the process can hold? The numbers (prefetch vs throughput, partitions vs consumers) are perf § 23; executors are § 14. **Finding when** the consumer can buffer the whole backlog in memory. **Proof (V299):** publish 100 k: RSS stays under budget and unacked ≤ prefetch.

### 10. Broker durability configuration (MQ-10)

```
BAD:   appendonly no on the job Redis · KAFKA_MIN_INSYNC_REPLICAS 1 with acks all · unclean.leader.election.enable=true
       a JetStream payments stream without sync_interval: always (NA4) · ha-mode mirroring on RabbitMQ ≥ 4.0 (dead config, RQ9)
GOOD:  persistence on the store that holds work; min.insync.replicas ≥ 2 with replication 3; sync_interval: always where an ack must survive a crash
```
**Read the code:** Is the config the production broker's (a compose file for local dev is not), and does code depend on it (a queue carrying orders)? Both ends cited (tier S). A managed broker is Unconfirmed. **Finding when** the production broker can lose an acknowledged message on a crash or failover. **Proof:** the static fact with both ends; there is no V-slot.

### 11. Library and version traps (MQ-11)

```
BAD:   repeat: { … } on BullMQ ≥ 6 (BQ1) · new QueueScheduler( on BullMQ ≥ 2 (BQ7) · a void sqs-consumer handler after an upgrade to ≥ 14 (AW4)
       processing.guarantee=exactly_once on Kafka Streams ≥ 4 (KA5) · code relying on the quorum delivery limit to stop nack loops on RabbitMQ ≥ 4.3 (RQ2)
GOOD:  upsertJobScheduler · return the message · exactly_once_v2 · reject, or nack with requeue false + a DLX
```
**Read the code:** Which version is installed (F1), and which dated change in `broker-semantics.md` § Dated changes crossed it? kafkajs (KJ1) and the `nats` npm package (NA5) are migration notes, never a row. MassTransit 9 is commercial (NT1): never recommend the upgrade as a fix. **Finding when** the installed version changed a behaviour the code relies on. **Proof:** the version read from the lockfile plus the row's dated change; the class oracle of the behaviour that changed.

## Output

```
messaging-scan coverage — scope=whole repo  stacks=bullmq 6.3.4, ioredis 5.11.1 (pnpm-lock.yaml) · server: Valkey (managed) UNREAD
Inventory: 7 consumers, 13 producer rows (1 wrapper), 20/20 resolved · processes: api (HPA 2–10), worker (KEDA)

Findings: 0 · Unconfirmed: 3

1. apps/api/src/queue/base.producer.ts:150                                        [report-flagged]   medium
   §7 MQ-7 — part A: the shared enqueue wrapper. Part B: `Promise.race` answers 503 at 3 s while an `add` already in ioredis's
   offline queue runs when Redis returns; a caller that retries the 503 without a dedupe key enqueues twice. Settling test:
   V297 stall-then-recover — pause Redis, enqueue, resume, count jobs.
2. apps/api/src/queue/shipping-label.producer.ts:34 · apps/worker/src/jobs/shipping-label.processor.ts:29[report-flagged]   medium
   §3 MQ-3 — jobs carry backoff { type: 'custom' } at attempts 3 (base.producer.ts:205, queue.constants.ts:64) and the worker
   sets no backoffStrategy. Settling test: V293 with one failing job — does attempt 2 run?
3. deploy (no maxmemory-policy) · apps/api/src/redis/connection.ts:26 (comment claims noeviction)  Unconfirmed
   §8 MQ-8 — BullMQ needs noeviction (BQ6); the managed cache's policy is UNREAD (RD5). Read: the provider's config.

Verification: 14 candidates → 0 findings · 3 unconfirmed · 1 hardening · 10 refuted (self-verified)

Class coverage:
  §1  ack before effect          checked (8 consumer files → 0)
  §2  consumer idempotency       checked (6 files with no marker → 0; 3 removeOn* resolved, BQ4) · → security logic-race-scan §4 (0)
  §3  poison / DLQ               checked (1 → 0 refuted; 1 inventory candidate → unconfirmed)
  §4  ordering                   checked (7 concurrency lines → 0; no per-key overwrite)
  §5  rebalance                  N/A (no Kafka client in any manifest)
  §6  lock vs run                checked (lockDuration default 30 s, BQ2; deadline aborts, precedent 36 → 0)
  §7  producer                   checked (1 → 1 unconfirmed)
  §8  retention / eviction       Unconfirmed (managed Valkey policy UNREAD)
  §9  buffering                  N/A (no amqplib or Redis Streams consumer)
  §10 broker durability          Unconfirmed (no broker config in the repo; managed)
  §11 version traps              checked (BullMQ 6 range, BQ1; 0)
  → infrastructure serverless-reliability-scan §2–§4 (0) · → observability trace-propagation-scan §2 (1 queue client)
```

`[report-with-fix]`: the oracle failed on the unfixed code against the real broker, and the fix is local to the project's base processor, producer wrapper, queue definition or reserve helper. `[report-flagged]`: one link is unproven (no container run, a managed setting UNREAD, a p99 not measured); the row names it and the settling test. The coverage block lists **all eleven** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 1** auto-commit with a fully awaited handler is at-least-once, not MQ-1 (flips back on an executor, a buffer, an un-awaited promise, librdkafka's offset store, LD1).
- **§ 2** a naturally idempotent effect needs no inbox; **§ 3** an in-memory set is never a reserve; **§ 4** "exactly-once" settings clear producer duplicates only.
- **§ 5** a DLQ configured in another repo is a control once read; **§ 6** at-most-once by written decision; **§ 7** a bounded nack is not a loop.
- **§ 8** ordering matters only under a per-key invariant; **§ 9** per-key serialisation is the control.
- **§ 32** one replica by design does **not** make MQ classes latent: redelivery and broker crashes happen on one replica too. **§ 33** mocked brokers prove nothing.
- **§ 34** a comment claiming `noeviction`, "idempotent" or "one replica" is a pointer, not evidence (refute-before-report § 7). **§ 36** a deadline that aborts the work is the control for a retry running beside the original.

Shapes this skill must not report: a `catch` in a failure hook that runs after the dead letter is kept; a `jobId` used only for lookup; `concurrency > 1` on commutative jobs; `noAck` on a presence or cache-bust fan-out with a written loss budget; a `Promise.all` over messages grouped by key and handled serially per group.

## When to run

- On any diff that touches a producer, a consumer, a base processor or producer wrapper, a queue registration, a broker client version, or broker config (`definitions.json`, `redis.conf`, compose, IaC queues) — `/ds-audit`'s "a producer, consumer or broker config file" signal.
- On every whole-repo `/ds-audit`, reporting all eleven §s; before raising worker concurrency, adding a second worker fleet, or upgrading a broker client across a dated change.
- After `/add-event-handler`: its Phase 6 runs V292 and V303 from the same oracle file.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the `broker-semantics.md` row, the version lines and the F2 row — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt before any § when F1 is unread.** A verdict resting on a default whose version is unknown is invalid; when no `broker-semantics.md` row covers the installed range, the row is Unconfirmed with the release notes to read.
- **Halt on any finding missing its anchors:** the consumer or producer `file:line`, the delivery event, the `broker-semantics.md` row, the effect, the fix in the project's own primitive.
- **No `[report-with-fix]` without a container oracle that failed** (or a two-ended static fact for §5, §6 and §10). A mocked broker, eager mode or an in-memory harness is not one.
- **No proposed fix may trade a duplicate for a loss** without a written decision: `attempts: 1`, `maxStalledCount: 0`, `noAck: true`, `removeOnFail: true`, `alwaysAcknowledge: true`, or a bigger lock or visibility where a heartbeat and an idempotent effect belong.
- **Never contact a broker outside a scratch container**, and never run `kubectl`, `helm` or a cloud CLI against a default context or profile; the live lane is `/ds-audit --live` only, read-only, with an isolated `KUBECONFIG`.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "queues look fine"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Delivery, Order and groups and Producers and brokers ledger rows; `/ds-fix` closes findings with the failing-first oracle, the fix at the root primitive, a re-run of this detector and the sibling sweep.
- `dual-write-scan`, `retry-deadline-scan` and `coordination-scan` (this pack) are the neighbours named in § Boundaries; `/add-event-handler` builds consumers that pass §1–§3; `dlq-replay` drains what §3 dead-letters; `@resilience-reviewer` judges these rows.
- performance `request-path-scan` § 22–§ 24, security `logic-race-scan` § 4–§ 5, database `transaction-scan` § 1, infrastructure `serverless-reliability-scan` § 2–§ 4 and observability `trace-propagation-scan` § 2, when those packs are installed.

## Sources

Defaults are rows of `broker-semantics.md` (read 2026-10-14 from bullmq `src/classes/worker.ts` and docs, kafkajs docs, confluent `MIGRATION.md`, amqplib `lib/api_args.js`, rabbitmq.com *Quorum queues* and *Consumers* 4.3, the SQS Developer Guide, bbc/sqs-consumer v14 release and README, nats-server `consumer.go`, redis.io `XADD`/`XREADGROUP`, celery `app/defaults.py`). Fetched for this skill on 2026-10-14: bullmq `src/classes/backoffs.ts` (an unknown backoff type throws `Unknown backoff strategy`). Grep literals are the distributed-systems research notes A (BMQ, KJS, RMQ, SQS, NATS, RS ids, tested on the research samples 2026-10-14) and the batch-5 eval § 3.2 and § 3.8, re-measured here. Paraphrased; no text reproduced beyond identifiers.
