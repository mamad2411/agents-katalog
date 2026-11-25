---
name: better-ax-for-computer-use
description: Design, audit, and repair source-modifiable web and native applications so Computer Use can understand the UI, act on the right object, and verify outcomes. Use for DOM/ARIA, AX/UIA, custom controls, consumer interoperability, or app-side activity-history readiness. Not for operating apps or installing recorders.
---

# Better AX for Computer Use

Engineer the application around real user tasks. Make its visible UI and
accessibility representation express the same objects, state, permissions and
actions. Then verify what the intended consumer receives and what an operation
actually changes.

The unit of work is a workflow or component contract, not a count of ARIA
attributes or named nodes. Human accessibility remains a requirement even when
the selected agent uses screenshots.

## Establish the Assignment

Determine the requested outcome and change authority from the user and repo:

| Request | Work to perform | Completion means |
|---|---|---|
| Audit or review | Trace the relevant flow using source and permitted evidence | Findings, responsible layers, coverage and unknowns reported |
| Repair or improve | Reproduce a defect, repair its owner, compare before/after | The scoped defect is fixed with evidence; consumer limits remain explicit |
| Build or redesign | Define the contract, then implement when requested | Design-only work delivers a reviewable contract; implementation requires relevant tests |
| Improve activity history | Design or repair app identity, observable transitions and privacy; test an existing consumer only when available and authorized | App-side claims supported independently; capture/reconstruction claims need pipeline evidence |

Source-unmodifiable targets require a separately scoped adapter task. Custom
rendering is in scope when its source can be changed. Audits do not authorize
edits or state-changing probes. Application improvements do not authorize a new
runtime, MCP server, recorder, wider permissions, or personal-history access.

Read only the references needed for the selected work:

| Need | Reference |
|---|---|
| Define or repair a component's behavior | [Component contracts](references/developer-checklist.md) |
| Diagnose Web names, input, layers, frames or shadow roots | [Web AX/DOM](references/web-ax-dom.md) |
| Implement native or custom-rendered semantics | [Platform patterns](references/platform-patterns.md) |
| Identify what a named TryCua/Codex path consumes | [Consumer profiles](references/web-consumers.md) |
| Diagnose scope, stale targets, delivery or unknown outcomes | [Consumer contract](references/consumer-contract.md) |
| Choose evidence and state completion accurately | [Verification](references/verification.md) |
| Improve recording or reconstruction | [History readiness](references/history-readiness.md), then its linked test plan |
| Review rationale or source versions | [Evidence notes](references/evidence-and-ecosystem.md) |

## 1. Define the Task and Its Evidence

Read the owning components, state transitions and existing tests. Write down
what the user must be able to do, to which object, under which conditions, and
what would establish success or failure. A short paragraph suffices for one
control; use a workflow table for broader work.

For example: edit the name of project Alpha, submit, and confirm that Alpha's
stored name changed while Beta remained unchanged. A visible field changing
does not alone satisfy that task.

Identify the actual observation and action paths when known:

```text
shared application state
  -> rendered pixels / DOM semantics / browser AX / native accessibility
  -> consumer selection, projection and scope
  -> model-visible observation
  -> resolved target and input/action delivery
  -> application transition, commit or failure
  -> new observation; retained evidence only when history is in scope
```

Record relevant app/client versions, model adapter, platform, surface and access.
An SDK tree method need not feed the model; DOM role matching need not equal
browser AX; an AX target need not receive a native accessibility action.

If no consumer is specified or available, proceed with the application's native
semantics and normal interaction contract. Use an available authorized inspector
or synthetic fixture where useful, and label interoperability untested. Do not
install a consumer or require a product-wide audit to repair one button.

## 2. Find Where the Contract Breaks

Compare the failing task at adjacent layers. Choose a targeted observation or
experiment that can distinguish causes before adding attributes.

| Evidence | Likely owner to investigate |
|---|---|
| Visible label, role, focus or state is wrong in the component | Application primitive or owning view |
| Application semantics are correct but platform output is absent/wrong | Framework or platform bridge |
| Raw semantics are correct but the model gets a subset, summary or no tree | Consumer configuration, projection or host forwarding |
| Correct target is observed but input goes elsewhere or is rejected | Target lifetime, action backend, focus or runtime support |
| Input arrives but state/commit is wrong | Application event, validation or persistence path |
| Operation succeeds but history loses its source or outcome | App observability, event capture or reconstruction; inspect each separately |

These are diagnostic leads, not automatic blame assignments. Empty, denied,
truncated, redacted and unsupported observations are different states.
Inspect the actual frame/window and current document before inferring missing
semantics. Preserve correct markup when a downstream client drops information.

For broad requests, derive coverage from source-defined workflows and shared
component call sites. Include critical loading/error, modal, large-data,
responsive and platform states. Prioritize shared causes, then owning views;
do not equate a few screenshots with full-product coverage.

## 3. Implement at the Owning Layer

Use native controls and existing design-system primitives first. For custom
controls or rendered objects, expose platform-supported semantics from the same
state and command path that rendering uses. Do not maintain a second hidden
agent UI or independent semantic object model.

Maintain these application contracts:

- Understand: useful visible and accessible labels, structure, values and
  relationships let the user identify the object and its current state.
- Act: focus, keyboard/pointer behavior, permissions, validation and supported
  actions agree with that state. ARIA declarations do not implement behavior.
- Verify: pending, committed, failed and unknown outcomes remain distinguishable.
  Use an independent test oracle when the task promises persistence.
- Attribute, when history matters: document/window identity and meaningful
  transitions remain observable without exposing secrets or fabricating events.

Use scoped object context for repeated labels. Keep domain identity separate
from ephemeral action references; re-resolve after relevant mutations. Spatial
operations may use current geometry, while ordinary commands should also have
usable semantic/keyboard access. Do not force a pointer failure to pass or
blindly replay a timed-out mutation.

Only change the authorized owner. If the application is correct and the
consumer loses its tree, an app patch may be unnecessary. Report the integration
gap and complete independent app work; do not smuggle runtime changes into an
accessibility repair.

Keep semantics in the existing render/state lifecycle. No new global DOM scans,
polling, duplicated content or eager-loading of unrelated views merely to feed
an agent. Preserve secure-field behavior and sanitize diagnostics; hidden text
and custom privacy attributes are not general exclusion mechanisms.

## 4. Validate the Task, Then Report the Claim

Use [Verification](references/verification.md) to match tests to the changed
contract and uncertainty. Reuse the same task, object and outcome across baseline
and candidate. Test a relevant adverse case such as remount, delayed commit,
modal interference or focus change, not only the default state.

Separate source/component evidence, platform observation, actual consumer
delivery and business outcomes. The included Chromium lint and synthetic Web
probes are diagnostic aids; neither certifies an application or a recorder.

Report what changed or what the audit found, the layer responsible, the measured
scope and evidence, and the remaining constraints. Say whether the result is
source-verified, platform-tested, consumer-tested or history-tested as supported;
these claims are independent, not a single readiness score. If a required check
cannot run, explain that gap instead of marking it passed.
