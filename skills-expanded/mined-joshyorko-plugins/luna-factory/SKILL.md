---
name: luna-factory
description: Use when a substantial objective has potentially independent workstreams and the user wants Luna-first cost control, native Codex subagents, evidence-backed completion, or bounded Sol escalation.
---

# Luna Factory

## Core principle

The current Luna owner keeps the outcome; use the cheapest sufficient current Luna effort for delegated work and reserve stronger effort for a named unresolved need. Delegate only when delegation is cheaper than doing the work locally. Sol is a bounded exceptional interrupt, never the resident manager.

This skill is the canonical orchestration policy of the Luna Factory plugin, which also bundles the local Rust runtime and MCP Apps workbench. Direct skill invocation uses native host/Codex collaboration primitives. Installing the plugin or asking to use this skill, agents, delegation, fan-out, convergence, or unattended work does not authorize runtime actions. Invoke Luna Factory runtime tools only when the user explicitly asks to use that runtime for the current objective. This authority does not extend to another runtime merely because its name is similar, including `luna_factory_*`, `/factory`, or Review Factory surfaces.

For the current rollout, request `gpt-6-luna` only when the live Codex catalog exposes that exact model. This operational target is not a permanent generation policy: never silently substitute an older Luna, Sol, Astra, Terra, `/fast`, or another family when it is unavailable.

Use native Codex collaboration primitives directly. Direct skill use does not require starting the bundled runtime. In an explicitly requested runtime-managed run, the Rust service owns durable identity, lifecycle, and evidence records while the native Luna owner retains semantic orchestration. Do not require another orchestration skill or write runtime state into target repositories.

## Capability gate

Before the first routing decision, reuse a verified compatibility snapshot when its runtime signature still matches and observed routing does not contradict it. Audit only when capabilities are unknown, the Codex version or relevant runtime configuration changed, or actual routing behavior conflicts with the snapshot.

1. Compare the known signature: Codex version, multi-agent mode, relevant agent configuration, model catalog routing fields, and any verified nesting/metadata behavior.
2. When the signature is unknown or changed, inspect the live `spawn_agent`, follow-up, list, and wait schemas and run `python scripts/audit_runtime.py` from this skill directory when shell access is available. Read [runtime compatibility](references/runtime-compatibility.md) for the cached snapshot and probe procedure. Live schemas override remembered syntax and this skill.
3. Distinguish catalog support, requested routing, and verified effective routing. A successful spawn request proves acceptance, not execution on that model or effort.
4. If effective model or effort is not observable, label it `unverified`. Never claim savings from unverified routing.

Do not change global Codex configuration merely to run this skill. When invoked from Luna Max, keep that agent as the durable owner: do not spawn a replacement parent, downgrade it, or ask the user to optimize root effort. Luna Medium, High, and xHigh roots remain compatible but are secondary, and the current parent remains owner unless the user requests a new session.

Concentrate Max reasoning at consequential control points: outcome/world-model understanding, decomposition, dependencies, READY decisions, evidence judgment, integration, shared-assumption and false-convergence detection, completion judgment, and exceptional escalation. Push repetitive search, inventory, mechanical edits, formatting, routine test runs, and receipt extraction to deterministic tools or cheaper Luna workers. Do not manufacture workers for a trivial SOLO task.

## Own the objective

Before substantive work, reuse the request, selected issue, repository rules, and native plan to record a compact contract: **G1 / observable goal; A1..An / mandatory behavior and invariants; non-goals; authority / finish deliverable; appetite / repair limits**. A trivial SOLO task needs only a sentence and its check. Freeze acceptance meaning, not implementation steps. Keep generation separate from commit/subject: better substeps and necessary defect repairs stay in G1; changed outcomes, weakened gates, or expanded effects require G2 and the appropriate authority. An explicit user change already supplies that authority. Never drop mandatory acceptance or safety requirements to finish.

Keep ownership of G until every mandatory criterion has current proof or autonomous work is honestly quiescent. Plans, worker returns, successful intermediate checks, compaction, and knowing the next action are progress, not completion; perform already-authorized in-scope/reversible work without asking the user to authorize it again, and never return partial results merely to save time, tokens, or effort. Escalate new scope, new external effects, weakened acceptance, or missing authority; a blocked lane does not stop useful independent admitted work.

### Admit, reconcile, finish

Discovery creates candidates, not authority. Initial tasks, worker `NEXT`/`UNRESOLVED`, review findings, and owner ideas all use the same admission rule **before READY or owner-local implementation**: name an unproved/failed A# or required invariant (possibly through a necessary dependency), cite the observation or necessary uncertainty, choose the smallest sufficient action, and check authority, appetite, ownership, and dependencies. Batch related observations and reuse duplicates.

- **ADMIT:** necessary and authorized; `READY` only when dependencies and ownership permit, otherwise `BLOCKED` with a reason.
- **DEFER:** useful but unnecessary; retain a concise `DEFERRED` follow-up and do not execute it.
- **DISMISS:** unsupported, duplicate, irrelevant, or already covered by valid proof.
- **NEEDS_AUTHORITY:** `ESCALATE` the precise missing permission or outcome decision.

Use the existing small ledger:

```text
TASK | A# / GAP | DEPENDS ON | OWNER | STATE | EVIDENCE / SUBJECT
CANDIDATE -> READY | BLOCKED | DEFERRED | ESCALATE
READY -> RUNNING -> VERIFY -> DONE
VERIFY -> bounded repair of the same admitted task | CANDIDATE discovery
```
Treat the first line as the admission record, not a dispatch queue: retain the disposition, the cited A#/invariant and observation, the owner, and the relevant subject. Reuse that record when a duplicate or out-of-order receipt arrives.

Transitions are guarded:

- `CANDIDATE` becomes `READY` only after `ADMIT` and satisfied dependencies; a necessary but blocked item is `BLOCKED`, not dispatchable.
- `READY` becomes `RUNNING` only through the owner's admitted dispatch or local implementation. `DEFERRED`, `BLOCKED`, and `ESCALATE` have no mutable execution path.
- A return or check result enters `VERIFY`; it becomes `DONE` only after the owner accepts execution and acceptance evidence for the current subject.
- A failed check reopens the same admitted task for bounded repair. It does not reset its attempt lineage or create a replacement task. A new observation enters `CANDIDATE` and must pass admission independently.

No mutable dispatch from `CANDIDATE`, `BLOCKED`, `DEFERRED`, or `ESCALATE`. Workers repair within their admitted packet and return discoveries outside it; they do not start successor missions. A return is `VERIFY`, not automatic `DONE`: the owner judges execution and acceptance proof for the relevant generation, subject, and assumptions. Dependency loss or contradictory/stale proof removes readiness and reopens affected verification; retain historical receipts and explicitly unaffected proof. Optional discoveries alone cannot reopen a proven objective.

At start/resume, meaningful receipt/integration, relevant review/environment change, and before new work: refresh only relevant authoritative facts; mark mandatory criteria proven/failed/unproved; reconcile candidates, dependencies, and ownership; take the minimum useful authorized step. Keep one run note with G, remaining gaps, deferred items, and next decision. At handoff preserve subjects, retry history, active owners, and resumption conditions; do not restart discovery.

**Plateau:** unless user limits override, two consecutive attempts on the same gap without material new evidence or acceptance progress trigger diagnosis before another repair. Progress means proven criteria, reproduced/root-caused blockers, resolved necessary uncertainty, or integrated dependencies—not commits, receipts, or unrelated green tests. Classify the failure; choose a materially different authorized approach or one bounded same-goal replan. Preserve retry lineage across workers and generations. If that replan stalls again, checkpoint the unresolved decision. Real new evidence can justify continued in-scope repair. Once the end-to-end path exists, focus on remaining verification/repair; admit no speculative enhancements.

**Converged** means all mandatory criteria have valid proof for G/current subjects. **Quiescent** means no authorized autonomous step can reduce remaining gaps; it can still be unconverged. Continue independent admitted work around a blocked lane, then report the exact blocker/resumption condition. Empty queues, returned workers, and exhausted budgets are not success. When proven, stop creating work, safely collect/drain relevant in-flight activity, confirm it cannot invalidate the accepted subject, and return the authorized deliverable. Completion never independently authorizes merge/deploy. Coordinate declared shared acceptance without inventing cross-PR gates.

This is a cooperative owner protocol, not runtime enforcement or a termination guarantee. Read [routing and evidence](references/routing-and-evidence.md#convergence-decisions) for admission, proof freshness, and repair examples; forward-test with [eval scenarios](references/evals.md#convergence-trials).

## Choose a mode

- **SOLO:** Prefer for trivial, tightly coupled, or coordination-expensive implementation. Observe, implement, verify, finish. Do not spawn a worker for a task cheaper to do locally. Ambiguity alone is not a reason for SOLO when bounded read-only scouting can reduce uncertainty economically.
- **SPLIT:** Use only for two or more genuinely independent READY tasks with clear ownership and acceptance, with no conflicting concurrent write ownership. Overlapping read scope is allowed, including read-only scouts examining the same subsystem from different perspectives. If write scopes overlap, serialize integration or assign a single writer. Start with 2–3 workers. Do not dispatch dependents early.
- **ESCALATE:** Use only at a bounded judgment boundary that stronger Luna effort is unlikely to resolve safely. Sol answers one decision or review, then exits; Luna resumes ownership.

Route by semantic difficulty: clarity, judgment, reversibility, blast radius, state, mechanical verifiability, dependencies, concurrency, security boundary, and failure consequence. File count and prompt length are weak signals. Read [routing-and-evidence](references/routing-and-evidence.md) for the effort ladder, risk rules, and evidence.

For every delegated investigation, implementation, debugging, repair, acceptance review, and independent verification task, prefer the current Luna owner’s cheapest sufficient effort:

```text
deterministic tool
→ current Luna at the cheapest sufficient effort
→ stronger Luna effort only when needed
→ deliberate alternate-family diversity only when diversity itself is required
→ current Sol only for a bounded exceptional judgment or execution interrupt
```

This is a capability order, not a model-generation or mandatory-effort staircase. Keep the already-selected root when inheritance is requested; do not parse versions or silently select the highest available Luna generation. If multiple Luna generations are available and neither an explicit request nor the selected root resolves the choice, require an explicit choice. Requested model/effort and observed model/effort remain separate; missing effective metadata is `unverified`.

Alternate-family diversity is exceptional: the family must exist in the live catalog, the reason must be named, and the exact requested/observed route must be recorded. Do not assume a Terra tier exists in the current generation. Sol remains an interrupt, not a resident stronger manager.

Before crossing from Luna to an alternate family, the owner must name the specific unresolved diversity, capability, or judgment question that a fresh or stronger Luna context cannot reasonably address. A normal successful run uses no alternate-family call. A current explicit user request overrides this preference; historical output does not.

## Dispatch READY work

Prefer a clean bounded context. When the parent is Luna Max, omit `model` for Luna workers so inheritance is requested; specify a model only to change families for an explicitly justified exception. Request the cheapest sufficient Luna reasoning effort only when the live schema supports it. If the schema couples override fields to a clean/limited-history fork, obey it.

Every worker packet has:

```text
OBJECTIVE:
SCOPE / NON-OWNERSHIP:
RELEVANT FILES OR COMPONENTS:
CONSTRAINTS / DEPENDENCIES:
ACCEPTANCE CRITERIA:
ALLOWED MUTATIONS:
REQUIRED EVIDENCE:
STOP / ESCALATION CONDITIONS:
```

Require this receipt:

```text
RESULT:
CHANGED:
EVIDENCE:
TESTS:
CLEAN_ENV: pass|fail|skipped:<reason>; evidence=<source>
UNRESOLVED:
CONFIDENCE:
NEXT:
ROUTING: requested=<model/effort>; verified=<model/effort/unknown>; source=<metadata/error>
```

Concurrent work has no conflicting write owners. Overlapping read-only work is allowed; overlapping writes are serialized or assigned to one writer. Use follow-up on the same worker for bounded repair. Do not duplicate parent and worker reasoning.

## Wait and verify

Do useful independent owner work while workers run. When idle, use the native event-oriented wait with a long bounded timeout; never loop on short status polls. Reconcile terminal state after a wake or timeout.

Separate verification by responsibility:

1. **Execution proof:** deterministic tests, build, lint, schemas, searches, diff inspection, and clean-environment/runtime checks prove what actually ran.
2. **Acceptance proof:** prefer a fresh Luna context as the bounded reviewer; it checks the explicit acceptance criteria and reports pass, fail, or unproved for each item.
3. **Design/premise review:** Luna Max challenges architecture, requirements, shared assumptions, and false convergence; use Sol only when a bounded unresolved decision actually needs it.

Do not ask several models the same generic “is this good?” question or treat agreement as proof. Terra is not a routine reviewer: use it only when model-family diversity is itself the stated reason for review or the user explicitly requests Terra. Historical or pasted Terra/Sol output is evidence, not a continuing routing requirement.

For meaningful changes, verification must challenge clean checkout/environment, declared dependencies, changed-path coverage, stale fallback state, and behavioral acceptance. Async/concurrency, database or other persistence, auth/authz, file I/O, migrations, destructive operations, distributed lifecycle/state machines, production deployment, data-loss risk, and similar stateful boundaries require stronger execution and fresh acceptance verification even when the diff is small. Add rollback/recovery, partial-failure, ordering/idempotency, least-privilege, and preserved human approval checks where relevant.

## Escalate narrowly

Classify failure before increasing intelligence: decomposition, dependency, environment, assumption, ambiguity, scope, reasoning, external blocker, or test infrastructure. A broken environment is not a Sol problem.

Choose the Sol interrupt by the capability the unresolved question requires:

- **Reasoning-only Sol:** For design, requirements, or compatibility questions that do not require repository/runtime execution, prepare a bounded packet suitable for ChatGPT Sol or another read-only reasoning context. External ChatGPT integration is optional, never a dependency; if no route is available, return the packet for manual use.
- **Codex Sol:** Reserve a Codex Sol child for a repository/runtime-dependent question that Luna cannot safely resolve and that requires tools or execution. If the original objective already authorizes source mutations, Luna may delegate a narrower write scope within that authority without another user prompt. Bound exact paths, actions, commands, and acceptance evidence. Any scope expansion or mutation not covered by the original objective requires new authorization.

Use this decision packet for either route:

```text
DECISION REQUIRED:
ROLE / NON-OWNERSHIP: read-only reasoning adviser | bounded execution specialist; owns only this decision/task
EXECUTION REQUIRED: no|yes; if yes, exact repository/runtime scope and allowed commands
ALLOWED MUTATIONS: none | exact paths/actions already authorized by the original objective
AUTHORITY SOURCE: original user request | new explicit approval
CONTEXT / CONSTRAINTS:
EVIDENCE:
OPTION A / OPTION B:
TRADEOFFS:
EXACT QUESTION:
```

If the selected Sol route is unsupported or unverified, do not substitute silently: return the packet and identify whether it needs a read-only reasoning context or execution-capable Codex review.

## Finish

Report the objective result; separate execution proof, acceptance proof, and design/premise findings; list failed or skipped gates, unresolved risks, and routing verification status. Normal Luna-only completion needs no routing narrative. If Terra or Sol appeared, state the concise unresolved diversity/capability/judgment reason and whether effective routing was verified. Include only passive telemetry already exposed by native results/session metadata; never ask the user to benchmark roots, block work for metrics, or pollute the target repository. Use [eval scenarios](references/evals.md) to forward-test changes to this skill.
