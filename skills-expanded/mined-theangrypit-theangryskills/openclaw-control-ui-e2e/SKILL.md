---
name: openclaw-control-ui-e2e
description: "Use when changing or proving OpenClaw Control UI behavior with deterministic Gateway fixtures, browser flows, rendered evidence or interaction profiling."
---

# Control Ui E2E

Codex adaptation of the pinned OpenClaw source. Repository-specific commands apply only to a verified OpenClaw checkout; portable debugger commands apply to their selected process.

## Repository and UI boundary
Use only in the selected OpenClaw checkout. Read root and scoped UI instructions, inspect current package scripts and the relevant UI owners before choosing commands. Use the packaged upstream workflow for test shape and mock patterns. Follow [visual proof](references/upstream/references/visual-proof.md), [interaction profiling](references/upstream/references/interaction-performance.md) and [Run Inspector evidence](references/upstream/references/run-inspector.md) for those branches. Resolve repository-owned imports in that checkout.

For substantial UI changes, follow the upstream visual-proof guidance and prepare a fixture-driven state gallery covering relevant normal, empty, loading, error, permission, long-content and expanded/selected states. Label proposed/static states, preserve a baseline for comparisons, and give each example a stable feedback identifier. Keep gallery/recording output task-local unless explicitly selected for commit.

Use native Codex file/panel/browser tools for presentation and inspection; OpenClaw tools named in upstream material do not become Codex capabilities. Follow applicable effective-html/Impeccable guidance. Never replace required real interaction with a screenshot of a mock.

Run focused Vitest/Playwright proof through existing repository commands. Separate mocked-Gateway boundary evidence from real Gateway/product evidence and rendered-client evidence. Creating an isolated test state is different from touching the operator's live Gateway, account or data; preserve the applicable authorization.

Inspect the actual requested output and relevant wide/narrow states through an authorized surface, fix concrete defects and inspect again. If native rendering access is denied, preserve that refusal and report visual proof pending. Do not upload recordings without scoped publication authority and disclosure review.

## Visual evidence and recordings

Pair before/after captures with deterministic behavior assertions for appearance changes. Keep final captures separate from the evolving gallery and inspect the actual screenshots and finalized video before reporting them. If a recorder fails or shows unexpected behavior, stop, fix the behavior, add or update a regression test, then record again. Keep generated media task-local and do not upload it without scoped publication authority.

## Interaction profiling

For responsiveness work, define named actions, visible-result assertions and expected Gateway requests across the relevant desktop/mobile, keyboard, loading/error, permission and large-data states. Use the production UI build with matching `serverBuildId` and `serverVersion`; measure each action from before interaction through its asserted visible outcome and requests, separately from navigation and deferred background work. Begin report-only. One successful sample proves collection and behavior, not stable latency; do not treat route visits or test-file counts as interaction coverage or report automation-to-assertion wall time as INP. See the packaged [interaction profiling procedure](references/upstream/references/interaction-performance.md) for capture and artifact requirements.

## Run Inspector evidence

Count evidence only when the rendered panel has an unambiguous matching run and execution identity and the selected receipt is present. The requested URL alone is not proof. Preserve the caller's Chat page and unsent draft, and never manufacture a terminal transcript key from a DOM selector or history row. Use the packaged [Run Inspector capture details](references/upstream/references/run-inspector.md) for selectors and lifecycle.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
