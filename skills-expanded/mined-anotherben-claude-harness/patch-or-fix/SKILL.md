---
name: patch-or-fix
description: >
  Evidence-gated post-fix review that classifies whether a bug change removes the
  root cause or only masks the symptom. Any invocation, including a one-sentence
  prompt, requires the full canonical workflow and Required Output sections:
  Evidence Ledger, Assumption Ledger, Boundary Ledger, Specialist Reviews, Causal
  Chain, Structural Checks, Falsification, Required Fix, and Verification. Requires
  code/runtime proof, specialist subagents, assumption review, SRP/ownership/domain
  boundary checks, recurrence guards, a diagnose.build_packet.v1 JSON handoff for
  gh-issues/build follow-up, and finite stop rules before any FIX verdict.
---

# Patch or Fix?

A patch changes what happens when things go wrong. A fix changes why things go wrong.
**We don't ship patches. We ship fixes.**

## Non-Negotiable Rule

`FIX` is a proof verdict, not an opinion. Every factual claim must be backed by direct
code or runtime evidence. If the evaluator cannot read it, run it, query it, inspect it,
or see it in a tool result, the assessment fails closed.

A local symptom repair is not a `FIX` when the boundary is still wrong. If the rule
belongs in a domain service, repository, policy module, typed contract, schema
constraint, ownership registry, or one authoritative route/coordinator, then leaving
it in a route, UI, worker wrapper, script, fixture, fallback, or duplicated consumer
path is `PATCH` or `PARTIAL FIX`, not `FIX`.

`FIX` requires this recurrence claim to be proven: the same class of bad state cannot
be produced again through any active entry point because the invariant has one owner,
one authoritative boundary, and all relevant writers/consumers go through that owner.

Short prompts do not relax this skill. If the user only asks "is this a patch or a
fix?", still run the full workflow and produce the full Required Output. Summary-only
answers are forbidden.

Before assessment, confirm the loaded skill body contains these headings:
`Required Specialist Agents`, `Evidence Ledger`, `Assumption Ledger`,
`Boundary Ledger`, `Toyota-Way Structural Checks`, `Required JSON Handoff Packet`,
`Required Output`, and `Shipping Patches`.
If the loaded body declares itself only a trigger, delegates to another file for the
real workflow, or lacks the required headings above, stop with `SKILL_BODY_NOT_LOADED`.

Accepted evidence:
- Source code reads with exact file paths, line numbers, symbols, and call paths.
- Diffs, commits, or PR diffs that show the exact changed code.
- Focused test, canary, build, schema, browser, API, log, or runtime command output.
- Live or migrated-integration database proof when schema/query/data shape is part of the claim.

Not accepted as proof of behavior:
- Memory, naming guesses, intent, PR titles, summaries, docs, comments, ticket text, or reviewer claims.
- Mock-only proof when runtime code, real schema, browser proof, or integration proof is available.
- "Looks right", "should", "probably", or "the pattern implies".

Docs and tickets can explain intent. They cannot prove the system behaves correctly.

## Required Specialist Agents

For every substantive bugfix assessment, spawn specialist subagents when the tooling is
available. Each subagent gets one job and must return an evidence ledger plus an
assumption ledger. Do not assign one agent more than one role.

Minimum roles:
- `source-truth-reviewer`: read current changed files, surrounding callers, sibling
  patterns, and exact file/line/symbol evidence.
- `root-cause-tracer`: prove the causal chain from symptom to root cause using
  code/runtime evidence.
- `runtime-evidence-reviewer`: run or inspect the tests, browser/API flows, DB/schema
  checks, logs, worker proof, rendered artifacts, or canaries required for behavior.
- `assumption-auditor`: extract every assumption and mark it proven, contradicted, or
  unproven against direct evidence.
- `blast-radius-sibling-hunter`: find direct callers, downstream consumers, sibling bug
  shapes, shared helpers, states/statuses, routes, SQL, integrations, and tests.
- `ownership-srp-domain-reviewer`: prove whether the behavior lives in the correct
  owner, has one responsibility, and respects domain boundaries.
- `adversarial-fix-reviewer`: try to falsify the fix claim by looking for symptom
  guards, hidden fallbacks, swallowed errors, stale proof, under-scoped fixes, and
  over-broad fixes.

The lead agent integrates results, resolves contradictions, and writes the verdict. The
lead may inspect evidence directly but must not erase a specialist gap without evidence.

If subagent tooling is unavailable, still include the `Specialist Reviews` section
with each required role listed, `Ledger received` set to `UNAVAILABLE`, and the
blocking gap named. Classify the result as `FAIL: UNPROVEN` unless the user explicitly
accepts a single-agent degraded review.

## Finite Loop Rules

No infinite review loops:
- Run one initial specialist round.
- If evidence gaps remain and edits are allowed, run one repair or focused recheck round.
- If the same class of gap remains after the recheck, stop with `FAIL: UNPROVEN` or
  `UNDIAGNOSED`.
- Do not run more than two specialist rounds without explicit user approval.
- Do not ask a specialist to redo the same job unless the input evidence changed.
- Stop if specialists disagree on a material assumption and direct evidence cannot
  resolve the disagreement.
- Stop if the investigation expands beyond the original bug/root-cause class; create
  or request a new scoped task instead.

## Required JSON Handoff Packet

Every substantive assessment must also produce a machine-readable JSON artifact so
`$gh-issues` can create durable follow-up issues from the same evidence.

Default path:

```text
.codex/patch-or-fix/<slug>-handoff.json
```

If repo artifact writes are blocked, write the packet to an approved scratch path or
return the full JSON in the final response and state why no file was written.

Use the existing diagnose packet schema, not an ad hoc patch/fix schema:

```json
{ "schema_version": "diagnose.build_packet.v1" }
```

Populate the packet only from the Evidence Ledger, Assumption Ledger, Boundary Ledger,
Specialist Reviews, Causal Chain, Structural Checks, Required Fix, and Verification
sections. Do not add issue-ready claims that are not proven in those ledgers.

Status mapping:
- `FIX` with no remaining required work: use `diagnosis_status: "fixed_pending_verify"`.
  This is an archive packet, not a `$gh-issues` ready-for-agent packet.
- `PARTIAL FIX`, `PATCH`, `HARMFUL PATCH`, `OVERENGINEERED`, or issue-worthy
  `CONTAINED PATCH`: use `build_ready` only when Required Fix names exact files,
  symbols, owner boundary, acceptance criteria, and verification commands. Otherwise
  use `root_cause_ready`.
- `UNDIAGNOSED`: use `repro_ready` when the symptom/proof surface is known, otherwise
  `blocked`.
- `FAIL: UNPROVEN`: use `blocked` unless enough evidence exists for `repro_ready` or
  `root_cause_ready`.

Packet field mapping:
- `source_issue_or_pr`: PR, issue, incident, or manual source being assessed.
- `root_cause_chain`: Causal Chain rows converted to evidence nodes.
- `ownership`: Boundary Ledger owner, source of truth, consumers, wrong owners, and
  governed paths.
- `srp_refactor` and `domain_refactor`: Structural Checks and Required Fix items, with
  every `FIX-NOW` item represented as build work.
- `seam`: Recurrence Guard and falsification seam; if no correct seam exists, record
  that as `missing_seam_findings`.
- `write_leak_impact`: direct writes, transitive writes, external side effects,
  leak/tenant/auth paths, retries/jobs/events, or an evidence-backed no-write/no-leak
  finding for the assessed path.
- `ratchets`: regression tests, invariant checks, contract gates, ownership registry
  checks, canaries, or source-truth updates that prevent recurrence.
- `root_cause_confirmation`: decisive evidence, rejected hypotheses, remaining
  uncertainty, and whether the root cause was confirmed before any build-ready
  plan.
- `consensus_review`: specialist/cohort agreement status, rounds, participants,
  agreed issue/root cause/resolution, dissent, stop reason, and optional
  diagnostic-cohort contract path.
- `fix_evals`: evals that define expected failure before the fix and expected
  pass after the fix.
- `goal_prompt`: pasteable `/goal` text, required eval IDs, scope limits, and
  do-not-do guardrails. Do not emit `build_ready` without a goal prompt that
  references the required evals.
- `build_plan`: exact future build tasks only; do not list vague cleanup.
- `subagent_tasks`: one job per subagent, bounded file/symbol scope, explicit outputs,
  and `forbidden` entries that block editing outside the named scope or implementing
  consumer-layer patches when the owner boundary is named.
- `verification_plan`: exact commands or proof actions required before the issue can
  be closed.
- `do_not_do`: include concrete guardrails, such as "Do not edit outside the files and
  boundaries named in this packet" and "Do not implement a consumer-layer patch when
  the owning boundary is named."

Validate the packet before presenting it as `$gh-issues` ready:

```bash
python3 /Users/ben/.agent-platform/skills/diagnose/scripts/validate_diagnosis_packet.py <packet.json> --diagnosis-only
```

If validation fails, keep the JSON artifact but mark `GH issues eligible: no` in the
final output and name the failing fields. Do not tell the user to run `$gh-issues` on
an invalid packet.

## Workflow

### 1. Name the Change Set

Resolve what is being assessed before judging it:
- Original symptom or bug report.
- Proposed fix, current diff, PR, commit, or changed files.
- Runtime surface: route, worker, UI flow, schema/query, integration, scheduled job, or domain service.
- Proof surface that would have to fail if the defect returns.

If the change set is unknown, stop with `FAIL: UNPROVEN`.

### 2. Build the Evidence Ledger

Every assessment must include this table:

```markdown
## Evidence Ledger

| ID | Claim | Evidence | Source/command | SHA/env/time | Result |
|---|---|---|---|---|---|
| E1 | [claim] | [file:line, symbol, output, observation] | [read/run/query/action] | [current SHA, runtime target, timestamp] | PROVEN/CONTRADICTED/UNPROVEN |
```

Rules:
- Every verdict claim must cite one or more evidence IDs.
- Evidence must be concrete enough that another engineer can rerun or reread it.
- If a command was required but not run, record it as `UNPROVEN`; do not infer the result.
- `Result` must be exactly one of `PROVEN`, `CONTRADICTED`, or `UNPROVEN`.
  If a claim is proven only for a report, mock, doc, old branch, or partial surface but
  not for the behavior being judged, split the row or mark the behavior claim `UNPROVEN`.
- If evidence contradicts the proposed fix, the verdict cannot be `FIX`.
- Evidence must be current to the assessed checkout/runtime. Stale PR diffs, old logs,
  old screenshots, old canary output, prior-run memory, or evidence from the wrong
  branch/database/env is inadmissible.
- Proposed snippets are not proof. Prove the code was actually applied in the current
  diff/commit and that the relevant behavior was executed or inspected.
- Every touched file, changed branch, data path, route, query, status cohort, and
  external integration in the blast radius needs evidence or an explicit blocking gap.

### 3. Build the Boundary Ledger

Every substantive assessment must include this table. If any required boundary field is
unknown, `FIX` is forbidden.

```markdown
## Boundary Ledger

| Invariant / rule | Correct owner | Active entry points | Allowed writers | Allowed consumers | Boundary contract | Forbidden non-owner layers | Result |
|---|---|---|---|---|---|---|---|
| [rule] | [domain/service/repository/policy/contract/schema/registry] | [routes/jobs/UI/scripts/webhooks] | [writer paths] | [consumer paths] | [method/schema/event/DTO/queue/repository route] | [layers that must not own/copy rule] | PASS/FAIL/UNPROVEN |
```

Rules:
- Do not abbreviate this table. All eight columns must be present exactly as shown.
  A shortened Boundary Ledger, renamed columns, or missing writer/consumer/forbidden-layer
  fields is `OUTPUT_INCOMPLETE`, and the verdict cannot exceed `FAIL: UNPROVEN`
  until the artifact is rewritten.
- The owner must be source-proven, not inferred from names.
- Multiple entry points are allowed only when they all delegate to the same owner.
- A route, UI, worker, script, or test can verify or call the invariant; it cannot be
  the only place the invariant exists unless that layer is the proven owner.
- If the same logic must be copied into another path to prevent recurrence, the result is
  `FAIL` and the verdict cannot be `FIX`.
- If the correct owner should be a domain/service/repository/policy/contract but the
  proposed/current fix stays in a consumer or orchestration layer, classify the required
  move as `FIX-NOW`.

### 4. Build the Assumption Ledger

Every assumption must be reviewed:

```markdown
## Assumption Ledger

| ID | Assumption | Evidence check | Status |
|---|---|---|---|
| A1 | [assumption] | [evidence ID or missing proof] | PROVEN/CONTRADICTED/UNPROVEN |
```

Rules:
- Unproven assumptions cannot support a `FIX` verdict.
- `Status` must be exactly one of `PROVEN`, `CONTRADICTED`, or `UNPROVEN`.
  Mixed statuses are forbidden; split the assumption or choose the weakest applicable
  status. If any required part is unproven, the assumption is `UNPROVEN`.
- Contradicted assumptions must appear in the verdict rationale.
- Do not silently drop assumptions because they are inconvenient.

### 5. Trace the Causal Chain

Map symptom to root cause with evidence on every edge:

```text
Symptom: [observed failure] (E1)
  caused by: [immediate failed behavior] (E2)
    caused by: [upstream missing/incorrect invariant] (E3)
      ROOT: [source invariant or ownership failure] (E4)
```

If any edge is missing evidence, stop with `UNDIAGNOSED` or `FAIL: UNPROVEN`.

## Toyota-Way Structural Checks

Run these checks mechanically. Vague statements like "clearer", "cleaner", or "sharper"
do not count.

Before classification, the Boundary Ledger must identify:
- Owning entity/table.
- Owning service/module/policy/repository/domain contract.
- Active entry points: routes, UI actions, jobs, webhooks, scripts, scheduled tasks, and external callbacks.
- Allowed write paths and mutation authority.
- Allowed read/projection/consumer paths.
- Public boundary contract: route/API schema, exported method, DTO, event, queue payload, repository method, schema constraint, or ownership registry.
- Forbidden non-owner layers that must not carry or copy the rule.

The `ownership-srp-domain-reviewer` has veto power: if this check fails, the maximum
verdict is `PARTIAL FIX` when the immediate source was corrected, or `PATCH` when only
local compensation was added.

#### Defect Source

Pass requires:
- The exact broken invariant is named.
- The exact file/symbol/path that allowed the defect is cited.
- The current fix changes the source that creates or permits the bad state.

Fail signals:
- The change only handles the bad state after it exists.
- The root cause is named but the changed code does not touch it.

#### Ownership

Pass requires:
- One owning module/service/policy/repository is named for the rule.
- Evidence shows the rule is centralized there or delegated there.
- Routes, UI, scripts, workers, and tests call the owner instead of copying the rule.
- Cross-domain behavior goes through an explicit contract: exported service method,
  DTO/projection, event, queue payload, API schema, or documented ownership handoff.
- Every active entry point that can produce the same bad state is named and shown to
  call the same owner, or is explicitly out of scope with evidence.
- If there is "one route" for the behavior, that route must delegate to the owner; if
  there are many routes/jobs/webhooks, they must still converge on one owner.

Fail signals:
- The same business rule is copied in multiple layers.
- A consumer layer now owns policy, validation, persistence, formatting, and recovery.
- The fix adds another special case outside the owning domain.
- A consumer reaches around the owner to read private shape, write owned tables,
  duplicate lifecycle rules, infer status meaning, or locally repair owner-created data.
- The owner cannot be identified from source.
- The fix depends on another route, worker, UI path, or script remembering to add the
  same guard later.
- The fix creates a second owner for the same invariant.

Layer ownership rules:
- Routes own transport concerns: auth handoff, request parsing, response shape, and
  status codes. They do not own domain policy, lifecycle classification, persistence
  invariants, or cross-entity decisions.
- UI components own rendering and interaction. They do not own canonical status rules,
  permission rules, pricing/inventory/order policy, or data repair.
- Shared helpers own generic mechanics. They do not own domain-specific tables,
  statuses, tenant rules, permissions, or product/order/supplier semantics.
- Domain services own domain rules for their entity or workflow. They do not mutate
  another domain's owned state unless the cross-domain contract names them as coordinator.
- Workers/jobs own scheduling, retries, idempotent execution, and operational
  bookkeeping. They cannot be the only place a business invariant is enforced if
  synchronous writers can bypass them.
- Migrations/backfills own historical correction. They are not a fix unless the
  runtime writer that created the bad rows is also corrected.

#### SRP and Cohesion

Pass requires:
- Each changed unit has one primary reason to change after the fix.
- The changed unit's responsibilities can be listed as one cohesive domain or orchestration job.
- New helper/service boundaries remove mixed responsibilities from the defect path.

Fail signals:
- A route/controller now performs business policy, data mutation, response shaping, and recovery.
- A service now mixes unrelated domains or state machines.
- A helper is named generically but encodes one business exception.
- Equivalent logic must be copied into a sibling route, worker, page, query, or service
  to prevent the same failure.
- The bug still occurs through another entry point using the same bad source of truth.
- A touched file already has three or more unrelated responsibilities and the proposed
  fix adds a new one instead of extracting the defect-path owner.

#### Domain Boundary

Pass requires:
- Business invariants live in domain code, policy modules, repositories, or typed contracts
  that own the behavior.
- Orchestration layers coordinate; they do not define the invariant.
- UI and tests verify behavior; they do not become the only place the rule exists.

Fail signals:
- Domain logic is added to UI event handlers, route glue, cron glue, SQL fragments only,
  mocks, fixtures, or one-off scripts.
- The fix depends on callers remembering to apply a rule manually.
- The rule should move to a domain/service/repository/policy/contract owner, but the
  proposed/current fix leaves it in a non-owner layer.

#### Standard Work

Pass requires:
- The fix follows an existing codebase pattern, or creates a named standard path for this
  class of defect.
- Sibling flows use the same owner or are explicitly migrated.
- Deviations are justified by evidence, not preference.

Fail signals:
- The fix creates a one-off branch while sibling flows still use a different rule.
- The new behavior cannot be reused by the next caller with the same invariant.

#### Recurrence Guard

Pass requires at least one guard that would fail if the same class of bug returns:
- Focused regression test.
- Integration or browser test.
- Schema constraint, typed contract, invariant assertion, ownership registry, canary, or
  runtime check.

Fail signals:
- Only the visible symptom is tested.
- The test proves the patch behavior but not the root invariant.
- The proof was not run or cannot be run in the current environment.

Also require negative or falsification proof:
- Show the old symptom fails, cannot be produced, or is rejected at the owner seam.
- Show adjacent/sibling cases still behave correctly.
- Show guards, fallbacks, retries, catch blocks, defaults, or masking behavior are not
  the only reason the observed symptom disappeared.
- Show every active entry point listed in the Boundary Ledger either goes through the
  owner or cannot produce the same class of bad state.

#### Refactor Requirement

Classify structural work:
- `FIX-NOW`: required when mixed responsibilities, duplicated rules, or owner ambiguity are
  on the defect path or recurrence path.
- `FIX-NOW`: required when the invariant belongs in a domain/service/repository/policy,
  typed contract, schema constraint, or ownership registry but the proposed/current fix
  leaves it in route/UI/worker/script/test/consumer glue.
- `FIX-NOW`: required when tests cannot target the invariant without driving through
  unrelated transport, UI, job, or persistence behavior.
- `FIX-NOW`: required when a non-owner writes owned state and the bug comes from that
  write authority.
- `FOLLOW-UP`: allowed only when the structural issue is outside the defect path, has no
  current recurrence risk, and the current fix has a passing recurrence guard.
- `FOLLOW-UP`: must name the exact file/module, the responsibility to move or split,
  the owner it should move to, and the risk if it remains.
- `NOT NEEDED`: allowed only with evidence that ownership, SRP, and domain boundaries already pass.

Do not use `FOLLOW-UP` to defer work needed to prevent recurrence.

### 6. Classify

Use the strongest applicable verdict:

- `FIX`: root cause proven, source invariant corrected, ownership centralized, SRP/domain checks pass,
  recurrence guard exists, and verification passed.
- `PARTIAL FIX`: part of the root cause is corrected, but a named recurrence path or structural
  requirement remains.
- `CONTAINED PATCH`: symptom mitigation is deliberate, bounded, documented, and paired with a
  concrete fix plan because the real fix cannot ship now.
- `PATCH`: local symptom handling without proven root-cause removal.
- `HARMFUL PATCH`: hides errors, destroys diagnostic signal, masks corruption, or makes later
  root-cause proof harder.
- `OVERENGINEERED`: root cause is addressed but the solution adds disproportionate machinery;
  include the smaller evidence-backed fix.
- `UNDIAGNOSED`: causal chain has an unknown edge.
- `FAIL: UNPROVEN`: required code/runtime evidence, specialist review, or physical test/inspection is missing.

`FIX` is forbidden if any required evidence row or assumption row is `UNPROVEN` or
`CONTRADICTED`.
`FIX` is also forbidden if any Boundary Ledger row is `FAIL` or `UNPROVEN`, or if
Ownership, SRP/cohesion, Domain boundary, Standard work, Recurrence guard, or Refactor
requirement fails on the defect path.

## Required Output

Output completeness is non-negotiable. A terse invocation or one-sentence prompt still
requests the full structure below. Include every section header exactly as shown. Do
not collapse the response into a summary, abbreviated verdict, or partial ledger. If
evidence, tooling, runtime access, or edit permission is missing, keep the relevant
section/table and record the gap as `UNPROVEN`, `UNAVAILABLE`, or `FAIL: UNPROVEN`.

Before the final response, run this self-check:
- `VERDICT_FIRST_BLOCK`: the first non-empty output line must be the `## Verdict:`
  header. Do not lead with a short answer, informal classification, caveat, or prose
  summary. If the formal verdict is not `FIX`, do not use stronger informal language
  such as "real fix" before or after the verdict.
- `JSON_HANDOFF_BLOCK`: a JSON handoff packet must be written or embedded. The final
  response must include its path or explain why file output was blocked.
- `GH_ISSUES_GATE`: if the packet is meant for `$gh-issues`, the final response must
  include the validation command and PASS/FAIL result. An invalid packet is not
  `$gh-issues` eligible.
- `OUTPUT_INCOMPLETE`: if any required heading or table header below is missing, do
  not emit a narrative summary; return `FAIL: UNPROVEN` with the missing section named.
- `LEDGER_STATUS_ENUM_BLOCK`: Evidence Ledger `Result` and Assumption Ledger `Status`
  cells must use only their exact allowed enum values. Any mixed, qualified, partial,
  or prose status is `OUTPUT_INCOMPLETE`.
- `BOUNDARY_LEDGER_SHAPE_BLOCK`: if the Boundary Ledger does not use all eight
  required columns exactly (`Invariant / rule`, `Correct owner`, `Active entry points`,
  `Allowed writers`, `Allowed consumers`, `Boundary contract`,
  `Forbidden non-owner layers`, `Result`), return `FAIL: UNPROVEN`; do not substitute
  a shortened ownership table.
- `SPECIALIST_RECEIPT_BLOCK`: if any required specialist role is missing, or if its
  evidence/assumption ledger was not received and integrated, verdict cannot be `FIX`.
- `CITATION_COVERAGE_BLOCK`: every factual verdict, root-cause, structural,
  falsification, or verification claim must cite an `E#`, `A#`, or Boundary Ledger row; uncited claims
  cannot support `FIX`.
- `SUMMARY_ONLY_FORBIDDEN`: narrative summaries may follow the required tables, but
  cannot replace them.
- `AB_ARTIFACT_VETO`: for A/B testing or skill evaluation, any candidate output missing
  mandatory ledgers/tables is disqualified even if the prose is accurate.

Use this structure:

```markdown
## Verdict: [FIX/PARTIAL FIX/CONTAINED PATCH/PATCH/HARMFUL PATCH/OVERENGINEERED/UNDIAGNOSED/FAIL: UNPROVEN]

**Bug**: [one line]
**Change assessed**: [diff/PR/commit/files]
**Root cause**: [claim with evidence IDs]
**Why this verdict**: [short evidence-backed rationale]

## Evidence Ledger
[table]

## Assumption Ledger
[table]

## Boundary Ledger
| Invariant / rule | Correct owner | Active entry points | Allowed writers | Allowed consumers | Boundary contract | Forbidden non-owner layers | Result |
|---|---|---|---|---|---|---|---|

## Specialist Reviews
| Role | Job | Ledger received | Assumption rows integrated | Result | Blocking gaps |
|---|---|---|---|---|---|

## Causal Chain
[chain with evidence IDs]

## Structural Checks
| Check | Result | Evidence | Required action |
|---|---|---|---|
| Defect source | PASS/FAIL | E# | ... |
| Ownership | PASS/FAIL | E# | ... |
| SRP/cohesion | PASS/FAIL | E# | ... |
| Domain boundary | PASS/FAIL | E# | ... |
| Standard work | PASS/FAIL | E# | ... |
| Recurrence guard | PASS/FAIL | E# | ... |
| Refactor requirement | FIX-NOW/FOLLOW-UP/NOT NEEDED | E# | ... |

## Falsification
[old symptom proof, adjacent/sibling proof, and any failed attempts to disprove the fix]

## Required Fix
[If verdict is not FIX, provide exact file/symbol changes when edit permission and evidence allow.
If code cannot be safely written from proven evidence, say what must be inspected or tested next.]

## Verification
[commands run, results, and missing proof]

## JSON Handoff Packet
Path: [.codex/patch-or-fix/<slug>-handoff.json or scratch path]
Schema: diagnose.build_packet.v1
GH issues eligible: yes/no
Validation: [command + PASS/FAIL/NOT RUN and reason]
Goal prompt: [pasteable /goal handoff, or blocker preventing one]
```

When editing is allowed and the root-cause fix is proven, write real code:
- Actual files, symbols, and line numbers.
- Complete implementation, not pseudocode.
- Minimal change that removes the recurrence path.
- Tests or guards that fail if the defect returns.

When editing is not allowed, provide the smallest implementable change plan with exact files,
symbols, and proof commands. Do not call it fixed.

## Shipping Patches

Default answer: no.

A patch may ship only when all are true:
- The evidence proves it is a patch, not a fix.
- Production or delivery risk justifies containment.
- The patch preserves diagnostic signal.
- The real fix is written or specified with exact files/symbols.
- There is an owner and deadline.

Use this marker in code when a contained patch is explicitly approved:

```text
// PATCH: [root cause]. Fix owner: [owner]. Deadline: [date/ticket].
```

Patches without owners and deadlines are permanent defects.
