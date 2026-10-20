---
name: lambdas-node
description: Node.js AWS Lambda conventions — when Node is justified over Go, ESM/.mjs modules, the nodejs runtime and index.handler entry point, factory-function dependency injection, node --test with co-located .test.mjs files, the structured log line format, npm-install-on-package packaging, and the same trigger-based directory naming as Go Lambdas (api-, api-socket-, alb-, url-, sqs-, sns-, dynamo-, kinesis-, kafka-, s3-, bus-, pipe-, schedule-, cognito-, secrets-, ninja- and the rest). Use when writing, editing, reviewing or testing a Node.js Lambda, or deciding whether a Lambda may be written in Node at all. Prototype and proof-of-concept projects only — not for production.
---

# Node.js Lambda Conventions

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

Applies to every Node.js Lambda function in the repository.

Go is the default for Lambdas (see the `lambdas-go` skill). **A Node.js Lambda is a registered
exception, not a free choice** — but where it is justified, it is a first-class Lambda held to
equivalent standards, not a scratch script.

## When Node Is Justified

The bar is that **an official vendor library exists for Node and not for Go, and reimplementing it
in Go would be the wrong kind of original work** — security-sensitive, cryptographic, or protocol
code whose bugs surface intermittently in production rather than as a failing test.

The worked example: Cognito's Custom Email Sender trigger encrypts the code it hands the Lambda
using the AWS Encryption SDK message format (KMS keyring, HKDF key derivation, an embedded
signature). AWS publishes official AWS Encryption SDK clients for Java, Python, JavaScript/Node.js,
.NET and C — **there is no official Go implementation.** Hand-rolling that decryption in Go was
judged too high-risk for a security-sensitive path (password reset and sign-up codes) against using
AWS's own `@aws-crypto/client-node`.

What does **not** clear the bar: familiarity, a nicer npm package for something Go can already do,
or wanting to reuse frontend code. "There is a convenient library" is not the same as "there is no
viable Go path".

**Every Node Lambda is recorded as a deliberate exception in the project's own conventions, with its
reason** — otherwise the next reader takes it as precedent. See the `conventions` skill on
registered exceptions.

## Runtime & Packaging

- **Runtime**: a current `nodejs<N>.x` Lambda runtime, pinned in Terraform
- **Handler**: `index.handler` — the exported handler in `index.mjs`
- **ESM, not CommonJS.** `package.json` sets `"type": "module"`; source files are `.mjs`. No
  `require`, no bundler, no transpiler
- **`package.json` is `"private": true`** with an explicit `main`, and pins its dependencies
- **`.gitignore` ignores `node_modules/`**
- **No build step of our own.** `terraform-aws-modules/lambda/aws` given a **plain-string
  `source_path` pointing at a folder containing `package.json`** runs `npm install` automatically
  before zipping. That is deliberately the whole build: there is no separate step to remember, and
  no bundler config to keep in sync

```hcl
# A plain string source_path pointing at a folder containing package.json
# makes this module run `npm install` automatically before zipping — no
# separate build step to maintain here.
source_path = "${path.module}/../lambdas/cognito-custom-email-sender"
```

Note this differs from a Go Lambda's `source_path`, which is a list with explicit `commands` and
`patterns`. Don't copy the Go form here.

## Directory Naming

**Identical to Go Lambdas** — the trigger must be visible from the directory name alone:

| Trigger | Name |
| --- | --- |
| API Gateway HTTP route | `api-<http-method>-<purpose>` (route under an `/api` prefix) |
| API Gateway WebSocket route | `api-socket-<route>`, dropping the `$` — `api-socket-connect` |
| Application Load Balancer target | `alb-<http-method>-<purpose>` |
| Lambda function URL | `url-<purpose>` — no method |
| SQS queue | `sqs-<sqs-queue-name>` (drop a `.fifo` suffix) |
| SNS, Amazon MQ, DynamoDB stream, Kinesis, MSK/Kafka, DocumentDB change stream | `sns-`, `mq-`, `dynamo-`, `kinesis-`, `kafka-`, `docdb-`, then what the Lambda does |
| S3 lifecycle event | `s3-<what-it-handles>` — the event, or a terse summary of the work; see `lambdas-go` |
| EventBridge bus event | `bus-<what-the-lambda-does>`, not the event name — see `lambdas-go` |
| EventBridge Pipe | `pipe-<what-the-lambda-does>` |
| Schedule (scheduled rule or EventBridge Scheduler) | `schedule-<frequency>-<purpose>` — `schedule-nightly-clear-caches` |
| Cognito User Pool trigger | `cognito-<what-it-handles>` — `cognito-custom-email-sender`; see `lambdas-go` |
| CloudWatch Logs subscription, CloudWatch alarm, SES receipt rule, IoT Core rule | `logs-`, `alarm-`, `email-`, `iot-`, then what the Lambda does |
| Aurora MySQL from SQL, Lambda destination | `aurora-`, `lambda-`, then what the Lambda does |
| Secrets Manager rotation | `secrets-<what-it-rotates>` — `secrets-aurora-credentials` |
| Manual invocation only | `ninja-<purpose>` |
| Anything else | the function's purpose |

**Corrected:** the last row used to read "A provider trigger, or anything else", with
`custom-email-sender` — a Cognito trigger — as its example. Cognito triggers now take the
`cognito-` prefix, for the reasons given in `lambdas-go`; an existing unprefixed one is not wrong,
but new ones take the prefix.

The language a Lambda is written in is **not** part of its directory name. A reader should not have
to care.

## Structure

```
lambdas/<function-name>/
  package.json         # "type": "module", "private": true, pinned deps
  package-lock.json
  .gitignore           # node_modules/
  index.mjs            # factory functions + the exported handler, wired at module load
  index.test.mjs
  <topic>.mjs          # one file per subject — templates, validation, a client wrapper
  <topic>.test.mjs
  schema.md            # required — the input contract
  README.md            # required — four sections + flow diagram
```

- **One file per subject**, named for the subject. The same principle as a Go Lambda's sub-packages,
  flattened: a Node Lambda small enough to justify the exception rarely needs directories
- **Test files sit beside the file they test** — `templates.test.mjs` tests `templates.mjs`

Read **`reference/structure-and-testing.md`** for the factory-function pattern and the test
approach before writing one.

## Dependency Injection via Factory Functions

**Logic is structured as small factory functions that take their external dependencies as
parameters** — `makeHandler`, `makeDecryptCode`, `makeSendEmail` — so tests exercise real
orchestration logic against fake dependencies rather than mocking the AWS SDK or hitting real AWS.

```js
export function makeHandler({ decryptCode, sendEmail, frontendUrl }) {
  return async function handler(event) { /* … */ }
}
```

This is the **direct analogue of a Go Lambda's `Handler` struct holding interface-typed
dependencies**, and it is there for the same reason: the orchestration is the part worth testing,
and it is only testable if the I/O is injected.

**Module top-level is the wiring layer** — the Node equivalent of Go's `main.go`. Read environment
variables, construct the real SDK clients, call the factories, and export the result:

```js
const sesClient = new SESv2Client({})
const decryptCode = makeDecryptCode({ decryptFn: buildDecrypt(...).decrypt, kmsKeyArn: process.env.KMS_KEY_ARN })
const sendEmail   = makeSendEmail({ sesClient, fromEmail: process.env.FROM_EMAIL })

export const handler = makeHandler({ decryptCode, sendEmail, frontendUrl: process.env.FRONTEND_URL })
```

**Export the factories as well as the wired handler**, since the factories are what tests call.

## Logging

**The same format as Go Lambdas** — one convention across the whole platform, so log searches work
regardless of a function's language:

```js
console.log(`[module:file:function:step] message key=value`)
console.log(`[cognito-custom-email-sender:index.mjs:handler:start] triggerSource=${triggerSource} userName=${userName}`)
```

- Log at function entry, before and after significant operations, and at decision points —
  **including the paths that do nothing**, which are the ones you cannot infer from an absence
- **Never log secrets, tokens, decrypted codes, or unmasked PII.** A Lambda handling a decrypted
  credential must be read carefully on this point: log that a code was decrypted, never the code

## Testing

- **Node's built-in test runner** — `node --test`, wired as `"test": "node --test"` in
  `package.json`. **No external test framework dependency**
- Test files are `*.test.mjs`, **co-located** with the source they test
- Tests call the **factories** with fake dependencies and assert on real orchestration — never mock
  the AWS SDK, never hit AWS

```bash
npm test                                  # from the Lambda's own directory
node --test index.test.mjs                # a single file
```

## Required Documentation

**The same two files as every Go Lambda** — the language changes nothing about the documentation
contract:

- **`schema.md`** — the input contract: summary, TypeScript-syntax schema, worked JSON examples. See
  the schema-md reference **in the `lambdas-go` skill** — the template is language-agnostic
- **`README.md`** — four sections (Invocation, Purpose, Interface, Implementation with a rendered
  flow diagram). See the `documentation` skill's READMEs reference

## Related

- `lambdas-go` skill — the default, and the source of the naming, logging and documentation rules
  this skill shares
- `conventions` skill — how a registered exception is recorded, and why the reason must travel with
  it
- `infrastructure` skill — the Lambda module, timeouts, and (for a Custom Email Sender) the KMS key
  policy and the Cognito trigger's dependency cycle
