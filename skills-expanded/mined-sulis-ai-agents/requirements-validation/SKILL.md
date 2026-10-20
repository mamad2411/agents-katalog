---
name: requirements-validation
description: "Checks a specification for completeness and reports gaps."
---

# Requirements Validation

When invoked, run the requirements completeness spiral on a specification folder.

If arguments are provided, treat them as the path to the specification folder.
If no path is provided, use the most recently modified folder in `.specifications/`.

Execute five verification perspectives, run up to 3 passes, fix small gaps inline,
surface larger gaps to the user. Produce `COMPLETENESS_REPORT.md` with a PASS or
GAPS_FOUND verdict.

---

## Spiral Mechanism

The completeness assessment uses a spiral approach rather than a single-pass checklist.

**The verification perspectives** examine the specification from different angles:
1. Requirement Traceability — Can every goal be traced through use cases to testable requirements?
2. Integration Completeness — Is every external system specified well enough to build against?
3. NFR Coverage — Are non-functional requirements measurable and comprehensive?
4. Tree Completeness — Are all primitive tree nodes adequately specified and represented in artifacts?
5. Referential Integrity — Does the content of generated artifacts accurately reflect the design decisions and assumptions from facilitation?
6. Term Consistency — Does every recurring noun in the artifacts reconcile with GLOSSARY.md (the locked vocabulary from Phase 3.5 Disambiguation Sweep)?
7. Adversarial Coverage — Does every security-sensitive use case have a corresponding misuse case (or explicit "no plausible adversary" note), and does every misuse case have a defined system response?
8. Verification Posture (**P-VER**) — Does every specification artifact (SRD + TDD + WP set) carry a populated `## Verification Plan` section per ADR-001's literal heading, with the six required subsections drawn from the canonical 20-question set, and every named integration carrying its `existing` / `deferred` / `out-of-scope` classification? Invoked as a rubric pass against [`plugins/sulis/references/decompose-validation-rubric.md`](../../references/decompose-validation-rubric.md) §Phase 9. Canonical question set: [`plugins/sulis/references/standards/VERIFICATION_QUESTIONS.md`](../../references/standards/VERIFICATION_QUESTIONS.md). Cross-reference: [`ADR-001`](../../../../.architecture/verification-by-design/adrs/ADR-001-section-name-verification-plan.md) fixes the section name.

**Fix-as-you-go via AAF triage (MUST).** Every gap found by every perspective passes
through the AAF-01 triage from `plugins/sulis/references/audience-adapted-framing-standard.md`
before becoming a user question. The default posture is *fix inline and journal-record*;
only gaps that survive AAF-01 step 1 + step 2 + step 3 become user-facing questions.

- **Step-1-silent gaps** (artifact maintenance, missing diagrams for already-specified
  entities, identifier renumbering, glossary additions, state-machine internals, wording
  cleanup) → fix inline, record under `## Auto-Resolved` in COMPLETENESS_REPORT.md with
  the AAF-01 step that fired.
- **Step-2-silent gaps** (technical-only trade-offs with no plain-English framing) →
  apply the convention per CP-01..CP-05, record under `## Auto-Resolved`.
- **Step-3 survivors** (genuine business or UX gaps the founder can answer) → list
  under `## User Input Required` in plain English, with the corresponding triage trace
  written to `EXPLORATION_JOURNAL.md` § `Triage Trace` per AAF-07.

**Per-perspective output contract (AAF-06).** Each perspective emits results as three
explicit lists, never as "I found N things, want me to fix them all?":

```
## Perspective N — {name}
### Already done (fixed inline)
- {gap} — {one-line rationale citing AAF-01 step that fired}

### Done with announcement
- {gap} — applied {convention}; rationale: {one line}

### Need your input
- {plain-English question, no IDs, no jargon}
```

**Max 3 passes:** The spiral runs up to 3 times. Each pass re-examines all eight perspectives.
Fixes applied in pass N are verified in pass N+1.

**Exit conditions:**
When the verdict is **PASS**, the analyst's `Phase Auto-Progression (MUST)` rule fires:
all step-1-silent cleanups are taken automatically (wording, line-count drift,
formatting), Phase 6 Handover Preparation begins, and the next command
(`/sulis:draft-architecture .specifications/{name}/`) is surfaced in the **action-then-report
shape**:

> *"PASS confirmed. Cleaned up {N} items in COMPLETENESS_REPORT.md. HANDOFF_TO_SEA.md
> ready. Starting `/sulis:draft-architecture`."*

**Never** as a permission-theater closure:

> ✗ *"PASS. Recommend `/sulis:draft-architecture` as the natural next step. Want me to proceed?"*

This is an AAF-08 violation. The validation skill does not surface a "proceed?"
question after PASS. Auto-progression is the analyst's responsibility (see
`plugins/sulis/agents/requirements-analyst.md` → Phase Auto-Progression rule); the
validation skill simply reports the verdict and identifies the cleanup items as
Auto-Resolved entries.

SEA reads `SRD.md`, `NFR.md`, and `PRIMITIVE_TREE.jsonld` directly and produces a
hardened Technical Design Document, ADRs, and atomic Work Packages with
Red-Green-Blue Definitions of Done. A passing SRD specification is the input SEA
is built to consume.

- **PASS** — All traces complete, all integrations specified, all NFR categories covered
  with measurable requirements, all tree nodes represented with attack patterns addressed,
  all artifacts semantically consistent with facilitation decisions, all recurring terms
  reconcile with the glossary, every security-sensitive use case has adversarial
  coverage with defined system responses, **every leaf in PRIMITIVE_TREE.jsonld carries
  a `leaf_category`, `RECONCILIATION_MAP.md` has zero unresolved-gap or
  undisposed-orphan rows, the Reconciliation Cycle Stack is closed**, **and P-VER
  passes against every specification artifact** (the eight failure modes 9.01..9.08
  from the rubric's Phase 9 each pass or are grandfathered per ADR-002's merge-date
  constant). No flags remain.
- **GAPS_FOUND** — After 3 passes, some gaps remain that require user input or decisions
  that cannot be made by the agent. All remaining gaps are documented with their flags.
  **A P-VER FAIL (any of the eight failure modes in
  [`decompose-validation-rubric.md`](../../references/decompose-validation-rubric.md)
  §Phase 9) collapses the overall verdict to GAPS_FOUND** — P-VER is a MUST-blocking
  rubric phase per FR-009, and the overall verdict pass-through is mechanical: any
  P-VER failure mode that fires on the artifact set produces a GAPS_FOUND verdict
  regardless of how the other perspectives score. The reciprocal also holds: a P-VER
  PASS does not by itself elevate the overall verdict to PASS — the other seven
  perspectives must also pass.

**Sufficiency test:** The guiding question for every check is: "Could a development team
implement this without making undocumented assumptions?" If the answer is no, a flag is raised.

---

## Perspective 1: Requirement Traceability

For each element in the SRD, verify that it connects to the elements above and below it
in the traceability chain.

### Checks

**Goal to Use Case:**
Every goal stated in the SRD must trace to at least one use case that, when implemented,
advances that goal.
- Flag: `UNTRACEABLE_GOAL` — A goal exists with no use case connected to it.
- Fix strategy: Review use cases to find implicit connections, or flag for user to
  identify which use case serves this goal.

**Use Case to Diagram:**
Every use case with a multi-step flow must have at least one supporting diagram (process
flow or sequence diagram) that visualises the flow.
- Flag: `UNDIAGRAMMED_USE_CASE` — A use case has a described flow but no diagram.
- Fix strategy: If the basic flow is described in enough detail, generate the diagram
  immediately. Record as a fix.

**Integration to Sequence Diagram:**
Every integration with an external system must have a sequence diagram showing the
interaction pattern, including error scenarios.
- Flag: `UNDIAGRAMMED_INTEGRATION` — An integration is described but has no sequence diagram.
- Fix strategy: If protocol, data format, and error handling are specified, generate the
  diagram. Otherwise, flag for user.

**Lifecycle Entity to State Diagram:**
Every entity that has distinct lifecycle states (e.g., order: draft, submitted, processing,
completed, cancelled) must have a state diagram.
- Flag: `MISSING_STATE_MODEL` — An entity has lifecycle states described in text but no
  state diagram.
- Fix strategy: If states and transitions are described, generate the diagram. Record as fix.

**Feature to Functional Requirement:**
Every feature must have at least one functional requirement with acceptance criteria that
could be used to write a test.
- Flag: `UNTESTABLE_FEATURE` — A feature is described but has no functional requirement
  with acceptance criteria.
- Fix strategy: If the feature description is detailed enough, draft the requirement and
  acceptance criteria. Flag for user verification.

---

## Perspective 2: Integration Completeness

For each external system referenced in the SRD, verify that the integration is specified
completely enough to implement.

### Checks Per Integration

**Protocol specified?**
The communication protocol must be explicitly stated: REST, GraphQL, gRPC, webhook,
message queue (RabbitMQ, Kafka, SQS), SMTP, file transfer (SFTP, S3), or other.
- Flag: `AMBIGUOUS_PROTOCOL` — The integration mentions communication but does not specify
  the protocol.

**Authentication specified?**
How the system authenticates with the external service must be stated: API key, OAuth 2.0
(which flow), bearer token, mutual TLS, certificate, basic auth, or no authentication.
- Flag: `UNDERSPECIFIED_INTEGRATION` — Protocol is specified but authentication is not.

**Error handling specified?**
What happens when the integration fails must be defined:
- Timeout duration (how long to wait before giving up)
- Retry policy (how many retries, backoff strategy)
- Fallback behaviour (what the system does if the integration is unavailable)
- Circuit breaker (whether to stop trying after repeated failures)
- Flag: `MISSING_ERROR_HANDLING` — No error handling specified for this integration.

**Data format specified?**
The format of data exchanged must be defined: JSON (with schema or example), XML,
protobuf, CSV, binary, or other.
- Flag: `UNDERSPECIFIED_INTEGRATION` — Data format not specified.

**Sync/async specified?**
Whether the interaction is synchronous (request-response, caller waits) or asynchronous
(fire-and-forget, callback, polling) must be stated.
- Flag: `UNDERSPECIFIED_INTEGRATION` — Timing model not specified.

**Rate limits specified?**
Whether the external system imposes rate limits, and how the system handles them, must
be stated: requests per second/minute, backpressure strategy (queue, shed, throttle),
and monitoring/alerting for approaching limits.
- Flag: `UNDERSPECIFIED_INTEGRATION` — Rate limits not addressed.

### Fix Strategy

If the SRD contains enough context to infer a missing detail (e.g., "calls the Stripe API"
implies REST + JSON), the agent fills it in and records the fix. If the detail cannot be
inferred, the gap is flagged for user review.

---

## Perspective 3: NFR Coverage

Verify that non-functional requirements are comprehensive and measurable. The specification
must include at least one measurable requirement in each of the following categories.

### Minimum NFR Categories

**Performance:**
Response time, throughput, or latency targets with specific thresholds.
- Good: "API responses < 200ms at p95 under normal load"
- Bad: "The system should be fast"
- Flag: `UNMEASURABLE_NFR` — Requirement uses an adjective instead of a threshold.
- Flag: `MISSING_NFR_CATEGORY` — No performance requirements specified.

**Scalability:**
Concurrent user targets, data volume expectations, or growth rate projections.
- Good: "Support 10,000 concurrent users with < 5% degradation"
- Bad: "The system should scale"
- Flag: `UNMEASURABLE_NFR` — No specific scale targets.
- Flag: `MISSING_NFR_CATEGORY` — No scalability requirements specified.

**Security:**
Authentication method, authorisation model, encryption requirements, compliance frameworks.
- Good: "All API endpoints require OAuth 2.0 bearer tokens. Data encrypted at rest using AES-256."
- Bad: "The system should be secure"
- Flag: `UNMEASURABLE_NFR` — Security described as an adjective.
- Flag: `MISSING_NFR_CATEGORY` — No security requirements specified.

**Availability:**
Uptime SLA, recovery time objective (RTO), recovery point objective (RPO).
- Good: "99.9% monthly uptime. RTO: 4 hours. RPO: 1 hour."
- Bad: "The system should always be available"
- Flag: `UNMEASURABLE_NFR` — No specific availability targets.
- Flag: `MISSING_NFR_CATEGORY` — No availability requirements specified.

**Data:**
Retention policy, backup frequency, privacy requirements (GDPR, CCPA, HIPAA).
- Good: "User data retained for 7 years. Daily backups with 30-day retention. GDPR compliant — right to deletion within 30 days."
- Bad: "Data should be backed up"
- Flag: `UNMEASURABLE_NFR` — No specific data management targets.
- Flag: `MISSING_NFR_CATEGORY` — No data requirements specified.

### Fix Strategy

- `UNMEASURABLE_NFR`: If context exists in the SRD to infer a threshold, propose one and
  flag for user confirmation. If not, flag for user input.
- `MISSING_NFR_CATEGORY`: Flag for user. The agent cannot invent NFRs without user input.

---

## Perspective 4: Tree Completeness

When a PRIMITIVE_TREE.jsonld exists in the specification folder, verify that the primitive
tree and the SRD artifacts are mutually consistent.

If no PRIMITIVE_TREE.jsonld exists, skip this perspective entirely.

### Checks

**Attack Pattern Coverage:**
For each validated node, check that every attack pattern defined for its node type has
been evaluated against the SRD content. An attack pattern is "addressed" when the SRD
contains a specification element that answers the question the pattern poses.
- Flag: `UNADDRESSED_ATTACK_PATTERN` — A validated node has attack patterns that were
  never addressed during facilitation or in the SRD.
- Fix strategy: If the SRD contains enough context to address the attack pattern, add
  the specification element and record the fix. Otherwise, flag for user input.

**Active Invalidation Signals:**
For each node (any health status), check whether any invalidation signals defined for
its node type are currently active — i.e., the condition described by the signal is true
based on the SRD content.
- Flag: `ACTIVE_INVALIDATION` — An invalidation signal condition is met. Include the
  specific evidence that triggered it.
- Fix strategy: If the invalidation can be resolved from conversation context (e.g., by
  adding a missing error path), fix inline. Otherwise, flag for user input.

**Artifact Representation:**
For each validated node, check that it appears in at least one SRD artifact matching
its `artifactAffinity`. A node with affinity `["use-case", "data-flow"]` must appear in
either the use case diagrams or the data flow diagrams (or both).
- Flag: `UNREPRESENTED_NODE` — A validated node has no representation in any artifact
  matching its affinity.
- Fix strategy: If the facilitation record contains enough information to add the node
  to the appropriate artifact, do so and record the fix. Otherwise, flag for user input.

**Risk-Accepted Documentation:**
For each node with health_status "accepted-as-risk", verify that the risk justification
is documented.
- Flag: `RISK_ACCEPTED_NODE` — Informational flag. Lists the node and its risk
  justification. Does not block PASS verdict.

### Fix Strategy

- `UNADDRESSED_ATTACK_PATTERN`: Small gaps (single missing detail that can be inferred
  from context) fixed inline. Large gaps (require domain knowledge not in the
  facilitation record) surfaced one at a time to the user.
- `ACTIVE_INVALIDATION`: Always surface to the user — invalidation signals indicate
  structural issues that require domain judgement.
- `UNREPRESENTED_NODE`: Generate the missing artifact element if facilitation context
  is sufficient. Otherwise, flag for user.

---

## Perspective 5: Referential Integrity

Verify that the content of generated artifacts is semantically consistent with what was
decided during facilitation. Perspectives 1-4 check structural completeness (does every
goal have a use case?). This perspective checks content accuracy (does the use case
accurately describe what was decided?).

The authoritative source of truth is the exploration journal — specifically its recorded
answers, design decisions, assumption register, and context ledger entries. When an
artifact contradicts the journal, the artifact is wrong.

### Checks

**Use Case Accuracy:**
For each use case in the SRD and use-cases.md, verify:
- The actor matches who actually performs the action per facilitation (not who was initially
  assumed). If a design decision changed the actor (e.g., from user-initiated to
  system-automated), the use case must reflect the final decision.
- The trigger and preconditions are consistent with the agreed interaction model.
- The basic flow matches the process agreed during facilitation, not an earlier version
  that was subsequently revised.
- Flag: `STALE_USE_CASE` — A use case reflects an earlier version of a design decision
  that was revised during facilitation.
- Fix strategy: Rewrite the use case to match the current design decision from the journal.
  Record the specific journal entry that establishes the correct version.

**Design Decision Propagation:**
For each design decision recorded in the exploration journal, verify that it is reflected
in every artifact it affects. A design decision that changes the system's interaction
model, data flow, or architectural shape should be visible in use cases, diagrams, and
requirements — not just the artifact where it was first discussed.
- Flag: `UNPROPAGATED_DECISION` — A design decision is reflected in some artifacts but
  not all artifacts it logically affects.
- Fix strategy: Identify which artifacts are affected by the decision and update them.
  Record each fix with the journal entry that establishes the decision.

**Assumption Consistency:**
For each active assumption in the assumption register, verify that no artifact contains
content that contradicts it. For each invalidated assumption, verify that no artifact
still depends on it.
- Flag: `ASSUMPTION_CONTRADICTION` — An artifact contains content that contradicts an
  active assumption, or still depends on an invalidated assumption.
- Fix strategy: If the assumption is active, fix the artifact. If the assumption is
  invalidated, update all dependent artifacts to reflect the current understanding.

**Glossary Conformance:**
For each term in GLOSSARY.md, verify that the term is used consistently across all
artifacts. If a glossary term was redefined during facilitation (e.g., "workspace" changed
from meaning a UI container to a self-contained domain unit), all artifacts must use the
current definition.
- Flag: `GLOSSARY_DRIFT` — An artifact uses a term in a way that contradicts or predates
  the current glossary definition.
- Fix strategy: Update the artifact to use the term consistently with the glossary.

### Fix Strategy

- `STALE_USE_CASE`: Always fix inline — the correct version exists in the journal.
- `UNPROPAGATED_DECISION`: Fix inline where the decision's implications are clear. Flag
  for user when the decision's impact on a specific artifact is ambiguous.
- `ASSUMPTION_CONTRADICTION`: Fix inline for active assumptions. For invalidated
  assumptions, surface to the user if the correct replacement is unclear.
- `GLOSSARY_DRIFT`: Always fix inline — the glossary is the authoritative definition.

---

## Perspective 6: Term Consistency

Enforce the vocabulary locked during Phase 3.5 (Disambiguation Sweep). The glossary is
the authoritative source — every recurring noun in artifacts must reconcile against it.

This perspective overlaps with `GLOSSARY_DRIFT` in Perspective 5 but operates at a
broader scope: Perspective 5 catches *contradiction* with the glossary; Perspective 6
catches *absence from* the glossary and *synonym reuse* across artifacts.

### Checks

**Undefined Terms:**
For each recurring noun in SRD.md, NFR.md, MISUSE_CASES.md, and the diagrams, check
whether the term appears in GLOSSARY.md as either a preferred term or in the
`Also Known As` column. Generic words (the, system, user when defined elsewhere, etc.)
do not warrant a glossary entry.
- Flag: `UNDEFINED_TERM` — A domain-specific recurring noun is used in artifacts but
  not present in GLOSSARY.md.
- Fix strategy: If the term's meaning is clear from the journal, add it to GLOSSARY.md
  with a precise definition and record the fix. Otherwise, flag for user input.

**Deprecated Synonym Use:**
For each preferred term in GLOSSARY.md, check that its deprecated synonyms (the
`Also Known As` entries) do not appear in artifacts. If they do, the artifact is using
the wrong form.
- Flag: `DEPRECATED_SYNONYM` — An artifact uses a synonym that was deprecated in
  favour of a preferred term during Phase 3.5.
- Fix strategy: Replace the deprecated synonym with the preferred term throughout the
  artifact. Always fix inline.

**Cross-Artifact Term Conflict:**
For each recurring noun used across multiple artifacts, verify that all artifacts use
the same form. If artifact A uses `order` and artifact B uses `request` for what the
glossary identifies as the same concept, both artifacts must converge on the preferred
term.
- Flag: `CROSS_ARTIFACT_TERM_CONFLICT` — The same concept is named differently in
  different artifacts.
- Fix strategy: Apply the preferred term per the glossary. Always fix inline.

**Missing Disambiguation:**
For each pair of terms in GLOSSARY.md's `NOT the Same As` column, verify that no
artifact uses them interchangeably. If artifacts conflate two terms that the glossary
distinguishes, flag it.
- Flag: `CONFLATED_DISTINCT_TERMS` — An artifact uses two terms interchangeably that
  the glossary marks as distinct concepts.
- Fix strategy: Surface to user — this is usually a content error in the artifact, not
  a substitution error.

### Fix Strategy

- `UNDEFINED_TERM`: Add to glossary if meaning is clear from journal; otherwise flag.
- `DEPRECATED_SYNONYM`: Always fix inline.
- `CROSS_ARTIFACT_TERM_CONFLICT`: Always fix inline.
- `CONFLATED_DISTINCT_TERMS`: Always surface to user.

---

## Perspective 7: Adversarial Coverage

Enforce the negative-requirements work from Phase 3.6 (Adversarial Sweep). The
specification must surface the system's hostile-actor behaviour, not just its
happy-path behaviour.

### Checks

**Security-Sensitive Use Cases Without Misuse Cases:**
Identify use cases that touch authentication, authorisation, payment, data
modification (write/delete), external integration, or PII handling. For each, verify
either (a) at least one misuse case in MISUSE_CASES.md references this use case in
its `Targets` field, or (b) the exploration journal records an explicit "no plausible
adversary" note under `## Adversarial Sweep` for this use case.
- Flag: `UNCOVERED_SECURITY_USE_CASE` — A security-sensitive use case has no misuse
  case and no journal note explaining why.
- Fix strategy: If the journal contains enough context to generate a misuse case
  (abusive actor, abuse pattern, required system response), generate it. Otherwise,
  flag for user input.

**Misuse Cases Without System Response:**
For each misuse case in MISUSE_CASES.md, verify the `System response (REQUIRED)` field
is populated with a concrete negative requirement (MUST refuse, MUST detect, MUST log,
MUST rate-limit, MUST alert, etc.).
- Flag: `MISUSE_CASE_NO_RESPONSE` — A misuse case lacks a defined system response.
- Fix strategy: Surface to user — the response is the load-bearing requirement; the
  agent cannot invent it without domain authority.

**Negative Requirements Not Reflected in SRD:**
For each misuse case's system response, verify that the corresponding negative
requirement appears in SRD.md (typically under a `Negative Requirements` section of
the affected use case).
- Flag: `UNPROPAGATED_NEGATIVE_REQUIREMENT` — A misuse case has a system response but
  SRD.md does not reference it.
- Fix strategy: Add the negative requirement to the affected use case's specification.
  Always fix inline.

**Missing Pre-mortem:**
Verify that EXPLORATION_JOURNAL.md contains a `## Adversarial Sweep` section with the
pre-mortem question recorded and at least one user-supplied failure scenario.
- Flag: `MISSING_PREMORTEM` — The adversarial sweep was skipped or the pre-mortem step
  was not run.
- Fix strategy: If the system has any security-sensitive primitives, flag as
  `GAPS_FOUND` and surface to user. If the system is genuinely scope-skip (read-only
  public dashboard with no auth, integrations, or sensitive data), record the skip
  rationale in the journal and accept.

**STRIDE Categories Unconsidered:**
For each authenticated action, external integration, and sensitive data-store, verify
that the journal records which STRIDE categories were considered (and which were N/A
with reason). If a primitive has none recorded, the sweep was incomplete for that
primitive.
- Flag: `STRIDE_GAPS` — A security-sensitive primitive has no STRIDE consideration in
  the journal.
- Fix strategy: If the primitive's threat surface is clear from the SRD content, run
  STRIDE-lite inline and record the result. Otherwise, surface to user.

### Fix Strategy

- `UNCOVERED_SECURITY_USE_CASE`: Fix inline if journal context is sufficient; otherwise flag.
- `MISUSE_CASE_NO_RESPONSE`: Always surface to user.
- `UNPROPAGATED_NEGATIVE_REQUIREMENT`: Always fix inline.
- `MISSING_PREMORTEM`: Surface to user unless explicit skip rationale exists.
- `STRIDE_GAPS`: Fix inline if SRD content is sufficient; otherwise surface to user.

---

## Perspective 8: Two-Model Reconciliation

This perspective enforces that the Two-Model OODA Reconciliation rule (in
`plugins/sulis/agents/requirements-analyst.md` → Section 2) has run to closure. The rule
recursively decomposes every requirement until it terminates at an irreducible-leaf
category, reconciles the Domain Model (what's needed) against the Code Model (what
exists), and produces `.specifications/{project}/RECONCILIATION_MAP.md` plus the
`## Reconciliation Cycle Stack` in `EXPLORATION_JOURNAL.md`.

Without this perspective, an SRD can pass all other perspectives while shipping with
hidden prerequisite gaps (UC-X requires UC-Y, but UC-Y was never specified) or with
orphan code that has no traceable requirement.

### Checks

For every leaf node in `PRIMITIVE_TREE.jsonld`:

- **`UNCATEGORISED_LEAF`** — A leaf node (zero outgoing depends-on edges to
  non-terminated nodes) does not have `leaf_category` set to one of the five values
  (`external-system | genesis-bootstrap | primitive-component | external-spec |
  existing-impl`). Fix strategy: if Prior-Art Check or CP-01 lookup resolves it
  from context, fix inline by setting the category and recording the resolution in
  RECONCILIATION_MAP.md; otherwise surface to user with the orphan-question template.

For every row in `RECONCILIATION_MAP.md`:

- **`UNRESOLVED_GAP`** — A row has `Category: gap` with `Resolution: unresolved`
  or blank. Fix strategy: surface to user as a missing UC and either draft it
  inline or accept it as out-of-scope with explicit rationale.
- **`UNDISPOSED_ORPHAN`** — A row has `Category: orphan` without a disposition
  in the Resolution column (referenced / out-of-scope / deprecated). Fix
  strategy: surface the orphan-question to user; default to `out-of-scope` with
  a journal note if no response.

For `EXPLORATION_JOURNAL.md`:

- **`OPEN_CYCLE_FRAME`** — The `## Reconciliation Cycle Stack` section contains
  frames with `status: open`. Recursion did not terminate. Fix strategy: surface
  to user as un-terminated decomposition; either resolve the cycle or explicitly
  terminate with `leaf_category: primitive-component` and a rationale note.

### Fix Strategy by Code

- `UNCATEGORISED_LEAF`: Fix inline if Prior-Art Check resolves; otherwise surface.
- `UNRESOLVED_GAP`: Always surface to user.
- `UNDISPOSED_ORPHAN`: Always surface to user.
- `OPEN_CYCLE_FRAME`: Always surface to user.

---

## Content Quality Verification

In addition to the five requirement perspectives, verify that all generated artifacts
comply with the Content Quality Standard (CQ-01 through CQ-06):

- **CQ-01:** Every artifact over 50 lines has a summary section
  - Flag: `CQ_MISSING_SUMMARY` — Artifact exceeds 50 lines with no summary section.
- **CQ-02:** Detail sections use stable identifiers for traceability
  - Flag: `CQ_MISSING_IDENTIFIERS` — Detail section lacks stable identifiers.
- **CQ-03:** Prose paragraphs vary sentence rhythm (no 3+ consecutive same-band sentences)
  - Flag: `CQ_RHYTHM_VIOLATION` — Three or more consecutive same-band sentences.
- **CQ-04:** Prose meets plain language baseline (Flesch-Kincaid Grade Level targets per
  audience: ≤10 for user-facing, ≤14 for technical)
  - Flag: `CQ_READABILITY` — Prose exceeds grade level target for its audience.
- **CQ-05:** No AI-tell anti-patterns in prose (filler phrases, excessive hedging, empty emphasis)
  - Flag: `CQ_AI_TELL` — AI-generated content markers detected.
- **CQ-06:** Content quality verified before finalising (rhythm check, readability scoring,
  anti-pattern scan applied to all prose sections)
  - Flag: `CQ_UNVERIFIED` — Artifact finalised without content quality verification.

### Fix Strategy

- `CQ_MISSING_SUMMARY`: Generate summary from artifact content. Always fix inline.
- `CQ_MISSING_IDENTIFIERS`: Add stable identifiers to detail sections. Always fix inline.
- `CQ_RHYTHM_VIOLATION`: Rewrite affected paragraph to vary sentence length. Fix inline.
- `CQ_READABILITY`: Simplify prose to meet grade level target. Fix inline.
- `CQ_AI_TELL`: Rewrite affected sentences to remove filler/hedging. Fix inline.
- `CQ_UNVERIFIED`: Run the verification checks. Always fix inline.

---

## Output Format

The completeness assessment produces `COMPLETENESS_REPORT.md` in the specification folder.
**Every perspective MUST emit three lists per AAF-06**: gaps fixed inline under
`## Auto-Resolved`, gaps decided with announcement under `## Done with announcement`,
and gaps requiring user input under `## User Input Required`. Each `## User Input
Required` entry must have a corresponding row in `EXPLORATION_JOURNAL.md` § `Triage
Trace` per AAF-07.

```
REQUIREMENTS COMPLETENESS ASSESSMENT
Specification: {name}
Date: {date}
Passes completed: {1|2|3}

VERDICT: PASS | GAPS_FOUND

## Auto-Resolved (step-1-silent and step-2-silent gaps fixed inline)

- [Perspective N] {flag} {gap description} — fixed by {action}; AAF-01 step {1|2} fired because {one-line rationale}
- ...

## Done with announcement (convention applied; user can audit and override)

- [Perspective N] {flag} {gap} — applied {convention from CP-01..CP-05}; rationale: {one line}
- ...

## User Input Required (step-3 survivors, plain English)

- [Perspective N] {plain-English question with no IDs, no jargon}
  Triage trace: t{NN} — step 1 pass / step 2 pass / step 3 ask
- ...

--- PERSPECTIVE 1: REQUIREMENT TRACEABILITY ---
[COMPLETE] Goal G-01 → UC-01, UC-02 → sequence-diagram SD-01, process-flow PF-01
[UNTRACEABLE_GOAL] Goal G-03 — no use case traces to this goal
[UNDIAGRAMMED_USE_CASE] UC-05 — has basic flow but no diagram
[MISSING_STATE_MODEL] Order entity — states described in UC-02 but no state diagram
[UNTESTABLE_FEATURE] F-07 — feature described but no functional requirement with acceptance criteria

--- PERSPECTIVE 2: INTEGRATION COMPLETENESS ---
[COMPLETE] Stripe integration — protocol, auth, errors, format, sync all specified
[UNDERSPECIFIED_INTEGRATION] Email service — protocol specified but no error handling
[AMBIGUOUS_PROTOCOL] Analytics service — "sends data" but protocol not specified
[MISSING_ERROR_HANDLING] Payment webhook — no timeout or retry policy specified

--- PERSPECTIVE 3: NFR COVERAGE ---
[COMPLETE] Performance — "API responses < 200ms at p95" (measurable)
[COMPLETE] Security — "OAuth 2.0 + AES-256 at rest" (measurable)
[MISSING_NFR_CATEGORY] Scalability — no requirements specified
[UNMEASURABLE_NFR] Availability — "system should be highly available" (adjective, not threshold)
[MISSING_NFR_CATEGORY] Data — no retention or backup requirements specified

--- PERSPECTIVE 4: TREE COMPLETENESS ---
[COMPLETE] node-user (domain-entity) — all attack patterns addressed, represented in use-cases.md
[UNADDRESSED_ATTACK_PATTERN] node-place-order (action) — "What happens if this action fails mid-execution?" not addressed
[ACTIVE_INVALIDATION] node-order-lifecycle (state-machine) — "cancelled" state has no outgoing transitions and is not marked terminal
[UNREPRESENTED_NODE] node-auth-policy (policy) — validated but not represented in any artifact matching affinity [business-rule, nfr]
[RISK_ACCEPTED_NODE] node-analytics (integration) — accepted-as-risk: "Analytics integration deferred to post-MVP"

--- PERSPECTIVE 5: REFERENTIAL INTEGRITY ---
[COMPLETE] UC-01 — actor, trigger, flow consistent with journal design decisions
[STALE_USE_CASE] UC-02 — actor is "User" but design decision DD-04 (turn 18) changed to system-automated provisioning
[UNPROPAGATED_DECISION] DD-03 (authorization-driven workspace access) — reflected in UC-01 but not in sequence-diagram SD-02
[ASSUMPTION_CONTRADICTION] A-02 (single-tenant) invalidated at turn 22, but NFR-12 still references single-tenant deployment model
[GLOSSARY_DRIFT] "workspace" in process-flow PF-01 uses original definition, not current glossary definition (updated turn 15)

--- PERSPECTIVE 6: TERM CONSISTENCY ---
[COMPLETE] "order", "approver", "submission" — all preferred terms appear consistently across SRD.md, MISUSE_CASES.md, and diagrams
[UNDEFINED_TERM] "settlement" — used 4 times in NFR.md but not in GLOSSARY.md
[DEPRECATED_SYNONYM] sequence-diagram SD-03 uses "request" — glossary marks this as deprecated; preferred term is "order"
[CROSS_ARTIFACT_TERM_CONFLICT] SRD.md uses "customer" but MISUSE_CASES.md uses "account holder" for the same actor (glossary preferred: "customer")
[CONFLATED_DISTINCT_TERMS] process-flow PF-02 uses "approve" and "authorise" interchangeably — glossary marks these as distinct concepts

--- PERSPECTIVE 7: ADVERSARIAL COVERAGE ---
[COMPLETE] UC-01 (place order) — covered by MUC-01 (replay payment webhook) and MUC-03 (fraudulent input)
[UNCOVERED_SECURITY_USE_CASE] UC-07 (admin reset password) — touches authentication; no misuse case and no journal note
[MISUSE_CASE_NO_RESPONSE] MUC-04 (mass enumeration of user emails) — abuse pattern described but no system response defined
[UNPROPAGATED_NEGATIVE_REQUIREMENT] MUC-02 requires rate-limit-and-alert response — not reflected in SRD.md UC-04 negative requirements
[MISSING_PREMORTEM] EXPLORATION_JOURNAL.md has no `## Adversarial Sweep` section
[STRIDE_GAPS] Stripe webhook integration — no STRIDE consideration recorded in journal

--- CONTENT QUALITY ---
[COMPLETE] SRD.md — summary self-sufficient, rhythm varied, no AI-tell patterns
[CQ_FLAG] HANDOVER.md — missing summary section (CQ-01)

--- FIXES APPLIED ---
Pass 1:
  Fix 1: Generated sequence diagram for Stripe payment flow (was UNDIAGRAMMED_INTEGRATION)
  Fix 2: Generated state diagram for Order entity (was MISSING_STATE_MODEL)
  Fix 3: Added performance NFR for database queries based on SRD context

Pass 2:
  Fix 4: Generated process flow diagram for UC-05 checkout flow (was UNDIAGRAMMED_USE_CASE)
  Fix 5: Added summary section to HANDOVER.md (was CQ_FLAG)

--- REMAINING GAPS ---
1. [UNTRACEABLE_GOAL] Goal G-03 — user input required
2. [MISSING_NFR_CATEGORY] Scalability — user must specify targets
3. [UNMEASURABLE_NFR] Availability — needs specific uptime percentage and RTO/RPO
4. [MISSING_NFR_CATEGORY] Data — retention, backup, and privacy requirements not discussed
```

### Report Rules

- Every item in the report must reference the specific SRD element by identifier (G-01, UC-05, etc.)
- Fixes applied must reference what they fixed and which flag they resolved
- Remaining gaps must include enough context for the user to provide the missing information
- The verdict is PASS only when zero flags remain after all passes
- If GAPS_FOUND, the remaining gaps section must be actionable — each gap states what
  information is needed from the user

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-13 | Initial version | Standards team |
| 2026-03-13 | Renamed from requirements-completeness. Merged verify command. Added Content Quality verification. | Standards team |
| 2026-03-17 | Added Perspective 4: Tree Completeness. Updated from three to four perspectives. | Standards team |
| 2026-03-17 | Added Perspective 5: Referential Integrity. Cross-checks artifact content against exploration journal design decisions, assumptions, and glossary. Updated from four to five perspectives. | Standards team |
| 2026-03-17 | Audit fixes: updated stale "three" to "five" in pass description; added tree completeness to PASS exit condition; added rate limits to integration checks; formalised content quality flags (CQ_MISSING_SUMMARY, CQ_MISSING_IDENTIFIERS, CQ_RHYTHM_VIOLATION, CQ_READABILITY, CQ_AI_TELL, CQ_UNVERIFIED) with fix strategies; added CQ-04 and CQ-06 checks. | Standards team |
| 2026-05-13 | Added Perspective 6 (Term Consistency) — enforces Phase 3.5 Disambiguation Sweep vocabulary lock across artifacts. Added Perspective 7 (Adversarial Coverage) — enforces Phase 3.6 Adversarial Sweep produced MISUSE_CASES.md, system responses, propagated negative requirements, and pre-mortem. Updated PASS exit condition to require seven perspectives. | Standards team |
| 2026-05-15 | Added Perspective 8 (Two-Model Reconciliation) — enforces the Two-Model OODA Reconciliation rule has run to closure: every leaf node in PRIMITIVE_TREE.jsonld carries `leaf_category` from the five-value taxonomy, RECONCILIATION_MAP.md has zero unresolved-gap or undisposed-orphan rows, and the journal's Reconciliation Cycle Stack is closed. New failure codes: UNCATEGORISED_LEAF, UNRESOLVED_GAP, UNDISPOSED_ORPHAN, OPEN_CYCLE_FRAME. Updated PASS exit condition to require eight perspectives. | Standards team |
| 2026-05-15 | Replaced "Fix-as-you-go" with AAF triage gate per perspective. Every gap from every perspective now passes through the AAF-01 closed positive list before becoming a user question. Three-list output contract (AAF-06): Auto-Resolved / Done with announcement / User Input Required. Every User Input Required entry must carry a Triage Trace row per AAF-07. Removes the failure mode where Phase 5 surfaced artifact-maintenance findings (missing diagrams, glossary additions, identifier renumbering) as founder questions. | Standards team |
| 2026-05-15 | Rewrote PASS exit prose to use action-then-report shape per AAF-08 (Decided Actions Are Not Questions). The validation skill no longer suggests "recommend `/sulis:draft-architecture` as the natural next step. Want me to proceed?" — that pattern is now an explicit AAF-08 violation. PASS verdict triggers the analyst's Phase Auto-Progression rule; cleanups taken silently as Auto-Resolved entries; next command surfaced in action-then-report shape. | Standards team |
