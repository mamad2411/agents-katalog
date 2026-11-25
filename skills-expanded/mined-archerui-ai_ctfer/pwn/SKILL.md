---
name: pwn
description: "针对提供的 CTF 原生二进制与服务，检查保护、输入边界、崩溃和可复现交互，再验证挑战输出。"
metadata:
  category: "pwn"
  keywords: "[\"pwn\",\"binary\",\"ELF\",\"二进制\",\"checksec\",\"libc\",\"ROP\",\"heap\",\"format string\",\"内存\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/pwn.md\",\"section\":\"# Pwn Skill\",\"start_line\":1,\"end_line\":107,\"sha256\":\"967ec7de6a68a67036bcb22061bbdb8d73a7f0afbc670567189c08ad183c5fa4\"}"
  resources: "[\"references/checklist.md\"]"
---

# 原生程序与交互重放

## 适用前提
存在题目提供的可执行文件、配套库或声明的挑战服务，且需要理解原生输入处理或内存行为。

## 工作流
1. 用 `file`、`checksec`、`readelf`、`strings` 识别架构、PIE/NX/RELRO/canary、libc、链接方式和输入面。
2. 优先使用题目配套 loader/libc，以简单输入记录本地 prompt/response 基线。把菜单、收发边界和解析封装为确定性的脚本，再切换到 remote。
3. 按证据选择局部分析：崩溃与偏移、挑战自身的成功函数、格式字符串、堆对象生命周期、syscall 限制或整数/解析错误；具体检查按需读参考。
4. 已确认的偏移、泄漏和保护条件保存在脚本和结构化证据中，减少重复大范围探测。
5. 最终脚本非交互地读取挑战输出并退出；本地测试占位使用 `LOCAL_TEST_VALUE`。

## 验证与失败处理
先复现本地行为并核对地址、页对齐和配套 libc。远程结果须来自题目服务的实际响应；未得到结果时不能靠本地占位或成功退出推断完成。尚无输入原语时回到 Rev；HTTP 或密码 oracle 主导时换对应 Skill。

## 按需参考
`references/checklist.md` 保留原文各分析分支与脚本纪律。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/pwn.md` 的 1–107 行（# Pwn Skill）。完整原文件 SHA-256：`967ec7de6a68a67036bcb22061bbdb8d73a7f0afbc670567189c08ad183c5fa4`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

