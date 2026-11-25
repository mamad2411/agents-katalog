---
name: implementation-harness
metadata:
  version: 4.2.0
description: >
  Install the portable AI-dev harness, rebuild its operational graph standalone,
  harvest project skill improvements into its canonical templates, package direct
  canonical edits into a portable bundle, or apply canonical updates to an existing
  project.
  Use /implementation-harness launch, /implementation-harness reindex-graph, or
  /implementation-harness patch harvest|prepare|apply.
---

# Implementation harness

# SKILL METADATA

Owner: Anton Merkulov
Backup Owner: None
Team: Harness / Platform
Created: 2026-09-15
Last Reviewed: 2026-11-15
Purpose: Install the portable AI-dev harness, rebuild its operational graph standalone, harvest project skill improvements into its canonical templates, package direct canonical edits into a portable bundle, or apply canonical updates to an existing project.
Data Class: Internal
External Connections: None — operates on local project files; any MCP servers it configures for other skills (e.g. Jira/Confluence, AWS) are declared per-project in the generated `.mcp.json`, not used by this skill itself
Capabilities: Filesystem read/write scoped to the host project and this package's own directories (no access outside the repo); spawns one pinned local subprocess (`scripts/check-mermaid.mjs` renders via a configured, non-shell `spawnSync` call — no shell, no network-fetched code); may delegate single, disjoint-path stages to subagents per "Delegation safety" below. No credential handling, no network calls, and no push/deploy/commit of its own — those remain guarded commands presented to the developer to run.
Input: A route word (`launch` / `reindex-graph` / `patch harvest` / `patch prepare` / `patch apply`) plus project context gathered from the local repository
Output: Installed or updated skill/agent/doc files under the target project, plus launch/patch reports and manifests under `.harness/state/`

[Process guide and diagrams](README.md)

The user request accompanying invocation selects the operation. This folder is the authoring source in this repository. Consumers install the released
ZIP archive as a skill package; they do not copy this source directory. Installed
skills, agents, and guide docs are personalized copies.

## Execution host and package location

Resolve this entrypoint to its physical package directory once. In this source
repository that is `skills/implementation-harness/`; in a consumer project it is
the installed package (a provider skills folder or a host plugin cache). Record it as
`package:` (name, version, channel and this machine's path; see Patch State) and use it
for scripts. Shared state lives in the project's `.harness/state/`.
The execution host (the current agent), installation targets (Q6), and package
location are independent. Never infer Q6 from the host or discovery directory.

Read [Host capabilities](references/host-capabilities.md) before executing an operation.
Use the current host's procedures for execution; the target provider's procedures
are copied into installed artifacts by the manifest. Invoke this skill using the
host's native syntax (`/implementation-harness` in Claude or Copilot, `$implementation-harness` in Codex).

## Route

Parse command words, not substrings in file paths or bundle names:

- `launch` (or no arguments): follow [Launch](references/launch/01-launch.md), including provider selection and launch-state setup.
- `reindex-graph`: follow [Reindex graph](references/reindex-graph.md) — rebuild the
  operational graph standalone, without a full launch run.
- `patch harvest [scope]`: read [Patch Harvest](references/patch/04-patch-harvest.md).
- `patch prepare [scope]`: read [Patch Prepare](references/patch/07-patch-prepare.md).
- `patch apply [scope | bundle path]`: read [Patch Apply](references/patch/05-patch-apply.md).
- `patch` alone: read [Patch router](references/patch/03-patch.md) and ask for the direction.
- Compatibility: `update` means `patch apply`. Explain the replacement once; execute the same recipe.
- Conflicting or unknown operations: ask which operation was intended before writing.

## Shared contract

Read [Patch State](references/patch/06-patch-state.md) for harvest/prepare/apply and when
recording a launch baseline. All three patch operations create manifest records;
packaging and tracking are part of the operation, not additional modes.

Harvest generalizes selected permanent edits into canonical sources, bundling the
result. Prepare packages canonical sources already edited directly — no permanent
file involved — into a bundle, with no personalization and no deployment. Apply
personalizes canonical sources (current, or from a supplied bundle) into permanent
files; with no bundle argument and no prior unapplied `prepare` bundle for the
requested scope, it packages direct canonical edits itself before deploying them.
With a supplied bundle, apply reconciles its frozen canonical payload into this
package first.

Canonical authority does not authorize discarding unharvested local edits.
Use stored baselines to identify conflicts and resolve them before overwriting.
Preserve project substitutions and explicitly retained local customizations.

Launch follows **Q&A → JSON → mjs script → INTENT → verify** in the single launch guide.
The initial report, plan, and materialization receipt are checkpoints, not launch
completion. After setup, continue with the next pending stage; do not return while
required autonomous stages remain pending or in progress. A truthful in-progress
report does not itself justify stopping. Stop only at a concrete external blocker
or after final verification, and record the exact blocker or evidence.

Never hand the launch (or any span of its remaining stages) to a background/async
subagent and end the turn expecting to resume from its completion notification later —
the session ending is exactly what "do not return" forbids, and a killed or orphaned
background task leaves the run permanently stuck mid-stage. Execute every stage's work
directly in this session; a delegated worker (per "Delegation safety" below) is
acceptable only for a single stage's disjoint file writes, dispatched and awaited
synchronously before moving on, never as a fire-and-forget handoff of the whole run.

## Progress and continuity

**Initialize task tracking before context inspection or Q&A**, immediately after
provider selection and storage setup and report initialization. Create/resume one task per row of the
[Launch task table](references/launch/01-launch.md#launch-task-table); the table owns stage
names, dependencies, and completion evidence. Load the execution host's
`canonical/adaptors/<host>/task-tracking.md`: Claude uses its Task tools when
exposed; Codex uses `update_plan` when exposed; Copilot uses the durable report and
mirrors an exposed native TODO tracker when available. Otherwise track in the report. Enforce
ordering explicitly when the native tracker has no dependency support. Record the
selected mechanism once. Updating progress does not enter Plan mode.
Reports persist progress across sessions and accompany available native tracking.

For patch operations, create `.harness/state/launch/reports/<timestamp>-<mode>.md` from
the package report template. Load `.harness/state/launch/answers.json` and the latest local
report. Use the mode's
three progress rows, recording scope, the resolved provider scope, manifest ID,
decisions, and per-file outcomes. A project can have several providers installed at
once: name the providers the run deployed to or harvested from, never "both" by
assumption. See `references/patch/06-patch-state.md`'s "Provider scope of an operation".
Mirror these rows with the tracker selected above; preserve their order in a
progress checklist or report when native Tasks are unavailable. On resume, read the report, selected recipe, and manifest/state first.
Verify current hashes before continuing; never replay completed writes blindly.

Proceed within the user's requested scope. Ask only for missing values, ambiguous
scope/direction, or concrete conflicts and deletions not already authorized.
Show the proposed diff before writes; existing authorization covers clean changes.
Report actual outcomes and suggest a Conventional Commit. Follow the project's
guarded-command rules; do not push, deploy, or commit merely because patching ran.
On a script failure (`scripts/*.mjs`), surface the failed check and the project-
relative path it names — never a raw stack trace, a host/IP, or an absolute
filesystem path outside the project.

## Delegation safety

If any stage's work is delegated to subagents rather than performed directly, each
dispatched worker owns a disjoint set of target paths — never two workers materializing
into the same output directory or shared companion file. No delegated worker may itself
spawn further workers through any delegation tool; give it the concrete file list and
recipe instead of asking it to plan and fan out its own sub-delegation. This applies
whether the worker is a fresh agent or a fork (forks inherit the ability to call every
tool the parent has, including delegation, and must be explicitly told not to use it here).
Shared coordination files — the run report, `answers.json`, `registry.md`, plan/manifest
JSON — are written only by the orchestrator, never by a delegated worker, to avoid
concurrent-edit races. Before trusting a delegated worker's completion claim, verify
its actual file writes (`git status`/`git diff`, real hashes) rather than its self-report,
and check for unexpected additional running agents before continuing to the next stage.
Uncontrolled nested delegation has previously raced on shared state and destroyed
project config; these rules prevent that failure mode.
