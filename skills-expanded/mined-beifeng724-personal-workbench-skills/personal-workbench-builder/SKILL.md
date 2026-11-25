---
name: personal-workbench-builder
description: Build a durable personal or professional workbench as a runnable application, or produce a six-stage generic prompt pack for building it. Use when the user wants to turn a recurring workflow into a dashboard, management system, workspace, personal operating system, or long-lived website with multiple connected modules and persistent state. Trigger for project, CRM, creator, learning, family, finance, travel, teaching, legal, or team workbenches. Do not trigger for marketing sites, one-off scripts, ordinary coding tasks, or informational questions.
---

# Personal Workbench Builder

Create a durable workbench without silently dropping confirmed requirements. Adapt questions and delivery language to the user's technical comfort.

## Run The Workflow

1. Check for an existing specification and manifest before starting a new interview. Read [iteration-and-recovery.md](references/iteration-and-recovery.md) and resume the recorded state when work already exists.
2. Confirm the output mode: build a runnable workbench or create a generic prompt pack. Do not rewrite prompts for a named AI tool.
3. Set communication mode: use plain when the user says they are a beginner, technical only when consistently demonstrated, and otherwise guided.
4. Read [interview-and-levels.md](references/interview-and-levels.md). Gather only missing decisions progressively. Devices, synchronization, data importance, acceptable loss, persistence, and deployment must be decided before specification approval.
5. Create or update `workbench-spec.md` from [workbench-spec-template.md](references/workbench-spec-template.md). Preserve the user's wording and every confirmed requirement.
6. Classify L1-L4 by technical and operational complexity, never by profession or module count. Remove only AI-invented extras; alter or defer a confirmed item only after explicit user approval.
7. Run the privacy review in [privacy-security.md](references/privacy-security.md) whenever sensitive people, client, child, health, education, finance, legal, or company data may be stored.
8. In direct mode, run `scripts/workflow_guard.py` for every state transition and honor every blocked result. In prompt mode, read [prompt-pack.md](references/prompt-pack.md) and generate all six stages with the same contracts.
9. Before direct implementation, read [data-lifecycle.md](references/data-lifecycle.md), [module-contract.md](references/module-contract.md), and [deployment-options.md](references/deployment-options.md). Build a useful end-to-end vertical slice before expanding.
10. Verify according to [verification-contract.md](references/verification-contract.md), then deliver according to [delivery-deployment.md](references/delivery-deployment.md).

## Enforce State Transitions

Move direct builds through `spec-approved`, `ui-approved`, `implementation-complete`, and `verification-passed` in order. Record evidence for each state in `workbench-spec.md`.

- L1 may use the documented fast path after a clear scope summary and no objection. L2-L3 require explicit specification approval. L4 requires explicit approval of the complete current plan.
- New or materially changed UI requires explicit approval. When an existing approved design is unchanged, inherit its evidence and record why no new visual approval was required.
- `implementation-complete` requires every confirmed in-scope requirement to map to implemented behavior and an acceptance condition.
- `verification-passed` requires actual results and evidence for all required tests. Failed, blocked, or not-run required checks prevent completion.
- Never describe a direct build as complete before `verification-passed`.

## Generate The UI

Read [ui-quality.md](references/ui-quality.md). Build a visual brief from the confirmed product, audience, repeated workflow, communication level, tone, formality, density, mobile priority, stack, and any user references.

Run scripts/ui_design_intelligence/workbench_design.py for every direct build and for the UI stage of a prompt pack. Pass references with --reference and page-specific needs with --page. Persist the result into the generated project so design-system/MASTER.md is the shared contract and design-system/pages/<page>.md contains only genuine page overrides.

Treat screenshots, existing brands, and named repositories supplied by the user as authoritative evidence for that project. Separate intended UI from status bars, browser chrome, watermarks, checkerboards, and presentation frames before recording the visual fingerprint. Do not copy references into this Skill or turn them into reusable UI directions. Use UI UX Pro Max recommendations only to fill unspecified gaps.

Generate an original, workflow-specific composition. Do not offer fixed visual choices, copy a bundled UI project, or fall back to a generic sidebar and card grid. Exclude marketing heroes, AIDA/CTA funnels, ornamental effects, and dead controls.

Render desktop and phone visual prototypes for a new or materially changed interface. Ask whether the user approves the direction and what still feels wrong. Do not continue a required UI gate until `ui_confirmation_status` is approved. Follow [ui-audit.md](references/ui-audit.md) before delivery.

## Enforce Delivery Quality

- Use fictional, visibly labeled demonstration data and provide a clear-sample-data action.
- Never place secrets, service-role keys, or private tokens in frontend code.
- Create `workbench-manifest.json` and use the async storage and versioned backup contracts when persistent data exists.
- Inventory every visible control and record its acceptance condition, actual result, evidence, and status.
- Treat HTTP 200, syntax success, and selector existence as preconditions, not functional proof.
- Test desktop and mobile layouts, overflow, accessibility, empty states, primary interactions, persistence, import/export, migration, and failure recovery as applicable.
- Record test evidence and unresolved limitations in workbench-spec.md; never claim a test was run when it was not.
- In direct mode, include the runnable project, specification, tests, usage, backup, update, recovery, and deployment instructions.
- Carry the applicable project license and third-party notices into every direct-mode project.
- Do not call personal-workbench-explorer automatically. If the user does not yet know what to build, mention that they may explicitly invoke it.

