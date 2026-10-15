---
name: aliyun-devops-cli
description: Set up and use the Alibaba Cloud CLI to call Yunxiao (云效 / Apsara Devops) OpenAPI. Use this whenever someone wants to install, configure credentials for, or run commands against Yunxiao/云效 — the Aliyun DevOps platform covering Codeup (repos), Flow (pipelines), Projex (projects/workitems), AppStack (apps), etc. — via the `aliyun devops` CLI. Trigger on phrases like "云效 CLI", "yunxiao", "aliyun devops", "配置云效", "流水线 CLI", "Codeup CLI", or any mention of the ALIBABA_CLOUD_YUNXIAO_* environment variables, even if the user doesn't say "skill". Do NOT use this for general Alibaba Cloud (ECS/OSS/RDS) AK/SK configuration — that uses `aliyun configure` profiles, which Yunxiao explicitly does NOT use.
---

# Yunxiao (云效) CLI setup & usage

## The one thing that trips everyone up

Yunxiao's data-plane account system is **different from the rest of Alibaba Cloud**. It does **NOT** use AK/SK profiles. Running `aliyun configure` and storing an AccessKey will **not** let `aliyun devops` commands authenticate.

Yunxiao authenticates with a **Personal Access Token (PAT)**, passed through environment variables (or per-command flags). Getting this distinction right is the entire battle — everything else is mechanical. When a user says "I configured aliyun but yunxiao commands fail", the cause is almost always that they ran `aliyun configure` instead of setting a PAT.

## Setup workflow

### 1. Install the Alibaba Cloud CLI + verify the devops plugin

Install the `aliyun` CLI for the user's OS (official guide: Windows / Linux / macOS), then confirm the Yunxiao plugin loads:

```
aliyun devops version
```

It should print something like `aliyun-cli-devops 0.5.0 (...)`.
- `aliyun: command not found` → CLI not installed, or installed but not on PATH (on Windows, refresh PATH by opening a new terminal after install).
- `devops` not recognized → the plugin didn't load (rare on recent versions); reinstall via the official installer.

### 2. Get a Personal Access Token (PAT)

From the Yunxiao console: avatar → 个人访问令牌 (Personal Access Token) → create new.
- Grant the **minimum** API scopes needed (e.g. only `flow-*` if the user works with pipelines).
- Set a reasonable expiry; avoid permanent tokens.
- **The token is shown only once, at creation.** Save it immediately — it cannot be viewed again.
- If it leaks, delete it right away.

### 3. Determine org type — this decides which env vars are required

Ask the user, or inspect their Yunxiao console URL:

- **中心版 (Central)** — unified endpoint `openapi-rdc.aliyuncs.com`. Needs `ACCESS_TOKEN` + `ORGANIZATION_ID`. No api-base-url.
- **Region 版** — per-instance endpoint. Needs `ACCESS_TOKEN` + `API_BASE_URL`. No organization-id.

| Env var | 中心版 (Central) | Region 版 |
|---|---|---|
| `ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN` | required | required |
| `ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID` | required | not used |
| `ALIBABA_CLOUD_YUNXIAO_API_BASE_URL` | not used | required |

The org-id is visible in the console URL (`organizationId=...`) or in org settings. The Region api-base-url is obtained from the console's 服务接入点 (service access point) page.

### 4. Set the credentials persistently

**Never paste the token directly on the command line** — it lands in shell history and process lists. Use environment variables instead. The exact persistence command differs by OS/shell — see `references/platforms.md` for Windows (registry or PowerShell `$PROFILE`) and macOS/Linux (shell rc files).

The rules that catch people, regardless of platform:
- Persistent env vars are read at **process start**. After setting them, **open a new terminal** — the old one will not see the change. (In PowerShell you can also reload with `. $PROFILE`.)
- In PowerShell, `$env:VAR = "..."` is **session-only**. For persistence use either `[Environment]::SetEnvironmentVariable("VAR","val","User")` (visible to all processes) or add a `$env:VAR = "..."` line to `$PROFILE` (PowerShell sessions only).

### 5. Verify with a real call

```
aliyun devops flow-list-pipelines --page 1 --per-page 5
```

Diagnose by the returned error:
- `InvalidAccessToken` / `Unauthorized` → token is wrong, expired, or the request lacks permission.
- `Organization not found` (or similar) → wrong `ORGANIZATION_ID`.
- `AccessDenied` / `Forbidden` → token was created without the relevant permission point; recreate it with the needed scope.
- Returns data → setup is complete.

## Common commands

```
aliyun devops --help                                          # full command list
aliyun devops codeup-list-repositories --page 1 --per-page 20 # list repos
aliyun devops flow-list-pipelines --page 1 --per-page 20      # list pipelines
aliyun devops projex-search-projects --page 1 --per-page 10   # ⚠ returns ALL public org projects, NOT "mine" — filter via --conditions; see references/commands.md (Projex)
# Trim output with JMESPath — list commands return a BARE array, so query from the root []
aliyun devops codeup-list-repositories --cli-query '[].{name:name,id:id}'
```

### Response shape — list commands return a BARE array

`aliyun devops` **list/search commands return a bare JSON array at the top level** (`codeup-list-repositories`, `flow-list-pipelines`, `projex-search-projects`, `base-list-organizations`, `packages-list-repositories`, …) — NOT wrapped in `{ "result": [...] }`. So `--cli-query` starts at the root with `[]`, never `result[]`:

```
aliyun devops flow-list-pipelines --cli-query '[].{id:pipelineId,name:pipelineName}'
```

`get-*` / single-resource commands return an object. If a `--cli-query` ever returns `null`, dump the raw output once (`aliyun devops <cmd> --page 1 --per-page 2`) to confirm the shape.

Module prefixes: `codeup-*` (repos), `flow-*` (pipelines), `projex-*` (projects/workitems), `app-stack-*` (apps), `base-*` (org/members/roles), `insight-*` (metrics), `packages-*` (artifacts), `test-hub-*` (testing).

## Looking up a command's semantics

~300 commands — don't try to remember their flags or semantics. When a command's behavior isn't obvious, climb this ladder; it stops you re-deriving the same thing every session:

1. **`<cmd> --help`** — start here. Local, instant, and version-accurate (it matches the installed plugin). But it often stops at the *name*: `--conditions  The conditions` confirms the flag exists and says nothing about its JSON shape.
2. **`references/commands.md`** — when `--help` is silent on *semantics* (JSON structures, enum values, counter-intuitive defaults, field-name traps), check the distilled notes here first. These are conclusions prior runs already paid for.
3. **Official docs online** — if step 2 is empty, fetch the one page you need: search `云效 <API名> 阿里云帮助文档` or open `help.aliyun.com/zh/yunxiao/developer-reference/...`. Read the single page; don't bulk-download.
4. **Write it back** — once you've cracked something non-obvious, distill it into `references/commands.md` (lead with the *why*, keep it short). Next session it's just step 2.

Two cautions:
- **Verify against the actual run — the docs lag the CLI.** The official `ListProjects` page still shows API `devops-2021-06-25`; the plugin ships `2026-05-25`. The command's `--help` and its real output are ground truth; reconcile the doc against them, don't copy it blindly.
- **Never bundle raw `--help` or doc pages into the skill** — `--help` is already local and version-perfect, and doc pages are too big and go stale. Bundle only the *distilled conclusion*.

## Per-command fallback (no env vars)

If the user can't or won't set env vars, each command accepts flags instead. This exposes the token in shell history, so prefer env vars:

```
# 中心版
aliyun devops flow-get-flow-tag-group --id 603 \
  --yunxiao-access-token=<token> --organization-id=<org-id>

# Region 版
aliyun devops flow-get-flow-tag-group --id 0 \
  --api-base-url=<url> --yunxiao-access-token=<token>
```

Flags map 1:1 to the env vars: `--yunxiao-access-token`, `--organization-id`, `--api-base-url`.

## Reference

- `references/commands.md` — routine day-to-day operations (list/get/create repos, pipelines, work items, apps, etc.) grouped by module, with copy-pasteable examples and confirmed flags.
- `references/platforms.md` — how to persist the three env vars on Windows / macOS / Linux, with the gotchas for each.
