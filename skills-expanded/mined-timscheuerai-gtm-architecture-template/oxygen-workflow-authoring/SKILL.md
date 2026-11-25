---
name: oxygen-workflow-authoring
description: Author, validate and operate deterministic OXYGEN Workflows and durable recipes with explicit inputs, call previews, smoke tests, capped live runs, hosted triggers and inspectable effects.
---

# Compose the hosted workflow

Read [composition](../../../docs/composition.md), [the runtime contract](../../../docs/runtime-contract.md) and the relevant function definitions. This kit contains six disabled workflow graphs and, in [the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md), three durable recipes.

Use Workflows for deterministic control flow across tables and schedules, Tables for row dependencies, Sequences for outreach cadence and Agents for adaptive goals. Local files author definitions; OXYGEN runs them.

```sh
oxygen workflows schema --subject graph --json
oxygen workflows lint --file my-workflow.workflow.json --phase draft --json
oxygen workflows apply --file my-workflow.workflow.json --draft --json
```

1. Write the spec as data: goal, trigger (API, webhook, cron or event), input schema, steps with exact tool ids (`tools search --workflow-eligible`, then `tools get`), outputs, failure behavior, idempotency keys and credit expectations.
2. Lint for the intended phase, then apply. Applying is inert: 0 credits, no run.
3. `workflows call <ref> --preview` shows what leaves OXYGEN, which accounts it uses and the credit floor. Then smoke-test or dry-run.
4. A live call needs `--approved` and a positive `--max-credits`. Enabling a cron, event or webhook trigger is a standing grant with its per-delivery ceiling, so keep demo workflows on an API trigger until the schedule is approved.
5. Tail the run (`workflows tail <run_id>`) and read each step's output and receipt.

Recipes (`defineRecipe`) suit work that crosses tables: read rows, upsert rows, run paid columns on exact row ids under a ceiling, wait durably with `ctx.wait`, and pause for a person with `ctx.approvals.require`. Lookups, AI inputs and run conditions read stored values, so a recipe that depends on formulas starts with a free forced column run.

Outbound enrolls through the native Sequence action on a bounded Sequence, never a raw provider message. A plain GET can use `oxygen.http_json_request`. Reconcile ambiguous external effects before retrying.
