---
name: repo-init-official
description: "Use inside repo-init-scan to try a target-local `init` skill, Claude `/init`, or `copilot init`, normalize official init output into `.github/instructions/project.instructions.md`, and decide whether manual fallback is still needed."
---

# Repo Init Official

## Immediate Execution Rule

When this stage has just been loaded inside `repo-init-scan`, the next assistant action must attempt the official initializer or report `official_init_unavailable`, then emit `## Repo Init Official`. Do not stop at `Skill(...repo-init-official...) Successfully loaded`, and do not inspect business source before this stage returns.

## Contract

- This is the best-copilot official-init stage. Loading `/best-copilot:repo-init-official` or `Skill(best-copilot:repo-init-official)` makes this stage's instructions available; it is not the same thing as running the runtime's built-in `/init`.
- Try a target-local `init` skill first when it is discoverable and the active runtime can invoke skills non-interactively. This means `skills/init/SKILL.md` for Claude Code and Copilot plugin directories, plus `.claude/skills/init/SKILL.md` for Claude Code. For Copilot CLI, `skills/init/SKILL.md` is mechanically invokable only when the target root is a plugin directory with `plugin.json`; otherwise report `local_init_skill_status=uninvokable_missing_plugin_json` and fall back to `copilot init`. Invoke successful candidates from the target root through the bundled official helper, record `attempted=target_local_init_skill`, and treat them as successful only when a recognized init artifact is written on disk.
- In Copilot CLI or other shell-capable runtimes, if no target-local `init` skill succeeds and `copilot init` exists, run `copilot init` automatically before manual fallback through `repo-init-official/scripts/run-copilot-native-init.sh`. This is the normal command fallback for Copilot.
- In Claude Code, if no target-local `init` skill succeeds, attempt Claude Code's built-in `/init` command automatically through the bundled helper script before manual fallback when the helper path is discoverable from `CLAUDE_SKILL_DIR` or the active plugin directory. This is the native command shown by Claude as "Initialize a new CLAUDE.md file with codebase documentation"; it is not a best-copilot skill. The helper uses a bounded `claude --bare --permission-mode acceptEdits -p "/init"` attempt so the native Claude initializer can write the target `CLAUDE.md` without loading this plugin recursively. `BEST_COPILOT_CLAUDE_NATIVE_INIT_TIMEOUT_SECONDS` may shorten the default 45-second timeout for smoke tests. If the helper cannot be located, report `official_init_unavailable` and continue to manual fallback instead of blocking solely on helper discovery.
- Prefer a directly invokable bare runtime `/init` command when the active session exposes one. This bare `/init` is distinct from best-copilot plugin skills such as `/repo-init-official` or `/best-copilot:repo-init-official`.
- Normalize useful output into the target `.github/instructions/project.instructions.md` when the official initializer produces enough facts directly. Recognized helper artifacts such as target `CLAUDE.md`, `.github/copilot-instructions.md`, and `AGENTS.md` are also successful official evidence; `repo-init-manual-fallback` must then preserve and normalize their useful facts into `.github/instructions/project.instructions.md`.
- Do not treat chat output alone as success. Either the facts file must exist on disk with real facts or explicit `unknown` gaps, or the helper must have written a recognized artifact that the manual fallback can normalize.
- In Claude Code, do not report `official_init_unavailable` merely because the assistant cannot call a UI slash command directly. First try the helper script. If the helper succeeds and creates `.github/instructions/project.instructions.md`, `CLAUDE.md`, `AGENTS.md`, or another recognized init artifact, report `success`.
- In Copilot CLI, do not report `official_init_unavailable` merely because the assistant loaded this skill text. First try the target-local `init` skill when present, then `copilot init` through the bundled helper when the shell command is available. If the helper succeeds and creates `.github/instructions/project.instructions.md`, `.github/copilot-instructions.md`, `AGENTS.md`, or another recognized init artifact, report `success`.
- Report `official_init_unavailable` only when no official initializer is available or known in the current runtime, no `copilot init` command can be run, and no prior `/init` / `copilot init` output or artifacts are available to normalize.
- If official init runs but only returns chat text without a verified facts file, fails, times out, or reports missing authentication, report `official_init_no_write`, `official_init_incomplete`, or `official_init_unavailable` and continue to `repo-init-manual-fallback`. Do not stop after loading this skill.
- If official init is unavailable, does not write the file, or leaves those fact categories incomplete, hand off to `repo-init-manual-fallback`.
- This stage does not certify scaffold completeness and does not write `best-copilot.md`; those remain owned by `repo-init-manual-fallback`.

## Output

```markdown
## Repo Init Official
- status: success|official_init_unavailable|official_init_no_write|official_init_incomplete
- attempted: target_local_init_skill|copilot_init|claude_native_slash_init|bare_init|none
- native_command: /init when attempted=claude_native_slash_init
- native_command: copilot init when attempted=copilot_init
- artifacts: <files created or normalized, such as CLAUDE.md, .github/copilot-instructions.md, and .github/instructions/project.instructions.md>
```

When a target-local `init` skill is present but does not write a recognized artifact, the helper may continue to the runtime command fallback. In that case `attempted` may contain a comma-separated attempt chain such as `target_local_init_skill,claude_native_slash_init`.
