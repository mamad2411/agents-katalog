---
name: stata-runner
description: Use this skill when an AI agent needs to actually run Stata code locally to verify results, check whether a do-file runs, locate errors from Stata output, or execute repetitive data-processing steps. This is a reference-type entry pointing to the Stata AI Skill bundled with the "Stata All in One" VS Code extension; it is installed via the extension, not copied into this repository.
---

# stata-runner（引用型条目）

让 AI agent（Claude Code、Codex、Cursor 等）通过本地服务**运行 Stata 代码**并验证结果。本条目
**不复制入库**——它由王梓豪《Stata All in One》VS Code 插件附带的 `Stata AI Skill` 提供，学员经
插件一键安装即可获得。

## 何时用

- 让 AI 检查一段 do 文件是否能运行；
- 让 AI 根据报错信息尝试定位问题；
- 让 AI 辅助完成重复性的数据处理步骤；
- 让 AI 在本地环境中验证部分 Stata 命令。

## 安装

1. 在 VS Code 扩展市场搜索 `Stata All in One` 并安装（Cursor/Trae 等从
   [Open VSX](https://open-vsx.org/extension/ZihaoVistonWang/stata-all-in-one) 或
   [GitHub](https://github.com/ZihaoVistonWang/stata-all-in-one) 下载 `.vsix`）；
2. 按插件提示安装其附带的 `Stata AI Skill`；原生实现、开箱即用，Windows / macOS 均支持，
   即使卸载插件后 skill 仍可继续使用。

**独立版本**（不装插件）：把下面这段发给 agent 即可自动安装配置：

```text
请访问 https://raw.giteeusercontent.com/ZihaoVistonWang/Stata-AI-Skill/raw/main/guide/installation.md，安装并配置 Stata AI Skill.
```

## 输入输出约定

- 输入：一段 Stata 代码或一个 `.do` 文件路径；
- 输出：命令执行结果、错误信息、图形输出与运行耗时。
- 内置社区命令 `lianxh` 调用方式，可在连享会平台检索 Stata 相关文章、教程与示例。

## 最小使用示例

> 用 stata-runner 跑一下 `examples/ch01/ch01_main.do` 的第 1 节，确认能正常运行并把输出贴回来。

## 人工检查清单

- AI **不替代研究者判断**：回归设定、变量口径等仍需研究者自己把关；把它当"辅助调试工具"，
  不是"自动研究工具"。

## 来源与许可

- 来源：王梓豪《Stata All in One》VS Code 插件附带的 `Stata AI Skill`
  （<https://github.com/ZihaoVistonWang/stata-all-in-one>，<https://zihaowang.cn>）。
- 许可：插件与其 AI Skill 归原作者所有；本条目为**引用型**，不再分发其代码，仅提供安装指引与
  链接。作者已授权本课件引用其文档（作者为本期助教）。
- 最后验证日期：<!-- TODO: T7 彩排实测后填写 -->
- 本地化改动：无（引用型条目，不复制内容）。
