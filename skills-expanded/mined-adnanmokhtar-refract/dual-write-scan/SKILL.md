---
name: dual-write-scan
description: "Dual write: commit/publish order, outbox use, relay, inbox atomicity, CDC, gap-blind cursors — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: dual-write-scan

## Premise

A use case that commits a row and then publishes an event writes to two systems that share no commit. A crash, a deploy or a broker error between the two loses the event: the order exists and the warehouse never hears of it. Publish first and a rollback leaves an event for a state that never committed. The usual cure, a transactional outbox, moves the problem rather than ending it: its relay can mark a row sent before the broker confirmed it, publish rows in parallel and out of order, or hold row locks across the network call; its consumers can keep their dedupe reserve in Redis while the effect lands in SQL; a CDC connector can re-emit a snapshot or drop an UPDATE; and a catch-up cursor (`WHERE id > $last`) can step over a row whose transaction commits late. Each is silent: both stores look healthy, and they disagree. This skill finds those places and proves each with its oracle against a real database and broker in containers. Read-only: it never edits code and never touches a store that is not a scratch container.

**The project's own outbox writer is the control, and it is resolved first.** On a hardened real repository, 27 of the 28 write-then-publish matches went through the project's outbox port, which persists an outbox row inside the caller's transaction. A lane that does not find the port before it lists candidates prints 96 % noise. The pre-flight therefore resolves the writer (F2): the code that inserts an outbox row, the class that holds it, the interface it implements, and every field typed as either. Calls through those receivers are tagged `outbox port`. The writer is verified **once**, not per call site: does it write through the caller's transaction handle?

It owns `/ds-audit`'s Dual write ledger row (§1–§6). `@resilience-reviewer` (this pack) judges its rows.

**Every finding cites the write `<file:line>` + the publish, mark, reserve or cursor `<file:line>` + the crash point between them + the outbox writer it bypasses, or `no outbox` (F2 printed none) + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row when a framework or library default decides (OX1–OX7, ID1–ID9, NT2, CY5, RB3, RB4, LV1, KA10, BQ4) + the oracle that showed it, or the test that would settle it + the fix in the project's own primitive** (its outbox port, its relay, its inbox helper). A grep hit is a candidate. "Events look consistent" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) (§ 10–13 dual write and outbox). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V300–V303, with V292's concurrent variant.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them.

1. **Part A holds: this is a write and a publish of a fact another process consumes**, on a path a deployed process runs (F3). A broker publish, an enqueue, an SNS/EventBridge put, a webhook to another service. A one-off script, a seed or a test fails here (refute-before-report § 4). An in-process event bus (`@nestjs/cqrs` `EventBus`, Spring `ApplicationEventPublisher`) is a publish only through what its handlers do (OX6). A customer email or SMS sent after commit is an external effect judged by precedent 6 when its loss is a written choice.
2. **Part B holds: nothing durable sits between the two writes.** No outbox row in the same transaction, no framework outbox (precedent 11), no reconciler that re-derives the event from state (precedent 10). A verdict that rests on a framework's behaviour names its row: after-commit helpers close the phantom and keep the loss window (OX5, CY5, RB3, LV1); a MassTransit publish after the last `SaveChangesAsync` under the bus outbox is never persisted (NT2, `[K?]`); Spring's chained Kafka + DB manager is best-effort 1PC (KA10).
3. **Nothing already controls it**, across files. The outbox port's implementation joins the caller's transaction; the relay marks only after the broker confirmed; the consumer's reserve lives in the effect's transaction (precedent 2 and its amendment: an effect table that carries the event id, read through an anti-join, *is* the reserve). **Read the whole file and its callees**: in the real-repo run every one of 27 matches was refuted only by the port's implementation in another module.
4. **The oracle fired, or the fact is two-ended.** A container oracle (tier C) shows the lost, phantom, duplicated, reordered or skipped event, or a static fact cites both ends (a connector config value and the consumer that depends on it). Without one, the row is `[report-flagged]` / Unconfirmed with the settling test written out. A mocked broker or an in-memory bus is not a tier (precedent 33).

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **Publish or enqueue inside an open transaction** — the phantom job that reads "not found", Celery `delay` in `atomic`, Rails `after_save` mailers, Laravel `dispatch` in `DB::transaction`, enqueue before commit (backend BJ-01) — is database `transaction-scan` § 1 (V8), when the database pack is installed. This skill **routes, never detects** it: 1d prints the transaction openers in each candidate's file, and a publish inside the callback is listed `→ database transaction-scan §1 (k)`. Without the database pack it is reported here, tagged `in-transaction publish (owner pack not installed)`. **After** the commit with nothing durable between is §1 here.
- **The relay's claim**: a claim without `SKIP LOCKED` across several relays → database § 5; row locks or a claim transaction held open across the publish → database § 1 (external I/O inside a transaction). §3 here owns order, parallel publish, mark before a confirmed publish, no relay, no pruning, and the relay's lease.
- **The outbox writer outside the caller's transaction** (a second connection, a repository not taken from the transaction's handle) is §1's "outbox misused"; database `transaction-scan` § 2 lists the same `file:line` as corroboration.
- **A consumer with no reserve, or a reserve on a broker id that changes on redelivery** → `messaging-scan` § 2 (this pack). §4 here owns a reserve that exists but is not atomic with the effect, and its retention.
- **Money, stock and credit effects** → security `logic-race-scan` § 4–§ 5, when the security pack is installed: §4 hands those rows over with the two-store mechanism as evidence. Without it they are reported here, tagged `money effect (owner pack not installed)`.
- **A relay's leader lease** whose `extend()` result is dropped is §3's; everywhere else → `coordination-scan` § 4 (this pack). **A cursor floor minted on several hosts' clocks** is §6's; `coordination-scan` § 8 corroborates on the clock half.
- **Producer fire-and-forget and missing confirms** → `messaging-scan` § 7. **Event schema changes, event-store appends without an expected version and a projection checkpoint outside the projection's transaction** → `event-contract-scan` § 1, § 6 and § 8 (this pack).
- **Batch ELT watermarks over OLTP tables** (a nightly or incremental load that copies rows by `updated_at`) → data-engineering `incremental-load-scan` §1, when installed. §6 here keeps the gap-blind catch-up cursor of an event, outbox or CDC relay.
- **Model callbacks with side effects** (backend BS-04): inside the transaction → database § 1; after the commit with nothing durable → §1 here.
- **Outbox lag and backlog at runtime** → `/audit-distributed-tx` (the runtime lane).

## Adapt to the codebase — the outbox lanes

Read the ORM, the broker client and any outbox framework **with its version** (F1). Facts are rows of `broker-semantics.md` (tagged `[V]`/`[K]`/`[K?]` and dated there); a row tagged `[K?]` makes its verdict Unconfirmed until the settling test runs.

| Lane | The control that clears §1 | What does not clear it | Rows |
|---|---|---|---|
| **Hand-written outbox port** (MikroORM, TypeORM, Prisma, Drizzle, Sequelize, Knex, Django, SQLAlchemy, EF Core, JPA, GORM) | the port's implementation inserts the outbox row through the caller's transaction: MikroORM's context `em` inside `transactional`/a `tx.run` port, TypeORM the transaction's `manager`, Prisma the `tx` client, Django inside `atomic()`, SQLAlchemy the same `Session`, EF the same `DbContext` | a repository or client that is not the transaction's handle (database § 2's shape); a second direct publish of the same event beside the outbox (a duplicate path) | — |
| **MassTransit** EF Core / Mongo outbox | `AddEntityFrameworkOutbox` + `UseBusOutbox`, publish before the last `SaveChangesAsync` | `UseInMemoryOutbox` alone (not durable); a publish after the last save | NT2, NT1 |
| **Spring** Modulith registry; Kafka + JPA | publication rows in the business transaction, republish and staleness configured | `@Externalized` alone; `ChainedKafkaTransactionManager`; `repo.save` then `kafkaTemplate.send` | OX4, KA10 |
| **Debezium** Outbox Event Router | an insert-only outbox table, key = `aggregateid` | an UPDATE on the outbox (`table.op.invalid.behavior` warn), the key overridden | OX1–OX3 |
| **After-commit helpers** — Celery `delay_on_commit`, Rails after-commit enqueue, Laravel `afterCommit`, Sidekiq `after_commit` | they close the phantom (database V8) | the loss window stays: a crash after commit, a broker down (precedent 11) | OX5, CY5, RB3, LV1 |
| **DB-backed queues** — GoodJob, Solid Queue, graphile-worker | enqueue on the app's own connection, in its transaction | Solid Queue on its separate `queue` database (read `config/database.yml`) | OX7, RB4 |
| **In-process buses** — `@nestjs/cqrs`, Spring events | — | not durable; an `EventBus.publish` after `save` is lost on a crash | OX6 |
| Wolverine, CAP, NServiceBus, the Watermill forwarder | their durable outbox (precedent 11) | a publish outside their transaction scope | — |

A **stable id** is the key a consumer's reserve must use: rows ID1–ID9 (`messaging-scan` § 2 owns an unstable one).

## Read the code — per write-and-publish site, before any §

The outbox writer first (F2), once: what does its implementation write through, and is that the caller's transaction? Then for each candidate, with the § each answer feeds:
- **Which store commits the write, which system receives the publish, and what does each crash point leave?** A crash after the commit and before the publish, a broker that refuses, a rollback after the publish [§1, §2].
- **Is the publish inside the transaction's callback?** Then it is database § 1's, and this skill routes it [§1].
- **Is the event recorded durably in the same transaction** — an outbox row, a framework outbox, a CDC'd table? Does **every** publish of that event go through it, or does a second direct path publish it too [§1]?
- **Who consumes the event, and does anything rely on it?** An advisory push or cache bust with a reconciler is precedent 10; a "refresh" ping the client re-polls is not a dual write [§1].
- **For the relay:** in what order does it read, does it publish in parallel, does it mark before the broker confirmed (an un-awaited send, a fire-and-forget emit), does it hold row locks across the send, how many relay processes run (F3), what renews its lease, what prunes the table [§3]?
- **For each consumer of the events:** where is the reserve — in the effect's transaction, in Redis beside a SQL effect, a read-then-write, a claims table in its own transaction? Is its retention longer than broker retention + DLQ retention + the replay window [§4]?
- **For CDC:** what is the message key, does a consumer handle a null value (a tombstone), what does a re-snapshot emit, is the outbox ever updated [§5]?
- **For a catch-up cursor:** who writes the column it compares — one serial writer (precedent 13) or concurrent transactions? Is the id or timestamp minted before commit, on several hosts' clocks? Is there a lag and a rescan [§6]?

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). F2 runs **before** the § greps: 1a's split depends on it. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (for a path several globs match, the last one wins: `scripts/lint-rg-traps.sh`). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). Multi-line matches print **one line each** (`-o -r '$1'`: `file:first-line:publish call`), so a count is a count of matches, not of the lines they span — the eval's first count of this lane was 102 "hits" for 29 matches.

```bash
ROOTS=(.)   # the server-side code: in a monorepo name the apps (ROOTS=(apps/api apps/worker)); config, schema and CDC greps always search .
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,go,cs,rb,php}')
XT=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,generated,__generated__,vendor,target,bin,obj}/**'
    -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
    -g '!**/*.{spec,test,e2e-spec,fuzz,stories}.*' -g '!**/{test_*,*_test}.{py,go}' -g '!**/*{Test,Tests,IT}.{java,kt,cs}'
    -g '!**/*.d.ts' -g '!**/*.min.*' -g '!**/{docs,ai,.claude}/**')
X=("${XT[@]}" -g '!**/{migrations,migration,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**')
CFG=(--hidden -g '*.{json,yml,yaml,properties,tf,conf,env}' -g '!.git/**' -g '!**/node_modules/**' -g '!**/{package-lock,npm-shrinkwrap,composer}.json'
     -g '!**/{test,tests,__tests__,e2e,fixtures,__fixtures__,testdata}/**' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
T=$(mktemp -d "${TMPDIR:-/tmp}/dws.XXXXXX"); trap 'rm -rf "$T"' EXIT   # the split lists live here; nothing is written into the repo
# F1 ORMs, broker clients, outbox frameworks and CDC with their declared versions (gate 3); F1L the locked versions (pnpm, npm, yarn) — the lockfile wins over the range
rg -n --no-heading --pcre2 '"(?:@mikro-orm/core|typeorm|@prisma/client|drizzle-orm|sequelize|knex|kysely|mongoose|@nestjs/cqrs|pg-transactional-outbox|nestjs-outbox|@event-driven-io/emmett|bullmq|kafkajs|@confluentinc/kafka-javascript|amqplib|@aws-sdk/client-(?:sqs|sns|eventbridge|kinesis)|nats|@nats-io/jetstream|@google-cloud/pubsub|ioredis)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:@mikro-orm/core|typeorm|@prisma/client|drizzle-orm|sequelize|knex|kysely|mongoose|@nestjs/cqrs|pg-transactional-outbox|nestjs-outbox|@event-driven-io/emmett|bullmq|kafkajs|@confluentinc/kafka-javascript|amqplib|@aws-sdk/client-(?:sqs|sns|eventbridge|kinesis)|nats|@nats-io/jetstream|@google-cloud/pubsub|ioredis)@\d[\w.-]*|"node_modules/(?:@mikro-orm/core|typeorm|@prisma/client|drizzle-orm|sequelize|knex|kysely|mongoose|@nestjs/cqrs|pg-transactional-outbox|nestjs-outbox|@event-driven-io/emmett|bullmq|kafkajs|@confluentinc/kafka-javascript|amqplib|@aws-sdk/client-(?:sqs|sns|eventbridge|kinesis)|nats|@nats-io/jetstream|@google-cloud/pubsub|ioredis)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:@mikro-orm/core|typeorm|@prisma/client|drizzle-orm|sequelize|knex|kysely|mongoose|@nestjs/cqrs|pg-transactional-outbox|nestjs-outbox|@event-driven-io/emmett|bullmq|kafkajs|@confluentinc/kafka-javascript|amqplib|@aws-sdk/client-(?:sqs|sns|eventbridge|kinesis)|nats|@nats-io/jetstream|@google-cloud/pubsub|ioredis)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '\b(?:celery|django|sqlalchemy|spring-modulith-events[\w-]*|eventuate-tram[\w-]*|debezium[\w-]*|masstransit(?:\.entityframeworkcore|\.mongodb)?|wolverinefx[\w.]*|dotnetcore\.cap[\w.]*|nservicebus[\w.]*|good_job|solid_queue|sidekiq|threedotslabs/watermill[\w/-]*)\b' -g '**/{requirements*.txt,pyproject.toml,Pipfile,pom.xml,build.gradle,build.gradle.kts,*.csproj,Directory.Packages.props,Gemfile,composer.json,go.mod}' -g '!**/node_modules/**' .
# F2 THE OUTBOX WRITER, resolved before any § (gate 4). O1 outbox/inbox/processed stores (schemas and migrations included); O2 code that writes an outbox row;
#    O3 the classes in O2's files and what they implement (PORTS; a raw INSERT into an *outbox table with no event column on the line is not a port source), then every field or parameter typed as one (RECV); O4 framework outboxes and after-commit helpers
rg -n --no-heading --pcre2 '(?i:\btableName\s*:\s*["\x27`][\w.]*(?:outbox|inbox|processed_(?:messages|events))|@(?:Entity|Table)\(\s*(?:name\s*=\s*)?["\x27][\w.]*(?:outbox|inbox)|\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["\x60]?[\w.]*(?:outbox|inbox|processed_(?:messages|events))|\bpgTable\(\s*["\x27][\w.]*(?:outbox|inbox)|\bToTable\(\s*"[\w.]*(?:outbox|inbox)|\bdb_table\s*=\s*["\x27][\w.]*(?:outbox|inbox))|^\s*model\s+\w*(?:Outbox|Inbox)\w*\s*\{|\bclass\s+\w*(?:Outbox|Inbox)\w*\s*\(\s*models\.Model\s*\)' "${CODE[@]}" -g '*.{sql,prisma}' "${XT[@]}" "${ROOTS[@]}"
rg -n --no-heading --pcre2 '\bnew\s+\w*Outbox(?:Event|Message|Entry|Record|Row|Item)?\s*\(|\.(?:create|add|add_all|persist|save)\(\s*\[?\s*\w*Outbox(?:Event|Message|Entry|Record|Row|Item)?\s*[,(]|\bOutbox\w*\.(?:objects\.(?:create|bulk_create)|create!?)\(|(?i:\boutbox\w*\.(?:create|createMany|insert|insertOne|add)\(|\binsert\s+into\s+["\x60]?[\w.]*outbox|\.insert\(\s*\w*outbox\w*\s*\))' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" > "$T/ow"; cat "$T/ow"
rg -v -i --pcre2 '\binsert\s+into\s+["\x60]?[\w.]*outbox\w*["\x60]?\s*\((?![^)]*\b(?:payload|event\w*|type|topic|aggregate\w*|message\w*|body|headers|destination)\b)' "$T/ow" > "$T/ow.port"; rg -c -v -F -x -f "$T/ow.port" "$T/ow" >/dev/null && echo "O2 not a port source (an *outbox table inserted with no event column — a dedupe or mail table; read it):" && rg -v -F -x -f "$T/ow.port" "$T/ow"
cut -d: -f1 "$T/ow.port" | sort -u | tr '\n' '\0' | xargs -0 -r rg -o --no-filename --no-line-number --pcre2 -r '$1,$2,$3,$4' '\bclass\s+(\w+)(?:[^{\n]*?\bimplements\s+([\w.]+(?:\s*,\s*[\w.]+)*)|\s*:\s*([\w.]+(?:\s*,\s*[\w.]+)*))?|\bfunc\s+\(\s*\w+\s+\*?(\w+)\s*\)' | tr ', ' '\n\n' | rg --pcre2 '^[A-Z]\w+$' | sort -u > "$T/ports"
PORT_RE=$(paste -sd'|' - < "$T/ports"); echo "O3 ports: ${PORT_RE:-none resolved}"
true > "$T/recv"; [ -n "$PORT_RE" ] && rg -o --no-filename --no-line-number --pcre2 -r '$1$2' "\\b(\\w+)\\s*\\??\\s*:\\s*(?:readonly\\s+)?(?:${PORT_RE})\\b|\\b(?:${PORT_RE})\\s+(\\w+)\\s*[;,)=]" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 '^(?:useClass|useExisting|useValue|useFactory|provide)$' | sort -u > "$T/recv"
RECV_RE=$(paste -sd'|' - < "$T/recv" 2>/dev/null); echo "O3 receivers: ${RECV_RE:-none}"
rg -n --no-heading --pcre2 '\b(?:AddEntityFrameworkOutbox|AddMongoDbOutbox|UseBusOutbox|UseInMemoryOutbox|UseDurableOutbox\w*|UseDurableInbox\w*|EnableOutbox)\b|\bBeginTransaction\(\s*_?capPublisher|\bspring\.modulith\.events\.[\w.-]+|@Externalized\b|\bio\.debezium\.transforms\.outbox\.EventRouter\b|\bforwarder\.NewForwarder\b|\bdelay_on_commit\(|\bon_commit\(|\bafter_(?:create_|update_|save_)?commit\b|\bafterCommit\b|\benqueue_after_transaction_commit\b|\bShouldDispatchAfterCommit\b|["\x27]after_commit["\x27]\s*=>' "${CODE[@]}" "${CFG[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"
# O5 the relays: files that read or update the outbox store AND publish — a 1a or 2 hit in one whose write is the mark is §3's (publish, then mark, is precedent 12)
rg -l0 --pcre2 '(?i:\b(?:from|update)\s+["\x60]?[\w.]*outbox\w*["\x60]?(?:\s|,|\)|$)|\boutbox\w*\.(?:find\w*|where|select|filter)\()|\.(?:find|findAll|findMany|findOne|count|createQueryBuilder|getRepository|select_for_update)\(\s*\w*Outbox(?:Event|Message|Entry|Record|Row|Item)?\b|\bOutbox\w*\.objects\.(?:filter|select_for_update|all)\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l --pcre2 '\.(?:publish|send|produce|emit\w*|sendMessage|sendToQueue|xadd|add|addBulk|Publish|Send|PublishAsync|SendAsync|WriteMessages)\(' > "$T/relay"; echo "O5 relays: $(wc -l < "$T/relay" | tr -d ' ')"; cat "$T/relay"
# F3 deployment shape (gate 7): replicas and autoscalers — more than one relay process needs a claim (database §5) or a leader
rg -n --no-heading --pcre2 '^\s*replicas:\s*\d|\bkind:\s*(?:HorizontalPodAutoscaler|ScaledObject|CronJob|Job)\b|\b(?:min|max)Replicas:\s*\d|^\s*(?:CMD|ENTRYPOINT)\b' -g '**/Dockerfile*' "${CFG[@]}" . | "${NC[@]}"
# 1a commit, then publish (X-DUALWRITE, await-style: TS/JS, Python async, C#). One line per match — file:write-line:publish call — then split three ways by the publish receiver
rg -n --no-heading -U -o -r '$1' --pcre2 '^[ \t]*(?:(?:const|let|var)\s+[\w{}\[\], ]+\s*=\s*|[\w.]+\s*=\s*)?await\s+[\w.$]*\.(?:save|saveAndFlush|insert|insertOne|insertMany|create|createMany|update|updateOne|upsert|persist|persistAndFlush|flush|commit|\$transaction|transactional|transaction|execute|SaveChanges(?:Async)?)\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*;?[ \t]*\n(?:(?![ \t]*\}[ \t]*\)?;?[ \t]*\n)(?![^\n]*\b(?:function|def|func)\b)(?![^\n]*\basync\s+\w+\s*\()[^\n]*\n){0,3}?[^\n]*\bawait\s+([\w.$]*(?:\.(?:publish|publishAll|emit|send|sendMessage|produce|add|addBulk|sendToQueue|dispatch|Publish|Send|PublishAsync|SendAsync|perform_async|perform_later|delay|apply_async)|new\s+(?:Publish|SendMessage|PutEvents|PutRecord)\w*Command))\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/dw"
if [ -n "$RECV_RE" ]; then rg --pcre2 ":[\\w.\$]*\\b(?:${RECV_RE})\\.[\\w\$]+\$" "$T/dw" > "$T/dw.port"; rg -v --pcre2 ":[\\w.\$]*\\b(?:${RECV_RE})\\.[\\w\$]+\$" "$T/dw" > "$T/dw.rest"; else : > "$T/dw.port"; cp "$T/dw" "$T/dw.rest"; fi
rg -i --pcre2 ':[\w.$]*outbox[\w$]*\.[\w$]+$' "$T/dw.rest" > "$T/dw.named"; rg -v -i --pcre2 ':[\w.$]*outbox[\w$]*\.[\w$]+$' "$T/dw.rest" > "$T/dw.cand"
echo "1a $(wc -l < "$T/dw" | tr -d ' ') matches → outbox port $(wc -l < "$T/dw.port" | tr -d ' ') (control, verify the writer once) · in an O5 relay file $(rg -c -F -f "$T/relay" "$T/dw.cand" 2>/dev/null || echo 0) (a mark → §3) · outbox-named, writer unresolved $(wc -l < "$T/dw.named" | tr -d ' ') · candidates $(wc -l < "$T/dw.cand" | tr -d ' ')"; head -3 "$T/dw.port"; cat "$T/dw.named" "$T/dw.cand"
# 1b other lanes, write then publish: Java save → template send; Go Commit() → Publish; .NET SaveChanges → Publish/Send (MT-01); Python CEL-04; Ruby SQ-03; PHP LAR-02
rg -n --no-heading -U --pcre2 '\.save(?:AndFlush|All)?\([^;\n]*\)\s*;[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*\b\w*(?:[kK]afkaTemplate|[rR]abbitTemplate|[sS]treamBridge|[jJ]msTemplate|[sS]qsTemplate|[sS]nsTemplate)\.(?:send|convertAndSend|sendDefault)\(' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.save'
rg -n --no-heading -U --pcre2 '\b(?:tx|txn)\.Commit\((?:ctx)?\)[^\n]*\n(?:[^\n]*\n){0,4}?[^\n]*\.(?:Publish|Produce|WriteMessages|SendMessage|Send)\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.Commit\('
rg -n --no-heading -U --pcre2 'SaveChanges(?:Async)?\([^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*\.(?:Publish|Send)(?:Async)?\(' -g '*.cs' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'SaveChanges'
rg -n --no-heading -U --pcre2 '^[ \t]*(?!with\b)[^\n]*\b(?:objects\.(?:create|update|bulk_create|get_or_create|update_or_create)|\.save)\([^\n]*\n(?:[^\n]*\n){0,3}?[ \t]*(?!transaction\.on_commit)[\w.]+\.(?:delay|apply_async)\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\b(?:objects\.|\.save\()'
rg -n --no-heading -U --pcre2 '^[ \t]*[^\n]*\.(?:create|update|save|insert_all|upsert_all)!?(?=[\s(])[^\n]*\n(?:[^\n]*\n){0,3}?[ \t]*[\w:]+\.(?:perform_async|perform_in|perform_at|perform_later|perform_bulk)\b' -g '*.rb' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.(?:create|update|save|insert_all|upsert_all)'
rg -n --no-heading -U --pcre2 '^[ \t]*[^\n]*::(?:create|updateOrCreate|firstOrCreate|insert)\([^\n]*\n(?:[^\n]*\n){0,3}?[ \t]*(?:[\w\\]+::dispatch\(|dispatch\(|Bus::dispatch\()(?![^\n]*afterCommit)' -g '*.php' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '::'
# 1c in-process buses that look like publishing (OX6) — read what each handler does; 1d transaction openers in the files 1a left as candidates (inside the callback → database transaction-scan §1)
rg -n --no-heading --pcre2 '\b\w*[eE]ventBus\.publish(?:All)?\(|\bapplicationEventPublisher\.publishEvent\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
cut -d: -f1 "$T/dw.cand" "$T/dw.named" | sort -u | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 '\b(?:tx|txn|uow|unitOfWork|transaction\w*)\.run\(|\.transactional\(|\$transaction\(|\.transaction\(|\bwithTransaction\(|\btransaction\.atomic\b|@Transactional\b|\bBeginTransaction(?:Async)?\(|\bDB::transaction\(|\.Begin(?:Tx)?\(' | "${NC[@]}"
# 2 publish, then commit (X-PUBTHENCOMMIT) — file:publish-line:the write that follows; Go Publish before Commit()
rg -n --no-heading -U -o -r '$1' --pcre2 '^[ \t]*await\s+[\w.$]*(?:\.(?:publish|emit|send|sendMessage|produce|add|addBulk|sendToQueue|dispatch|Publish|Send|PublishAsync|SendAsync|perform_async|perform_later|delay|apply_async)\(|new\s+(?:Publish|SendMessage|PutEvents|PutRecord)\w*Command\()[^\n]*\n(?:(?![ \t]*\}[ \t]*\)?;?[ \t]*\n)(?![^\n]*\b(?:function|def|func)\b)(?![^\n]*\basync\s+\w+\s*\()[^\n]*\n){0,3}?[^\n]*\bawait\s+([\w.$]*\.(?:save|insert|insertOne|insertMany|create|createMany|update|updateOne|upsert|persistAndFlush|flush|commit|\$transaction|transactional|transaction|execute|SaveChanges(?:Async)?))\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -v -i --pcre2 ':\d+:[\w.$]*outbox'
rg -n --no-heading -U --pcre2 '\.(?:Publish|Produce|WriteMessages|SendMessage)\([^\n]*\n(?:[^\n]*\n){0,4}?[^\n]*\b(?:tx|txn)\.Commit\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\.(?:Publish|Produce|WriteMessages|SendMessage)\('
# 3 the relay (O5's files). 3a relays with no ORDER BY; 3b parallel publish; 3c a mark before a confirmed publish, or an un-awaited publish then a mark;
#   3d row locks, a claim or a lease around the publish (FOR UPDATE held across I/O → database §1; no SKIP LOCKED → database §5) and extend() results dropped; 3e pruning
tr '\n' '\0' < "$T/relay" | xargs -0 -r rg --files-without-match --pcre2 '(?i:\border\s+by\b)|\borderBy\b|\border_by\b|\border\s*:|\.OrderBy(?:Descending)?\(|\.order\('
tr '\n' '\0' < "$T/relay" | xargs -0 -r rg -H -n --no-heading --pcre2 'Promise\.(?:all|allSettled)\(\s*[\w.$]*\.map\(|\.parallelStream\(|\basyncio\.gather\(|\bParallel\.ForEach(?:Async)?\(|^\s*go\s+func\b|\bpMap\(' | "${NC[@]}"
tr '\n' '\0' < "$T/relay" | xargs -0 -r rg -H -n --no-heading -U --pcre2 '(?i:(?:published|processed|sent|dispatched|relayed)_?at)\s*[:=](?!=)(?!\s*(?:null|None|nil)\b)[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*\b(?:await\s+)?[\w.$]*\.(?:publish|send|produce|emit\w*|sendMessage|sendToQueue|xadd|Publish|Send)\(|^[ \t]+(?!await\b|return\b|yield\b)(?:this\.)?[\w$.]+\.(?:publish|send|produce|emit\w*|sendMessage|sendToQueue|xadd|Publish|Send)\([^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*(?i:(?:published|processed|sent|dispatched|relayed)_?at)\s*[:=](?!=)' | rg --pcre2 '(?i:_?at\s*[:=])|\.(?:publish|send|produce|emit\w*|sendMessage|sendToQueue|xadd|Publish|Send)\('
tr '\n' '\0' < "$T/relay" | xargs -0 -r rg -H -n --no-heading --pcre2 '(?i:\bfor\s+update\b|\bskip\s+locked\b)|\bselect_for_update\(|\bLockMode\.\w+|\blockMode\s*:|\bPESSIMISTIC_WRITE\b|\.forUpdate\(|\.setLock\(|\.extend\(\)\s*;|\bwith\w*(?:Leader|Lock)\w*\(' | "${NC[@]}"
rg -l --pcre2 '(?i:\bdelete\s+from\s+["\x60]?[\w.]*outbox|\boutbox\w*\.(?:delete\w*|destroy|remove)\(|outbox[\w-]*(?:retention|prune|purge|cleanup|sweep))|\.(?:nativeDelete|deleteMany|delete|remove)\(\s*\w*Outbox(?:Event|Message|Entry|Record|Row|Item)?\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
# 4 the inbox. 4a Redis SET NX that is not a lock (file:line:key) — a reserve in a second store; 4b read-then-write on a dedupe key; 4c a claim or reserve in its own
#   transaction (a forked session, REQUIRES_NEW); 4d retention on the dedupe store (THR-DS-DEDUPE-WINDOW)
rg -n --no-heading -U -o -r '$1$2' --pcre2 '(?:\.set\(\s*|\bredis\.call\(\s*["\x27]SET["\x27]\s*,\s*)([\w.$]+(?:\([^()\n]*\))?|["\x27`][^"\x27`\n]*["\x27`]|\w+\[\w+\])\s*,[^;]*?["\x27]NX["\x27]|(?:\.setnx\(|\.setIfAbsent\(|\bSetNX\(|\bSetIfNotExists\w*\()\s*([^,\s)]+)' "${CODE[@]}" "${X[@]}" -g '!**/*{lock,leader,throttle,rate-limit,ratelimit}*' "${ROOTS[@]}" | rg -v -i --pcre2 ':\d+:[^\n]*(?:lock|leader|mutex|lease|throttle|cooldown)'
rg -n --no-heading -U --pcre2 '(?i:\b(?:find(?:One|Unique|First)?|exists|count|get|select)\w*\([^\n]*\b(?:processed|inbox|dedup\w*|idempot\w*|event_?id|message_?id)\b[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*\b(?:insert|create|save|persist|add)\w*\()' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -i --pcre2 '\b(?:find|exists|count|get|select)\w*\('
rg -l0 -i --pcre2 '\b(?:claim\w*|inbox\w*|processed_(?:messages|events)|dedup\w*|idempot\w*)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\.fork\(\)[^\n]*\.transactional\(|\bREQUIRES_NEW\b|\brequiresNew\b|\bTransactionScopeOption\.RequiresNew\b' | "${NC[@]}"
rg -n --no-heading -i --pcre2 '(?:inbox|processed_(?:messages|events)|consumer_claims|dedup\w*)[^\n]*(?:ttl|expire|retention|older_?than|interval\s*["\x27]|delete\s+from)|delete\s+from\s+["\x60]?\w*(?:inbox|processed_(?:messages|events)|claims)' "${CODE[@]}" -g '*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5 CDC: connector configs (key, tombstones, snapshot, op on the outbox); consumers of change topics with no null-value branch
rg -n --no-heading --pcre2 '\bconnector\.class\b|\bio\.debezium\.transforms\.outbox\.EventRouter\b|\btable\.field\.event\.key\b|\broute\.tombstone\.on\.empty\.payload\b|\bsnapshot\.mode\b|\btombstones\.on\.delete\b|\btable\.op\.invalid\.behavior\b|\btable\.expand\.json\.payload\b' "${CODE[@]}" "${CFG[@]}" "${XT[@]}" .
rg -l0 -i --pcre2 '\bdebezium\b|\bcdc\b|\bdbserver\d*\.|["\x27]outbox\.event\.|\.public\.\w+["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\bvalue\s*(?:===?|==|is)\s*(?:null|None|nil)\b|!\s*(?:message|msg|record|m)\.value\b|\bvalue\(\)\s*==\s*null\b|(?i:tombstone)'
# 6 gap-blind cursor: a > comparison on an id, a sequence, a position or a timestamp in a file that keeps a cursor between runs (floor, checkpoint, watermark) — keyset pagination is not one
rg -l0 -i --pcre2 '(?<![.\w])(?:floor|checkpoint|watermark|high_?water\w*|next_?floor|last_?(?:event_?id|position|seq\w*|offset|processed\w*|seen_?id)|resume_?(?:from|after|token))\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '(?i:\bwhere\b[^\n]*\b(?:id|seq\w*|sequence\w*|position|global_?position|offset|created_?at)\s*>\s*(?:\$\d+|\?|:\w+|@\w+|\$\{))|\b(?:id|seq\w*|sequence\w*|position|globalPosition|createdAt|created_at)\s*:\s*\{\s*\$?gte?\s*:|\b(?:id|seq\w*|position)\s*:\s*MoreThan(?:OrEqual)?\(|\b(?:id|seq\w*|position|created_at)__gte?\s*=' | "${NC[@]}"
```

Reading the output:
- **F1 is the version gate**: the ORM, the broker client and any outbox framework, each with its source (a manifest range is marked `range`; its floor decides which rows apply). **F1L** prints the locked version: when it printed one, that is the version, not the range's floor (a package locked at two versions: the importer's entry in `pnpm-lock.yaml`, or `<app>/node_modules/<pkg>` in `package-lock.json`, says which one the app gets).
- **F2 is the subject list, and the control.** O1 names the outbox, inbox and processed-message stores (migrations included: a table with no writer is a finding of its own, §3). O2 names the code that inserts an outbox row. O3 prints the resolved `ports` and `receivers`. **Read O2's writer once**: if it writes through the caller's transaction, every 1a line split as `outbox port` inherits the control (precedent 11); if it does not, they are **one** §1 finding with N sites. `outbox-named, writer unresolved` lines publish through a receiver whose name says outbox but whose type O3 did not resolve (a factory, a module function, an injected token with no type): read the callee once. O4 lists framework outboxes and after-commit helpers — the lanes above. O5 lists the relays.
- **1a is three lists, not one.** Only `candidates` are read per site. A candidate in an O5 relay file whose write is the relay's mark is §3's (precedent 12). 1d prints the transaction openers in each candidate's file: a publish inside the callback is routed to database § 1.
- **Every other line is a candidate for the read questions**, never a verdict. 2 (publish, then write) in a relay is the correct order (precedent 12). 4a prints `file:line:key` for every Redis `SET NX` whose key or file is not a lock; a reserve whose effect is SQL is the two-store shape. 6 admits a pagination loop that shares a file with a stored cursor: part A refutes it in one read.

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **The port can be a function, not a class.** `export async function recordEvent(tx, …)` inserting the outbox row is a writer O3 cannot type: its callers print as candidates. Name it, and treat its call sites as `outbox port` once its first parameter is shown to be the caller's transaction.
- **The publish can hide behind a wrapper** (`this.events.notify(…)`, a domain-event dispatcher drained after `flush`). 1a sees only publish verbs; read the wrapper's callers when F1 shows a broker client and 1a prints nothing.
- **The outbox and the relay can live in another repository** (a CDC platform team, a shared relay service). Quiet greps mean "not in this repo" (precedent 5); the row is Unconfirmed with the repo to read.

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples (outbox, BullMQ, Java, Go, .NET, Celery, Ruby, PHP files, bad and good) | 0.3 s, 0 rg errors. **Every BAD line surfaces in its §**: commit-then-`kafka.send` and a one-line `$transaction` then `sns.send` (1a), `repo.save` → `kafkaTemplate.send`, `tx.Commit()` → `Publish`, `SaveChangesAsync` → `Publish`, `objects.create` → `.delay`, `create!` → `perform_async`, `::create` → `dispatch` (1b), publish-then-`update` (2), a relay with no `ORDER BY` and a parallel `Promise.all` publish (3a, 3b). The good files print only what the read clears: the outbox writers (O2), MassTransit EF outbox, `delay_on_commit`, `after_create_commit`, `->afterCommit()` (O4), a BullMQ job enqueued beside its own outbox row (1a — a double path, read it), an `apply_async` after the `atomic` block (1b, a true candidate kept), and a `SKIP LOCKED` relay (3d) |
| Seeded tree for shapes the samples lack (7 files) | A port named `EventOutbox` with a field called `events` is resolved, so `this.events.publish` is split as `outbox port` — resolution goes by type, not by the word "outbox". Found: a direct `kafka.send` after `save` (1a), an un-awaited `eventBus.publish` (1c), mark-then-send in a relay (3c), `FOR UPDATE SKIP LOCKED` inside a `$transaction` that publishes (3d → database § 1), a Redis `SET NX` reserve before a SQL effect (4a), find-then-insert on an event id (4b), a Debezium router with `table.op.invalid.behavior: warn` and a change-topic consumer with no null branch (5), `WHERE id > $1` against a stored checkpoint (6). Keyset pagination in the same file prints too (the documented part-A refutation) |
| `benchmarks/fixtures/*` (18 fixtures) | 0 detector lines in 17 (F1/F3 context only). `slow-marketplace` prints 6: its outbox migration and two `new OutboxEvent` writers (O1, O2 — the writer is the service itself, so O3 resolves no port and none is needed), the relay (O5), its publish-then-mark (2, cleared by precedent 12) and its `for update` claim with no `SKIP LOCKED` (3d) — the fixture's database § 5 seed, routed. Two first-draft misses were fixed before shipping: O5 did not see a relay that claims with `update outbox_event` over a line break, and did not count `addBulk` as a publish |
| Real repository (NestJS 11 + Fastify, MikroORM 6.6.16 and BullMQ 6.3.4 in the lockfile — F1L prints them since 2026-10-14 (8 lines: the package and snapshot entries for MikroORM, BullMQ, ioredis and knex), F1 the manifest ranges `^6.6.16`, `^6.3.4` — ioredis on managed Valkey; read-only, about 11,100 files; re-run on the full tree 2026-10-14) | 1.7 s. O1 the outbox and the consumer-claims tables; O2 **1 writer** (`new OutboxEvent()` in the outbox service); O3 ports `OutboxPort`, `OutboxService` → receiver `outbox` (107 fields typed as the port). **1a: 29 matches → 28 `outbox port`, 1 candidate** (28 → 27 on the earlier partial copy; one use case added since). The writer, read once, persists through the request-scoped entity manager inside the caller's `tx.run`: the 28 inherit the control (one of them is in `scripts/`, closed at part A). The candidate is a reserve-then-send SMS whose unique claim row commits before the send — at-most-once by written choice, Refuted by precedent 6. (The eval's battery counted 29: one more in a Markdown recipe, which `CODE` does not search.) 2: **0**. O5 1 relay, ordered (3a 0, 3b 0); 3c the relay emits to tenant rooms with an un-awaited Socket.IO push and marks the row processed — at-most-once for an advisory push, and 3d its leader lease's `extend()` result is dropped: both Hardening (precedent 19, amended). 4a **9** non-lock `SET NX` sites (11 on the earlier copy: two jobs now take the shared leader-lock helper) → 6 refuted at part A (single-use and OTP keys whose only effect is Redis, a rescan stamp, an enqueue admission script), 1 handed to security `logic-race-scan` § 5 (a paid extraction's charge claimed in Redis beside a Postgres debit — the eval's § 3.8 row), 2 bulk-dispatch slot claims `Live, unreviewed`. 4b 0; 4c the claims ledger in a forked transaction → cleared by precedent 2 (amended): the effect table carries the event id. §5 N/A (no CDC). 6: **3** → 1 refuted at part A (keyset pagination over ids in an erasure port; a matching rule's "floor" on the earlier copy), the outbox consumers' UUIDv7 floor (30 s lag, late-commit rescan, hourly full rescan → Hardening, precedent 13; clock half → `coordination-scan` § 8), and **1 live candidate**: a money-collection watermark compared with `createdAt > since` over ledger rows written by concurrent transactions — a row stamped before a collection and committed after it is never collected. Read again on the full tree: `createdAt` is stamped by the app when the entity is built, before its commit, and the mark moves to the newest visible row; the only writer is one leader-elected consumer that applies events in order, so the gap needs the leader moving between replicas with skewed clocks or a lease overrun. The same read found a second shape: the mark and the sum are two statements under READ COMMITTED, so a row committed between them is summed now and again next time. Both Unconfirmed until V301's gap variant and its double-take variant (§ 6's proof) run (security § 5 corroborates: money) |

## The 3,000-hit path

1. **Resolve the writer first** (F2). A large repo's 1a list is mostly its own port: in the real run, 27 of 28. Verify the writer once and close the group with one row of evidence.
2. **Intersect** with F3: a write and publish in code no production process type starts is dismissed with one read (a script, a seed, a CLI). Name the directory in the coverage block.
3. **Group by root cause**: one outbox writer, one relay, one inbox helper, one base consumer is **one** finding with N sites. A use-case template copied across fifty modules is one row.
4. **Rank**: events another service acts on (orders, payments, stock, shipments) first; then customer-visible notifications; then advisory events.
5. **Read the top 30 groups** with the read-the-code questions; sample 10 sites per group, and the rest inherit the verdict with the group's id.
6. **Run the bulk oracle once**: V300 kill-between over the top use case of each group, against Postgres and the broker in containers.
7. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production path reached by F3. One replica does **not** make a dual-write row latent (precedent 32).

| § | Classes | Default severity |
|---|---|---|
| 1 | DW-1 commit, then publish, nothing durable between; the outbox missing or misused | high; BLOCKER when the lost event is the only way another service learns of an order, a payment or a stock movement and nothing reconciles; not a row for an advisory event with a reconciler (precedent 10) |
| 2 | DW-2 publish, then commit | high; not a row when consumers re-verify the state before acting |
| 3 | DW-4 outbox relay: order, parallel publish, mark before a confirmed publish, no relay, no pruning, the relay's lease | high for loss (mark before confirm, no relay); high for reorder under a per-aggregate invariant, else not a row (precedent 8); medium for no pruning; Hardening for an advisory relay (precedent 19) |
| 4 | DW-5 inbox not atomic with the effect; retention shorter than the redelivery window | high with an external or financial effect (money → security); medium for an internal write |
| 5 | DW-6 CDC consumer gaps | high for a dropped event (an UPDATE on the outbox) or a crash-looping tombstone; medium for snapshot duplicates a reserve absorbs |
| 6 | ES-4 / E5 gap-blind catch-up cursor | high for a silent permanent skip; Hardening with a lag and a rescan that bound it |

### 1. Commit, then publish — the outbox missing or misused (DW-1)

```
BAD:   const order = await this.orders.save(dto); await this.kafka.send({ topic: 'orders', … })   // crash between = lost event
       await prisma.$transaction(async (tx) => { … }); await this.sns.send(new PublishCommand(…))
       repo.save(o); kafkaTemplate.send(…) · tx.Commit(); w.WriteMessages(…) · SaveChangesAsync(); Publish(…) (MT-01, NT2)
       order.save(); send_receipt.delay(order.pk) after atomic · delay_on_commit for a fact billing relies on (OX5)
       await this.orders.save(o); this.eventBus.publish(new OrderPlaced(o.id))   // in-process, not durable (OX6)
       an outbox port whose implementation writes with a repository that is not the transaction's handle
GOOD:  await this.tx.run(async () => { await this.orders.insert(o); await this.outbox.emit('order.placed', { id: o.id }) })
       — the port inserts the row through the caller's transaction; a relay or CDC publishes it after commit
```
**Read the code:** Start from F2: is the writer the caller's transaction, and does every publish of this event go through it? For each candidate: which store commits, which system receives, and is the publish inside the transaction's callback (→ database § 1)? Is a framework outbox configured for this endpoint (O4: the lanes table)? Does a reconciler re-derive the event from state on a schedule (precedent 10)? Is the after-commit helper on an event someone relies on (OX5: the loss window stays)? Is the outbox row written **and** the event published directly (a duplicate path the consumers must absorb)? **Finding when** a crash or a broker error after the commit loses a fact another process relies on, or the outbox row can commit apart from the domain write. **Proof (V300):** inject a fault after the commit and before the publish (a spy that throws once, or `SIGKILL` in a child process) against Postgres and the broker in containers; restart: the event is missing (fails); after the fix it is delivered exactly once within the relay interval, and DB and broker counts agree. The broker-down variant stops the broker container instead.

### 2. Publish, then commit (DW-2)

```
BAD:   await this.bus.publish(new OrderCancelled(id)); await this.orders.update(id, { status: 'cancelled' })
       w.WriteMessages(ctx, msg); …; tx.Commit()          // a rollback or crash after the publish = a phantom event
GOOD:  write first and publish through the outbox; or publish an intent that consumers re-verify against the source
```
**Read the code:** Can the write after the publish fail or roll back (a constraint, a version check, a timeout)? Do consumers act on the event or re-read the state first? Inside an O5 relay, publish-then-mark is the correct order (precedent 12) — not a row. **Finding when** a consumer can act on a state that never committed. **Proof (V300, reverse probe):** fault the write after the publish: the consumer sees an event for a row that does not exist (fails); after the fix, no event for a rolled-back row.

### 3. The outbox relay (DW-4)

```
BAD:   const rows = await db.outbox.findMany({ where: { publishedAt: null } })            // no order (OBX-01)
       await Promise.all(rows.map(publish))                                              // parallel (OBX-02)
       row.publishedAt = new Date(); await em.flush(); await producer.send(…)            // marked before the broker confirmed
       socket.emit(…) (un-awaited); row.processedAt = new Date()                         // fire-and-forget, then marked
       SELECT … FOR UPDATE SKIP LOCKED; await producer.send(…) inside the claim's transaction   // locks held across I/O → database §1
       an outbox table (O1) with no relay, no CDC router and no pruning (OBX-03) · UseInMemoryOutbox alone (NT2)
GOOD:  read in id order, publish per aggregate in order, await the confirm, then mark; claim with a lease column or SKIP LOCKED
       and publish outside the claim's transaction; prune published rows; one leader or per-aggregate partitions
```
**Read the code:** Is the relay's read ordered, and does per-aggregate order matter to a consumer (precedent 8)? Is each publish awaited and confirmed before its row is marked? Does a claim transaction stay open across the send (route the claim to database § 1 / § 5)? How many relay processes run (F3), and what keeps two from publishing one row — a leader lease whose `extend()` result is checked, `SKIP LOCKED`, a partition? What prunes the table, and is lag alerted? A relay that publishes twice is correct (precedent 12): the finding is loss, reorder, or a consumer with no reserve. **Finding when** a crash or a parallel relay loses, reorders (under a per-key invariant) or never publishes an event. **Proof (V301):** kill the relay between send and mark → 1 effect per event (the consumer's reserve absorbs the resend); mark-before-confirm with the broker paused → the event is missing (fails); two updates to one aggregate under relay parallelism 4 → the consumer sees v1 then v2.

### 4. Inbox absent or not atomic with the effect (DW-5)

```
BAD:   if (!(await redis.set(`processed:${evt.id}`, '1', 'EX', 86400, 'NX'))) return; await em.persistAndFlush(effect)
       const seen = await inbox.findOne({ eventId }); if (seen) return; …; await inbox.insert({ eventId })   // read-then-write
       await applyEffect(evt); await inbox.insert(evt.id)                                  // reserve after the effect
       a claims row committed in a forked transaction while the effect commits in another, with no event id on the effect
       inbox rows pruned after 1 day on a queue with 14-day retention and a replay tool
GOOD:  INSERT INTO processed_messages(consumer, event_id) … ON CONFLICT DO NOTHING in the effect's transaction, then the effect,
       then commit and ack; or an effect table carrying event_id (precedent 2, amended); retention ≥ the redelivery window
```
**Read the code:** Where is the reserve, and is it the same store and the same transaction as the effect? A Redis reserve beside a SQL effect loses the effect on a crash after the reserve (it reads as "done") or doubles it on a crash after the effect when the reserve expires. Is the key stable (ID1–ID9; an unstable key is `messaging-scan` § 2)? Is a claims table a coordination aid beside a reserve on the effect table (precedent 2, amended — cleared), or the only reserve? How long does the reserve live against broker retention + DLQ retention + the replay window (`THR-DS-DEDUPE-WINDOW`)? A money, stock or credit effect goes to security (§ Boundaries). **Finding when** a crash between the reserve and the effect, or a redelivery after the reserve expired, loses or repeats the effect. **Proof (V303):** crash after the reserve and before the effect, redeliver → the effect exactly once (fails before the fix); crash after the effect and before the ack → no second effect; V292's barrier-concurrent duplicate also passes.

### 5. CDC consumer gaps (DW-6)

```
BAD:   "table.op.invalid.behavior": "warn" with code that UPDATEs outbox rows (the update is dropped, OX1)
       "table.field.event.key": "id" — the key overridden away from aggregateid (per-aggregate order lost)
       a consumer of dbserver1.public.orders with no value == null branch (a tombstone crash-loops it, OX3)
       snapshot.mode=initial re-emitting every row as op=r into a consumer with no reserve (OX2)
GOOD:  an insert-only outbox (delete in the same transaction if you must clean); key = aggregateid; a null branch; a reserve on the event id header
```
**Read the code:** Is the config the production connector's? What does the code do to outbox rows after insert? Does every consumer of a change topic handle a null value? What happens on a connector restart or a re-snapshot — does the consumer's reserve (§4) absorb the replay? **Finding when** a CDC event is dropped, crash-loops its partition, or is applied twice with an effect. **Proof (V302):** restart the connector from a committed offset, re-snapshot, delete a row → consumer state unchanged, tombstones handled, per-aggregate order kept.

### 6. Gap-blind catch-up cursor (ES-4 / E5)

```
BAD:   SELECT * FROM events WHERE id > $1 ORDER BY id  -- $1 = the stored checkpoint; ids from a sequence many transactions draw
       { createdAt: { $gt: watermark } } over rows stamped before commit by concurrent writers
       a UUIDv7 / ULID floor minted on each writer's clock, compared to the consumer's last id with no lag and no rescan
       mark = max(created_at); total = sum(amount) WHERE created_at > since; save mark  -- two READ COMMITTED statements
GOOD:  one serial writer (an advisory-locked appender), a log-ordered source (Debezium, the event store's position),
       or a floor held back by a lag longer than the longest transaction plus a periodic rescan;
       the mark and the sum in ONE statement (or REPEATABLE READ), the sum bounded by the mark it saves, or each row tied to its collection
```
**Read the code:** Who writes the compared column — one serial writer (precedent 13) or concurrent transactions? Is the id or timestamp assigned before commit (a sequence `nextval`, `now()` — the transaction's start —, an app-side UUIDv7)? Does the cursor advance past rows a still-open transaction will commit below it? Is there a lag and a rescan, and what bounds the residual (clock skew between replicas → `coordination-scan` § 8)? Keyset pagination over a one-shot read is not a cursor (part A). **Do the mark and the read share one snapshot?** A watermark read in one statement and the rows summed or collected in a second, both under READ COMMITTED (the Postgres and MySQL-with-`READ-COMMITTED` default; read the transaction helper's isolation and `default_transaction_isolation`), see two snapshots: a row committing between them, stamped after the mark, is taken now and again by the next pass when the sum is not bounded by the mark it saves (precedent 13). **Finding when** a row that commits late is never read, or a row is collected twice. **Proof (V301, gap variant):** hold transaction A open with sequence 10 while B commits 11 and the consumer advances; commit A → event 10 is still delivered (fails before the fix). Double-take variant: pause between the mark and the sum (a latch in the port), commit one row from another connection, resume, run the next pass — the row is counted once (fails before the fix).

## Output

```
dual-write-scan coverage — scope=whole repo  stacks=@mikro-orm/core ^6.6 range (apps/api/package.json:39), bullmq ^6.3 range, ioredis ^5.4
Outbox writer: OutboxService implements OutboxPort (apps/api/src/outbox/outbox.service.ts:28) — joins the caller's tx.run (read once)
Relays: 1 (apps/api/src/outbox/relay.worker.ts, one leader) · processes: api (HPA 2–10), worker (KEDA)

Findings: 0 · Unconfirmed: 1 · Hardening: 3

1. apps/api/src/wallets/collections.port.ts:132 · apps/api/src/wallets/ledger.writer.ts:58     [report-flagged]   high
   §6 ES-4 — part A: a watermark kept between collections. Part B: `createdAt > since` over ledger rows stamped before
   commit by concurrent writers; a row committed after a collection with a later mark is never collected. Money →
   security logic-race-scan §5 corroborates. Settling test: V301 gap variant — hold a ledger insert open across a collection.
2. apps/api/src/outbox/relay.worker.ts:205    Hardening   §3 un-awaited Socket.IO emit, then marked: advisory push (precedent 19)
3. apps/api/src/outbox/relay.worker.ts:116    Hardening   §3 the leader lease's extend() result dropped; advisory relay (precedent 19)
4. apps/api/src/outbox/outbox-consumer.ts:218 Hardening   §6 UUIDv7 floor with a 30 s lag and two rescans (precedent 13; skew → coordination-scan §8)

Verification: 45 candidates → 0 findings · 1 unconfirmed · 3 hardening · 38 refuted · 1 routed · 2 live, unreviewed (self-verified)

Class coverage:
  §1  commit then publish      checked (28 → 27 outbox port, 1 refuted: precedent 6) · → database transaction-scan §1 (0)
  §2  publish then commit      checked (0)
  §3  relay                    checked (1 relay → 2 hardening) · → database transaction-scan §5 (0)
  §4  inbox atomicity          checked (11 SET NX → 0; 1 claims ledger cleared, precedent 2) · → security logic-race-scan §5 (1) · Live, unreviewed (1 group / 2 hits)
  §5  CDC                      N/A (no connector config, no CDC client)
  §6  gap-blind cursor         checked (3 → 1 unconfirmed, 1 hardening)
```

`[report-with-fix]`: the oracle failed on the unfixed code against a real database and broker, and the fix is local to the project's outbox port, relay or inbox helper. `[report-flagged]`: one link is unproven (no container run, the outbox in another repo, a connector config not read); the row names it and the settling test. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 10** commit-then-publish of an advisory, re-derivable event with a written reconciler is not a dual write. **§ 11** a framework outbox is the control; after-commit helpers clear the phantom, not the loss window. **§ 12** an at-least-once relay that publishes twice is correct. **§ 13** `WHERE id > $last` is safe with one serial writer or a log-ordered source.
- **§ 2** (amended) an effect table carrying the event id, read through an anti-join, is the reserve; a claims table beside it need not be atomic with the effect. **§ 6** at-most-once by written decision. **§ 19** (amended) an advisory relay — a websocket push, a cache warm — is efficiency only.
- **§ 32** one replica does not make a dual-write row latent. **§ 33** an in-memory bus or a mocked broker proves nothing. **§ 34** a comment saying "atomic", "in the same transaction" or "the relay dedupes" is a pointer: read the writer, the relay and the consumer (refute-before-report § 7).

Shapes this skill must not report: a publish through the resolved port inside the caller's transaction; publish-then-mark inside a relay; an outbox row plus a CDC router with an insert-only table; keyset pagination; a reserve-then-send whose loss is written down.

## When to run

- On any diff that touches a write followed by a publish, an outbox entity, writer or relay, an inbox or processed-messages table, a CDC connector config, or a catch-up cursor — `/ds-audit`'s "a write followed by a publish; an outbox entity, writer or relay; a CDC config" signal.
- On every whole-repo `/ds-audit`, reporting all six §s; before introducing an outbox, a second relay process, a CDC pipeline or a new consumer of an existing event.
- After `/add-event-handler`: its Phase 6 runs V292 and V303 from the same oracle file.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the writer F2 resolved, the `broker-semantics.md` row and the version lines — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt before §1 when F2 did not run.** Without the writer resolved, 1a's list is the project's own port; printing it as candidates is the 96 %-noise failure this skill exists to avoid.
- **Halt on any finding missing its anchors:** the write and publish (or mark, reserve, cursor) `file:line`s, the crash point, the writer it bypasses or `no outbox`, the fix in the project's own primitive.
- **No `[report-with-fix]` without a container oracle that failed** (or a two-ended static fact for §5). An in-memory bus, `Queue::fake()`, eager Celery or a mocked producer is not one.
- **No proposed fix may trade a loss for a phantom** (publishing before the commit) **or a duplicate for a loss** (marking before the confirm) without a written decision. The fix is the project's outbox port; with none, `/ds-fix` proposes one and its migration half goes to `/db-fix` when the database pack is installed.
- **Never contact a database, broker or connector outside a scratch container**, and never run `kubectl`, `helm` or a cloud CLI against a default context or profile.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "events look consistent"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Dual write ledger row; `/ds-fix` closes findings with the failing-first oracle, the fix at the project's outbox port, relay or inbox helper, a re-run of this detector and the sibling sweep.
- `messaging-scan` (consumer reserve absence, producer confirms), `coordination-scan` (leases, clock skew) and `event-contract-scan` (schemas, event stores, projections) are the neighbours named in § Boundaries; `@resilience-reviewer` judges these rows; the `outbox` and `idempotency` patterns are the design references.
- database `transaction-scan` § 1, § 2, § 5 and security `logic-race-scan` § 4–§ 5, when those packs are installed.

## Sources

Defaults are rows of `broker-semantics.md` (OX1–OX7, ID1–ID9, NT1–NT2, CY5, RB3–RB4, LV1, KA10, BQ4; read 2026-10-14 from debezium.io *Outbox Event Router* 3.7, docs.spring.io spring-modulith 2.1.1 *Events*, the MassTransit *Outbox* page, celery and rails changelogs, the laravel skeleton `config/queue.php`, spring-kafka source and NestJS *CQRS*). Grep literals are the distributed-systems research notes A § 15 (X-DUALWRITE, X-PUBTHENCOMMIT, OBX-01–03, CDC-01) and the per-stack C7 lanes (CEL-04, SQ-03, LAR-02, MT-01, the Java and Go save/commit-then-send shapes), tested on the research samples 2026-10-14; the outbox-writer resolution (F2) and the batch-5 eval § 3.2 and § 3.8 real-repo lesson, re-measured here. Paraphrased; no text reproduced beyond identifiers.
