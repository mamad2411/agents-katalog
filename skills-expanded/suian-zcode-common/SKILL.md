---
name: suian-zcode-common
description: ZCode 公共插件的源码兼容入口，按请求定位安装升级、连接配置或网关排障技能。
---

# ZCode 公共插件入口

<!-- suian-zcode-common:root -->

本文件供源码安装和旧技能副本路由；原生插件自动发现 skills/ 中的独立技能。

先确定公共根：沿用上方注入的位置，或使用 zcode plugins list --json 中公共插件的 rootPath。源码模式使用已确认的仓库公共目录。不要把仅有文档的全局技能目录当作代码根。

确定根后按请求只读取对应文件：

| 请求 | 技能 |
| --- | --- |
| 安装、升级、修复启动入口或卸载 | skills/setup/SKILL.md |
| 连接模式、端口、上游地址与重启生效 | skills/configuration/SKILL.md |
| 网关、启动任务、Desktop 或手机共存故障 | skills/debug/SKILL.md |

先完成全部配置，最后才交付用户择时重开的步骤。命名和 MCP 业务配置由各自技能处理。
