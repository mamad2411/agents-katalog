---
id: serverless-security
version: "2.0.0"
title: "Serverless Security"
description: "What a function-as-a-service platform changes: an execution environment reused between invocations so /tmp and module globals outlive a request, an event envelope that is attacker-influenced whichever trigger delivered it, encrypted-at-rest configuration that the control-plane API still returns in cleartext, and concurrency as the boundary between an incident and a bill. Use when generating Lambda, Cloud Functions, or Azure Functions code, serverless.yml or SAM templates, or wiring API Gateway, EventBridge, SQS, or S3 triggers."
category: hardening
severity: high
applies_to:
  - "when generating AWS Lambda / GCP Cloud Functions / Azure Functions code"
  - "when generating serverless.yml, SAM, or function infrastructure"
  - "when wiring an HTTP, queue, storage, or event-bus trigger to a function"
  - "when a function caches, writes to /tmp, or keeps state between invocations"
languages: ["python", "javascript", "typescript", "go", "java", "yaml"]
token_budget:
  minimal: 1300
  compact: 1700
  full: 2100
rules_path: "checklists/"
related_skills: ["iam-best-practices", "iac-security", "api-security", "logging-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP Serverless Top 10"
  - "AWS Well-Architected: Security Pillar — Serverless"
  - "CWE-770: Allocation of Resources Without Limits or Throttling"
---

# Serverless Security

## Rules (for AI agents)

### ALWAYS
- Treat the **execution environment as reused**. The platform freezes it when the
  handler returns and thaws it for the next invocation, which may serve a different
  tenant. So a module-level global holding per-request state — a decrypted payload, an
  authorization decision, a tenant id, a connection bound to one caller's credentials
  — is visible to the next request. Cache only what is safe to share, and reset or
  scope everything else inside the handler.
- Treat **`/tmp` as shared, persistent, and finite**. It is the only writable path, it
  survives across invocations in the same environment, and a fixed filename written
  for one user is readable by the next. Use a per-invocation subdirectory, delete it
  before returning, and never read back a path without having written it in the same
  invocation.
- Validate the **whole event, envelope included**. The trigger's identity is not
  authentication: an S3 object key is chosen by whoever can PUT to the bucket, SQS
  message attributes and EventBridge `detail` are producer-supplied, and an API
  Gateway authorizer context is only as trustworthy as the authorizer. Validate
  against an explicit schema before any code touches the payload, and where a function
  has more than one trigger, check the source discriminant and route by allowlist.
- Give each function its **own execution role** with only the permissions its stated
  job needs. `iam-best-practices` owns policy scope and the escalation paths;
  what is serverless-specific is one role per function, never shared, because a shared
  role gives every function the union of what any of them needs.
- Set concurrency deliberately, and know which control you are reaching for.
  **Reserved** concurrency caps a function's parallel executions and is the
  denial-of-wallet control; **provisioned** concurrency pre-initialises environments to
  remove cold starts and *bills for them whether or not they are used*. Reserved
  capacity is also drawn from a shared account pool, so setting it per function is a
  decision about the account, not just that function.
- Bound the **retry and failure path**. Asynchronous invocations are retried by the
  platform, so one poison event becomes repeated executions, repeated spend, and
  repeated side effects if the handler is not idempotent. Configure the retry count,
  the maximum event age, and a dead-letter queue or failure destination — and for a
  batch source, report partial batch failures rather than failing the whole batch.
- Decide what the handler **returns on a message it could not process**. Returning
  success deletes the message and loses the data; raising on every message creates an
  infinite retry loop feeding a queue nobody drains. Both are silent.
- Set a timeout that reflects the work, and know it holds a concurrency slot for its
  whole duration — which is what makes a long timeout an amplifier during an attack
  rather than merely a slow response.

### NEVER
- Rely on **encryption at rest** to keep a configuration value secret. Encrypting a
  function's environment variables protects the stored bytes; the control-plane API
  that reads a function's configuration still returns them in cleartext to anyone with
  permission to call it, and they appear in the deploy artifact and the IaC state file.
  Fetch the secret from a secret manager at initialisation and cache it with a TTL, or
  store ciphertext and decrypt in the handler.
- Expose a **function URL or HTTP trigger with authentication turned off** and treat
  the obscurity of the URL as the control. Every platform has an unauthenticated
  setting and every platform makes it the easy one. `api-security` owns what
  authenticating the endpoint means; the reference has the per-platform setting names.
- Pass event-derived strings to a shell — `os.system`, `subprocess` with `shell=True`,
  `child_process.exec`. An S3 object key reaches a converter this way as readily as an
  HTTP parameter does; the trigger type does not change the sink.
- Attach a **long-lived static access key** to a function to call its own cloud. The
  execution role already provides credentials, and a static key in the environment is
  the one credential the platform cannot rotate.
- Put a function in a private subnet and assume it can still reach the services it
  needs. Network attachment is not an egress control — a subnet with a NAT route has
  full outbound internet — and a subnet *without* one cannot reach the secret manager,
  so the hardened function times out on its first initialisation.
- Log the whole event. `print(json.dumps(event))` at the top of a handler publishes
  authorization headers, authorizer context and message attributes to the log group.
  `logging-security` owns the rule; this is the line that generates it.

### KNOWN FALSE POSITIVES
- A **cold-start warmer** on a schedule is an operational choice, not a finding.
- A function that legitimately needs elevated permissions for a **bounded setup task** —
  a custom infrastructure resource, a one-off migration — is not a least-privilege
  violation while it is gated and revoked on completion. A bootstrap role that survives
  bootstrap is a finding again.
- A long timeout on a function whose work genuinely takes that long is correct. The
  finding is a timeout nobody chose, or one set to the platform maximum to avoid
  thinking about it.
- Caching a secret, a client, or a database connection in a module-level global is the
  intended pattern and is why environment reuse exists. The finding is *request* state
  in the same place — and a cached secret still needs a TTL, or it outlives its
  rotation.

## Context (for humans)

Most serverless advice is ordinary application-security advice with different nouns.
The parts that are genuinely different are the ones this skill leads with, and they all
come from the same source: the platform reuses the environment.

That single fact produces the `/tmp` bleed, the global-variable bleed, the cached
secret that outlives its rotation, and the background promise that resumes under the
next invocation's request context and logs to its log stream. None of it looks wrong in
a code review, because a module-level global is exactly what you would write in a
long-running process — where it is also correct, since there the process serves one
deployment rather than a queue of unrelated callers.

The second theme is that the event is input. Teams reason about an HTTP handler as
untrusted and a queue consumer as internal, but a queue message carries values someone
chose, and "someone" is whoever can write to the queue or the bucket. The trigger tells
you how the invocation arrived, not who caused it.

Denial-of-wallet is the third, and it is the one with no equivalent on a server: an
attacker cannot exhaust capacity that scales, so they exhaust the budget instead. The
control is a concurrency cap, and the reason it is worth stating carefully is that the
setting next to it — provisioned concurrency — makes the bill larger.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/platform-settings.md` — per-platform names for the HTTP-trigger auth
  mode, environment-variable encryption, concurrency, retries and dead-letter
  configuration, ephemeral-storage sizing, and the code-signing and image-pinning
  options that apply to each package type
- `checklists/lambda_hardening.yaml`
- `checklists/event_validation.yaml`
- [OWASP Serverless Top 10](https://owasp.org/www-project-serverless-top-10/).
- [CWE-770](https://cwe.mitre.org/data/definitions/770.html).
