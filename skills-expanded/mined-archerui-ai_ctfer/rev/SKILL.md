---
name: rev
description: "Rev 题目工作流：识别运行时、定位比较与数据变换、提取常量、重实现校验并验证候选。"
metadata:
  category: "rev"
  keywords: "[\"rev\",\"reverse\",\"逆向\",\"checker\",\"校验\",\"bytecode\",\"VM\",\"memcmp\",\"XOR\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/rev.md\",\"section\":\"# Reverse Engineering Skill\",\"start_line\":1,\"end_line\":65,\"sha256\":\"fccac49394886c286978e5656ca67926cd2676a7155f9f3bcc30c911f9c74572\"}"
  resources: "[\"references/checklist.md\"]"
---

# 逆向校验与变换还原

## 适用前提
需要理解可执行程序、脚本、字节码、自定义 VM、移动端文件或混淆校验逻辑。

## 工作流
1. 保存文件 hash，识别格式、语言/运行时，观察简单输入的输出及必要的调用信息。
2. 定位比较函数、校验分支和常量。无反编译器时用 `objdump`、符号/重定位表及局部 rodata 提取，不反复输出整份反汇编。
3. 先理解控制流再修改执行；将按字节变换、排列、PRNG mask 或编码按相反顺序还原，并在 Python 重实现。
4. 可表达为条件时使用现有 z3；自定义 VM 先恢复指令格式、字节码及模拟器，再解状态约束。工具不可用时记录限制。
5. 打包/混淆时确认 UPX、运行时解码或自修改线索，保存小型分析输出与提取文件。

## 验证与失败处理
用未修改的原校验器或等价已核对逻辑验证候选；补丁跳过分支不证明输入正确。核心变为密码分析、内存行为或文件提取时分别加载 Crypto、Pwn、Forensics。

## 按需参考
`references/checklist.md` 保存静态/动态分析、常见变换和打包分支。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/rev.md` 的 1–65 行（# Reverse Engineering Skill）。完整原文件 SHA-256：`fccac49394886c286978e5656ca67926cd2676a7155f9f3bcc30c911f9c74572`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

