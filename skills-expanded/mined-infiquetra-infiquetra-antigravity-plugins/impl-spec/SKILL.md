---
name: impl-spec
description: Author and prove a profile-backed multi-document implementation specification through a bounded six-stage Antigravity pipeline. Use for context-library style spec sets with a declared README folder contract; do not use for ordinary single-document feature specs.
argument-hint: "<profile.json> [autonomous|interactive]"
---

# Impl-Spec

`/impl-spec` turns a settled service or system requirement into a buildable multi-document
specification set. It is distinct from `/spec`: `/spec` sharpens one WHAT document, while
`/impl-spec` authors a profile-defined set of architecture, contract, workflow, and operations
documents whose completeness can be checked mechanically.

## Lifecycle position

The reference route is:

`/ideate -> /brainstorm -> /impl-spec -> /plan -> /doc-review -> /work -> /code-review -> /qa -> /retro or /handoff`

`/impl-spec` is an off-chain obligation. It never writes a stored Saga lifecycle phase. Its promoted
`saga.impl-spec-set.v1` manifest is the durable input to `/plan`. The buildability probe inside this
pipeline does not replace the later `/doc-review` hard gate on the plan.

Do not route to or create `/product-review`; that separately approved capability remains deferred.

## Entry contract

Require one repository-relative `saga.impl-spec-profile.v1` JSON file. Discover the declared README
folder contract before asking authoring questions:

```bash
python3 plugins/saga/scripts/impl_spec.py discover --repo-root . --profile <profile.json>
```

If the profile, spec root, README, table, folder, file list, completeness rule, or dependency graph is
missing or invalid, stop with `unavailable`. Never infer a CAMPPS layout or ask the model to invent a
replacement contract.

The operator chooses `autonomous` or `interactive`. Autonomous mode pauses only for unresolved
product decisions, exhausted probe remediation, or unsafe promotion conflicts. Interactive mode also
pauses after Research, Author, Review, and each failed probe round.

Create an ignored staging mirror at
`.gemini/saga/impl-spec/<profile-id>/workspace/`. Copy the profile and declared README into the same
repository-relative paths inside that mirror. Stages 2 through 6 read and write only the mirror;
their `impl_spec.py` commands pass the mirror as `--repo-root`. The profile paths still name the
eventual canonical `docs/specs/` targets. Do not write those canonical targets until the promotion
transaction runs.

## Execution capability

Bind a current sanitized host receipt for consumer `saga.impl-spec` before independent authoring or
review:

- `agy.agent.execution=passed`: use native `invoke_subagent` conversations. Launch independent
  folders in one wave together; wait for the whole wave before dependent folders.
- `agy.agent.execution` is `unknown` or `unavailable` and
  `agy.sequential.isolation=passed`: use separately isolated sequential document conversations. Each
  folder or review result needs a unique execution identity and receipt.
- `agy.agent.execution=failed`, missing isolation proof, or same-context roleplay: stop independent
  execution. Do not relabel inline prose as an author or reviewer receipt.

This narrow fallback applies to profile-backed document authoring and review only. It does not enable
code implementation workers or the full multi-agent-consensus backend.

## Six-stage pipeline

Read `references/impl-spec-stages.md` in full, then execute every stage in order:

1. **Research** — produce a grounding brief with sources, inventories, cross-spec obligations,
   divergences, and costed open questions.
2. **Author** — execute folder assignments in dependency waves and close lifecycle,
   cross-record-rule, and contract-to-prose classes.
3. **Assemble** — rewrite the spec-set README last so it indexes the authored set.
4. **Verify** — run profile completeness, links, counts, and applicable contract validators.
5. **Review** — run separate security/access-control and consistency/standards reviews; fix every
   actionable P0-P3 finding.
6. **Probe+Remediate** — invoke `/doc-review` buildability-probe mode with fresh context. Fix finding
   classes and re-probe, capped at three rounds.

After each completed stage, update only the ignored checkpoint
`.gemini/saga/impl-spec/<profile-id>.json`. The checkpoint records stage name and artifact references;
it is not evidence, resumability authority, or a Saga tick.

## Completion and promotion

Completion requires all of these:

1. `impl_spec.py validate` against the ignored staging mirror reports `complete: true`.
2. Security and consistency reviews have no actionable P0-P3 findings.
3. A fresh `saga.buildability-probe.v1` result passes `impl_spec.py probe-check` with verdict `PASS`.
4. Independent author/reviewer identities and the probe receipt bind into the applicable transition
   receipt.
5. Every required staged spec document is promoted into the profile's `docs/specs/` target through
   `artifact_promotion.py`; no earlier stage writes canonical content.
6. `impl_spec.py manifest` runs against the staging mirror and emits the deterministic set manifest;
   promote that manifest last to `docs/specs/<profile-id>/spec-set-manifest.json`.

A document present without the final manifest and promotion receipt is useful work but does not
satisfy `/impl-spec`. A divergent canonical predecessor returns `conflicting`; preserve both sides
and stop for operator adjudication.

Route the promoted manifest path to `/plan`. `/plan` must name it as an input; the resulting plan then
passes the ordinary `/doc-review` readiness gate.

## Hard boundary

- No stored Saga phase or fabricated completion tick.
- No implicit commit, push, PR, issue, board, merge, deployment, or live canary.
- No `/product-review` surface.
- No schema invention when the profile or README contract is absent.
- No probe pass with a boundary-test defect or after more than three rounds.
- No claim that runtime staging or a checkpoint is canonical evidence.

## Reference files

- `references/impl-spec-stages.md` — entry, output, and exit criteria for all six stages.
- `references/authoring-subagent-prompt.md` — closed author assignment template.
- `../../references/buildability-probe-protocol.md` — fresh-context probe and hard verdict.
- `../../references/lifecycle-closure-matrix-template.md` — required stateful-entity closure.
- `../../references/artifact-promotion-contract.md` — canonical repository promotion.
- `../../references/operator-choice.md` — host capability and fallback authority.

## Executable receipt commands

Run the executable receipt path for every required staged spec and promote the set manifest last.
Read `$SAGA_PLUGIN_ROOT/references/live-receipt-commands.md` for the closed JSON inputs and full flags.

```bash
SAGA_PLUGIN_ROOT="${AGY_PLUGIN_ROOT:-$HOME/.gemini/config/plugins/saga}"
test -f "$SAGA_PLUGIN_ROOT/scripts/transition_receipts.py"
test -f "$SAGA_PLUGIN_ROOT/scripts/artifact_promotion.py"
```
