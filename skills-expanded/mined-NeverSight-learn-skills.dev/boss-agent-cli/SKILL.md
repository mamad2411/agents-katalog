---
name: boss-agent-cli
description: AI Agent 专用的 BOSS 直聘本地辅助 CLI。通过 boss schema 自描述能力，stdout 只输出 JSON 信封；默认低风险模式只做本地辅助、只读优先、用户主动触发。当用户需要搜索职位、按福利筛选、整理候选岗位、查看职位详情等求职辅助时使用本技能。
license: MIT
compatibility: 需要本机可执行 boss CLI（uv tool install boss-agent-cli，Python>=3.10）；浏览器辅助登录需 patchright install chromium；真实查询需可访问 zhipin.com 且用户本人完成登录。
---

# boss-agent-cli

> AI Agent 专用的 BOSS 直聘本地辅助 CLI。默认低风险模式只做本地辅助、只读优先、用户主动触发，不自动触达、不批量操作、不抓取平台数据。

## Install

### Skills CLI

```bash
npx skills add can4hou6joeng4/boss-skill
```

### CLI（本技能的运行依赖，未安装时先执行）

```bash
uv tool install boss-agent-cli
patchright install chromium  # only needed for browser-assisted login
```

## First Minute

按这个顺序跑，不需要先读完整文档：

```bash
boss doctor
boss schema
boss status
boss login   # only if status reports AUTH_REQUIRED / AUTH_EXPIRED
```

完成标准：

- `boss doctor` 返回 `ok=true`，或给出可执行的 `error.recovery_action`。
- `boss schema` 返回当前命令、参数、平台和错误码自描述——它是能力真源，不要硬编码命令表。
- `boss status` 返回当前登录态；未登录时由用户主动执行 `boss login`（扫码/浏览器交互，Agent 不可代替）。

## Safe Candidate Loop

求职者侧默认只推荐这个低风险闭环：

```bash
boss schema
boss search "Golang" --city 广州 --welfare "双休,五险一金"
boss detail <security_id>
boss shortlist add <security_id> <job_id>
```

规则：

- 先调用 `boss schema`，不要硬编码完整命令表。
- 只解析 stdout 的 JSON 信封；stderr 只当日志和进度信息。
- `ok=false` 时读取 `error.code` 和 `error.recovery_action`，不要猜测恢复步骤。
- `--welfare` 是核心筛选能力，适合用于低风险职位搜索和本地整理。
- 投递、打招呼、沟通、交换联系方式等动作回到平台官网由用户手动完成。

## Recruiter Boundary

招聘者侧默认只保留低风险职位管理入口：

```bash
boss schema
boss hr jobs list
boss hr jobs online <job_id>
boss hr jobs offline <job_id>
```

候选人搜索、投递申请、在线简历、附件简历、聊天记录、消息回复、联系方式交换等链路涉及个人信息或平台关系写入，默认低风险模式会返回 `COMPLIANCE_BLOCKED`。遇到这类结果时，停止自动化，回到官方页面由用户手动处理。

## Output Contract

所有命令都遵守同一 stdout JSON 信封：

```json
{
  "ok": true,
  "schema_version": "1.0",
  "command": "search",
  "data": [],
  "pagination": null,
  "error": null,
  "hints": {}
}
```

- `stdout`: 只输出 JSON 信封。
- `stderr`: 只输出日志和进度，受 `--log-level` 控制。
- exit code `0`: `ok=true`。
- exit code `1`: `ok=false`，必须读取 `error.code`、`error.recoverable`、`error.recovery_action`。

## Recovery

优先按错误信封恢复：

| Error code | Agent action |
|---|---|
| `AUTH_REQUIRED` / `AUTH_EXPIRED` / `TOKEN_REFRESH_FAILED` | 让用户主动执行 `boss login`，然后再跑 `boss status` |
| `BROWSER_KERNEL_MISSING` | 运行 `patchright install chromium` 后让用户重新登录 |
| `RATE_LIMITED` / `NETWORK_ERROR` | 等待后按 `recovery_action` 重试 |
| `INVALID_PARAM` | 修正参数后重试，例如城市、页码、福利关键词 |
| `AI_NOT_CONFIGURED` / `AI_API_ERROR` / `AI_PARSE_ERROR` | 按 `recovery_action` 配置或重试 AI 能力 |
| `ACCOUNT_RISK` / `COMPLIANCE_BLOCKED` | 停止自动化，使用平台官网或官方页面手动完成 |

不要把登录降级、浏览器通道或 CDP 当作规避风控的手段。

## References（本地，随技能安装）

- [references/usage-patterns.md](references/usage-patterns.md)：稳定使用模式——URL 复用网页筛选、福利关键词、本地整理与导出、AI 辅助链路、多平台注意、请求节律。

Agent 需要的一切真源都在本地：能力与参数查 `boss schema`，环境诊断跑 `boss doctor`，恢复动作读错误信封的 `recovery_action`。

## 延伸阅读（外部，仅供人类维护者，Agent 无需依赖）

- [Agent Quickstart](https://github.com/can4hou6joeng4/boss-agent-cli/blob/master/docs/agent-quickstart.md) · [Command Reference](https://github.com/can4hou6joeng4/boss-agent-cli/blob/master/docs/commands.md) · [Troubleshooting](https://github.com/can4hou6joeng4/boss-agent-cli/blob/master/docs/troubleshooting.md) · [CLI README](https://github.com/can4hou6joeng4/boss-agent-cli)

## License

MIT
