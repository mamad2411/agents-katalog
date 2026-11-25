---
name: build-ui-screens
description: Build the visual UI screens for one approved UI branch as an ordered element-batch loop — one flow step at a time, with a per-batch visual checkpoint and a minimum-UI stop — using fake, fixture, local, or in-memory data, then hand the screens to logic-wiring to make them clickable.
type: execution
version: v0.4
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "[approved-ui-experiment]"
context_intake: scoped
visual_tier: prototype
---

# Build UI Screens

Invoke as `$build-ui-screens`.

Build the visual UI screens for one approved UI branch. Use this skill after `$ui-interview [specific-ux-variation]` approves a UI experiment branch and the branch needs concrete screens before the clickable, state-backed prototype exists. This is the visual half of the build leaf; `$logic-wiring` is the wiring half that makes these screens reachable and interactive.

This skill builds screens as an **ordered element-batch loop**: one flow step at a time, adding the elements that step needs, pausing at a **per-batch visual checkpoint**, and stopping at the **minimum UI** that lets the flow step read as real. It uses fake, fixture, local, or in-memory data. It must not introduce durable database/storage, auth, payments, analytics, deployment, admin tooling, multi-tenancy, production observability, or other production infrastructure — that wiring belongs to `$logic-wiring` and later production planning.

Follow `DESIGN-TREE-LOOP.md` for design-tree routing, state storage, branch decisions, approval boundaries, and task classification. UI experiment branch state belongs in `design/**/flow-tree-*.yaml`, not `tasks/todo.md`.

## Gate

Before building, verify the approved branch is explicit:

- Read `design/**/flow-tree-*.yaml` and resolve the named `ui_experiments[]` branch. If `$ARGUMENTS` is missing, choose the first approved UI experiment branch that has no visual screens yet (no `build_ledger[]` past `minimum-ui-reached` and no `experiment_path`/`review_evidence`), honoring any recorded branch-order override.
- Read the branch packet from `design/ui-[topic].md`, `design/ui-requirements-[topic].md`, or product-path-scoped equivalents.
- Read the parent `design/ux-variations-[topic].md`, `design/user-flow-[topic].md`, and any relevant `design/brainstorm-inspirations-{topic}.md` or `design/take-inspiration-{topic}-*.md` when present.
- Stop if no UI branch has an explicit approve decision. Route back to `$ui-interview [specific-ux-variation]`.
- Stop if the requested work needs production infrastructure. Record the deferred infrastructure and route to prototype evidence first.

## Process

1. **Resolve scope.** Identify the product path, topic, parent user-flow branch, UX variation branch, and approved UI experiment branch. Preserve branch IDs from the flow-tree manifest. Read the batch plan authored by `$ui-interview` when present.
2. **Define the first-value journey.** Name the first-value moment, the primary task path, the entry route, the exit/success state, and the evidence needed before moving deeper.
3. **Choose the screen home.** Prefer a project-native lightweight route when the app already has a safe local experiment surface. Otherwise create a disposable route under `experiments/{topic}/{ui-experiment-id}/`. Keep the screens easy to remove.
4. **Walk the element-batch loop.** Treat each flow step as one batch (`build_ledger[]` entry = one `flow_step`). For each batch, in flow order:
   - Add only the visual elements that flow step needs. Use fake, fixture, local, or in-memory data.
   - Pause at a **per-batch visual checkpoint**: render the screen and confirm it reads as the intended moment before moving to the next batch.
   - Apply the **minimum-UI stop rule**: stop adding elements once the flow step reads as real. Do not over-build secondary controls, alternate states, or dense admin surfaces in this pass.
   - Record the batch in the `ui_experiments[].build_ledger[]` array: `id`, `flow_step`, `elements_added[]`, status `minimum-ui-reached` once the stop rule fires (or `parked` if the batch is deferred out of this pass), and a short `notes`.
5. **Progressive reveal.** Introduce first value and the primary task path before dense secondary controls. Hide, defer, or stub secondary controls until the screens prove the core journey.
6. **Review evidence.** Produce a concise review note naming what the user should look at, what the screens establish, what worked, what remains unknown, and which deferred infrastructure stays out of scope.
7. **Update branch state.** Write the `build_ledger[]` entries and add `experiment_path` and `review_evidence` to the relevant `ui_experiments[]` branch in the flow-tree manifest. Keep `artifacts[]` for canonical design and review files. Do not create or update the prototype build plan from here.
8. **Build the alignment page.** Render the per-batch screens, first-value journey, fake-data boundary, build ledger, deferred infrastructure, and review gate in `alignment/build-ui-screens-{topic}.html`.

## Output

The skill may create or update:

```text
experiments/{topic}/{ui-experiment-id}/
design/**/flow-tree-*.yaml
alignment/build-ui-screens-{topic}.html
```

When using a project-native route instead of `experiments/`, record the exact route path in `experiment_path` and the concise note or repo-relative review artifact in `review_evidence` in the flow-tree manifest and in the alignment page.

## Next Work

After the screens exist and the build ledger is written, hand off to wiring:

- `$logic-wiring` to make the built screens clickable and state-backed (the default next step; advances `build_ledger[]` entries from `minimum-ui-reached` to `wired`).
- `$user-flow-map --prototype-build-plan [topic]` when approved UI experiments are ready to become prototype build-plan items.
- `$uat --variant-evaluation` when the screens themselves are being used as the evaluated variant artifact.

**Recommended next command:** `$logic-wiring`.

Do not route to production planning, roadmap work, or durable infrastructure until experiment review evidence explicitly promotes the branch.

## Constraints

- Use fake, fixture, local, or in-memory data only.
- Build one approved UI experiment branch per run.
- Build one flow-step batch at a time; stop each batch at the minimum UI that lets the step read as real.
- Use progressive reveal; do not expose dense secondary controls before the primary task path reads.
- Do not wire clickable navigation, state transitions, or runnable logic — that is `$logic-wiring`'s job.
- Do not build production infrastructure, external account integrations, deployment automation, or durable storage.
- Do not skip the review evidence gate before handing off to `$logic-wiring`, `$uat --variant-evaluation`, or `$user-flow-map --prototype-build-plan`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell before the target skill.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/build-ui-screens-{topic}.html`.

The page must show the per-batch screens, first-value journey, primary task path, build ledger, fake-data boundary, deferred infrastructure, review evidence, and the exact downstream handoff gate.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
