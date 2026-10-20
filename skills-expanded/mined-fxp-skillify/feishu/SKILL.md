---
name: feishu
description: 接入飞书开放平台（open.feishu.cn，国际版 Lark 为 open.larksuite.com）服务端 API 的使用手册——涵盖 tenant_access_token、app_access_token、user_access_token 三种凭证与 OAuth 授权、通讯录用户与部门、应用机器人发消息与收消息、自定义群机器人 webhook 签名、多维表格记录读写与筛选、审批实例与任务、飞书人事 CoreHR 员工与入职、事件订阅与回调（challenge、验签、解密、去重）、错误码频控与分页。当用户提到"飞书""Feishu""Lark""飞书开放平台""open.feishu.cn""lark-oapi""飞书机器人""群机器人 webhook""多维表格 API""Bitable""飞书审批""飞书人事""CoreHR""tenant_access_token"，或要求写代码调用上述任意飞书能力时，应主动使用本技能，不要凭记忆编造接口路径和字段，也不要套用钉钉、企业微信、Slack 的接口习惯。
---
# 飞书开放平台接入指南

飞书开放平台的服务端 OpenAPI：用应用凭证换 access token，再调用通讯录、消息、多维表格、审批、飞书人事等业务接口，
并通过长连接或 Webhook 接收事件。本 skill 的目标是第一次就写对鉴权、ID 类型、消息体格式和事件验签。
**本页只做分流与规则，字段表和示例在 `references/`。**

## ⚠ 验证状态

文档版：内容整理自 <https://open.feishu.cn/document/>（`llms.txt` 二级索引逐页 Markdown，157 页，抓取于 2026-09-11），
**未用真实凭证调用验证**。做过 20 次无凭证探测（伪造 app_id / token / webhook ID，不创建任何资源），覆盖换 token 接口、
OAuth v3 / v2 令牌端点、通讯录、发消息、自定义机器人 webhook、多维表格、审批（含 `www.feishu.cn` 上传路径）、飞书人事、
事件出口 IP、Lark 域名；结论在各 reference 中标「无凭证探测（2026-09-11）」。字段必填性、ID 类型混用的后果、分页上限、
频控响应头都**没有实测**。拿到凭证后按 `feishu-workspace/verification-plan.md` 补测；with / without skill 对照实验待凭证到位后进行。

## 当前事实

| 项 | 值 |
| :--- | :--- |
| Base URL | `https://open.feishu.cn/open-apis`；Lark 国际版 `https://open.larksuite.com/open-apis`（探测同路径可达）；OAuth 在 `https://accounts.feishu.cn` |
| 鉴权头 | `Authorization: Bearer <token>`；**少了 `Bearer ` 前缀服务端当作没带 token**（探测：`99991661`） |
| 三种 token | `tenant_access_token`（`t-`，应用身份，最常用）/ `app_access_token`（商店应用中转）/ `user_access_token`（OAuth，新端点下发 `eyJ...`） |
| 自建应用取 token | `POST /open-apis/auth/v3/tenant_access_token/internal` `{app_id, app_secret}` → **顶层** `tenant_access_token` + `expire`（秒，最长 7200）；剩余 <30 分钟再取才发新值 |
| user token | 授权页 `accounts.feishu.cn/open-apis/authen/v1/authorize` → `POST https://accounts.feishu.cn/oauth/v3/token`（索引里的 v2 端点已标历史）；响应字段 `access_token` / `expires_in`；`refresh_token` 一次性，需 `offline_access` |
| 最容易选错的字段 | `user_id_type`（默认 `open_id`，可 `union_id` / `user_id`）与 `department_id_type`（默认 `open_department_id`）；例外：飞书人事 `GET /corehr/v1/job_datas` 默认 `people_corehr_id` |
| 响应结构 | `{"code":0,"msg":"success","data":{...}}`，`code != 0` 即失败，不要用 `msg` 判断；排障用响应头 `X-Tt-Logid` |
| 官方 SDK | `pip install lark-oapi`（Python ≥3.7），`lark.Client` 自动获取并缓存 tenant_access_token |

## 照通用经验写容易错的地方（来自文档，未实测）

1. **换 token 失败 HTTP 仍是 200（无凭证探测证实）。** `app_id=test` → HTTP 200 + `{"code":10003,"msg":"invalid param"}`；
   自定义机器人 webhook 失败也是 HTTP 200。`raise_for_status()` 抓不到，一律判 body 的 `code`。
2. **路径或方法写错返回纯文本 404（无凭证探测证实，与文档不符）。** 不是文档列的 JSON `99991201` / `99991301`，
   直接 `resp.json()` 会抛解析异常；先判 `Content-Type`。
3. **两种机器人的消息体格式不同。** 应用机器人 `POST /im/v1/messages` 的 `content` 是 **JSON 字符串**，`receive_id_type` 在 query 且必填；
   自定义群机器人 webhook 的 `content` 是**对象**，卡片还要改放 `card` 字段。
4. **两套签名都不是常见的 HMAC(secret, payload)。** 自定义机器人：`HMAC-SHA256(key = timestamp + "\n" + secret, msg = 空)` 再 Base64，timestamp 为秒；
   事件 / 回调 Webhook：`sha256(timestamp + nonce + encrypt_key + 原始 body)` 的 hex，纯 SHA-256；解密 key 是 `SHA256(Encrypt Key)`、IV 取密文前 16 字节。
5. **所有用户 ID 跟着 `user_id_type` 走，默认 `open_id`。** 手里是工号式 user_id 却不带 `user_id_type=user_id`，会被当 open_id 查成"用户不存在"；
   open_id 跨应用无效（`99992361`）；返回 user_id 还要单独的字段权限。
6. **时间单位按接口变。** 多维表格日期写**毫秒**、筛选用 `["ExactDate","<毫秒>"]` 且按天生效；审批日期控件是 **RFC3339 字符串**；
   消息 `create_time` 毫秒而历史消息查询参数是**秒**；通讯录 `join_time` 秒。
7. **后台配置改完要发布应用才生效。** 机器人能力、API 权限、通讯录权限范围、事件订阅都要发版；审批事件还要对每个 approval_code 调
   `subscribe`；用 tenant_access_token 访问多维表格前要先把应用加为该表格的协作者。

## 我要做什么 → 读哪一份

| 我要做什么 | 读 | 核心 endpoint |
| :--- | :--- | :--- |
| 换 tenant / app / user token、OAuth 登录、商店应用、Lark 域名 | [`auth.md`](references/auth.md) | `POST /auth/v3/tenant_access_token/internal` · `POST accounts.feishu.cn/oauth/v3/token` |
| 查 / 建用户与部门、手机号邮箱换 ID、遍历组织架构 | [`contacts.md`](references/contacts.md) | `POST /contact/v3/users/batch_get_id` · `GET /contact/v3/users/find_by_department` · `GET /contact/v3/departments/:id/children` |
| 发消息、回复、传图片、收消息事件、自定义群机器人 webhook | [`messaging-bots.md`](references/messaging-bots.md) | `POST /im/v1/messages` · `POST /bot/v2/hook/:hook_id` |
| 多维表格建表、批量写记录、条件查询 | [`bitable.md`](references/bitable.md) | `POST /bitable/v1/apps/:app_token/tables/:table_id/records/batch_create` · `POST .../records/search` |
| 发起审批、同意 / 拒绝任务、订阅审批事件 | [`approval.md`](references/approval.md) | `POST /approval/v4/instances` · `POST /approval/v4/tasks/approve` · `POST /approval/v4/approvals/:code/subscribe` |
| 飞书人事查员工、待入职与完成入职、标准版花名册 | [`corehr.md`](references/corehr.md) | `POST /corehr/v2/employees/search` · `POST /corehr/v2/pre_hires` · `POST /corehr/v2/pre_hires/:id/complete` |
| 事件订阅与回调：长连接、challenge、验签、解密、去重 | [`events-callbacks.md`](references/events-callbacks.md) | `lark.ws.Client` 长连接 · Webhook 回调地址 · `GET /event/v1/outbound_ip` |
| 错误码、频控、分页、IP 白名单、重试 | [`errors-and-limits.md`](references/errors-and-limits.md) | HTTP 429 + `x-ogw-ratelimit-reset` · `page_token` / `has_more` |

本 skill 不覆盖：云文档 / 电子表格 / 知识库 / 云空间、日历、视频会议、考勤、任务、邮箱、招聘、OKR、绩效、Payroll、
飞书卡片搭建细节、群组管理（仅含群列表）、网页应用与 JSAPI、三方审批、aPaaS / Aily / MCP 等——文档见
<https://open.feishu.cn/llms.txt> 下对应的二级索引 `llms-docs/zh-CN/llms-*.txt`。

## House rules

- 基址与凭证走环境变量（如 `FEISHU_BASE`、`FEISHU_APP_ID`、`FEISHU_APP_SECRET`）；webhook 地址和签名密钥同样当密钥管，不进仓库。
- 缓存 tenant_access_token，按 `expire` 计算，剩余 30 分钟内再刷新；商店应用按 `tenant_key` 分开缓存。
- 每个请求判 `code == 0`；失败时记录 `X-Tt-Logid` 与 `error.troubleshooter`。
- 选 token 先看接口文档「请求头 Authorization」：搜索用户、搜索部门、`authen/v1/user_info` 只收 user token；审批、飞书人事基本只收 tenant token。
- 写接口带幂等键：消息 `uuid`、多维表格 `client_token`（uuidv4）、审批 `uuid`、通讯录 `client_token`。
- 分页一律 `has_more` + `page_token`，首次不传 token；各接口上限不同（通讯录 50、多维表格查询 500、待入职查询 10）。
- 事件在 3 秒内回 HTTP 200、业务异步处理，按 `event_id` / `uuid` / `message_id` 去重。
- 权限与范围类错误（`99991672`、`99991679`、`40004`、`41050`、`230013`）不重试：开权限、改范围、发布应用。

## 文档自相矛盾 / 未说明之处（⚠ 汇总）

reference 中共 42 处 ⚠、2 处 `<!-- Gap -->`（`grep -n '⚠\|<!-- Gap' references/*.md` 可定位）。要点：

- **auth.md**：用 PKCE 时换 token 该走 v2 还是 v3（授权码页与 v2 迁移说明矛盾）；`99991671` "must start with t-/u-" 与新版 `eyJ` token 矛盾；
  SDK 配置表把 `app_ticket` 描述成 app_access_token；Lark 的 OAuth 域名、SDK 的 Lark 常量名、`open.larkoffice.com` 的关系、换 token 各失败码的触发条件均未说明。
- **messaging-bots.md**：接收消息去重用 `message_id`（事件页）与总览"用 event_id"不一致；webhook 失败码 `19001` 未收录；批量发送、上传文件字段未展开。
- **bitable.md**：记录上限"开放平台无额外限制"与错误码 `1254103`"限制 20,000 条"矛盾；关联字段写入是数组还是 `{link_record_ids}` 两页写法不同；batch_get 的 `user_id_type` 默认值与 `record_ids` 上限未说明。
- **approval.md**：上传文件响应字段、转交目标人字段、`instances/query` 过滤组合约束未抓全；明细 / 请假等复杂控件未展开。
- **corehr.md**：缺数据权限时的表现、`job_datas` 的 `page_size` 上限未说明；添加人员 / 待入职的必填性以租户档案配置为准；待入职事件 event_type 未抓取。
- **events-callbacks.md**：签名时间戳的容忍窗口未说明；app_ticket 事件结构未抓取。
- **errors-and-limits.md**：两处 Gap——路径不存在、方法不对都返回纯文本 404，不是文档所列 `99991201` / `99991301`。

## 目录结构

```
feishu/
├── SKILL.md
├── references/  auth · contacts · messaging-bots · bitable · approval · corehr · events-callbacks · errors-and-limits
└── evals/evals.json
```

内容整理自 <https://open.feishu.cn/document/>（抓取于 2026-09-11）。实际调用报错时优先信任 API 的真实返回。
