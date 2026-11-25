---
name: observer-ward
description: 使用 ObserverWard（命令为 observer_ward）对明确范围内的 HTTP 目标进行 Web 应用、中间件、服务、版本与 CPE 风格指纹识别。用户需要服务指纹、技术栈识别、从 httpx/DNS/浏览器结果中交叉验证产品版本，或需要保留 probe、响应和证书证据时使用。
---

# ObserverWard 服务指纹识别

ObserverWard 的匹配结果用于决定下一步验证方向，不是漏洞存在或版本确认的充分证据。重要结论应与响应头、页面内容、TLS 证书、浏览器观测或其他工具交叉验证。

## 运行前

1. 读取 `../../tool-index.md` 确认 `observer_ward` 的实际路径与可用状态；不要猜路径。
2. 先执行本机帮助，以已安装版本的参数为准：

```powershell
observer_ward --help
```

3. 单个目标使用 `-t`/`--target`；目标清单使用 `-l`/`--list` 或 stdin。大清单必须写入任务输出目录。

## 执行原则

- 优先 JSON 格式，便于后续筛选和证据归档。
- 管道输出时启用静默模式，避免进度消息混入结构化结果。
- 只在需要原始请求/响应时使用 `--ir`，只在需要证书证据时使用 `--ic`；两者都会显著放大输出。
- 仅在排障或证据收集时启用 debug。
- 不启动 update、plugin、daemon、MITM、webhook、API server、MCP 或 Redis/asynq 模式，除非用户明确要求该工作流。

## 协作路径

```text
DNS / 资产输入 → httpx 存活与响应初筛 → ObserverWard 指纹
  → 浏览器或原始响应交叉验证 → 后续专项分析
```

- HTTP 存活、标题、重定向、TLS 与轻量技术栈初筛 → `pentest-tools` 的 httpx 参考。
- Cookie、页面流程、控制台或 CDP 网络证据 → `browser-automation/`。
- 已确认的组件、接口或认证逻辑 → 根据任务进入 `api-security/`、`js-reverse/` 或 `pentest-tools/`。

## 输出要求

记录目标、查询时间、实际命令、结果文件、匹配产品与版本、关键响应/证书/probe 证据、交叉验证状态与未确认项。
