---
name: argos-alarm
description: Manage Argos-Alarm rules — list/get/create/update/delete alarm rules by PSM or rule UID across CN/I18N/TTP/BOE regions. Use whenever the user mentions alarm rules, monitoring alerts, Argos alarm, wants to list who owns an alarm rule, check rule thresholds, or needs to register / modify / remove an alarm rule. Also trigger when investigating why a service is (or is not) alerting, comparing alarm rules across regions, or auditing alarm configuration by owner.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Argos-Alarm Agent

Manage Argos-Alarm rules across CN / I18N / TTP / BOE control planes.

> **When to Use**: List alarm rules for a PSM, inspect a rule's thresholds / receivers, or create / update / delete rules you own.

> **IMPORTANT Safety Rules**:
> 1. **MUST follow two-phase workflow for writes**: For `create_rule` / `update_rule` / `delete_rule`, always run the preview phase (without `confirm`) first, show the result to the user, and wait for explicit user approval before running with `"confirm": true`. NEVER skip the preview phase.
> 2. **NEVER change the target region**: Only operate on the exact `vregion` the user requested. If a region fails (timeout, network error, etc.), report the error — do NOT silently switch to a different region.
> 3. **NEVER auto-retry with different parameters**: If a call fails, report the failure and let the user decide what to do next. Do NOT silently switch PSM, uid, or rule body.
> 4. **Owner scope only**: This skill authenticates via the current `gdpa-cli login` user JWT. It only works for PSMs where the caller is the service-tree owner. Non-owner writes will return `41010403` — do NOT try workarounds, report to the user.

> **session_id（推荐带上）**：`--session-id` 技术上可省略，但**推荐一律带上**，把同一轮多次调用串到同一个 session 里便于回溯与日志关联。首次跑 `export SID=${SID:-$(gdpa-cli create-session)}`，后续命令统一用 `--session-id "$SID"`。

## Quick Start

```bash
# 1. List rules for a PSM
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"list_rules", "vregion":"sg", "psm":"ies.gdp.open_api", "limit":20
}'

# 2. Get one rule by uid
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"get_rule", "vregion":"sg", "uid":"43980985834928"
}'

# 3. Create a rule — MUST be two-phase
# Phase 1: preview (no confirm) — server receives zero bytes
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"create_rule", "vregion":"sg",
  "rule":{"name":"my-rule","attach_model":{"psm":"ies.gdp.open_api","vregion":"Singapore-Central","cluster":"default"}, "...":"..."}
}'
# >>> Show data.preview to the user, wait for explicit confirmation <<<

# Phase 2: ONLY after user confirms
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"create_rule", "vregion":"sg",
  "rule":{"...":"..."},
  "confirm": true
}'

# 4. Update / Delete — same two-phase pattern
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"update_rule", "vregion":"sg", "uid":"<uid>", "rule":{"level":"notice"}
}'   # preview
gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"update_rule", "vregion":"sg", "uid":"<uid>", "rule":{"level":"notice"},
  "confirm": true
}'   # execute

gdpa-cli run argos-alarm --session-id "$SID" --input '{
  "action":"delete_rule", "vregion":"sg", "uid":"<uid>"
}'   # preview, then re-run with "confirm": true
```

## Actions

| Action | Scope | Endpoint |
|---|---|---|
| `list_rules` | read | `POST /alarm/openapi/v3/rules/list` |
| `get_rule` | read | `GET /alarm/openapi/v3/rules/get` |
| `create_rule` | **write (two-phase)** | `POST /alarm/openapi/v3/rules/create` |
| `update_rule` | **write (two-phase)** | `POST /alarm/openapi/v3/rules/patch` |
| `delete_rule` | **write (two-phase)** | `POST /alarm/openapi/v3/rules/delete` |

## Input Parameters

### Required per action

| Action | Required |
|---|---|
| `list_rules` | `action`, `vregion` (filter by `psm` strongly recommended) |
| `get_rule` / `delete_rule` | `action`, `vregion`, `uid` |
| `create_rule` | `action`, `vregion`, `rule` |
| `update_rule` | `action`, `vregion`, `uid`, `rule` |

### Common

| Parameter | Type | Description |
|---|---|---|
| `vregion` | string | `cn` / `china-east` / `sg` / `us` / `ttp` / `euttp` / `boe` (aliases) or full name. See VRegion table |
| `psm` | string \| []string | Filter by PSM (one value currently enforced server-side) |
| `uid` | string | Rule UID for get / update / delete |
| `rule` | object \| string | Rule body for create / update. Accepts typed map or raw JSON string; uid in body for update must match top-level `uid` |
| `confirm` | bool | **Must be literal `true`** for create/update/delete to execute. Strings `"true"` / `1` / `"yes"` are ignored on purpose |

### `list_rules` filters (all optional)

| Parameter | Type | Notes |
|---|---|---|
| `check_vregion` | []string | `rule.check_vregions` filter, ≤20 |
| `cluster` / `executor` | []string | `balarm` / `canary` / `mscrawler` |
| `level` / `levels` | string \| []string | `notice` / `warning` / `critical`; singular & plural merge |
| `rule_alias` | []string | Up to 20 aliases |
| `status` | string \| []string | `normal` / `pause` |
| `suit_type` | []string | e.g. `bosun_raw` |
| `tags` / `tags_relation` | []string / string | `and` \| `or` (default `or`) |
| `limit` | int | Page size, server max 200 |
| `token` / `page_token` | string | Pagination cursor from previous `data.next_token`. **Not an auth alias** |
| `with_tsap` | bool | Include `extension.tsap` in response |

### Diagnostics

| Parameter | Type | Notes |
|---|---|---|
| `debug` | bool | Log outgoing HTTP body and raw envelope to stderr |

## Output Format

Top level always: `{success, action, vregion, data?, error?}`.

### `list_rules`
```json
{ "results": [ {...rule-record...} ], "next_token": "<cursor>", "total": 12 }
```

### `get_rule`
```json
{ "rule": { "uid": "...", "name": "...", "level": "warning", "...": "..." } }
```

### Write actions — preview (no `confirm`)
```json
{
  "requires_confirmation": true,
  "hint": "Re-run the same call with \"confirm\": true to execute this write.",
  "preview": { "action":"...", "method":"POST", "endpoint":"...", "vregion":"...", "body":{...}, "uid":"..." }
}
```

### Write actions — confirmed
```json
{ "uid": "<new-or-target-uid>", "detail": { /* server after-image, may be empty */ } }
```

## Two-Phase Workflow for Writes (MANDATORY)

**Every `create_rule` / `update_rule` / `delete_rule` call must go through both phases. NEVER skip Phase 1.**

1. **Phase 1 — Preview** (no `confirm` or `confirm=false`): Agent builds the HTTP request it *would* send (method, endpoint, body with uid injected), but does NOT call the server. `data.requires_confirmation=true` and `data.preview` surface the full plan. **Show `data.preview` to the user and wait for explicit approval before proceeding.**
2. **Phase 2 — Execute** (`"confirm": true`): Same input plus `confirm: true`. Agent re-validates, then calls the Argos API. Returns the new / target uid plus any `detail` the server provides.

**uid consistency**: For `update_rule`, if the body contains `uid` it must equal the top-level `uid`. Mismatch errors loudly on Phase 1 — you never reach Phase 2 with a bad uid.

## VRegion Mapping

| VRegion | Aliases | Alarm Gateway | JWT |
|---|---|---|---|
| `China-North` | `cn`, `china` | `alarm.byted.org` | CN |
| `China-East` | `china-east` | `alarm-china-east.byted.org` | CN |
| `Singapore-Central` | `sg`, `singapore`, `i18n` | `alarm-sg.tiktok-row.org` | I18N |
| `US-East` | `us`, `useast` | `alarm-us.tiktok-row.org` | I18N |
| `US-TTP` / `US-TTP2` | `usttp`, `ttp` / `usttp2`, `ttp2` | `alarm-us.tiktok-row.org` | TTP |
| `EU-TTP` / `EU-TTP2` | `euttp` / `euttp2`, `eu-ttp2` | `alarm-sg.tiktok-row.org` | I18N |
| `China-BOE` | `boe`, `cn-boe` | `alarm-boe.byted.org` | BOE |

> SG / US / EU traffic uses the external `tiktok-row.org` front-end because the
> internal LBs are private to the I18N control plane.

## Lark 群 / LarkBot 通知配置

告警通道、飞书群 / 应用机器人 / 自定义 webhook 的接入方式、`receiver_mode × lark_ids × follow_empty_receivers` 决策矩阵以及三个可复用示例 JSON 都在独立的 reference 文件里：

→ **[`references/lark-notification.md`](references/lark-notification.md)**

速查：不配也能发（回退到服务树 owner + oncall）；进群：`lark_ids` + `receiver_mode=override`；都收：`append`；真静默：`follow_empty_receivers=true` + `lark_ids=""`。

## Auth

User JWT via `gdpa-cli login`，按 vregion 自动选 CN / i18n / ttp site。所有读/写都走这条路径。**仅支持 owner 自己 PSM 的操作**；非 owner 写入（跨团队治理、批量注入）不在 skill 范围内。

JWT 失效时报 `authentication failed`，重新 `gdpa-cli login` 即可。

## Error Handling

### Agent-side errors

| Error | Cause | Solution |
|---|---|---|
| `action is required` | Missing `action` | Set one of the 5 supported actions |
| `uid is required for <action>` | `uid` missing for get/update/delete | Pass `uid` |
| `rule ... is required` / `rule body is not valid JSON` | Missing / malformed body for create/update | Pass a valid `rule` object or JSON string |
| `patch uid mismatch` | `update_rule` top-level `uid` disagrees with body.uid | Align them or drop body.uid |
| `unsupported vregion "..."` | Unknown vregion | Use a value from the VRegion table |
| `authentication failed` | JWT cache invalid/missing | Re-run `gdpa-cli login` |
| `requires_confirmation: true` in data | First write call without `confirm` | Show `data.preview` to user, then re-run with `"confirm": true` |

### Server-side business error codes

Errors surface as `argos_alarm API error (code=N): <message>` and the CLI tags them with an errcode category. Per the [official Argos-Alarm error doc](https://cloud.bytedance.net/docs/argos/docs/63a91dd0caaad3021d130a84/64748d21c1633d0223a24b43):

| error_code | Meaning | CLI tag | Action |
|---|---|---|---|
| `41010401` / `41010403` | Unauthenticated / unauthorized | `[AUTH-000]` | Re-run `gdpa-cli login`; verify you are the service-tree owner of the target PSM |
| `41010000` / `41010001` / `41010404` | Rule / event / generic resource not found | `[API-003]` | Check `uid` / `rule_id` — rule may have been deleted (soft-delete tombstones are still fetchable via `get_rule` but hidden from `list_rules`) |
| `41010429` | Rate limited | `[API-002]` | Exponential backoff; don't loop |
| `50000000` | Server internal error | `[API-001]` | Include `X-Tt-Logid` from debug logs when reporting to argos oncall |
| `41010400` / `41010422` | Request parameter invalid (incl. template validation) | `[API-004]` | Check `error_message` — common substrings: `already has the same rule expression`, `unknown archetype`, `deployUnits not found in ms-meta`, `should not be empty`, `num of level ... will exceed threshold` |
| `41010002` | Alarm event expired | `[API-004]` | Event is out of retention window |
| `-1` / unknown | Generic business error (subtype in `error_message`) | `[API-004]` | Match on `error_message` substring; see above for common ones |

> **Paas-gw gateway errors** (body shape `{"code":-1,"error":"..."}` on HTTP 4xx — e.g. `该用户 ... 无调用权限`, `该secret有误`) are also recognized by the codec and surface as `*ArgosAlarmError` with the HTTP-status-derived tag (`[AUTH-000]` for 401/403, `[API-003]` for 404, `[API-002]` for 429, `[API-001]` for 5xx). They're **not** silently swallowed.

## Notes

- **Read vs write**: reads run immediately; writes require Phase 1 preview + Phase 2 confirm. Never skip Phase 1.
- **`token`** is the `list_rules` pagination cursor, **never** an auth field. Pass `data.next_token` back as `token` to get the next page.
- **`rule` body**: accepts either a typed map or a raw JSON string; either way it is forwarded verbatim to Argos so the skill tracks server-side schema evolution automatically.
- **Soft delete**: `delete_rule` marks the rule `status=deleted`; `get_rule` still returns the tombstone, `list_rules` omits it.
- **Debug**: pass `"debug": true` to log the outgoing HTTP body and raw envelope on stderr — useful when filters unexpectedly return empty.
- **PSM scope**: skill is purpose-built for "owner manages their own PSM" use cases. High-QPS automation or cross-team governance should extend the skill with an explicit credential path instead of tunneling through the user JWT.
