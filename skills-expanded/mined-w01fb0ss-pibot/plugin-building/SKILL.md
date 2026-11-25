---
name: plugin-building
description: "使用随技能附带的 SDK 构建并自测 Pi Bot 连接插件。"
metadata:
  pibot-version: "6"
  pibot-name: "构建插件"
---

1. 明确要连接什么、要哪些读写操作；默认只读，写操作确认，不可逆操作默认关闭。在当前工作位置建立独立目录，把本技能的 template/ 复制进去，不在技能目录内开发。
2. 阅读 sdk/README.md 和 SDK 类型声明。用本地 sdk/pibot-plugin-sdk.tgz 安装：npm install --offline --ignore-scripts --no-audit --no-fund <tgz绝对路径>。不替换为联网包；离线依赖缺失时如实报告，不能宣称安装通过。
3. 按 SDK 的 createStdioServer 接口写工具，在输入边界校验，限制结果大小，设置 AbortSignal 和超时。stdout 只用于 MCP，诊断写 stderr，不含凭据或文件内容。
4. `.claude-plugin/plugin.json` 写名称、版本、描述，并固定声明 `pibotApp: true`；这是 Pi Bot 应用插件，不是技能包或普通 MCP。需要 secret 或 API key 时，不在聊天、plugin_install.config、源码、.env、命令参数、日志或插件包中收集；让用户去「连接 → 访问令牌」配置，使用现有访问令牌/secret 通道。.mcp.json 只作为应用运行时适配层声明必需联网域名，用 ${CLAUDE_PLUGIN_ROOT} 引用相对资源；不要单独交付 skills/。
   界面遵循 Pi Bot 风格：简洁克制、中文英文成对、浅色深色一致；配置字段使用用户可读标题和补充说明，枚举使用双语选项，互斥配置用条件显示，不把内部环境变量名直接展示给用户。
5. 用有界的 MCP 客户端启动 stdio 服务，完成 initialize、tools/list，再 tools/call 一个没有副作用的只读工具；核对错误输入。成功、失败、超时和取消都关闭 transport 与子进程。不用真实写入或不可逆工具测试账号。若只读工具需要访问外部 API，先核对 `.mcp.json` 和 `pibot.json` 是否声明了最小联网域名；命令沙箱本身没有该域名的联网授权时，不要把 `ENOTFOUND`、代理拒绝或 DNS 失败误判成插件代码错误，也不要为了测试关闭隔离。
6. 插件包保留可移植运行依赖，不含符号链接、开发机器绝对路径、秘密或无关文件。改完执行插件交付检查；任何失败先修复再安装。
7. 调用 plugin_install，传插件目录和非敏感配置。外部 API 的真实调用应在安装后的连接沙箱中，按插件声明的联网域名测试；如果当前测试环境没有该域名的网络权限，完成协议级自测后仍可安装，并明确标记“真实联网调用未验证”，不能把测试环境的网络失败包装成插件未安装，也不能改用沙箱外运行来绕过。只有收到成功收据才宣称安装成功；工具不可用或安全检查拒绝时原样报告。更新也走同一工具。
8. 返回 needs_setup 时，让用户先到「连接 → 访问令牌」新建或选择令牌，再到这个插件现有设置处完成配置；不在聊天索取密钥。交付名称、版本、工具、联网域名、自测和实际安装状态。
