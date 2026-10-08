---
name: model-tier-rightsizing
description: >-
  Fires before ANY agent or workflow dispatch that names a model or effort — before a
  `RuntimeAssignment` is written — routing workflow agents by wrong-output blast radius and
  verification strength. Also fires when a caller must inject a certified exact model ID and
  requested effort into a bounded dispatch or preserve a high-impact recommendation lane, and
  on the mid-run symptoms that require a stop: null output, semantic uncertainty, throttling,
  missing readback, or unresolved transport identity. Stable doctrine stays here;
  generation-specific routing stays in one canonical reference.
---

# Model-tier rightsizing

Route the consequence of a wrong answer, not task prestige or marketing rank.

## Dispatch ladder

The stable policy has four tiers and three incumbent eligible primary pairs. A pair declares
the production-admitted route family; the row-specific selection condition decides which exact
member can run. The candidate universe is deliberately broader: `/sdlc-rightsize` discovers live
configured providers and Claude-subscription passthrough, then may evaluate another exact route.
Discovery or benchmark rank does not add that route to a pair. Only target-representative local
qualification may recommend promotion, and the checked-in runtime receipt policy must separately
admit the exact tuple before production dispatch. Do not convert a pair into a provider default
or a requirement to spend tokens on both.

1. **Frontier / derail:** `gpt-5.6-sol` or `claude-fable-5`. Sol carries an advisory
   frame, scale-setting recommendation, or candidate settled-truth derivation. Fable is
   eligible only for a certified bounded frontier/adversarial packet that independently
   re-derives assumptions or supplies counterexamples; it never settles truth, replaces a
   Sol peer, or runs as an unbounded fan-out. Its use also requires the current transport to
   certify the applicable retention, refusal, and capacity constraints. Settled-truth work
   stops or reduces scope if no certified peer is available.
2. **Judgment workhorse / degrade:** `gpt-5.6-terra` or `claude-opus-4-8`.
   An error may pass ordinary gates and silently weaken an artifact. Choose Terra for the
   semantic candidate or synthesis, and Opus for an immutable-delta review or another
   certified independent judgment artifact. Require explicit acceptance criteria and
   independent review of an immutable candidate.
3. **Capable volume / retry:** `gpt-5.6-luna` or `claude-sonnet-5`. A compiler, test,
   schema, deterministic comparison, evidence check, or diff makes a wrong answer visible.
   Choose the member that has the better verified transport, task fit, and independent
   perspective for the bounded artifact. This is the default for gated and cross-checked
   fan-out.
4. **Mechanical floor / redo:** use the cheapest certified member of the capable-volume
   pair when a complete deterministic check makes the result cheap to repeat. Historical
   Haiku/Spark evidence may justify a recertified fallback, but those models are not part of
   the six-primary set.

A task moves down only when a real gate changes its failure from silent damage to a
visible retry. Importance alone never moves it up. Choose inside each pair by task fit,
independent perspective, verified transport, current quota, and correlated-error risk.
There is no global provider preference and no requirement to spend tokens on all six.

## OCX Ultracode Workflow marker rule

For an **OCX Ultracode Workflow**, every explicit `model` ID passed to `agent()` must use that
model's exact `[1m]` request form. The marker is part of the immutable outbound request: do not
strip it, substitute an unsuffixed/base ID, or retry on an unsuffixed form.

Before constructing the `agent()` call, the external authenticated harness must establish that
that exact `[1m]` model/effort/context tuple is certified by policy, admitted by the active
transport/catalog, and readable through the required identity/request-injection evidence. If any
of those facts is unavailable, ambiguous, or fails, **stop before dispatch**; make no Workflow
call and return one advisory `SeedProposal` to the conductor. A model's bare/base tuple is not a
fallback for this OCX Ultracode Workflow rule.

The suffix remains a request rather than proof of served context. The identity readback may report
the base model ID, and effective-context readback may honestly be `unavailable`; neither fact
permits removing `[1m]`, and neither claims a provider intrinsically serves 1M.

## Required dispatch contract

A model name is not a route; a route is provider+lane+wire-format+auth+region+id+
thinking-level. Two lanes that happen to serve the same nominal model ID are two separate
routes and two separate qualification targets — certifying one never certifies the other.

Every delegated call or named-workflow worker consumes one provider-neutral
`RuntimeAssignment` and must state:

- a caller-injected **exact model ID** certified by the active transport; never dispatch
  from an inherited/default model or unverified alias;
- an explicit requested effort and context form, kept separate from independently observed
  provider, model identity, effective effort, and effective context telemetry;
- immutable request-injection evidence: `request_injection_status: verified` and closed
  `request_injection_evidence` proving the exact model, effort, and context form sent by the
  launcher or adapter;
- independent model-identity evidence: non-unknown `resolved_provider` and
  `resolved_model_id`, `model_readback_status: verified`, a closed
  `model_readback_evidence`. Independent provider/model observation may honestly be unavailable
  ID maps uniquely under the versioned policy and immutable request/model evidence verifies
  identity;
- `effort_readback_status` and `context_readback_status`, each `verified` with independent
  evidence when exposed or `unavailable` with explicit source/evidence markers when the
  transport cannot expose effective effort or context behavior;
- one bounded artifact, owner, stop condition, and wrong-output class;
- the gate or independent reviewer that detects failure; and
- the fallback and escalation action before work starts.

A provider-neutral static role definition does not select a model. `resolution_state` must
equal `resolved`. Requested, inherited, unresolved, or unverified model-identity assignments
stop before dispatch. Exact request injection is mandatory and immutable. Request injection
and effective readback are different evidence classes: never copy requested values into
resolved or readback fields, and never require impossible effective effort or context readback
after request injection and model identity are verified. A requested value, host default,
alias, or echoed prompt text is not resolution evidence.

## Local qualification and Pareto evidence

`skills/model-tier-rightsizing/scripts/rightsize.py` is the bounded measurement surface behind
`/sdlc-rightsize`. It separates three route states: `catalog-only`, `route-probed`, and the
task-class-scoped `role-qualified`. The bundled smoke pack tests transport and verifier mechanics
only; it can never promote. Qualification requires a digest-bound target-representative pack,
at least five held-out tasks in the selected class, at least three attempts per task, 90% accepted
attempts, a 95% Wilson lower bound of at least 0.70, zero route/identity failures, and zero
critical-task failures. Frontier/authority cases are all critical. These are minimum evidence
requirements, not a claim that every workload needs only fifteen attempts; a calibration may
require more.

Provenance remains a precedence, not an average: `observed > declared > mined`. Published
DeepSWE, Artificial Analysis, CursorBench, Prime Intellect, or vendor results may nominate and
order already discovered candidates for local evaluation. They cannot raise a qualification rung,
prove a route or context form, fill a scale-setter slot, or grant runtime-policy admission.

After hard filters for route identity, semantic control, context feasibility, qualification, and
runtime admission, compute a separate Pareto front per task class. Maximize the locally observed
success lower bound and minimize route/identity failure plus the selected cost, token/quota, or
wall-time measure. Missing data is not zero and cannot establish dominance. Keep mean, median,
observed per-accepted economics, and provenance distinct. Claude-subscription marginal cost is
unknown (`null`), never free; API-equivalent cost and quota/usage-credit state are separate facts.

Context is a feasibility constraint rather than an optimization reward. Choose the smallest exact
certified request form that fits peak input, output reserve, and safety margin. Keep model ID and
context form separate; `[1m]` is eligible only for an already certified exact tuple or dedicated
long-context qualification, and requested context never proves served context.

A generated `model-task-map/v2` is still advisory. Local `role-qualified` evidence and checked-in
runtime-policy admission are both required for a dispatchable recommendation; neither authorizes
spawn. Evaluation calls themselves require an explicit authorization digest after the operator
has reviewed routes, attempts, data egress, budgets, usage-credit implications, outputs, and stop
conditions. Never turn the evaluator into a worker scheduler, queue, daemon, or production
launcher.

## Route qualification admission boundary

A measured cell and a *currently qualified* cell are different facts, and the second is what a
conductor needs at dispatch time. `skills/model-tier-rightsizing/scripts/route_qualification.py`
owns that durable layer against `policy/route-qualification-v1.json`: `issue` turns one recorded
`rightsize-evidence/v1` artifact into one immutable `route-qualification/v1` generation for one
exact route/class cell, `validate` checks a store, `admit` derives the pre-dispatch verdict,
and `quarantine`/`recover` take a cell out of service and bring it back. Every verb is pure over
documents named on the command line: none reaches a network, runs a subprocess, or writes a file —
a transform prints the store the caller would persist and the caller decides whether to keep it.

**Where a conductor asks the question.** Before writing a resolved `RuntimeAssignment`, run
`admit --store <store> --route-id <digest> --task-class <class> --at <instant>` with the observed
provider and model the conductor actually holds. `admit-dispatch` means the cell holds a current
qualified generation and the presented identity correlates to it. `refuse-dispatch` means no
assignment is written: return one `SeedProposal` instead. The verdict names one closed reason —
`no-generation-for-cell`, `generation-unqualified`, `ambiguous-current-generation`,
`qualification-expired`, `floor-policy-drift`, `route-identity-uncorrelated`,
`default-provider-fallthrough`, `identity-evidence-missing`, or `cell-quarantined` — and carries
`quarantine_required` with the cause when the refusal is itself a quarantine event.

This is deliberately a **separate gate rather than a clause inside receipt validation**, for two
reasons that are not stylistic. Decision 50 makes the lifecycle layers independent, so a valid
receipt must not be able to *imply* qualification. And qualification is class-specific while the
v1 receipt carries no task class at all, so the receipt cannot express the question. Passing this
gate authorizes nothing further: request injection, runtime-receipt admission, and host identity
readback remain separate and unproven by it.

**One floor, not two.** The promotion floor is not reimplemented here. `route_qualification.py`
imports `rightsize.qualification_floor`, the same function `summarize_route` uses, because Decision
49 delegates qualification to the one rightsizing evaluator and two floors that can disagree would
mean a route qualified by whichever was consulted. The contract therefore states no threshold of
its own; it names `rightsize-evaluation-v1.json#/qualification` and records that block's digest in
every generation, so a threshold change refuses old generations as `floor-policy-drift` while an
unrelated budget edit does not.

**Freshness, immutability, and scope.** A generation is current for at most 30 days from
`issued_at` (Decision 41) and `expires_at` is derived, never supplied; only a qualification refresh
renews it, and no probe or credential refresh can. Generations, quarantines, and recoveries are
append-only, and `generation_id` digests the generation's own content, so an edited record stops
naming itself. A quarantine names one exact `route_id` and one `task_class` (story 67): the same
route in another class and another route in the same class stay admissible, and the last-good
generation is preserved beside the quarantine rather than removed, which is what keeps a failed or
quarantined cell visible and non-dispatchable (Decision 40). Re-qualification is the only exit:
`recover` requires a qualified generation for that cell issued strictly after the quarantine plus
an acknowledgement of the quarantine's own cause. Mined evidence cannot issue a qualification at
all, so its separate 90-day horizon bounds nomination rather than promotion.

**What this control is not.** Both instants are supplied by the caller and this surface reads no
clock, so freshness is checked arithmetic over declared values rather than observed elapsed time: a
backdated `--issued-at` widens its own horizon and a past `--at` makes an expired generation compare
as current. Closing that needs host/boot/monotonic binding on the issuing receipt, which a
generation does not carry today. Nor is the gate an interlock — like `receipt_admission.py` it is a
control the conductor must invoke, so it makes an unqualified dispatch *refusable and recorded*, not
impossible. Under Decision 54 it is mechanical against the documents it is given and no stronger.

## Receipt admission boundary

`skills/model-tier-rightsizing/scripts/receipt_admission.py` validates one concrete
`RuntimeAssignment` receipt against the versioned
`policy/runtime-assignment-receipt-v1.json`. The v1 receipt fields are exactly:
`schema_version`, `requested_model_id`, `requested_effort`, `requested_context_form`,
`request_injection_status`, `request_injection_evidence`, `resolution_state`,
`resolved_provider`, `resolved_model_id`, `model_identity_basis`,
`model_readback_status`, `model_readback_evidence`, `effort_readback_status`,
`effort_readback_evidence`, `effort_effective_divergence`, `context_readback_status`,
`context_readback_evidence`, and `context_effective_divergence`.

It rejects duplicate JSON members and arbitrary provenance strings. Each evidence object has a
closed shape: request evidence binds the canonical requested-tuple digest; mapping evidence is
only the policy reference; verified model evidence names its `observed_identity_source` and binds
the observed provider/model to the resolved pair. Verified effort/context evidence is different in kind: it carries
the transport's own response bytes, and `readback_bytes_sha256` binds exactly those bytes —
never a digest recomputed from a requested value, which any holder of the request could write.
Those bytes must parse as JSON, and `observed_value_pointer` names the exact RFC 6901 location
the transport reported the value at: a value that merely appears somewhere in the bytes proves
nothing, because unrelated content can contain it. Freeform transport prose therefore cannot
bind a value and must be recorded as `unavailable` instead. The observed value must also be in
the policy's own effort or context vocabulary; an out-of-vocabulary transport report is
`unavailable`, never verified. `effective_value_state` records whether the value matched or
diverged from the requested value, and the top-level `effort_effective_divergence` and
`context_effective_divergence` declare that same fact where a consumer reading only the summary
fields will see it. A divergent effective effort or context is admissible and recorded as a
divergence; it is never refused for diverging and never upgraded to agreement, and a receipt
whose evidence records a divergence its top level omits or contradicts is refused. It rejects
prompt echoes, caller defaults, and copied-request masquerading as readback, comparing
request-derived shapes after canonicalization so reformatting does not evade the check — that
refuses provably request-derived bytes, and cannot by itself authenticate that any other bytes
came from the transport. `validated` means only that this internal schema and
digest consistency check passed; `invalid` means it did not. The validator never authenticates
an issuer or claims external injection, readback, admission, or spawn identity.

A gateway-routed assignment is held to two further rules, because a gateway is a second router
between the caller and the model. `observed_identity_source` must be `gateway_attribution_log`:
the gateway's response `model` field is inadmissible by name, since it echoes the caller's own
requested string — a caller-chosen alias comes back as identity while the attribution record
names the model that actually served the request. Identity then binds through
`observed_provider_pointer` and `observed_model_pointer` into the attribution bytes, because that
record names the requested model alongside the resolved one and only the position tells them
apart. Second, the dispatched exact ID must be present in the gateway's served `GET /v1/models`
catalog, proven by `catalog_bytes`, its digest, and `catalog_model_pointer`. Catalog membership is
the enforceable rule and a provider-prefix convention is not: an unrecognized model string is
forwarded verbatim to the default provider rather than refused, so bare and prefixed forms of an
unknown ID behave identically. These fields exist only on the gateway route; a direct-adapter
receipt records `adapter_response_readback` and carries neither.

A gateway's own refusal is not evidence about a provider. An HTTP 413 from opencodex's
input-admission preflight — an inbound token estimate above the route's ceiling × 2.5 — is refused
locally before any provider request exists, so `rightsize.py` records it as
`input_admission_refused`, its own classification: fail-closed like every other identity failure,
but never readable as a provider, model, or quota fault, and never a verified receipt. The gateway
log fields and route-kind union named here were re-verified against opencodex `2.28.0`; behaviors
that need a live gateway to observe stay attributed to the `2.11.1` measurement until the `2.28.0`
canary re-measures them (`references/model-routing-calibration.md`).

The policy validates only certified requested tuples. Claude base tuples remain eligible outside
OCX Ultracode Workflow; exact Claude `[1m]` forms are invalid until tuple-specific policy evidence
exists, so that mode stops before dispatch rather than selecting the base tuple. GPT `[1m]` forms
remain eligible only where calibration supports that tuple. It emits deterministic validated/invalid
JSON with a canonical JSON SHA-256 digest. It is stdlib-only.

This repository supplies no production worker launcher. The bounded rightsizing evaluator may
invoke the existing reviewed `ccodex` launcher only for an operator-approved evaluation plan; it
cannot dispatch workflow roles. `receipt_admission.py` checks only a supplied receipt's internal
schema and tuple consistency; it does not by itself enforce the OCX Ultracode `[1m]` marker rule,
observe the outbound `agent()` argument, admit a route, or spawn a worker. An external authenticated
harness remains the sole production admission and spawn authority: it must invoke validation
immediately before spawn, correlate the digest with immutable spawn evidence, and enforce no-bypass
request injection, worker identity, and the OCX Ultracode marked-form rule. Unsupported native host
paths fail closed; do not replace that failure with a host default, adapter class, scheduler,
retries, journal, queue, daemon, or Evolutionary Core.

Ordinary non-OCX dispatch remains governed by the certified tuple policy: a certified `base`
tuple can validate there, but it is never an OCX Ultracode fallback.

An executable Workflow call pins both fields on every worker; a second vendor is used only
when it produces a distinct artifact. In OCX Ultracode Workflow mode, every explicit model form
carries `[1m]` and must be certified/admitted/readable before the call. This currently admitted
GPT-only example does not make an uncertified Claude form executable:

```js
const candidate = await agent(implementationPrompt, {
  model: 'gpt-5.6-terra[1m]', effort: 'xhigh', schema: Candidate,
})
const review = await agent(reviewPrompt(candidate), {
  model: 'gpt-5.6-luna[1m]', effort: 'high', schema: ReviewFinding,
})
```

Do not omit either field on direct subagents, named workflows, retry workers, or reviewers.
If a host's API separates model/effort assignment from the role prompt, the dispatch receipt
must still carry the same requested values and the adapter readback state. If the adapter cannot
accept the exact `[1m]` form, stop before the call and return one `SeedProposal`; never remove
the suffix as a fallback.

## Fallback discipline

Treat null, malformed, truncated, missing, or transport-rejected output as failure.
Classify transport failure versus task-output failure, apply bounded backoff, and retry the
same certified cell once. Reduce fan-out on capacity pressure, but do not silently weaken
the blast-radius class or gate. A fallback may cross lanes only when the same class and
control predicate remain true. If no certified route exists, stop or decompose into smaller
verifiable artifacts.

## Canonical calibration

Load the [canonical calibration](references/model-routing-calibration.md) before dispatch.
It is the sole human reference for current exact IDs, requested effort bands, alias
behavior, context boundaries, per-model context windows and their shared-versus-separate
input/output shape, smoke evidence, quotas, roadmap-family lanes, vendor
complements, fallbacks, rerun triggers, and auditable receipts. Load the versioned
[benchmark evidence](references/model-benchmark-evidence-2026-08-12.json) only when nominating
local evaluation candidates; its `mined` claims never replace calibration or observed evidence.
Do not copy the calibration matrices here; recalibrate the reference when transport, lineup,
telemetry, or representative results change.
