---
name: vuln-deserialization
description: Insecure deserialization validation — detect unsafe object deserialization across Java, PHP, Python, .NET, and Node.js stacks using time-based and OOB oracles without deploying gadget-chain payloads against production systems.
disable-model-invocation: true
risk: destructive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Deserialization — unsafe object-deserialization validation

Use this skill to validate insecure deserialization on an authorized, in-scope target. Detect whether user-controlled serialized objects are accepted and whether they can trigger code execution through gadget chains. Focus on detection and confirmation — identify the serialization format, the framework, and the fact that user input reaches a deserialization sink. Do not deploy full gadget-chain payloads against production, run reverse shells, or exfiltrate data from the target.

## Required inputs

- Written scope naming the target, authorized endpoints for deserialization testing (API endpoints accepting binary/Base64 payloads, cookie values, hidden form fields, JWT payloads), and explicit permission for deserialization validation including the approved detection methods (magic-byte probe, time oracle, OOB oracle).
- Valid authorization cache. Destructive risk class requires explicit maintainer approval before any execution probe.
- OOB callback infrastructure if using blind detection.
- Known framework stack (Java/Spring, PHP/Laravel, Python/Django, .NET, Node.js) from recon — this informs which serialization format to prioritize.
- Explicit acknowledgment that gadget-chain detection carries inherent risk: even a probe payload may trigger unintended code execution if the target uses vulnerable libraries. The scope must accept this risk.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution with destructive-risk approval — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — serialization-format discovery

Determine which serialization format the target uses before attempting any deserialization probe:

**Java (most common target)**:
- Magic bytes: `AC ED 00 05` (hex). Base64-encoded objects begin with `rO0`.
- Look for: `Content-Type: application/x-java-serialized-object`, JSESSIONID cookies with Base64 values, `javax.faces.ViewState` in JSF applications, `__VIEWSTATE` in ASP.NET.
- Framework indicators: `X-Powered-By: Servlet/3.0`, Spring Boot error pages, Java stack traces.

**PHP**:
- Format: `O:<length>:"<class>":<num_properties>:{...}` (human-readable).
- Look for: PHP session cookies, serialized data in hidden form fields, `laravel_session` cookies.
- Framework indicators: `X-Powered-By: PHP/7.x`, Laravel/Symfony error pages.

**Python (pickle)**:
- Protocol version bytes: `80 02` (protocol 2), `80 03` (protocol 3), `80 05` (protocol 5).
- Look for: Flask/Django session cookies (often Base64-encoded pickle), `session` cookie values.
- Framework indicators: `Server: Werkzeug/...`, Django debug pages.

**.NET**:
- Format: `BinaryFormatter` binary payload, `LosFormatter` (Base64), `ObjectStateFormatter`.
- Look for: `__VIEWSTATE`, `__EVENTVALIDATION` in ASP.NET Web Forms.

**Node.js**:
- Look for: `node-serialize`, `serialize-javascript`, or custom JSON-with-function serialization.
- Framework indicators: `X-Powered-By: Express`.

Record the likely format, the endpoints carrying serialized data, and framework indicators before probing.

### Phase 2 — magic-byte and format validation

Send structurally valid but semantically empty serialized payloads to confirm the endpoint deserializes user input:

- **Java**: send a valid serialized `java.lang.String` object (non-malicious, no gadget chain).
- **PHP**: send `O:8:"stdClass":0:{}` (empty object).
- **Python pickle**: send a pickle of `{"test": "probe"}` (simple dict).
- **.NET**: send a minimal valid `BinaryFormatter` payload with a safe type.

Observe the response:
- If the endpoint returns a different status or error when receiving valid vs invalid format → the endpoint processes serialized data.
- If the endpoint returns data that reflects the probe object's content → deserialization and reflection confirmed.
- If the endpoint consistently rejects all formats → likely not a deserialization endpoint.

### Phase 3 — time-based gadget detection

When deserialization is confirmed, test for gadget-chain execution using time delays:

This phase requires destructive-risk maintainer approval. Do not proceed without it.

For each relevant gadget chain family:
1. Generate a probe payload that calls `Thread.sleep(5000)` (Java), `sleep(5)` (PHP/Python), or equivalent.
2. Send the payload and measure response time.
3. If response time increases by ≥4 seconds consistently → gadget-chain RCE confirmed.
4. Cross-validate by varying sleep duration (3s, 5s, 7s).

Use only well-known, low-risk gadget probes. Never generate payloads that:
- Execute commands beyond sleep/timeout.
- Write files, modify system state, or open network connections.
- Exploit zero-day or unpatched gadget chains without maintainer approval.

### Phase 4 — OOB gadget detection

When time-based detection is unreliable, use OOB callback gadgets:

```text
Java JNDI probe (Log4Shell-style detection, not full JNDI injection):
  ldap://<CANARY>/probe

DNS callback probe:
  nslookup <CANARY> (via Runtime.exec gadget)

HTTP callback probe:
  curl http://<CANARY>/gadget (via URLClassLoader or Runtime.exec gadget)
```

Rules:
- The CANARY domain must be engagement-specific.
- The callback URL must carry no data — callback alone is proof.
- If a gadget chain executes and the callback arrives, RCE is confirmed. Stop immediately.

### Phase 5 — framework-specific assessment

Based on Phase 1 discovery, prioritize:

- **Java + Spring**: test CommonsCollections, Spring, Hibernate, Groovy, ROME gadget families. Check for `ysoserial` compatibility.
- **PHP + Laravel/Symfony**: test `phpggc` gadget chains. Focus on `__destruct`, `__wakeup`, `__toString` magic methods.
- **Python + Flask/Django**: test pickle `__reduce__` and `__reduce_ex__` gadgets. Check if `pickle.loads()` is reachable from cookies.
- **.NET**: test `ObjectDataProvider`, `TypeConfuseDelegate`, `TextFormattingRunProperties` gadgets.
- **Node.js**: test `node-serialize` `_$$ND_FUNC$$_` function injection and `serialize-javascript` eval vectors.

## Decision points

- **Stop at format confirmation with no execution**: if the endpoint deserializes but gadget probes produce no time delay or OOB callback → the deserialization is present but not exploitable with tested gadgets. Record finding with "needs further gadget research" note.
- **Stop at first time delay**: if `sleep(5)` gadget executes, RCE is confirmed. Do not test additional gadget chains.
- **Stop at first OOB callback**: OOB callback is RCE confirmation. Do not escalate.
- **Refuse reverse-shell escalation**: reverse shells, file writes, and data exfiltration are outside safe validation scope.

## Prohibited behavior

- Deploying gadget chains that execute commands beyond sleep/timeout or OOB callback.
- Writing files, modifying database records, or altering system state via gadget execution.
- Running reverse shells, bind shells, or persistent backdoors.
- Exfiltrating data through gadget chains (file read, environment variable dump, credential access).
- Using JNDI injection to load remote codebases or establish persistent access.
- Testing gadget chains on production during business hours without explicit coordination.

## Stop conditions

- Sleep gadget executes (≥4s delay) → RCE confirmed, stop.
- OOB callback received → RCE confirmed, stop.
- All gadget families tested produce no execution → negative result for known gadgets, document.
- WAF blocks serialized payloads, endpoint returns consistent 400/415 → protected, document.
- Error message reveals internal classpath or vulnerable library versions → redact, document cleanup recommendation, stop.

## Evidence — deserialization matrix

For each tested endpoint, record:

```text
Endpoint: <URL>
Serialization format: <Java | PHP | Python pickle | .NET BinaryFormatter | Node.js | unknown>
Framework indicators: <Spring Boot | Laravel | Django | Express | ...>
Format validation: <accepted | rejected | indeterminate>
Gadget family tested: <CommonsCollections6 | __wakeup | __reduce__ | ...>
Time-based result: <no delay | delay: N seconds | timeout>
OOB callback received: <yes (dns) | yes (http) | no>
Impact: <none | deserialization accepted but no gadget | RCE confirmed via sleep | RCE confirmed via OOB>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a format × gadget-family matrix. Never store: serialized payload bytes that contain functional exploits, OOB callback URLs with target data, stack traces with internal classpaths, or gadget-chain configurations that could be replayed.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected endpoint, serialization format, confirmed gadget family, CVSS estimate (8.5–9.8 for confirmed RCE, 6.0–7.5 for deserialization without confirmed gadget), and remediation guidance.
2. Reference the deserialization matrix.
3. Recommend: avoid deserializing user-controlled data entirely, use safe serialization formats (JSON with schema validation), implement type allowlists for deserialization, apply runtime application self-protection (RASP) to block gadget chains, upgrade libraries with known gadget-chain CVEs, and run deserialization security tests in CI.
