---
name: unknown
description: "根据附件格式和服务行为路由未知类别的 CTF 题目，区分提取阶段与核心求解阶段。"
metadata:
  category: "unknown"
  keywords: "[\"unknown\",\"分类\",\"routing\",\"ELF\",\"pcap\",\"题目\",\"未知\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/unknown.md\",\"section\":\"# Unknown Category Skill\",\"start_line\":1,\"end_line\":24,\"sha256\":\"b2f82ff1949b7e4bf44477fc5db582699d7a66601344d80a3b1fb5e9b68a3044\"}"
  resources: "[\"references/checklist.md\"]"
---

# 未知题目分类

## 适用前提
题目 category 未知，或现有标签与附件、服务行为不一致。

## 工作流
1. 列出目录形态、文件大小和类型，读取题面、README、文件名与注释，针对可疑附件查看 `file` 和 `strings`。
2. 有 remote 时先识别协议：HTTP 可能是 Web 或附件分发；带 ELF 的原始 TCP 服务可能是 Pwn；数学问答可能是 Misc/Crypto。
3. 使用证据路由：输入校验程序先 Rev，确认内存破坏后 Pwn；应用/API 源码到 Web；n/e/c、密文、密钥、nonce 或签名到 Crypto；pcap、镜像、转储、媒体或归档到 Forensics；编码、pyjail、esolang、自动化到 Misc。
4. 加载对应类别 Skill。两类交织时先提取内部对象，再解决核心逻辑。

## 验证与失败处理
分类必须引用附件或服务观察，不能只依赖题目名。如果新证据否定分类，更新假设并切换 Skill，保留先前判断理由。

## 按需参考
`references/checklist.md` 保存来源中的完整类别信号。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/unknown.md` 的 1–24 行（# Unknown Category Skill）。完整原文件 SHA-256：`b2f82ff1949b7e4bf44477fc5db582699d7a66601344d80a3b1fb5e9b68a3044`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

