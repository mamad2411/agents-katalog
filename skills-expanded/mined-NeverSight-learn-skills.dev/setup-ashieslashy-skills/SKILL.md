---
name: setup-ashieslashy-skills
description: Add or refresh Ashie's Architect methodology in a global, project, devcontainer, or Codespace AGENTS.md after `npx skills@latest add ashieslashy/skills`. This preserves existing instructions, uses bundled canonical guidance, and includes project-memory guidance when that skill is installed for the target AGENTS.md scope.
---

# Setup AshieSlashy Skills

Set up AshieSlashy's operating guidance without silently rewriting the user's existing instructions.

The Skills CLI owns skill selection, agent selection, and global/project install scope. This setup skill does not install, select, enable, disable, or enumerate skills. It only proposes Ashie's Architect methodology from the bundled template, includes project-memory methodology guidance when that skill is installed for the target `AGENTS.md` scope, and keeps all changes review-first.

## Assets

- Architect methodology template: `assets/templates/global-architect-agents.md`

## Workflow

1. Resolve the target `AGENTS.md`:
   - Use the file the user named when they provide one.
   - Otherwise, if inside a git repository or obvious workspace, use the repository/workspace root `AGENTS.md`, not the current subdirectory.
   - For global setup, use the user's Codex `AGENTS.md` only when the user explicitly asks for global setup or no repository/workspace target applies.
   - If the target is ambiguous, ask one concise question. Do not ask the user to reselect skills or install scope; `npx skills` already handled that.
2. Load bundled assets before proposing:
   - Read `assets/templates/global-architect-agents.md` from this installed skill directory and treat it as the source candidate for Architect methodology.
   - Render the Architect methodology from the bundled template. Do not recreate, paraphrase, or infer this methodology from active session instructions, global `AGENTS.md`, memory, or conversation history.
   - Determine the target skill scope from the resolved `AGENTS.md`: project/devcontainer/Codespace targets use the target repo or workspace skill install; global targets use the global Codex skill install.
   - If `$project-memory` is installed for the target skill scope, read its bundled `assets/snippets/project-memory-methodology.md` and replace `{{PROJECT_MEMORY_METHODOLOGY}}` with that snippet. If `$project-memory` is not installed for the target skill scope, remove the placeholder.
   - A globally installed `$setup-ashieslashy-skills` may configure a project-local `AGENTS.md`; in that case, use the project-local skill state for `$project-memory`, not the global setup skill's sibling directory.
   - When file inspection is needed for a project target, check the target repo's `skills-lock.json` and `.agents/skills/`. If they disagree, surface the inconsistency in the proposal and prefer actually present skill files for rendering bundled snippets.
   - When file inspection is needed for a global target, check the global Codex skill directory that contains this setup skill and any available global skills lock/state.
   - Use an existing target `AGENTS.md`, current/global instructions, and conversation context only as merge context. Do not use them as the source for AshieSlashy's Architect methodology.
   - If active/global instructions contradict the bundled template, prefer the bundled template for Ashie-owned methodology and surface the conflict in the proposal.
   - If the bundled Architect template cannot be read or rendered, stop and report the missing asset. Do not fall back to ambient or global `AGENTS.md` prose.
3. Inspect before proposing:
   - Read the target `AGENTS.md` if it exists.
   - For project/devcontainer scope, inspect repo-local guidance enough to avoid contradicting it.
   - Notice existing generated blocks and manually maintained instructions from any collection. Preserve them unless the user explicitly asks to clean them up.
4. Apply the Architect methodology policy:
   - Architect behavior is scope-independent. Apply it to global, project, devcontainer, and Codespace targets from the same bundled template.
   - Do not weaken, omit, or reinterpret Architect behavior because the target is project-local.
   - Project-local instructions may add domain-specific constraints, but they do not disable Architect behavior unless the user explicitly asks to remove or change it.
   - Preserve stronger existing local constraints around safety, approvals, commands, secrets, validation, and project conventions. Surface conflicts instead of silently resolving them.
5. Prepare the proposal:
   - If the target `AGENTS.md` is missing, propose the rendered Architect template as the new file.
   - If the target `AGENTS.md` already has meaningful instructions, propose an intelligent merge between the rendered bundled source candidate and the existing target as merge context, rather than a blind replacement.
   - Preserve unrelated skill collection instructions. Do not generate a per-skill instruction list; installed skills are loaded from the scope selected by `npx skills`.
   - Remove duplicate or contradictory Ashie-owned setup guidance only. Preserve user/project safety rules and unrelated collection guidance unless the user explicitly approves changing them.
   - If older AshieSlashy setup prose duplicates only now-obsolete setup guidance, propose removing or replacing it, but preserve it unchanged unless the user approves.
6. Show before writing:
   - The source path used for the Architect methodology and its first non-heading sentence, so the user can verify provenance.
   - Whether project-memory guidance was included because `$project-memory` is installed for the target skill scope, or omitted because `$project-memory` is not installed for that scope.
   - Short semantic summary.
   - Unified diff, or full proposed file if creating a missing file.
   - Any conflicts, assumptions, or questions.
   - If the proposed file matches the target, report that no changes are needed and do not ask to apply.
7. Write only after explicit approval:
   - Re-read the target immediately before writing. If it changed since the diff was shown, stop and show a refreshed proposal instead of writing stale approved content.
   - Back up the existing target first when one exists, using a unique timestamped backup path that will not overwrite an earlier backup.
   - Apply the approved content exactly.
   - Tell the user to restart Codex, reload the workspace, or start a new Codex thread so the updated `AGENTS.md` is loaded.

## Boundaries

- This skill does not install skills or choose which skills are active. Use `npx skills@latest add ashieslashy/skills` for that.
- This skill does not wire installed skills into `AGENTS.md`; Codex loads installed skills from the selected install scope.
- This skill does not create the project docs memory baseline. Use `$project-memory` for that when the target repo wants one.
- Architect methodology adoption is review-first; never silently replace or substantially rewrite an existing `AGENTS.md`.
- Canonical instruction prose belongs in assets, not shell scripts.
