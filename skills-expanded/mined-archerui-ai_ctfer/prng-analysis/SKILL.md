---
name: prng-analysis
description: "连续或截断随机输出中的 LCG、MT19937、时间种子和线性状态分析，先确认生成器与输出条件。"
metadata:
  category: "crypto"
  keywords: "[\"PRNG\",\"随机数\",\"LCG\",\"MT19937\",\"624\",\"seed\",\"时间种子\",\"z3\",\"xorshift\",\"LFSR\"]"
  source: "{\"path\":\"src/ai_ctfer/prompts/skills/crypto.md\",\"section\":\"PRNG checklist:\",\"start_line\":113,\"end_line\":119,\"sha256\":\"5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777\"}"
  resources: "[\"references/checklist.md\"]"
---

# PRNG 状态与约束分析

## 适用前提
程序使用可复现的伪随机生成器，且存在输出、种子范围、部分位或相关状态线索。

## 工作流
1. 从源代码和采集方式确认具体生成器、输出位宽、顺序、截断方式及是否属于同一状态序列。
2. LCG 连续输出可用于恢复模数、乘数和增量；MT19937 的 624 个完整输出可用于重建状态，不能直接把同样结论套到截断输出。
3. 时间种子只在题目提供的合理时间窗口内枚举。Python random、C rand、Java Random、xorshift、LFSR 和 middle-square 需要对应实现模型。
4. 部分位或截断输出可按源代码建立 z3 模块方程，而不是先猜完整状态。

## 验证与失败处理
使用未参与恢复的实际输出检查预测，核对序列是否存在跳步、重置或会话切换。预测不符时回看模型和采样，不把拟合已知样本当作验证成功。

## 按需参考
`references/checklist.md` 仅收录现有 PRNG 段落；具体恢复脚本需基于当前题目实现，库中没有已验证实例。

## 来源
仅迁移现有 `src/ai_ctfer/prompts/skills/crypto.md` 的 113–119 行（PRNG checklist:）。完整原文件 SHA-256：`5071cdb2ea828c613f46c3482fd48fe4087a0a7959b6d42a5b7458308833d777`。来源是方法指导，未提供真实比赛题目或完成验证的运行记录。

