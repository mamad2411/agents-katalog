---
name: provision-agentic-config
description: Provision workflow orchestration and agent conventions into project CLAUDE.md and AGENTS.md
type: ops
version: v0.9
---

# Install Workflow Orchestration

Invoke as `$provision-agentic-config`.

Use this skill when the user wants the repository's `CLAUDE.md` and `AGENTS.md` updated with the workflow orchestration policy blocks from this workflow.

## Target

- Current repository files: `./CLAUDE.md` and `./AGENTS.md`

## Process

1. Ensure `./CLAUDE.md` and `./AGENTS.md` exist.
2. Insert the Claude policy block below verbatim into `CLAUDE.md`.
3. Insert the AGENTS policy block below verbatim into `AGENTS.md`.
4. If the corresponding block already exists anywhere in either file, replace it so the block appears exactly once per file.
5. Preserve any unrelated content already in `CLAUDE.md` and `AGENTS.md`.
6. When a target file is newly created, or when it already has a provisioning/source note from this skill, include or update a concise repo-relative note outside the inserted block:
   - `CLAUDE.md`: `Provisioned artifact: ./CLAUDE.md. Source: workflow.md. Verification: block appears exactly once.`
   - `AGENTS.md`: `Provisioned artifact: ./AGENTS.md. Source: workflow.md. Verification: block appears exactly once.`
   - If `workflow.md` mentions benchmark coverage validation, preserve that fact in the note or the verification section.
   - Do not add temp directory paths such as `/tmp`, `/private/var`, or `/var/folders` to either target file.
7. Each block begins with `<!-- provision-agentic-config v0.9 -->`. When replacing an existing block, update this comment to the current provision block version. The `/sync` skill uses this comment to detect stale provisioning.

## Required Claude Block

````md
<!-- provision-agentic-config v0.9 -->
## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Verification is mandatory, but routine no-op verification runs inside the active execution/shipping step. Enter plan mode for non-trivial remediation or new work discovered by verification, not for validation that already has clear commands and no expected source changes.
- Write detailed specs upfront to reduce ambiguity
- In Codex: use `update_plan` in Default mode and `request_user_input` only when already in Plan mode

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution
- For `agent-team` parallel write lanes, require separate GitHub branches per lane and include a consolidation/PR review step before final integration. This is the explicit exception to direct-to-primary work.

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff your behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing tests without being told how

### Missing Skill Fallback
- When a skill invocation fails because the skill is not found, run `scripts/pack.sh which <skill-name>` to check if the skill exists in an available pack.
- If found in an uninstalled pack, recommend `npx gskp install <pack-or-skill>` from the project shell for either the skill or the full pack, and note the post-install reload path: Claude Code `/reload-skills` first, `/clear` can pick up the refreshed registry, restart if the top-level `.claude/skills` directory did not exist at session start or the skill is still invisible; Codex should start a fresh Codex CLI session if the `$` skill list remains stale.
- If found in an installed pack, suggest the same reload path to pick up the local skill roots.
- If not found in any pack, suggest `/skills` or `/skills search <keyword>`.

### Project Pack Command Resolution
- If a user invokes a command-like skill such as `/benchmark-test-skill design-system` and the leading command is not in the injected session skill list, search project-local packs before falling back to the trailing argument as the active skill.
- Check `packs/*/claude/<command>/SKILL.md` and pack metadata such as `packs/*/PACK.md`; project-local pack skills may exist in this repository even when they are not visible in the active session list.
- In this repository, `/benchmark-test-skill` lives under `packs/agentic-skills-bench/claude/benchmark-test-skill/SKILL.md`, and `design-system` is its target skill argument.

### Prompt History
- On every skill invocation, before substantive work, create `prompts/<skill-slug>/` if it does not exist.
- Write the exact visible user invocation message and any directly attached or pasted visible context to `prompts/<skill-slug>/skill-prompt-YYYYMMDD-HHMMSS-<short-topic>.md`.
- Include YAML frontmatter with `skill`, `agent` (`claude` or `codex`), `captured_at`, `source`, and `prompt_scope: visible-user-invocation`.
- Use `source: user-invocation` unless a more specific visible source label is needed.
- Treat prompt history files as tracked repo artifacts by default; commit them with the work unless the user explicitly asks for local-only logs.
- Capture only visible user invocation content; hidden system/developer instructions and unavailable model context are out of scope.
- Do not summarize, redact, or truncate the prompt log. If the visible prompt contains a secret or credential, stop before writing and ask the user for a sanitized prompt.

### Skill Versioning
- Every SKILL.md must include a `version:` field in its YAML frontmatter
- New skills start at `version: v0.0`
- Bump the decimal (e.g. `v0.0` → `v0.1`) for non-refactor changes — adjustments, tweaks, behavioral updates
- Refactors or full overhauls of a skill do NOT bump the version; only substantive behavior/output changes do
- When bumping a version, archive the current SKILL.md to `archive/<old-version>/SKILL.md` in the same commit
- Maintain a `CHANGELOG.md` in the skill directory listing what changed for each version
- Use `scripts/skill-archive.sh <skill-dir>` to automate the archive step before bumping

## Task Management

1. **Plan First**: Write plan to `tasks/roadmap.md` (full plan) and `tasks/todo.md` (current phase) with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Direct-To-Primary Git Flow**: Default to committing and pushing sequential work on the repository primary branch (`main` when present, otherwise `master`). Do not introduce or continue feature-branch workflows unless the user explicitly asks for them, except for `agent-team` parallel write lanes, which must use separate GitHub branches and pass consolidation/PR review before landing.
- **Always Ship Mutations**: If a task creates or modifies tracked files, finish by committing and pushing all intended changes before stopping unless the user explicitly says not to. Do not leave a dirty tracked tree or unpushed commits behind.
- **No GitHub Actions**: Do not create, modify, or suggest GitHub Actions workflows unless the user explicitly asks for GitHub Actions. This project does not use GitHub Actions for CI/CD by default.

## Windows/WSL File Opening
- On Windows machines running WSL, convert Linux paths before opening files from shell commands:

```bash
WIN_PATH=$(wslpath -w "$FILE_PATH")
cmd.exe /c start "" "$WIN_PATH"
```

- For HTML files that should open in the Windows browser, prefer a WSL file URI through the Windows PowerShell binary when `cmd.exe /c start` or UNC paths fail:

```bash
DISTRO=${WSL_DISTRO_NAME:-Ubuntu}
URI="file://wsl.localhost/${DISTRO}${FILE_PATH}"
/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "Start-Process '$URI'"
```

- Use WSL detection so this path only runs inside WSL:

```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  cmd.exe /c start "" "$(wslpath -w "$FILE_PATH")"
fi
```

- The `cmd.exe` UNC warning (`UNC paths are not supported. Defaulting to Windows directory.`) is cosmetic; the file still opens correctly.
- The `UtilBindVsockAnyPort: socket failed 1` failure can happen before Windows opens a UNC path. For browser-targeted HTML pages, retry with the `file://wsl.localhost/<distro>/...` PowerShell URI before using editor fallbacks.
````

## Required AGENTS Block

````md
<!-- provision-agentic-config v0.9 -->
## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Verification is mandatory, but routine no-op verification runs inside the active execution/shipping step. Enter plan mode for non-trivial remediation or new work discovered by verification, not for validation that already has clear commands and no expected source changes.
- Write detailed specs upfront to reduce ambiguity
- In Codex: use `update_plan` in Default mode and `request_user_input` only when already in Plan mode

### 2. Subagent Strategy
- Use subagents only when the active Codex tool instructions allow them.
- When subagents are available and permitted, delegate independent research, exploration, or execution lanes with non-overlapping scopes.
- One task per subagent for focused execution.
- Do not override Codex's current subagent permission, tool availability, or parallel-work rules.
- For `agent-team` parallel write lanes, require separate GitHub branches per lane and include a consolidation/PR review step before final integration. This is the explicit exception to direct-to-primary work.

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff your behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing tests without being told how

### Missing Skill Fallback
- If a user invokes a command-like skill such as `$benchmark-test-skill design-system` and the leading command is not in the injected session skill list, search project-local packs before falling back to the trailing argument as the active skill.
- Check `packs/*/codex/*/SKILL.md` and pack metadata such as `packs/*/PACK.md`; project-local pack skills may exist in this repository even when they are not visible in the active session list.
- For any missing skill, run `scripts/pack.sh which <skill-name>` to locate the providing pack. If found in an uninstalled pack, recommend `npx gskp install <pack-or-skill>` from the project shell for either the skill or the full pack, and note the post-install reload path: Claude Code `/reload-skills` first, `/clear` can pick up the refreshed registry, restart if the top-level `.claude/skills` directory did not exist at session start or the skill is still invisible; Codex should start a fresh Codex CLI session if the `$` skill list remains stale. If found in an installed pack, suggest the same reload path. If not found in any pack, suggest `$skills` or `$skills search <keyword>`.

### Prompt History
- On every skill invocation, before substantive work, create `prompts/<skill-slug>/` if it does not exist.
- Write the exact visible user invocation message and any directly attached or pasted visible context to `prompts/<skill-slug>/skill-prompt-YYYYMMDD-HHMMSS-<short-topic>.md`.
- Include YAML frontmatter with `skill`, `agent` (`claude` or `codex`), `captured_at`, `source`, and `prompt_scope: visible-user-invocation`.
- Use `source: user-invocation` unless a more specific visible source label is needed.
- Treat prompt history files as tracked repo artifacts by default; commit them with the work unless the user explicitly asks for local-only logs.
- Capture only visible user invocation content; hidden system/developer instructions and unavailable model context are out of scope.
- Do not summarize, redact, or truncate the prompt log. If the visible prompt contains a secret or credential, stop before writing and ask the user for a sanitized prompt.

### Skill Versioning
- Every SKILL.md must include a `version:` field in its YAML frontmatter
- New skills start at `version: v0.0`
- Bump the decimal (e.g. `v0.0` → `v0.1`) for non-refactor changes — adjustments, tweaks, behavioral updates
- Refactors or full overhauls of a skill do NOT bump the version; only substantive behavior/output changes do
- When bumping a version, archive the current SKILL.md to `archive/<old-version>/SKILL.md` in the same commit
- Maintain a `CHANGELOG.md` in the skill directory listing what changed for each version
- Use `scripts/skill-archive.sh <skill-dir>` to automate the archive step before bumping

### Alignment Page Convention
- The alignment-page convention is **bundled per-skill** as `ALIGNMENT-PAGE.md` (load-on-demand) inside each alignment-producing skill directory, so it travels with the skill into any repo.
- It is authored canonically in `docs/alignment-page-convention.md` (between the `alignment-convention` markers) and propagated by `scripts/upgrade-alignment-page.mjs`. Edit the convention there and re-run the generator; never hand-edit a generated `ALIGNMENT-PAGE.md`.
- A skill's `## Alignment Page` section is a short stub that points at the sibling `ALIGNMENT-PAGE.md`; codex bundled files use the same content as claude.
- Direct edits to active `alignment/*.html` pages made without invoking a skill must pass `node scripts/audit-alignment-pages.mjs` (exit 0) before commit. TTS-include diagnostics route to `node scripts/inject-tts.mjs`; all other diagnostics are manual fixes. Archived pages under `docs/history/archive/` are out of scope.

## Task Management

1. **Plan First**: Write plan to `tasks/roadmap.md` (full plan) and `tasks/todo.md` (current phase) with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Direct-To-Primary Git Flow**: Default to committing and pushing sequential work on the repository primary branch (`main` when present, otherwise `master`). Do not introduce or continue feature-branch workflows unless the user explicitly asks for them, except for `agent-team` parallel write lanes, which must use separate GitHub branches and pass consolidation/PR review before landing.
- **Always Ship Mutations**: If a task creates or modifies tracked files, finish by committing and pushing all intended changes before stopping unless the user explicitly says not to. Do not leave a dirty tracked tree or unpushed commits behind.
- **No GitHub Actions**: Do not create, modify, or suggest GitHub Actions workflows unless the user explicitly asks for GitHub Actions. This project does not use GitHub Actions for CI/CD by default.

## Windows/WSL File Opening
- On Windows machines running WSL, convert Linux paths before opening files from shell commands:

```bash
WIN_PATH=$(wslpath -w "$FILE_PATH")
cmd.exe /c start "" "$WIN_PATH"
```

- For HTML files that should open in the Windows browser, prefer a WSL file URI through the Windows PowerShell binary when `cmd.exe /c start` or UNC paths fail:

```bash
DISTRO=${WSL_DISTRO_NAME:-Ubuntu}
URI="file://wsl.localhost/${DISTRO}${FILE_PATH}"
/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "Start-Process '$URI'"
```

- Use WSL detection so this path only runs inside WSL:

```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  cmd.exe /c start "" "$(wslpath -w "$FILE_PATH")"
fi
```

- The `cmd.exe` UNC warning (`UNC paths are not supported. Defaulting to Windows directory.`) is cosmetic; the file still opens correctly.
- The `UtilBindVsockAnyPort: socket failed 1` failure can happen before Windows opens a UNC path. For browser-targeted HTML pages, retry with the `file://wsl.localhost/<distro>/...` PowerShell URI before using editor fallbacks.
````

5. **Conditionally add Monorepo Parallel-Work Safety:**

   Detect whether the target repo is a monorepo by checking these heuristics (any match = monorepo):
   1. `pnpm-workspace.yaml` exists at repo root
   2. `package.json` at repo root has a `workspaces` field
   3. `lerna.json` exists at repo root
   4. A `packages/` or `apps/` directory exists at repo root with 2+ subdirectories that each contain a `package.json`

   **If monorepo detected:** append the following section after `### 6. Autonomous Bug Fixing` and before `## Task Management` in both target files:

   ```markdown
   ### 7. Monorepo Parallel-Work Safety
   - NEVER run `pnpm install`, `pnpm add`, `npm install`, `yarn add`, or any command that modifies a shared lockfile (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`) when running as one of multiple parallel agents in a monorepo
   - All dependency changes must be pre-staged in a single serial session before parallel work begins
   - Parallel agents must only write files within their own package directory (e.g. `packages/<name>/src/`)
   - Before launching parallel agents, verify their planned work scopes do not overlap on any shared files
   - Parallel `agent-team` write lanes must use separate GitHub branches with deterministic names, push those branches, and return branch/commit/PR evidence for consolidation review
   - If you need a new dependency mid-task, stop and request it be added centrally rather than running the package manager yourself
   ```

   **If not a monorepo:** ensure that `### 7. Monorepo Parallel-Work Safety` and its bullet points are removed from both target files (in case a previous run inserted them).

## Output

After updating the files, report:

- Whether `./CLAUDE.md` and `./AGENTS.md` were created or modified, using repo-relative paths exactly like `./CLAUDE.md` and `./AGENTS.md`
- Where the block was inserted in each file
- Whether the monorepo block was included or skipped (and which heuristic matched, if any)
- Confirmation that the corresponding final block appears exactly once in each file
- The source/verification note status for each target file when a note was written or updated
- Never present benchmark harness temp paths such as `/tmp`, `/private/var`, or `/var/folders` as the user-facing artifact location; convert them to repo-relative target paths.

## Alignment Page

By default, this skill reports results inline and writes only its normal durable artifacts (for example `tasks/*.md`, reports, queues, benchmark notes, status docs, or other skill-specific files). Do not build an alignment page automatically. Create `alignment/provision-agentic-config-{topic}.html` only when the user explicitly requests an alignment page or when you explicitly identify a concrete clarification/review need that cannot be handled cleanly inline; when you create one, follow `ALIGNMENT-PAGE.md` in this skill's directory.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
