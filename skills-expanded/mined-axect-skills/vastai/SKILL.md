---
name: vastai
description: Manage Vast.ai GPU cloud instances via the vastai CLI. Use this skill whenever the user mentions Vast.ai, GPU rentals, cloud GPU instances, searching for GPU offers, creating/destroying instances, vast.ai billing, or any task involving the vastai command-line tool. Also trigger when the user wants to rent GPUs, find cheap GPUs, deploy Docker containers on remote GPUs, manage remote training infrastructure, or transfer data to/from cloud GPU machines. Even if the user just says "spin up a GPU" or "find me an A100", this skill likely applies.
---

# Vast.ai CLI Skill

This skill helps you use the `vastai` CLI to manage GPU cloud resources on the Vast.ai marketplace. Vast.ai is an open marketplace for GPU compute — you can search for available machines, rent them, deploy Docker containers, transfer data, and manage billing, all from the command line.

## Prerequisites

- **Install**: `pip install vastai` (or `uv pip install vastai`)
- **Authenticate**: Get your API key from https://cloud.vast.ai/cli/ then run:
  ```bash
  vastai set api-key YOUR_API_KEY
  ```
  The key is stored at `~/.vast_api_key`. Never share API keys.

## Core Workflow

The typical workflow is: **Search** -> **Create** -> **Use** -> **Verify artifacts** -> **Destroy within explicitly authorized retirement scope**.

### 1. Search for GPU Offers

```bash
vastai search offers '<query>' -o '<sort_field>'
```

The query uses a simple `field operator value` syntax. Multiple conditions are space-separated (implicit AND).

**Operators**: `>`, `>=`, `<`, `<=`, `=`, `!=`

**Common examples:**

```bash
# Find RTX 4090 machines with 99%+ reliability
vastai search offers 'gpu_name=RTX_4090 reliability>0.99 num_gpus=1'

# Find multi-GPU A100 setups, sorted by price
vastai search offers 'gpu_name=A100_SXM4 num_gpus>=4 reliability>0.98' -o 'dph'

# Find any GPU with 24GB+ VRAM under $0.50/hr
vastai search offers 'gpu_ram>=24 dph<0.5 reliability>0.95' -o 'dph'

# Datacenter-only machines with fast internet
vastai search offers 'datacenter=true inet_down>500 inet_up>500'

# Exclude China-region hosts (GFW blocks uv/pip/github during setup)
vastai search offers 'gpu_name=RTX_4090 reliability>0.99 geolocation notin [CN]' -o 'dph'
```

**Exclude China-region hosts to avoid setup failures.** Hosts physically in mainland China (`geolocation=CN`) sit behind the Great Firewall, so the setup phase intermittently fails: the `uv` installer (`astral.sh`), PyPI, and GitHub clones time out or hang, leaving a billing-but-unusable instance. Add `geolocation notin [CN]` to every search query before renting. The `geolocation` filter takes a two-letter country code and accepts `in` / `notin` with a bracketed list, so extend it if you hit other blocked regions (e.g. `geolocation notin [CN,HK]`). This is the single most reliable guard against the "uv install just won't run" problem.

**Key search fields** (see `references/search-fields.md` for full list):

| Field | Description |
|---|---|
| `gpu_name` | GPU model (use underscores: `RTX_4090`, `A100_SXM4`) |
| `num_gpus` | Number of GPUs |
| `gpu_ram` | Per-GPU VRAM in GB |
| `gpu_total_ram` | Total VRAM across all GPUs |
| `cpu_cores` | vCPU count |
| `cpu_ram` | System RAM in GB |
| `disk_space` | Available storage in GB |
| `dph` | Cost per hour ($/hr) |
| `reliability` | Machine reliability score (0-1) |
| `cuda_vers` | Max supported CUDA version |
| `compute_cap` | CUDA compute capability (e.g., 800 = 8.0) |
| `inet_down` / `inet_up` | Network speed in Mb/s |
| `datacenter` | Datacenter-only flag (true/false) |
| `geolocation` | Two-letter country code of the host. Operators: `=`, `!=`, `in`, `notin` (e.g. `geolocation notin [CN]`) |
| `dlperf` | Deep learning performance score |
| `gpu_max_power` | Host's GPU power limit in W (a capped value, e.g. 180 on a 3090, means a throttled, slower card) |
| `cuda_max_good` | Max CUDA version the host DRIVER supports (gates the torch wheel you can run, see python-setup.md) |
| `total_flops` | Combined GPU TFLOPs |
| `rentable` | Currently available |
| `static_ip` | Has stable IP |
| `verified` | Verification status |

**Sorting**: Use `-o 'field'` for ascending, `-o 'field-'` for descending.

**Pricing type**: Add `-d` (on-demand), `-b` (bid/spot), or `-r` (reserved).

**Before renting for multi-day work, always check the `Max_Days` column** in the formatted search output (far right of the price row). This is the host's committed contract length — when it elapses, vast.ai terminates your container regardless of training state. See `references/search-fields.md` for details on reading/parsing `Max_Days` and the 1.5× duration rule.

**Filter by `inet_up` when you sync checkpoints OUT** (pulls depend on the instance's UPLOAD, not `inet_down`). Add `inet_up>400` for sync-heavy jobs. If upload is slow AND the file is rewritten during training (e.g. per-epoch `latest_model.pt`), a direct rsync reads a moving target and corrupts the local copy: `cp` to a frozen snapshot on the instance first, then rsync the snapshot with `--partial-dir` + retries.

**Pick the GPU for the WORKLOAD, not by raw FLOPS.** A small model in a launch-heavy / sequential regime is latency-bound (kernel-launch + CPU), so a faster GPU buys little at 2-3× the cost. Benchmark min/epoch on a candidate before committing multi-day; `dlperf` over-weights big-model tensor-core throughput you may not use.

**The same GPU model can differ ~1.6× in speed across hosts — check `gpu_max_power` and the CPU, not just `gpu_name`.** A power-capped card (e.g. a 3090 limited to 180W vs the full 350W) runs at roughly 1/3 the SM clock (measured 510 vs 1620 MHz) and is silently much slower; an old Xeon + high host `load` also drags a CPU-bound phase (AR sampling, dataloading). Prefer full-rating `gpu_max_power` and a modern CPU (EPYC/Ryzen over old Xeon). After renting, verify: `nvidia-smi --query-gpu=power.limit,clocks.sm --format=csv,noheader` (limit = full rating, clock boosts to ~1500-1900 MHz under load). A same-model swap to a full-power host is worth it for multi-day runs and adds no scientific confound (results depend on config+seed+epochs, not hardware).

### 2. Create an Instance

```bash
vastai create instance OFFER_ID --image IMAGE --disk DISK_GB [OPTIONS]
```

**Key options:**
- `--image IMAGE`: Docker image. **Prefer a plain Ubuntu image (`ubuntu:22.04`) + `uv`** over a `pytorch/pytorch:*` image — see "Image choice" below.
- `--disk DISK_GB`: Local disk size in GB
- `--ssh`: Enable SSH access
- `--jupyter`: Enable Jupyter access
- `--direct`: Direct connection (vs proxied)
- `--onstart SCRIPT`: Startup script filename
- `--label LABEL`: Human-readable label
- `--env ENV`: Environment variables and port mappings
- `--price PRICE`: Bid price for spot instances ($/hr)

**Example:**
```bash
# Rent offer 2459368 with a plain Ubuntu image, 60GB disk, direct SSH
vastai create instance 2459368 --image ubuntu:22.04 --disk 60 --ssh --direct --label my-run
```

**Image choice — prefer plain Ubuntu + uv, NOT a pytorch image.** A `pytorch/pytorch:*` image pins a torch+CUDA you override anyway and tempts a `--index-url cuXY` pin that breaks on other GPU archs; `ubuntu:22.04` + `uv pip install -U torch` auto-resolves the right wheel. A bare Ubuntu image has none of `/workspace`, `rsync`, `curl`, `git`, `tmux`, so setup MUST start with `apt-get install -y rsync curl git build-essential tmux` + `mkdir -p /workspace/<project>` before any rsync. See `references/python-setup.md`.

Billing starts immediately for storage; GPU billing once the instance is "running".

**Provisioning is NOT atomic — verify after creating.** `vastai create` bills immediately, but the rsync/install/launch phase is separate and may never run if your orchestration dies mid-way, leaving a bare, idle, still-billing instance. After creating, check `vastai show instances` for both the instance COUNT (catch duplicates) and per-instance state (torch present? `nvidia-smi` util > 0? training alive?). If setup died, FINISH it manually rather than re-running the provisioner (which may rent yet another).

**Avoid autonomous auto-re-provision loops (money-runaway risk).** A daemon that auto-rents a replacement on death can runaway from one bug (e.g. not persisting the new instance id, so every tick re-rents): a 4-instance runaway happened in practice. Default to on-demand or manual resume. If you must automate: persist+verify state each tick, hard-cap the provision count, and fail-safe (an empty/errored `vastai show` is NOT "instance gone").

### 3. Manage Instances

```bash
# List your instances
vastai show instances

# View specific instance details
vastai show instance ID

# Get SSH connection string
vastai ssh-url ID

# View logs
vastai logs ID --tail 100

# Stop — DANGER: releases the GPU; `start` may never succeed. See "Retire Within Authorized Scope".
# Do NOT use stop to "park" an instance you still need — keep it running; destroy only after authorization and verification.
vastai stop instance ID

# Start a stopped instance — only works if that exact GPU is still free (often it is NOT)
vastai start instance ID

# Reboot without losing GPU priority
vastai reboot instance ID

# Label for easy identification
vastai label instance ID "my-training-run"
```

**SSH has two independent routes: direct and proxy. If one wedges, try the other before rebooting.** The direct port can fail every attempt with `kex_exchange_identification: Connection closed by remote host` while the GPU keeps training and the proxy still connects, so a dead direct SSH does NOT mean sshd is down. `ssh-url` gives only the direct url; get the proxy from raw: `vastai show instance ID --raw` -> `ssh_host` (`ssh<idx>.vast.ai`), `ssh_port`. Point sync scripts at the proxy (non-destructive, training never stops); confirm the GPU is alive meanwhile via the `gpu_util` field of `vastai show instances`.

### 4. Transfer Data

```bash
# Copy local file to instance
vastai copy local_file instance_id:/path/on/instance

# Copy from instance to local
vastai copy instance_id:/path/on/instance local_destination

# Cloud storage transfers
vastai cloud copy --src cloud_service:path --dst instance_id:/path --transfer "Cloud To Instance"
```

**Warning**: Never copy to `/root` or `/` as destination — this corrupts SSH permissions.

**IRON RULE — verify every retrieved artifact before trusting it. `scp`/`vastai copy` can exit 0 on a TRUNCATED or corrupted file.** A successful exit code does NOT mean the bytes arrived intact. This has caused real loss: a 29 MB model checkpoint pulled back at exit 0 was 182 KB short, was not a valid zip, and `torch.load` failed with "failed finding central directory" — after the source instance had already been destroyed, so the result was unrecoverable and the whole run had to be repeated. After EVERY pull of an important artifact (model checkpoint, results archive, dataset):
1. **Compare byte size** remote vs local: `ssh ... "stat -c%s REMOTE"` vs `stat -c%s LOCAL` — they must be exactly equal.
2. **Compare a checksum** remote vs local: `ssh ... "sha256sum REMOTE"` vs `sha256sum LOCAL` — they must match. (Size match alone is necessary but not sufficient.)
3. **Load/parse test** each required recovered artifact before retirement: `python -c "import torch; torch.load(PATH, map_location='cpu', weights_only=True)"`, `tar tzf archive.tgz >/dev/null`, `python -c "import zipfile; assert zipfile.is_zipfile(PATH)"`, etc. Use the artifact's real loader/parser; archive listing alone is not a complete load test.
4. For large or flaky transfers, prefer **`rsync -P --append-verify` over a manual ssh tunnel with retries** instead of plain `scp`/`vastai copy`; rsync re-checks and resumes, and `--append-verify` rechecksums the whole file. Re-pull on any mismatch.

### 5. Retire Within Authorized Scope

**Authorization and integrity are separate gates.** Require explicit user authorization for the specific instances to retire and the artifact set to preserve. Finished work, storage charges, and passing checks do not create permission to destroy.

**Before any destroy**, use `artifact-sync-completeness-gate`: establish the expected manifest; reconcile expected/source/staging counts per instance; compare byte size and sha256 for every required stable artifact; load/parse every recovered artifact; and confirm empty expected-minus-staging and expected-minus-durable-destination sets. Assert verified count equals expected count. Freeze or quiesce required mutable files before this gate; do not omit them merely because live hashing is unsafe. Confirm no unfinished work remains on the source.

If verification fails, keep the source available while performing bounded recovery. Report the exact missing set, recovery attempts, and ongoing cost. Obtain explicit approval before reducing the required set or accepting losses at retirement; never describe that outcome as fully verified.

```bash
# After explicit retirement authorization AND the complete integrity gate:
# Destroy single instance (irreversible!)
vastai destroy instance ID -y

# For multiple authorized instances, repeat once per instance after its gate passes:
vastai destroy instance ID2 -y
vastai destroy instance ID3 -y
```

`vastai destroy instance` prompts `Are you sure...? [y/N]` on stdin and may abort without a TTY. Use `-y` (or `--yes`) in a non-interactive call **only after authorization and the applicable retirement gate are satisfied**. It suppresses the CLI prompt; it is never a permission bypass.

**IRON RULE — NEVER `vastai stop` an instance you still need. `stop` is not a safe pause.** A stopped instance releases the GPU back to the pool; `start` only succeeds if that GPU is still free, which for popular cards may fail indefinitely ("Required resources are currently unavailable, state change queued"). Storage charges continue. Keep needed instances running during work or recovery; destroy only within explicitly authorized retirement scope and after the applicable integrity or approved loss-acceptance gate. Do not use `stop` to bypass either gate.

Retire completed instances promptly to stop storage charges only when retirement is explicitly authorized and the integrity gate passes. Otherwise report the blocker and cost; do not expand permissions.

## Setting up Python on a Fresh Instance

For any GPU work on a rented instance, use `uv` to set up Python — it auto-resolves the CUDA-correct PyTorch wheel for the GPU architecture. **Always read `references/python-setup.md` before writing a setup script**, especially when:
- Using Blackwell GPUs (RTX 5070/5080/5090) — needs PyTorch 2.7+ with CUDA 12.8+
- Installing PyTorch — never pin `--index-url` unless you know the target sm_ version
- The host driver is older than the latest torch's CUDA (e.g. driver CUDA 12.8): `uv pip install -U torch` silently installs cu130 and `torch.cuda.is_available()` returns False — ALWAYS verify it after install and pin DOWN to cu128 if needed
- Launching a detached long run (avoid the tmux-log-misplacement and `pkill -f` self-match traps)
- Switching Python versions in an existing venv

## Pre-flight Dependency Smoke Test

Before queuing N jobs (pueue / a job runner), smoke-test ONE end-to-end run per distinct script first. Late-bound imports (`from X import Y` inside a function body) pass `python -c "import script"` but die when that codepath fires mid-run, and a pueue `--after` chain cascade-fails every downstream task. Common stealth deps to install preemptively: `scipy`, `scikit-learn`, `pandas`, `tqdm`, `wandb`, `optuna`. Full checklist + setup pattern in `references/python-setup.md`.

## Additional Features

For detailed documentation on these topics, read the corresponding reference file:

- **Python/uv setup on remote instances**: `references/python-setup.md`
- **Instance management** (stop/start/reboot/recycle/update, labels, SSH, logs, execute): `references/instances.md`
- **Search fields & query syntax**: `references/search-fields.md`
- **Volumes** (persistent storage): `references/volumes.md`
- **Autoscaling & Endpoints** (serverless GPU): `references/autoscaling.md`
- **Hosting** (list your own machines): `references/hosting.md`
- **Billing & Account** (invoices, credits, teams): `references/billing.md`

## Quick Reference

```bash
# Check account balance
vastai show user

# Get help on any command
vastai COMMAND --help

# Output raw JSON (for scripting)
vastai show instances --raw

# Show the equivalent curl command
vastai search offers 'gpu_name=RTX_4090' --curl
```

## Common Patterns

**Find the cheapest GPU for a given task:**
```bash
vastai search offers 'gpu_ram>=24 reliability>0.98 inet_down>200 geolocation notin [CN]' -o 'dph'
```

**Deploy a training job:**
```bash
# 1. Find an offer — inspect Max_Days from formatted output
#    geolocation notin [CN] keeps the GFW from breaking uv/pip/github during setup
vastai search offers 'gpu_name=A100_SXM4 num_gpus=1 reliability>0.99 geolocation notin [CN]' -o 'dph'

# 1a. CRITICAL for jobs > 24h: verify Max_Days >= 1.5 × expected_hours / 24
#     The formatted table shows Max_Days in the price row (far right).
#     A host with Max_Days < your training duration will kill the container mid-run.
#     For exact values, parse raw:
vastai search offers '<query>' --raw | python3 -c "
import sys, json, time
for o in json.load(sys.stdin)[:10]:
    print(o['id'], f\"{(o['end_date']-time.time())/86400:.1f} days\", o['dph_total'])
"

# 2. Create instance with your training image
vastai create instance OFFER_ID --image your-registry/training:latest \
  --disk 100 --ssh --direct --onstart setup.sh

# 3. Monitor
vastai logs INSTANCE_ID --tail 50
# Also watch end_date mid-training — set an alert when hours_until_end < training_hours_left
vastai show instance INSTANCE_ID --raw | python3 -c "
import sys, json, time
d=json.load(sys.stdin); h=(d['end_date']-time.time())/3600
print(f\"hours until contract end: {h:.1f}\")"

# 4. Copy results back
vastai copy INSTANCE_ID:/workspace/results ./local_results

# 5. Verify the full required manifest before retirement:
#    expected/source/staging counts per instance; verified count == expected count;
#    remote/local byte size + sha256 for every stable required artifact;
#    load/parse every recovered artifact; empty expected-minus-staging and
#    expected-minus-durable-destination sets. Freeze required mutable files first.
#    Any gap blocks normal retirement; report it and seek explicit loss approval.

# 6. Destroy only if this instance's retirement is explicitly authorized,
#    its work is finished, and the gate above passes.
#    -y suppresses the CLI prompt only; it never supplies user permission.
vastai destroy instance INSTANCE_ID -y
```

**Contract expiration is a silent failure mode.** When `end_date` (host `Max_Days`) passes, the container goes `exited`, billing stops, and unsynced in-container state is lost. SSH refuses and `actual_status: exited` (but `status_msg` may still say "running", so compare `end_date` to wall time, don't trust that field). Mitigate: filter by `Max_Days` before renting, keep checkpoints rsyncing to local, and poll `end_date` vs now.

**Manage spot instances (cheaper but interruptible):**
```bash
# Search for bid-type offers
vastai search offers 'gpu_name=RTX_4090 reliability>0.95' -b -o 'dph'

# Create with a max bid price
vastai create instance OFFER_ID --image pytorch/pytorch:latest --disk 50 --ssh --price 0.30

# Change bid later
vastai change bid INSTANCE_ID --price 0.35
```
