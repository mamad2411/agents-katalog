---
name: comfyui-self-maintenance
description: Use ONLY when the user explicitly asks this ComfyUI Development Skills pack to maintain, refresh, or update its own upstream awareness or routing. Ordinary ComfyUI development never activates this skill automatically.
metadata:
  version: "00.01.11"
  invocation: "explicit-only"
---
# ComfyUI self-maintenance

This skill maintains the pack's awareness of current `Comfy-Org` sources.

It is **explicit-only**. A normal ComfyUI task can discover and use a new official repository without changing this package.

## Two maintenance levels

### Normal maintenance

Normal maintenance may update only the root `comfyui-development` skill's:

- `sources.json` authority/routing registry;
- `upstream-snapshot.json` organization baseline.

Use the root skill's `self_maintain.py` helper for this level.

### Optional local self-modification

Sometimes a durable upstream change cannot be represented by source routing alone. Examples include a new subsystem that needs a specialist skill or a task-routing change.

Do **not** cross that boundary automatically.

When broader work is needed, present these four choices exactly and wait for an explicit choice:

1. **Report only** — prepare a maintainer-ready GitHub Issue draft. Make no local self-modification.
2. **Self-modify only** — modify this installed copy within the local skill-only boundary. Do not prepare a maintainer Issue draft.
3. **Report and self-modify** — prepare the maintainer report, apply the local skill-only workaround, then update the report with the local changes and validation results.
4. **Stop** — make no broader changes and do not prepare an Issue draft.

There is no default choice. Do not infer consent from silence, a previous maintenance request, or ordinary development work. These four choices govern only work beyond normal routing/snapshot maintenance. If the user wants no package writes at all, keep the run in scan-only mode and do not call normal `apply`.

## Hard release boundary

Neither normal maintenance nor optional local self-modification may perform an official package release.

Do not automatically change:

- `VERSION`;
- `CHANGELOG.md`;
- the public `README.md` or `docs/`;
- tests;
- package/plugin manifests;
- CI;
- licenses or notices;
- Git tags, commits, releases, npm state, or publishing state.

The package maintainer handles official releases and official public documentation.

## Local self-modification boundary

If the user explicitly chooses option 2 or 3, the agent may teach **that installed copy** about the durable upstream change.

Allowed local changes are limited to non-executable skill knowledge under `skills/`, such as:

- the root router `SKILL.md`;
- an existing specialist `SKILL.md`;
- a new `comfyui-*` specialist skill with a `SKILL.md`;
- Markdown or JSON references inside skill directories.

Machine routing state is separate: `sources.json` and `upstream-snapshot.json` must be changed only through normal `self_maintain.py apply --yes`, not through the broader local self-modification guard.

Local self-modification must **not**:

- rewrite `comfyui-self-maintenance` itself;
- rewrite any executable helper under `skills/comfyui-development/scripts/`;
- create Python, JavaScript, TypeScript, shell, binary, or other executable maintenance code;
- modify package-level docs, tests, manifests, CI, versions, changelogs, licenses, or release files;
- publish, commit, push, or file a GitHub Issue automatically.

If the needed workaround falls outside this boundary, report the unresolved part. Do not weaken the boundary to make the task fit.

## Procedure

### 1. Scan without mutation

Activate the root `comfyui-development` skill and use:

```bash
python skills/comfyui-development/scripts/self_maintain.py scan
```

The scan compares the current public `Comfy-Org` repository list with `upstream-snapshot.json` and looks for likely authority moves.

Replacement detection is heuristic. A phrase such as `moved to` or `merged into` is evidence to investigate, not proof by itself.

### 2. Verify durable changes

For each candidate:

1. Confirm it is an official `Comfy-Org` source.
2. Read the current README plus relevant source or official docs.
3. Decide whether it has a durable development responsibility.
4. Verify replacements from official evidence when practical.
5. Decide whether existing routing is enough.
6. If broader skill knowledge is required, stop before broader edits and present the four choices.

Do not add every new repository to the curated routing registry.

### 3. Apply normal routing changes

Use reviewed route decisions with:

```bash
python skills/comfyui-development/scripts/self_maintain.py apply \
  --decisions /path/to/reviewed-decisions.json \
  --yes
```

There is no delete action. Keep superseded sources as history for older compatibility targets.

### 4. If the boundary is reached, ask the user

Present:

```text
Self-maintenance found a ComfyUI upstream change that needs more than authority routing.

Choose what to do:
1. Report only
2. Self-modify this installation only
3. Report and self-modify this installation
4. Stop with no further changes
```

Do not continue until the user chooses.

## Report path

Use this path for option 1 or 3.

Create a temporary findings JSON using schema version `1`, then run the root helper:

```bash
python skills/comfyui-development/scripts/maintenance_boundary.py report \
  --findings /path/to/findings.json
```

The report must include:

- installed/base skill-pack version;
- reason codes;
- plain-language summary;
- affected official repositories;
- official evidence checked;
- recommended maintainer action;
- whether the installation has local modifications;
- local workaround files and validation when applicable;
- a suggested GitHub Issue title and body;
- the configured maintainer repository and a candidate Issues URL.

The report helper does not contact GitHub. Verify that the configured repository exists and accepts Issues before submission.

Do not file the Issue automatically. If the user later explicitly asks an agent with GitHub access to file it, that is a separate action.

For **Report and self-modify**, generate the initial report before editing. After the local workaround is complete and recorded, regenerate the report so it includes the local workaround and validation results.

## Local self-modification path

Use this path for option 2 or 3.

### A. Prepare and validate the exact plan

Create a schema-version `2` plan. Every file entry contains the complete new text. A `modify` entry also contains the SHA-256 of the file the plan was prepared from.

Validate it without writing:

```bash
python skills/comfyui-development/scripts/maintenance_boundary.py validate-plan \
  --plan /path/to/local-plan.json
```

### B. Apply through the guard

Do not edit the package manually after plan validation. Apply the same reviewed plan through the transactional helper:

```bash
python skills/comfyui-development/scripts/maintenance_boundary.py apply-local \
  --plan /path/to/local-plan.json \
  --yes
```

For option 3, add `--report-generated`. The helper checks stale hashes, validates `SKILL.md` names and JSON, backs up affected files, uses atomic same-filesystem replacements, verifies after-hashes, updates the divergence ledger, and rolls the transaction back if apply or ledger recording fails.

A new specialist is appropriate only when the subsystem is durable and no existing specialist fits. Its directory/frontmatter name must match and use the `comfyui-` prefix.

### C. Validate the modified installation

At minimum run the package tests when present and confirm learned specialist routes point to real skills. If validation fails, use the guarded restore path or prepare another allowed plan. Do not broaden the write boundary.

### D. Check or restore local state

Check recorded state and drift:

```bash
python skills/comfyui-development/scripts/maintenance_boundary.py status
```

Restore the latest transaction only when the user explicitly asks to undo it:

```bash
python skills/comfyui-development/scripts/maintenance_boundary.py restore-local --yes
```

Restore refuses to overwrite a file that changed after the recorded local transaction.

A locally modified installation is reported as the official base version plus local divergence, for example:

```text
00.01.11+local
```

Official updates may overwrite local modifications. The local record exists so the user and maintainer can see what diverged. If the installed package is not writable, do not bypass permissions or relocate files silently; explain that local self-modification could not be applied and offer the report path instead. After a successful local skill change, reload or restart the harness when its skill discovery requires it.

## Maintainer handoff reason codes

Use the narrowest applicable code or codes:

- `new_specialist_required`
- `task_router_change_required`
- `protocol_change_detected`
- `manifest_change_required`
- `test_contract_change_required`
- `public_documentation_change_required`
- `release_update_recommended`
- `maintenance_logic_change_required`
- `other_maintainer_review_required`

Some reasons cannot be fully fixed by local self-modification. For example, a manifest or maintenance-guard change remains maintainer work even if a local skill workaround can reduce the immediate problem.

## Replacement authority rule

For current-upstream work, a route marked `superseded` follows `superseded_by`.

For a pinned historical target, the older source can still be relevant. Learning a replacement must not erase history.

## Acceptance gate

Before self-maintenance is complete:

- the current user explicitly requested self-maintenance;
- the read-only scan ran before mutation;
- every authority change is backed by current official evidence;
- normal routing changes modify only the normal machine-state files;
- if broader work was required, the user was shown all four choices and explicitly selected one;
- report-only and stop performed no broader self-modification;
- self-modification used a validated file plan;
- local self-modification touched only allowed non-executable skill knowledge and did not bypass normal maintenance for `sources.json` or `upstream-snapshot.json`;
- the maintenance guard, executable helpers, public docs, tests, manifests, CI, versions, changelogs, licenses, and release state were not rewritten by local self-modification;
- any local divergence was created and recorded through `apply-local --yes`;
- a failed local transaction rolled back rather than leaving a partial installation;
- report mode produced a maintainer-ready Issue draft but did not file it automatically;
- report-and-self-modify preserved the original finding and then added the local workaround and validation results;
- unresolved work outside the local boundary was clearly reported.
