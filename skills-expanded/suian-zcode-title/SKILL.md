---
name: suian-zcode-title
description: ZCode 自动命名的源码兼容入口，按请求定位安装、模型配置、命名控制或排障技能。
---

# ZCode 自动命名入口

<!-- suian-zcode-title:plugin-root -->

本文件供源码安装和旧技能副本路由；原生插件自动发现 skills/ 中的独立技能。

插件根优先沿用上方注入的位置；原生安装读取插件清单的 rootPath，源码安装使用用户已指定的仓库位置。不要把全局技能目录当作代码根。

确定根后按请求只读取对应文件：

| 请求 | 技能 |
| --- | --- |
| 安装、升级、迁移旧 Hook 或卸载 | skills/setup/SKILL.md |
| 命名模型、思考档位、SQLite 路径与超时 | skills/configuration/SKILL.md |
| 暂停、恢复、固定或解除固定标题 | skills/control/SKILL.md |
| 命名不触发、标题异常或通知问题 | skills/debug/SKILL.md |

手动改名使用会话 MCP。公共网关由公共插件维护，不在命名技能中复制配置流程。
