---
name: suian-zcode-app-mcp
description: ZCode 会话 MCP 的源码兼容入口，按请求定位安装、配置、会话或工件管理、GLM 额度及排障技能。
---

# ZCode 会话 MCP 入口

<!-- suian-zcode-app-mcp:plugin-root -->

本文件供源码安装和旧技能副本路由；原生插件自动发现 skills/ 中的独立技能。

插件根优先沿用上方注入的位置；原生安装读取插件清单的 rootPath，源码安装沿用已有 MCP 的 cli.mjs 所在目录或用户指定仓库。技能副本目录只有文档。

确定根后按请求只读取对应文件：

| 请求 | 技能 |
| --- | --- |
| 安装、升级或迁移旧 MCP 注册 | skills/setup/SKILL.md |
| 数据库、网关路径与客户端接入 | skills/configuration/SKILL.md |
| 检索、读取、改名、创建、发信、压缩、归档或置顶会话 | skills/sessions/SKILL.md |
| 定时任务查询、启停或派发轮内恢复官方 Cron 工具 | skills/automations/SKILL.md |
| 登记、查看、更新、清理当前会话工件或只读侧栏 | skills/artifacts/SKILL.md |
| GLM 套餐额度、卡片与许可后重置 | skills/glm/SKILL.md |
| 服务、来源定位或原 Host 故障 | skills/debug/SKILL.md |

基础十九个工具，宿主索引含 projects 表（3.16+）时另公布只读的 list_projects（共二十个）。工件使用插件自有 SQLite；公共模块和网关由公共插件提供，业务插件不复制其实现。
