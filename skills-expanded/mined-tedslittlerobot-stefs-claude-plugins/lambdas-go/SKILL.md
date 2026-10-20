---
name: lambdas-go
description: Go AWS Lambda conventions — directory naming by trigger (api-<method>-, api-socket-, alb-<method>-, url-, sqs-, sns-, mq-, dynamo-, kinesis-, kafka-, docdb-, s3-, bus-, pipe-, schedule-, cognito-, logs-, alarm-, email-, iot-, aurora-, lambda-, secrets-, ninja-) for API Gateway, WebSocket, ALB, function URL, queue, topic, stream, schedule/cron and other event-source triggers, one Go module per Lambda compiled to a bootstrap binary, the main.go/handler.go root package with everything else in sub-packages, Go package naming, the structured log line format, file organisation, build commands and testing. Use when writing, editing, reviewing or testing Go Lambda code, creating a new Lambda directory, or deciding which package something belongs in. Prototype and proof-of-concept projects only — not for production.
---

# Go Lambda Conventions

> **Prototypes and proofs of concept only — not for production.** This skill is part of the
> `prototype-conventions` plugin, whose rules are chosen for building a prototype or
> proof-of-concept project quickly, not for what a production system needs.
>
> Before applying it, check that this project is a prototype or proof of concept — its README,
> `CLAUDE.md` or `conventions/` files will usually say. If they do, carry on without raising it
> again. If nothing says either way, ask the user before applying any of these rules. If the project
> is **not** a prototype, **do not apply these rules**: say so, and offer to disable the plugin for
> this project by adding it to the project's `.claude/settings.json`, merged into whatever is
> already there:
>
> ```json
> {
>   "enabledPlugins": {
>     "prototype-conventions@stefs-plugins": false
>   }
> }
> ```
>
> Make that change only once the user agrees. Project settings override user settings, so this
> switches the plugin off for this repository alone, and committing the file does so for everyone
> who works on it.

Applies to every Go Lambda function in the repository. A Lambda written in another language is a
**registered exception** recorded in the project's own conventions — see the `lambdas-node` skill
for the Node.js case.

## Language & Runtime

- **Go**, version pinned via [`goenv`](https://github.com/go-nv/goenv) —
  `goenv install <version> && goenv local <version>`
- Lambda runtime **`provided.al2023`** (Amazon Linux 2023 custom runtime for Go)
- Each Lambda compiles to a standalone binary named **`bootstrap`**
- Each Lambda directory needs a `.gitignore` ignoring the `build/` directory, the
  `bootstrap`/`bootstrap.zip` artefacts, **and a file named after the directory itself** — a bare
  `go build` with no `-o` drops a host binary there beside the source, and without that last line it
  is committable. This is not hypothetical: five had been committed before the rule existed

## Directory Naming

Each Lambda lives in its own directory under the service's `lambdas/` folder, named so its **trigger
is visible from the directory name alone**:

| Trigger | Name | Example |
| --- | --- | --- |
| API Gateway HTTP route | `api-<http-method>-<purpose>` | `api-get-profile` for `GET /api/me/profile` |
| API Gateway WebSocket route | `api-socket-<route>` | `api-socket-connect` for `$connect`, `api-socket-send-message` |
| Application Load Balancer target | `alb-<http-method>-<purpose>` | `alb-post-webhook` |
| Lambda function URL | `url-<purpose>` | `url-stripe-webhook` |
| SQS queue | `sqs-<sqs-queue-name>` | `sqs-new-users` for the `new-users` queue |
| SNS topic | `sns-<what-the-lambda-does>` | `sns-notify-admins` |
| Amazon MQ broker (ActiveMQ / RabbitMQ) | `mq-<what-the-lambda-does>` | `mq-import-orders` |
| DynamoDB stream | `dynamo-<what-the-lambda-does>` | `dynamo-index-search` |
| Kinesis data stream | `kinesis-<what-the-lambda-does>` | `kinesis-aggregate-clicks` |
| Amazon MSK or self-managed Kafka | `kafka-<what-the-lambda-does>` | `kafka-sync-inventory` |
| DocumentDB change stream | `docdb-<what-the-lambda-does>` | `docdb-audit-changes` |
| S3 lifecycle event | `s3-<what-it-handles>` | `s3-upload-scan` for `ObjectCreated:*` on the uploads bucket |
| EventBridge bus event | `bus-<what-the-lambda-does>` | `bus-send-welcome-email`, subscribed to `user.registered` |
| EventBridge Pipe (enrichment or target) | `pipe-<what-the-lambda-does>` | `pipe-enrich-orders` |
| Schedule (EventBridge scheduled rule or EventBridge Scheduler) | `schedule-<frequency>-<purpose>` | `schedule-nightly-clear-caches` |
| Cognito User Pool trigger (a lifecycle hook or event) | `cognito-<what-it-handles>` | `cognito-custom-email-sender`, `cognito-pre-sign-up` |
| CloudWatch Logs subscription filter | `logs-<what-the-lambda-does>` | `logs-forward-errors` |
| CloudWatch alarm action | `alarm-<what-the-lambda-does>` | `alarm-page-on-call` |
| SES receipt rule (inbound email) | `email-<what-the-lambda-does>` | `email-parse-replies` |
| IoT Core rule | `iot-<what-the-lambda-does>` | `iot-store-telemetry` |
| Aurora MySQL, from SQL (`lambda_sync` / `lambda_async`) | `aurora-<what-the-lambda-does>` | `aurora-notify-on-signup` |
| Lambda destination (on success or failure of another function) | `lambda-<what-the-lambda-does>` | `lambda-report-failed-import` |
| Secrets Manager rotation | `secrets-<what-it-rotates>` | `secrets-aurora-credentials` |
| Manual invocation only (`aws lambda invoke`, no route or event source) | `ninja-<purpose>` | `ninja-add-user` |
| Anything else | the function's purpose | `register-user`, `validate-token` |

- An API route **must** live under an `/api` prefix — see the `infrastructure` skill's
  frontend-hosting reference for why (one CloudFront path pattern forward-matches every route)
- An **API Gateway WebSocket route has no HTTP method, so `socket` takes the method's place** —
  `api-socket-<route>`, with the route key's leading `$` dropped (`$connect` → `api-socket-connect`,
  `$default` → `api-socket-default`). The Lambdas behind one API then sort together whichever
  protocol they speak, and a WebSocket handler is still never mistaken for a request/response one
- An **`alb-` Lambda follows the `api-` shape**, method then purpose, because it is the other HTTP
  front door. The prefix says which door it is: an ALB hands the handler a different event and
  expects a different response from API Gateway's, so the two are not interchangeable
- A **`url-` Lambda has no method in its name.** A function URL is a single endpoint that answers
  every method, so there is nothing to put there; any routing on method happens inside the handler
- **A `schedule-` Lambda's name says how often it runs, then what it does** —
  `schedule-nightly-clear-caches`, `schedule-hourly-sync-users`, `schedule-weekly-send-digest`. The
  question asked of a scheduled job is *when does it run?*, which neither its purpose alone nor
  `bus-` answers — so a scheduled rule takes `schedule-` even though it technically lives on the
  default event bus. Write the frequency as a word at the granularity least likely to change
  (`nightly`, `hourly`), not as an exact interval: the cron or rate expression, with its timezone,
  belongs in `schema.md` and the README invocation section, and a changed interval should not mean a
  renamed Lambda
- For a **FIFO** queue, drop the `.fifo`/`fifo` suffix when forming the Lambda name: a
  `new-users.fifo` queue still yields `sqs-new-users`
- A **`bus-` Lambda is named after what it does, not after the event it subscribes to.** The two
  often overlap — `bus-send-welcome-email` does overlap with `user.registered` — but the event is
  not the name. An event bus is fan-out: the whole point is that several Lambdas subscribe to the
  same event, and naming them after the event means the second subscriber has no name left. It also
  makes the interesting question — *what happens when a user registers?* — unanswerable from a
  directory listing, which is exactly what trigger-based naming is for
- The event a `bus-` Lambda subscribes to belongs in its `schema.md` and README invocation section,
  where the full event pattern can be written out; the directory name carries the behaviour
- An **`s3-` Lambda's name after the prefix is terse, and says whatever makes it clearest among its
  siblings** — the lifecycle event alone (`s3-object-created`) when one Lambda handles one event on
  one bucket and nothing else could be meant, or a short summary of what it does (`s3-upload-scan`,
  `s3-thumbnail`) when the bucket, the prefix filter or a sibling Lambda would otherwise be
  ambiguous. Prefer the summary as soon as there is a second `s3-` Lambda in the service: two
  directories named for their events answer *which bucket?* for neither
- The bucket, the event pattern and any key prefix filter belong in the Lambda's `schema.md` and
  README invocation section, where they can be written out in full — the directory name carries the
  trigger kind and the behaviour, the same split as `bus-`
- **Every other event source is named the way `bus-` is: the prefix for the trigger kind, then what
  the Lambda does** — `sns-`, `mq-`, `dynamo-`, `kinesis-`, `kafka-`, `docdb-`, `pipe-`, `logs-`,
  `alarm-`, `email-`, `iot-`, `aurora-` and `lambda-`. Topics, streams and change feeds are fan-out
  as much as a bus is, so a name taken from the topic, table, stream or log group leaves the second
  consumer with no name. The specific source — the topic, table, stream, broker, log group, alarm,
  receipt rule, IoT rule, the stored procedure or trigger that calls out, or the function and
  condition for a destination — goes in `schema.md` and the README invocation section. `sqs-` is the
  exception, and names the queue, because a queue's messages each go to one consumer: the queue
  identifies the Lambda
- An **`aurora-` Lambda called with `lambda_sync` runs inside the SQL statement that invokes it**,
  so a failure or a slow response surfaces as a failed or slow query — the same reason
  `cognito-` is worth seeing at a glance
- A **`secrets-` Lambda is named for the secret it rotates**, without a `rotate-`: rotation is the
  only thing Secrets Manager invokes a Lambda for, so the word would distinguish nothing — the same
  reasoning that removed `handler-` from `sqs-` names below
- **Every Lambda attached to a Cognito User Pool trigger takes the `cognito-` prefix** — pre
  sign-up, post confirmation, pre token generation, custom message, custom email or SMS sender, the
  custom auth challenge triggers, and any other hook in the pool's `LambdaConfig`. Cognito invokes
  these synchronously, inside a user's sign-up or sign-in, so a failure in one blocks that user
  rather than landing on a retry queue; that is worth knowing from the directory listing alone.
  After the prefix, name the trigger it handles (`cognito-custom-email-sender`) — a pool accepts
  one Lambda per trigger, so the trigger name is unambiguous — or a terse summary of the work when
  one Lambda is wired to several triggers
- **Corrected:** Cognito triggers used to fall under "anything else" and be named for their
  purpose alone (`custom-email-sender`), which left the one trigger kind whose failures reach users
  directly as the only kind not visible from its name. Existing unprefixed directories are not
  wrong, and renaming one is a separate decision with Terraform and log-prefix consequences; new
  ones take the `cognito-` prefix
- The `ninja-` prefix exists so an operational/admin utility is identifiable at a glance and never
  mistaken for a user-facing endpoint
- **Sources with no prefix yet take the "anything else" row** — Step Functions tasks, AppSync
  resolvers, CloudFormation custom resources, Lambda@Edge, Firehose transformation, S3 Object
  Lambda, Config rules, CodePipeline actions and the like. Do not invent a prefix for one in a
  project; add it here, so every project names the same trigger the same way
- **Corrected:** this table used to cover only API Gateway HTTP routes, SQS, S3, the event bus,
  Cognito and manual invocation, with every other source falling under "anything else". That left
  most event sources — schedules above all — invisible from the directory listing, which is the
  thing the table exists to prevent. Existing directories named under the old table are not wrong;
  new ones take the prefixes above
- **Corrected:** this rule used to read `sqs-handler-<sqs-queue-name>`. The `handler-` was
  superfluous — every Lambda in the table is a handler, so the word distinguished nothing and only
  pushed the part that *does* carry information, the queue name, further from the front of the
  directory listing. Existing `sqs-handler-` directories are not wrong, and renaming one is a
  separate decision with Terraform and log-prefix consequences; new ones take the short form

## Module & Package Layout

Each Lambda is **its own Go module**, with one `go.mod`/`go.sum` at the Lambda directory's root. The
only code it may import from outside its own directory is an explicitly registered shared library.

**The root `package main` holds only two source files — `main.go` and `handler.go` — plus their
co-located tests.** Everything else lives in a sub-package.

- **`main.go`** is wiring and nothing else: resolve environment variables, construct dependencies,
  instantiate the `Handler`, call `lambda.Start`. No business logic, no validation, no queries
- **`handler.go`** holds a `HandlerInterface` and the `Handler` that satisfies it. `handle`
  sequences sub-packages and maps their errors onto a response — **high-level control flow only**

Read **`reference/module-layout.md`** for the full tree, the `handler.go` contract, the sub-package
table and Go package-naming rules before creating a new Lambda or adding a package.

## Logging

**Log frequently** — at function entry, before and after significant operations (AWS calls, DB
queries, external service calls), and at decision points. Under-logging a Lambda is expensive
because a production trace is often all you get.

Every log line includes the **module**, **file**, **function** and a **unique step identifier**
within that function:

```go
log.Printf("[module:file:function:step] message key=value ...")
log.Printf("[admin-create-user:handler.go:Handle:cognito-create] creating user email=%s", maskedEmail)
log.Printf("[admin-create-user:main.go:main:secrets-retrieved] successfully retrieved DB credentials")
```

Include relevant variables for inspection — request IDs, masked email addresses, resource
identifiers, error messages.

**Never log secrets, passwords, tokens, or unmasked PII.**

## File Organisation

Within **every** package — the root `package main` and each sub-package alike:

- Plain structs with **no** methods group into **`models.go`**
- A struct **with** methods gets its own **`<name>.go`** (a `Study` struct with methods → `study.go`)
- Interfaces group into **`interfaces.go`**
- **Test files always sit beside the file they test** — `input/input_test.go` tests `input/input.go`

The root `package main` is the exception to the first three: it holds only `main.go` and
`handler.go`, so any struct, interface or helper it would otherwise need **belongs in a
sub-package.**

## Frameworks & Libraries

- [`github.com/aws/aws-lambda-go`](https://github.com/aws/aws-lambda-go) — event types, handler
  interface
- [`github.com/aws/aws-sdk-go-v2`](https://github.com/aws/aws-sdk-go-v2) — AWS SDK v2
- [`github.com/DATA-DOG/go-sqlmock`](https://github.com/DATA-DOG/go-sqlmock) — repository tests

## Required Documentation

Every Lambda directory needs **both**:

- **`schema.md`** — the input contract: summary, TypeScript-syntax schema, worked JSON examples. See
  `reference/schema-md.md` for the exact template
- **`README.md`** — the narrative overview, in exactly four sections (Invocation, Purpose,
  Interface, Implementation, the last with a rendered flow diagram). See the `documentation` skill's
  READMEs reference

## Commands

Run from inside a Lambda's own directory:

```bash
GOOS=linux GOARCH=amd64 go build -o build/bootstrap .   # build (deployment artifact)
go test ./...                                            # test
go test -run TestName ./...                              # single test
go test -cover ./...                                     # coverage
go fmt ./...
golangci-lint run
go mod tidy
```

All build output goes into a **`build/` directory** within the Lambda's directory; Terraform zips
`build/bootstrap` for deployment.

**A shared library is never built on its own** — it has no `main` and is compiled into each
consuming Lambda's binary. Only the test, vet, format and tidy commands apply to it.

## References

- **`reference/module-layout.md`** — the module tree, `main.go`/`handler.go` contracts, package
  naming, the sub-package table
- **`reference/shared-libraries.md`** — when shared source is allowed at all, the register, layout,
  naming, consuming one, and **the rebuild trap** (read this before editing any shared library)
- **`reference/testing.md`** — interface-based AWS mocking, `go-sqlmock`, testing `crypto/rand` and
  `log.Fatalf` paths, coverage expectations
- **`reference/schema-md.md`** — the `schema.md` template

## Related

- `lambdas-node` skill — the Node.js sibling, for a Lambda that cannot be Go
- `infrastructure` skill — packaging, timeouts, and the `hash_extra` requirement for shared libraries
- `documentation` skill — the Lambda `README.md` and shared-library `README.md` formats
- `mysql` skill — the schema the `models` package reads and writes
