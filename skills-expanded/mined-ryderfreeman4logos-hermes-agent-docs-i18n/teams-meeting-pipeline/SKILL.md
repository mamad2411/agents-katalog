---
name: teams-meeting-pipeline
description: Teams meeting summaries, job replay, Graph subscriptions.
version: 1.1.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [MSGRAPH_TENANT_ID, MSGRAPH_CLIENT_ID, MSGRAPH_CLIENT_SECRET]
  commands: [hermes]
metadata:
  hermes:
    tags: [Teams, Microsoft Graph, Meetings, Productivity, Operations]
    # Channel-gated: this pipeline only makes sense on the Teams gateway
    # channel (and in cron jobs, where its scheduled summary/replay work
    # actually runs). Hidden from every other session's skills index.
    session_platforms: [teams, cron]
    related_docs:
      - /docs/guides/microsoft-graph-app-registration
      - /docs/user-guide/messaging/teams-meetings
      - /docs/guides/operate-teams-meeting-pipeline
---

# Microsoft Teams 会议处理流程

当用户询问关于 Microsoft Teams 会议的摘要、文字记录、录像文件、待办事项、Graph 订阅信息，或与会议处理流程相关的任何操作问题时，均可使用此技能。该技能支持多种语言——下述触发条件仅为示例，并非完整列表。

所有面向操作人员的功能均通过终端工具执行 `hermes teams-pipeline` 子命令来实现。该处理流程并未新增专门的模型工具，CLI 才是其交互界面。

## 何时使用此技能

当用户需要执行以下操作时，可使用此技能：
- 撰写 Teams 会议摘要/提取待办事项/获取会议笔记
- 查看处理流程状态、查看已存储的会议任务或浏览近期会议记录
- 重新播放/运行那些失败或需要重新生成摘要的已存储任务
- 在更改环境或配置后验证 Microsoft Graph 的设置是否正常
- 排查“会议摘要始终未发送”或“没有新会议被导入”的问题
- 管理 Graph Webhook 订阅（创建、续订、删除、查看状态）
- 设置自动订阅续订功能（详见下文注意事项）

多语言触发条件示例（非完整列表）：
- 英语：「summarize the Teams meeting」、「pipeline status」、「replay job X」
- 土耳其语：「Teams meeting özetle」、「action item çıkar」、「toplantı notu」、「pipeline durumu」、「replay job」

## 先决条件

在使用该处理流程之前，请先确认以下配置已在 `${HERMES_HOME:-~/.hermes}/.env` 文件中设置完毕：

```bash
MSGRAPH_TENANT_ID=...
MSGRAPH_CLIENT_ID=...
MSGRAPH_CLIENT_SECRET=...
```

如果缺少任何必要项，请引导用户前往 `/docs/guides/microsoft-graph-app-registration` 中的 Azure 应用注册指南——在流水线能够正常运行之前，必须先完成 Azure AD 应用注册，并授予具备管理员权限的 Graph 应用权限。 

## 命令参考

### 状态查询与检查（从这里开始）

```bash
hermes teams-pipeline validate              # config snapshot — run first after any change
hermes teams-pipeline token-health          # Graph token status
hermes teams-pipeline token-health --force-refresh   # force a fresh token acquisition
hermes teams-pipeline list                  # recent meeting jobs
hermes teams-pipeline list --status failed  # only failed jobs
hermes teams-pipeline show <job-id>         # full detail of one job
hermes teams-pipeline subscriptions         # current Graph webhook subscriptions
```

### 重新运行 / 调试

```bash
hermes teams-pipeline run <job-id>          # replay a stored job (re-summarize, re-deliver)
hermes teams-pipeline fetch --meeting-id <id>   # dry-run: resolve meeting + transcript without persisting
hermes teams-pipeline fetch --join-web-url "<url>"   # dry-run by join URL
hermes teams-pipeline fetch --join-web-url "<url>" --organizer-user-id <id>   # organizer-scoped lookup (required for /meet/ short URLs)
```

### 订阅管理

```bash
hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllTranscripts \
  --notification-url https://<your-public-host>/msgraph/webhook \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"

hermes teams-pipeline renew-subscription <sub-id> --expiration <iso-8601>
hermes teams-pipeline delete-subscription <sub-id>
hermes teams-pipeline maintain-subscriptions            # renew near-expiry ones
hermes teams-pipeline maintain-subscriptions --dry-run  # show what would be renewed
```

## 常见问题的决策流程

- 用户询问“为何没有收到今日会议的摘要？”→ 首先执行 `list --status failed`，然后在对应行上执行 `show <job-id>`。如果该任务根本不存在，则需检查 `subscriptions` —— 可能是 webhook 已过期（详见下文注意事项）。
- 用户询问“设置是否正常？”→ 先执行 `validate`，接着是 `token-health`，最后是 `subscriptions`。若这三项均检测通过，则可安排一场测试会议，并通过 `list` 查看是否有新生成的记录。
- 用户询问“重新生成会议 X 的摘要”→ 先使用 `list` 查找任务 ID，再执行 `run <job-id>` 重新处理。如果仍失败，则执行 `show <job-id>` 查看错误信息，并使用 `fetch --meeting-id` 进行模拟处理。
- 用户询问“将会议 X 添加到处理流程中”→ 通常无需如此操作——该处理流程是基于订阅驱动的，而非针对单次会议。若用户希望汇总某次已结束的会议内容，可先使用 `fetch` 获取会议记录，待任务创建完成后再执行 `run`。

## 重要注意事项：Microsoft Graph 订阅有效期为 72 小时

Microsoft Graph 对 webhook 订阅设置了 72 小时的时间限制，且**不会自动续期**。如果未安排 `maintain-subscriptions` 任务，任何手动创建的订阅在 3 天后就会停止发送通知。

当用户反馈“昨天处理流程还能正常工作，今天却没有任何通知了”时：
1. 运行 `hermes teams-pipeline subscriptions` 命令——如果该命令的输出为空，或所有条目的 `expirationDateTime` 都是过去的时间，那就是问题所在。
2. 按上述方法使用 `subscribe` 命令重新创建订阅。
3. **立即通过 `hermes cron add`、systemd 定时器或普通 crontab 设置自动续订功能**。文档 `/docs/guides/operate-teams-meeting-pipeline#automating-subscription-renewal-required-for-production` 中介绍了这三种方案，其中12小时的间隔是较为安全的（相比72小时的限制还有6倍的缓冲时间）。

## 其他常见问题

- **转录内容尚未生成**。Teams 需要在会议结束后的一段时间才能生成转录文件。对刚结束的会议执行 `fetch --meeting-id` 命令可能会返回空结果。建议等待2-5分钟后再试，或者让 Graph webhook 自动处理数据的导入。
- **传输模式不匹配**。如果已生成摘要（`list` 命令显示成功），但内容并未出现在 Teams 中，请检查 `platforms.teams.extra.delivery_mode` 设置以及对应的目标配置（`incoming_webhook_url`、`chat_id` 或 `team_id`+`channel_id`）。写入程序会从 config.yaml 文件或 `TEAMS_*` 环境变量中读取这些配置。
- **Graph 应用权限问题**。虽然令牌获取成功（`token-health` 检测通过），但由于添加了权限但未重新获得管理员同意，Graph API 调用仍会返回 401/403 错误。此时需让用户再次登录 Azure 门户查看应用注册信息，并重新点击“授予管理员同意”。

## 相关文档

当用户需要比当前内容更深入的信息时，可引导他们查阅这些文档：
- Azure 应用注册操作指南：`/docs/guides/microsoft-graph-app-registration`  
- 完整流程配置指南：`/docs/user-guide/messaging/teams-meetings`  
- 运维操作手册（包括续期自动化、故障排查及上线检查清单）：`/docs/guides/operate-teams-meeting-pipeline`  
- Webhook 监听器配置指南：`/docs/user-guide/messaging/msgraph-webhook`
