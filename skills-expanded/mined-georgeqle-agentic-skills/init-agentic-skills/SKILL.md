---
name: init-agentic-skills
description: Initialize this agentic-skills checkout on a developer machine by running the repository init script, verify global managed skill installs, uninstall repo-managed installs when requested, and route project-local pack setup to the pack skill. Use when Codex needs to make all global agentic-skills skills available on the current machine, repair stale installs, confirm initialization status, or explain how to enable packs for a project.
type: ops
version: v0.9
argument-hint: "[init|status|doctor|update|latest|--uninstall]"
---

# Init Agentic Skills

Invoke as `$init-agentic-skills`.

Initialize this `agentic-skills` checkout on the current machine by installing global core skills for both Claude and Codex. Active installs are repo-managed directories that expose the canonical `SKILL.md` and exclude `archive/`; copied managed launchers resolve this checkout through `.agentic-skills-managed` provenance. Pinned installs intentionally point at `archive/<version>`. Keep domain packs project-local; use `$pack` from the target project or `npx skillpacks install <pack-or-skill>` from the project shell when packs are needed.

## Process

1. Parse `$ARGUMENTS`:
   - No args, `init`, `refresh`, or `sync`: run `scripts/init-agentic-skills.sh`, then run the first-run setup prompts in step 6 when the drift preferences are still unset.
   - `status`: run `scripts/init-agentic-skills.sh status`, then report the local checkout commit, remote URL, and whether GitHub freshness is enabled by `~/.agentic-skills/preferences.json` at `sync.github_freshness_check`.
   - `doctor`: run `scripts/init-agentic-skills.sh doctor` to report global skill-install drift (read-only). It compares installed `~/.claude/skills` and `~/.codex/skills` copies against canonical `global/<tool>/<skill>` via the `.agentic-skills-managed` marker's `source_sha`. Report `stale` skills with the fix `$init-agentic-skills update`, `unknown` skills as needing a re-init to enable tracking, and `pinned` skills as frozen.
   - `update` or `latest`: run `scripts/init-agentic-skills.sh update` only after confirming the user wants to check GitHub, fast-forward the local checkout, and rerun `init.sh`. This re-copy is the global "refresh" — it rewrites markers with current `source_version`/`source_sha`, clearing drift.
   - `--uninstall`, `uninstall`, or `remove`: run `scripts/init-agentic-skills.sh --uninstall` only after confirming the user wants repo-managed global installs removed.
   - `help`, `--help`, or `-h`: run `scripts/init-agentic-skills.sh --help`.
2. Report the initializer command, the Claude and Codex skill directories, installed/skipped counts, and warnings about non-repo-managed collisions.
3. Explain pack access separately:
   - Do not install `packs/*` globally.
   - In the project that needs domain workflows, run `$pack` for guided setup, or `npx skillpacks install <pack-or-skill>` from the project shell for an explicit pack or individual pack skill.
   - If a project already has `.agents/project.json`, use `$pack refresh` after this global initialization to recreate local pack skill roots.
4. If the active session still cannot see a newly installed or refreshed skill, report the skill-visibility reload path:
   - Claude Code: run `/reload-skills` first; `/clear` starts a new empty-context conversation and can pick up the refreshed registry; restart if the top-level `.claude/skills` directory did not exist at session start or the skill is still invisible.
   - Codex: start a fresh Codex CLI session if the `$` skill list remains stale.
5. For `update` / `latest` mode:
   - Confirm before running commands that fetch, pull, or reinstall.
   - Fetch GitHub freshness, compare the local checkout to `origin/HEAD`, and update only with a fast-forward-only operation such as `git pull --ff-only` or an equivalent `git fetch` + `git merge --ff-only`.
   - If the update cannot fast-forward cleanly, stop and report the exact reason without rebasing, merging, stashing, or force-resetting.
   - After a successful fast-forward, rerun `init.sh`.
   - Warn that Claude Code should use `/reload-skills` first, then `/clear` or restart if needed, and that Codex should start a fresh Codex CLI session if the `$` skill list remains stale.
6. First-run drift preferences (init / clone setup):
   - Default policy is **track-latest** (installed skills follow canonical; drift is observable). The two prompts below are **opt-in and off by default**, so the explicit-control default stays out of the box.
   - Only prompt when the preference keys are still unset. Check with `scripts/init-agentic-skills.sh show-prefs`; skip silently when both are already set.
   - Ask (a): "Enable a session-start hook that warns when tracked skills are behind canonical?" Default **no**.
     - If yes: run `scripts/init-agentic-skills.sh hook enable` (registers a `SessionStart` hook in `~/.claude/settings.json` invoking `scripts/skill-drift-hook.sh` and sets `skills.session_start_hook=true`).
     - If no: run `scripts/init-agentic-skills.sh set-pref session_start_hook false`.
   - Ask (b): "Auto-refresh latest skills on session start (instead of just warning)?" Default **no**.
     - Run `scripts/init-agentic-skills.sh set-pref auto_refresh <true|false>` with the answer. Auto-refresh only takes effect when the hook is enabled.
   - To disable later: decline the prompt, run `scripts/init-agentic-skills.sh set-pref session_start_hook false`, or run `scripts/init-agentic-skills.sh hook disable` to remove the settings entry.

## Constraints

- Delegate global initialization to `scripts/init-agentic-skills.sh`; do not recreate install logic by hand.
- Do not overwrite real directories or files under `~/.claude/skills`, `~/.codex/skills`, `.claude/skills`, or `.codex/skills`.
- Treat packs as project-local capabilities managed by `scripts/pack.sh` through `$pack`.
- Stop and report exact errors if the launcher cannot resolve the repository root or if root `init.sh` fails.
- Do not install `packs/*` globally in any mode.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
