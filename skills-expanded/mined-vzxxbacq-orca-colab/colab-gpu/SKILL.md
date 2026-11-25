---
name: colab-gpu
description: Set up and use a Google Colab GPU runtime as a remote compute backend through the Google Colab API over the public internet (no VPN or tailnet needed). Trigger when a task needs a GPU or CUDA, model training, fine-tuning, heavy inference that exceeds local laptop resources, or when the user mentions "Colab" or "run this on a GPU".
---

# Colab GPU Compute Backend (`colab-gpu`)

Use disposable Google Colab GPU runtimes directly from the local machine while keeping the workspace, coding agent, and credentials local. See [`references/cli.md`](references/cli.md) for the full command and exit-code table.

## 1. Resolve the CLI

Prefer `orca-colab` if installed on `PATH` (or `node bin/orca-colab.mjs` inside the repo); otherwise run:

```sh
npx -y https://codeload.github.com/vzxxbacq/orca-colab/tar.gz/2944ee151e7ef2d08a5598c00c6cce4e3109f13c <command> --json
```

Always pass `--json` and parse **stdout** only (progress and diagnostics go to `stderr` prefixed with `[colab]`).

## 2. Resource Discovery & User Guardrails

1. Run `doctor --json`:
   - Inspect `ok`, `mode` (`"direct-api"` or `"unconfigured"`), `checks.oauth`, and `policy` (`allowedGpus`, `maxConcurrentSessions`).
   - If `ok === false`, ask the user to sign in once via `orca-colab auth login` (or click **Sign in with Google** in the Orca Colab panel), ticking the Colab permission on Google's consent page (it starts unticked).
2. Run `status --json` (or `ls --json`) to discover any already-active GPU sessions (`name`, `gpu`, `rateKey`, `cuPerHour`, `reachable`, `ageSeconds`).
3. Run `credits --json` (or `credits calibrate --json`) to check the user's approximate Compute Units balance (`estimatedBalanceCu`) and monthly budget (`budgetCu`, `estimatedBudgetUsedPercent`).

## 3. Resource Management (Provisioning & Scaling Sessions)

1. Choose an accelerator within the user's `policy.allowedGpus` (from `doctor --json`). Prefer `T4` for inference/debugging or `L4` / `A100` for training if allowed by `policy.allowedGpus`.
2. Provision or attach to a runtime:
   - Reuse or start a session: `up --gpu T4 --json` (or `up --gpu auto --json` to pick the default allowed GPU).
   - Start an additional concurrent session (up to `policy.maxConcurrentSessions` on Colab Pro+): `up --gpu L4 --new --name worker2 --json`.
   - If `up` exits `1` with `code: "PROVISIONING_IN_PROGRESS"` (`step: "assign_lock"`), another Agent is currently creating a Colab runtime; wait `retryAfterSeconds` (~15s) and retry `up`.
   - If `up` exits `1` with `step: "policy"`, respect the user's hardware guardrail and select from the returned `allowedGpus` list.

## 4. Calling Compute Resources (Sync, Run, and Jobs)

1. **Sync workspace**: `sync [--session N] --json` pushes the current directory (honoring `.gitignore` and `.colabignore`, excluding `.git/`) to `/content/orca/<basename>` and records `remoteRoot`.
2. **Execute GPU tasks (`job submit` or `run`)**:
   - **Managed task (`job submit`)**: `job submit [--session N] --name "Train Model" [--sync] [--wait] --json -- python3 train.py ...` streams live clean output to `~/.orca-colab/tasks/<id>.log` (visible in the Orca Colab panel's **Agent Runs & Live Output** console).
   - **Quick command (`run`)**: `run [--session N] --json -- python3 -c "import torch; ..."` executes directly and returns `{ ok, session, exitCode, stdout, stderr }` (also recorded in the panel's Agent Runs history).
   - **Inspect / manage tasks**: `job ls --json`, `job logs <id> --json`, `job stop <id> --json`.
3. **Pull artifacts**: `pull [--session N] <remotePath> <localDir> --json` downloads a file or directory (checkpoints, weights, metrics) into `<localDir>/<basename>` over HTTPS; binary files arrive intact.
4. **Reach a service on the runtime**: there is no port forwarding. Query it from the runtime itself, e.g. `run --json -- curl -s localhost:8000/metrics`.

## 5. Hygiene

- Run `down [--session N | --all] --json` as soon as GPU work is finished so the runtime is unassigned (`DELETE /v1beta/runtimes/<id>`) and stops burning compute units.

## 6. Failure table

| Symptom / Exit code | Likely cause | Action |
|---|---|---|
| `up` exits `1` (`step: "prerequisites"`) | Not signed in to Google, or the Colab permission was not ticked | Ask the user to run `orca-colab auth login` (or use the panel) and tick the Colab permission. |
| `up` exits `1` (other `step`) | Policy limit or Colab refused the assignment (quota, GPU unavailable) | Read `error`; pick another allowed GPU or wait. |
| `run` / `sync` / `pull` says the session has no Colab runtime proxy | Session was started by an older orca-colab over Tailscale | Run `down --session <name>` then `up`. |
| `run` / `sync` / `pull` fails with a WebSocket or HTTP error | Colab runtime died or was recycled | Run `status --json`; offer `down` + `up` and re-`sync`. |
| `down` exits `4` (`reason: "api-delete-failed"`) | The Colab API refused to delete the runtime (sign-in expired, network) | Ask the user to `auth login` and retry `down`, or delete the runtime at colab.research.google.com (`Runtime → Disconnect and delete runtime`). |
