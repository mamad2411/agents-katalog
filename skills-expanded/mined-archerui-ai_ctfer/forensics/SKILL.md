---
name: forensics
description: "Forensics：识别归档、pcap、磁盘/内存、媒体和文档，保留原件并追踪每一步提取与解码。"
metadata:
  category: "forensics"
  keywords: "[\"forensics\",\"取证\",\"pcap\",\"archive\",\"PNG\",\"LSB\",\"disk\",\"memory\",\"stego\",\"音频\",\"隐写\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/forensics.md\",\"section\":\"# Forensics Skill\",\"start_line\":1,\"end_line\":70,\"sha256\":\"0c79bf358141c860073ce5f3dce74e5edea83b7976e0e8ad7cac778bcad19d4a\"}"
  resources: "[\"references/checklist.md\"]"
---

# 取证提取与来源追踪

## 适用前提
输入是磁盘或内存镜像、pcap、日志、归档、图片/音频、文档、core、Docker 层或待恢复文件。

## 工作流
1. 保存文件 hash，查看 magic、大小、metadata、归档目录和必要的 strings；在 `extract/` 中工作，保留原件。
2. 归档先列出内容，再按层保存提取结果；密码线索从题面、文件名、注释和字符串获取。
3. 按格式选参考分支：图像通道/LSB/尾随数据，pcap 会话/流重组，磁盘/内存痕迹，PDF/Office 对象，音频信号，Git/Docker 历史。
4. 工具缺失时使用原文列出的轻量替代（例如 tcpdump、strings、Python），脚本保存每次提取的输入、参数、输出和对应 artifact。
5. 解出的内部对象若是密文、可执行文件或 Web 源码，则切换到相应核心 Skill。

## 验证与失败处理
通过文件格式解析、重组顺序和可重复提取确认结果，保留来源链而非只记最终字符串。无结果时换有证据的通道/格式假设，不破坏原件。

## 按需参考
`references/checklist.md` 保存原文所有格式分支和工具替代方案。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/forensics.md` 的 1–70 行（# Forensics Skill）。完整原文件 SHA-256：`0c79bf358141c860073ce5f3dce74e5edea83b7976e0e8ad7cac778bcad19d4a`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

