---
name: ops-browser
description: "Operate browser pages, including mobile-browser content, and capture runtime evidence; use ops-device for device/app state."
---

# Browser Operations

## Entry Gate

Select this workflow from browser testing/verification context without requiring the user to name the Skill or repeat an invocation prompt. Operate the requested browser surface within existing task authority. A request to run
and inspect a local result authorizes its ordinary read-only acceptance; do not ask
again merely because implementation hands off here. Preflight browser/profile/tab,
target URL/state and applicable account/side-effect boundary. Stop only the operation
whose target or authority is unresolved. External sends and writes retain their gates.

Resolve whether the supplied request identifies a page/tab or authorizes target
creation before loading operation profiles. When that identity is absent, report
the target gap directly; repository-source discovery and platform-profile expansion
cannot establish the missing browser target.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any browser operation | [platform operations](references/platform-operations.md), [tab lifecycle](references/tab-lifecycle.md), and [viewport policy](references/viewport-policy.md) | Bounded target operation with an observed viewport and qualified claims |
| External-AI turn, attachment/submission, or structured operation handoff | Applicable sections of [browser operation protocol](references/browser-operation-protocol.md) | Correlated side-effect and response evidence |
| Local workspace/browser ownership applies | [local workspaces](references/local-browser-workspaces.md) | Verified target selection |
| Runtime visual comparison applies | [visual evidence](references/frontend-visual-evidence.md) | Same-state capture/comparison |
| Focused UI geometry or overlay-interaction acceptance applies | [runtime coverage](references/frontend-visual-evidence.md#required-runtime-coverage) | Contract-scoped geometry and interaction evidence |
| DevTools/console/network debugging or performance capture applies | [DevTools debugging](references/devtools-debugging.md) | Scoped observation |
| A page runs in a physical phone browser or native-app WebView | [usage](references/usage.md) | Browser evidence with bound device/app context and a scoped device handoff |
| Browser acceptance encounters an abnormal/empty API and task context permits synthetic test inputs | [Network Mock](references/network-mock.md) | Scoped response replacement, request lifecycle and separate Mock evidence |
| Axure/Lanhu evidence extraction applies | [Axure evidence](references/axure-product-evidence.md) and/or [Lanhu evidence](references/lanhu-ui-evidence.md) | Qualified source evidence |

## Invariants

- Inventory and identify the exact target before action; absent target with no creation policy is not verified.
- Separate read observation from side effects; never infer identity, authorization, or application acceptance from browser reachability.
- Preserve target/profile and avoid focus theft; report actual postcondition and unverified gaps.
- Route by the page result being verified, then choose the best authorized adapter
  available on this host, including native computer controls when they bind the
  target and meet the evidence need. A mobile browser page remains browser-owned;
  device launch, guest state and permissions belong to `ops-device`. A native app's
  WebView remains owned by its device or desktop-client Skill.
- Resolve viewport control authority from host policy and user authorization. Choose built-in browser and isolated Playwright dimensions without an extra size question; use a local user browser at its current size unless responsive or exact-viewport acceptance requires otherwise. Task-owned tabs do not prove isolation; when shared-state changes are prohibited or their scope is unknown, use passive observation and stop only affected operations.

## Output Map

Return surface/profile/tab identity, target state, authorized action, evidence/captures, postcondition, cleanup state, and gaps.

## Reference Map

- Read [platform operations](references/platform-operations.md), [tab lifecycle](references/tab-lifecycle.md), and [viewport policy](references/viewport-policy.md) for target and side-effect invariants. Load the [browser operation protocol](references/browser-operation-protocol.md) only for external-AI turns, attachments/submissions, or structured handoffs; ordinary page inspection needs no provider-turn ledger.
- Read [local workspaces](references/local-browser-workspaces.md), [visual evidence](references/frontend-visual-evidence.md), [DevTools debugging](references/devtools-debugging.md), [Axure evidence](references/axure-product-evidence.md), and [Lanhu evidence](references/lanhu-ui-evidence.md) only when applicable.
- Read [Network Mock](references/network-mock.md) when browser acceptance needs synthetic inputs under current task authority, including an established fallback preference. Do not request repeated permission for the same scope; the caller owns project contracts, fixtures and runner versions.
- Read [usage](references/usage.md) when selecting a backend or mode, performing a write, capture, recording, or download, or producing a protocol handoff. Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
