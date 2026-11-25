---
name: vastkit
description: "Operate temporary Vast.ai GPU rentals through the bundled Vastkit CLI: search and rank offers by effective session cost, rent cost-capped instances, wait for SSH, transfer projects, run commands and detached jobs, retrieve outputs, inspect status and logs, and stop billing. Use when an agent needs temporary GPU compute on Vast.ai, when a user asks to select, rent, use, or clean up a GPU server, or when running ML, training, inference, rendering, or other CUDA workloads remotely."
---

# Vastkit

Use the Vastkit runtime bundled with this plugin as the execution layer. Apply
the workflow and guardrails below; do not install a separate Vastkit package or
recreate Vast.ai API requests in ad hoc scripts.

## Resolve the CLI

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. In Claude
Code, `${CLAUDE_SKILL_DIR}` is that directory. In other agents, use the skill
path shown by the host.

```bash
VK="<skill-dir>/scripts/vastkit-cli"
"$VK" --version
```

The launcher resolves the Python package from the installed plugin. If the
version check reports that the runtime is missing, stop and ask the user to
update or reinstall the plugin through their agent. Do not use `pip` as a
fallback.

Require Python 3.9+, internet access, `ssh`, and `tar`. Prefer `rsync` when
available; Vastkit falls back to tar transfers when the remote image lacks it.

## Protect Credentials

- Use `VAST_API_KEY` or `~/.vast_api_key`. Never put an API key in a command,
  pass `--api-key`, print it, commit it, or ask the user to paste it into chat.
- Let Vastkit auto-detect an SSH key, or use `VASTKIT_SSH_KEY`. Never print or
  transfer private keys.
- Do not upload `.env` files or credential directories. Vastkit excludes common
  environment files by default; add explicit exclusions for any project-specific
  secret paths.
- Pass remote secrets only by referencing an already-exported local variable,
  for example `--env HF_TOKEN="$HF_TOKEN"`. Never place a literal token in the
  command or response.

If authentication is not configured, stop and ask the user to configure it
locally using the Vast.ai API key page. Continue only after they confirm.

## Apply Spending Guardrails

Run read-only discovery commands without approval: `whoami`, `search`, `ls`,
`status`, `jobs`, and `logs`.

Before `rent` or `start`, obtain explicit user approval for the cost-bearing
action. A prior request counts only when it clearly authorizes renting or
resuming. State:

- GPU and minimum VRAM
- maximum hourly price
- disk allocation and image
- expected duration and download volume
- estimated session cost and any known excluded costs
- instance label
- whether to destroy automatically after verified output retrieval

Always include `--max-price` on agent-selected rentals. Treat
`est_session_cost` as an estimate, not a guaranteed bill. Use `--yes` only
after approval, and only for the approved limits.

Before `stop`, `destroy`, `push --delete`, or replacing remote data, confirm
that the exact instance or data is authorized unless the user's request already
said to perform that action. Never use `destroy --all` unless the user
explicitly requested every matching instance be destroyed.

Stopping releases the GPU but storage remains billed. Destroying is
irreversible and is the action that ends instance billing.

## Run the Workflow

### 1. Establish Requirements

Inspect the workload before choosing hardware. Determine the minimum VRAM, GPU
count, CUDA compatibility, disk space, image, approximate runtime, model or
dataset download size, local project path, remote command, outputs to retrieve,
and cleanup policy. Infer technical values from the project when reliable; ask
about missing financial limits or destructive cleanup intent.

### 2. Preflight the Account

```bash
"$VK" whoami --json
"$VK" ls --json
```

Check for an existing suitable instance before creating another. Do not reuse,
stop, or destroy an existing instance without user authorization. For all
automation, use explicit instance IDs even when Vastkit could infer the only
instance.

### 3. Search and Explain the Choice

Use realistic session assumptions so bandwidth-heavy hosts rank honestly:

```bash
"$VK" search \
  --gpu "L40S" --gpu "RTX 6000Ada" \
  --vram 45 --disk 80 --max-price 1.00 \
  --hours 2 --download-gb 40 --max-bw 10 \
  --reliability 0.95 --json
```

Read the structured results. Prefer the lowest effective session cost that
meets the workload, not merely the lowest hourly price. Present the chosen
offer's GPU, VRAM, location, reliability, hourly price, bandwidth price, and
estimated session cost before requesting approval.

Avoid `rent --offer` for agent-selected machines because it bypasses the search
filters. Use it only when the user selected a current offer and approved its
current price.

### 4. Rent Within the Approved Limits

Repeat the approved search constraints in `rent`, choose a distinctive safe
label, and request JSON output:

```bash
"$VK" rent \
  --gpu "L40S" --gpu "RTX 6000Ada" \
  --vram 45 --disk 80 --max-price 1.00 \
  --hours 2 --download-gb 40 --max-bw 10 \
  --reliability 0.95 --label agent-training \
  --attempts 3 --boot-timeout 600 --yes --json
```

Record the returned instance ID immediately and use it in every later command.
Tell the user when billing starts, including the ID and hourly rate.

### 5. Transfer and Execute

Push only required inputs. The default excludes cover `.git`, virtual
environments, caches, and `.env` files. Additional `--exclude` flags extend
those defaults.

```bash
"$VK" push "$ID" ./project /workspace/project \
  --exclude outputs --exclude checkpoints

"$VK" exec "$ID" --cwd /workspace/project -- \
  'python -m pip install -r requirements.txt && python prepare.py'

"$VK" exec "$ID" --detach --job training --cwd /workspace/project -- \
  python train.py --output /workspace/project/outputs
```

Use job names containing only letters, digits, dots, underscores, and hyphens.
Use a detached job for long work so it survives connection loss. Quote a
compound remote shell command as one argument after `--`.

Monitor without starting duplicate work:

```bash
"$VK" jobs "$ID" --json
"$VK" logs "$ID" --job training -f
```

`logs -f` returns the detached job's exit code. Treat a nonzero code as a
workload failure and inspect the log before retrying.

### 6. Retrieve and Verify Outputs

Pull results before any destructive cleanup:

```bash
"$VK" pull "$ID" /workspace/project/outputs/ ./outputs/
```

Verify locally that expected files exist, are non-empty, and are usable. Do not
destroy the instance merely because a transfer command returned zero when the
expected artifacts are missing.

### 7. End Billing

When cleanup was approved and output verification succeeded:

```bash
"$VK" destroy "$ID" --yes
"$VK" ls --json
```

Verify that the exact ID is gone. Report the approximate accrued cost shown by
Vastkit. If the user wants to keep the instance, report its ID, hourly rate,
status, and the exact destroy command prominently.

## Recover Safely

- If any command fails after a rental may have been created, run `ls --json`
  immediately and locate the distinctive label. Do this after interruptions
  during `rent` as well.
- Vastkit destroys boot attempts that time out, but verify account state after
  an interrupted process or a failed destroy request.
- If approved automatic cleanup applies, make a best-effort exact-ID destroy
  after a failed workload. Preserve outputs first when possible.
- If cleanup is not authorized or destruction fails, do not hide the state.
  Report the live instance ID, price, and dashboard/CLI cleanup action.
- Never finish a normal run while an active billed instance is unaccounted for.
