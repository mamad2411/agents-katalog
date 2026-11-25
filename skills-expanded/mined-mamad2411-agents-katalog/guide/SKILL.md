---
name: guide
description: >-
  Top-level user guide for THIS Claude Code config — the orchestration mainlines and when each applies, how to start on a project (including project-local claude-env-bootstrap), how to install, update and maintain the global config, and where the full skill index lives. Triggers: "guide / help / cheat sheet / how do I use this config / what are the orchestrators / how to start on a project / 指南 / 帮助 / 怎么用 / 五条主线 / 这套配置怎么用 / 老项目怎么用".
allowed-tools:
  - Read
---

<objective>
Output the reference block below VERBATIM. Do NOT add project-specific analysis, git status,
file context, or next-step suggestions — this is a static help screen.
</objective>

<reference>
# Claude Code Config — User Guide

This config is built around FIVE orchestration mainlines. Each is fronted by an orchestrator skill
that turns a plain-language task description into the right narrow skills. You rarely pick skills by
hand — describe the task, and the matching orchestrator routes and composes the work.

## 1. The five orchestration mainlines
| # | Mainline | Orchestrator | Fires | Use when |
|---|---|---|---|---|
| 1 | Project setup | `claude-env-bootstrap` | manual | give a project its own tailored `.claude/` (see §2) |
| 2 | Delivery / PM | `gsd-pipeline-orchestrator` | auto | any non-trivial build: new project / phase / feature / refactor |
| 3 | UI / UX | `uiux-product-orchestrator` | auto | design, visual direction, style lock, screenshot-to-code, UI audit |
| 4 | QA / testing | `enterprise-qa-testing` | auto | test strategy, E2E, CI quality gates, release readiness |
| 5 | AppSec (defensive) | `appsec-security-orchestrator` | auto | backend / API / auth / payment / pre-deploy security review |

Mainlines 2–5 fire automatically when your task matches; mainline 1 (`claude-env-bootstrap`) is
manual-only. Sub-layer: `discoverability-orchestrator` (L12 — SEO / AEO / Local SEO / ASO) is a
UI/UX downstream release gate, not a sixth orchestrator.

## 2. Starting on a project
First lay the foundation, then decide how much process you want.

### Step 1 (foundational) — give the project its environment: `claude-env-bootstrap` (manual)
This is the setup step that makes the config actually work INSIDE a project — do it once per real
repo. It composes a tailored, self-contained `.claude/` (only the orchestrators + skills + rules +
agents + subsystem hooks + tools THIS repo needs), writes a project `CLAUDE.md` + `manifest.json`,
and registers the subsystem (AppSec/QA/UIUX/L12) hooks so their enforcement actually fires. Result:
the repo is clone-and-run for the whole team.
- Run it: `/claude-env-bootstrap` (manual-only — never auto-fires). Re-sync after the global config
  changes: `/claude-env-bootstrap --update`.
- Fresh repo → composes from scratch. A repo that already has `.claude/` → it BLOCKS (back up or use
  `--update`); it never silently overwrites.
- Skip it and you only get the GLOBAL layer: the auto orchestrators (mainlines 2–5) still respond
  from `~/.claude`, but there is NO project-local enforcement, no tailored/self-contained env, and
  no project `CLAUDE.md`. Fine for a one-off edit; not enough for an ongoing project.

### Step 2 — choose how much PM structure (GSD)
- Level 0 — just get tasks done: describe the task; nothing else to set up. Quick fixes, small features, exploration.
- Level 1 — light structure for one task: `/gsd-fast` (trivial, inline) or `/gsd-quick` (atomic commits + state tracking).
- Level 2 — full GSD: `gsd-map-codebase` (analyze existing code into `.planning/codebase/`) and, if
  you have docs, `gsd-ingest-docs`; then `gsd-plan-phase` -> `gsd-execute-phase`.

The GSD guards stay dormant until the project has a `.planning/` dir, so Level 0 stays frictionless
even after bootstrap. Easiest entry: just say "I'm on an existing project and want to do X" — the PM
orchestrator routes you to setup vs. just doing the task.

## 3. Installing / maintaining the global config (this repo)
> Don't confuse the two "installs": `claude-env-bootstrap` (§2) sets up ONE repo's project-local
> `.claude/`; `claude-config.js` (below) installs / updates the GLOBAL `~/.claude` toolkit on your
> machine — the full skill + rule set the bootstrapper composes from.

Run `node claude-config.js <cmd>` from the cloned repo dir (default DRY-RUN; add `--apply` to write):
- `status` — installed-vs-repo drift + hook health (read-only)
- `install --apply` — first-time deploy; then interactively offers hook wiring (batches below)
- `update --apply [--pull]` — sync to latest + clean files removed upstream + re-pin
- `wire --apply [--hooks=A,B]` — (re)wire hooks into settings.json (idempotent; never hangs headless)

New machine: `git clone <repo-url> ~/.claude-config && node ~/.claude-config/claude-config.js install --apply`
(answer the wiring prompts; headless: append `--wire --hooks=A,B`). Update later via `/sync-config`
or `node …/claude-config.js update --apply --pull`. Needs node + git; cross-platform.
`settings.json` is per-machine — `wire` MERGES hook entries (never overwrites); your model /
statusline / gitnexus / credentials are preserved.

Hooks come in two batches, chosen at install/wire time:
- Batch A — GSD core governance: workflow/read/prompt guards, prompt-injection scan on Read, context monitor, commit validation, session bootstrap.
- Batch B — ECC quality: config-protection (block edits to existing lint/format configs), block-no-verify, per-file auto-format, design-quality nudge.

## 4. Full reference
- `SKILLS-INDEX.md` — complete skill taxonomy + routing tables + trigger disambiguation
- `CLAUDE.md` — constitutional hard rules + governance
- `docs/ORCHESTRATOR-MAP.md` — orchestrator routing map
- `/gsd-help` — full GSD command list
- Native `/` menu — lists every installed command/skill with its description
</reference>

<process>
Execute end-to-end. Display the reference content directly — no additions or modifications.
</process>
