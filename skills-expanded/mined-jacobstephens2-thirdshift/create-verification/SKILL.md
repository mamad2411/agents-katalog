---
name: create-verification-skill
description: "Create a project-local verification skill and feature map for an app surface."
disable-model-invocation: true
---

# Create a verification skill

Imported from [Cursor pstack](https://github.com/cursor/plugins/blob/eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10/pstack/skills/create-verification-skill/SKILL.md)
at `eb4db2b55b2b7dec3d9282754cddf0a56bf4ff10`; [MIT license](LICENSE).
Local adaptation: target `.agents/skills/verify-<app>/` (separate from Factory `skills/`),
align generated skills with `verify-ui` (Factory: `thirdshift-verify-ui`), and edit using `/writing-for-agents`.

Every app surface needs a scripted way to boot cleanly, drive real user paths, and capture proof. Generate a project-local `.agents/skills/verify-<app>/` skill written for an agent reading cold mid-task, deferring shared recording and upload mechanics to `verify-ui` (Factory: `thirdshift-verify-ui`) and `pr` (Factory: `thirdshift-pr`) rather than duplicating them.

## 1. Interview the repo, not the user

Answer these from code, tests, scripts, and docs; ask the user only what cannot be observed:

- **Surface:** identify each user-facing surface (web UI, CLI/TUI, API, desktop). Multi-surface repositories get one `verify-<app>` skill per surface.
- **Run:** find build, seed, and start commands in repository scripts, Makefiles, and READMEs. Record how the app binds an OS-assigned ephemeral port (`127.0.0.1:0` or repo equivalent) and signals usable readiness from an empty `mktemp -d` state. Note whether flow setup needs optional host-only faux credentials from `~/.config/thirdshift/verify-env/<owner>/<repo>.env` (derived from `origin`, kept outside git; leave Launch-directory `.env` files untouched).
- **Drive:** prefer existing harnesses first (Playwright/Cypress, PTY/expect, curl), then shell/CLI browser tools (`@playwright/cli`, `agent-browser`, or disposable Playwright scripts — zero MCP config required).
- **Observe:** capture ARIA snapshots, rendered DOM state, console/`pageerror`/failed-network/`5xx` events, `.png` screenshots, H.264 `.mp4` walkthroughs, exit codes, and persisted side effects.
- **Isolate:** verify concurrent runs can use independent `mktemp -d` data/profile directories and ephemeral ports; when an app cannot isolate, have the generated skill refuse concurrent driving explicitly.

Confirm the checkout builds and boots cleanly before generating. Mark any temporary missing-asset scaffolding explicitly so `Cleanup` removes it.

## 2. Generate the skill

Write `.agents/skills/verify-<app>/SKILL.md` (linking `.claude/skills/verify-<app>` to `../../.agents/skills/verify-<app>` when the repo mirrors skills there; keep project skills separate from Factory `skills/`). Add YAML frontmatter (`name: verify-<app>` and a model-invoked `description` naming the app, surface, and source/route paths that trigger it) and these six grounded sections with zero placeholders:

- **Launch:** exact build, seed, and start commands inside one `( ... )` subshell whose `trap ... EXIT` handler is registered *before* starting any server or browser daemon. Use `mktemp -d` for isolated app/DB/profile state, bind loopback on port `0`, read the actual port from readiness output, and poll until the app is genuinely usable from empty state (migrations and seeds finished, not just TCP open). Source `~/.config/thirdshift/verify-env/<owner>/<repo>.env` inside the subshell only when the documented setup needs credentials (`set -a; . "$verify_env"; set +a`, tracing off). For short-lived CLIs/TUIs, build once and start each drive in an isolated PTY or tmux session.
- **Doctor:** one read-only check verifying the tracked server PID is alive, the expected binary/build answers on its owned loopback port, and seeded state/auth is valid across supported launch modes. Run `Doctor` before the first drive and after any failure.
- **Drive:** repo-specific selectors, routes, Playwright package location, expected harmless noise, and any CSP/sandbox quirks. Defer the generic two-phase workflow (interactive exploration before clean walkthrough pass, viewport pairing, `showActions` vs init-script cursor fallback, and error listeners) to `verify-ui` / `thirdshift-verify-ui` instead of duplicating it here.
- **Evidence:** create proof paths with `mktemp` outside the cleaned state directory (so `Cleanup` leaves `.png` and H.264 `yuv420p` `+faststart` `<= 8 MB` `.mp4` captures intact on disk, kept out of git). Name what faux/redacted data proves the surface and defer capture-pairing, `ffmpeg` transcoding commands, and `gh --attach` PR publishing (ADR 0034) to `verify-ui` / `thirdshift-verify-ui` and `pr` / `thirdshift-pr`. Verify what any dry-run/test mode actually skips by observing files, network, and git refs.
- **Cleanup:** the single `trap ... EXIT` handler stops and waits for exact tracked server PIDs/process groups and browser contexts/daemons across success, assertion failure, and interruption, deletes temporary state and disposable scripts, preserves proof captures at their `mktemp` paths, and verifies zero server or browser child processes remain after exit.
- **Helpers:** make every shipped helper script executable and document its exact invocation in `SKILL.md`.

## 3. Seed the feature map

Create `.agents/skills/verify-<app>/features/README.md` plus one file per top user-facing feature (3–5 to start), following [`references/feature-map-example/`](references/feature-map-example/). Each feature file uses the four H2 headings `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. When seed data lacks a required precondition, fail the journey loudly and record the unmet precondition or setup trap in `Gotchas` rather than weakening the check.

## 4. Prove it end to end

Execute the generated skill's own `Launch`, `Doctor`, `Drive` (at least one mapped feature), `Evidence`, and `Cleanup` instructions once. Confirm after `Cleanup` that a non-empty `1440×900` `.png` screenshot and a playable H.264 `+faststart` `.mp4` walkthrough (`<= 8 MB`) remain intact at their `mktemp` paths and zero server or browser child processes outlive the command. Fix anything that fails (running `Cleanup` on every failed attempt) and record any stand-in setup steps that differ from the real target.

## 5. Point to maintenance

Direct operators to `/maintain-verification-skill` to keep the skill and feature map aligned as routes and setup evolve.
