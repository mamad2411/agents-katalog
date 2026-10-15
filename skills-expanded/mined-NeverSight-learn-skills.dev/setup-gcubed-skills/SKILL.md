---
name: setup-gcubed-skills
description: Bootstrap/refresh MSG Architect methodology in AGENTS.md; show a review-first diff, validate, then self-remove.
---

# Setup G-Cubed Skills

Set up MSG operating guidance without silently rewriting the user's existing instructions.

The Skills CLI owns skill selection, agent selection, and global/project install scope. This setup skill does not install, select, enable, disable, or enumerate other skills. It only proposes MSG Architect methodology from the bundled template, includes project-memory methodology guidance when that skill is installed for the target `AGENTS.md` scope, keeps all changes review-first, and removes this setup skill after successful validation.

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
   - A globally installed `$setup-gcubed-skills` may configure a project-local `AGENTS.md`; in that case, use the project-local skill state for `$project-memory`, not the global setup skill's sibling directory.
   - When file inspection is needed for a project target, check the target repo's `skills-lock.json` and `.agents/skills/`. If they disagree, surface the inconsistency in the proposal and prefer actually present skill files for rendering bundled snippets.
   - When file inspection is needed for a global target, check the global Codex skill directory that contains this setup skill and any available global skills lock/state.
   - Use an existing target `AGENTS.md`, current/global instructions, and conversation context only as merge context. Do not use them as the source for MSG Architect methodology.
   - If active/global instructions contradict the bundled template, prefer the bundled template for MSG-owned methodology and surface the conflict in the proposal.
   - If the bundled Architect template cannot be read or rendered, stop and report the missing asset. Do not fall back to ambient or global `AGENTS.md` prose.
3. Inspect before proposing:
   - Read the target `AGENTS.md` if it exists.
   - For project/devcontainer scope, inspect repo-local guidance enough to avoid contradicting it.
   - When `$project-memory` is installed for the target scope, inspect the target docs memory set enough to identify durable project facts that already belong in `docs/`.
   - Notice existing generated blocks and manually maintained instructions from any collection. Preserve them unless the user explicitly asks to clean them up.
4. Apply the Architect methodology policy:
   - Architect behavior is scope-independent. Apply it to global, project, devcontainer, and Codespace targets from the same bundled template.
   - Do not weaken, omit, or reinterpret Architect behavior because the target is project-local.
   - Project-local instructions may add domain-specific constraints, but they do not disable Architect behavior unless the user explicitly asks to remove or change it.
   - Preserve stronger existing local constraints around safety, approvals, commands, secrets, validation, and project conventions. Surface conflicts instead of silently resolving them.
5. Prepare the proposal:
   - If the target `AGENTS.md` is missing, propose the rendered Architect template as the new file.
   - If the target `AGENTS.md` already has meaningful instructions, propose an intelligent merge between the rendered bundled source candidate and the existing target as merge context, rather than a blind replacement.
   - When `$project-memory` is installed, do not preserve durable project facts in `AGENTS.md` merely because they already exist there. Propose moving runtime flow, environment variable catalogs, release procedure, architecture overview, current status, roadmap, and long maintenance notes into the smallest appropriate `docs/` files, leaving `AGENTS.md` as concise guardrails plus pointers.
   - Keep project-local guardrails short and actionable: usually 5-10 bullets, one or two lines each. If a guardrail needs background, examples, runtime flow, or operational procedure, put the explanation in `docs/` and link or point to it from `AGENTS.md`.
   - Preserve unrelated skill collection instructions. Do not generate a per-skill instruction list; installed skills are loaded from the scope selected by `npx skills`.
   - Remove duplicate or contradictory MSG-owned setup guidance only. Preserve user/project safety rules and unrelated collection guidance unless the user explicitly approves changing them.
   - If older G-Cubed setup prose duplicates only now-obsolete setup guidance, propose removing or replacing it, but preserve it unchanged unless the user approves.
6. Quality-check the proposal:
   - Report the proposed `AGENTS.md` line count and word count.
   - Warn when global guidance exceeds roughly 40 lines or 500 words.
   - Warn when project-local guidance grows beyond 5-10 concise guardrail bullets or starts carrying durable project facts.
   - Flag content that should move behind progressive disclosure: long procedures, tool catalogs, environment catalogs, runtime flow, release steps, architecture overviews, current status, roadmaps, pasted transcripts, and repeated per-skill instructions.
   - Flag contradictions or weakened constraints around delegation, first-start sub-agent disclosure, approvals, destructive changes, local override order, read-only versus implementation behavior, dirty worktree preservation, validation, and secret handling.
   - Prefer warnings over hard failure, but stop when the proposal would silently weaken safety, discard user/project constraints, or contradict the bundled Architect source.
   - Include a short "kept / compressed / moved to docs or skills" summary before the diff.
7. Show before writing:
   - The source path used for the Architect methodology and its first non-heading sentence, so the user can verify provenance.
   - Whether project-memory guidance was included because `$project-memory` is installed for the target skill scope, or omitted because `$project-memory` is not installed for that scope.
   - The proposal quality-check counts, warnings, and kept/compressed/moved summary.
   - Short semantic summary.
   - Unified diff, or full proposed file if creating a missing file.
   - Any conflicts, assumptions, or questions.
   - A clear note that approval means the setup skill will re-read the target, write the approved content when changes are needed, validate the result, and then uninstall only `$setup-gcubed-skills` from the scope that supplied the running skill.
   - If the proposed file matches the target, report that no `AGENTS.md` changes are needed, skip the write and backup steps, then continue to validation and self-removal because setup is already complete.
8. Write only after explicit approval when changes are needed:
   - Re-read the target immediately before writing. If it changed since the diff was shown, stop and show a refreshed proposal instead of writing stale approved content.
   - Back up the existing target first when one exists, using a unique timestamped backup path that will not overwrite an earlier backup.
   - Apply the approved content exactly.
9. Validate the completed setup before uninstalling:
   - Re-read the target `AGENTS.md` after writing, or immediately for a no-change setup, and confirm it exactly matches the approved or already-matching proposed content.
   - Confirm no unresolved setup placeholders remain, including `{{PROJECT_MEMORY_METHODOLOGY}}`.
   - Confirm the project-memory methodology block is present or absent according to the proposal.
   - Re-run the line and word counts from the proposal and report material drift.
   - Confirm a backup path was created when the target already existed and the setup wrote changes.
   - If validation fails, stop, do not uninstall the setup skill, and report the exact issue and recovery path.
10. Remove this bootstrap skill after successful validation:
   - Remove only `$setup-gcubed-skills`, and remove it from the scope that supplied the running skill. Do not remove project workflow skills such as `$project-memory`, `$skill-capture`, `$review-synthesis`, or `$code-structure-cleanup`.
   - For a global setup skill, run `npx skills remove --global setup-gcubed-skills`.
   - For a project/devcontainer/Codespace setup skill, run `npx skills remove setup-gcubed-skills` from that project or workspace root.
   - If the running setup skill scope is ambiguous, ask one concise question before removing anything.
   - If the Skills CLI is unavailable or removal fails, leave the setup result in place, report the manual command to run, and explain that the skill remains installed until removal succeeds.
11. Finish with lifecycle guidance:
   - Tell the user validation passed, what scope the setup skill was removed from, and that this keeps future startup context lean because the durable guidance now lives in `AGENTS.md`.
   - Tell the user to restart Codex, reload the workspace, or start a new Codex thread so the updated `AGENTS.md` and skill inventory are loaded.
   - Point back to this repo's README install instructions for reinstalling `$setup-gcubed-skills` if Architect guidance needs refreshing later.

## Boundaries

- This skill does not install skills or choose which skills are active. Use `npx skills@latest add McKibbin-Software-Group/gcubed-skills` for that.
- This skill removes only itself after successful validation. It must never remove or disable unrelated skills.
- This skill does not wire installed skills into `AGENTS.md`; Codex loads installed skills from the selected install scope.
- This skill does not create the project docs memory baseline. Use `$project-memory` for that when the target repo wants one.
- Architect methodology adoption is review-first; never silently replace or substantially rewrite an existing `AGENTS.md`.
- Canonical instruction prose belongs in assets, not shell scripts.
