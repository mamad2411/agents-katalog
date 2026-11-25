---
name: misc
description: "Misc：编码层、pyjail、交互问答、自定义语言、游戏或 AI/ML 小题的分类与自动化。"
metadata:
  category: "misc"
  keywords: "[\"misc\",\"杂项\",\"encoding\",\"编码\",\"pyjail\",\"esolang\",\"QR\",\"game\",\"automation\",\"交互\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/misc.md\",\"section\":\"# Misc Skill\",\"start_line\":1,\"end_line\":45,\"sha256\":\"0a25f2d68e55b15bc1e636b3630347236fe81b89b342cb5d21196b9ea9d2c356\"}"
  resources: "[\"references/checklist.md\"]"
---

# 杂项分类与交互自动化

## 适用前提
当前证据尚未明确指向 Web、Pwn、Rev、Crypto 或 Forensics，或题目主要是编码、受限解释器与重复交互。

## 工作流
1. 识别附件类型、差异和样本规律；有服务则进行一次最小交互并保存 transcript。
2. 编码逐层解码，每一层都检查字节格式与变化；QR/条码先检查已有解码工具和图像变换。
3. Pyjail 根据版本和错误消息确认限制，再进行小型允许性检查；交互问答把读取、解析、计算和响应放进一个确定性脚本。
4. 自定义语言/VM 先识别语法和必要子集；游戏检查存档、校验、RNG 与脚本；AI/ML 文件检查格式、预处理、标签和配置。
5. 路线清晰后立即加载最接近的专项 Skill。

## 验证与失败处理
每层转换保留输入输出 artifact，避免把解码成功当作解题成功。交互脚本应验证服务器响应状态而不只是成功发送；排除的编码或解释器假设需保留失败依据。

## 按需参考
`references/checklist.md` 保存原编码和类别检查项。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/misc.md` 的 1–45 行（# Misc Skill）。完整原文件 SHA-256：`0a25f2d68e55b15bc1e636b3630347236fe81b89b342cb5d21196b9ea9d2c356`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

