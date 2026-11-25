---
name: fbs-connector
description: Fbsir MCP connector guide for activation, entitlements, points, lebao, identity, scene packs,
  and logout.
metadata:
  source_frontmatter:
    description_zh: 福帮手 MCP 连接器：访问码激活、权益预检、积分/使用记录、乐包兑换/状态、身份、场景包与注销。
    description_en: 'Fbsir MCP connector: activate codes, check entitlements, handle points/usage records,
      redeem/check lebao, query scene packs, and logout.'
    version: 1.2.8.2
    author: 悟空共创（杭州）智能科技有限公司
    connector: fbs-connector
    source: connector
    disable: false
  imported_from: workbuddy
---

# 福帮手连接器 Skill

本 Skill 指导 AI 调用 `fbs-connector` MCP Server。连接器采用 `streamableHttp`，生产入口由同级 `mcp.json` 提供；连接器 ID、MCP server key 与 Skill 名称均为 `fbs-connector`。

## 调用原则

- 当前公网实时基线是 11 tools：`skill_activate`、`skill_precheck`、`skill_consume`、`skill_finish`、`skill_whoami`、`skill_logout`、`fbs_scene_pack_query`、`lebao_redeem`、`lebao_status`、`lebao_claim`、`lebao_drop`。
- 工具参数以线上 `tools/list` 返回的 JSON Schema 为准；不要把 `lebao_claim` 或 `lebao_drop` 降级成可选扩展。
- `skill_whoami` 用于查询当前身份、积分、权益和下一步引导；线上 `packCode` 应优先来自 `skill_whoami` 返回的权益包码或服务端确认包码。
- 当 WorkBuddy 已经能判断首轮入口时，应优先把 `entryId`、`scenePackId`、`assetType`、`intentFamily`、`profileSegment`、`personaCode`、`customizationLevel`、`entryPromptCode`、`entrySurface` 一并带给 `skill_whoami`，把首次有效触达写回福帮手运营系统。
- 专家包内的 `scenePackId` 属于本地专家团路由语义，不要直接当成线上 `fbs_scene_pack_query.packCode`。
- `sessionRef`、`sessionToken`、访问码、乐包签名字段属于敏感信息，不写入公开日志，不向服务端发送本地绝对路径。
- `skill_activate` 成功后，WorkBuddy 宿主里的后续鉴权工具优先传 `sessionRef`，不要复述长 `sessionToken`。`sessionToken` 仍可用于直连客户端，但必须当作 opaque 原始值处理：只从最近一次成功工具结果中结构化取值，不能手写、复述、纠错、换行、重编码或字段名修补；JWT payload 只要被改动一个字符，服务端就会按签名失效返回 `auth_session_invalid`。
- `fbs_scene_pack_query` 走最小参数集：只传 `packCode` 与可选 `sessionRef` / `sessionToken`。`scenePackId`、`entryId`、`assetType` 等属于 `skill_whoami` 语义提示，不要硬塞给 `fbs_scene_pack_query`。
- `skill_precheck` 一旦进入包码相关链路，就沿用最近一次服务端已确认的 `packCode`：优先取 `skill_whoami.nextAction.packCode`，其次复用刚刚成功的 `fbs_scene_pack_query.packCode`，不要在已知包码时省略 `packCode`，否则会落入 `schema_required_argument_missing`。
- `skill_consume` 与 `skill_finish` 不是固定成对调用：若 `skill_consume` 已返回成功且记录已结束，不要再补 `skill_finish`；`skill_finish` 只用于明确仍处于进行中或两阶段模式的使用记录。
- 若宿主缓存还显示旧工具数或旧 Skill 镜像，先提示刷新或重装连接器，不要伪造"已调用过"的结果。

## 工具说明

| Tool | 用途 | 关键参数 |
| --- | --- | --- |
| `skill_activate` | 使用访问码激活权益并获取会话 | `accessCode`、`skillCode`，可选 `hostType`；返回 `sessionRef` 与 `sessionToken` |
| `skill_precheck` | 检查会话、Skill/场景包权益与积分条件 | `sessionRef` 或 `sessionToken`、`skillCode`；命中包码链路时传服务端已确认的 `packCode` |
| `skill_consume` | 按场景包提交一次性消费或使用记录请求 | `sessionRef` 或 `sessionToken`、`usageRecordId`，其余字段按线上 Schema |
| `skill_finish` | 仅对仍处于进行中或两阶段模式的使用记录做结束更新 | `sessionRef` 或 `sessionToken`、`usageId`、`status` |
| `skill_whoami` | 查询当前用户、积分、权益和下一步引导；匿名状态也可提供公共引导 | 可选 `sessionRef` 或 `sessionToken`、`scenePackId`、`entryId`、`assetType`、`intentFamily`、`profileSegment`、`personaCode`、`customizationLevel`、`entryPromptCode`、`entrySurface` |
| `skill_logout` | 注销当前会话 | `sessionRef` 或 `sessionToken` |
| `fbs_scene_pack_query` | 查询场景包内容快照 | `packCode`，可选 `sessionRef` 或 `sessionToken` |
| `lebao_redeem` | 兑换乐包凭证为福帮手站内积分或权益 | `voucherId`、`sourceSkillCode`、`sourceEventCode`、`anonymousUserCodeHash`、`issuer`、`nonce`、`payloadEncoded`、`signature` |
| `lebao_status` | 查询乐包兑换与匿名绑定状态，纯读不发奖 | 至少提供 `voucherId`、`serverBindingId`、`anonymousUserCodeHash` 之一 |
| `lebao_claim` | 显式将已兑换乐包归并到当前会话用户并触发发奖 | `sessionRef` 或 `sessionToken`，另按 `voucherId`、`serverBindingId` 或 `anonymousUserCodeHash` 定位 |
| `lebao_drop` | 服务端里程碑投放的匿名乐包加速器 | `anonymousUserCodeHash`、`sourceEventCode`，可选 `scenePackId`、`intentFamily`、`profileSegment` |

## 典型流程

1. 激活访问码：调用 `skill_activate`，保存返回的 `sessionRef` 与 `sessionToken`；WorkBuddy 宿主链式调用优先用 `sessionRef`。
2. 使用前检查：调用 `skill_precheck` 或 `skill_whoami` 确认身份、积分、权益、当前阶段和下一步动作；若 `skill_whoami` 已返回 `nextAction.packCode`，后续 `fbs_scene_pack_query` 与 `skill_precheck` 共用同一个 `packCode`。WorkBuddy 首轮入口若已明确，还应把 `entryPromptCode` 与 `entrySurface` 一并写回。
3. 记录消费：先用 `skill_precheck(sessionRef, skillCode, packCode)` 确认当前包码是否可用；若走一次性消费，调用 `skill_consume` 成功即视为本轮使用已落账，不再补 `skill_finish`。只有服务端仍保留进行中记录或当前流明确为两阶段模式时，才调用 `skill_finish`。
4. 乐包闭环：调用 `lebao_redeem` 提交凭证；用 `lebao_status` 纯读查询进度；用户确认领取后再调用 `lebao_claim`。匿名状态若存在待领取提示，应先激活再领取。
5. 里程碑投放：在明确的可控流程中使用 `lebao_drop`，不要把它替代普通用户的常规兑换动作。
6. 场景包查询：调用 `fbs_scene_pack_query(packCode[, sessionRef])` 获取指定 `packCode` 的内容快照，不追加 schema 之外的路由字段。
7. 结束会话：用户要求退出或切换账号时调用 `skill_logout`。

## 福帮手·家族IP合伙人专项流程

当用户提到"福帮手·家族IP合伙人"、程序员/创业者 IP 起步、智能转型、家族发展、`.FBS`、乐包兑换或无注册绑定时，按以下顺序处理：

1. 若用户有访问码，优先 `skill_activate`，`skillCode` 使用 `iplib-core`。
2. 若用户仍在匿名态，先调用 `skill_whoami` 获取公共引导与可执行的下一步。
3. 如存在待领取或待绑定提示，优先完成激活，再进入领取动作。
4. 场景包查询时，优先使用 `skill_whoami` 返回的已解锁 `packCode`；本地 `scenePackId` 先作为专家团路由语义，不直接假定为线上包码。
5. 乐包凭证处理时，不上传本地绝对路径，不暴露完整签名，不把本地凭证说成权威账本。

## 错误处理

- 参数缺失或类型错误时，向用户说明缺少的字段，并重新收集后再调用。
- 返回"会话已过期或无效"时，请用户重新激活或重新连接福帮手。
- 若 `skill_activate` 刚成功而下一次鉴权工具立刻返回 `auth_session_invalid`，优先改用同次返回的 `sessionRef` 重试；若仍失败，再判断是否服务端过期或会话已被注销。
- 若 `skill_precheck` 返回 `schema_required_argument_missing`，优先补齐服务端已确认的 `packCode`，不要误判成会话失效或后端故障。
- 返回业务失败时，保留服务端 `failReason` 的含义，不自行推断积分、权益或乐包状态。
- 对非法 JSON 请求，若返回 `400` 与 `invalid_json`，按请求格式异常处理，不误报成服务端宕机。
