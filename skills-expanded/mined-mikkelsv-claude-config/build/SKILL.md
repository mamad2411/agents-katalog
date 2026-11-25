---
name: build
description: "Build and serve the application via the project's launch config. Use whenever the user says \"build\", \"run the app\", \"start the server\", or \"check if it compiles\" — or automatically after any code change per the auto-build rule. Reads .claude/launch.json and no-ops gracefully when it's absent."
---

# Build & Serve

Mechanical execution — follow the steps in order.

Execute user instructions, then build and serve the application. Reads project-specific config from the committed `.claude/skill-config/build.md`.

## Phase 1 — User Task

If the user provided instructions after `/build`, execute them fully first:

> $ARGUMENTS

If no instructions were provided, skip to Phase 2.

## Phase 2 — Build & Serve

Once the task is complete (or immediately if no task was given):

0. **Check for build config.** If `.claude/launch.json` does not exist, report "No build configured for this repo; skipping build/serve." and return success. Phase 2 ends here. The Auto-build Rule inherits this no-op for repos without a build config (e.g., docs-only or config repos).
1. Read `.claude/launch.json` for the server config (name, port, command).
2. If `.claude/skill-config/build.md` exists, read it for overrides (e.g. a separate build command that differs from the serve command). Optional — infer from `launch.json` when it's absent, and say so.
3. Stop any existing preview server (use `preview_stop` if one is running, check with `preview_list` first).
4. Kill any orphaned processes on the port (Windows: `kill-port.ps1`; elsewhere `lsof -ti :<port> | xargs kill`):

   ```bash
   pwsh -NoProfile -File "$HOME/.claude/scripts/kill-port.ps1" -Port <port>
   ```

5. Build using the build command from `.claude/skill-config/build.md` if present, otherwise infer from `launch.json` (can run in parallel with steps 3–4).
6. If the build **fails**, fix the errors and rebuild. If it still fails after 2 attempts, stop and report.
7. If the build **succeeds**, start the dev server via `preview_start` with the server name from `launch.json`. If `preview_start` fails after a successful build, re-run the port-kill step and retry once before reporting.
8. Report: "Build OK. Dev server running in preview."

## Auto-build Rule

Implements the auto-build rule — see `wf-auto-build-and-serve.md`.
