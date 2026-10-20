---
name: plan-setup
description: >
  Set up or resume missing Ultimate SDD project scaffolding without replacing
  existing work. Use when onboarding a greenfield or brownfield repo, repairing
  missing setup artifacts, inspecting project policy, or running /ultimate-sdd:setup.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

Set up the target project, not the plugin or global agent rules.

**Read:** `references/recovery.md` for setup/configuration contracts and `references/model.md` for plugin and plan-root resolution.

## Procedure

1. Resolve the target repo and plan root. Read applicable project instructions, README, existing plan context, configuration, and workflow before writing anything.
2. Bound the scan to root manifests and the entry points relevant to the requested work. Classify greenfield vs brownfield from inspected evidence, not the folder name. Reuse existing context rather than rescanning unrelated areas.
3. Summarize the verified product/stack, relevant modules, and documented build/test commands with `path:line` evidence. Separate `[inferred]` observations and unresolved gaps. Do not guess a stack or executable command. In a greenfield repo, record only user-selected or otherwise evidenced choices; leave undecided choices open.
4. Run non-destructive setup with the supplied project title:

   ```
   python <plugin>/scripts/sdd.py setup --repo <target> --root docs/plan --title "Project title" --json
   python <plugin>/scripts/sdd.py config --repo <target> --root docs/plan --json
   python <plugin>/scripts/sdd.py doctor --repo <target> --root docs/plan --json
   ```

   Replace placeholders and quote paths as needed. Substitute the resolved plan root if it is not `docs/plan`. Common flags follow the subcommand.
5. Report created vs preserved artifacts and any remaining setup/configuration errors. Existing context, configuration, and workflow stay intact; rerunning setup fills missing artifacts rather than resetting the project. Do not hide malformed existing state by replacing it.
6. If the platform map is missing, use `plan-context` with the bounded evidence already gathered. Preserve an existing map; offer a targeted context refresh separately. The workflow is project-owned guidance, not permission to rewrite repository instructions or install global rules.

## Guardrails

- Skip secrets, generated output, dependencies, and irrelevant subtrees. Record scan coverage and gaps rather than forcing a style inventory.
- Configuration uses schema version 1 and the defaults in `references/recovery.md`. Report the effective values, not assumed runtime capabilities.
- Store test commands only when evidenced, as arrays of argv. Setup/configuration/doctor do not automatically execute them.
- No application code changes, overwrites of existing context/configuration/workflow, dependency installs, automatic git initialization, or commits.
- Do not create speculative REQs or TASKs just to finish onboarding. Report unresolved choices and the next supported planning action.
