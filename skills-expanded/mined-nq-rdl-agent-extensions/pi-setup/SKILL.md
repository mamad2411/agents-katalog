---
name: pi-setup
license: MIT
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: "Preflight pi worker orchestration: check pi, Worktrunk, gh, jq, provider readiness, exact model/thinking and private state storage; record user-approved defaults. Use before /pi:dispatch or to diagnose launch prerequisites, not to grant permissions or write credentials automatically."
compatibility: Verified pi 0.99.1 and wt 0.77.0; Fast catalog contract from Codex CLI 0.159.1 (2026-10-01). Bash 3.2+, jq >=1.6 and Git; gh auth and repo fields verified on gh 2.97.0. Provider credentials are user-managed.
user-invocable: true
argument-hint: "[provider/model:thinking]"
---

# Set up pi workers

Verify correctness-critical flags against installed `pi --help`, `pi auth --help`
and `wt switch --help` and the [canonical Pi CLI](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md)
and [Worktrunk docs](https://worktrunk.dev/) after upgrades, before giving guidance.

1. Ask for a model with explicit provider and thinking, e.g.
   `openai-codex/gpt-6.1-sol:high` is an example, **not a guaranteed catalog entry**.
   From the target repo, run [pi-preflight.sh](scripts/pi-preflight.sh):
   `bash "$SKILL_DIR/scripts/pi-preflight.sh" "$MODEL"`.
   Report **each** prerequisite even if one fails: pi/version, wt/version,
   interactive-shell integration, gh/login, jq, provider, chosen model/thinking,
   state directory and writable parent. A nonzero result needs remediation,
   not a worker launch. See [setup details](references/setup.rst) for install links.
2. Verify the **exact provider/id** in `pi --offline --list-models <pattern>`;
   fuzzy search or exit 0 alone is not verification. Confirm the thinking level
   is supported by that model (levels can be clamped). `pi auth check --model
   <provider/id> --no-refresh` checks readiness without emitting credentials or
   refreshing/writing OAuth tokens. If expired/missing, the user authenticates
   with `/login` inside pi in their own terminal and reruns preflight.
   Never print auth keys/tokens, use `--credentials`, or ask them to paste secrets.
   Offer a Fast default, **off unless explicitly approved**. For GPT on
   `openai-codex`, explain increased plan usage (gpt-6.1-sol catalog: **2x speed,
   increased usage**) and check its advertised `priority` tier when the Codex
   catalog is available. Unknown/unlisted support means warn and ask; offer normal
   mode. Fast requires the bundled dispatch `assets/service-tier.mjs` extension,
   loaded via `pi -e`, not a pi setting or `--fast` CLI flag. Verify the installed
   asset is present before saving a Fast default. Status shows only
   **priority (requested)**; the backend tier echo cannot confirm Fast. See setup
   details for provenance (orchestrator investigation, 2026-10-01, pi 0.99.1 /
   Codex CLI 0.159.1), not new live/paid checks by setup.
3. Inspect `type wt` in the **user's interactive shell** for integration; a child
   Bash script cannot prove it. Offer `wt config shell install` only for user
   approval. `--no-cd` worker creation itself does not need shell integration.
4. Choose state default
   `${XDG_STATE_HOME:-$HOME/.local/state}/pi-dispatch/<owner>--<repo>/` and a cap
   (default **2**). Use a private parent outside the repo. Confirm before creating
   it with `umask 077; mkdir -p "$STATE"`; inspect existing permissions and ask
   before any chmod. All launches for this repo must share this directory.
   Workers' test suites can be memory-heavy: two is a ceiling, not a target;
   lower it under memory pressure and account for other running repos.
5. Explain **before launch**: pi tool calls run with the process's OS permissions;
   a worktree is not isolation. Review global pi extensions. The dispatch helper
   uses `--no-approve`, not `--approve`; neither flag sandboxes tools. Live/paid
   checks require explicit authorisation, a call/budget cap, an isolated environment
   and a credential cleanup plan. Setup itself makes no inference calls.
6. Explain Claude Code auto-mode may deny `pi -p` with **Create Unsafe Agents**.
   Offer a reviewed, narrow Bash permission rule (see details), never apply it
   silently or promise it overrides the classifier. The user can explicitly run
   the confirmed dispatch helper via `!`; that retains status tracking and cap.
   Do not evade denial by renaming/wrapping the command for automatic retries.
7. Optionally offer `wt config approvals add` to review project hook approvals.
   **The user decides and runs it; never `--yes`.** Skipping worktree creation
   hooks does not approve them. Never write credentials or permission rules
   without the user's approval.
8. With explicit approval, save only non-secret defaults at
   `${XDG_CONFIG_HOME:-$HOME/.config}/pi-dispatch/config.json` using jq and umask 077:
   `model` (including thinking suffix), `concurrency`, `fast` (boolean, default
   false), optional `stateDirectory`.
   Merge existing unrelated JSON keys rather than overwrite them. Do not change
   pi settings or repo files. Without approval, report defaults without saving.
   Summarise readiness, exact versions/model, storage, cap and remaining blockers;
   then offer `/pi:dispatch`. No worker is launched by setup.
