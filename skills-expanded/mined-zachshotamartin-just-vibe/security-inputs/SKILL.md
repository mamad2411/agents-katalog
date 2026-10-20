---
name: security-inputs
description: "Audit validation and injection risks at input boundaries. Use for injection and unsafe interpreter boundaries; llm-injection handles model instruction confusion, and security-fix repairs a confirmed injection."
---

# security-inputs

Audit validation and injection risks at input boundaries.

## Choose this workflow

Use for injection and unsafe interpreter boundaries; llm-injection handles model instruction confusion, and security-fix repairs a confirmed injection.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Security methods](../../references/packs/security.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; entry points, input formats, interpreters/sinks, and relevant source.

**Pack prerequisites:** Defined application boundary, authorized code/environment, relevant trust/access rules, and evidence sources. Default to defensive inspection; active tests use owned or explicitly authorized isolated targets. Minimize sensitive evidence and never print usable credentials.

- **Infer from evidence:** Resolve the requested surface, source/runtime version, reachable callers and actual trust/access boundaries.
- **Reasonable default:** Start with source analysis and bounded owned fixtures; treat scanner output as leads and preserve legitimate controls.
- **Ask only when needed:** Ask when target authorization or necessary trust semantics are unresolved before active probing; source inspection need not wait for production access.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Injection, unsafe parsing, traversal, and validation gaps along reachable paths.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Trace each untrusted value from its source through transformations and validation to the final sink.
2. Assess parameterization or contextual encoding at the actual interpreter boundary, distinguishing validation from authorization.
3. Propose safe regression cases.

## Technical method

- **Inspect:** Identify attacker-controlled sources, transformations and actual SQL/shell/template/URL/parser/path sinks.
- **Method:** Load matching vulnerability cards and framework defaults; trace a reachable path and effective parameterization, encoding or allowlist controls.
- **Avoid misdiagnosis:** A dangerous-looking API with trusted constants is not automatically exploitable; input validation alone does not make every interpreter safe.
- **Check the result:** Exercise a safe local regression for the unsafe boundary and a valid control; retain unknown reachability/configuration as conditional.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Security worked example](../../references/examples/security.md).
- Untrusted values reach queries, commands, rendering, URLs or parsers: [Injection and interpreter boundaries](../../references/security/injection.md).
- An available scanner or dependency advisory check can answer the scoped question: [Scanner selection and evidence](../../references/security/scanners.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves bug bounty, authorized pentest, security proof; load only the matching method: [Authorized vulnerability research](../../references/methods/authorized-security-research.md).

## Decision branches

- **When the input reaches a safe parameterized sink:** Do not flag injection solely because the input is user controlled; inspect other reachable sinks separately.

## Deliver and verify

- Evidence-backed findings or justified protections with the source-to-sink path, required conditions, focused remediation and a safe regression fixture.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A concatenated query path is assessed end to end; safe parameterization is not flagged solely due to user input presence.

## Stop and recover

- No destructive payloads or third-party probing. Unsupported exploitability remains a risk hypothesis rather than a confirmed breach.

## Example requests

- **Normal (inspect):** Trace untrusted filters to SQL and template sinks without active remote probing.
- **Edge (inspect):** Review SQL and template paths where only one uses unsafe concatenation.
- **Blocked (inspect):** Inspect source without sending destructive payloads or probing third parties.
