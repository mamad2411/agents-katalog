---
name: runpod-vllm-gpu-deploy
description: Deploys OpenAI-compatible vLLM servers on RunPod GPU pods using the runpod-vllm CLI. Use when asked to deploy vLLM on RunPod, spin up a GPU pod, serve an OpenAI-compatible LLM endpoint, plan a deployment offline, validate a deployment config, wait for pod readiness, smoke-test an inference endpoint, recover a partial deployment, or tear down a GPU pod. Do not use for unrelated RunPod tooling or as authorization to create, mutate, or destroy live resources.
---

# RunPod vLLM Deployer

## Overview

Use this repository's `runpod-vllm` CLI to plan, create, inspect, validate, and remove OpenAI-compatible vLLM GPU Pods. Keep configuration validation offline until the user explicitly authorizes a live operation, and preserve the local state needed for verified teardown.

## Use and non-use triggers

Use this skill when the current request involves:

- Installing or checking the `runpod-vllm-deployer` repository.
- Producing an offline, redacted deployment plan.
- Creating a RunPod vLLM Pod after clear user approval.
- Listing Pods or inspecting the Pod recorded in local state.
- Waiting for vLLM readiness or running the deterministic endpoint smoke test.
- Recovering after Pod creation when local state could not be saved.
- Destroying a specifically verified Pod and confirming provider-side absence.

Do not use this skill to operate a different RunPod client, manage Serverless endpoints, alter accounts, estimate costs, or claim that a model will fit a GPU. A request to explain, plan, inspect code, run tests, or validate configuration does not authorize any live resource mutation.

## Hard safety boundaries

1. Treat `deploy` as billable. Do not run it unless the user's current request clearly authorizes creation of the reviewed configuration. Prior approval from another request is not current approval.
2. Treat `destroy` as destructive. Do not run it unless the user's current request authorizes termination of the exact verified target.
3. Do not use `--yes` to infer consent. It only bypasses the CLI prompt after authorization already exists.
4. Do not contact RunPod during repository tests, offline planning, or documentation work. Never substitute `deploy` or `destroy` for a smoke test.
5. Keep the default API URL. Use `--api-url` only when the user explicitly selects a trusted RunPod-compatible endpoint. Choose the API version as described in "RunPod REST API version" below.
6. Stop if the selected state file, model, Pod name, Pod ID, API URL, or requested operation conflicts with the user's request.

## Installation and prerequisite checks

Run from the repository root. Require Python 3.11 or newer.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
command -v runpod-vllm
runpod-vllm --help
```

For repository development, use `make setup` to install development dependencies. Before any live command, check secret presence without printing values:

```bash
test -n "${RUNPOD_API_KEY:-}"
test -z "${HF_TOKEN:-}" || test -n "${HF_TOKEN:-}"
```

Require `RUNPOD_API_KEY` for `deploy`, `list`, `status`, and `destroy`. Use `HF_TOKEN` only when the model repository requires it. `wait` accesses the vLLM endpoint and does not use the RunPod API key. `smoke-test` optionally reads an endpoint bearer token from `VLLM_API_KEY` or the variable named by `--bearer-token-env`.

## Exact CLI reference

Place global options before the command:

| Global option | Help definition |
| --- | --- |
| `--state-path PATH` | Local teardown state; default `.runpod-vllm-state.json`. |
| `--env-file PATH` | Optional selected file containing `RUNPOD_API_KEY` and `HF_TOKEN`. |
| `--api-url TEXT` | RunPod REST base URL; default `https://rest.runpod.io/v1` for v1, `https://api.runpod.io/v2` for v2, or the URL recorded in state. |
| `--api-version [v1\|v2]` | RunPod REST API version; defaults to `v2` (since RunPod retired v1 on 2026-11-15) or the version recorded in state (legacy v1 state moves to v2 automatically); env var `RUNPOD_API_VERSION`. |
| `--version` | Show the version and exit. |
| `--help` | Show help and exit. |

Use these exact command forms and options:

| Command | Exact form | Command options from current help | Network and effect |
| --- | --- | --- | --- |
| `plan` | `runpod-vllm plan --model TEXT [OPTIONS]` | `--model`, `--name`, `--gpu`, `--gpu-type-id`, `--gpu-count`, `--tensor-parallel-size`, `--container-disk-gb`, `--volume-gb`, `--min-vcpu-per-gpu`, `--min-ram-per-gpu`, `--max-model-len`, `--gpu-memory-utilization`, `--dtype`, `--quantization`, `--kv-cache-dtype`, `--revision`, `--trust-remote-code`, `--reasoning-parser`, `--image`, `--cloud-type`, `--data-center`, `--port`, `--env`, `--help` | Offline; validates and prints a redacted payload. |
| `deploy` | `runpod-vllm deploy --model TEXT [OPTIONS]` | All `plan` options, plus `--yes` or `-y`; `--env` is never printed unredacted. | RunPod API; creates a billable GPU Pod and saves state. |
| `list` | `runpod-vllm list` | `--help` | RunPod API; lists active GPU Pods without mutation. |
| `status` | `runpod-vllm status` | `--help` | RunPod API; inspects the state-recorded Pod and shows URLs. |
| `wait` | `runpod-vllm wait [OPTIONS]` | `--base-url TEXT`, `--timeout FLOAT` default `900.0`, `--interval FLOAT` default `5.0`, `--help` | vLLM endpoint; waits for `/health` and non-empty `/v1/models`, then prints a redacted `OpenAI base URL` and `export OPENAI_BASE_URL=...` snippet. |
| `smoke-test` | `runpod-vllm smoke-test [OPTIONS]` | `--base-url TEXT`, `--model TEXT`, `--bearer-token-env TEXT` default `VLLM_API_KEY`, `--timeout FLOAT` default `30.0`, `--help` | vLLM endpoint; sends a deterministic four-token chat request, then prints a redacted `OpenAI base URL` and `export OPENAI_BASE_URL=...` snippet. |
| `destroy` | `runpod-vllm destroy [OPTIONS]` | `--pod-id TEXT`, `--yes` or `-y`, `--verify-timeout FLOAT` default `60.0`, `--verify-interval FLOAT` default `2.0`, `--help` | RunPod API; deletes, verifies absence, then removes matching state. |

`plan` and `deploy` share these validated defaults and constraints:

| Option | Default or allowed value |
| --- | --- |
| `--model TEXT` | Required Hugging Face model ID. |
| `--name TEXT` | `vllm-server`; sanitized to at most 63 characters. |
| `--gpu TEXT` | `A40`; allowed profiles are `RTX4090`, `RTX5090`, `A6000`, `A40`, `L40S`, `A100`, `H100`, `H200`, `B200`. |
| `--gpu-type-id TEXT` | Optional raw RunPod GPU type ID (2 to 120 printable ASCII characters, no leading or trailing whitespace); overrides `--gpu` when set. |
| `--gpu-count INTEGER` | `1`; range 1 through 8. |
| `--tensor-parallel-size INTEGER` | `1`; range 1 through 8, no greater than GPU count, and must divide GPU count. |
| `--container-disk-gb INTEGER` | `50`; validated range 10 through 4096. |
| `--volume-gb INTEGER` | `40`; validated range 0 through 4096. |
| `--min-vcpu-per-gpu INTEGER` | `4`; validated range 1 through 128. |
| `--min-ram-per-gpu INTEGER` | `16`; validated range 1 through 2048 GB. |
| `--max-model-len INTEGER` | `8192`; validated range 256 through 1048576. |
| `--gpu-memory-utilization FLOAT` | `0.9`; validated range 0.1 through 0.99. |
| `--dtype TEXT` | `auto`; allowed `auto`, `bfloat16`, `float16`, `float32`. |
| `--quantization TEXT` | Optional vLLM quantization method. |
| `--kv-cache-dtype TEXT` | `auto`; allowed `auto`, `fp8`, `fp8_e4m3`, `fp8_e5m2`. |
| `--revision TEXT` | Optional model revision or commit. |
| `--trust-remote-code` | Off; opt in only after reviewing the model repository. |
| `--reasoning-parser TEXT` | Optional vLLM reasoning parser. |
| `--image TEXT` | `vllm/vllm-openai:v0.19.1`; must have an explicit tag other than `latest`. |
| `--cloud-type TEXT` | `SECURE`; allowed `SECURE` or `COMMUNITY`. |
| `--data-center TEXT` | Optional and repeatable. |
| `--port INTEGER` | `8000`; validated range 1024 through 65535. |
| `--env KEY=VALUE` | Optional and repeatable. Never use it for secrets. |

Confirm the executable reference when the installed checkout may differ:

```bash
runpod-vllm --help
runpod-vllm plan --help
runpod-vllm deploy --help
runpod-vllm list --help
runpod-vllm status --help
runpod-vllm wait --help
runpod-vllm smoke-test --help
runpod-vllm destroy --help
```

## RunPod REST API version

RunPod retired REST API v1 (`https://rest.runpod.io/v1`) on 2026-11-15. REST API v2 (`https://api.runpod.io/v2`) is the current surface and the automatic CLI default since 2026-11-15.

- New deployments default to `v2` (`https://api.runpod.io/v2`), so no `--api-version` flag is needed. You can still pass `--api-version` (a global option, placed before the command) or set `RUNPOD_API_VERSION` when targeting a custom endpoint.
- Run `plan` before `deploy`; the v2 payload uses nested `gpu`, `image`, `disk`, `entrypoint`, `cloud`, and `mounts` fields.
- With v2, `--volume-gb` must be `0` or at least `10`.
- `deploy` records `api_version` in state. `status` and `destroy` reuse it unless `--api-version` is passed, and automatically move legacy v1 state files (including files written without `api_version`) to v2 using the same Pod ID.
- Do not pass `--api-version v1` against RunPod now that v1 is retired.
- `--api-url` does not change the version. Pair a custom v2 URL with `--api-version v2`.

## Plan-first workflow

1. Read the request and classify the intended action as offline, read-only network access, billable creation, endpoint validation, or destructive teardown.
2. Check installation, CLI help, working directory, selected `--state-path`, and credential presence. Never reveal credential values.
3. Gather the exact model revision, GPU profile and count, tensor parallel size, context length, dtype, quantization, storage, cloud type, image tag, and data center constraints.
4. Run `plan` with the proposed deployment options. Confirm its header says `offline; no API call`. Review the redacted payload and correct validation errors.
5. For `deploy`, restate the reviewed model, GPU count and profile, state path, and billable effect. Continue only with current, unambiguous authorization. Prefer the interactive confirmation.
6. Preserve the state file immediately. Record its path in the operational handoff, but do not copy its contents into prompts or shared logs.
7. Run `status`, then `wait`, then `smoke-test`. Readiness alone is not an inference that generation works.
8. When authorized to tear down, verify the exact target, run `destroy`, confirm the CLI reports verified absence, and verify matching state was removed. Use `list` for a final provider-side check.

## Credential handling

- Obtain `RUNPOD_API_KEY`, optional `HF_TOKEN`, and optional endpoint bearer tokens from the user's approved secret manager or an already prepared process environment.
- Never ask the user to paste a credential into a prompt. Never place a value in commands, `--env`, examples, source files, commits, issue text, chat, terminal transcripts, or logs.
- Never run `env`, `printenv`, `set`, `set -x`, or shell tracing around credential-bearing commands. Do not echo variables or embed them in URLs.
- If interactive entry is necessary, use a silent input facility that leaves no value in shell history, then export only into the current process. Do not capture the terminal session.
- Prefer process environment variables. If the user explicitly selects `--env-file`, require an ignored, local file with restrictive permissions; never inspect or print its values. The process environment overrides the file.
- `HF_TOKEN` is sent into the Pod only when present. Treat enabling `--trust-remote-code` as a separate code-execution decision, not as a credential requirement.
- Pass only the endpoint token variable name to `--bearer-token-env`; never pass its value. Rotate any credential exposed in a prompt, log, history, or commit.

## State and resource lifecycle

- Default to `.runpod-vllm-state.json`. Use one distinct `--state-path` per Pod when operating multiple deployments.
- Treat state as the teardown anchor. It contains the Pod ID, model, port, API URL, and derived endpoint URLs, but no credentials.
- Do not overwrite existing state. If `deploy` reports that state already exists, inspect that Pod or select a deliberate new state path.
- After creation, verify the state file exists and is not tracked by Git. Do not manually edit or delete it while the Pod may exist.
- If creation succeeds but state saving fails, the CLI prints an exact recovery command containing the returned target ID. Treat this as an active billable partial deployment. With explicit cleanup authorization, verify the target using `list`, then run the printed `destroy --pod-id ...` recovery command promptly.
- `wait` succeeds only when `/health` returns HTTP 200 and `/v1/models` returns at least one model ID. A running Pod is not necessarily a ready model server.
- Run `smoke-test` after readiness. It requires a response containing `choices` from `/v1/chat/completions`.
- `destroy` treats an already absent Pod as success. It retains state when deletion verification times out and removes matching state only after provider absence is confirmed.

## Destructive target verification

Before `destroy`:

1. Resolve the selected global `--state-path` and confirm it is the intended deployment's state file.
2. Run `status` and `list`. Match the state-recorded ID, Pod name, model context, and requested environment to the user's exact target.
3. If `--pod-id` is required for state-write recovery, obtain it only from the CLI recovery output or a carefully matched `list` result. Never guess, shorten, or reuse an ID from another deployment.
4. State the exact target and irreversible termination effect to the user. Require current authorization.
5. Prefer interactive `destroy`. Use `--yes` only for explicitly approved unattended cleanup.
6. Require the output `verified absent`. If verification times out, retain state, inspect again, and retry. Do not report cleanup complete while the Pod remains or its status is unknown.

## GPU and model sizing

Treat every profile as an API identifier, not a compatibility guarantee. Before deployment, consult primary documentation for the exact checkpoint and selected vLLM image. Consider weight precision and quantization, KV cache growth with context and concurrency, dtype support, reasoning parsers, trusted code, tokenizer behavior, tensor parallel support, GPU interconnect, container disk, volume size, and host RAM.

Start with the smallest operational context that meets the request and a tensor parallel size supported by the model. If increasing GPU count, keep GPU count divisible by tensor parallel size. Inventory changes continuously. Removing a data center restriction or changing a GPU profile changes placement behavior and must be reviewed in a new offline plan. Never promise that a configuration will fit, start, or be available.

## Troubleshooting decision tree

Follow the first matching branch:

1. **CLI or validation error before network access**
   - Run the relevant `--help` and then `plan`.
   - Correct the exact reported issue: model or revision syntax, unsupported GPU, tensor parallel divisibility, disk or memory bounds, context bounds, dtype, KV cache dtype, port, cloud type, data center format, environment syntax, or an unpinned image.
2. **`RUNPOD_API_KEY is required`**
   - Check presence without printing it. Confirm the intended process environment or explicit global `--env-file` is selected. Rotate the key if exposed.
3. **`State already exists`**
   - Do not overwrite it. Run `status`; destroy the recorded Pod only when authorized, or choose a separate `--state-path` for an independently approved deployment.
4. **RunPod request failure or HTTP error**
   - Preserve the redacted diagnostic. For authentication errors, verify secret source and scope without printing it. For unavailable inventory, reconsider GPU profile or data center restrictions and generate a new plan. For transport failures, verify connectivity and the trusted API URL before retrying.
5. **Pod exists but `wait` times out**
   - Run `status`. Inspect provider-side Pod and container logs without copying credentials. Look for gated checkpoint access, insufficient disk, incompatible model or image revision, unsupported quantization, out-of-memory errors, or excessive context. Adjust one cause at a time and re-plan before any replacement deployment.
6. **Model does not fit**
   - Consider a shorter `--max-model-len`, compatible quantization, supported dtype or KV cache dtype, compatible tensor parallel configuration, or another GPU profile. Verify against exact checkpoint and vLLM documentation; do not guarantee the next choice.
7. **Smoke test returns HTTP 401 or 403**
   - Confirm the endpoint bearer token is present under `VLLM_API_KEY` or the selected `--bearer-token-env` name. Never place the token on the command line.
8. **Smoke test has invalid JSON or no `choices`**
   - Confirm the base URL, served model ID, OpenAI-compatible route, and server logs. Re-run `wait` before retrying.
9. **State is missing after creation**
   - Treat billing as active. Use `list` to identify the exact target. With explicit authorization, use `destroy --pod-id` and verify absence.
10. **Deletion verification times out**
    - Keep the state file. Re-run `status`, inspect provider state, and retry `destroy` with reviewed verification timing if needed. Escalate if provider state remains ambiguous.

## Common pitfalls

- Putting global options after the subcommand instead of before it.
- Assuming `plan` reserves inventory or proves a model fits.
- Passing credentials through `--env`, command arguments, copied transcripts, or debug tracing.
- Using `--yes` without a separately established billable or destructive authorization.
- Reusing one state file for multiple Pods or deleting state before verified absence.
- Treating Pod `RUNNING` status as vLLM readiness or skipping the generation smoke test.
- Setting tensor parallel size greater than GPU count or to a value that does not divide GPU count.
- Using an image tagged `latest`, enabling remote code without review, or guessing a quantization method.
- Restricting data centers without checking changing inventory.
- Reporting cleanup complete after only a DELETE response, rather than verified absence.

## Copy-pasteable recipes

### Offline planning

```bash
runpod-vllm plan \
  --model ORG/MODEL \
  --gpu A40 \
  --gpu-count 1 \
  --tensor-parallel-size 1 \
  --max-model-len 8192
```

### Approved deployment

Run only after the current request authorizes this reviewed billable configuration and required credentials are securely present in the process environment:

```bash
runpod-vllm --state-path .runpod-vllm-state.json deploy \
  --model ORG/MODEL \
  --gpu A40 \
  --gpu-count 1 \
  --tensor-parallel-size 1 \
  --max-model-len 8192
```

### Inspection

```bash
runpod-vllm list
runpod-vllm --state-path .runpod-vllm-state.json status
```

### Endpoint validation

```bash
runpod-vllm --state-path .runpod-vllm-state.json wait \
  --timeout 900 \
  --interval 5
runpod-vllm --state-path .runpod-vllm-state.json smoke-test \
  --timeout 30
```

For an authenticated endpoint, securely preload the token under the selected variable name and pass only that name:

```bash
runpod-vllm --state-path .runpod-vllm-state.json smoke-test \
  --bearer-token-env VLLM_API_KEY \
  --timeout 30
```

### Verified teardown

Run only after status and list output match the exact target and the current request authorizes termination:

```bash
runpod-vllm --state-path .runpod-vllm-state.json status
runpod-vllm list
runpod-vllm --state-path .runpod-vllm-state.json destroy
runpod-vllm list
test ! -e .runpod-vllm-state.json
```

## Verification checklist

- [ ] Run from the intended repository and confirm `runpod-vllm --help` matches this reference.
- [ ] Confirm Python 3.11 or newer and required credential presence without printing values.
- [ ] Select one explicit state path and verify it does not conflict with another deployment.
- [ ] Run the exact proposed configuration through offline `plan` and review the redacted payload.
- [ ] Confirm current user authorization before `deploy`; record no secrets in command history or logs.
- [ ] Confirm state exists after creation and remains untracked by Git.
- [ ] Run `status`, receive successful `wait` readiness, and pass `smoke-test`.
- [ ] Before `destroy`, match the exact state-recorded target against `status`, `list`, and the user's request.
- [ ] Receive `verified absent`, confirm matching state removal, and verify the target is absent from `list`.
- [ ] Report partial failures and retained state; never claim success from an unverified provider state.

## Repository documentation

- [README](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/README.md)
- [Quickstart](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/quickstart.md)
- [Configuration](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/configuration.md)
- [Lifecycle and teardown safety](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/lifecycle.md)
- [Security model](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/security.md)
- [Troubleshooting](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/troubleshooting.md)
- [Architecture](https://github.com/1solomonwakhungu/runpod-vllm-deployer/blob/main/docs/architecture.md)
