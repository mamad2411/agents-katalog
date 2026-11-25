---
name: event-contract-scan
description: "Event contracts: schema compatibility, tolerant readers, naming, event-store appends, projections — read-only."
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: event-contract-scan

## Premise

An event outlives the code that wrote it. It sits in a topic, a dead-letter queue, an event store or a replay corpus while producers and consumers deploy on their own schedules, so every change to its shape is a change to a contract nobody re-signs. A required field added to the producer's schema rejects every event already stored; a field removed breaks every consumer still reading it; an enum symbol added crashes a reader that throws on the unknown; `amount` that quietly moves from minor to major units passes every compatibility tool and charges a hundred times over. Event-sourced systems add their own: an append with no expected version lets two deciders both win, a custom event table with no `UNIQUE(stream, version)` stores both, a projection that increments and saves its checkpoint separately double-counts on every redelivery, an `apply()` that sends mail resends it on every replay, and a UI that redirects to a projection right after a command shows the old state. This skill finds those places and proves each with its oracle. Read-only: it never edits code and never touches a registry, broker or store that is not a scratch container.

**A compatibility tool is an oracle only when it parsed both sides.** Measured on 2026-10-14 (the tool lane below): json-schema-diff exits **1** both for "breaking" and for a file it could not parse; `asyncapi diff -t breaking` exits **0** on a required payload field added (payload changes are *unclassified*); oasdiff reads a head with no paths as "every path removed"; buf exits **1** on "no .proto files" and **100** on a misaligned `--against` root. So a run prints one of `PASS`, `BREAKING`, `NOT-RUN (exit n: <first line>)` or `blocked (lane not installed)` — a tool that parsed nothing is **NOT-RUN, never PASS**, and with no base to compare against §1 and §4 print NOT-RUN.

It owns `/ds-audit`'s Contracts (§1–§5) and Event sourcing (§6–§10) ledger rows. `@event-sourcing-architect` (this pack) judges its rows.

**Every finding cites the schema, event type or append `<file:line>` + the base it was compared against (`--contract-base=<dir>` or the merge-base) + the reader or decider that breaks + the [`broker-semantics.md`](../../../../snippets/broker-semantics.md) row its verdict rests on (SZ1–SZ13, EV1–EV3), read at the installed version + the tool exit or the oracle that showed it, or the test that would settle it + the fix in the project's own primitive** (its schema module, its event envelope, its store's expected-version API, its projection base). A grep hit is a candidate. "Contracts look compatible" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) § 28–30. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Distributed, V323–V327.

## The rule

A candidate is a finding when all four hold — the protocol's gates as `precedents/distributed.md` § Reading the seven gates applies them.

1. **Part A holds: this is an event contract, an event-store write or a projection** that another process, a replay or a later release reads. A schema another service consumes, an envelope on a broker topic, an append to a stream, a read model fed from events. An HTTP request DTO, an LLM tool-parameter schema, a websocket push to a browser, a config schema or a type used inside one process fails here.
2. **Part B holds at the installed version.** The format's rule or the store's default is a named row: a reader field with no default (SZ2), `BACKWARD` checked against the latest version only (SZ3), Jackson's `FAIL_ON_UNKNOWN_PROPERTIES` on a plain `new ObjectMapper()` (SZ6), KurrentDB's Node `appendToStream` defaulting to `streamState: ANY` (EV1), Marten's plain `Append` with no guard (EV3). A verdict with no row is invalid.
3. **Nothing already controls it**, across files and repositories. A registry with `_TRANSITIVE` compatibility and auto-registration off, a CI compatibility gate, a Pact provider verification with `can-i-deploy`, a tolerant reader configured on the shared mapper, an upcaster for the old version, a library store that owns uniqueness (precedent 30), a projection write and checkpoint in one transaction. **Read the consumers in this repo and name the ones outside it**: a change with no reader anywhere is not a break.
4. **The oracle fired, or the fact is two-ended.** The format tool exited breaking on base → head (tier T, V323), a fixture or replay corpus failed (V324), two deciders both appended (V325), a redelivered event changed the read model (V326), or a static fact cites both ends — the removed field's `file:line` and the reader that dereferences it. Without one the row is `[report-flagged]` / Unconfirmed with the settling test written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration.
- **HTTP API drift** (an OpenAPI spec against the running server, request and response shapes) → backend `http-contract-scan` § 10 (its `oasdiff` lane), when the backend pack is installed. §1 here runs `oasdiff` only on **webhook** payloads this service sends. **Job payload drift inside one service across a deploy** (a job enqueued by the old release, run by the new) → backend `job-lifecycle-scan` § 3; this skill owns events that cross a process or service boundary. **Money as a float in a payload** → backend `wire-format-scan` § 5; §4 cites it when the unit or encoding of an existing event changes.
- **HTTP type drift — a shared contracts-package type re-declared by hand** (a type exported or `z.infer`-ed in the contracts package, and a hand-written `interface` with the same name in a web or mobile app) → code-quality `type-safety-scan` § 1, when that pack is installed: the client reads the response through its own copy, so a field the package renames compiles on both sides and fails at run time; the fix imports the package's type or schema. The server's side of the same shape stays backend `http-contract-scan` § 10. 5c prints these because its name rule cannot tell an HTTP payload from an event; part A routes them, never as a broker row. Without code-quality they are reported here tagged `HTTP type drift (owner pack not installed)`.
- **A parsed message cast to a type with no runtime check** (`JSON.parse(raw) as OrderEvent`, `cast(Order, json.loads(body))`) → code-quality `type-safety-scan` § 1, when that pack is installed: its measured BAD lines are exactly these, so §2 prints `→ code-quality type-safety-scan §1 (k)` and does not grade them. §2 owns the contract half — a topic whose schema is in S1–S3 consumed without its schema or registry deserializer, and what a malformed event does to the consumer. Without the code-quality pack §2 reports the casts, tagged `boundary cast (owner pack not installed)`.
- **NestJS microservice transports the global pipe never reaches** (`@EventPattern` / `@MessagePattern` without `inheritAppConfig` or `@UsePipes`) → backend `validation-boundary-scan` § 8; **unknown-key policy on HTTP DTOs** (`forbidNonWhitelisted`, a strict request schema) → its § 6. A strict reader on an **outbound** DTO is not §3 (precedent 28).
- **What happens to an event that keeps failing** (poison, DLQ, requeue loop) → `messaging-scan` (this pack) § 3; §2 and §3 here hand over a crash-looping malformed or unknown event with the contract mechanism as evidence. **A consumer with no reserve** → `messaging-scan` § 2; §8 here owns a **projection's** write and checkpoint.
- **A gap-blind catch-up cursor over an event table** (`WHERE id > $last`) → `dual-write-scan` (this pack) § 6. **Events ordered by a wall-clock timestamp across streams** (`ORDER BY created_at` in a projector) → `coordination-scan` (this pack) § 9; 9d prints its count. **Workflow history versioning** (a Temporal change with executions open) and a process manager's compensation → `workflow-scan` (this pack) § 2 and § 4–§ 6; the event schemas a process manager reads are §1–§5 here.
- **An async projection daemon on every replica** (Marten `DaemonMode.Solo` behind an HPA) → performance `request-path-scan` § 20 (V40), when that pack is installed; without it reported here tagged `once-per-fleet (owner pack not installed)`. **A read after a write on a lagging database replica** → database `connection-config-scan` § 8; §10 owns the projection lag.
- **A decide-append on a balance, stock or credit stream** → security `logic-race-scan` § 5, when the security pack is installed, with the missing expected version as evidence; without it reported here tagged `money invariant (owner pack not installed)`.
- **Writing consumer-driven contract tests** (Pact message pacts, Spring Cloud Contract) → testing `contract-test`. §1 reads whether they run and gate a deploy.

## Adapt to the codebase — the contract lanes

Read every schema, registry, contract and event-store library **with its version** (F1). Facts are rows of `broker-semantics.md` § Event contracts and event stores (tagged and dated there); a row tagged `[K?]` makes its verdict Unconfirmed until the settling test runs. The event-store lanes beyond Node (Marten, KurrentDB .NET and Python, Axon, the Python `eventsourcing` library) and the typed-deserializer lanes are in [`stacks.md`](stacks.md), loaded only when F1 printed that stack.

| Lane | What decides compatibility | Tool (§1) | Rows |
|---|---|---|---|
| **Protobuf** (`*.proto`, `buf.yaml`) | field numbers and types; FILE is buf's default category, WIRE_JSON the recommended minimum for events | `buf breaking <module> --against <base>/<module>` | SZ1 |
| **Avro** (`*.avsc`, a Confluent registry) | a reader field with no default the writer lacks is an error; a writer enum symbol unknown to the reader needs the reader's `default`; renames only through aliases; `BACKWARD` checks the latest version only | the `avsc` resolver both ways (block below), or the registry's `test-compatibility` | SZ2, SZ3 |
| **JSON Schema** (`$schema` = json-schema.org) | open vs closed content model (`additionalProperties`); `required`; types | `json-schema-diff` both directions | SZ5 |
| **AsyncAPI 2/3** | channel addresses and operations (classified); message payloads (**unclassified** — compare them as JSON Schema) | `asyncapi diff -t breaking`, plus the unclassified count | SZ4 |
| **OpenAPI `webhooks:`** this service sends | a webhook body is judged as a request: removed or retyped properties break receivers | `oasdiff breaking --fail-on WARN`, read for direction | SZ7 |
| **TS-only event types** (no schema file) | the old consumer compiled against the new type | read the diff of the type (5c/§4); a `tsc` run on a scratch copy is the oracle | — |
| **Consumer-driven** — Pact message pacts, Spring Cloud Contract | the provider's `MessageProviderPact.verify()` in CI; `pact-broker can-i-deploy` before a deploy (pact-js 17.1.4, research notes B § 5.0, 2026-10-14) | the CI line in S6 is the gate | — |
| **Event stores** — KurrentDB Node (`@kurrent/kurrentdb-client`), Emmett, a custom table through an ORM | Node `appendToStream` defaults to `ANY`; a custom table owns no uniqueness until it declares it | 6a, 7a–7c | EV1; others in [`stacks.md`](stacks.md) (EV2, EV3) |

### The tool lane — exit codes (measured 2026-10-14, build)

| Tool | Clean | Breaking | NOT-RUN shapes | Traps the block guards |
|---|---|---|---|---|
| buf 1.73.0 | 0 | 100, with `file:line:col:` lines | 1: "had no .proto files", a missing path, a missing branch, a shallow clone without the base branch | `--against '.git#branch=main'` from a module that is not the repo root, without `subdir=`, exits 100 on an **additive** change ("Previously present file … was deleted"): roots misaligned. The block compares directory to directory and turns that line into NOT-RUN when the file exists in head |
| json-schema-diff 1.0.0 | 0 | 1 + "Breaking changes found" | 1 + `VError` (a parse error, a missing file, an unresolved `$ref`, a 2019-09 or 2020-12 `$schema`: `no schema with key or ref "https://json-schema.org/draft/2020-12/schema"`, measured 2026-10-14) — the **same exit code** as breaking; the block prints a 2019-09/2020-12 document NOT-RUN before running it | base → head is backward only: a head emptied to `{}` passes it and fails head → base, so both directions run. `enum`, `const`, `pattern`, `format`, `if`/`then`/`else` are **not compared** (the package's `KEYWORDS.md`): an added enum symbol prints "No differences found" — the block prints `PARTIAL` |
| @asyncapi/cli 6.2.1 | 0 | 1 + `DiffBreakingChangeError` | 1 + `ValidationError` | a required payload field added is `unclassified`, exit 0. An `info.version` edit alone (2.2.0 → 2.3.0) exits **1** as `"path": "/info/version", "type": "breaking"` (measured 2026-10-14): a correctly bumped document reads as broken — the block prints `VERSION-BUMP` when `/info/version` is the only breaking path. The CLI writes `~/.asyncapi-analytics` and reports each run to a remote metrics endpoint unless `CI=true` or `ASYNCAPI_METRICS_CONFIG_PATH` names a file with analytics off — the block sets both |
| oasdiff 1.33.0 | 0 | 1 at the `--fail-on` level | 102 (a file that did not load) | a head reduced to `openapi: 3.0.3` exits 1 as "api-path-removed": check S4 parsed. A webhook property removed is WARN (`--fail-on ERR` exits 0); a property newly *required* in what we send is ERR though receivers are unaffected. Never install it from npm (a placeholder package, SZ7) |
| avsc 5.7.9 resolver | 0 | 3 (the block's one-liner) | 2 (a schema that did not parse) | `createResolver` takes reader ← writer: run both directions; an added enum symbol fails forward only |

## Read the code — per event, before any §

Start from F2's contract inventory and the consumers, not from vocabulary. For each event type, answer these; the § each answer feeds is in brackets.
- **Who reads this event, where, and on which release?** The consumers in this repo (5b, the subscribe lines), the ones outside it (an AsyncAPI `receive` operation, a Pact consumer, a README), and the stored events a replay will read [§1, §5].
- **Which direction must the change be compatible in?** Consumers upgrade first (backward), producers first (forward), or independently (full); is the registry mode transitive for a topic whose retention is long or infinite [§1]?
- **Where is the payload checked against its contract** — a registry deserializer, a generated class, a zod or pydantic parse on the path — and what does the consumer do with a malformed one: park it, or throw and redeliver it forever [§2]?
- **What does the reader do with what it does not know** — an extra field, a new enum symbol, a new event type? Is the strict schema on the inbound or the outbound side [§3]?
- **Did the meaning change while the shape stayed** — a unit, a scale, a time zone, what `null` means, what a status covers [§4]?
- **Is the name in one place** — a shared constant, a generated client, the AsyncAPI document — and does the envelope carry a version the readers branch on, with an upcaster for each old one [§5]?
- **For a store:** what did the decider read before it appended, and does the append carry that version; what keeps two writers from both appending version n+1 [§6, §7]?
- **For a projection:** is its write idempotent per event, and does the checkpoint commit in the same transaction; does `apply` only mutate state; does a snapshot carry the schema version it was written with [§8, §9]?
- **For a UI flow:** after the command returns, what does the next screen read, and does it wait for the position the command returned [§10]?

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 has no `mapfile`). Grep **N** feeds detector **§N**; F lines are the gates and the inventory. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first** in every command, exclusions last (for a path several globs match, the last one wins). Any `rg` exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`). Migrations are searched **on purpose** for §7: the schema is the evidence.

```bash
export LC_ALL=C; ROOTS=(.)   # server and client code; in a monorepo name the apps. Schema, migration and CI greps always search .
CODE=(-g '*.{ts,mts,cts,tsx,js,mjs,cjs,jsx,py,java,kt,go,cs,rb,php}')
XT=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,generated,__generated__,vendor,target,bin,obj}/**'
    -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
    -g '!**/*.{spec,test,e2e-spec,fuzz,stories}.*' -g '!**/{test_*,*_test}.{py,go}' -g '!**/*{Test,Tests,IT}.{java,kt,cs}'
    -g '!**/*.d.ts' -g '!**/*.min.*' -g '!**/{docs,ai,.claude,.refract-fixture}/**')
X=("${XT[@]}" -g '!**/{migrations,migration,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
T=$(mktemp -d "${TMPDIR:-/tmp}/ecs.XXXXXX"); trap 'rm -rf "$T"' EXIT   # lists and base copies live here; nothing is written into the repo
CONS='@Processor\(|\bextends\s+\w*WorkerHost\b|\bnew\s+Worker\(|\beachMessage\b|\beachBatch\b|\.subscribe\(|\.consume\(|@(?:EventPattern|MessagePattern|OnEvent|EventsHandler|SqsMessageHandler|RabbitSubscribe)\(|@(?:KafkaListener|RabbitListener|SqsListener|JmsListener|StreamListener)\b|\bIConsumer<|@(?:shared_task|app\.task)\b|\bhandleMessage\b|\bon_message\b|\bConsumer\(|\bmessage_handler\b'
# F1 schema, contract and event-store libraries with their declared versions (gate 3: SZ1-SZ7, EV1-EV3 are read at these); F1L the locked versions (pnpm, npm, yarn) — the lockfile wins over the range
rg -n --no-heading --pcre2 '"(?:@bufbuild/[\w-]+|protobufjs|google-protobuf|@grpc/proto-loader|avsc|@kafkajs/confluent-schema-registry|@confluentinc/schemaregistry|@asyncapi/[\w-]+|json-schema-diff|ajv|zod|valibot|class-validator|@sinclair/typebox|@pact-foundation/[\w-]+|@kurrent/kurrentdb-client|@eventstore/db-client|@event-driven-io/emmett[\w-]*|@nestjs/cqrs|@nestjs/microservices)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -U --pcre2 '^[ \t]*["\x27]?/?(?:@bufbuild/[\w-]+|protobufjs|google-protobuf|@grpc/proto-loader|avsc|@kafkajs/confluent-schema-registry|@confluentinc/schemaregistry|@asyncapi/[\w-]+|json-schema-diff|ajv|zod|valibot|class-validator|@sinclair/typebox|@pact-foundation/[\w-]+|@kurrent/kurrentdb-client|@eventstore/db-client|@event-driven-io/emmett[\w-]*|@nestjs/cqrs|@nestjs/microservices)@\d[\w.-]*|"node_modules/(?:@bufbuild/[\w-]+|protobufjs|google-protobuf|@grpc/proto-loader|avsc|@kafkajs/confluent-schema-registry|@confluentinc/schemaregistry|@asyncapi/[\w-]+|json-schema-diff|ajv|zod|valibot|class-validator|@sinclair/typebox|@pact-foundation/[\w-]+|@kurrent/kurrentdb-client|@eventstore/db-client|@event-driven-io/emmett[\w-]*|@nestjs/cqrs|@nestjs/microservices)":\s*\{\s*\n\s*"version":\s*"[^"]+"|^"?(?:@bufbuild/[\w-]+|protobufjs|google-protobuf|@grpc/proto-loader|avsc|@kafkajs/confluent-schema-registry|@confluentinc/schemaregistry|@asyncapi/[\w-]+|json-schema-diff|ajv|zod|valibot|class-validator|@sinclair/typebox|@pact-foundation/[\w-]+|@kurrent/kurrentdb-client|@eventstore/db-client|@event-driven-io/emmett[\w-]*|@nestjs/cqrs|@nestjs/microservices)@[^\n]*:\s*\n\s+version:?\s+"?[\d.]+' -g '**/{pnpm-lock.yaml,package-lock.json,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '\b(?:Marten|KurrentDB\.Client|EventStore\.Client[\w.]*|Confluent\.SchemaRegistry[\w.]*|PactNet|axon[\w-]*|kafka-avro-serializer|kafka-protobuf-serializer|kafka-json-schema-serializer|kafka-schema-registry-maven-plugin|spring-cloud-contract[\w-]*|au\.com\.dius\.pact[\w.:-]*|jackson-databind|eventsourcing|kurrentdbclient|esdbclient|pydantic|pact-python|fastavro|confluent-kafka)\b' -g '**/{requirements*.txt,pyproject.toml,Pipfile,pom.xml,build.gradle,build.gradle.kts,*.csproj,Directory.Packages.props,go.mod,Gemfile,composer.json}' -g '!**/node_modules/**' .
# F2 the contract inventory. S1 proto/Avro files; S2 AsyncAPI documents; S3 JSON Schemas (json-schema.org $schema only — tool configs point at schemastore);
#    S4 OpenAPI documents with webhooks; S5 buf breaking config and registry compatibility settings; S6 the CONTRACT GATE in CI (a compatibility tool or Pact verify/can-i-deploy)
rg --files -g '*.{proto,avsc,avdl}' "${XT[@]}" . | sort > "$T/s1"; echo "S1 proto/avro $(wc -l < "$T/s1" | tr -d ' ')"; head -20 "$T/s1"
rg -l --pcre2 '^\s*["\x27]?asyncapi["\x27]?\s*:\s*["\x27]?[23]\.' -g '*.{yml,yaml,json}' "${XT[@]}" . | sort > "$T/s2"; echo "S2 asyncapi $(wc -l < "$T/s2" | tr -d ' ')"; head -20 "$T/s2"
rg -l --pcre2 '"\$schema"\s*:\s*"https?://json-schema\.org/' -g '*.json' "${XT[@]}" . | sort > "$T/s3"; echo "S3 json-schema $(wc -l < "$T/s3" | tr -d ' ')"; head -20 "$T/s3"
rg -l --pcre2 '^webhooks:|"webhooks"\s*:\s*\{' -g '*.{yml,yaml,json}' "${XT[@]}" . | sort > "$T/s4"; echo "S4 openapi-webhooks $(wc -l < "$T/s4" | tr -d ' ')"; head -20 "$T/s4"
rg -n --no-heading -i --pcre2 '^\s*breaking:|\b(?:schema\.)?compatibility(?:[._]?level)?\b["\x27]?\s*[:=]\s*["\x27]?(?:BACKWARD|FORWARD|FULL|NONE)(?:_TRANSITIVE)?\b|\bauto[._]?register[._]?schemas\b|\buse[._]?latest[._]?version\b' --hidden -g '**/buf.yaml' -g '*.{yml,yaml,json,properties,conf,env,ts,js,java,kt,cs,py}' -g '!.git/**' -g '!**/node_modules/**' -g '!**/package-lock.json' "${XT[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bbuf\s+breaking\b|\basyncapi\s+diff\b|\bjson-schema-diff\b|\boasdiff\s+breaking\b|\bcan-i-deploy\b|\btest-compatibility\b|\bMessageProviderPact\b|\bpact(?:-provider)?[\w-]*\s+verify\b' --hidden -g '**/.github/**' -g '**/.gitlab-ci.yml' -g '**/{Makefile,Jenkinsfile,azure-pipelines.yml,bitbucket-pipelines.yml,package.json}' -g '**/.circleci/**' -g '!**/node_modules/**' .
# 2a a message body parsed straight into an object (a parse wrapped in a schema call is excluded by the lookbehind); 2b the 2a files with no schema or validator call at all; 2c 2a lines in a consumer file
rg -n --no-heading --pcre2 '(?<![\w.]\()\bJSON\.parse\(\s*(?:\w+(?:\?|!)?\.)*(?:value|content|body|data|Body|payload|message|msg)\b|(?<![\w.]\()\bjson\.loads\(\s*(?:\w+\.)?(?:value|body|data|payload|message|msg|raw)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" > "$T/p2"
echo "2a $(wc -l < "$T/p2" | tr -d ' ') parses"; cut -d: -f1 "$T/p2" | sort -u | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?<!\bJSON)\.(?:parse|safeParse|parseAsync|safeParseAsync|validate\w*|decode|assert\w*|check)\(|\bplainToInstance\(|\bvalidate(?:OrReject|Sync)?\(|\bmodel_validate(?:_json)?\(|\bparse_obj\(|\bTypeAdapter\(|\bajv\b|\bValue\.Check\(|\bis\w+Event\(' > "$T/p2b"; echo "2b files with no validator: $(wc -l < "$T/p2b" | tr -d ' ')"; cat "$T/p2b"
cut -d: -f1 "$T/p2" | sort -u | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 "$CONS" > "$T/p2c"; echo "2c in a consumer file: $(rg -c -F -f "$T/p2c" "$T/p2" 2>/dev/null || echo 0)"; rg -F -f "$T/p2c" "$T/p2" 2>/dev/null
# 3a a switch or guard that throws on an unknown type; 3b strict readers in code, and additionalProperties:false in schema documents and consumer files only (inbound or outbound is the read, precedent 28);
#    3c tolerance markers that clear 3b; 3d Avro enums with no default (a new symbol breaks old readers, SZ2)
rg -n --no-heading --pcre2 'default:\s*(?:return\s+)?assertNever\(|default:\s*throw\s+new\s+\w*Error\(\s*[\x60"\x27](?:Unknown|Unhandled|Unexpected|Unsupported)\s+(?:event|message|type)|const\s+_\w*\s*:\s*never\s*=|\bcase\s+_\s*:\s*raise\b|\bassert_never\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\.strict\(\)|\bextra\s*=\s*["\x27]forbid["\x27]|\bExtra\.forbid\b|UnmappedMemberHandling\.Disallow\b|=\s*new\s+ObjectMapper\(\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
{ cat "$T/s2" "$T/s3"; rg -l --pcre2 "$CONS" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"; } | sort -u | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 '["\x27]?additionalProperties["\x27]?\s*:\s*false'
rg -n --no-heading --pcre2 'FAIL_ON_UNKNOWN_PROPERTIES\s*,\s*false|\bignoreUnknown\s*=\s*true|\.passthrough\(\)|\.catchall\(|\bextra\s*=\s*["\x27](?:ignore|allow)["\x27]|READ_UNKNOWN_ENUM_VALUES_(?:USING_DEFAULT_VALUE|AS_NULL)|@JsonEnumDefaultValue' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U -o -r '$1' --pcre2 '"type"\s*:\s*"enum"\s*,\s*"name"\s*:\s*"(\w+)"(?:(?!"default")[^}])*\}' -g '*.avsc' "${XT[@]}" .
# 5a one topic or queue name spelled as a literal in 2+ files, and near-twins (orders.placed / order.placed); 5b names produced but never consumed here, and the reverse;
#    5c one *Event/*Message/*Payload type declared in 2+ services; 5d version fields and upcasters (their absence in a store whose events changed shape is the read)
rg -o --no-heading --no-line-number --pcre2 '\b(?:topic|topics|queue|queueName|routingKey|routing_key|exchange)\s*[:=]\s*\[?\s*["\x27]\K[\w.:/-]{3,}(?=["\x27])|@(?:EventPattern|MessagePattern|OnEvent|Processor|KafkaListener|RabbitListener|SqsListener)\(\s*(?:topics\s*=\s*)?["\x27]\K[\w.:/-]{3,}(?=["\x27])|\.(?:emit|publish|subscribe|send|add)\(\s*["\x27]\K[\w-]+(?:[.:/][\w-]+)+(?=["\x27])' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/n5"
awk '{i=index($0,":"); print substr($0,i+1)"\t"substr($0,1,i-1)}' "$T/n5" | sort -u | awk -F'\t' '{n[$1]++; f[$1]=f[$1]" "$2} END {for (k in n) if (n[k]>1) print "5a " n[k] " files  " k " :" f[k]}' | sort -k2,2nr | head -40
awk '{print substr($0,index($0,":")+1)}' "$T/n5" | sort -u | awk '{k=tolower($0); gsub(/[._:\/-]/,"",k); sub(/s$/,"",k); g=k; gsub(/s/,"",g); if (seen[g] && seen[g]!=$0) print "5a near-twin  " seen[g] "  " $0; else seen[g]=$0}'
rg -o --no-filename --no-line-number --pcre2 '\b(?:subscribe|consume)\(\s*\{?\s*(?:topics?|queue|subject)\s*:\s*\[?\s*["\x27]\K[\w.:/-]+|@(?:EventPattern|MessagePattern|OnEvent|KafkaListener|RabbitListener|SqsListener)\(\s*(?:topics\s*=\s*)?["\x27]\K[\w.:/-]+|\bnew\s+Worker\(\s*["\x27]\K[\w.:/-]+|@Processor\(\s*["\x27]\K[\w.:/-]+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$T/sub"
rg -o --no-filename --no-line-number --pcre2 '\b(?:send|sendMessage|publish|produce|emit)\(\s*(?:\{\s*(?:topic|queue|subject|exchange|channel)\s*:\s*)?["\x27]\K[\w-]+(?:[.:/][\w-]+)+|\bnew\s+Queue\(\s*["\x27]\K[\w.:/-]+|\bregisterQueue\(\s*\{\s*name\s*:\s*["\x27]\K[\w.:/-]+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$T/pub"
echo "5b produced, never consumed here: $(comm -23 "$T/pub" "$T/sub" | tr '\n' ' ')"; echo "5b consumed, never produced here: $(comm -13 "$T/pub" "$T/sub" | tr '\n' ' ')"
rg -o -n --no-heading --pcre2 '(?:\binterface|\btype|\bclass|\brecord|^\s*message)\s+\K\w+(?:Event|Message|Payload)\b(?=\s*(?:[{=(<:]|extends|implements|$))' "${CODE[@]}" -g '*.proto' "${X[@]}" "${ROOTS[@]}" | awk -F: '{split($1,d,"/"); print $NF"\t"d[2]"/"d[3]"\t"$1}' | sort -u | awk -F'\t' '{if (!((($1) SUBSEP $2) in seen)) {seen[$1,$2]=1; n[$1]++}; f[$1]=f[$1]" "$3} END {for (k in n) if (n[k]>1) print "5c " n[k] " services  " k " :" f[k]}' | sort -k2,2nr | head -30
rg -c --pcre2 '\b(?:schemaVersion|schema_version|eventVersion|event_version|payloadVersion|dataschema|specversion)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | head -20; cat "$T/s1" "$T/s2" "$T/s3" | tr '\n' '\0' | xargs -0 -r rg -c --pcre2 '\b(?:schemaVersion|schema_version|eventVersion|event_version|version)\b'
rg -n --no-heading --pcre2 '\b(?:\w*Upcaster|SingleEventUpcaster|EventUpcaster|upcast\w*|Upcast<|registerUpcaster|eventUpcasters)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -20
# ES evidence (§6-§9 read it): an event-store client call or an aggregate base (es0); an event table carrying a stream id and a version (es7)
rg -l0 --pcre2 '\.appendToStream\(|\bAppendToStreamAsync\(|\bappend_to_stream\(|\.Events\.(?:Append|StartStream|FetchForWriting|AggregateStreamAsync)\b|\bextends\s+\w*Aggregate\w*\b|\bAggregateRoot\b|@Aggregate\b|@EventSourcingHandler\b|\bloadFromHistory\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/es0"
rg -l0 -i --pcre2 'create\s+table\s+(?:if\s+not\s+exists\s+)?["\x60\w.]*event' -g '*.sql' "${XT[@]}" . | xargs -0 -r rg -l0 -i --pcre2 '\b(?:stream|aggregate)_?id\b' | xargs -0 -r rg -l0 -i --pcre2 '\b(?:version|seq\w*|revision)\b' > "$T/es7"
echo "ES evidence: $(tr -cd '\0' < "$T/es0" | wc -c | tr -d ' ') store/aggregate files, $(tr -cd '\0' < "$T/es7" | wc -c | tr -d ' ') event tables"
# 6a a Node append with no expected version (EV1: the default is ANY) — Marten, KurrentDB .NET/Python → stacks.md
rg -n --no-heading --pcre2 '\.appendToStream\(\s*[^,]+,\s*[^,{}]+(?:\([^()]*\))?\s*\)\s*;|\.appendToStream\([^\n]*\b(?:streamState|expectedRevision)\s*:\s*ANY\b|\bappendToStream\([^\n]*\bexpectedStreamVersion\s*:\s*undefined\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7a es7 tables lacking UNIQUE/PK(stream, version); 7b a later unique index that clears 7a; 7c Prisma models and ORM entities with a stream id and no composite unique
xargs -0 -r rg --files-without-match -i --pcre2 '(?:unique|primary\s+key)\s*\(\s*["\x60\w]*(?:stream|aggregate)\w*["\x60]?\s*,\s*["\x60\w]*(?:version|seq|sequence|revision|position)' < "$T/es7"
rg -n --no-heading -i --pcre2 'create\s+unique\s+index[^\n]*\bon\s+["\x60\w.]*event\w*["\x60]?\s*\([^)]*(?:stream|aggregate)\w*[^)]*(?:version|seq|revision|position)' -g '*.{sql,ts,js,py}' "${XT[@]}" .
rg -n --no-heading -U --pcre2 '^\s*model\s+\w*Event\w*\s*\{(?=[^}]*\b(?:streamId|stream_id|aggregateId|aggregate_id)\b)(?:(?!@@(?:unique|id)\(\s*\[\s*\w*(?:stream|aggregate)\w*\s*,)[^}])*\}' -g '*.prisma' "${XT[@]}" . | rg --pcre2 '^\S+:\d+:\s*model\b'
rg -l0 --pcre2 '\bclass\s+\w*Event\w*\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '@Entity\b|@Table\b|\bmodels\.Model\b|\bpgTable\(|\b__tablename__\b' | xargs -0 -r rg -l0 --pcre2 '\b(?:streamId|stream_id|aggregateId|aggregate_id)\b' | xargs -0 -r rg --files-without-match --pcre2 '@Unique\(|@Index\([^)]*unique|unique_together|UniqueConstraint\(|@@unique|\bunique\(\s*\[|\.unique\(\)'
# 8a projection files (an event-handler registration, a projection class, a projector or read-model file name) that increment, save a checkpoint, or insert with no conflict guard
rg -l0 --pcre2 '@(?:EventsHandler|EventHandler|OnEvent|Projection)\b|\bclass\s+\w*(?:Projection|Projector|ReadModel)\w*|\b(?:project|when|on)\w*\s*\(\s*\w+\s*:\s*\w+Event\b' "${CODE[@]}" "${X[@]}" -g '!**/*.{tsx,jsx,vue,svelte}' "${ROOTS[@]}" > "$T/proj0"; rg --files -0 -g '**/*{projector,read-model,readmodel,read_model}*.{ts,mts,js,mjs,py,java,kt,go,cs,rb,php}' "${X[@]}" "${ROOTS[@]}" >> "$T/proj0"
tr '\0' '\n' < "$T/proj0" | sort -u | tr '\n' '\0' | xargs -0 -r rg -H -n --no-heading --pcre2 '(?i:\bset\s+\w+\s*=\s*\w+\s*[+-]\s*(?:\d|\$|:|\?))|\$inc\b|\.increment\(|\bcheckpoints?\w*\.(?:save|set|update|store|upsert|commit)\(|\bsave\w*Checkpoint\(|(?i:insert\s+into\s+\w+(?![^\n]*on\s+conflict))' | "${NC[@]}"
# 9a apply/when/evolve bodies in aggregate files that do I/O, the body ending at the method's own closing line (read: rebuild must be pure); 9b snapshot code (saveSnapshot, OrderSnapshots, order_snapshots) in a file that names an aggregate or a stream id, with no version; 9c an async projection daemon (replicas → performance §20); 9d events ordered by a timestamp (→ coordination-scan §9)
rg -l0 --pcre2 '\bextends\s+\w*Aggregate\w*\b|\bAggregateRoot\b|@Aggregate\b|@EventSourcingHandler\b|\bloadFromHistory\(|\bevolve\s*[(=:]|\bclass\s+\w+Aggregate\b|\bdef\s+(?:apply|when|mutate)\s*\(\s*self\s*,\s*\w*event' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading -U -o -r '$2' --pcre2 '^([ \t]*)(?:(?:public|private|protected|override)\s+)*(?:async\s+)?(?:def\s+)?((?:apply|when|evolve|mutate|on[A-Z])\w*)\s*\([^)]*\)\s*(?::\s*[\w<>\[\]]+\s*)?[{:](?:(?!\1(?:\}|def\s|async\s+def\s))[^\n]*\n){0,12}?(?!\1(?:\}|def\s|async\s+def\s))[^\n]*(?:\bawait\s|\bfetch\(|\.send\w*\(|\.publish\(|\.emit\(|\bqueue\w*\.add\(|\bhttp\w*\.|\bmailer\b|\bemail\w*\.|\bsms\w*\.)' | "${NC[@]}"
[ -s "$T/es0" ] && rg -l0 -i --pcre2 'snapshot\w*\s*(?:=|\(|:)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 -i --pcre2 '\baggregate\w*|\bstream_?id\b|\bloadFromHistory\b|\bAggregateStream\w*' | xargs -0 -r rg --files-without-match -i --pcre2 '\bsnapshot_?(?:schema_?)?version\b|\bschemaVersion\b|\bstreamVersion\b|\bsnapshot\w*\.version\b|\bversion\s*[:=]'
[ -s "$T/es0" ] && rg -n --no-heading --pcre2 '\bDaemonMode\.(?:Solo|HotCold)\b|\bAddAsyncDaemon\(|\bstartProjectionDaemon\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -c -i --pcre2 'from\s+["\x60\w.]*events?\b[^\n]*order\s+by\s+(?:\w+\.)?(?:created_at|occurred_at|timestamp|ts|recorded_at)\b(?![^\n]*,\s*(?:id|version|position|seq))' "${CODE[@]}" -g '*.sql' "${X[@]}" "${ROOTS[@]}"
# 10 only where an async read model exists: 10a a command dispatched, then a redirect, in one file; 10b a client mutation, then navigation; 10c position or version waits that clear it
rg -l0 --pcre2 '\bclass\s+\w*(?:Projector|ReadModel|EventProjection|StreamProjection)\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$T/projR"; rg --files -0 -g '**/*{projector,read-model,readmodel,read_model}*.{ts,mts,js,mjs,py,java,kt,go,cs,rb,php}' "${X[@]}" "${ROOTS[@]}" >> "$T/projR"
if [ -s "$T/projR" ] || [ -s "$T/es0" ]; then
  rg -l0 --pcre2 '\bcommandBus\.execute\(|\bCommandBus\b|\bmediator\.Send\(|\b_mediator\.Send\(|\bsender\.Send\(|\bdispatch\(\s*new\s+\w+Command\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bres\.redirect\(|\breply\.redirect\(|@Redirect\(|\bRedirect(?:ToAction|ToRoute)?\(|\bredirect\(|\bHttpStatus\.SEE_OTHER\b|\b303\b' | "${NC[@]}"
  rg -n --no-heading -U --pcre2 '\b(?:await\s+[\w.]*(?:mutateAsync|post|create\w*|submit\w*)\(|method:\s*["\x27]POST["\x27])[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*\b(?:navigate|router\.(?:push|replace)|redirect|goto)\(' -g '*.{ts,tsx,js,jsx,vue,svelte}' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '\b(?:navigate|router\.(?:push|replace)|redirect|goto)\('
  rg -n --no-heading --pcre2 '\b(?:waitFor(?:Position|Version|Projection|Checkpoint)\w*|minPosition|expectedVersion|atLeastVersion|consistencyToken|readYourWrites|WaitForNonStaleProjectionData\w*|waitForNonStale\w*)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -10
else echo "10 N/A (no projection or read-model class and no event store)"; fi
```

### The contract lane — §1 and §4 against a base

Appended to the block above, in the same script (it reads `$T/s1`–`$T/s4` and `$T/n5`). The base is `--contract-base=<dir>` — a tree that mirrors repo-relative paths (`<dir>/schemas/orders.avsc` is the base of `schemas/orders.avsc`), for a repo with no base branch or a fixture — passed as `CONTRACT_BASE`, else the merge-base with `BASE_BRANCH` (default `origin/main`), whose copies are read with `git show` into `$T`. No base → `BASE NOT-RUN`, and §1 and §4 print `NOT-RUN (no base)`. Tools resolve from `PATH` or `./node_modules/.bin`; a missing one prints `blocked`, and its schema's changed lines still print in 4 for the read.

```bash
printf '{"analyticsEnabled":"false","infoMessageShown":"true","userID":"none"}' > "$T/aa.json"   # the AsyncAPI CLI reports usage to a remote endpoint unless told not to
CB="${CONTRACT_BASE:-}"; BB="${BASE_BRANCH:-origin/main}"; B="$T/base"; mkdir -p "$B"; MB=""
cat "$T/s1" "$T/s2" "$T/s3" "$T/s4" | sed 's|^\./||' | sort -u > "$T/heads"
if [ -n "$CB" ]; then if [ -d "$CB" ]; then B="${CB%/}"; echo "BASE contract-base $B"; else B=""; echo "BASE NOT-RUN (contract-base $CB is not a directory)"; fi
elif MB=$(git merge-base HEAD "$BB" 2>/dev/null); then echo "BASE $BB @ $MB"
  { cat "$T/heads"; cut -d: -f1 "$T/n5" | sed 's|^\./||'; git diff --relative --name-only --diff-filter=D "$MB" -- '*.proto' '*.avsc' '*.avdl' '*.json' '*.yaml' '*.yml'; git ls-tree -r --name-only "$MB" -- . | rg --pcre2 '\.(?:proto|avsc|avdl)$'; } | sort -u > "$T/bl"
  while read -r p; do git cat-file -e "$MB:./$p" 2>/dev/null || continue; mkdir -p "$B/$(dirname "$p")"; git show "$MB:./$p" > "$B/$p"; done < "$T/bl"
else B=""; echo "BASE NOT-RUN (no merge-base with $BB: a shallow clone or no such branch; pass --contract-base=<dir>)"; fi
v() { if [ "$3" = 0 ]; then echo "1t $1 $2 PASS"; elif [ "$3" = "$4" ] && rg -q --pcre2 "$5" "$T/o"; then echo "1t $1 $2 BREAKING"; rg -v --pcre2 '^(?:WARNING|FATAL)\b|^\s*$' "$T/o" | head -6; else echo "1t $1 $2 NOT-RUN (exit $3: $(rg -m1 -v --pcre2 '^(?:WARNING|FATAL)\b|^\s*$' "$T/o"))"; fi; }
if [ -n "$B" ]; then
  { rg --files -g '*.{proto,avsc,avdl}' "$B"; rg -l --pcre2 '^\s*["\x27]?asyncapi["\x27]?\s*:|"\$schema"\s*:\s*"https?://json-schema\.org/|^webhooks:' -g '*.{json,yml,yaml}' "$B"; } | sed "s|^$B/||" | sort -u | while read -r p; do [ -e "$p" ] || echo "1d deleted since base: $p (a removed schema breaks every consumer still subscribed)"; done
  BUF=$(command -v buf || ls ./node_modules/.bin/buf 2>/dev/null); JSD=$(command -v json-schema-diff || ls ./node_modules/.bin/json-schema-diff 2>/dev/null)
  AAPI=$(command -v asyncapi || ls ./node_modules/.bin/asyncapi 2>/dev/null); OAS=$(command -v oasdiff); AVSC=$(node -e 'require.resolve("avsc")' 2>/dev/null && echo yes)
  # 1a protobuf (SZ1): one run per module root (a buf.yaml directory, else the protos' common directory); exit 0 clean · 100 breaking · anything else NOT-RUN
  MODS=$(rg --files -g '**/buf.yaml' "${XT[@]}" . | sed 's|/buf.yaml$||'); [ -z "$MODS" ] && MODS=$(rg --pcre2 '\.proto$' "$T/s1" | sed 's|/[^/]*$||' | awk 'NR==1{p=$0} {while (index($0"/", p"/")!=1) sub(/\/[^\/]*$/,"",p)} END{print p}')
  for m in $MODS; do [ -d "$B/$m" ] || { echo "1t buf $m NOT-RUN (no base copy)"; continue; }
    if [ -z "$BUF" ]; then echo "1t buf $m blocked (lane not installed: buf@1.73.0 — npm i -D @bufbuild/buf)"; continue; fi
    "$BUF" breaking "$m" --against "$B/$m" > "$T/o" 2>&1; e=$?
    rg -o -r '$1' --pcre2 'Previously present file "([^"]+)" was deleted' "$T/o" | while read -r f; do [ -e "$m/$f" ] && echo "1t buf $m NOT-RUN (roots misaligned: $f exists in head — a missing subdir= or a different module root)"; done
    v buf "$m" "$e" 100 '^\S+:\d+:\d+:'; done
  # 1b JSON Schema (SZ5): backward = old events read with the new schema; forward = new events read by old readers. enum, const, pattern, format, if/then/else are NOT compared by json-schema-diff 1.0.0
  for f in $(cat "$T/s3"); do f=${f#./}; [ -f "$B/$f" ] || continue; if [ -z "$JSD" ]; then echo "1t json-schema-diff $f blocked (lane not installed: json-schema-diff@1.0.0)"; continue; fi
    rg -q --pcre2 '"\$schema"\s*:\s*"https?://json-schema\.org/draft/20(?:19-09|20-12)/' "$f" "$B/$f" && { echo "1t json-schema-diff $f NOT-RUN (a 2019-09/2020-12 \$schema: json-schema-diff 1.0.0 cannot load its meta-schema, SZ9 — read the diff of required, properties and additionalProperties)"; continue; }
    "$JSD" "$B/$f" "$f" > "$T/o" 2>&1; v json-schema-diff "$f(backward)" $? 1 '^Breaking changes found'
    "$JSD" "$f" "$B/$f" > "$T/o" 2>&1; v json-schema-diff "$f(forward)" $? 1 '^Breaking changes found'
    rg -q --pcre2 '"(?:enum|const|pattern|format|if|patternProperties|dependencies)"\s*:' "$f" "$B/$f" && echo "1t json-schema-diff $f PARTIAL (enum/const/pattern/format/if not compared — read their diff)"; done
  # 1c AsyncAPI (SZ4): -t breaking classifies channels and operations; payload schema changes are 'unclassified' and never fail it — count them and compare the payloads (1b) or read
  for f in $(cat "$T/s2"); do f=${f#./}; [ -f "$B/$f" ] || continue; if [ -z "$AAPI" ]; then echo "1t asyncapi $f blocked (lane not installed: @asyncapi/cli@6.2.1)"; continue; fi
    CI=true ASYNCAPI_METRICS_CONFIG_PATH="$T/aa.json" "$AAPI" diff "$B/$f" "$f" -t breaking -f json > "$T/o" 2>&1; e=$?; n=$(rg -c --pcre2 '"path":' "$T/o")
    if [ "$e" = 1 ] && [ -n "$n" ] && [ "$n" = "$(rg -c --pcre2 '"path":\s*"/info/version"' "$T/o")" ]; then echo "1t asyncapi $f VERSION-BUMP (the only 'breaking' change is /info/version, SZ10 — no channel or operation broke; the payload verdict is the unclassified count)"; else v asyncapi "$f" "$e" 1 'DiffBreakingChangeError'; fi
    CI=true ASYNCAPI_METRICS_CONFIG_PATH="$T/aa.json" "$AAPI" diff "$B/$f" "$f" -t unclassified -f json > "$T/o" 2>&1; echo "1t asyncapi $f payload changes unclassified: $(rg -c --pcre2 '"path":\s*"[^"]*/payload' "$T/o" || echo 0)"; done
  # 1d OpenAPI webhooks (SZ7): oasdiff reads a webhook body as a request, so a property the receivers read can be removed at WARN — fail on WARN and read the direction
  for f in $(cat "$T/s4"); do f=${f#./}; [ -f "$B/$f" ] || continue; if [ -z "$OAS" ]; then echo "1t oasdiff $f blocked (lane not installed: oasdiff@1.33.0 — brew or the GitHub release, never npm)"; continue; fi
    "$OAS" breaking "$B/$f" "$f" --fail-on WARN > "$T/o" 2>&1; v oasdiff "$f" $? 1 '^\d+ changes: '; done
  # 1e Avro (SZ2): the avsc resolver both ways — exit 0 compatible · 3 incompatible · 2 a schema that did not parse
  for f in $(rg --pcre2 '\.avsc$' "$T/s1"); do f=${f#./}; [ -f "$B/$f" ] || continue; if [ -z "$AVSC" ]; then echo "1t avsc $f blocked (lane not installed: avsc@5.7.9)"; continue; fi
    for d in "$B/$f $f backward" "$f $B/$f forward"; do set -- $d
      node -e 'const a=require("avsc"),fs=require("fs");let w,r;try{w=a.Type.forSchema(JSON.parse(fs.readFileSync(process.argv[1],"utf8")));r=a.Type.forSchema(JSON.parse(fs.readFileSync(process.argv[2],"utf8")))}catch(e){console.log("PARSE "+e.message);process.exit(2)}try{r.createResolver(w);process.exit(0)}catch(e){console.log("INCOMPATIBLE "+e.message);process.exit(3)}' "$1" "$2" > "$T/o" 2>&1; v avsc "$f($3)" $? 3 '^INCOMPATIBLE'; done; done
  # 4 semantic drift (read-only): changed lines in event schemas and in files that name a topic (5a's files) carrying a unit factor, a rounding call or a unit-suffixed field
  { cut -d: -f1 "$T/n5" | sed 's|^\./||'; cat "$T/heads"; } | sort -u | while read -r p; do [ -f "$B/$p" ] && [ -f "$p" ] && diff -U0 "$B/$p" "$p" | sed "s|^|$p:|"; done > "$T/d4"
  rg --no-heading --no-line-number --pcre2 '^[^:]+:[+-](?![+-]{2})[^\n]*(?:[*/]\s*(?:100|1000|1e3|1e6|60|3600|86400)\b|\bMath\.(?:round|floor|ceil)\(|\btoFixed\(|\b\w+(?:Ms|Millis|Sec|Secs|Seconds|Cents|Minor|Major|Units)\b\s*["\x27]?\s*[:=?(]|"(?:description|format|x-unit|unit)"\s*:|\b(?:nullable|optional)\b)' "$T/d4" | head -40
fi
```

Reading the output:
- **F1 is the version gate** and the lane selector: the schema tooling, the registry client, Pact, the store. **F1L** prints the locked version: when it printed one, that is the version, not the range's floor (a package locked at two versions: the importer's entry in `pnpm-lock.yaml`, or `<app>/node_modules/<pkg>` in `package-lock.json`, says which one the app gets). A stack beyond Node loads [`stacks.md`](stacks.md). **F2 is the subject list.** S1–S4 empty and no TS event type in 5c means §1 is `N/A (no schema files)` and the CONTRACT GATE is `N/A`; S6 empty with schema files present is a gate gap the audit prints, not a finding. S5 shows the registry mode: `BACKWARD` on a topic with long retention is §1's transitive row (SZ3).
- **`1t` lines are verdicts of a tool, never of this run.** `BREAKING` is a candidate whose part A (a reader exists) still needs the read; `PASS` with a `PARTIAL` line means the enum and pattern half is unread; `NOT-RUN` and `blocked` are listed in the coverage block as such.
- **2a is the input; 2b the strong list.** A 2a line wrapped as `X.parse(JSON.parse(…))` is excluded; a cast `as T` goes to code-quality (§ Boundaries). 3b prints every strict reader; part A decides inbound vs outbound (precedent 28). 5a–5c print lists for the read, never verdicts: a name another vendor owns (a third-party webhook topic) refutes at part A.
- **ES evidence gates §6–§9.** Zero files and zero tables → `N/A (no event store, aggregate or event table)`. 9d's count is printed for `coordination-scan` § 9, never graded here.

Three blind spots are structural, so work around them instead of trusting a quiet grep:
- **The consumer lives in another repository.** A schema with no reader here (5b "produced, never consumed") is the normal shape of a platform event: name the consuming services from the AsyncAPI `receive` operations, the registry's subjects or the README, and keep the §1 row Unconfirmed until one is read (precedent 5's shape).
- **The schema is generated.** A schema emitted from code (zod-to-json-schema, a protobuf from annotations) has no committed base; the diff of the source type is the evidence, and the generator run on base and head is the oracle.
- **Names built at run time** (`${domain}.${event}`) never reach 5a or 5b: read the producer wrapper once and list its names.

### Measured (2026-10-14)

| Tree | Result |
|---|---|
| Research samples (`contracts/`, `es/`: TS, Python, Java, C#, SQL; bad and good) | 0.3 s, 0 rg errors. **Every Node and SQL BAD line surfaces in its §**: `JSON.parse(message.value…)` and `json.loads(msg.value())` (2a), `default: assertNever(evt.type)` (3a), `.strict()`, `extra="forbid"`, `new ObjectMapper()`, `UnmappedMemberHandling.Disallow` (3b, 4 of 4; the Java file's two tolerance markers in 3c), `appendToStream(s, e)` and `{ streamState: ANY }` (6a, with `BigInt(rev)` and `NO_STREAM` quiet), the events table with no `UNIQUE(stream, version)` (7a; the one with it quiet), the increment and the separate checkpoint (8a), `ORDER BY created_at` (9d's count). `stacks.md` hits the Marten read-decide-append, `StreamState.Any` and `current_version=StreamState.ANY` with `FetchForWriting` quiet. The samples' topic pair sits in **one** file, so 5a — which counts files — stays quiet by design |
| Seeded tree (20 files, five schema formats with a `--contract-base` copy, plus the same tree as a two-commit git repo and a shallow clone of it) | Contract lane: buf **100** on a reused field number; json-schema-diff backward **BREAKING** on a required field added, forward PASS, plus PARTIAL (the schema has an enum); `asyncapi -t breaking` **PASS** with **4** unclassified payload changes for the same required field; oasdiff **BREAKING** only at `--fail-on WARN` (a webhook property removed); the Avro field added with a default PASS both ways (precedent 28); a deleted schema (1d); `amount: total / 100` in a producer (4). The git base gives the same verdicts; the shallow clone prints `BASE NOT-RUN`. Unparseable heads print **NOT-RUN** (json-schema-diff `VError`, asyncapi `ValidationError`) — never PASS. Greps: the near-twin `order.placed` / `orders.placed` and the produced-never-consumed / consumed-never-produced pair (5a, 5b), `OrderPlacedEvent` declared in two modules (5c), `json.loads(body)` in a Celery task (2b), `apply()` that mails (9a), a snapshot with no version (9b), a Prisma event model with no `@@unique` (the one with it quiet), an ORM entity, a SQL table cleared by a later unique index (7b), command → 303 and mutate → navigate (10a, 10b). The `.strict()` request DTO and the `streamState: ANY` audit stream print, for part A and precedent 29 to clear |
| `benchmarks/fixtures/*` (18 fixtures) | 0 rg errors; detector lines in 6. `quality-mix`: 2b the order-import consumer's `JSON.parse(message.body) as ImportedOrder` — its QM-TY-01 seed, code-quality `type-safety-scan` § 1's (routed). `slow-marketplace`: 2c two Redis pub/sub `JSON.parse(message) as PriceEvent` (the same owner's measured shape, routed); 5b one name. `brittle-suite`: 2b a webhook callback's `json.loads(body)` (HTTP → backend, part A) and 5b a queue registered with no worker in the fixture. `ci-defects`: 5b two worker queues whose producers name them through a constant. `mobile-defects`: 2a a WebView message (not a broker, part A). 12 fixtures print nothing. A first draft's 2b counted `JSON.parse(` itself as a validator and missed the QM-TY-01 file; fixed before shipping |
| Real repository (NestJS 11 + Fastify, MikroORM, BullMQ, zod 4.5.4 and class-validator 0.15.1 in the lockfile — F1L prints them since 2026-10-14 (19 lines; ajv is locked at 6 and 8 and `@grpc/proto-loader` at 0.7 and 0.8, so the importer's entry decides); read-only, about 11,100 files) | Re-run 2026-10-14 on the full tree, a git checkout with the shared contracts package, CI and the lockfile readable: 2.2 s, 0 rg errors. S1–S4 still **0** (the contracts package is zod HTTP schemas, not message schemas) and CI holds no contract gate. Changed: F1 adds the package's zod; 2a 4 parses (the fourth a browser CSP report body: HTTP, part A); 3c 1; **5c 1 → 5** — the report payload now also in the contracts package, plus four chat, support, team-chat and system message types declared in the contracts package (zod-inferred) and again as hand-written interfaces in the web app: HTTP payloads, so part A routes them — the hand-written web copies to code-quality `type-safety-scan` § 1, the server's shape to backend — never a broker row. The rest below is the earlier partial copy (not a git checkout) | 1.8 s, 0 rg errors. S1–S4 **0** → §1 `N/A (no schema files)`, CONTRACT GATE N/A, `BASE NOT-RUN`. 2a **3 → 0**: an outbound carrier-API response and a token payload (not messages, part A), and a Redis pub/sub session event parsed inside a `try` with a hand-written guard that returns `null` on a wrong shape (gate 4). 3a 0, 3b 0, 3c 2 zod `.passthrough()`. 5a **1 → refuted** (a third-party platform's webhook topic named in two connectors — the vendor owns the name); 5b 1 (a websocket event to browsers, part A); 5c 1 (an HTTP report payload declared in the API and the web app → backend). Queue names are shared constants — the GOOD shape — so 5a sees none. ES evidence 0 → §6–§9 N/A; §10 N/A. First-draft noise removed before shipping: 56 `additionalProperties: false` in LLM tool-parameter schemas (3b now reads that key only in schema documents and consumer files), `address`/`channel`/`subject` keys that are data fields (5a), a name split on `:` (`session:ended` read as `ended`), browser DOM event types (5c now counts services), and a SQL column-projection helper that opened §10 |

## The 3,000-hit path

1. **Start from F2, not from the greps.** A repo with schema files is judged by the tool lane first; one tool run per module or document replaces a thousand grep lines. A repo with none prints §1 `N/A` and moves to the consumers.
2. **Intersect** 2a–3b with the consumer files (`CONS`, 2c) and the process types that run them: a parse in a script, a seed or a test fixture is dismissed with one read. Name the directory in the coverage block.
3. **Group by root cause**: one shared deserializer, one base consumer, one envelope type, one projection base class is **one** finding with N sites. Schema findings group by the event, not by the field.
4. **Rank**: events another service or a stored stream depends on first (orders, payments, stock, identity); then events with a replay path; then internal notifications.
5. **Read the top 30 groups**; sample 10 sites per group, and the rest inherit the verdict with the group's id.
6. **Run the bulk oracle once**: V324's replay-old-events corpus over every consumer of the top event; V325 over the top aggregate.
7. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production path. One replica does not make a contract or store row latent (precedent 32).

| § | Classes | Default severity |
|---|---|---|
| 1 | EC-1 breaking schema change (diff lane) | high; BLOCKER when a removed or retyped field is read by a consumer that deploys apart from the producer, or a deleted schema still has subscribers; medium for `BACKWARD` (latest only) on a long-retention topic |
| 2 | EC-2 inbound event not checked against its contract | medium; high when a malformed event crash-loops a partition or persists garbage another service reads |
| 3 | EC-3 intolerant reader | high when the producer deploys independently; medium otherwise; not a row for the service's own internal union or an outbound schema (precedent 28) |
| 4 | EC-4 semantic change with the same type (read-only) | high; never above Unconfirmed without V324's replay corpus |
| 5 | EC-5 name drift; producer-only types; no version or upcaster | medium for a near-twin live on both sides (split brain); low for a duplicated literal; high for a stored event shape changed with no upcaster |
| 6 | ES-1 append without expected version after a read-decide | high; money, stock and credit invariants → security (§ Boundaries) |
| 7 | ES-2 custom event table without UNIQUE(stream, version) | high |
| 8 | ES-3 projection not idempotent; checkpoint outside the projection's transaction | high when someone acts on the figure; medium for a display-only read model |
| 9 | ES-5 side effects in `apply`; snapshot without version | high for an external effect on replay; medium for a snapshot |
| 10 | CN-2 eventual consistency assumed in a UI flow | medium |

### 1. Breaking schema change (EC-1)

```
BAD:   message OrderPlaced { string order_id = 1; string coupon = 2; }   // field 2 was int64 amount_minor: tag reused (buf 100)
       "required": ["orderId", "amountMinor", "currency"]                  // a required field added: every stored event fails the new reader
       {"type":"enum","name":"Status","symbols":["PLACED","PAID","REFUNDED"]}   // old readers have no enum default (SZ2)
       compatibility: BACKWARD on a topic with infinite retention          // latest-only check (SZ3)
       a webhook body losing a property receivers read (oasdiff WARN) · a schema file deleted while consumers subscribe
GOOD:  a new field number and `reserved 2;` · a new optional field with a default · an enum default · BACKWARD_TRANSITIVE / FULL_TRANSITIVE
       a new versioned event type for a breaking shape, both published until every reader moved · the compatibility tool in CI
```
**Read the code:** Which `1t` line, at which exit, against which base? Who reads the event (in this repo, in another, in a replay), and which direction must hold — is the registry mode transitive (S5)? Did the tool parse both sides (a `NOT-RUN` is never a pass)? For AsyncAPI, compare the payloads (`unclassified`) as JSON Schema or read them; for JSON Schema with `PARTIAL`, read the enum and pattern diff by hand. For a TS-only type, would the old consumer still compile against the new one? Is the change fronted by a new event type or an upcaster (§5)? **Finding when** a reader that deploys apart from the writer cannot read an event it will receive or has stored. **Proof (V323):** the format tool exits breaking on base → head before the fix and 0 after (tier T); a fix that adds `--no-error` or sets the registry to `NONE` fails the variant. Writing a provider verification is testing `contract-test`.

### 2. Inbound event not checked against its contract (EC-2)

```
BAD:   const evt = JSON.parse(message.value.toString()); await apply(evt.amount)      // no schema on a topic whose schema is in S3
       evt = json.loads(body); Order.objects.create(**evt)                            // a Celery task writing whatever arrived
       a consumer of an Avro topic reading raw bytes with JSON.parse instead of the registry deserializer
GOOD:  const evt = OrderPlaced.parse(JSON.parse(raw)) · Order.model_validate_json(body) · the registry's AvroDeserializer
       — and a malformed event parked (DLQ, a failed set) instead of thrown back for redelivery
```
**Read the code:** Is this a broker message from another process (part A — an HTTP body, a WebView message, a cache entry is not)? Is the value cast (`as T`) — then code-quality `type-safety-scan` § 1 owns it — or used raw? Does the topic have a schema (S1–S3) that this consumer bypasses? Is there a guard further down (a `typeof` check, a try that returns `null`)? What does a malformed event do: park, skip with a log, or throw and redeliver (→ `messaging-scan` § 3)? **Finding when** a malformed or wrong-version event reaches an effect or a crash loop. **Proof (V324):** feed the malformed fixture to the real handler: parked, not a crash loop, no write.

### 3. Intolerant reader (EC-3)

```
BAD:   switch (evt.type) { …; default: assertNever(evt.type) }   // in a consumer of another team's events
       z.object({...}).strict() / extra="forbid" / UnmappedMemberHandling.Disallow on an INBOUND event
       private final ObjectMapper mapper = new ObjectMapper();     // FAIL_ON_UNKNOWN_PROPERTIES on (SZ6)
       an Avro reader enum with no "default" (3d) · additionalProperties: false on a consumer-side schema
GOOD:  default: log and ack (or park) the unknown type · zod's default strip or .passthrough() · the Spring Boot mapper
       mapper.configure(FAIL_ON_UNKNOWN_PROPERTIES, false) · READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE · an Avro enum default
```
**Read the code:** Is the strict schema applied to what this service **receives** from another producer, or to what it sends or owns (precedent 28)? Is the `assertNever` over the service's own compile-time union, or over a type read from the network? Is the mapper the framework's configured bean or a hand-made one? Does a tolerance marker (3c) configure the same mapper? **Finding when** a producer adding a field, an enum symbol or an event type makes this consumer throw. **Proof (V324):** the extra-field and unknown-type fixtures are acked or parked by policy without a throw.

### 4. Semantic change with the same type (EC-4)

```
BAD:   - JSON.stringify({ id, amount: total })   + JSON.stringify({ id, amount: total / 100 })   // minor → major units, same field, same type
       durationS now carrying milliseconds · a nullable field whose null now means "unknown" instead of "none"
GOOD:  a new field (amountMinor) or a new event version, the old one kept until readers moved · units in the field name
```
**Read the code:** Line 4 prints changed lines with a scale factor, a rounding call or a unit-suffixed field, in schemas and in files that name a topic: did the meaning of a field another reader uses change? Money as a float in the payload is backend `wire-format-scan` § 5's — cite it. Every compatibility tool passes this class (the seeded `amount` change passed buf, json-schema-diff and avsc). **Finding when** an existing reader computes a wrong value from an event it reads correctly. **Proof (V324, replay corpus):** deserialise captured events of each version through the current consumer: same meaning, 0 failures.

### 5. Name drift, producer-only types, no version or upcaster (EC-5)

```
BAD:   topic: 'orders.placed' in three files, 'order.placed' in one        // a rename splits producers from consumers
       interface OrderPlacedEvent { … } re-declared in billing with a different field
       a stored event class changed in the diff, no schemaVersion in the envelope, no upcaster registered
       an envelope with no producer-set event id, so every consumer reserves on a broker id that changes on redelivery
GOOD:  one constant, a generated client or the AsyncAPI document · one shared schema package · schemaVersion + an upcaster per old version
       a producer-set event id in the envelope (CloudEvents `id`, `eventId`) minted once per fact
```
**Read the code:** For 5a, is each literal the same channel, and is one side a typo or a stale rename? Is the name owned by another vendor (part A)? For 5b, where is the other side — another repo, a CDC topic, a test only? For 5c, do the declarations' fields differ, and is the type an event at all? A contracts-package type re-declared by hand in a client app is HTTP type drift → code-quality `type-safety-scan` § 1 (§ Boundaries), not only backend. For 5d, has the envelope already changed shape (the §1 diff, a branch on `'field' in evt`), and is there an upcaster for each stored version? Does the envelope carry an event id the producer sets once — the contract half of `messaging-scan` § 2's unstable reserve id (rows ID1–ID9)? **Finding when** a producer and a consumer that must meet do not, or a stored event can no longer be read. **Proof (V324):** the replay-old-events corpus through the current consumer; for a rename, publish on the producer's name and assert the consumer receives it.

### 6. Append without expected version after a read-decide (ES-1)

```
BAD:   const s = await load(id); if (s.stock < qty) throw …; await client.appendToStream(`order-${id}`, evts)   // default ANY (EV1)
       await client.appendToStream(stream, evts, { streamState: ANY })   after a decision on loaded state
GOOD:  await client.appendToStream(stream, evts, { streamState: revisionLoaded })   // WrongExpectedVersionError → reload, re-decide
       Marten FetchForWriting<T>(id) (EV3; stacks.md) · the store's optimistic API with the version read
```
**Read the code:** Did the code read the stream and branch on its state before this append? Then which revision did it read, and is it passed? Is the stream append-only facts with no invariant — audit, telemetry (precedent 29)? Is a lock or a single writer per stream the control instead (name it)? A money, stock or credit invariant goes to security (§ Boundaries). **Finding when** two deciders working from the same version can both append. **Proof (V325):** two deciders released by a barrier → one append succeeds, the other gets `WrongExpectedVersion`.

### 7. Custom event table without UNIQUE(stream, version) (ES-2)

```
BAD:   CREATE TABLE order_events (id bigserial primary key, stream_id uuid not null, version int not null, data jsonb)
       model OrderEvent { id Int @id; streamId String; version Int }     // no @@unique([streamId, version])
GOOD:  UNIQUE (stream_id, version) or PRIMARY KEY (stream_id, version) · @@unique([streamId, version]) · @Unique({ properties: ['streamId', 'version'] })
```
**Read the code:** Does a later migration add the unique index (7b)? Is the table written by a library store that owns the constraint (Marten, the Axon JPA store, the Python `eventsourcing` library — precedent 30)? Is it an event *log* (webhook deliveries, an outbox) rather than a stream store? Is the version computed from a read (`max(version) + 1`)? **Finding when** two concurrent appends of version n+1 both commit. **Proof (V325, SQL layer):** two transactions insert `(stream, n+1)` → the second fails with a unique violation after the fix.

### 8. Projection not idempotent; checkpoint outside its transaction (ES-3)

```
BAD:   await db.query('UPDATE stats SET orders = orders + 1'); await checkpoints.save('stats', e.position)   // two commits
       the checkpoint saved before the projection write · INSERT INTO order_view … with no conflict guard
GOOD:  the read-model write and the checkpoint in one transaction · an upsert keyed by event id or position
       (ON CONFLICT DO NOTHING, WHERE last_position < :pos) · a rebuild-and-swap projection
```
**Read the code:** Are the projection write and the checkpoint in one transaction on one store? Is the write idempotent per event (keyed by event id, position-guarded, SET not INCREMENT)? Does a redelivery or a restart from the last checkpoint re-apply the event? Is it a full rebuild-and-swap (cleared for the rebuild path)? A projection fed by a broker with no reserve at all is `messaging-scan` § 2's. **Finding when** a redelivery or a crash between the two writes changes the read model. **Proof (V326):** inject a throw between the write and the checkpoint, restart → the read model unchanged; redeliver one event → unchanged.

### 9. Side effects in `apply`; snapshot without version (ES-5)

```
BAD:   apply(e: OrderShipped) { this.status = 'shipped'; this.mailer.sendShipped(this.id) }   // replay mails every customer again
       a snapshot row { id, state } with no schema version, loaded and returned without applying the tail
GOOD:  apply mutates state only; a subscriber with its own reserve sends the mail · a snapshot carrying schemaVersion and streamVersion,
       discarded on a mismatch, then the events after streamVersion applied
```
**Read the code:** Does the method run during rehydration (`loadFromHistory`, an `evolve` fold, an `@EventSourcingHandler`) or only on the command path? Is the I/O a pure in-memory call? Does the snapshot loader compare the version it was written with against the aggregate's current shape, and replay the tail? A daemon running on every replica is performance § 20's (9c); timestamp ordering is `coordination-scan` § 9's (9d). **Finding when** a replay or a rebuild repeats an external effect, or a snapshot of an old shape is used as current state. **Proof (V326):** replay the full stream through the aggregate with the side-effect port mocked to count → 0 sends; load a v1 snapshot into the v2 aggregate → discarded or upcast.

### 10. Eventual consistency assumed in a UI flow (CN-2)

```
BAD:   await this.commandBus.execute(new PlaceOrderCommand(dto)); return res.redirect(303, '/orders')   // the list reads an async projection
       await createOrder.mutateAsync(v); navigate('/orders')   // the loader reads the lagging read model
GOOD:  return the new id and position; the next read waits for it (or reads the write side) · an optimistic UI entry reconciled later
```
**Read the code:** What does the redirect target read — the write model, or a read model fed asynchronously? Does the command return a position or version, and does the read wait on it (10c)? Is the lag observable (a list missing the new row, a stale balance)? A replica lag is database's. **Finding when** the next screen reads a projection that has not caught up and shows the old state as fact. **Proof (V327):** write → redirect → read with the projection paused: the new value appears, or the read waits on the returned position.

## Output

```
event-contract-scan coverage — scope=diff (base: --contract-base=.refract-fixture/contract-base)  stacks=@kurrent/kurrentdb-client ^1.3 range, zod ^4.1, kafkajs ^2.2
Contract inventory: S1 3 (proto 1, avsc 2) · S2 1 · S3 1 · S4 1 · registry BACKWARD (deploy/registry.env:4) · CONTRACT GATE absent
Tools: buf 1.73.0 ran · json-schema-diff 1.0.0 ran (PARTIAL: enum) · asyncapi 6.2.1 ran (4 payload changes unclassified) · oasdiff blocked · avsc ran

Findings: 2 · Unconfirmed: 2 · Hardening: 0

1. schemas/proto/orders/v1/order.proto:6 · base .refract-fixture/contract-base/schemas/proto/orders/v1/order.proto    [report-with-fix]   BLOCKER
   §1 EC-1 — part A: OrderPlaced is consumed by src/consumers/orders.consumer.ts:2 and the billing service (AsyncAPI receive).
   Part B: field 2 reused as `string coupon` (was `int64 amount_minor`); buf breaking exit 100 (SZ1). Fix: `coupon = 4;` and `reserved 2;`.
2. src/es/order.service.ts:41    [report-with-fix]   high
   §6 ES-1 — part A: the stock check reads the stream at :37. Part B: appendToStream with no streamState (default ANY, EV1).
   V325: two deciders behind a barrier both appended (failed); after passing the loaded revision, one WrongExpectedVersion.
3. schemas/asyncapi/orders.yaml:14    [report-flagged]   high
   §1 EC-1 — `currency` added to `required`; asyncapi -t breaking PASS but the change is unclassified; json-schema-diff on the payload
   (backward) BREAKING. Settling test: V323 with the payload extracted, and the reader list from the billing repo.
4. src/orders/orders.service.ts:3    [report-flagged]   high
   §4 EC-4 — `amount: total` → `amount: total / 100`, same field, same type; every tool passed. Settling test: V324 replay corpus.

Verification: 19 candidates → 2 findings · 2 unconfirmed · 9 refuted · 4 routed · 2 live, unreviewed (self-verified)

Class coverage:
  §1  breaking schema change     checked (5 tool runs → 1 finding, 1 unconfirmed; oasdiff blocked (lane not installed: oasdiff@1.33.0))
  §2  unvalidated payload        checked (3 → 1 refuted) · → code-quality type-safety-scan §1 (2)
  §3  intolerant reader          checked (4 → 1 refuted: outbound DTO, precedent 28) · Live, unreviewed (1 group / 2 hits)
  §4  semantic change            checked (4 changed lines → 1 unconfirmed)
  §5  names and versions         checked (5a 1, 5b 2, 5c 1 → 0)
  §6  append without version     checked (2 → 1 finding, 1 refuted: audit stream, precedent 29) · → security logic-race-scan §5 (0)
  §7  stream uniqueness          checked (3 → 1 cleared by a later index, 2 refuted: library store, precedent 30)
  §8  projection idempotency     checked (1 → 0: rebuild-and-swap)
  §9  apply / snapshot           checked (0) · 9c → performance request-path-scan §20 (0) · 9d → coordination-scan §9 (1)
  §10 UI read after write        N/A (no projection or read-model class and no event store)
```

`[report-with-fix]`: the tool or the oracle failed on the unfixed code, and the fix is local to the project's schema, envelope, store call or projection. `[report-flagged]`: one link is unproven (a tool `blocked` or `NOT-RUN`, a reader in another repo, no replay corpus); the row names it and the settling test. The coverage block lists **all ten** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `NOT-RUN (no base)`, `blocked (<tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/ds-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/distributed.md`](../../../../snippets/precedents/distributed.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 28** additive, optional changes are compatible (an Avro field with a default, a new protobuf field number, a JSON field for tolerant readers); a strict reader on an **outbound** DTO is not an intolerant reader. **§ 29** `streamState: ANY` is correct for append-only facts with no invariant. **§ 30** library event stores own the uniqueness constraint.
- **§ 13** `WHERE id > $last` over one serial writer (the cursor itself is `dual-write-scan` § 6's). **§ 31** timestamps are fine for display and audit. **§ 32** one replica does not make a store row latent. **§ 33** a mocked store or bus proves nothing about concurrency. **§ 34** a comment saying "backward compatible", "consumers ignore unknown fields" or "the registry checks it" is a pointer: read the registry mode, the mapper and the consumer.

Shapes this skill must not report: a `.strict()` request DTO or an LLM tool schema; `assertNever` over the service's own union; a topic a third-party vendor names; a schema change no reader receives; a tool `PASS` reported as proof while its `PARTIAL` line is unread; `ORDER BY created_at, id` within one stream.

## When to run

- On any diff that touches a schema file, an event type, an envelope, a producer mapping, an event-store append, an event table migration or a projection — `/ds-audit`'s "a schema file, an event type, an event-store append, a projection" signal. Pass `--contract-base=<dir>` when the repo has no base branch (a fixture, an export, a vendored copy).
- On every whole-repo `/ds-audit`, reporting all ten §s; before changing a registry compatibility mode, renaming a topic, adding a field to a long-retention event, or introducing snapshots.
- After `/add-event-handler`: its Phase 6 runs V324 from the same oracle file.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A, part B, the base, the tool's exit and first line, the `broker-semantics.md` row and the version lines — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/distributed.md`. Under `/ds-audit` that is its verification phase; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Never print PASS for a tool that did not parse both sides.** A non-zero exit without the tool's breaking marker, a `VError` or `ValidationError`, a load failure, a misaligned buf root or a missing base is `NOT-RUN` with the first line; with no base at all §1 and §4 are `NOT-RUN (no base)`.
- **Never run the AsyncAPI CLI with its metrics on** (`CI=true` and `ASYNCAPI_METRICS_CONFIG_PATH`, as in the block), never install `oasdiff` from npm, and never call a schema registry, broker or event store outside a scratch container — `test-compatibility` against a shared registry registers nothing, but its credentials are the user's to give.
- **Halt on any finding missing its anchors:** the schema or append `file:line`, the base, the reader or decider, the row, the fix in the project's own primitive.
- **No fix may make the check pass instead of the contract:** `--no-error`, a registry set to `NONE`, `.passthrough()` on a schema whose strictness was a decision, or a version gate removed. Changing a registry compatibility mode is a STOP for `/ds-fix`.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "contracts look compatible"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/ds-audit` dispatches this skill and folds its coverage block into the Contracts and Event sourcing ledger rows and the CONTRACT GATE; `/ds-fix` closes findings with the failing-first tool run or oracle, the fix in the project's schema, envelope, store call or projection, a re-run of this detector and the sibling sweep.
- `messaging-scan` (poison, consumer reserve), `dual-write-scan` (the outbox, gap-blind cursors), `coordination-scan` (timestamp ordering) and `workflow-scan` (history versioning) are the neighbours named in § Boundaries; `@event-sourcing-architect` judges these rows.
- code-quality `type-safety-scan` § 1, backend `http-contract-scan` § 10, `job-lifecycle-scan` § 3, `wire-format-scan` § 5 and `validation-boundary-scan` § 6, § 8, testing `contract-test`, security `logic-race-scan` § 5, performance `request-path-scan` § 20 and database `connection-config-scan` § 8, when those packs are installed.

## Sources

Format and store facts are rows of `broker-semantics.md` (SZ1–SZ13, EV1–EV3; read 2026-10-14 from buf.build *Breaking rules*, the Avro 1.12.0 specification, Confluent Platform 8.3 *Schema evolution*, the AsyncAPI CLI `docs/usage.md`, the json-schema-diff README, the oasdiff README, library docs for Jackson, System.Text.Json, pydantic and zod, the KurrentDB Node client source and martendb.io). Pact's message-pact API and `can-i-deploy` are the distributed-systems research notes B § 5.0 (pact-js 17.1.4, 2026-10-14). The tool-lane exit codes and traps were measured in this build on 2026-10-14 against buf 1.73.0, json-schema-diff 1.0.0 (and its `KEYWORDS.md`), @asyncapi/cli 6.2.1 (and its metrics code path), oasdiff 1.33.0 (the checksum-verified GitHub release) and avsc 5.7.9, on scratch schemas only. Grep literals are the research notes B § 5.1 (C1–C8) and § 6.1 (E1–E9), tested on the research samples, re-measured here with the fixtures and a read-only real repository. Paraphrased; no text reproduced beyond identifiers.
