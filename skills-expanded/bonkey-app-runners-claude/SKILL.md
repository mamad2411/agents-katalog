# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Self-hosted GitHub Actions runner infrastructure for the **Bonkey Apps** org
(`bonkey-cards-app`, `bonkey-puzzles-app`, `bonkey-math-app`, and related repos
like `bonkey-puzzles`). This repo owns the runner *infrastructure* only — no
application code lives here. It was migrated out of `bonkey-puzzles-app`'s
`infra/` directory so the runner infra isn't nested inside one app's repo.

Two independent runner mechanisms live side by side:

- **`docker-runner/`** — a containerised runner for any Docker host (Docker
  Desktop or Rancher Desktop; the image is Linux/amd64, so the host OS only has
  to run Docker). Registers at the **GitHub organisation** layer
  (`https://github.com/Bonkey-Apps`), so one running container serves CI for
  any repo in the org.
- **`gcp-runner/`** — Terraform for GCE-hosted runners. A live root config
  (registered to `bonkey-puzzles-app`), a reusable `modules/runner-mig/` child
  module, and per-repo `environments/` roots that instantiate the module with
  their own Terraform state.

These are not alternatives to pick between — they're deployed independently
and can run concurrently; the Docker runner is for local/burst capacity, GCE
is the cloud fleet.

## On-demand only (GCE)

**There is no standing, always-on GCE runner fleet.** `runner_mode` defaults
to `"ephemeral"` and `runner_target_size` defaults to `0` across the root
config, the `runner-mig` module, and both `environments/` roots (`graphics`,
`bonkey-puzzles`). A runner is provisioned only when CI actually needs one —
via `gcp-runner/scripts/runner-up.sh` or a deliberate, temporary resize — not
left running idle and billing between jobs. When changing any of these
defaults, keep the root config, the module, and every `environments/` root in
sync — they currently duplicate the same variables rather than all
consuming the module (see "Duplicated root vs. module" below).

The local Docker runner is unaffected by this policy — it runs on a
developer's own desktop (not billed GCE compute), so leaving it up persistently
is fine.

**Current deployment, 2026-08-27:** one container, `bonkey-runner-01`, on a
Windows 11 host under Docker Desktop (24 CPU, 16.4 GB to the VM), running
Ubuntu 24.04 inside. `runner-2` and `runner-3` exist in `docker-compose.yml`
but sit behind the `x2`/`x3` profiles and are **off by default**, so total
org self-hosted capacity is **one concurrent job** shared by all three
products. A second runner does not currently fit in the VM's memory — the
runner's own `mem_limit` is 8g and two would exceed it.

## Commands

### `docker-runner/`

```bash
cd docker-runner
cp .env.example .env
# edit .env → set GH_PAT (org runner-admin PAT: classic scope admin:org, or
# fine-grained Organization "Self-hosted runners" = Read and write)

docker compose pull && docker compose up -d   # pull the published GHCR image
# — or, to build locally instead of pulling —
docker compose up --build -d

docker compose logs -f                         # watch registration + jobs
docker compose --profile x2 up -d               # 2 runners, on disjoint cores
docker compose --profile x3 up -d               # 3 runners, on disjoint cores
docker compose down                             # deregisters cleanly on stop
```

### `gcp-runner/`

Via the `deploy-gcp-runner.yml` workflow (`workflow_dispatch`): choose
`runner_profile` (e.g. `android-emulator`), `region`, and `action`
(`plan`/`apply`/`destroy`/`resize`). `resize` scales the **live** MIG directly
via `gcloud` (the only way to change size on an existing MIG — Terraform
`apply` won't, since the module sets `ignore_changes = [target_size]` so
bursts aren't reverted).

Locally:
```bash
cd gcp-runner              # or gcp-runner/environments/<name> for a specific env
terraform init
terraform plan
terraform apply
```

On-demand ephemeral runners without touching the persistent-fleet Terraform:
```bash
cd gcp-runner/scripts
GH_PAT=ghp_xxx ./runner-up.sh --count 2 [--android]   # needs gcloud ADC
```

## Architecture

### Docker runner: `entrypoint.sh` lifecycle

`docker-runner/entrypoint.sh` is the container's PID 1. Key behaviors, each
motivated by a real failure mode hit in production use:

- **Mints its own registration token** from `GH_PAT` at every startup (never
  written to disk) rather than requiring a pre-minted `RUNNER_TOKEN`.
- **Wipes stale `.runner`/`.credentials` on every ephemeral cycle.** Docker's
  `restart: unless-stopped` restarts the *same* container (same writable
  layer) rather than recreating it, so a prior cycle's registration files
  persist on disk. For `RUNNER_EPHEMERAL=true` (the default), GitHub deletes
  that registration server-side once the one job it was for completes — so
  blindly reusing those files on the next restart authenticates with dead
  credentials and fails with `Registration ... was not found`. The entrypoint
  always deletes and re-registers fresh when ephemeral.
- **Forwards stop signals to `run.sh` and waits**, rather than deregistering
  immediately. `run.sh`/`Runner.Listener` has its own graceful-shutdown
  handling that lets an in-flight job finish reporting before it stops;
  deregistering out from under it would risk cutting off a job's result
  upload to GitHub mid-flight.
- The random-suffix generator for the default runner name uses `|| true` on
  its `tr | head -c6` pipe — under `set -o pipefail`, `head` closing the pipe
  early sends `tr` a SIGPIPE that would otherwise abort the whole script even
  though the random suffix came out fine.

### GCE runner: duplicated root vs. module

`gcp-runner/`'s **root-level** `.tf` files (`main.tf`, `variables.tf`, etc.)
are the **live** config for `bonkey-puzzles-app` (confirmed by
`deploy-gcp-runner.yml`'s default `working-directory: gcp-runner` +
`TF_CHDIR="."`). `modules/runner-mig/` is a reusable child module that
duplicates this same logic; it's currently consumed by
`environments/graphics/` (the GPU runner) and `environments/bonkey-puzzles/`
(a separate `bonkey-puzzles` repo target), **not** by the root config itself —
migrating the root onto the module is a known, deliberately-deferred follow-up
(it touches live Terraform state). Each `environments/<repo>/` root has its
**own** GCS backend state prefix, so none of these deployments share state
even though they share code via the module.

`runner-startup.sh.tftpl` (root) and `modules/runner-mig/runner-startup.sh.tftpl`
(module) are near-duplicates — check both when changing boot-time behavior
(baked toolchain, host readers/writer lock for KVM/emulator jobs, etc.), since
which one applies depends on which Terraform root you're editing.

### CI-runner baked toolchain — golden-image manifest

`gcp-runner/IMAGE-MANIFEST.md` is the auditable record of what's baked into
GCE runner VMs at boot (Node, pnpm, Playwright, GitHub CLI, Android
SDK/emulator system-image) so per-job `setup-*` steps become warm no-ops.
Version pins here must stay in lockstep with each consuming app repo's
`package.json`. For most entries a mismatch means the bake "misses" and the
per-job installer falls back to a (slower) on-demand install, not a hard
failure.

**Playwright is the exception, and it is a hard failure.** Playwright resolves
its browser by *revision* — `playwright install` writes
`$PLAYWRIGHT_BROWSERS_PATH/chromium-<rev>/` and leaves nothing
version-agnostic behind (the app repos' `playwright.config.ts` probes for
`/opt/pw-browsers/chromium`, does not find it, and falls through to the
revision lookup) — and the per-job `playwright install` is **banned** by the
app repos' own rules. So a mismatched pin has no fallback at all.

Because this is an **org-level** runner (one image serves Puzzles, Cards and
Math) and those repos drift apart during an upgrade, the runner bakes **one
Chromium per pin in use, not one overall**: `PLAYWRIGHT_VERSION` (plus one
further ARG + install line per additional pin) in `docker-runner/Dockerfile`,
and a
`PLAYWRIGHT_VERSIONS` array in **both** `runner-startup.sh.tftpl` copies. Add
an entry when a repo adopts a new pin; remove one only once no repo pins it.

### Runner toolchain changes are two-sided and ordered

Any toolchain the runner bakes and an app pins is a two-sided change with a
mandatory order: **publish and roll the runner image first, bump the app
second.** Reversed, the failure signature is *locally green / CI-red* — every
local gate passes, only Actions fails, and it fails for every open PR until the
image catches up.

Rolling the local Docker runner: `docker compose pull`, then `docker compose up
-d`. **A pulled image is not a replaced runner — verify before believing it.**
Mid-roll the container has been seen still on the old image id while `docker
images` already showed the new `:latest` (whether `up -d` had finished and
failed to recreate, or was still in flight behind a multi-GB pull, was not
established — so trust the check, not a theory). Compare `docker inspect -f
'{{.Image}}' docker-runner-runner-1` against `docker images`, and confirm the
change is actually inside the container (`docker exec … ls /opt/pw-browsers`).
`up -d --force-recreate` resolves a mismatch.

Which runner a job lands on is decided per job by its `runs-on:`, which reads a
`CI_RUNNER*` Actions variable **with a fallback baked into the workflow**. The
fallback is usually what decides, because most of these variables are unset.

Verified 2026-08-27:

| repo | variables set | reaches the self-hosted runner via |
| --- | --- | --- |
| `bonkey-cards-app` | **none** | the *fallback* in `vars.CI_RUNNER_LINUX \|\| '["self-hosted","linux","x64"]'` |
| `bonkey-math-app` | `CI_RUNNER=["self-hosted"]` | the variable |
| `bonkey-puzzles-app` | `CI_RUNNER`, `CI_RUNNER_HEAVY` self-hosted; `CI_RUNNER_LIGHT` ubuntu-latest | the variables, tiered |
| `bonkey-app-runners` | `CI_RUNNER=["ubuntu-latest"]` | never |

**Listing variables under-reports — the absent variable is the dangerous one.**
`gh variable list` shows `bonkey-cards-app` completely clean, and it is not: its
release builds have always run on the self-hosted fleet, via an unset variable's
fallback, with nothing recording that anywhere. Note the asymmetry inside a
single Cards workflow file — `CI_RUNNER` falls back to `ubuntu-latest` while
`CI_RUNNER_LINUX` falls back to `self-hosted`. **Enumerate the fallbacks at the
use sites, not the configured variables.**

### Host readers/writer lock (GCE, KVM/emulator jobs)

Each GCE VM can run multiple runner agents (`runners_per_vm`), but only one
Android emulator/KVM-heavy job should run at a time per VM. The startup
script installs a host-level readers/writer lock (`ACTIONS_RUNNER_HOOK_JOB_STARTED`/
`_COMPLETED` hooks): regular jobs take a shared lock (up to N concurrent),
an emulator job (`HOST_LOCK_MODE=exclusive`, or inferred from `GITHUB_JOB`
since job-level `env:` isn't forwarded to the hook) takes an exclusive lock
that drains regular jobs first, then blocks new ones until it finishes.
