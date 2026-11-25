---
name: edit-idl
description: Workflow specification for IDL editing. If a task involves any IDL change, read and follow this document before execution.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# edit-idl

`edit-idl` is documentation-only orchestration guidance.

- Do not run `gdpa-cli run edit-idl --session-id "$SESSION_ID" --input ...`.
- Run the 3 runnable agents directly: `idl-pull` -> local edit -> `idl-commit` -> `idl-codegen`.

## Required Flow

1. Pull PSM-scoped IDL files.
2. Edit local IDL files.
3. Commit IDL changes via NextCode API.
4. Trigger code generation and check status.

## Branch Rule

Keep branch aligned across business code and IDL whenever possible:

- `idl-pull.branch == idl-commit.branch == idl-codegen.branch == business branch`
- Never commit IDL changes to `master` in this workflow.
- Even if `idl-pull` falls back to `master` for reading, `idl-commit.branch` must still use the target feature branch.
- If the feature branch does not exist in the IDL repo, `idl-commit` will create it automatically before commit.

## Working Directory Rule

## Important Constraint

- `base.thrift` must not be modified in this workflow.
- Modifying `base.thrift` may break downstream code generation.


Use a temporary output directory for IDL pull, for example:

- `/tmp/gdpa-idl/<task-id>`
- `.tmp/gdpa-idl/<task-id>`

After generation is verified, clean up the temporary directory.

## Command: `idl-pull`

### Input

- `psm` (required): target service PSM.
- `branch` (required): requested IDL branch.
- `output_dir` (optional): local output directory. Default: `.gdpa/idl`.

### Behavior

- Pulls only PSM-related IDL files, not the full repo.
- If requested branch is unavailable, automatically falls back to `master` and reports fallback.
- This fallback is read-only for pull. It does not change commit target branch.
- Writes metadata file `.gdpa_idl_meta.json` for commit stage.

### Output (key fields)

- `idl_dir`: local directory containing pulled IDL files.
- `meta_path`: metadata file path.
- `branch_used`: actually used branch.
- `fallback_msg`: branch fallback note (empty when no fallback).
- `files`: pulled IDL file list.
- `main_idl`, `repo_namespace`, `repo_type`.

### Example

```bash
gdpa-cli run idl-pull --session-id <sid> --input '{
  "psm": "tiktok.gdp.my_service",
  "branch": "feat/my-change",
  "output_dir": "/tmp/gdpa-idl/my-task"
}'
```

## Command: `idl-commit`

### Input

- `meta_path` (required if `idl_dir` absent): path to `.gdpa_idl_meta.json`.
- `idl_dir` (required if `meta_path` absent): pulled IDL directory.
- `branch` (required): target commit branch.
- `commit_message` (optional): commit message.

### Behavior

- Commits only IDL files (`.thrift` / `.proto`) via NextCode `CreateCommit`.
- Commit target branch must be your feature branch, not `master`.
- If branch does not exist, creates it first; if it exists, commits directly.
- After commit, creates BAM version.

### Output (key fields)

- `repo`, `repo_id`, `branch`, `branch_created`.
- `commit_id`, `commit_url`, `commit_message`.
- `changed_files`.
- `bam_result`, `bam_version`.

### Example

```bash
gdpa-cli run idl-commit --session-id <sid> --input '{
  "meta_path": "/tmp/gdpa-idl/my-task/.gdpa_idl_meta.json",
  "branch": "feat/my-change",
  "commit_message": "feat(idl): add request/response fields"
}'
```

## Command: `idl-codegen`

### Input

- `psm` (required for `action=run`).
- `branch` (required for `action=run`).
- `mode` (optional): `auto` / `overpass` / `gdp_local` / `gdp_remote` / `pb_builder`.
- `prod` (optional, `gdp_remote`): default `tiktok`.
- `service_type` (required for `gdp_remote`): `rpc` or `api` (`thrift -> rpc`, `proto -> api`).
- `action` (optional): `run` (default) or `query_status`.

### Mode Notes

- `auto`: detect and choose codegen mode.
- `overpass`: force overpass generation.
- `gdp_local`: run local `gdp update`. Requires GDP 本地开发模式 — service repo must contain `.gdp/rpcmodels.local.yaml`. The agent prechecks this and returns a structured error with fix commands when the file is missing.
- `gdp_remote`: trigger GDP remote task and wait.
- `pb_builder`: unsupported by tool trigger.

### `gdp_local` not configured

If `idl-codegen` returns an error stating `.gdp/rpcmodels.local.yaml` is missing, do not retry. Surface the error to the user and ask them to run one of:

- `gdp update --local-rpcmodels` — one-time switch to local dev mode
- `gdp update --idl ../path/to/your_service.thrift --save-local` — pin a local IDL path

### Network Jitter Handling (Overpass)

Overpass may occasionally return HTTP 200 with empty body on `CreateRepoConfig`
(client-side unmarshal error: `unexpected end of JSON input`).

`idl-codegen` detects this transient signature and retries internally up to 3 times.

### Output (key fields)

- `status`: `running` / `success` / `error`.
- `error`.
- `decision_mode`.
- `branch`.
- `repositories`.
- `mr_links`.
- `go_get_cmds`.
- `task_id`, `task_view_url` (for GDP remote when available).

### Example (run)

```bash
gdpa-cli run idl-codegen --session-id <sid> --input '{
  "psm": "tiktok.gdp.my_service",
  "branch": "feat/my-change",
  "mode": "gdp_remote",
  "prod": "tiktok",
  "service_type": "rpc"
}'
```

## Query Existing Task Status

Use `action: "query_status"`.

### GDP Remote

- Required: `mode="gdp_remote"`, `task_id`.

```bash
gdpa-cli run idl-codegen --session-id <sid> --input '{
  "action": "query_status",
  "mode": "gdp_remote",
  "task_id": 194697
}'
```

### Overpass

- Required: `mode="overpass"`, `psm`.
- Optional: `branch`.

```bash
gdpa-cli run idl-codegen --session-id <sid> --input '{
  "action": "query_status",
  "mode": "overpass",
  "psm": "tiktok.gdp.my_service",
  "branch": "feat/my-change"
}'
```

## Quick End-to-End Example

```bash
# 1) pull
gdpa-cli run idl-pull --session-id <sid> --input '{"psm":"tiktok.gdp.my_service","branch":"feat/my-change","output_dir":"/tmp/gdpa-idl/my-task"}'

# 2) edit local files under /tmp/gdpa-idl/my-task

# 3) commit
gdpa-cli run idl-commit --session-id <sid> --input '{"meta_path":"/tmp/gdpa-idl/my-task/.gdpa_idl_meta.json","branch":"feat/my-change","commit_message":"feat(idl): update"}'

# 4) codegen
gdpa-cli run idl-codegen --session-id <sid> --input '{"psm":"tiktok.gdp.my_service","branch":"feat/my-change","mode":"auto","service_type":"rpc"}'
```
