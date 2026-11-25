---
name: team-adspower-browser
description: 在 DSH 中核对 AdsPower Local API、读取浏览器环境清单并按任务占用独立环境；仅在实际需要浏览器环境时加载。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.0'
---

# AdsPower 浏览器环境

本模块用于已安装的 AdsPower Global 与 DSH 的 `adspower` MCP。先确认任务目标、授权范围、环境所有者、可观察的数据以及交付位置。浏览器环境包含会话和身份数据；团队成员之间不能共用正在操作的同一环境。

## 工具确认

1. 先检查当前会话实际可见的 AdsPower MCP 工具及参数，选用它提供的状态检查入口；不猜测服务前缀或工具名称。读取部署中的实际端口，50325 只是常用默认值。连接失败先检查客户端和 Local API 状态，不反复启动或猜测密钥。
2. 需要既有环境清单时调用 `mcp__adspower__get-browser-list`，只保留任务所需的环境标识和版本，不把代理、Cookie 或身份数据写入团队消息。
3. 团队成员只具备 profile 明确列出的 MCP 工具。未看到工具时读取 `team_help` 和当前工具清单，记录“未接入”“接口离线”“缺少密钥”中实际出现的一项；不要改用命令行绕开成员限制。
4. 启动、停止、修改或删除环境前，先取得该环境的任务占用与授权；由具有对应工具权限的角色执行，并记录环境 ID、执行人和回执。没有对应工具时提交准备结果，等待队长分配。

## 环境实验

固定浏览器内核、扩展、窗口与时间设置、测试页面版本和采样时间。对 Canvas、WebGL、字体、音频、屏幕、语言、时区、Worker 与网络环境分别记录可观察值和不可观察项。一个变量一次变化，重复采样验证稳定性；网页结果不能代表整个设备或网络协议栈。

交付环境标识、测试版本、采样报告、差异与失败原因。状态接口成功只说明 Local API 可达，不能证明某个浏览器环境已准备好。

上游参考资料来自 [AdsPower/adspower-browser](https://github.com/AdsPower/adspower-browser) 的 `06dc59d65e094365139134d22e8eacb95ebedd62` 版本，按需读取 [官方技能](official/SKILL.md) 和其 `official/references/`，无需整套加载；该资料的 CLI 示例须按 DSH 当前 MCP 工具与权限重新核对。MIT 许可见 `official/LICENSE`。
