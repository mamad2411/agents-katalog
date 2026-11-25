---
name: agent-access
license: MIT
github: https://github.com/r266-tech/agent-access
description: "查询已有站点 CLI、登录态和应用入口；用于需要本机访问路线的任务。普通公开搜索和官方文档查询可直接使用现有工具。"
metadata:
  author: Agent Access 贡献者
  version: "0.2.5"
---

# Agent Access

需要本机访问路线时，查询已登记的能力：

```bash
agent-access list --target <query>
agent-access info <route>
agent-access contract --target <url>
```

按结果中的 `owner_refs` 使用对应工具或专用说明。安装状态、历史记录和 help
检查都不能证明当前账号或业务操作可用。`discovery_only` 路线由 owner 执行。

公开包的 `install.state` 区分可安装和只有契约的路线。内置 CLI 可通过
`agent-access run <route> -- <args>` 使用。安装和更新默认预览，显式 `--run`
才执行；执行目标必须唯一。`verify` 预览不表示验证已通过。

登录诊断见 [auth-sessions.md](references/auth-sessions.md)。核心不保存第二份
认证状态。路由查询字段见 [tool-routing.md](references/tool-routing.md)。
CLI 建设、目录维护和贡献准备按需读取 [README.md](README.md)。
