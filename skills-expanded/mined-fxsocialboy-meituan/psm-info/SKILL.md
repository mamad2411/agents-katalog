---
name: psm-info
description: Query PSM metadata information including code repository, SCM version, directory path, and deployment region coverage. Use when you already know a PSM and need repo or deployment metadata for that PSM.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# PSM Info Agent

Query PSM metadata for a known PSM: code repository URL, SCM version, directory path, and regional deployment details.

## When to Use

Use this skill when you already know the `psm` and want to:

- find the code repository
- check the SCM version
- inspect the repo subdirectory
- see which regions the PSM is deployed in

## Do Not Use

Do **not** use this skill:

- to infer or guess the `vregion` for `metrics`
- to infer or guess the `vregion` for `argos-query`
- as an automatic pre-step before every metrics or log query

If a metrics or logs request is region-sensitive and the user did not provide a region, ask the user directly instead of using `psm-info` to guess.

## Quick Start

```bash
gdpa-cli run psm-info --session-id "$SESSION_ID" --input '{"psm": "tiktok.story.api"}'
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `psm` | string | Yes | Service PSM identifier (e.g., `tiktok.story.api`) |

## Typical Follow-up

- "这个 PSM 对应哪个 repo？"
- "这个 PSM 在哪些 region 有部署？"
- "这个 PSM 当前 SCM/version 是什么？"

## Output Format

```json
{
  "success": true,
  "psm": "tiktok.story.api",
  "repo": "code.byted.org/tiktok/story_api",
  "repo_uri": "https://code.byted.org/tiktok/story_api",
  "scm": "v1.2.3",
  "dir": ".",
  "region": "cn",
  "regions": {
    "cn": {
      "psm": "tiktok.story.api",
      "repo": "code.byted.org/tiktok/story_api",
      "scm": "v1.2.3",
      "dir": "."
    },
    "i18n": {
      "psm": "tiktok.story.api",
      "repo": "code.byted.org/tiktok/story_api",
      "scm": "v1.2.4",
      "dir": "."
    }
  }
}
```

## Output Fields

| Field | Description |
|-------|-------------|
| `psm` | The PSM identifier |
| `repo` | Code repository path |
| `repo_uri` | Full repository URL |
| `scm` | SCM version string |
| `dir` | Directory path within the repo |
| `region` | Default region |
| `regions` | Per-region metadata (repo, scm, dir for each region) |

## Examples

```bash
# Query repo + deployment metadata for a known PSM
gdpa-cli run psm-info --session-id "$SESSION_ID" --input '{"psm": "tiktok.story.api"}'

# Query another PSM
gdpa-cli run psm-info --session-id "$SESSION_ID" --input '{"psm": "tiktok.user.service"}'
```

## Related Skills

- If you know the repo but do not know the PSM yet, use `repo2psm` first.
- If you want metrics or logs and the region is missing, ask the user for the target `vregion` instead of guessing.

## Debugging

```bash
DEBUG=1 gdpa-cli run psm-info --session-id "$SESSION_ID" --input '{"psm": "tiktok.story.api"}'
```

Logs saved to `/tmp/gdpa-agents/logs/`.
