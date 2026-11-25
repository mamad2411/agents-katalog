---
name: repo-init-manual-fallback
description: "Use inside repo-init-scan after the official stage whenever scaffold verification, bounded repair, or `best-copilot.md` rewrite is still needed."
---

# Repo Init Manual Fallback

Use this stage inside `repo-init-scan` whenever scaffold verification, bounded repair, or `best-copilot.md` rewrite is still needed. After official init succeeds, this stage still owns the final scaffold verification barrier and sentinel rewrite.

## Immediate Execution Rule

When this stage has just been loaded inside `repo-init-scan`, the next assistant action must create/repair/verify the required init artifacts or return `BLOCKED`, then emit `## Repo Init Manual Fallback`. Do not stop at `Skill(...repo-init-manual-fallback...) Successfully loaded`, and do not inspect business source except the bounded evidence allowed below.

## Boundary

- This stage is fail-closed. Do not continue to requirements analysis, planning, implementation, or security rewrites until the required files have been created or a `BLOCKED` result has been returned.
- Reading package/build files is allowed only as bounded evidence for creating `.github/instructions/project.instructions.md`.
- Write persistent state into the target repository, never into the plugin installation/cache directory.
- Loading this skill or the bootstrap skills is not enough. Success requires actual create/repair operations followed by path and content checks on disk.
- In shell-capable runtimes, first run the bundled deterministic helper when its path is discoverable. If it cannot be located, perform the documented create-or-repair fallback inline instead of blocking.
- If `target-instructions-bootstrap`, `target-memory-bootstrap`, or `target-spec-bootstrap` cannot be invoked mechanically, read their `SKILL.md` templates and perform the documented create-only repair inline.
- Do not hand-write improvised versions of scaffold files. When creating files inline (no shell helper), use the exact template content from `inline-templates-reference.md`. When a template is not there, read the corresponding bootstrap skill for the full template before writing.
- The `best-copilot.md` sentinel must be written ONLY after all runtime-required artifacts exist and pass content verification.
- **PM inline analysis requirement**: When creating `.github/instructions/project.instructions.md` inline (no shell helper), the PM MUST analyze the target repository before writing. Do NOT write "unknown" for fields that can be determined by reading the repository:
  1. Read the root build file (`pom.xml`, `build.gradle`, `package.json`, `go.mod`, etc.) for build system, modules, dependencies.
  2. For Maven: parse `<modules>` from root pom.xml, identify main module, find `@SpringBootApplication` or `main()`.
  3. Search for security/auth files (`*Security*`, `*Auth*`, `*OAuth*`, `WebSecurityConfig*`).
  4. Read `application.yml`, `application.properties`, Docker files for runtime requirements.
  5. Infer build/test commands from build file and wrapper scripts (`mvnw`, `gradlew`).
  6. Record genuine `unknown` only for things undetectable without running the application.
  - A `project.instructions.md` with more than 3 "unknown" values for detectable fields is a protocol violation.
- **PM post-script enhancement**: When the shell helper creates `.github/instructions/project.instructions.md` but the file contains "unknown" for detectable fields, the PM MUST read the file, analyze the target repository, and update those fields with real data. Do not accept shell-script "unknown" for fields determinable by reading source files.

## Sentinel Ownership

This skill owns constructing target-root `best-copilot.md`. The companion `repo-init-gate` skill owns validating it, and `repo-init-scan` owns orchestrating when this stage may write it.

## Required First-Use Artifacts

Before `next_task_ready: yes`, verify these paths in the target repository:

- `.github/instructions/project.instructions.md`
- `.github/instructions/must.instructions.md`
- `.github/instructions/skills-index.instructions.md`
- `CLAUDE.md` (when Claude Code compatibility is required)
- `AGENTS.md` (when Codex compatibility is required)
- `.codex/agents/senior-project-expert.toml`, `.codex/agents/technical-architect.toml`, `.codex/agents/developer.toml`, `.codex/agents/frontend-designer.toml`, `.codex/agents/quality-assurance-expert.toml`, `.codex/agents/security-reviewer.toml`, `.codex/agents/specification-writer.toml`, `.codex/agents/root-cause-fixer.toml` (when Codex compatibility is required)
- `memories/README.md`, `memories/repo/INDEX.md`, `memories/repo/current-workstreams.md`, `memories/repo/project-state.md`, `memories/repo/workflow-rules.md`, `memories/repo/decisions.md`, `memories/repo/logs/README.md`, `memories/repo/archive/deprecated-decisions.md`
- `spec/INDEX.md`, `spec/templates/requirements-template.md`, `spec/templates/design-template.md`, `spec/templates/tasks-template.md`

`best-copilot.md` is the verified-init sentinel for contract version `0.8.0`. Must be written only after the other runtime-required artifacts and content checks pass. The canonical write content is the exact 3-line YAML frontmatter block -- no headings, descriptions, or dates. Repeat-request readers use only the frontmatter version for the cheap skip decision.

## Required Content Checks

- `must.instructions.md` contains: `## Request Flow`, `## Per-Request Hard Gates`, `### PM Native Ask Trigger Gate`, `## Shared State Contracts`, `## Search Precision`, `## Command Output Budget`, `## Memory And Spec`, `## Agents and Dispatch`, `## Implementation and Verification`, plus `NEEDS_USER_INPUT`, `BLOCKED`, `work_mode`, `task_type`, `pm_action`, `fixed-string-before-regex`, `vscode_askQuestions`, `Self-evolution`, and `evolution_signal`.
- `skills-index.instructions.md` contains bootstrap routing and `## Claude Code Skill Names`.
- `CLAUDE.md` references all three `.github/instructions/` files (when Claude Code compatibility is required).
- `AGENTS.md` references `.codex/agents/*.toml`, and every Codex TOML adapter has the expected `name = "<role>"` field (when Codex compatibility is required).

## Steps

1. Start from the current `.github/instructions/project.instructions.md` when it already exists and passed the official-init success bar:
   - Reuse that file as the primary fact packet.
   - Scan only the missing fact categories, missing scaffold surfaces, or unresolved `unknown` gaps.
2. Otherwise do a bounded manual scan:
   - Read `CLAUDE.md`, `.github/copilot-instructions.md`, or `AGENTS.md` first when `repo-init-official` created or updated one.
   - Read `README*`, package/build files, CI files, app entrypoints, test directories.
   - Record unresolved facts as `unknown` instead of guessing.
3. **PM must analyze the project** to produce real project facts in `.github/instructions/project.instructions.md`. Skip this step only if the file already came from official init (step 1) and has no more than 3 "unknown" fields. Otherwise:
   - If the file already exists from the shell helper, read it and enhance any "unknown" fields.
   - If the file does not exist, analyze the project first, then create it.
   - Read `pom.xml`/`build.gradle`/`package.json` for build system, modules, dependencies.
   - For Maven: parse `<modules>`, find main module, find `@SpringBootApplication`.
   - Search for security/auth files, runtime config (`application.yml`, Docker files).
   - Infer build/test commands. Only mark genuinely undetectable items as `unknown`.
4. Create or repair `.github/instructions/project.instructions.md` with: `Project Facts`, `Build and Test Commands`, `Runtime and Entry Points`, `Module Boundaries`, `Known Unknowns`, `Verification Notes`, and `Init Status`.
5. Replace markers with `Init source: manual_fallback|official_init_plus_manual_fallback` and a real timestamp.
6. Ensure `## Init Status` contains: `Init ready`, `Required artifacts verified`, `Bootstrap contract version: 0.8.0`, `Last full verification`, `Reentry rule`.
7. Initialize missing scaffolds: shell helper → `target-instructions-bootstrap` → `target-memory-bootstrap` → `target-spec-bootstrap`.
8. Re-check the required artifact paths on disk.
9. Re-check the required instruction content.
10. After all other artifacts and content checks pass, write `best-copilot.md` with the exact sentinel.
11. Verify: `project.instructions.md` exists and is not placeholder-heavy, `Init Status` has version `0.8.0`, `best-copilot.md` matches sentinel, and `verified_paths` covers the full runtime-required path set.

## Inline Fallback Templates

When the shell helper and bootstrap skills are unavailable, read `inline-templates-reference.md` in this skill directory for the canonical templates. Do NOT improvise content.

## Output

```markdown
## Repo Init Manual Fallback
- status: success|blocked
- required_artifacts_verified: yes|no
- sentinel_written: yes|no
- next_task_ready: yes|no
- verified_paths: <every required artifact checked on disk, plus best-copilot.md>
- missing_paths: none|<paths not present or not content-valid>
```
