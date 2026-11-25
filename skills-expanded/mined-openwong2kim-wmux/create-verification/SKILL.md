---
name: create-verification-skill
description: "Generate a project-local verification skill that drives the real app the way a user does (launch, doctor, drive, evidence, cleanup) plus a feature map. Use for /create-verification-skill, \"make a control skill for this repo\", \"make a driver skill\", or when a repo (or a new wmux surface) has no scripted way to prove UI/CLI/service behavior. In this repo the generated skill is verify-wmux."
---

<!--
Adapted from pstack `skills/create-verification-skill/SKILL.md`
(https://github.com/cursor/plugins, MIT, Copyright (c) 2026 Lauren Tan) and its
Claude Code port in pstack-claude `plugins/pstack/skills/create-verification-skill/SKILL.md`
(https://github.com/anishekkamal/pstack-claude, MIT, Copyright (c) 2026 Lauren Tan,
Copyright (c) 2026 Michael Denyer). See THIRD_PARTY_NOTICES.md.
-->

# Create a verification skill

Every serious project needs a scripted way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. This skill generates that as a project-local Claude Code skill at `.claude/skills/verify-<app>/`, with its driver at `scripts/control-<app>.mjs` and its feature map at `.claude/skills/verify-<app>/references/features/`. You write the output for the next agent, not for a human: it will be read cold, mid-task, by an agent that has never seen the app.

In this repository the output already exists: `.claude/skills/verify-wmux/` and `scripts/control-wmux.mjs`. Re-running this skill here means extending it (a new surface, a new launch mode), not starting over; for keeping it honest use `/maintain-verification-skill`.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest. (wmux: the Electron main window is primary; the `wmux` CLI, the MCP server and the phone web client are secondary.)
- **Run:** how does the app start locally? Prefer the repo's own documented commands (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first: Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port, the repo's own dogfood scripts. Only then pick a generic recipe: CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** what evidence can be captured? ARIA snapshots, screenshots, terminal transcripts, response bodies, logs, exit codes, files and DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles, sockets)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session. Name the instance the driver must refuse to touch (for wmux: the owner's real instance, i.e. an empty `WMUX_DATA_SUFFIX`, plus the shared `-dev` and `-portable` suffixes).

Verify each answer in code before adopting it (who owns the process, which signal does not arrive, which flag is not honored). If the checkout doesn't build or start as-is, fix that first (or report it precisely) before generating; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup, the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

## 2. Generate the skill

Write `.claude/skills/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, the surface, and when to reach for it, including "launch/run the app"; without frontmatter the skill never registers, and with `disable-model-invocation` the model cannot call it) and these sections, each grounded in what the interview actually found (no placeholders left):

- **Launch:** the exact command that starts the app for verification, and how to tell it's ready (a log line, a port answering, a rendered root). Include teardown. For a short-lived CLI or TUI there is no server to keep alive: launch means build the binary once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only check that answers "is this instance worth driving?": process up, right version/build, port owned by us, auth valid, automation channel enabled. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors/commands from this repo, not examples. Prefer stable handles (`data-testid`, ARIA roles and labels, prompt strings, route paths) over coordinates and tab order. Never screen coordinates.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name.
- **Cleanup:** how to tear down instances the run created. Never kill by process name (`pkill`, `killall`); kill what you started, by recorded PID. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names and git ignores.
- **Helpers:** any script the skill ships is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper. Keep helpers few and composable, with JSON output, and put their pure logic where a unit test can reach it.

## 3. Seed the feature map

Create `.claude/skills/verify-<app>/references/features/README.md` plus one file per user-facing feature area you can identify (start with the most-used areas; take them from routes, commands, menus, rail/nav items or docs). The README holds the index, the shared preconditions, the driving conventions, the proof and skip reporting rules, and a sweep order. Each feature file starts with an H1 and one paragraph describing the user-visible behavior, then exactly four H2s in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with control-<app>` (starting with `Preconditions:`, then action → exact command → observed result), and `Gotchas`. Use real handles grepped from the source; never invent one. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location: a cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable: if the live run cannot complete, say `Status: draft` at the top of the generated SKILL.md with the exact blocker.

## 5. Offer the maintenance loop

Point the user at `/maintain-verification-skill` for keeping the map honest as the app changes. Suggest a cadence only if they ask.
