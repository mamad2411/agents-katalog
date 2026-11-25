---
name: secure-code-auditor
description: >-
  Backend security auditor for Django and DRF on an OWASP Top 10 (2025), API
  Security Top 10 (2023), and ASVS 5.0 foundation. Use when backend code is
  written or reviewed and touches authentication, sessions, cookies, JWT,
  OAuth2/OIDC, API keys, password hashing, permissions, access control,
  IDOR, SSRF, path traversal, open redirect, impersonation,
  SQL/command/template injection, LDAP, row-level security, encrypted
  columns, NoSQL, Redis, file uploads, S3, serializers, rate limiting,
  CSRF/CORS, OpenAPI schema, GraphQL, Django Ninja, FastAPI, gRPC, AI agents, MCP
  tools, secrets, payments, webhooks, Celery, Django tasks, race conditions,
  ReDoS, caching, deserialization, async/ASGI, WebSockets, audit logging,
  erasure, retention, personal data, migrations, JWKS, mutual TLS,
  SECRET_KEY, SBOM, X-Forwarded-For, SPF/DKIM/DMARC, or deployment config,
  even if "security" is never used. Review-time returns prioritized findings
  with fixes; write-time applies secure defaults. Django/DRF-first; general
  layer suits any stack.
license: MIT
allowed-tools: Read, Grep, Glob, Bash
metadata:
  author: n-shadloo
---

# secure-code-auditor

A backend security skill. It reviews server-side code, and it applies secure
defaults while new code is written. Django and DRF are the deep specialty. A
stack-neutral layer under them suits any backend. The scope is the backend:
server-side code, data, configuration, and the deployment the backend owns.
Browser and frontend concerns stay out, except where the server controls the
output. Other agents (Codex, Cursor, Gemini CLI) reuse this content through
`AGENTS.md`, with Claude as the primary integration.

## Self-improvement

If this skill's text or script caused a mistake, or you had to find a step
yourself, record it at once. Before you claim the task is done, end the report
with `Skill defects:`. Section 0 of `SELF-IMPROVEMENT.md` gives the rules. If
`~/.skill-improvements/secure-code-auditor/` exists, do section 3 first.

## How the reference material is organized

Everything sits on the **OWASP Top 10:2025 spine**. Each reference has two
layers. The **principle layer** states the vulnerability and the defense in
stack-neutral terms. The **Django & DRF layer** holds the settings, the code
patterns, the correct and wrong examples, and the gotchas. A sub-topic
checklist splits the same way, into `#### Stack-neutral` and `#### Django &
DRF`. A file's final `## Review checklist` may stay unsplit, and neither form
is a defect.

Every control is stated in two grammars. The review form says what to flag.
The write-time form says what to write, in a paragraph that opens
`**Write-time.**` directly under the control it completes. Every reference
that owns a control carries at least one. The two that do not are the
methodology file and the library index.

Load only the file for the concern in front of you. Pick the group, then the
row. Where two rows could both match, the ownership table below decides which
file is authoritative.

### Start here

| Concern | Reference file |
|---|---|
| How a codebase is swept: the phase order and per-phase artifacts, the entry-point inventory (URLconf chains at their resolved prefixes, DRF routers and `@action` methods, Django Ninja, FastAPI routers beside Django, GraphQL, gRPC, Channels, Celery and beat, management commands, signals, admin, webhooks, MCP tools, middleware), principals and trust boundaries, source-to-sink pairing, hypothesis order, the budget rule for a large tree, the six-item verification gate, the cross-cutting benign-pattern catalog, the coverage ledger, attack chains, the security regression harness and scanner gating, the WSTG section mapping | `references/01-audit-workflow.md` |
| How a finding is scored and written: the severity rubric and the baseline table under it, the confidence scale, the finding schema and its evidence line, the report structure, the ASVS 5.0 chapter mapping and its non-goals, mode selection, the standing write-time contract with its per-moment index, the conflict rule, the security-decisions note | `references/00-methodology-and-severity.md` |

### The OWASP Top 10:2025 spine

| Concern | Reference file |
|---|---|
| **A01** Object- and function-level authorization, IDOR/BOLA, generic relations and the client-chosen content type, URL resolution (missing anchors, shadowed routes, `reverse()` against `resolve()`), multi-tenancy and tenant freshness, caching and authorization with the 2026 cache CVEs, SSRF and egress control, path traversal on a read the request names, open redirect, locale redirects and language negotiation, admin exposure | `references/a01-broken-access-control.md` |
| **A02** `DEBUG` and `ALLOWED_HOSTS`, the `SECURE_*`/`SESSION_*`/`CSRF_*` matrix, `__Host-` and `__Secure-` cookie prefixes and cookie tossing, the signed-cookie legacy salt fallback, CSRF trusted origins, wildcard allowlist entries, Fetch Metadata, CORS and origin regexes, compression and BREACH, CSP, mail authentication (SPF, DKIM, DMARC, MTA-STS, TLS-RPT, `MAILERS`), CAA and dangling DNS, `security.txt`, `check --deploy` and its blind spots, project guardrail checks, configuration drift, the expiring exception | `references/a02-security-misconfiguration.md` |
| **A03** Supported Django lines, pins and hash verification, index resolution and dependency confusion, `pip-audit`, the SBOM from the lockfile, the scan gate read as configuration, build provenance and verification, SLSA claim levels, the artifact boundary, third-party vetting, the development-only package in the production requirements file, migration and data-integrity safety | `references/a03-software-supply-chain.md` |
| **A04** Password-hashing families and parameters, the wrapped-hasher migration for dormant accounts, peppering, randomness and token generation, constant-time comparison, signing and per-purpose salts, data in transit and at rest, key lifecycle and envelope encryption against a KMS, cryptographic agility and the four-step algorithm migration, post-quantum posture | `references/a04-cryptographic-failures.md` |
| **A05** The sink inventory the whole skill defers to, source-to-sink tracing, SQL and the ORM escape hatches, dictionary-expansion column aliases, GeoDjango raster and spatial lookups, OS command and argument injection, template injection and server-rendered output, Markdown renderers, LDAP filters and distinguished names, header and email injection, CSV and workbook formula injection, XML external entities | `references/a05-injection.md` |
| **A06** Which flows need a rate limit or anti-automation, the inventory of money, credit, entitlement, and status writers (commands, tasks, admin actions, signals, migrations, bulk writes), database-held invariants, amount and currency binding, capture, refund, and reversal, entitlement grant against revocation, side-effecting actions, email and notification abuse, algorithmic resource exhaustion and its per-surface bounds | `references/a06-insecure-design.md` |
| **A07** The user model as an identity contract (identifier, normalization, collation, `is_active`), password policy and breached-corpus screening, sessions and session engines, rotation and revocation, JWT and SimpleJWT, token storage, brute force and enumeration, password reset, email change and purpose-bound tokens, MFA and TOTP seed storage, OAuth2/OIDC and social login with the mix-up attack, passkeys and WebAuthn, `REMOTE_USER` header authentication, API keys | `references/a07-authentication-failures.md` |
| **A08** Insecure deserialization (`pickle`, `yaml`, and the cache, session, and fixture paths Django runs unasked), Celery task messages and the remote-control channel, Django's built-in tasks framework and its inline default backend, signed cookies and data, inbound webhook integrity (raw body, signature, timestamp, replay, per-provider schemes, tenant binding), outbound webhook delivery, pipeline and artifact integrity | `references/a08-integrity-and-deserialization.md` |
| **A09** The never-log list, error-report scrubbing, the security event set, lifecycle hooks and audit guarantees, log injection and integrity, forensic readiness (append-only sinks, hash chains and their limits, clocks, correlation identifiers), decoy records and canary tokens | `references/a09-logging-and-alerting.md` |
| **A10** Fail-open against fail-closed checks, error views and stack-trace leakage, races and TOCTOU, constraints against row locks, the `select_for_update()` failure modes, `get_or_create()`, state-transition enforcement, side effects and the commit boundary, idempotency-key design, ReDoS and regular-expression cost | `references/a10-exceptional-conditions.md` |

### Cross-cutting surfaces

These span several categories, so this group sorts by the surface in front of
you rather than by OWASP number.

| Concern | Reference file |
|---|---|
| The privilege model (RBAC/ABAC/ReBAC), what Django's permission layer does, `has_perm` with an object, the DRF object-hook table, admin permission hooks and custom admin views, default-deny and the URLconf audit test, field-level authorization (BOPLA), search indexes and denormalized copies, authorization test suites, permission decay, the joiner, mover, and leaver lifecycle | `references/authorization-architecture.md` |
| Impersonation and "log in as user", django-hijack, break-glass and just-in-time elevation, the operator audit identity | `references/privileged-access-and-impersonation.md` |
| Where DRF runs the object check and the routes that skip it, `@action` and function-level authorization (BFLA), serializer over-exposure and mass assignment (`ModelForm` and formsets included), writable relations, pagination, filter, and ordering leakage, throttling mechanics and the owned atomic counter, schema and browsable-API exposure, the endpoint inventory and shadow routes, versioning and deprecation, bulk endpoints, unsafe DRF defaults, DRF and CSRF, payment webhook bodies | `references/api-drf-specific.md` |
| GraphQL resolver authorization and nested traversal, all-fields types, document depth, alias, token, and cost limits, introspection and error masking, mutations and nested writes, batching, persisted operations, Django Ninja routes with no `auth=`, FastAPI routes with no dependency and its default validation echo, gRPC servicers, interceptors, and protobuf limits, reflection and channelz | `references/graphql-and-alternative-api-surfaces.md` |
| Async and ASGI boundaries, sync ORM access, request and tenant context, WebSocket origin checks, per-connection authentication and authorization, long-lived consumer limits, subscriptions on the subscribe and publish paths | `references/async-and-channels.md` |
| File uploads from the request to the reader: type and content validation, filenames and storage keys, object-storage configuration, per-tenant buckets against shared prefixes, delegated upload URLs across S3, GCS, and Azure, quarantine and promotion, scan verdict caching and CDR, callback trust, SVG, image and archive bombs, size and quota limits, private downloads, CDN caching of private objects | `references/file-uploads.md` |
| AI agents and MCP tool surfaces: DRF viewsets republished as tools, agent token audience validation, tool scope intersected with user permissions, model output and retrieved content as untrusted input, per-agent cost and concurrency limits, server-enforced confirmation, tool-call audit, the LLM and Agentic Top 10 mapping | `references/agent-and-llm-interfaces.md` |
| The auditing agent's own access: the credential files it must never open, the name-by-location rule for every output it writes, the kind, scope, and life of its own repository credential, CI token, and deploy key, instructions inside content as data, the confirmation gate on a recommended rotation or revocation, the command and change record a layer the agent cannot edit has to author | `references/agent-operator-security.md` |
| Database roles and privilege separation, row-level security, tenant context on pooled connections, verified database TLS, field-level encryption and blind indexes, raw SQL as an isolation bypass, NoSQL and Redis injection, read-replica staleness, transaction isolation and the serialization-failure retry, connection exhaustion, copies of production data | `references/data-layer-and-database.md` |
| Deletion completeness and erasure, soft-delete tombstones and the traversals they leak through, files left after a row is deleted, retention that can be shown to have run, anonymization against pseudonymization, the personal-data inventory in the model layer, export and subject-access endpoints, audit history against erasure, lower environments | `references/data-lifecycle-and-privacy.md` |
| Service-to-service identity: machine-token validation (algorithm pinning, `iss`, `aud`, required claims), JWKS caching and rotation, sender-constrained tokens, client-certificate identity behind a proxy, network position as authentication, downstream token exchange, secret storage and delivery, `SECRET_KEY` rotation, the leaked-secret response | `references/service-identity-and-secrets.md` |
| TLS, HSTS, and hybrid post-quantum key exchange at the edge, the reverse proxy and `X-Forwarded-*` trust, the client IP behind proxies, header ownership, request smuggling and the parser chain, operational and development endpoints in production, Gunicorn and systemd hardening, container images and secrets in layers, static and media, cache and queue exposure | `references/deployment-and-runtime.md` |

### Package decisions

| Concern | Reference file |
|---|---|
| Vetted security-library choices, compatibility, minimum-safe floors, conditional, existing-install-only, and rejected candidates (current as of 9 Aug 2026) | `references/security-hardening-libraries.md` |

## Ownership and boundaries

Overlap between these files is designed. Each contested topic below has
exactly one owner. Every other file names the topic and points at the owner,
rather than restates its rules. Each reference also repeats its own half of
the rule in its opening paragraph, which is why a row can carry the decision
here. The three splits below the table turn on an axis a row would misstate,
so they keep their sentences.

| Contested topic | Owner | Deciding distinction |
|---|---|---|
| Sweeping a codebase: phase order, the entry-point inventory, principals, hypothesis order, the budget rule, the coverage ledger, a chain as one finding | `references/01-audit-workflow.md` | Procedural — what gets opened, and in what order |
| Scoring and writing a finding: the rubric, confidence, the schema, the ASVS mapping, the report, the write-time contract | `references/00-methodology-and-severity.md` | Evaluative — what an opened file is worth. The ledger's not-examined lines become the limitations section, whose shape belongs here |
| The test that holds a closed finding, and the pipeline step that runs it | `references/01-audit-workflow.md` | Procedural, and the sweep's forward half. `references/authorization-architecture.md` still owns the authorization matrix, and A03 the dependency scan gate |
| A suppression, an ignore entry, or a silenced check, and its expiry | `references/a02-security-misconfiguration.md` | An exception is a configuration decision wherever it is written. A03 keeps what a pipeline does with a suppressed scanner result |
| The per-request access-control failure | `references/a01-broken-access-control.md` | The request that reached what it should not, and how to recognize it in code |
| The privilege model behind it, field-level authorization, and which DRF paths invoke the object hook | `references/authorization-architecture.md` | The model rather than the failure. The bypass-path table lives only here |
| The identity's own lifecycle: joiner, mover, leaver, and what a provider-side disable leaves running | `references/authorization-architecture.md` | The principal and its grants over time. A07 owns each credential's own rules |
| The call sites where a correct model still fails to run | `references/api-drf-specific.md` | DRF routes, actions, and defaults rather than the model behind them |
| Which view a path reaches when two patterns match it | `references/a01-broken-access-control.md` | The request that arrived at the wrong code. `references/api-drf-specific.md` owns producing the route inventory; the pass that groups it by resolved path is here |
| Operator privilege | `references/privileged-access-and-impersonation.md` | Impersonation and break-glass, and the accountable operator identity both have to carry |
| Which flows need a rate limit or anti-automation | `references/a06-insecure-design.md` | The design question, never the mechanism |
| Throttling mechanics, and the reasons a configured rate is not the effective one | `references/api-drf-specific.md` | The mechanism every other file defers to |
| Login lockout | `references/a07-authentication-failures.md` | The limit belonging to a human credential |
| Per-agent cost and concurrency limits | `references/agent-and-llm-interfaces.md` | Budget per caller rather than requests per window |
| Whether a limit holds under concurrent requests | `references/a10-exceptional-conditions.md` | Race and idempotency mechanics |
| Algorithmic resource exhaustion: which inputs multiply work and need a bound | `references/a06-insecure-design.md` | Its own table names the surface that enforces each bound. Each of those files keeps its mechanics, down to A10 for the regular expression alone |
| The injection-sink inventory for the whole skill | `references/a05-injection.md` | Exhaustive by design, so no other file keeps a partial copy. SQL, the shell, and server-side output are owned outright; every other row points outward |
| SSRF, including the cloud metadata endpoint | `references/a01-broken-access-control.md` | Absorbed into A01 in the 2025 list; every file that reaches it defers here |
| The choice of cryptographic primitive, its parameters, and the life of a key | `references/a04-cryptographic-failures.md` | The primitive, not the place it is consumed |
| Where a secret lives, how it reaches the process, and how it rotates, `SECRET_KEY` included | `references/service-identity-and-secrets.md` | A02 owns the settings module that names it, and `references/deployment-and-runtime.md` how the environment is injected |
| What happens when the expected sequence does not hold: concurrency, idempotency keys, fail-closed error handling | `references/a10-exceptional-conditions.md` | The mechanics and the fixes. A06 keeps the inventory of flows worth attacking. A08's event de-duplication is the same design as the idempotency key here |
| What must be recorded, what must never be, and whether the record survives as evidence | `references/a09-logging-and-alerting.md` | The record, not the failure being recorded. `references/data-lifecycle-and-privacy.md` keeps the erasure obligation the retained record reconciles with |
| The receiving end of cross-system trust: the inbound webhook, the task message, both task systems, every path that turns bytes back into objects | `references/a08-integrity-and-deserialization.md` | Only the integrity of what the project itself produces and consumes. A03 keeps dependency vetting, A01 the delivery worker's SSRF, `references/deployment-and-runtime.md` broker exposure, `references/service-identity-and-secrets.md` where signing secrets live |
| The file from the request to the reader: delegated upload URLs, quarantine and promotion, proxied against signed private downloads | `references/file-uploads.md` | A08 keeps the callback's signature and replay rules. A01 keeps import-from-URL SSRF and the cache-mediated leak. `references/data-lifecycle-and-privacy.md` keeps whether the bytes are gone |
| The database as a boundary: roles, row-level security, verified transport, encrypted columns, isolation, pooling | `references/data-layer-and-database.md` | The serialization-failure retry a raised level requires is here. The constraint-against-lock choice that usually makes raising it unnecessary is A10's |
| The record over time: deletion completeness, soft delete, retention, anonymization, every copy an erasure has to reach | `references/data-lifecycle-and-privacy.md` | Existence rather than access. `references/authorization-architecture.md` owns who may read a denormalized copy, and A09 what must be logged |
| The surface where the client composes the request, and every API surface that is not a DRF route | `references/graphql-and-alternative-api-surfaces.md` | Resolver-edge authorization, document cost, and schema exposure, plus Django Ninja, FastAPI, and gRPC defaults a DRF engineer assumes are present |
| The tool-call threat model and the MCP-specific controls | `references/agent-and-llm-interfaces.md` | What changes when the caller is a program driving the backend on someone's behalf; it restates none of the machinery it reuses |
| Agent-operator access | `references/agent-operator-security.md` | The auditing agent's own access rather than the audited backend's surface. `references/agent-and-llm-interfaces.md` keeps the serving side, and `references/service-identity-and-secrets.md` the project's own secrets |
| The container image | `references/deployment-and-runtime.md` | Stops at the artifact the repository produces. Orchestrator enforcement is a cross-team recommendation, and where a secret comes from at run time is `references/service-identity-and-secrets.md`'s |

**Path traversal.** The split between A01 and `references/file-uploads.md` is
by direction rather than by file type. A01 owns the read whose path the
request named, with what Django does and does not protect there. Those flows
are the report download, the export, and the artifact or log viewer, with no
upload in them. `references/file-uploads.md` owns the name an upload brought
and the key it landed under. It also owns the private download of a file the
application stored, because the application chose that path. A05's inventory
row for the filesystem path points at A01, and it names
`references/file-uploads.md` for the storage-key half.

**Configuration against runtime.** The split is by where the setting lives
rather than by topic, so a search by topic misroutes. A02 owns what a
settings module or a DNS zone declares. `references/deployment-and-runtime.md`
owns what the proxy, the process, and the image do with a request. That
includes forwarded-header trust, and the client IP that every rate limit and
audit record depends on. A cached response splits on the same line. A01 owns
whether a cached representation may be reused across principals. The
deployment file owns the edge rule that decides what is cached at all. Mail
authentication is A02, whether your domain can be forged, while whether your
mailer can be driven is A06.

**Human against machine identity.** A07 owns the human principal and every
credential issued to one. That includes the API-key discipline a static
service key still has to meet. `references/service-identity-and-secrets.md`
owns the machine principal: mechanism choice, inbound machine-token
validation, JWKS caching and rotation, proxy-set certificate identity, and a
downstream credential obtained by exchange. The prohibition on a passthrough
of an inbound token belongs to neither. It belongs to
`references/agent-and-llm-interfaces.md`, beside the tool-call threat model.
A04 owns the primitives all three are built on.

## Mode selection

**Review-time.** Trigger on three requests. The user asks to review, audit,
scan, or "check" existing code. The user pastes code and asks whether it is
safe. The user has just finished a feature and wants a look at it. Behavior:

- Load `references/01-audit-workflow.md` first, before any topic file. It
  owns the sweep, and the topic files answer the questions that sweep
  generates. If you open a topic file first, you review whatever the codebase
  made obvious.
- Treat the codebase as **read-only**. Do not edit, refactor, or "fix in
  place" unless the user explicitly asks you to apply fixes afterward.
- Optionally run the bundled scripts for fast triage, then read the code
  yourself. Scripts surface indicators. They do not replace judgment.
- Investigate before you flag. Confirm the data flow and the reachability of
  a sink. Do not pattern-match a keyword into a finding.
- Produce a findings report in the exact format in
  `references/00-methodology-and-severity.md`. Order it by severity. Each
  finding carries a location, a CWE, an OWASP mapping, the evidence it was
  confirmed on, and a concrete fix. End with what you did *not* review.

**Write-time.** Trigger when you generate or modify backend code. Behavior:

- Apply the secure defaults from the relevant reference as you write. Those
  defaults are parameterized queries, scoped querysets, explicit serializer
  fields, correct cookie flags, safe deserializers, and secrets from the
  environment. `references/00-methodology-and-severity.md` holds the standing
  contract, and the index of which file carries each generation moment's rule.
- Prefer built-in framework mechanisms over add-ons (see the library index).
- Where a secure default conflicts with the request, apply the default. Say
  so in one line that names the risk and the exact opt-out. Never downgrade
  silently, and never refuse silently.
- Close with a short **Security decisions** note: the defaults applied,
  anything the request forced with its residual risk, and anything left for
  the caller. Write-time does not produce a findings report.

**If it is ambiguous,** default to write-time guardrails while you code, and
offer to run a review afterward.

## Using the scripts

All three scripts are read-only, stdlib-only, and make no network calls. All
three take `--json`, which is JSON Lines in each: one object per line,
consumed a record at a time. Run them for triage. Always confirm what they
surface by a read of the code.

- Entry-point inventory, the instrument for the workflow's first phase:
  `python scripts/entrypoint_inventory.py path/to/project --settings path/to/settings --json`
- One or more entry-point families at a time on a large surface:
  `python scripts/entrypoint_inventory.py path/to/project --kind url,drf,action`
- Settings posture across a whole settings package (never imports the project):
  `python scripts/settings_scan.py path/to/settings/ --json`
- Risky-pattern indicators across a tree:
  `python scripts/dangerous_patterns.py path/to/project`
- The same tree as JSON Lines, filtered, for a large codebase:
  `python scripts/dangerous_patterns.py path/to/project --json --min-severity MEDIUM`
- Confirm the scanner itself before you trust a quiet result:
  `python scripts/dangerous_patterns.py --selftest`

The inventory enumerates the declared entry points: routes at their resolved
prefixes, routers and actions, Ninja, FastAPI, GraphQL, gRPC, Channels, Celery,
commands, signals, admin, and middleware. It marks each HTTP-reachable row
with one of three states. The row declares its authorization, inherits it
from somewhere not visible there, or has none.

All three parse with the `ast` module rather than match lines, so a hit is a
structural match. Parameterized SQL, `mark_safe` on a constant, and anything
inside a docstring are not reported. Every row names the reference file that
owns it. A `dangerous_patterns.py` hit also carries a stable rule identifier.
A file that fails to parse is reported as unparsed rather than skipped in
silence. Their output is a starting point, not a final report. Map each real
issue to a reference, verify it, and report it per the methodology.

## What proof is, and the commands that produce it

Proof in this domain is the evidence a finding carries, the coverage ledger,
and the script runs. A claim without those three is not a result.

- **A finding carries confirmed evidence.** That evidence is the shortest
  source-to-sink path the finding was confirmed on, and the protection that
  failed. `references/00-methodology-and-severity.md`, "Finding schema" owns
  its shape. `references/01-audit-workflow.md`, "Phase 5 — verification" owns
  the gate that produces it. A finding without that line is a hypothesis.
  Label it as one, and put it under "Worth checking" with the exact item to
  verify.
- **The not-examined list is part of the deliverable.** The coverage ledger
  keeps examined-and-clean apart from not-examined. Its not-examined lines
  become the report's limitations section. A report that drops that section
  claims coverage the sweep did not have.
- **The exact commands are the three scripts under `scripts/`.** Run them as
  "Using the scripts" above states. Their output is a lead to verify, and
  never a finding. `python scripts/dangerous_patterns.py --selftest` proves
  the scanner itself before you trust a quiet result.

Read `docs/architecture/GROUND-TRUTH.md` and
`docs/architecture/DESIGN-RECORD.md` in the target project before any
judgment that turns on scale, configuration, or topology. Treat an absent or
stale entry as unknown, and judge against the least forgiving case. Here that
case is a reachable path and an exposed surface.

Never lower a severity to shorten a report. Never mark a not-examined surface
as examined. Never close a finding without the test that holds it closed.

## Stop conditions

Two stops already stand, and they stay. Review-time treats the codebase as
read-only. `references/00-methodology-and-severity.md`, "When a secure
default conflicts with the request" holds the firmer stop on three write-time
changes. Those are disabled TLS verification, `pickle` on a broker or a cache
other software reaches, and a production credential written into the
repository. Three more apply to this skill's own actions.

- **A live credential exposure found during a sweep.** Stop the sweep at once
  and escalate with the five fields below. Do not continue the review while a
  live credential is exposed.
- **A rotation, a revocation, a disable, or a delete.** Never execute one, at
  any level of confidence. Recommend it, write the exact command, and wait
  for a person. `references/agent-operator-security.md`, "The confirmation
  gate on a recommended action" owns the rule.
- **A read that would open credential material.** Refuse it, and ask for the
  value instead. `references/agent-operator-security.md`, "What the agent
  must never read" owns the file set.

The handoff carries five fields:

1. **The goal and the exact blocked step.** Name the sweep phase, and the
   file or the surface the stop happened on.
2. **What you attempted, with the observed evidence verbatim.** Give the
   location and the shape of the exposure, and never the value.
3. **The candidate causes you eliminated, and how.** Name each one, and the
   retrieved text that ruled it out.
4. **The single decision or action you need from the human.** State one: the
   command to run, the value to supply, or the confirmation to proceed.
5. **The state you leave behind, and whether it is safe to leave.** Give the
   coverage ledger as it stands, and name the surfaces still unexamined.

## Severity, in one line each

- **Critical** — trivially exploitable; RCE, full auth bypass, mass data
  exposure, or financial/payment manipulation.
- **High** — directly exploitable under realistic conditions; account
  takeover, privilege escalation, significant data exposure.
- **Medium** — exploitable given specific conditions, or a meaningful
  defense-in-depth gap.
- **Low** — hardening / defense-in-depth with limited direct impact.

A race is rated on how reliably its window can be won, and on what the
collision costs. It is not filed as Medium merely because it is a race. A
failure that leaves personal data alive past a promised deletion is rated on
that promise as well as on attacker value.

Report findings you are ≥80% confident are real and reachable.
`references/00-methodology-and-severity.md` holds the full rubric, the
baseline severity table, the ASVS 5.0 chapter mapping, and the report
template.

## Freshness

The claims here were verified against Django 6.1, 6.0.8, and 5.2.17 LTS, with
DRF 3.18.0. The foundation is the OWASP Top 10:2025, the API Security Top
10:2023, and ASVS 5.0.0. The agent tokens come from the OWASP Top 10 for LLM
Applications 2026 and the Top 10 for Agentic Applications 2026.
`references/security-hardening-libraries.md` carries its own index date, and
that date governs every package version claim in it.

Review again at the next Django feature release, and no later than
9 Feb 2027. Re-run the A03 dependency gate against the project's actual
Python and Django versions on every use. That gate dates faster than the rest
of the skill.
