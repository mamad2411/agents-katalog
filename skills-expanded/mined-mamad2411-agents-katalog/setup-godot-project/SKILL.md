---
name: setup-godot-project
description: Configures or reconciles universal GUT, Just, validation, warning, and version-control infrastructure in a new or existing Godot project. Use when a directory containing project.godot needs reproducible Godot project guardrails or prior setup-godot-project artifacts need consolidation.
---

# Set Up a Godot Project

Configure universal Godot infrastructure only. Do not invent gameplay structure, audit gameplay quality, or refactor gameplay code.

## 1. Discover read-only

Require `project.godot`. Read [references/discovery.md](references/discovery.md) and [references/reconciliation.md](references/reconciliation.md). When legacy setup-godot-project policy artifacts are present, also read [references/legacy-v1.md](references/legacy-v1.md).

Inspect every owned setup step independently. Do not classify the whole repository as being in setup mode or consolidation mode. For each step classify:

- **Missing:** create the current artifact.
- **Current:** no-op.
- **Recognized legacy:** migrate or remove according to the documented rule.
- **Compatible customization:** preserve it and add only unambiguous missing behavior.
- **Hard conflict:** show focused evidence and ask how to proceed.
- **External mutation:** require separate explicit approval.

A single run may contain every classification.

When tracker setup is selected, invoke `$setup-bb-skills` for its owned tracker contract and external tracker configuration. Do not recreate those policies. If that skill is unavailable, stop only the owning workflow step, offer precise installation or remediation, and preserve its existing artifacts. Continue core Godot infrastructure only through an explicitly approved reduced setup.

## 2. Propose and approve

Present one complete plan that enumerates:

- every local file creation, edit, migration, and deletion;
- dependency and version choices;
- exact installation or download commands;
- preserved customizations;
- conflicts and reduced setup decisions;
- every proposed external mutation.

Include only actions that would change local or external state. Omit dependencies and setup steps classified as **Current** from the proposed action list; summarize them separately only when useful. In particular, never propose installing Just or changing `PATH` when discovery already resolves a Just executable.

Wait for explicit approval before local writes. Obtain separate approval for persistent `PATH` changes, downloads, GitHub/tracker/remotes, or other external mutations. A newly discovered hard conflict pauses only the affected step until resolved.

Tracker configuration is owned by `$setup-bb-skills` and uses its separate approval gate. Include that invocation in the proposal, but do not duplicate its tracker questions or proposed external mutations.

## 3. Reconcile

Reconcile these independent steps:

1. Godot, Just, Git, and conditionally GitHub tool discovery.
2. GUT installation and editor-plugin activation.
3. Public Just recipes for import, focused tests, all tests, runtime, and aggregate validation.
4. GUT setup smoke test and runtime verification script.
5. Applicable Godot warning settings.
6. Universal version-control ignore rules.
7. Optional tracker setup through `$setup-bb-skills`.
8. Recognized legacy setup-godot-project policy documents and AGENTS blocks.

Use `assets/project-template/` as merge input, never as authority to replace customized files wholesale. Install GUT only through [references/gut-installation.md](references/gut-installation.md).

Do not generate Deliver policy, workflow-adapter bindings, implementation guidance, architecture rules, language standards, testing policy, or code-review policy in the target repository. Deliver owns those standards internally.

Do not create GitHub Actions, placeholder scenes, gameplay folders, speculative architecture layers, or gameplay debt reports. Never commit or push unless the current user explicitly instructs it. An explicit instruction not to commit or push always wins.

## 4. Verify

Run discovery again after reconciliation. Verify:

- every owned step now classifies as Current, approved customization, or explicitly reduced;
- managed markers are unique and well formed;
- the GUT plugin is enabled without disturbing other plugins;
- `just --list` or `just --summary` exposes the required public recipes;
- `just import`, the focused setup smoke test, `just test-all`, `just runtime`, and `just validate` behave correctly on the detected operating system;
- runtime reports `NOT_APPLICABLE` successfully when no main scene exists.

Do not create a main scene to satisfy runtime validation. Use [references/report-schema.md](references/report-schema.md).
