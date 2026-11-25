---
name: team-windows-execution
description: Windows 与 PowerShell 工具的一致执行规则，覆盖实际环境探测、参数与编码、中文路径、后台任务、取消、依赖和错误恢复。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.0'
---

# Windows 执行

## 建立一次环境记录

从 DSH 实际运行环境确认当前目录、PowerShell 版本、程序绝对路径、Node/Python 版本、工具可用状态和目标权限。不能照抄其他会话或 Codex 的 PATH。安装在电脑上、DSH 可调用、成员可调用、完整流程通过是四个不同状态。

## 执行规则

1. 文件读取、搜索和编辑优先原生工具，勿用 shell 规避范围。受限目标下 pwsh/python/node/curl 的拒绝是执行权限限制；它们不会因为命令看起来只读而自动获准。
2. Windows 用当前提供的 pwsh 工具，参数按实际 schema 填写；不发不存在的 bash 工具。统一 PowerShell 语法，不能拼 Bash、cmd 与 PowerShell 的删除或移动命令。
3. 外部程序用明确入口及参数。复杂 JSON、脚本和正文写任务专属文件再传路径；不要把 JSON.stringify 结果当作 shell 转义。单引号字符串中的单引号需要双写；美元符和反引号在双引号里会解析。
4. 指定 workdir、超时、输出上限与 UTF-8。中文路径和空格用字面路径；不随任务改全局执行策略、PATH 或用户 Profile。模块需要交互时先说明并选择可管理入口。
5. 长任务走已提供的后台任务工具，保存 job ID、启动参数和实际进程；用 job_output/job_list 查询、job_kill 取消。等待程序事件，别反复模型轮询。
6. 递归删除、移动先解析绝对路径并核对其位于具体授权目录；使用原生 PowerShell LiteralPath，禁止跨壳拼接。共享成果经文件归属和发布步骤处理。

## 恢复与验收

相同参数或环境错误只诊断一次，记录可复用修复。区分启动失败、退出失败、超时、输出截断和已经继续后台运行。取消后检查进程和文件副作用，再续跑原任务。输出乱码先核对程序实际编码，不能把错误输出当空结果。

例子和故障表按需读 [详细参考](references.md)，实际参数始终以当前工具为准。
