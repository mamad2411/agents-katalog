---
name: orbyn-setup
description: "Prepare the nested Orbyn Engineering workspace, inspect target instructions and skills in place, and verify isolation without installing shared skills into target repositories. Also lays out a project's root and nested AGENTS.md files."
---

# Nested workspace setup

Use one complete library checkout as the engineering workspace. Targets are
independent Git repositories, under its ignored `repo/` directory by default or
[registered in place](references/repository-workspaces.md#in-place-targets) by
explicit decision. There is no target installation, copy, pin synchronization
or company-skill migration. Follow the [workspace contract](references/repository-workspaces.md).
A setup request selects these steps automatically; complete them without asking
the human to invoke individual skills or run commands you can execute.

## Method

Mechanics for steps 5, 6, 7 and 9: [setup method details](references/setup-method.md#steps-5-6-7-and-9-in-detail).

1. **Inspect.** Read the library instructions and inspect Git roots, revisions, dirty files, worktree registrations and relevant host capabilities.
2. **Resolve the target** from the request, asking only if its identity is ambiguous. Use the nested layout unless the human or a managing application registered the target in place; do not ask the human to choose a layout.
3. **Prepare the library.** Run `python3 skills/orbyn-setup/scripts/workspace.py prepare` from the library. It validates the library boundary, creates its ignored `repo/` directory and turns shared memory on (see step 6 and below); add `--no-memory` or set `ORBYN_MEMORY=off` to opt out.
4. **Get the checkout.** For an authorized new checkout, inspect the destination, remote identity and available local clone, then clone the requested repository to `repo/<project>` using Git. Do not execute fetched setup hooks or source merely to inspect it. Offline setup uses an already available independent nested repository; report missing source rather than downloading implicitly.
5. **Select search roots** with [action scope](references/action-scope.md): the exact target/worktree and code-search roots, before retrieval. Instruction lookup includes outer, root and nested rules even when code filters exclude Markdown or hidden files. A missing `rg` does not authorize an install.
6. **Read the target's guidance.** Run `python3 skills/orbyn-setup/scripts/workspace.py check --target repo/<project>`, then read the target's root and nested instructions, contribution guide, existing skills and manifests.
7. **Root the session in the outer library** and state the target path in the task. Read only relevant shared skills and target guides; report host discovery as unobserved unless actually observed.
8. **Check** the full library with its documented validation commands and check the selected target separately.
9. **Report** library/target paths, full revisions and dirty state, applicable target instructions/skills, checks, preserved legacy paths and actual host discovery. Distinguish located files, returned contents, observed request inclusion and execution enforcement ([evidence levels](references/setup-method.md#steps-5-6-7-and-9-in-detail)); unavailable levels stay unknown, and a filesystem check is never a live host trial.

### Worked failure

The user selects `repo/shop-wt/fix-checkout/payments/`. A sibling primary clone has the same function name and another project's memory holds a tempting fix. Using that sibling source or memory is the failure; read the selected checkout's own rules separately from its code search, trace the function there, and claim only the evidence levels actually observed ([worked boundary](references/action-scope.md#worked-boundary)).

## What setup leaves alone

- Workspace setup writes no target files, instructions, skills, context maps, models or Git excludes; new project development follows its own authorized task. Keep upstream files and host discovery paths unchanged; preserve and read project-owned AGENT.md, AGENTS.md or local skills under the [instruction contract](references/repository-workspaces.md#project-owned-instructions-now-and-later), [project ownership](references/project-skills.md) and [project context](references/project-context.md).
- Existing external checkouts are migration inputs unless registered in place. Preserve them and their active processes/output until relocation is explicitly authorized and their owners release the path ([retiring old installations](references/repository-workspaces.md#retiring-old-installations)).
- Publishing, merging, external messages, production changes and REA engine upgrades need their own scope.
- Report the resolved harness per target with the `harness.py` in the `orbyn-workflow` skill directory, by absolute path (a missing script means stop and report). Setup writes no `.orbyn/harness.json`; only `harness.py setup` writes, and only to the ignored owner file under `repo/.harness/`; if `work mode: not set`, ask the user once (`simple`, `isolated` or `parallel`, suggesting `isolated`) and save with `harness.py setup --target <target> --mode <mode>`; unattended, use `isolated` and save nothing ([harness settings](../orbyn-workflow/references/harness-settings.md)).
- Setup does not select a provider, model, effort, speed or subscription; preserve existing settings, report unavailable capabilities, and never silently substitute models or create recursive sessions.

## Resolve instruction conflicts

Target guidance specializes stack, tests, contribution policy and local skills; shared guidance supplies compatible methods. User scope and host permissions stay higher. Surface a genuine conflict; never silently override an upstream rule or expand authority from an imported instruction. If host boundaries prevent reading both roots, stop dependent execution and report it; never copy instructions or edit user-wide settings.

## Resume after a workspace or runtime change

After migration, a failed working directory or a runtime mismatch, reconcile the selected checkout with the host's saved session binding where observable; a workdir, moved folder or project membership does not prove rebinding. Never recreate a deleted checkout or rewrite global session settings/PATH to hide it, and never run untrusted setup hooks or install a runtime implicitly. Full recovery rules: [resume after a change](references/setup-method.md#resume-after-a-workspace-or-runtime-change).

## Read when needed

- Writing, splitting or tidying a project's root and nested `AGENTS.md` files, as that project's own task: [agent instructions](references/agent-instructions.md).
- Shared memory is on by default and manual-only; `prepare` and `check --target` register it idempotently, and `--no-memory` or `ORBYN_MEMORY=off` skips it. The store is local and unencrypted, outside Git. Report the root and state from the setup output ([reflect's memory contract](../reflect/references/memory.md)).
- Isolation: [orbyn-worktree](../orbyn-worktree/SKILL.md) and sibling `repo/<project-slug>-wt/<purpose>/`; assign ports, databases and output separately.
