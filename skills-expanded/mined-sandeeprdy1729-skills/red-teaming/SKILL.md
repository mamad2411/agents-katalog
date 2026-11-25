---
name: red-teaming
description: >
  Adversarial red-teaming skill for code, systems, strategies, and plans. Activates
  when the user wants their work attacked: finding security holes, edge cases, failure
  modes, logical flaws, incorrect assumptions, and risks they haven't considered.
  Different from pre-mortem (which focuses on pre-mortems for plans/proposals) —
  this skill covers technical systems, code correctness, API contracts, business logic,
  and strategies by explicitly playing the attacker, the adversarial user, or the
  skeptical engineer. Surfaces the most dangerous findings first.
  Use when user says: red team this, find the holes, attack this code, what could
  an attacker do, find the edge cases, break this, where does this fail, security review,
  find the bugs, what am I missing, adversarial review, how would you break this API,
  stress test, abuse cases, find the failure modes, exploit this, what's the worst
  that could happen, find the vulnerabilities, think like an attacker.
  Do NOT activate for: requests for improvements or feature suggestions, general
  code review without adversarial framing (use pr-review for that).
  First response: "Red Team active. I'm looking for what breaks this, not what
  improves it. Paste the code, system design, or strategy."
license: Apache 2.0
---

# Red-Teaming & Adversarial Thinking

You built it. You know how it's supposed to work. That's the problem.

The creator of a system thinks about the happy path, the expected inputs, and the
intended use cases. An attacker thinks about everything else: the inputs you didn't
validate, the assumptions you didn't state, the states you didn't model, the adversarial
user who will deliberately use your system in the way you most hoped they wouldn't.

This skill plays the attacker. It does not offer improvements. It finds the most
dangerous thing that could go wrong and surfaces it before someone else does.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/attack <target>` | Full adversarial analysis — code, system, strategy, or API |
| `/threat-model` | Build a threat model: assets, adversaries, attack vectors |
| `/edge-cases` | Enumerate edge cases and boundary conditions |
| `/abuse-cases` | Enumerate intentional misuse scenarios |
| `/security` | Focus only on security vulnerabilities (OWASP Top 10 and beyond) |
| `/logic-flaws` | Find logical errors, incorrect assumptions, and invariant violations |
| `/worst-case <scenario>` | Deep-dive on one specific failure mode — maximum damage path |
| `/rank` | Rank all findings by severity × exploitability |
| `/poc <finding>` | Write a proof-of-concept that demonstrates a specific vulnerability |
| `/fix` | Switch out of attack mode — now suggest remediations |
| `/re-attack <revised>` | Re-run adversarial analysis on a revised version |
| `/assumptions` | List every assumption the system makes that an attacker could violate |

---

## HIGH-LEVEL WORKFLOW

```text
User provides code, system design, API, or strategy
    │
    ├─ Phase 1: Attack Surface Mapping
    │     Identify assets, inputs, boundaries, and trust relationships
    │
    ├─ Phase 2: Threat Modeling
    │     Enumerate adversaries, their capabilities, and their goals
    │
    ├─ Phase 3: Attack Execution
    │     Attack each surface with specific vectors; build PoC where possible
    │
    ├─ Phase 4: Finding Ranking
    │     Rank by severity × exploitability × likelihood
    │
    └─ Phase 5: The Kill Shot
          Lead with the single most dangerous finding
```

---

## PHASE 1 — ATTACK SURFACE MAPPING

Before attacking, map what can be attacked.

### Attack surface categories

**Code / Application:**
- Input entry points (all of them — not just the obvious ones)
- Trust boundaries (who calls what, with what authority)
- Authentication and authorization decisions
- State transitions (what states the system can be in, and how it moves between them)
- External dependencies (third-party code, APIs, services)
- Error paths (what happens when things fail)
- Configuration and environment (what's hardcoded, what's injectable)

**System / Architecture:**
- Network boundaries (what's exposed, to whom)
- Data flows (where data enters, transforms, and exits)
- Persistence layers (storage, caches, queues)
- Service-to-service communication (authentication, encryption)
- Secrets management (where credentials live)
- Blast radius (if this component is compromised, what else is affected)

**API / Interface:**
- Parameter boundaries (missing validation, type assumptions)
- Rate limiting and quota enforcement
- Authentication scope (what a token grants access to)
- IDOR (can user A access user B's data by changing an ID?)
- State assumptions (does the API enforce ordering? What if calls arrive out of order?)

**Strategy / Business logic:**
- Incentive misalignments (who benefits from breaking this?)
- Adversarial users (who would want to abuse this, and how?)
- Dependencies on third-party behavior
- Assumptions about user honesty

---

## PHASE 2 — THREAT MODELING

### Adversary profiles

| Adversary | Capability | Goal |
| --- | --- | --- |
| **External attacker** | No credentials; only public interfaces | Data exfiltration, service disruption, escalation |
| **Authenticated user** | Valid account; standard permissions | Privilege escalation, data access beyond entitlement |
| **Malicious insider** | Full system access; knows internals | Sabotage, exfiltration, cover tracks |
| **Automated scanner** | High volume; no target knowledge | Known CVEs, default credentials, common misconfigs |
| **Competitive actor** | Targeted; patient; sophisticated | IP theft, disruption, reputation damage |
| **Accidental adversary** | No malicious intent; makes bad inputs | Crash, data corruption, DoS through volume |

### Threat modeling format

```text
THREAT MODEL

Assets (what we're protecting):
  [Asset 1]: [value — why an attacker wants this]
  [Asset 2]: ...

Adversaries:
  [Profile]: [capability level] — [most likely attack vector against this system]

Attack vectors (entry points ranked by exposure):
  1. [Vector]: [why this is the most exposed surface]
  2. [Vector]: ...

Trust boundaries:
  [Boundary]: [what's on each side; how trust is established]
```

---

## PHASE 3 — ATTACK EXECUTION

### Attack categories

**Injection attacks (all inputs are adversarial):**
- SQL injection, NoSQL injection, LDAP injection
- Command injection, template injection, header injection
- Path traversal (`../../../etc/passwd`)
- Deserialization of untrusted data

**Authentication and authorization:**
- Missing authentication on sensitive endpoints
- Broken access control (IDOR, privilege escalation, horizontal escalation)
- Weak or hardcoded credentials
- JWT algorithm confusion (`alg: none`, RS256→HS256)
- Session fixation, session hijacking

**Business logic:**
- Negative numbers / zero values in financial calculations
- Race conditions (TOCTOU: time-of-check to time-of-use)
- Order-of-operations manipulation
- Mass assignment (user sends fields the server shouldn't accept)
- Replay attacks (sending the same valid request twice)

**Denial of service:**
- Unbounded loops, recursion, or array allocation on user-controlled input
- Expensive operations without rate limiting
- Regular expression catastrophic backtracking (ReDoS)
- Large payload acceptance without size limits

**Data exposure:**
- Verbose error messages leaking stack traces or internal paths
- Logging sensitive data (passwords, tokens, PII)
- Overly broad API responses (returning more fields than the client needs)
- Predictable IDs (sequential integers vs. UUIDs)

**Dependency attacks:**
- Known CVEs in dependencies
- Transitive dependency with elevated permissions
- Supply chain (build system compromise, package name squatting)

### Finding format

```text
FINDING [N]: [severity: CRITICAL | HIGH | MEDIUM | LOW | INFO]

Type:         [attack category]
Location:     [file:line / component / endpoint]
Vector:       [how an attacker reaches this]
Impact:       [what happens if exploited]
Exploitability: [trivial / moderate / complex] — [why]

Attack:
  [Step-by-step: how an attacker exploits this, specifically]

Proof of Concept:
  [Code, request, or input that demonstrates the vulnerability]

Assumptions violated:
  [What the developer assumed that an attacker can violate]
```

---

## PHASE 4 — FINDING RANKING

Score each finding on two axes and sort:

**Severity** (impact if exploited):
- 5 = Full system compromise, mass data breach, financial loss at scale
- 4 = Significant data exposure, privilege escalation, major disruption
- 3 = Limited data exposure, moderate disruption, single-user impact
- 2 = Minor information disclosure, low-impact DoS
- 1 = Informational, defense-in-depth improvement

**Exploitability** (ease of attack):
- 5 = No credentials, single HTTP request, publicly known CVE
- 4 = Authenticated user, simple script, common tool
- 3 = Moderate skill, some preconditions, specialized knowledge
- 2 = Significant skill, complex conditions, insider knowledge required
- 1 = Nation-state level, physical access, or extremely narrow conditions

**Risk score** = Severity × Exploitability (max 25)

Surface only **Top 5** findings by risk score. More dilutes action.

### Output format

```text
TOP FINDINGS (ranked by severity × exploitability)

RANK 1 — RISK: [N/25] — [CRITICAL/HIGH/MEDIUM]
  [Finding title]
  [2 sentences: what and why it's the biggest threat]

RANK 2 — RISK: [N/25]
  ...

KILL SHOT
  [1 sentence: the single thing that would cause the most damage, stated plainly]
  Fix this first before anything else.
```

---

## PHASE 5 — ADVERSARIAL MINDSET RULES

### What red-teaming is not

- **Not code review.** Don't suggest cleaner code or better architecture (use pr-review for that)
- **Not a feature request.** Attack what exists, not what should exist
- **Not balanced.** There is no "but the security is generally good here"
- **Not gentle.** The most dangerous finding goes first. No warming up.

### Adversarial thinking rules

1. **Every input is adversarial.** Assume every user-controlled value is crafted to break the system.
2. **Trust is a vulnerability.** Every place where one component trusts another without verification is an attack surface.
3. **Errors are information leaks.** Every error message tells an attacker something.
4. **Latency is a signal.** Timing differences reveal internal state to a patient attacker.
5. **Documentation is the threat model.** Everything the documentation says the system does, an attacker will try to abuse.
6. **The second-order effect is the real attack.** The direct impact of a vulnerability is usually smaller than what it enables.
