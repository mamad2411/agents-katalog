---
name: colab-cli
description: "Control Google Colab runtimes from Codex or OpenClaw: assign or reuse CPU/GPU/TPU runtimes, start or reuse kernels, execute Python code or notebooks, inspect remote files, and sync artifacts. Use when the user wants Colab compute instead of local hardware for experiments, model training, notebook automation, or artifact transfer."
---

# Colab CLI

This skill automates the Jupyter server that `googlecolab/colab-vscode` connects to and can now also reproduce the extension's assignment flow: call Colab control-plane APIs, mint runtime-proxy tokens, and attach to the assigned runtime from a terminal.

## Preconditions

Before using the scripts:

- Use Colab API mode.
- Recommended setup: run `init-auth` once, let it save Colab OAuth credentials, then use the rest of the commands without retyping env vars.
- Keep secrets out of chat and committed files.

Connection notes and limitations live in `references/connection-model.md`.
Runtime, quota, and hardware selection guidance lives in `references/runtime-selection.md`. Load it when the task depends on choosing CPU vs GPU vs TPU, standard vs high-memory, compute-unit budget, or persistent vs ephemeral storage.
OAuth refresh-token lifecycle and reauthorization guidance lives in `references/oauth-refresh.md`. Load it when token refresh fails, when setting up a durable OAuth client, or when the error contains `invalid_grant`.
Runtime auth injection guidance for GitHub and Hugging Face lives in `references/runtime-auth.md`. Load it when the Colab kernel needs private GitHub access, Hugging Face gated downloads, or runtime-side repo creation and updates.
When reauthorization is actually needed, use `scripts/google_oauth_reauthorize.py` instead of handling the OAuth recovery flow ad hoc.

## Official Parity Goal

This skill targets behavior parity with `googlecolab/colab-vscode` for the parts that are reproducible outside VS Code:

- Google OAuth scope set and refresh behavior
- Colab assignment and runtime-proxy token flow
- Colab proxy headers for HTTP and websocket connections
- local persistence of assigned runtime metadata
- automatic runtime-proxy refresh before expiry
- Jupyter kernel execution, file transfer, and cleanup

The goal is to keep long-running runtime control and recovery semantics as close to the official extension as possible, even when the user drives Colab from a terminal instead of VS Code.

The following cases are not fully identical to the official extension because they depend on the VS Code host, UI, or an interactive browser-consent bridge:

- VS Code SecretStorage and server-provider integration are replaced by local auth/state files plus a local assigned-server registry.
- Colab ephemeral auth prompts such as Drive consent can now be surfaced and continued from this CLI, but they still require a browser consent round-trip and cannot be completed silently.
- Notebook UX is CLI-oriented, not integrated into the VS Code notebook controller lifecycle.

## Bootstrap

Run the bundled bootstrap once per machine or after deleting the local venv.
Commands below are written relative to the skill root:

```bash
scripts/bootstrap.sh
```

The bootstrap creates `.venv/` when `python3 -m venv` is available. If the host
lacks `ensurepip`, the skill still works with the bundled `vendor/websocket`
package, so `python3` remains a valid runtime entrypoint.

## Code Layout

The CLI entrypoint remains `scripts/colab_jupyter.py`, but the implementation is now split into an official-repo-inspired module layout under `scripts/colab_cli/`:

- `auth/`: Google OAuth and auth-env handling
- `auth/scopes.py`: explicit Colab/Drive scope policy, including required, drive-only, and allowed scope sets
- `common/`: shared models, network helpers, and state/registry utilities
- `config/`: default paths, constants, and environment-driven defaults
- `test/`: local smoke helpers for layout/import validation
- `colab/`: Colab control-plane client and runtime assignment helpers
- `drive/`: Google Drive API client. This skill uses Drive through the API, not through `drive.mount()`.
- `jupyter/`: Jupyter client, runtime refresh, websocket execution, and connection recovery
- `daemon/`: local `colab-sessiond` client, server, and SQLite-backed session registry
- `handlers/`: high-level command handlers split by auth, runtime, process, and artifact workflows
- `colab_api.py` and `jupyter_runtime.py`: compatibility shims for older imports
- `handlers.py`: command handlers and higher-level workflows
- `cli.py`: argument parser and top-level `main()`
- `core.py`: compatibility export layer for the modules above

This keeps the user-facing command stable while avoiding a single multi-thousand-line implementation file.

## Quick Start

One-time initialization:

```bash
python3 \
  scripts/colab_jupyter.py init-auth
```

This writes credentials to a default auth file:

```bash
~/.config/colab/auth.env
```

Then use the default state file and connect directly:

```bash
python3 \
  scripts/colab_jupyter.py connect-colab \
  --variant gpu
```

The default state file is:

```bash
~/.cache/colab/default-session.json
```

The default assigned-server registry is:

```bash
~/.cache/colab/assigned-servers.json
```

If you pass `--variant gpu` without `--accelerator`, the script auto-tries common GPU models and currently falls back from `T4` first. Exact availability is account- and quota-dependent.
If you do pass an explicit GPU model such as `--accelerator T4` and Colab rejects it with a precondition or availability error, the script now falls back to the normal GPU candidate chain instead of failing immediately.

Basic health check after connect:

```bash
python3 \
  scripts/colab_jupyter.py doctor
```

When you need to stage a whole code tree, prefer a single tarball upload over many small file uploads:

```bash
python3 \
  scripts/colab_jupyter.py upload-tree \
  repo/ \
  --remote-dir /content/work
```

Start a reusable kernel:

```bash
python3 \
  scripts/colab_jupyter.py start-kernel
```

Run a quick remote check:

```bash
python3 \
  scripts/colab_jupyter.py run-code \
  --code "import torch; print(torch.cuda.is_available())"
```

For long-running training or downloads, prefer detached background execution plus polling:

```bash
python3 \
  scripts/colab_jupyter.py start-process \
  --name train-smoke \
  --command "python3 /content/work/train.py"

python3 \
  scripts/colab_jupyter.py wait-process \
  --status-path /content/colab-jobs/train-smoke.status.json

python3 \
  scripts/colab_jupyter.py tail-file \
  --remote-path /content/colab-jobs/train-smoke.log \
  --lines 50
```

To wait for the process and collect its status, log, and artifact directories in one shot:

```bash
python3 \
  scripts/colab_jupyter.py collect-process-artifacts \
  --status-path /content/colab-jobs/train-smoke.status.json \
  --log-path /content/colab-jobs/train-smoke.log \
  --artifact-dir /content/checkpoints/run-001 \
  --artifact-dir /content/logs/run-001 \
  --out output/train-smoke
```

To also sync the collected output tree to Google Drive after it lands locally:

```bash
python3 \
  scripts/colab_jupyter.py collect-process-artifacts \
  --status-path /content/colab-jobs/train-smoke.status.json \
  --log-path /content/colab-jobs/train-smoke.log \
  --artifact-dir /content/checkpoints/run-001 \
  --out output/train-smoke \
  --drive-dir MyDrive/experiments/train-smoke \
  --drive-overwrite replace
```

Run a notebook end-to-end on Colab:

```bash
python3 \
  scripts/colab_jupyter.py run-notebook \
  notebooks/train.ipynb \
  --out output/train.executed.ipynb \
  --remote-path codex/train.ipynb
```

Pull a trained model back:

```bash
python3 \
  scripts/colab_jupyter.py download-file \
  --remote-path /content/checkpoints/model.safetensors \
  --out output/model.safetensors
```

Pull a whole checkpoint or log directory back in one shot:

```bash
python3 \
  scripts/colab_jupyter.py download-tree \
  --remote-dir /content/checkpoints/run-001 \
  --out output/run-001
```

Stop and release everything when done:

```bash
python3 \
  scripts/colab_jupyter.py cleanup
```

## Workflow

Use this sequence:

1. Bootstrap the local venv if missing.
2. Run `init-auth` once and let it save credentials to the default auth file.
3. Run `doctor` to confirm token refresh and state-file health.
4. Use `connect-colab` first.
5. Verify connectivity with `ping` or `list-dir`.
6. For iterative coding, create a kernel with `start-kernel`; the default state file is used automatically.
7. If you want separate sessions, override `--state-file`.
8. For notebook execution, use `run-notebook` so outputs are written back into an executed `.ipynb`.
9. For long training jobs, prefer `start-process` + `wait-process` + `tail-file` over a single long-lived `run-code`.
10. Write checkpoints and logs to deterministic remote paths under `/content` or Drive, then fetch them with `download-file`.
11. Send `keepalive` if you want to hold the runtime open between steps.
12. Use `cleanup` as the default way to stop kernels and release the runtime when done.

Before step 4, read `references/runtime-selection.md` when runtime cost, memory, or accelerator choice matters.

## Runtime Cleanup

- Colab can reclaim runtimes automatically after idleness or when the VM lifetime ends.
- Do not rely on automatic reclaim for normal operation. When the current phase is done, explicitly stop the kernel and run `unassign-server`.
- Apply that rule to default/CPU, GPU, and TPU runtimes. GPU and TPU are just the highest-priority cases because they are more expensive and more quota-sensitive.
- Assume an assigned runtime can continue consuming availability or paid quota while you keep it attached, even if you are not actively using it.

## Commands

Primary script:

```bash
python3 \
  scripts/colab_jupyter.py --help
```

Supported subcommands:

## Sessiond

`colab-sessiond` is the long-lived local session manager for this skill. It keeps Colab session metadata in a local SQLite database and lets short-lived CLI invocations reuse the same remote runtime without each command owning the whole connection lifecycle.

- Start it explicitly with:
  `python3 scripts/colab_jupyter.py sessiond-start`
- Inspect it with:
  `python3 scripts/colab_jupyter.py sessiond-status`
- Stop it with:
  `python3 scripts/colab_jupyter.py sessiond-stop`
- By default, stateful commands such as `connect-colab`, `start-kernel`, `run-code`, `start-process`, and `cleanup` will prefer the local daemon unless you pass `--no-daemon`.

- `sessiond-start`: start the local `colab-sessiond` background service and wait for health.
- `sessiond-status`: inspect daemon health, PID, and the active session registry.
- `sessiond-stop`: ask the daemon to shut down cleanly.
- `drive-list`: list a Google Drive folder through the Drive API without mounting Drive into the runtime.
- `drive-mkdir`: create a Drive folder path through the Drive API.
- `drive-upload`: upload a local file to Drive through the Drive API.
- `drive-download`: download a Drive file through the Drive API.
- `drive-upload-tree`: recursively sync a local directory to Drive through the Drive API.
- `drive-download-tree`: recursively sync a Drive directory to local storage through the Drive API.
- `init-auth`: run the Google OAuth flow once and save Colab credentials into the default auth file.
- `doctor`: inspect saved credentials, token refresh, websocket availability, and current state-file health.
  It now also reports explicit `scope_validation` and `drive_scope_validation`.
- `ping`: verify server connectivity and auth.
- `list-dir`: inspect `/content`, Drive mounts, or checkpoint folders.
- `upload-file`: push datasets, configs, or notebooks to the remote runtime.
- `upload-tree`: archive a local directory, upload it once, and extract it on the remote runtime.
- `download-file`: pull back logs, checkpoints, or executed notebooks.
- `download-tree`: archive a remote directory, download it once, and extract it locally.
- `inject-runtime-auth`: inject only the requested Hugging Face and/or GitHub secrets directly into the active Colab kernel, together with helper functions.
- `prepare-runtime`: inspect the current Colab Python/runtime baseline, inject requested GitHub/Hugging Face auth, and only install missing or too-old dependencies.
- `start-kernel`: create a reusable kernel and optionally persist it to `--state-file`.
- `run-code`: execute a Python snippet or `.py` file against a kernel.
- `start-process`: write a remote runner and start a detached background process on the Colab runtime.
- `process-status`: read the JSON status file for a detached background process.
- `wait-process`: poll a detached remote process until it exits.
- `collect-process-artifacts`: wait for a detached process, save its status JSON, fetch its log, and download one or more artifact directories.
- `tail-file`: read the tail of a remote text file such as a training log.
- `run-notebook`: execute a local `.ipynb` against a remote Colab kernel and save an executed notebook locally.
- `stop-kernel`: shut down a kernel directly or through `--state-file`.
- `connect-colab`: assign or reuse a Colab runtime through the same control-plane APIs the VS Code extension uses.
- `refresh-connection`: mint a fresh Colab runtime-proxy token for an assigned endpoint.
- `list-servers`: list existing Colab assignments for the authenticated account.
- `list-saved-servers`: inspect the locally persisted assigned-runtime registry that survives state-file loss.
- `keepalive`: reset the idle timer for the assigned Colab endpoint.
- `unassign-server`: release a Colab assignment and optionally clear the local state file.
- `cleanup`: stop the current kernel, unassign the current runtime, and clear the default state file.

## OAuth Scopes

This skill now enforces an explicit scope policy:

- `REQUIRED_SCOPES`: Colab plus profile/email identity scopes
- `DRIVE_SCOPES`: Google Drive API scopes
- `ALLOWED_SCOPES`: the union of the accepted Colab and Drive scopes

Default `init-auth` keeps the request minimal for Colab. If you want to use Drive API commands, run:

```bash
python3 scripts/colab_jupyter.py init-auth --include-drive-scope
```

or reauthorize with:

```bash
python3 scripts/google_oauth_reauthorize.py reauthorize --include-drive-scope
```

If the saved token does not include Drive scope, `drive-*` commands now fail early with a clear error instead of falling through to a later runtime failure.

## Drive

This skill now prefers the Google Drive API over Colab runtime mounts.

- Do not rely on `drive.mount()` for automation.
- Prefer `drive-list`, `drive-mkdir`, `drive-upload`, `drive-download`, `drive-upload-tree`, and `drive-download-tree`.
- Prefer Drive API sync over runtime mounts for datasets, logs, and checkpoint exports.
- Use `--overwrite replace|skip|fail` on Drive upload/download commands to make update behavior explicit.
- This keeps Drive operations independent from Colab websocket/runtime state and avoids runtime-side mount prompts when you only need file sync.

## Operating Rules

- Prefer `run-code` for small inspections, package installs, and one-off fixes.
- Prefer `start-process` plus `wait-process`/`tail-file` for long training jobs, large Hugging Face downloads, and any task that should keep running even if the local websocket reconnects.
- Prefer `collect-process-artifacts` after a detached training job when you need one command to gather status, logs, and checkpoint directories.
- When a run must also end up in Google Drive, prefer `collect-process-artifacts --drive-dir ...` so the collected local output tree is synced through the Drive API after download.
- Prefer `upload-tree` over repeated `upload-file` calls when staging a repository or experiment workspace.
- Prefer `download-tree` over many `download-file` calls when collecting a checkpoint directory, logs, or a run workspace.
- Prefer `inject-runtime-auth --need hf` when the runtime needs gated Hugging Face pulls or model publishing.
- Prefer `inject-runtime-auth --need github` when the runtime itself must clone private code, create repositories, or push commits.
- Prefer `prepare-runtime` before experiments that depend on GitHub or Hugging Face and a small set of Python packages; it treats Colab as a preloaded environment and avoids full environment recreation.
- Prefer minimum-version specs such as `transformers>=4.45` over old exact pins. By default, runtime preparation will not downgrade newer Colab packages unless you explicitly pass `--allow-downgrade-deps`.
- Prefer `--project-dir /path/to/repo` on `prepare-runtime` or `--prepare-runtime` commands when the repo already has `requirements.txt` or `pyproject.toml`; let the skill discover the minimum dependency set from the project before touching the runtime.
- Do not inject GitHub or Hugging Face secrets unless the current experiment actually needs them.
- Prefer `run-notebook` when the notebook itself is the source of truth.
- Prefer a stable `tmp/colab/session.json` state file when multiple commands must share Python state.
- Keep Google auth in env vars so `refresh-connection` can renew the runtime-proxy token when needed.
- Prefer the saved `~/.config/colab/auth.env` file as the durable auth source; this skill now reads that file before falling back to inherited process env vars.
- Treat `~/.cache/colab/assigned-servers.json` as the durable connection registry; it complements but does not replace the active state file.
- Treat `invalid_grant` during token refresh as a normal reauthorization case, not as a control-plane bug. Follow `references/oauth-refresh.md`.
- Expect the skill to refresh runtime-proxy tokens automatically before expiry and to retry one forced refresh when Jupyter HTTP calls receive `401/403`.
- Treat accelerator selection as a budgeting decision, not only a performance decision. Prefer the cheapest runtime that is likely to finish the job.
- Default to CPU for editing, data cleaning, light evaluation, and setup steps. Do not hold a GPU while doing mostly I/O, package installation, or notebook authoring.
- Default to `T4` for ordinary PyTorch training and LoRA-style experiments unless there is concrete evidence that memory or throughput is insufficient.
- Prefer plain `--variant gpu` for first connection attempts. Use an explicit `--accelerator` only when the workload truly needs a specific GPU model.
- Escalate from `T4` to `A100` or `H100` only when the model size, sequence length, batch size, wall-clock target, or prior OOM evidence justifies it.
- Prefer TPU only for workloads that are already JAX/XLA- or TPU-oriented. Do not move a PyTorch workflow to TPU just because TPU is available.
- When choosing hardware, treat accelerator names as requests, not guarantees. Google documents that the available GPU and TPU types vary over time.
- Do not treat any GPU example in this skill as a complete or permanent Colab menu. When the workload justifies it, it is acceptable to try additional accelerator labels and fall back cleanly if Colab rejects them.
- Use standard memory for light notebooks and data prep; use high-memory only when loading large datasets or models requires it.
- If the experiment is exploratory, start on a lower tier, measure memory use and iteration speed, then re-run on a premium GPU only if needed.
- Release premium runtimes promptly: stop kernels, avoid unnecessary `keepalive`, and `unassign-server` after checkpoints or artifacts have been downloaded.
- Prefer remote `/content/...` paths for scratch work and checkpoints that can be recreated; prefer Drive or server-side download for outputs that must survive runtime deletion.
- Make training jobs resumable: save checkpoints frequently and log to files, not only notebook cell output.
- If the runtime needs Drive, mount it explicitly in code before using Drive paths.
- If Colab sends an ephemeral auth request during `drive.mount`, this script now surfaces the consent URL and, in interactive mode, waits for the browser round-trip before replying to Colab. Silent browserless completion is still out of scope.
